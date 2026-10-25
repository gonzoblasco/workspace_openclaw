#!/usr/bin/env node
/**
 * apply.mjs - Orquestador de aplicación a una oferta.
 *
 * Uso (ejemplo):
 *   node apply.mjs --url https://jobs.lever.co/RyzLabs/… --ats auto \
 *       --cv /ruta/cv.pdf --answers data.json [--submit] [--out ./out]
 *
 * POR QUÉ EXISTE (2026-10-23): agrupa los adapters, los workarounds de React
 * y la lógica de verificación descrita en `ats-playbook.md`.  No lanza el
 * envío cuando quedan campos divergentes.
 */

import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { ADAPTERS, detectAdapter } from "./lib/ats.mjs";
import { openBrowser, hasCaptcha } from "./lib/real-browser.mjs";
import { verifyFields } from "./lib/react-form.mjs";

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith("--")) {
        out[key] = next;
        i++;
      } else {
        out[key] = true;
      }
    }
  }
  return out;
}

const opts = parseArgs();
if (!opts.url) {
  console.error("--url es obligatorio");
  process.exit(1);
}
if (!opts.cv) {
  console.error("--cv es obligatorio");
  process.exit(1);
}
if (!opts.answers) {
  console.error("--answers es obligatorio");
  process.exit(1);
}

const atsChoice = opts.ats || "auto";
const submitFlag = !!opts.submit;
const outDir = opts.out ? resolve(opts.out) : null;

// Cargar respuestas semánticas.
const answers = JSON.parse(readFileSync(opts.answers, "utf8"));
const files = { resume: resolve(opts.cv), coverLetter: opts.cover ? resolve(opts.cover) : null };

async function main() {
  // Detectar adaptador.
  const adapterName = atsChoice === "auto" ? detectAdapter(opts.url) : atsChoice;
  if (!adapterName) {
    console.error(`No se pudo detectar adaptador para ${opts.url}`);
    process.exit(1);
  }
  const adapter = ADAPTERS[adapterName];
  if (!adapter) {
    console.error(`Adapter ${adapterName} no está implementado`);
    process.exit(1);
  }

  // Abrir navegador. Si la página tiene captcha, preferimos el browser real.
  const { browser, context, isReal } = await openBrowser({ preferReal: true });
  const page = await context.newPage();
  const { url } = opts;
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
  // Detectar captcha antes de rellenar.
  const captcha = await hasCaptcha(page);
  if (captcha) {
    console.log("[WARN] captcha detectado, se requiere intervención humana antes de submit.");
  }

  // Llenar vía adaptador.
  const fillResult = await adapter.fill(page, { answers, files });

  // BUG CORREGIDO 2026-10-23: se llamaba `verifyFields(page, [])` con un
  // array VACIO, asi que la verificacion devolvia siempre [] y el gate
  // "no enviar si hay divergentes" era un no-op: podia enviar un formulario
  // con los campos sin registrar en React. Ahora cada adaptador declara
  // sus selectores (fieldSelectors) y se verifican contra el estado real.
  const selectors = fillResult.fieldSelectors || [];
  const divergentes = selectors.length ? await verifyFields(page, selectors) : [];
  // "No verificable" NO es lo mismo que "divergente": un form que no es
  // React (Lever) no tiene _valueTracker, asi que el DOM es la unica
  // evidencia. Se reporta aparte, para que el lector sepa que la
  // verificacion fue parcial y por que.
  const noVerificables = divergentes.noVerificables || [];
  if (!selectors.length) {
    console.log(
      "[WARN] el adaptador no declaro fieldSelectors: la verificacion DOM-vs-React no pudo correr."
    );
  }
  const missing = fillResult.missing || [];
  // Construir resumen.
  const summary = {
    ats: adapterName,
    ok: fillResult.ok,
    filled: fillResult.filled || [],
    missing,
    divergentes,
    noVerificables,
    captcha,
    notes: fillResult.notes || [],
    radios: fillResult.radios || null,
    verdict: null,
    evidence: "",
  };

  // BUG CORREGIDO 2026-10-23: `browser.close()` sobre un browser conectado
  // por CDP CIERRA el Chrome del usuario (con su sesion de LinkedIn). Solo se
  // cierra el browser que lanzo el propio script.
  const shutdown = async () => {
    if (isReal) {
      // Se cierra SOLO la pestana que abrio el script.
      try { await page.close(); } catch {}
    } else {
      try { await browser.close(); } catch {}
    }
  };

  if (divergentes.length) {
    console.log("[INFO] campos divergentes detectados, abortando submit.");
    console.log(JSON.stringify(summary, null, 2));
    await shutdown();
    process.exit(0);
  }

  if (submitFlag) {
    const submitRes = await adapter.submit(page);
    summary.verdict = submitRes.verdict;
    summary.evidence = submitRes.evidence || "";
    console.log(JSON.stringify(summary, null, 2));
  } else {
    console.log(JSON.stringify(summary, null, 2));
  }

  if (outDir) {
    // Guardar captura de pantalla.
    const path = `${outDir}/form-${Date.now()}.png`;
    await page.screenshot({ path, fullPage: true });
    console.log(`captura guardada: ${path}`);
  }
  await shutdown();
}

main().catch((e) => {
  console.error("ERR", e);
  process.exit(1);
});

