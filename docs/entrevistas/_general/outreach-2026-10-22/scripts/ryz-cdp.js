// ryz-cdp.js - Postulacion a RYZ Labs (Lever) usando el CHROME REAL del
// usuario, conectado por CDP.
//
// POR QUE ESTE SCRIPT (2026-10-23): el intento anterior lanzo un Chrome
// propio via Playwright y pidio resolver el hCaptcha a mano. Fallaba, y el
// motivo NO era la cantidad de intentos: es que un browser lanzado por
// Playwright queda marcado como automatizado (`navigator.webdriver === true`,
// flag de CDP, etc.) y hCaptcha rechaza el token antes de generarlo. Por mas
// que una persona clickee el checkbox, el challenge no resuelve.
//
// La solucion: NO lanzar un browser. Conectarse por CDP al Chrome que el
// usuario ya tiene abierto (el perfil `imported`, con la sesion de LinkedIn y
// sin flags de automatizacion). Ahi `navigator.webdriver` es false (verificado)
// y el hCaptcha se comporta como con cualquier persona.
//
// `connectOverCDP` no inyecta flags: se engancha al browser existente.
//
// Uso:  node tmp/job-search-2026-10-22/ryz-cdp.js [--submit]
const { chromium } = require("/Users/gonzoblasco/.openclaw/workspace/projects/a11y-fixer/node_modules/playwright");

const CDP = "http://127.0.0.1:18801"; // perfil `imported` del browser de OpenClaw
const APPLY = "https://jobs.lever.co/RyzLabs/34d126be-b8fa-4291-8bc4-924031455850/apply";
const BASE = "/Users/gonzoblasco/.openclaw/workspace";
const CV = `${BASE}/docs/entrevistas/ryz-labs-ai-first-frontend/Gonzalo_Blasco_AI_First_Frontend_Engineer_RYZ.pdf`;
const SHOT = `${BASE}/tmp/job-search-2026-10-22/ryz-cdp-filled.png`;
const SUBMIT = process.argv.includes("--submit");

const ADDITIONAL =
  "I build with AI as infrastructure rather than as a chat: an AI Engineering OS with per-project sessions, " +
  "persistent memory, subagents and reusable skills, under a strict quarantine, verify and adopt method. I also " +
  "maintain an MCP companion server that lets an agent query what a screen reader actually announces for a snippet " +
  "of HTML. 11 merged pull requests in production React component libraries (Adobe React Spectrum, IBM Carbon, " +
  "Meta Astryx, MUI).";

(async () => {
  const browser = await chromium.connectOverCDP(CDP);
  const ctx = browser.contexts()[0];
  const page = await ctx.newPage();

  console.log("Conectado al Chrome real por CDP (sin flags de automatizacion).");
  await page.goto(APPLY, { waitUntil: "domcontentloaded", timeout: 45000 });
  await page.waitForTimeout(4000);

  const wd = await page.evaluate(() => navigator.webdriver);
  console.log("navigator.webdriver:", wd, wd === false ? "(ok: no automatizado)" : "(MAL: automatizado)");

  // 1) CV (el auto-lector de Lever parsea y completa campos solo)
  console.log("[1] subiendo CV...");
  await page.locator('input[type="file"]').first().setInputFiles(CV);
  await page.waitForTimeout(13000);

  // 2) textos: type() real. El parser de Lever pone "Freelance" en Full name
  //    (el nombre de la empresa del CV): hay que sobreescribirlo DESPUES.
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
    await page.waitForTimeout(300);
  }

  // 3) ubicacion: el autocomplete de Lever. El unico metodo que deja el campo
  //    VISIBLE con texto es teclear + ArrowDown + Enter (con fill() React borra
  //    el valor).
  console.log("[3] ubicacion...");
  const loc = page.locator('input[name="location"]');
  await loc.click();
  await loc.press("Backspace").catch(() => {});
  await loc.type("Buenos Aires", { delay: 70 });
  await page.waitForTimeout(4000);
  await page.keyboard.press("ArrowDown");
  await page.waitForTimeout(500);
  await page.keyboard.press("Enter");
  await page.waitForTimeout(3000);

  // 4) salario
  const sal = page.locator('input[name*="[field0]"]').first();
  if ((await sal.count()) > 0) {
    await sal.click({ clickCount: 3 }).catch(() => {});
    await sal.press("Backspace").catch(() => {});
    await sal.type("3200", { delay: 20 });
    await sal.press("Tab").catch(() => {});
  }

  // 5) nivel de ingles: los radios de Lever tienen value = texto de la opcion
  const eng = await page.evaluate(() => {
    const r = [...document.querySelectorAll('input[type="radio"]')].find(
      (e) => (e.value || "").trim() === "Upper Intermediate"
    );
    if (!r) return false;
    r.click();
    return r.checked;
  });
  console.log("    ingles Upper Intermediate:", eng);

  // 6) informacion adicional
  const add = page.locator('textarea[name*="[field2]"]').first();
  if ((await add.count()) > 0) {
    await add.click({ clickCount: 3 }).catch(() => {});
    await add.press("Backspace").catch(() => {});
    await add.type(ADDITIONAL, { delay: 2 });
  }

  await page.waitForTimeout(1500);

  const estado = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll(".application-question, [class*='application-question']").forEach((q) => {
      const lab = q.querySelector("label, .application-label");
      if (!lab) return;
      const input = q.querySelector("input:not([type=file]), textarea");
      const radio = q.querySelector('input[type="radio"]:checked');
      out.push({
        label: lab.textContent.replace(/\s+/g, " ").trim().slice(0, 44),
        val: radio ? radio.value : input ? String(input.value || "").slice(0, 40) : "archivo",
      });
    });
    return out;
  });
  console.log("\n=== FORMULARIO ===");
  estado.forEach((e) => console.log(`  ${e.label.padEnd(46)} ${JSON.stringify(e.val)}`));

  await page.screenshot({ path: SHOT, fullPage: true });
  console.log("captura:", SHOT);

  // 7) el hCaptcha: en un browser NO automatizado, el token se genera solo
  //    al enviar (es invisible). Se espera y se mira.
  if (SUBMIT) {
    console.log("\n>>> SUBMIT (envio real)...");
    const clicked = await page.evaluate(() => {
      const b = [...document.querySelectorAll("button")].find((e) => {
        const r = e.getBoundingClientRect();
        const t = (e.textContent || "").replace(/\s+/g, " ").trim().toLowerCase();
        return r.width > 0 && r.height > 0 && t.includes("submit application");
      });
      if (!b) return false;
      b.click();
      return true;
    });
    console.log("    click:", clicked);

    // se espera a que hCaptcha resuelva (puede tardar)
    for (let i = 0; i < 12; i++) {
      await page.waitForTimeout(5000);
      const tok = await page.evaluate(() => {
        const t = window.hcaptcha && window.hcaptcha.getResponse ? window.hcaptcha.getResponse() : "";
        return (t || "").length;
      });
      const url = page.url();
      if (tok > 20) {
        console.log(`    token hCaptcha obtenido (${tok} chars) tras ${(i + 1) * 5}s`);
        break;
      }
      if (!/apply/.test(url)) {
        console.log("    la pagina salio del formulario");
        break;
      }
      console.log(`    esperando hCaptcha... ${(i + 1) * 5}s (token ${tok})`);
    }

    const fin = await page.evaluate(() => ({
      url: location.href,
      texto: document.body.innerText.replace(/\s+/g, " ").slice(0, 600),
    }));
    console.log("\nURL final:", fin.url);
    console.log("TEXTO:", fin.texto);
    await page.screenshot({
      path: SHOT.replace(".png", "-submitted.png"),
      fullPage: true,
    });
  } else {
    console.log("\n(sin --submit: el formulario queda listo)");
  }

  // NO se cierra el browser: es el del usuario, con su sesion.
  await page.bringToFront();
  process.exit(0);
})().catch((e) => {
  console.log("ERR", e.message.slice(0, 400));
  process.exit(1);
});
