#!/usr/bin/env node
/**
 * a11y-scan.mjs - Mide accesibilidad real de una pagina viva con axe-core.
 *
 * Por que existe (Kanam OS Etapa 4, 2026-10-06): la accesibilidad del sistema
 * se validaba de tres formas, todas ciegas a la misma cosa:
 *   - `ui-contrast-audit`: mide contraste de una paleta, no una pagina.
 *   - `a11y-at-validation`: define cuando la validacion MANUAL es obligatoria.
 *   - `check-a11y-trigger`: BLOQUEA un cambio que toca el anuncio, pero no mide
 *      nada: no deja pasar en silencio, no verifica.
 * Faltaba la pata que el analisis del ecosistema (§2.8) ya habia decidido:
 * "axe-core open source + la tool `browser` alcanza" - medir la pagina viva con
 * axe-core, sin suscripcion (`axe-devtools` se descarto por costo).
 *
 * Esto implementa esa decision. Corre axe-core sobre una URL (o un archivo
 * HTML) usando playwright-core y falla si hay violaciones del nivel o peor.
 *
 * Decisiones de diseno (leidas del resto del sistema):
 *   - Un fallo de infraestructura (playwright o axe no disponibles) sale con
 *     exit 2, NO con 0. Un gate que no puede correr y no lo dice es la
 *     "barrera que no corre y no lo dice" (check-a11y-trigger, CI del 2026-09-28).
 *   - El juicio es una funcion pura (`classify`): los tests lo prueban sin
 *     browser ni red, y prueban que PUEDE fallar. Un check que no puede fallar
 *     no verifica nada (check-contrast.py).
 *   - playwright-core se resuelve del propio OpenClaw (viaja con el gateway) o
 *     por OPENCLAW_PLAYWRIGHT_CORE; axe-core se usa local si esta, si no se
 *     trae pineado y se cachea. Cero deps nuevas en el workspace.
 *
 * Uso:
 *   node scripts/a11y-scan.mjs http://127.0.0.1:4317/
 *   node scripts/a11y-scan.mjs http://127.0.0.1:4317/todos --json
 *   node scripts/a11y-scan.mjs --file ./page.html --impact moderate
 *
 * Exit: 0 = pasa; 1 = gate falla (violaciones >= umbral); 2 = error de infra.
 */

import { createRequire } from "node:module";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);

// Severidad de axe, de menor a mayor. El umbral por defecto es `serious`.
export const IMPACT_ORDER = ["minor", "moderate", "serious", "critical"];

/**
 * Clasifica violaciones de axe por impacto respecto a un umbral.
 * Pura: es lo que prueban los tests, sin browser ni red.
 * Devuelve { gate: [violaciones que bloquean], info: [por debajo del umbral] }.
 */
export function classify(violations, threshold = "serious") {
  const min = IMPACT_ORDER.indexOf(threshold);
  if (min === -1) {
    throw new Error(`umbral invalido: ${threshold}. Validos: ${IMPACT_ORDER.join(", ")}`);
  }
  const gate = [];
  const info = [];
  for (const v of violations || []) {
    const idx = IMPACT_ORDER.indexOf(v.impact);
    // Un impacto desconocido o nulo no se descarta en silencio: se trata como
    // el peor caso (gate), porque "no se" no es "esta bien".
    if (idx === -1 || idx >= min) gate.push(v);
    else info.push(v);
  }
  return { gate, info };
}

/** Resumen legible de una corrida de axe. */
export function summarize(violations) {
  return (violations || []).map((v) => ({
    id: v.id,
    impact: v.impact,
    help: v.help,
    nodes: (v.nodes || []).length,
  }));
}

function resolvePlaywright() {
  const candidates = [
    "playwright-core",
    process.env.OPENCLAW_PLAYWRIGHT_CORE,
    "/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core",
    "/usr/local/lib/node_modules/openclaw/node_modules/playwright-core",
  ].filter(Boolean);
  for (const c of candidates) {
    try {
      return require(c);
    } catch {
      /* probamos el siguiente */
    }
  }
  return null;
}

const AXE_VERSION = "4.10.2";
const AXE_URL = `https://unpkg.com/axe-core@${AXE_VERSION}/axe.min.js`;

async function resolveAxeSource() {
  // 1) Local (si el proyecto lo declara como dependencia).
  try {
    const mod = require.resolve("axe-core");
    const dir = mod.replace(/axe\.js$/, "");
    const min = join(dir, "axe.min.js");
    if (existsSync(min)) return readFileSync(min, "utf8");
  } catch {
    /* sigue */
  }
  // 2) Cache local.
  const cacheDir = join(tmpdir(), "a11y-scan");
  const cacheFile = join(cacheDir, `axe-${AXE_VERSION}.min.js`);
  if (existsSync(cacheFile)) return readFileSync(cacheFile, "utf8");
  // 3) Fetch pinneado.
  const res = await fetch(AXE_URL);
  if (!res.ok) throw new Error(`no pude bajar axe-core ${AXE_VERSION}: HTTP ${res.status}`);
  const text = await res.text();
  mkdirSync(cacheDir, { recursive: true });
  writeFileSync(cacheFile, text);
  return text;
}

function parseArgs(argv) {
  const args = { target: null, file: null, impact: "serious", json: false, quiet: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--quiet") args.quiet = true;
    else if (a === "--impact") args.impact = argv[++i];
    else if (a === "--file") args.file = argv[++i];
    else if (!a.startsWith("--")) args.target = a;
  }
  return args;
}

async function main(argv) {
  const args = parseArgs(argv);
  const target = args.file ? pathToFileURL(args.file).href : args.target;
  if (!target) {
    console.error("Uso: a11y-scan.mjs <url> [--json] [--impact serious] | --file <html>");
    return 2;
  }

  const pw = resolvePlaywright();
  if (!pw) {
    console.error(
      "ERROR DE INFRA: playwright-core no disponible. Seteá OPENCLAW_PLAYWRIGHT_CORE " +
        "a la ruta del modulo, o instalalo. (Sin browser no hay medicion - no hay verde.)",
    );
    return 2;
  }

  let axeSource;
  try {
    axeSource = await resolveAxeSource();
  } catch (e) {
    console.error(`ERROR DE INFRA: ${e.message}`);
    return 2;
  }

  const browser = await pw.chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    await page.goto(target, { waitUntil: "networkidle", timeout: 30000 });
    await page.addScriptTag({ content: axeSource });
    const results = await page.evaluate(async () => {
      // @ts-ignore - axe se inyecta en la pagina
      return await window.axe.run(document, { resultTypes: ["violations"] });
    });

    const { gate, info } = classify(results.violations, args.impact);

    if (args.json) {
      console.log(
        JSON.stringify(
          { target, threshold: args.impact, blocking: summarize(gate), below: summarize(info) },
          null,
          2,
        ),
      );
    } else if (!args.quiet) {
      if (gate.length) {
        console.log(`BLOQUEA: ${gate.length} violacion(es) >= ${args.impact} en ${target}`);
        for (const v of summarize(gate)) {
          console.log(`  [${v.impact}] ${v.id} (${v.nodes} nodo/s) - ${v.help}`);
        }
      }
      if (info.length) {
        console.log(`  (${info.length} por debajo del umbral ${args.impact}, informativas)`);
      }
      if (!gate.length) console.log(`OK: sin violaciones >= ${args.impact} en ${target}`);
    }

    return gate.length ? 1 : 0;
  } finally {
    await browser.close();
  }
}

// Solo corre el main si se invoca como script (no al importarlo desde tests).
if (import.meta.url === pathToFileURL(process.argv[1] || "").href) {
  main(process.argv.slice(2))
    .then((code) => process.exit(code))
    .catch((e) => {
      console.error(`ERROR DE INFRA: ${e.stack || e.message}`);
      process.exit(2);
    });
}
