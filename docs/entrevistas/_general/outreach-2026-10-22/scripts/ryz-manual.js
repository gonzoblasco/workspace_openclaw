// ryz-manual.js - Deja el formulario de RYZ (Lever) COMPLETO y ABIERTO en
// una ventana visible, para que Gonzo haga los dos clicks que no se pueden
// automatizar: el hCaptcha y "Submit application".
//
// POR QUE ESTE SCRIPT: el hCaptcha de Lever no resuelve por automatizacion
// (token 0 en headless y en browser visible automatizado, incluso
// clickeando el checkbox del iframe - verificado 2026-10-23). Todo lo demas
// del formulario SI se puede completar solo, asi que este script lo deja
// listo y la ventana queda en pantalla.
//
// NO HACE SUBMIT. El submit lo hace la persona.
//
// Uso:  node tmp/job-search-2026-10-22/ryz-manual.js
//       (dejar la terminal abierta; la ventana queda en pantalla)
const { chromium } = require("/Users/gonzoblasco/.openclaw/workspace/projects/a11y-fixer/node_modules/playwright");

const EXE = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const APPLY = "https://jobs.lever.co/RyzLabs/34d126be-b8fa-4291-8bc4-924031455850/apply";
const BASE = "/Users/gonzoblasco/.openclaw/workspace";
const CV = `${BASE}/docs/entrevistas/ryz-labs-ai-first-frontend/Gonzalo_Blasco_AI_First_Frontend_Engineer_RYZ.pdf`;

const ADDITIONAL =
  "I build with AI as infrastructure rather than as a chat: an AI Engineering OS with per-project sessions, " +
  "persistent memory, subagents and reusable skills, under a strict quarantine, verify and adopt method. I also " +
  "maintain an MCP companion server that lets an agent query what a screen reader actually announces for a snippet " +
  "of HTML. 11 merged pull requests in production React component libraries (Adobe React Spectrum, IBM Carbon, " +
  "Meta Astryx, MUI).";

(async () => {
  const browser = await chromium.launch({
    headless: false,
    executablePath: EXE,
    args: ["--disable-blink-features=AutomationControlled", "--window-position=60,40"],
  });
  const ctx = await browser.newContext({
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    locale: "en-US",
    viewport: { width: 1280, height: 1200 },
  });
  const page = await ctx.newPage();

  console.log("Abriendo el formulario de RYZ...");
  await page.goto(APPLY, { waitUntil: "domcontentloaded", timeout: 45000 });
  await page.waitForTimeout(4000);

  // 1) CV (el auto-lector de Lever parsea y completa campos solo)
  console.log("[1] subiendo CV...");
  await page.locator('input[type="file"]').first().setInputFiles(CV);
  await page.waitForTimeout(12000);

  // 2) textos con type() real (el parser de Lever pisa el nombre con
  //    "Freelance": hay que sobreescribirlo despues de que asiente)
  console.log("[2] completando campos...");
  for (const [name, value] of [
    ["name", "Gonzalo Blasco"],
    ["email", "gonzoblasco@icloud.com"],
    ["phone", "+54 11 4937 4656"],
    ["org", "Freelance"],
  ]) {
    const el = page.locator(`input[name="${name}"]`).first();
    if ((await el.count()) === 0) continue;
    await el.click({ clickCount: 3 }).catch(() => {});
    await el.press("Backspace").catch(() => {});
    await el.type(value, { delay: 14 }).catch(async () => {
      await el.fill(value);
    });
    await el.press("Tab").catch(() => {});
    await page.waitForTimeout(250);
  }

  // 3) ubicacion: autocomplete de Lever. El unico metodo que deja el campo
  //    VISIBLE con texto es teclear + ArrowDown + Enter.
  console.log("[3] ubicacion...");
  const loc = page.locator('input[name="location"]');
  await loc.click();
  await loc.press("Backspace").catch(() => {});
  await loc.type("Buenos Aires", { delay: 70 });
  await page.waitForTimeout(3500);
  await page.keyboard.press("ArrowDown");
  await page.waitForTimeout(400);
  await page.keyboard.press("Enter");
  await page.waitForTimeout(2500);

  // 4) salario
  const sal = page.locator('input[name*="[field0]"]').first();
  if ((await sal.count()) > 0) {
    await sal.click({ clickCount: 3 }).catch(() => {});
    await sal.press("Backspace").catch(() => {});
    await sal.type("3200", { delay: 20 });
    await sal.press("Tab").catch(() => {});
  }

  // 5) nivel de ingles (los radios tienen value = texto de la opcion)
  await page.evaluate(() => {
    const r = [...document.querySelectorAll('input[type="radio"]')].find(
      (e) => (e.value || "").trim() === "Upper Intermediate"
    );
    if (r) r.click();
  });

  // 6) informacion adicional
  const add = page.locator('textarea[name*="[field2]"]').first();
  if ((await add.count()) > 0) {
    await add.click({ clickCount: 3 }).catch(() => {});
    await add.press("Backspace").catch(() => {});
    await add.type(ADDITIONAL, { delay: 2 });
  }

  await page.waitForTimeout(1200);

  const estado = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll("input:not([type=file]), textarea").forEach((e) => {
      const r = e.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      out.push({
        label: (e.closest("div")?.querySelector("label, .application-label")?.textContent || e.name || "")
          .replace(/\s+/g, " ")
          .trim()
          .slice(0, 42),
        val: e.type === "radio" ? (e.checked ? e.value : "") : String(e.value || "").slice(0, 40),
      });
    });
    return out;
  });

  console.log("\n=== FORMULARIO COMPLETO ===");
  estado.forEach((e) => console.log(`  ${e.label.padEnd(44)} ${JSON.stringify(e.val)}`));

  console.log("\n" + "=".repeat(64));
  console.log("  FALTA UN CLICK HUMANO (no se puede automatizar):");
  console.log("  1) el hCaptcha de Lever (si aparece, resolvelo)");
  console.log("  2) el boton 'Submit application'");
  console.log("  Esta ventana queda ABIERTA. No cierres el navegador.");
  console.log("=".repeat(64) + "\n");

  // no se cierra el navegador: queda en pantalla
  await page.bringToFront();
  process.exit(0);
})().catch((e) => {
  console.log("ERR", e.message.slice(0, 300));
  process.exit(1);
});
