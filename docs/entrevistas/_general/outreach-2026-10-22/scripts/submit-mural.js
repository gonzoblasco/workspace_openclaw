// submit-mural.js - Envio final de la postulacion a Mural (Ashby).
//
// Por que este script existe (2026-10-23): la v5 completaba los campos por
// LABEL y el servidor respondia "Missing entry for required field:
// Telephone Number / LinkedIn Profile / desired salary" - tres campos que
// se veian llenos en pantalla. La causa: el selector por label就打 el input
// equivocado (el ancestro mas cercano con texto no es el del campo), y el
// estado de React queda sin registrar.
//
// El fix: los textos se localizan por `name` (estable) y se escriben con
// `type()` (que deja el _valueTracker consistente). Los radios por indice
// dentro de su grupo, con click real. Location por combobox ("Argentina",
// que es lo unico que el autocomplete de Ashby reconoce).
//
// ORDEN (importante):
//   1) CV al panel de autofill -> dispara el reCAPTCHA invisible (sin token
//      el submit no se procesa) y parsea el CV.
//   2) esperar a que el autofill termine.
//   3) escribir TODOS los textos con type() (el autofill los pisa).
//   4) radios + checkbox + archivos (el autofill tambien los resetea).
//   5) verificar DOM vs estado de React.
//   6) submit, y capturar la respuesta GraphQL, que es el veredicto.
//
// Uso: node tmp/job-search-2026-10-22/submit-mural.js
const { chromium } = require("/Users/gonzoblasco/.openclaw/workspace/projects/a11y-fixer/node_modules/playwright");
const path = require("path");

const EXE = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const APPLY = "https://jobs.ashbyhq.com/mural/3493ea21-5b96-4383-964a-996249db3a14/application";
const BASE = "/Users/gonzoblasco/.openclaw/workspace";
const CV = `${BASE}/docs/entrevistas/mural-growth-senior-swe/Gonzalo_Blasco_Senior_SWE_Growth_Mural.pdf`;
const COVER = `${BASE}/tmp/job-search-2026-10-22/cover-letter-mural.pdf`;
const SHOT = `${BASE}/tmp/job-search-2026-10-22/mural-form-filled.png`;

// name -> valor. Los `name` de Ashby son UUID estables.
const TEXTOS = {
  _systemfield_name: "Gonzalo Blasco",
  _systemfield_email: "gonzoblasco@icloud.com",
  "2c6cb798-c815-4405-a439-f89427f47e6e": "+54 11 4937 4656",
  "d7ce58e9-6422-4759-b15c-3fb2c4759def": "linkedin.com/in/gonzalo-blasco",
  "6bb011c6-ca94-44ce-a0a1-41f0afec07a2": "3400",
};

// grupo -> indice de la opcion. Los `value` de los radios de Ashby son todos
// "on", as que la unica forma de distinguirlos es por posicion.
const RADIOS = [
  ["_e7e51cb6", 0, "autorizado a trabajar: Yes"],
  ["_b3a08088", 1, "depende de patrocinio: No"],
  ["eeoc_gender", 2, "genero: Decline to self-identify"],
  ["eeoc_race", 7, "etnia: Decline to self-identify"],
  ["eeoc_veteran_status", 2, "veterano: I decline to self-identify"],
];

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
    viewport: { width: 1280, height: 1800 },
  });
  const page = await ctx.newPage();

  let graphql = null;
  page.on("response", async (r) => {
    if (!r.url().includes("ApiSubmitMultipleFormsAction")) return;
    try {
      graphql = { status: r.status(), body: (await r.text()).slice(0, 2500) };
    } catch (e) {}
  });

  await page.goto(APPLY, { waitUntil: "networkidle", timeout: 45000 });
  await page.waitForTimeout(3000);

  // 1) CV al panel de autofill (dispara el reCAPTCHA)
  console.log("[1] CV al panel de autofill...");
  const head = await page.evaluateHandle(() => {
    const ins = [...document.querySelectorAll('input[type="file"]')];
    return (
      ins.find((e) => {
        let n = e;
        for (let k = 0; k < 6 && n; k++) {
          n = n.parentElement;
          if (!n) break;
          if (/autofill from resume/i.test(n.innerText || "")) return true;
        }
        return false;
      }) || null
    );
  });
  await head.asElement().setInputFiles(CV);
  await page.waitForTimeout(15000);
  const tok0 = await page.evaluate(() => {
    const t = document.querySelector("textarea[name^=g-recaptcha]");
    return t && t.value ? t.value.length : 0;
  });
  console.log(`    token reCAPTCHA=${tok0}`);

  // 2) textos por name, con type()
  console.log("[2] textos (por name, con type):");
  for (const [name, value] of Object.entries(TEXTOS)) {
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
    console.log(`    [${dom === value && react === value ? "ok" : "REVISAR"}] ${dom} (react=${react})`);
  }

  // 3) Location: combobox. El autocomplete de Ashby solo reconoce
  //    "Argentina" (devuelve "No results" para "Buenos Aires").
  console.log("[3] Location:");
  const cb = page.locator('input[role="combobox"]').first();
  await cb.click();
  await cb.press("Backspace").catch(() => {});
  await cb.type("Argentina", { delay: 60 });
  await page.waitForTimeout(4000);
  await page.evaluate(() => {
    const lb = document.querySelector("[role=listbox]");
    if (!lb) return;
    const it = [...lb.querySelectorAll("*")].find(
      (e) => e.children.length === 0 && /^Argentina$/i.test((e.textContent || "").trim())
    );
    if (it) it.click();
  });
  await page.waitForTimeout(2500);
  console.log(`    Location = ${JSON.stringify(await cb.inputValue().catch(() => ""))}`);

  // 4) radios + checkbox
  console.log("[4] radios:");
  for (const [key, idx, label] of RADIOS) {
    const loc = page.locator(`input[type="radio"][name*="${key}"]`).nth(idx);
    let ok = false;
    try {
      await loc.check({ force: true, timeout: 5000 });
      ok = await loc.isChecked();
    } catch (e) {}
    if (!ok) {
      await loc
        .evaluate((r) => {
          const lab = r.closest("label") || document.querySelector(`label[for="${r.id}"]`);
          if (lab) lab.click();
        })
        .catch(() => {});
      await page.waitForTimeout(400);
      ok = await loc.isChecked();
    }
    console.log(`    [${ok ? "ok" : "FALLO"}] ${label}`);
  }
  await page
    .locator('input[type="checkbox"][name="I agree"]')
    .check({ force: true, timeout: 5000 })
    .catch(() => {});
  await page.waitForTimeout(400);

  // 5) archivos a sus campos (por texto de ancestro)
  console.log("[5] archivos:");
  for (const [txt, file] of [
    ["Resume", CV],
    ["Cover Letter", COVER],
  ]) {
    const h = await page.evaluateHandle((ft) => {
      const ins = [...document.querySelectorAll('input[type="file"]')];
      for (const e of ins) {
        let n = e;
        for (let k = 0; k < 6 && n; k++) {
          n = n.parentElement;
          if (!n) break;
          const t = (n.innerText || "").replace(/\s+/g, " ").trim();
          if (t.toLowerCase().startsWith(ft.toLowerCase())) return e;
        }
      }
      return null;
    }, txt);
    const el = h.asElement();
    if (el) {
      await el.setInputFiles(file);
      await page.waitForTimeout(3000);
      const st = await el.evaluate((e) => e.files[0]?.name || null);
      console.log(`    [${st ? "ok" : "FALLO"}] ${txt} -> ${st}`);
    } else {
      console.log(`    [?] no se encontro ${txt}`);
    }
  }

  // 6) verificacion
  const verif = await page.evaluate(() => {
    const divergentes = [];
    document.querySelectorAll("input:not([type=file]):not([type=radio]):not([type=checkbox]), textarea").forEach((i) => {
      const t = i._valueTracker;
      const react = t && t.getValue ? String(t.getValue()) : "";
      if (react && react !== String(i.value || "")) {
        divergentes.push({ name: (i.name || i.id || "").slice(0, 40), dom: i.value, react });
      }
    });
    let radiosVacios = 0;
    document.querySelectorAll('input[type="radio"]').forEach((r) => {
      if (!r.checked) radiosVacios++;
    });
    const tok = document.querySelector("textarea[name^=g-recaptcha]");
    return {
      divergentes,
      radiosNoMarcados: radiosVacios,
      tokenRecaptcha: tok && tok.value ? tok.value.length : 0,
    };
  });
  console.log(
    `\n[6] divergentes=${verif.divergentes.length} radiosSinMarcar=${verif.radiosNoMarcados} token=${verif.tokenRecaptcha}`
  );
  if (verif.divergentes.length) console.log("   ", JSON.stringify(verif.divergentes));

  await page.screenshot({ path: SHOT, fullPage: true });

  // 7) submit
  console.log("\n>>> SUBMIT");
  await page.getByRole("button", { name: "Submit Application", exact: true }).first().click();
  await page.waitForTimeout(14000);

  console.log("\n=== RESPUESTA DEL SERVIDOR ===");
  if (graphql) {
    console.log("status:", graphql.status);
    let parsed = null;
    try {
      parsed = JSON.parse(graphql.body.split("\n").find((l) => l.trim().startsWith("{")) || graphql.body);
    } catch (e) {}
    const res = parsed?.data?.submitMultipleFormsAction?.applicationFormResult;
    if (res) {
      console.log("id de la postulacion:", res.id);
      console.log("errorMessages:", JSON.stringify(res.errorMessages || [], null, 1));
      console.log("fields:", JSON.stringify(res.fields || {}, null, 1).slice(0, 400));
    } else {
      console.log(graphql.body.slice(0, 900));
    }
  } else {
    console.log("(no se capturo la respuesta GraphQL)");
  }

  const fin = await page.evaluate(() => ({
    url: location.href,
    alerts: [...document.querySelectorAll('[role="alert"]')].map((x) =>
      x.textContent.replace(/\s+/g, " ").trim().slice(0, 400)
    ),
    exito:
      /application (was )?submitted|thank you for applying|we (have )?received your application|thanks for applying|your application has been/i.test(
        document.body.innerText
      ),
    texto: document.body.innerText.replace(/\s+/g, " ").slice(0, 600),
  }));
  console.log("\nURL final:", fin.url);
  console.log("EXITO:", fin.exito);
  console.log("ALERTS:", JSON.stringify(fin.alerts, null, 1));
  console.log("TEXTO:", fin.texto);

  await page.screenshot({ path: SHOT.replace(".png", "-submitted.png"), fullPage: true });
  console.log("captura:", SHOT.replace(".png", "-submitted.png"));

  await browser.close();
  process.exit(0);
})().catch((e) => {
  console.log("ERR", e.message.slice(0, 400));
  process.exit(1);
});
