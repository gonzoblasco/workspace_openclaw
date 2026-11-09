// real-browser.mjs - Selección del motor de navegador correcto
//
// POR QUÉ EXISTE (2026-10-23):
//   Los formularios de Lever y Ashby usan hCaptcha/recaptcha que detectan
//   contexto automatizado (navigator.webdriver, headless).  En Safari el
//   captcha no aparece, pero en Chrome necesita conectarse al navegador real
//   del usuario a través de CDP (Chrome DevTools Protocol) en el puerto 18801.
//   Esta librería encapsula la lógica de abrir el navegador: headless en la
//   mayoría de los casos, real‑browser cuando la página contiene captcha.

import { createRequire } from "module";
import { existsSync } from "node:fs";
const require = createRequire(import.meta.url);

export const CDP_URL = "http://127.0.0.1:18801";

/**
 * Detecta si la página contiene un captcha visible.
 *
 * @param {object} page Playwright Page.
 * @returns {Promise<boolean>}
 */
export async function hasCaptcha(page) {
  // Busca iframes con títulos típicos o variables globales de hcaptcha/recaptcha.
  const found = await page.evaluate(() => {
    // iframe con título que contenga "captcha"
    const iframe = [...document.querySelectorAll("iframe[title]")].find((i) => /captcha/i.test(i.title));
    if (iframe) return true;
    // variables globales de hcaptcha/grecaptcha
    if (window.hcaptcha && typeof window.hcaptcha.getResponse === "function") return true;
    if (window.grecaptcha && typeof window.grecaptcha.getResponse === "function") return true;
    return false;
  });
  return Boolean(found);
}

/**
 * Abre un navegador.
 *   - Si `preferReal` es true y la página tiene captcha, intentamos conectar
 *     a Chrome vía CDP (requiere que el usuario tenga Chrome ejecutándose con
 *     el puerto 18801 abierto, como hace el script `ryz-cdp.js`).
 *   - En caso de fallo, o cuando `preferReal` es false, se lanza Chrome en
 *     modo headless (playwright).
 *
 * @param {object} opts {preferReal:boolean}
 * @returns {Promise<object>} Playwright BrowserContext (para usar con page).
 */
export async function openBrowser({ preferReal } = { preferReal: false }) {
  // Lazy‑load playwright only when needed.
  const { chromium } = require("/Users/gonzoblasco/.openclaw/workspace/projects/kanam-fixer/node_modules/playwright");

  if (preferReal) {
    try {
      // Intentar conexión CDP al Chrome real del usuario.
      const browser = await chromium.connectOverCDP(CDP_URL);
      // BUG CORREGIDO 2026-10-23: `browser.newContext()` sobre un browser
      // conectado por CDP crea un contexto NUEVO, sin las cookies de la
      // sesion real (LinkedIn, etc.). Para heredar la sesion hay que usar
      // el contexto existente: `browser.contexts()[0]`. El script de
      // referencia (ryz-cdp.js) ya lo hacia asi.
      const existing = browser.contexts();
      const context = existing.length ? existing[0] : await browser.newContext();
      return { browser, context, isReal: true };
    } catch (e) {
      // Fallback a headless.
      console.warn("[real-browser] CDP connection failed, falling back to headless", e.message);
    }
  }
  // Headless launch.
  //
  // BUG CORREGIDO 2026-10-23: `chromium.launch()` sin `executablePath` usa
  // el binario que Playwright descarga en SU cache, que en esta maquina no
  // esta (la version de playwright instalada espera chromium_headless_shell-
  // 1228 y solo hay 1243). El error era "Executable doesn't exist".
  // Se resuelve buscando un Chrome/Chromium utilizable, en este orden:
  //   1. el Chrome del sistema (instalado, con sesion)
  //   2. el Chrome for Testing de Playwright, si existe
  //   3. el chrome-headless-shell de Playwright, si existe
  // y si no hay ninguno, el error dice QUE FALTA, en vez de un stack opaco.
  const launchOpts = { headless: true };
  const exe = findChromiumExecutable();
  if (exe) {
    launchOpts.executablePath = exe;
  } else {
    console.error(
      "[real-browser] no se encontro un Chrome utilizable. Instalá Chrome, o:\n" +
        "  npx playwright install chromium"
    );
    throw new Error("sin ejecutable de Chromium disponible");
  }
  const browser = await chromium.launch(launchOpts);
  const context = await browser.newContext({
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    locale: "es-AR",
    // BUG CORREGIDO 2026-10-23: el viewport debe coincidir con el del
    // script de referencia (1200x2000). Con 1280x1600 el dropzone del CV
    // de Eightfold queda fuera del area renderizada, el input de archivo no
    // se monta y el CV NO se adjunta - sin ningun error visible, el
    // formulario queda "completo" y vacio. Medido con dos corridas.
    viewport: { width: 1200, height: 2000 },
  });
  return { browser, context, isReal: false };
}

/**
 * Busca un Chromium utilizable. El orden importa: el Chrome del sistema es el
 * que tiene la sesion de LinkedIn y NO esta marcado como automatizado
 * (`navigator.webdriver === false`), asi que es el preferido.
 */
export function findChromiumExecutable() {
  const home = process.env.HOME || "";
  const candidates = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    `${home}/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`,
    `${home}/Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell`,
    `${home}/.cache/puppeteer/chrome/mac_arm-152.0.7977.75/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`,
  ];
  for (const c of candidates) {
    try {
      if (existsSync(c)) return c;
    } catch {}
  }
  return null;
}

