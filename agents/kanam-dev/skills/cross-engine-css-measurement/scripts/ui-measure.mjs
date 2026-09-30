// Mide el layout de una UI web a un ancho dado, via CDP, y saca una captura.
//
// Por que existe: un build verde y los tests de componente no ven GEOMETRIA. Los
// sintomas visuales que dependen del ancho (bloques pegados, desborde horizontal,
// una fila que se esconde) solo aparecen al medir al ancho real del contenedor. El
// caso tipico es el panel lateral angosto de una app, donde el diseno de escritorio
// no reproduce nada.
//
// Nace del proyecto kanam-story-bible (2026-09-25), donde dos fallas reales - una
// separacion de 0.0px y un documento estirado de 420px a 599px - eran invisibles al
// build y a los tests. Version especifica de ese proyecto, con su medicion de
// dominio: ~/projects/kanam-story-bible/scripts/ui-shot.mjs
//
// Vive en la skill que lo posee (cross-engine-css-measurement) desde 2026-09-29
// (ADR-084): era un huerfano en scripts/ que nacio como one-shot del proyecto.
//
// Uso:
//   APP_URL=http://127.0.0.1:5173/ W=420 TAB=Fichas OUT=/tmp/x.png \
//     node agents/kanam-dev/skills/cross-engine-css-measurement/scripts/ui-measure.mjs
//
// Variables de entorno:
//   APP_URL    URL a medir                      (default http://127.0.0.1:5173/)
//   W, H       viewport en px                   (default 420x900)
//   TAB        pestana a clickear por texto     (opcional; sin esto no cambia nada)
//   READY      selector CSS a esperar           (opcional; default: espera asentarse)
//   WAIT_MS    espera extra antes de medir      (default 400)
//   OUT        ruta del PNG                     (default /tmp/ui-measure.png)
//   CDP_PORT   puerto de debug                  (default 9333)
//   EXPR       expresion JS a evaluar en vez de la medicion estandar (diagnostico)
//   CHROME     ruta al binario de Chromium      (opcional; default: busca en la cache)
//
// No requiere el paquete de Playwright: usa el Chromium que Playwright ya dejo en
// ~/Library/Caches/ms-playwright, manejado por CDP directo.
import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, readdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const APP = process.env.APP_URL ?? "http://127.0.0.1:5173/";
const W = Number(process.env.W ?? 420);
const H = Number(process.env.H ?? 900);
const TAB = process.env.TAB ?? "";
const READY = process.env.READY ?? "";
const WAIT_MS = Number(process.env.WAIT_MS ?? 400);
const OUT = process.env.OUT ?? "/tmp/ui-measure.png";
const PORT = Number(process.env.CDP_PORT ?? 9333);
const EXPR = process.env.EXPR ?? "";

function buscarChrome() {
  if (process.env.CHROME) {
    if (!existsSync(process.env.CHROME)) throw new Error(`CHROME no existe: ${process.env.CHROME}`);
    return process.env.CHROME;
  }
  const base = join(process.env.HOME, "Library/Caches/ms-playwright");
  if (!existsSync(base)) throw new Error("sin cache de playwright en ~/Library/Caches/ms-playwright");
  const hallados = [];
  for (const d of readdirSync(base)) {
    if (!d.startsWith("chromium-")) continue;
    const p = join(base, d, "chrome-mac-arm64", "Google Chrome for Testing.app",
                   "Contents", "MacOS", "Google Chrome for Testing");
    if (existsSync(p)) hallados.push(p);
  }
  if (!hallados.length) throw new Error("sin binario de Chromium en la cache");
  return hallados.sort().at(-1);
}

function esperar(ms) { return new Promise((r) => setTimeout(r, ms)); }

// Se inyecta en la pagina: mide geometria y encuentra los culpables del desborde.
// El filtro de culpables es la parte que costo: un elemento dentro de un scroller
// reporta `right` mas alla del viewport aunque el scroller lo recorte, asi que sin
// excluir a los que tienen un ancestro que recorta la lista se llena de falsos
// positivos y la causa real no aparece.
const MEDIR = `(() => {
  const rect = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return { top: +b.top.toFixed(1), bottom: +b.bottom.toFixed(1),
             left: +b.left.toFixed(1), right: +b.right.toFixed(1),
             w: +b.width.toFixed(1), h: +b.height.toFixed(1) }; };

  const vw = window.innerWidth;
  const vh = window.innerHeight;

  // Un ancestro recorta si su overflow-x no es visible.
  const recortado = (el) => {
    let p = el.parentElement;
    while (p && p !== document.documentElement) {
      const ox = getComputedStyle(p).overflowX;
      if (ox === "auto" || ox === "hidden" || ox === "scroll") return true;
      p = p.parentElement;
    }
    return false;
  };

  // Desborde real del documento: el elemento que pasa el viewport sin que ningun
  // ancestro lo recorte. Si la lista esta vacia y el documento igual desborda,
  // el culpable es un descendiente con position absolute/fixed sin ancestro
  // posicionado: su bloque contenedor es el documento y ningun overflow lo corta.
  const culpables = [];
  let absolutosSinAncla = 0;
  for (const el of document.querySelectorAll("body *")) {
    const b = el.getBoundingClientRect();
    if (b.right <= vw + 0.5 && b.left >= -0.5) continue;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") continue;
    if (recortado(el)) continue;
    const pos = cs.position;
    const esAbsoluto = pos === "absolute" || pos === "fixed";
    if (esAbsoluto) absolutosSinAncla++;
    culpables.push({
      tag: el.tagName.toLowerCase(),
      cls: String(el.className || "").slice(0, 60),
      id: el.id || "",
      position: pos,
      right: +b.right.toFixed(1),
      left: +b.left.toFixed(1),
      w: +b.width.toFixed(1),
      texto: (el.textContent || "").trim().slice(0, 40),
    });
  }

  // Scrollers: elementos con contenido mas ancho que su caja. Es donde el desborde
  // esta LEGITIMAMENTE contenido (una tabla ancha con overflow-x: auto).
  const scrollers = [];
  for (const el of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(el);
    if (cs.overflowX !== "auto" && cs.overflowX !== "scroll") continue;
    if (el.scrollWidth > el.clientWidth + 1) {
      scrollers.push({
        tag: el.tagName.toLowerCase(),
        cls: String(el.className || "").slice(0, 40),
        clientW: el.clientWidth,
        scrollW: el.scrollWidth,
      });
    }
  }

  const docScrollW = document.documentElement.scrollWidth;
  const docScrollH = document.documentElement.scrollHeight;

  return {
    url: location.href,
    viewport: { w: vw, h: vh },
    documento: {
      scrollW: docScrollW,
      scrollH: docScrollH,
      desbordaHorizontal: docScrollW > vw,
      desbordaVertical: docScrollH > vh,
    },
    culpablesDelDesborde: culpables.slice(0, 12),
    totalCulpables: culpables.length,
    absolutosSinAncestroPosicionado: absolutosSinAncla,
    scrollers,
    // Anclas utiles: los landmarks, para saber que se midio.
    landmarks: [...document.querySelectorAll("main, [role=tabpanel], [role=tablist], table, form")]
      .slice(0, 6).map((el) => ({ tag: el.tagName.toLowerCase(),
                                  cls: String(el.className || "").slice(0, 30),
                                  ...rect(el) })),
  };
})()`;

async function main() {
  const chrome = buscarChrome();
  const perfil = mkdtempSync(join(tmpdir(), "ui-measure-"));
  const proc = spawn(chrome, [
    "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
    "--no-default-browser-check", `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${perfil}`, `--window-size=${W},${H}`, "about:blank",
  ], { stdio: "ignore" });

  // Esperar el endpoint de debug.
  let targets = null;
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/list`);
      targets = await r.json();
      if (targets.some((t) => t.type === "page")) break;
    } catch { /* aun no levanta */ }
    await esperar(250);
  }
  if (!targets) throw new Error("CDP no respondio");
  const pagina = targets.find((t) => t.type === "page");
  if (!pagina) throw new Error("sin target de tipo page");

  const ws = new WebSocket(pagina.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

  let id = 0;
  const pendientes = new Map();
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pendientes.has(m.id)) {
      const { res, rej } = pendientes.get(m.id);
      pendientes.delete(m.id);
      m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
    }
  };
  const send = (method, params = {}) =>
    new Promise((res, rej) => {
      const n = ++id;
      pendientes.set(n, { res, rej });
      ws.send(JSON.stringify({ id: n, method, params }));
    });

  const evaluar = async (expr) => {
    const r = await send("Runtime.evaluate", {
      expression: expr, returnByValue: true, awaitPromise: true,
    });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.text + " :: " + expr.slice(0, 80));
    return r.result.value;
  };

  const cerrar = () => { try { ws.close(); } catch { /* ya cerrado */ } proc.kill(); };

  await send("Page.enable");
  // Sin este override se mide a 800px y el bug de panel angosto no aparece.
  await send("Emulation.setDeviceMetricsOverride", {
    width: W, height: H, deviceScaleFactor: 2, mobile: false,
  });
  await send("Page.navigate", { url: APP });

  // Espera: un selector explicito si se paso, si no la carga del documento.
  if (READY) {
    for (let i = 0; i < 80; i++) {
      const hay = await evaluar(`!!document.querySelector(${JSON.stringify(READY)})`).catch(() => false);
      if (hay) break;
      await esperar(250);
    }
  } else {
    for (let i = 0; i < 40; i++) {
      const listo = await evaluar(`document.readyState === "complete"`).catch(() => false);
      if (listo) break;
      await esperar(250);
    }
  }

  if (TAB) {
    await evaluar(`(() => {
      const b = [...document.querySelectorAll('[role="tab"], button, a')]
        .find((x) => (x.textContent || '').trim() === ${JSON.stringify(TAB)});
      if (!b) throw new Error('no encontre un control con el texto: ' + ${JSON.stringify(TAB)});
      b.click();
      return true;
    })()`);
  }

  // Dos frames antes de medir: el compositor recalcula posicionados y anchors en el
  // frame siguiente, asi que medir en el mismo tick devuelve valores viejos.
  await evaluar(`new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))`);
  await esperar(WAIT_MS);

  if (EXPR) {
    console.log(JSON.stringify(await evaluar(EXPR), null, 2));
    cerrar();
    return;
  }

  const medicion = await evaluar(MEDIR);
  const shot = await send("Page.captureScreenshot", {
    format: "png", captureBeyondViewport: true,
  });
  writeFileSync(OUT, Buffer.from(shot.data, "base64"));

  console.log(JSON.stringify({ ancho: W, tab: TAB || null, out: OUT, medicion }, null, 2));
  cerrar();
}

main().then(() => process.exit(0)).catch((e) => {
  console.error("ERROR:", e.message);
  process.exit(1);
});
