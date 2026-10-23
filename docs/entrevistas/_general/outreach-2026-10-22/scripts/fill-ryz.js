// fill-ryz.js - Completa el formulario de RYZ (Lever) SIN enviar.
//
// Por que un script y no el browser de OpenClaw: el tool "browser" no arranca
// (no hay Chrome instalado en /Applications) y el que hay (Chrome for Testing
// de Playwright) se maneja con Playwright. Verificado 2026-10-23.
//
// El dry run del 23/10 mostro dos cosas que este script corrige:
//   1. El auto-lector de Lever pone "Freelance" en el campo Full name (el
//      nombre del CV). Hay que sobreescribir DESPUES de que el parser asiente.
//   2. Los radios de "English level" son CSS, no <select>: se eligen por
//      etiqueta, no por valor.
//
// Uso: node tmp/job-search-2026-10-22/fill-ryz.js [--submit]
const { chromium } = require("/Users/gonzoblasco/.openclaw/workspace/projects/a11y-fixer/node_modules/playwright");
const path = require("path");

const EXE =
  "/Users/gonzoblasco/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing";
const APPLY = "https://jobs.lever.co/RyzLabs/34d126be-b8fa-4291-8bc4-924031455850/apply";
const CV = path.resolve(
  "/Users/gonzoblasco/.openclaw/workspace/docs/entrevistas/ryz-labs-ai-first-frontend/Gonzalo_Blasco_AI_First_Frontend_Engineer_RYZ.pdf"
);
const SHOT =
  "/Users/gonzoblasco/.openclaw/workspace/tmp/job-search-2026-10-22/ryz-form-filled.png";

const SUBMIT = process.argv.includes("--submit");

// Decisiones de Gonzo (2026-10-23). Salarial en USD mensuales.
const ANSWERS = {
  name: "Gonzalo Blasco",
  email: "gonzoblasco@icloud.com",
  phone: "+54 11 4937 4656",
  location: "Buenos Aires, Argentina",
  org: "Freelance",
  salary: "3200",
  english: "Upper Intermediate",
  additional:
    "I build with AI as infrastructure rather than as a chat: an AI Engineering OS with per-project sessions, persistent memory, subagents and reusable skills, run under a strict quarantine -> analyze -> verify -> adopt method. I also maintain an MCP companion server that lets an agent query what a screen reader actually announces for a snippet of HTML. 11 merged pull requests in production React component libraries (Adobe React Spectrum, IBM Carbon, Meta Astryx, MUI).",
};

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

  console.log("->", APPLY);
  await page.goto(APPLY, { waitUntil: "domcontentloaded", timeout: 45000 });
  await page.waitForTimeout(3500);

  // 1) CV primero: el parser de Lever lee el archivo y rellena solo.
  console.log("[1] subiendo CV (el auto-lector de Lever corre con esto)...");
  const fi = await page.$('input[type="file"]');
  if (!fi) throw new Error("no hay input[type=file]");
  await fi.setInputFiles(CV);
  await page.waitForTimeout(10000);
  console.log("    CV subido y parseado. esperando que el parser asiente...");

  // 2) Campos por name= (Lever usa names estables: name, email, phone, location, org)
  console.log("[2] completando campos por name=");
  for (const [name, value] of [
    ["name", ANSWERS.name],
    ["email", ANSWERS.email],
    ["phone", ANSWERS.phone],
    ["org", ANSWERS.org],
  ]) {
    const el = await page.$(`input[name="${name}"], textarea[name="${name}"]`);
    if (!el) {
      console.log(`    [?] no existe name=${name}`);
      continue;
    }
    await el.click({ clickCount: 3 }).catch(() => {});
    await el.fill(value).catch(async (e) => {
      // los inputs de Lever con autocomplete a veces necesitan type()
      await el.type(value, { delay: 8 }).catch(() => {});
    });
    await page.waitForTimeout(350);
    const got = await el.inputValue().catch(() => "?");
    console.log(`    [${got === value ? "ok" : "REVISAR"}] ${name} = ${JSON.stringify(got)}`);
  }

  // 2b) Ubicacion: autocomplete de Lever. El camino que funciona es el
  //     humano: teclear, esperar el dropdown, y elegir con flecha+Enter.
  //     Con fill() o con click en la opcion, el input VISIBLE queda vacio
  //     (React re-renderiza y borra el valor) aunque el hidden
  //     selectedLocation quede bien. Verificado 2026-10-23: el screenshot
  //     con el metodo de teclado muestra el texto en el campo; con los otros
  //     dos, el campo en blanco.
  console.log("[2b] ubicacion (autocomplete, metodo teclado):");
  const locEl = page.locator('input[name="location"]');
  await locEl.click();
  await locEl.press("Control+a");
  await locEl.type("Buenos Aires", { delay: 70 });
  await page.waitForTimeout(3500);
  // primera sugerencia = "Buenos Aires, Ciudad Autonoma de Buenos Aires, ARG"
  await page.keyboard.press("ArrowDown");
  await page.waitForTimeout(400);
  await page.keyboard.press("Enter");
  await page.waitForTimeout(2500);
  const st = await page.evaluate(() => ({
    location: document.querySelector("input[name=location]")?.value,
    selected: document.querySelector("input[name=selectedLocation]")?.value,
  }));
  const okLoc = !!st.location && !!st.selected;
  console.log(`    [${okLoc ? "ok" : "REVISAR"}] location=${JSON.stringify(st.location)}`);
  console.log(`         selectedLocation=${(st.selected || "").slice(0, 90)}`);

  // 3) Salario: el input real de Lever es name="cards[<id>][field0]" (visible);
  //    hay otro hidden con el mismo label (baseTemplate) que NO se puede
  //    tocar. Por eso se busca por el name del field0 visible. Verificado
  //    2026-10-23 (el selector por label agarra el hidden y falla).
  console.log("[3] salario mensual (USD):");
  const sal = page.locator('input[name*="[field0]"]').first();
  if ((await sal.count()) > 0) {
    await sal.click({ clickCount: 3 }).catch(() => {});
    await sal.fill(ANSWERS.salary);
    await page.waitForTimeout(400);
    const v = await sal.inputValue();
    console.log(`    [${v === ANSWERS.salary ? "ok" : "REVISAR"}] salary = ${JSON.stringify(v)}`);
  } else {
    console.log("    [?] no se encontro el campo de salario");
  }

  // 4) Nivel de ingles: radios CSS. Se marca por etiqueta.
  console.log("[4] nivel de ingles (radio CSS):");
  // Los radios de Lever tienen `value` = texto de la opcion ("Upper Intermediate").
  // Se localiza por value, que es mas estable que por etiqueta.
  const englishOk = await page.evaluate((target) => {
    const r = [...document.querySelectorAll('input[type="radio"]')].find(
      (e) => (e.value || "").trim() === target
    );
    if (!r) return { ok: false, why: "no hay radio con ese value" };
    r.click();
    return { ok: r.checked, why: r.checked ? "" : "el click no lo marco" };
  }, ANSWERS.english);
  console.log(`    [${englishOk.ok ? "ok" : "REVISAR"}] english = ${ANSWERS.english} ${englishOk.why}`);

  // 5) Campo de informacion adicional: es el textarea con name
  //    cards[<id>][field2] (el unico textarea visible del formulario).
  const add = page.locator('textarea[name*="[field2]"]').first();
  if ((await add.count()) > 0) {
    await add.fill(ANSWERS.additional);
    await page.waitForTimeout(300);
    const v = await add.inputValue();
    console.log(`    [${v === ANSWERS.additional ? "ok" : "REVISAR"}] additional (${v.length} chars)`);
  } else {
    console.log("    [?] no se encontro el textarea de informacion adicional");
  }

  // 6) Verificacion: releer TODO el estado del formulario desde la pagina
  const state = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll(".application-question, [class*='application-question']").forEach((q) => {
      const lab = q.querySelector("label, .application-label");
      if (!lab) return;
      const title = lab.textContent.replace(/\s+/g, " ").trim().slice(0, 70);
      const input = q.querySelector("input:not([type=file]), textarea");
      const radio = q.querySelector('input[type="radio"]:checked');
      const file = q.querySelector('input[type="file"]');
      out.push({
        title,
        tipo: radio ? "radio" : file ? "file" : input ? input.tagName.toLowerCase() : "?",
        valor: radio ? radio.value : input ? String(input.value || "").slice(0, 50) : file ? "archivo" : "",
        req: lab.textContent.includes("✱"),
      });
    });
    return out;
  });

  console.log("\n=== ESTADO FINAL DEL FORMULARIO ===");
  state.forEach((q) => {
    console.log(`  [${q.req ? "REQ" : "   "}] ${q.title.padEnd(46)} ${q.tipo.padEnd(7)} ${q.valor}`);
  });

  const cap = await page.evaluate(() => {
    const f = [...document.querySelectorAll("iframe")].map((x) => x.src);
    return {
      hcaptcha: f.some((s) => s.includes("hcaptcha")),
      recaptcha: f.some((s) => s.includes("recaptcha")),
      token: (() => {
        const t = window.hcaptcha && window.hcaptcha.getResponse ? window.hcaptcha.getResponse() : "";
        return (t || "").length;
      })(),
    };
  });
  console.log("\ncaptcha:", JSON.stringify(cap));

  await page.screenshot({ path: SHOT, fullPage: true });
  console.log("captura:", SHOT);

  if (SUBMIT) {
    // Lever responde con el resultado del POST: el veredicto real.
    const respuestas = [];
    page.on("response", async (r) => {
      if (r.request().method() !== "POST") return;
      if (!/lever|ashby|recaptcha|hcaptcha/i.test(r.url())) return;
      try {
        const b = (await r.text()).slice(0, 900);
        if (b) respuestas.push({ status: r.status(), url: r.url().slice(-70), body: b });
      } catch (e) {}
    });
    console.log("\n>>> SUBMIT (envio real)...");
    // Lever tiene DOS button[type=submit]: el visible (btn-submit, "Submit
    // application") y uno OCULTO de hCaptcha (id=hcaptchaSubmitBtn). El
    // selector generico agarra el oculto y falla con timeout. Verificado
    // 2026-10-23.
    await page.locator("button.btn-submit").first().click();
    // El hCaptcha de Lever es invisible: el token se genera en el momento del
    // submit y puede tardar. Se espera mas que en los otros casos.
    await page.waitForTimeout(16000);
    const tok = await page.evaluate(() => {
      const t = window.hcaptcha && window.hcaptcha.getResponse ? window.hcaptcha.getResponse() : "";
      return (t || "").length;
    });
    console.log("token hCaptcha tras submit:", tok);
    const after = await page.evaluate(() => ({
      url: location.href,
      text: document.body.innerText.replace(/\s+/g, " ").slice(0, 400),
    }));
    console.log("URL final:", after.url);
    console.log("texto:", after.text);
    console.log("\n=== RESPUESTAS DEL SERVIDOR ===");
    respuestas.forEach((r) => console.log(`  [${r.status}] ${r.url}\n    ${r.body.slice(0, 500)}`));
    await page.screenshot({
      path: SHOT.replace(".png", "-submitted.png"),
      fullPage: true,
    });
  }

  await browser.close();
  process.exit(0);
})().catch((e) => {
  console.log("ERR", e.message.slice(0, 400));
  process.exit(1);
});
