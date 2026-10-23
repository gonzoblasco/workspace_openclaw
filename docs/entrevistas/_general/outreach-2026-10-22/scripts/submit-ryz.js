// submit-ryz.js - Envio final de la postulacion a RYZ Labs (Lever).
//
// Por que este script (2026-10-23): el boton de submit de Lever cambia de
// clase segun el estado del form (tras subir el CV, Lever re-renderiza y
// `button.btn-submit` deja de existir; el boton de hCaptcha oculto, en
// cambio, siempre esta). Por eso el boton se busca POR TEXTO entre los
// VISIBLES, que es lo que un humano clickea.
//
// Ademas: el hCaptcha de Lever es invisible. Su token se genera en el
// momento del submit. Si el token llega a 0, el envio no se procesa y hay
// que resolverlo a mano.
//
// Uso: node tmp/job-search-2026-10-22/submit-ryz.js
const { chromium } = require("/Users/gonzoblasco/.openclaw/workspace/projects/a11y-fixer/node_modules/playwright");
const path = require("path");

const EXE = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const APPLY = "https://jobs.lever.co/RyzLabs/34d126be-b8fa-4291-8bc4-924031455850/apply";
const BASE = "/Users/gonzoblasco/.openclaw/workspace";
const CV = `${BASE}/docs/entrevistas/ryz-labs-ai-first-frontend/Gonzalo_Blasco_AI_First_Frontend_Engineer_RYZ.pdf`;
const SHOT = `${BASE}/tmp/job-search-2026-10-22/ryz-form-filled.png`;

const TEXTOS = {
  name: "Gonzalo Blasco",
  email: "gonzoblasco@icloud.com",
  phone: "+54 11 4937 4656",
  location: "Buenos Aires, ARG",
  org: "Freelance",
  salary: "3200",
};

const ADDITIONAL =
  "I build with AI as infrastructure rather than as a chat: an AI Engineering OS with per-project sessions, persistent memory, subagents and reusable skills, run under a strict quarantine -> analyze -> verify -> adopt method. I also maintain an MCP companion server that lets an agent query what a screen reader actually announces for a snippet of HTML. 11 merged pull requests in production React component libraries (Adobe React Spectrum, IBM Carbon, Meta Astryx, MUI).";

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: EXE,
    args: ["--disable-blink-features=AutomationControlled"],
  });
  const ctx = await browser.newContext({
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    locale: "en-US",
    viewport: { width: 1280, height: 1600 },
  });
  const page = await ctx.newPage();

  const respuestas = [];
  page.on("response", async (r) => {
    if (r.request().method() !== "POST") return;
    if (!/lever|hcaptcha|recaptcha/i.test(r.url())) return;
    try {
      const b = (await r.text()).slice(0, 700);
      if (b) respuestas.push({ status: r.status(), url: r.url().slice(-64), body: b });
    } catch (e) {}
  });

  await page.goto(APPLY, { waitUntil: "domcontentloaded", timeout: 45000 });
  await page.waitForTimeout(3500);

  // 1) CV: el auto-lector de Lever lo parsea y completa campos solo.
  console.log("[1] subiendo CV...");
  await page.locator('input[type="file"]').first().setInputFiles(CV);
  await page.waitForTimeout(12000);

  // 2) textos: type() real. El parser de Lever pone "Freelance" en Full name
  //    y hay que sobreescribirlo DESPUES de que asiente.
  console.log("[2] textos:");
  for (const [name, value] of [
    ["name", TEXTOS.name],
    ["email", TEXTOS.email],
    ["phone", TEXTOS.phone],
    ["org", TEXTOS.org],
  ]) {
    const el = page.locator(`input[name="${name}"]`).first();
    if ((await el.count()) === 0) {
      console.log(`    [?] no existe ${name}`);
      continue;
    }
    await el.click({ clickCount: 3 }).catch(() => {});
    await el.press("Backspace").catch(() => {});
    await el.type(value, { delay: 14 });
    await el.press("Tab").catch(() => {});
    await page.waitForTimeout(250);
    const dom = await el.inputValue().catch(() => "?");
    const react = await el.evaluate((e) => {
      const t = e._valueTracker;
      return t && t.getValue ? String(t.getValue()) : "";
    });
    console.log(`    [${dom === value ? "ok" : "REVISAR"}] ${name} = ${JSON.stringify(dom)} (react=${JSON.stringify(react)})`);
  }

  // 3) Ubicacion: autocomplete de Lever. El unico metodo que deja el campo
  //    VISIBLE con texto es teclear + ArrowDown + Enter (con fill() React
  //    borra el valor). Verificado 2026-10-23.
  console.log("[3] ubicacion:");
  const loc = page.locator('input[name="location"]');
  await loc.click();
  await loc.press("Backspace").catch(() => {});
  await loc.type("Buenos Aires", { delay: 70 });
  await page.waitForTimeout(3500);
  await page.keyboard.press("ArrowDown");
  await page.waitForTimeout(400);
  await page.keyboard.press("Enter");
  await page.waitForTimeout(2500);
  const locVal = await loc.inputValue().catch(() => "");
  const locSel = await page.evaluate(
    () => document.querySelector('input[name="selectedLocation"]')?.value || ""
  );
  console.log(`    location = ${JSON.stringify(locVal)} | selected=${locSel.slice(0, 70)}`);

  // 4) salario
  console.log("[4] salario:");
  const sal = page.locator('input[name*="[field0]"]').first();
  if ((await sal.count()) > 0) {
    await sal.click({ clickCount: 3 }).catch(() => {});
    await sal.press("Backspace").catch(() => {});
    await sal.type(TEXTOS.salary, { delay: 20 });
    await sal.press("Tab").catch(() => {});
    await page.waitForTimeout(300);
    console.log(`    salary = ${JSON.stringify(await sal.inputValue().catch(() => ""))}`);
  }

  // 5) nivel de ingles: los radios de Lever tienen value = texto de la opcion
  console.log("[5] ingles:");
  const engOk = await page.evaluate(() => {
    const r = [...document.querySelectorAll('input[type="radio"]')].find(
      (e) => (e.value || "").trim() === "Upper Intermediate"
    );
    if (!r) return false;
    r.click();
    return r.checked;
  });
  await page.waitForTimeout(400);
  console.log(`    [${engOk ? "ok" : "FALLO"}] Upper Intermediate`);

  // 6) informacion adicional
  const add = page.locator('textarea[name*="[field2]"]').first();
  if ((await add.count()) > 0) {
    await add.click({ clickCount: 3 }).catch(() => {});
    await add.press("Backspace").catch(() => {});
    await add.type(ADDITIONAL, { delay: 4 });
    await page.waitForTimeout(400);
    console.log(`    [ok] additional (${(await add.inputValue()).length} chars)`);
  }

  // 7) verificacion
  const verif = await page.evaluate(() => {
    const campos = [];
    document.querySelectorAll(".application-question, [class*='application-question']").forEach((q) => {
      const lab = q.querySelector("label, .application-label");
      if (!lab) return;
      const input = q.querySelector("input:not([type=file]), textarea");
      const radio = q.querySelector('input[type="radio"]:checked');
      campos.push({
        label: lab.textContent.replace(/\s+/g, " ").trim().slice(0, 46),
        valor: radio ? radio.value : input ? String(input.value || "").slice(0, 40) : "archivo",
      });
    });
    return campos;
  });
  console.log("\n=== ESTADO ===");
  verif.forEach((c) => console.log(`  ${c.label.padEnd(48)} ${c.valor}`));
  await page.screenshot({ path: SHOT, fullPage: true });

  // 8) boton de submit: por TEXTO, entre los visibles
  console.log("\n[8] boton de submit:");
  const btn = await page.evaluate(() => {
    const b = [...document.querySelectorAll("button")].find((e) => {
      const r = e.getBoundingClientRect();
      const t = (e.textContent || "").replace(/\s+/g, " ").trim().toLowerCase();
      return r.width > 0 && r.height > 0 && t.includes("submit");
    });
    if (!b) return null;
    const t = (b.textContent || "").replace(/\s+/g, " ").trim();
    b.click();
    return t;
  });
  console.log(`    clickeado: ${JSON.stringify(btn)}`);

  await page.waitForTimeout(18000);

  const tok = await page.evaluate(() => {
    const t = window.hcaptcha && window.hcaptcha.getResponse ? window.hcaptcha.getResponse() : "";
    return (t || "").length;
  });
  console.log("token hCaptcha tras submit:", tok);

  console.log("\n=== RESPUESTAS DEL SERVIDOR ===");
  respuestas.forEach((r) => console.log(`  [${r.status}] ${r.url}\n    ${r.body.slice(0, 400)}`));

  const fin = await page.evaluate(() => ({
    url: location.href,
    exito:
      /thank you|application (was )?submitted|we (have )?received your application|success/i.test(
        document.body.innerText
      ),
    texto: document.body.innerText.replace(/\s+/g, " ").slice(0, 600),
  }));
  console.log("\nURL final:", fin.url);
  console.log("EXITO:", fin.exito);
  console.log("TEXTO:", fin.texto);
  await page.screenshot({ path: SHOT.replace(".png", "-submitted.png"), fullPage: true });

  await browser.close();
  process.exit(0);
})().catch((e) => {
  console.log("ERR", e.message.slice(0, 400));
  process.exit(1);
});
