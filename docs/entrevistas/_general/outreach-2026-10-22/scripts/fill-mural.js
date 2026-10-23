// fill-mural.js v4 - Mural (Ashby) sin el panel de autofill.
//
// Por que v4 (2026-10-23): despues de v3 (que completaba todo y aun asi
// devolvia "9 fields missing required information"), el problema NO era el
// typing (verificado: el _valueTracker de React queda con el valor correcto)
// sino el PANEL DE AUTOFILL. Al subir el CV ahi, Ashby lanza un parseo
// asincrono ("Parsing your resume. Autofilling key fields...") que
// SOBREESCRIBE el estado del formulario despues de que uno ya escribio.
// El upload del CV va unicamente al campo "Resume" que pide el formulario;
// el autofill es opcional.
//
// Uso: node tmp/job-search-2026-10-22/fill-mural.js [--submit]
const { chromium } = require("/Users/gonzoblasco/.openclaw/workspace/projects/a11y-fixer/node_modules/playwright");
const path = require("path");

const EXE = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const APPLY = "https://jobs.ashbyhq.com/mural/3493ea21-5b96-4383-964a-996249db3a14/application";
const BASE = "/Users/gonzoblasco/.openclaw/workspace";
const CV = path.resolve(`${BASE}/docs/entrevistas/mural-growth-senior-swe/Gonzalo_Blasco_Senior_SWE_Growth_Mural.pdf`);
const COVER = path.resolve(`${BASE}/tmp/job-search-2026-10-22/cover-letter-mural.pdf`);
const SHOT = `${BASE}/tmp/job-search-2026-10-22/mural-form-filled.png`;
const SUBMIT = process.argv.includes("--submit");

const ANSWERS = {
  name: "Gonzalo Blasco",
  email: "gonzoblasco@icloud.com",
  phone: "+54 11 4937 4656",
  location: "Núñez, Buenos Aires, Argentina",
  linkedin: "linkedin.com/in/gonzalo-blasco",
  salary: "3400",
};

const RADIO_GROUPS = [
  { key: "_e7e51cb6", index: 0, label: "autorizado a trabajar: Yes" },
  { key: "_b3a08088", index: 1, label: "depende de patrocinio: No" },
  { key: "eeoc_gender", index: 2, label: "genero: Decline" },
  { key: "eeoc_race", index: 7, label: "etnia: Decline" },
  { key: "eeoc_veteran_status", index: 2, label: "veterano: Decline" },
];

// typing real: el _valueTracker de React tiene que quedar con el valor.
const typeReal = async (el, value) => {
  await el.click({ clickCount: 3 }).catch(() => {});
  await el.press("Backspace").catch(() => {});
  try {
    await el.type(value, { delay: 14 });
  } catch (e) {
    await el.fill(value);
  }
  await el.press("Tab").catch(() => {});
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
    viewport: { width: 1280, height: 1800 },
  });
  const page = await ctx.newPage();

  console.log("->", APPLY);
  await page.goto(APPLY, { waitUntil: "networkidle", timeout: 45000 });
  await page.waitForTimeout(3500);

  // ---------------------------------------------------------------- 1. archivos
  // Se adjuntan a sus campos por el texto del ancestro. NO se toca el panel
  // de autofill: su parseo asincrono pisa el estado del formulario.
  // ---------------------------------------------------------------- 1. CV al panel de autofill
  // Orden IMPORTANTE (verificado 2026-10-23):
  //   a) el CV al panel de autofill dispara el reCAPTCHA invisible. Sin
  //      token, Ashby no procesa el submit (por eso el v4 no confirmaba:
  //      g-recaptcha-response estaba vacio).
  //   b) pero su parseo asincrono SOBREESCRIBE los textos del formulario.
  //   Por eso el CV va PRIMERO, se espera a que termine, y recien despues
  //   se escriben los textos (con type(), que deja el _valueTracker de React
  //   consistente) y se re-adjuntan los archivos.
  console.log("[1] CV al panel de autofill (dispara el reCAPTCHA):");
  const headHandle = await page.evaluateHandle(() => {
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
  const headEl = headHandle.asElement();
  if (headEl) {
    await headEl.setInputFiles(CV);
    await page.waitForTimeout(14000);
    const tok = await page.evaluate(() => {
      const t = document.querySelector("textarea[name^=g-recaptcha]");
      return t && t.value ? t.value.length : 0;
    });
    const af = await page.evaluate(() => /autofill completed/i.test(document.body.innerText));
    console.log(`    autofill=${af} | token reCAPTCHA=${tok}`);
  }

  console.log("[1b] adjuntando archivos a sus campos:");
  const uploadByField = async (fieldText, file, humanName) => {
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
    }, fieldText);
    const el = h.asElement();
    if (!el) {
      console.log(`    [?] no se encontro el campo ${humanName}`);
      return false;
    }
    await el.setInputFiles(file);
    await page.waitForTimeout(3000);
    const st = await el.evaluate((e) => ({ n: e.files.length, name: e.files[0]?.name || null }));
    console.log(`    [${st.n ? "ok" : "FALLO"}] ${humanName} -> ${st.name}`);
    return st.n > 0;
  };
  await uploadByField("Resume", CV, "Resume");
  await uploadByField("Cover Letter", COVER, "Cover Letter");

  // ---------------------------------------------------------------- 2. textos
  console.log("[2] textos:");
  const fillByName = async (name, value) => {
    const el = page.locator(`input[name="${name}"], textarea[name="${name}"]`).first();
    if ((await el.count()) === 0) {
      console.log(`    [?] no existe name=${name}`);
      return;
    }
    await typeReal(el, value);
    await page.waitForTimeout(250);
    const got = await el.inputValue().catch(() => "?");
    const tracked = await el.evaluate((e) => {
      const t = e._valueTracker;
      return t && t.getValue ? String(t.getValue()) : "";
    });
    console.log(
      `    [${got === value ? "ok" : "REVISAR"}] ${name} = ${JSON.stringify(got)}  [react=${JSON.stringify(tracked.slice(0, 24))}]`
    );
  };
  const fillByLabel = async (labelText, value) => {
    const h = await page.evaluateHandle((lt) => {
      const labels = [...document.querySelectorAll("label, [class*='label']")];
      const l = labels.find((x) =>
        x.textContent.replace(/\s+/g, " ").trim().toLowerCase().includes(lt.toLowerCase())
      );
      if (!l) return null;
      const id = l.getAttribute("for");
      if (id) {
        const el = document.getElementById(id);
        if (el) return el;
      }
      const scope = l.closest("div") || document;
      return scope.querySelector("input:not([type=file]):not([type=radio]), textarea");
    }, labelText);
    const el = h.asElement();
    if (!el) {
      console.log(`    [?] no encontrado: ${labelText}`);
      return;
    }
    await typeReal(el, value);
    await page.waitForTimeout(250);
    const got = await el.inputValue().catch(() => "?");
    console.log(`    [${got === value ? "ok" : "REVISAR"}] ${labelText} = ${JSON.stringify(got)}`);
  };

  await fillByName("_systemfield_name", ANSWERS.name);
  await fillByName("_systemfield_email", ANSWERS.email);
  await fillByLabel("Telephone Number", ANSWERS.phone);
  // Location es un COMBOBOX con autocompletado (role=combobox,
  // aria-autocomplete=list). Teclear no alcanza: hay que elegir una
  // sugerencia del dropdown, igual que el campo de ubicacion de Lever.
  // El autocomplete de Ashby NO reconoce "Buenos Aires" (devuelve "No
  // results"); solo "Argentina" y "Nunez" traen resultados. El dropdown se
  // renderiza en un portal con role=listbox, y sus items NO tienen
  // role=option: hay que leer las hojas de texto del listbox. Verificado
  // 2026-10-23 con una sonda dedicada.
  const locEl = page.locator('input[role="combobox"]').first();
  if ((await locEl.count()) > 0) {
    await locEl.click();
    await locEl.press("Backspace").catch(() => {});
    await locEl.type("Argentina", { delay: 60 });
    await page.waitForTimeout(4000);
    const picked = await page.evaluate(() => {
      const lb = document.querySelector("[role=listbox]");
      if (!lb) return null;
      const items = [...lb.querySelectorAll("*")]
        .filter((e) => e.children.length === 0 && (e.textContent || "").trim().length > 1)
        .map((e) => ({ el: e, txt: e.textContent.replace(/\s+/g, " ").trim() }));
      const hit = items.find((i) => /^Argentina$/i.test(i.txt));
      if (!hit) return null;
      hit.el.click();
      return hit.txt;
    });
    await page.waitForTimeout(2500);
    const locVal = await locEl.inputValue().catch(() => "");
    const locReact = await locEl.evaluate((e) => {
      const t = e._valueTracker;
      return t && t.getValue ? String(t.getValue()) : "(sin tracker)";
    });
    console.log(
      `    [${locVal ? "ok" : "REVISAR"}] Location = ${JSON.stringify(locVal)} (react=${JSON.stringify(locReact)}) opcion=${JSON.stringify(picked)}`
    );
  } else {
    console.log("    [?] no se encontro el combobox de Location");
  }
  await fillByLabel("LinkedIn Profile", ANSWERS.linkedin);
  await fillByLabel("desired salary expectations", ANSWERS.salary);

  // ---------------------------------------------------------------- 3. radios
  console.log("[3] radios:");
  for (const g of RADIO_GROUPS) {
    const loc = page.locator(`input[type="radio"][name*="${g.key}"]`).nth(g.index);
    let ok = false;
    try {
      await loc.check({ force: true, timeout: 5000 });
      ok = await loc.isChecked();
    } catch (e) {
      ok = false;
    }
    if (!ok) {
      try {
        await loc.evaluate((r) => {
          const lab = r.closest("label") || document.querySelector(`label[for="${r.id}"]`);
          if (lab) lab.click();
        });
        await page.waitForTimeout(400);
        ok = await loc.isChecked();
      } catch (e) {
        ok = false;
      }
    }
    console.log(`    [${ok ? "ok" : "FALLO"}] ${g.label}`);
  }
  const cb = page.locator('input[type="checkbox"][name="I agree"]');
  let cbOk = false;
  try {
    await cb.check({ force: true, timeout: 5000 });
    cbOk = await cb.isChecked();
  } catch (e) {
    cbOk = false;
  }
  console.log(`    [${cbOk ? "ok" : "FALLO"}] I agree`);

  // ---------------------------------------------------------------- 4. estado
  const state = await page.evaluate(() => {
    const out = { campos: [], grupos: {}, checkboxes: {}, archivos: [] };
    document.querySelectorAll("input, textarea").forEach((i) => {
      if (i.type === "radio") {
        if (!out.grupos[i.name]) out.grupos[i.name] = { checked: 0, opts: 0 };
        out.grupos[i.name].opts++;
        if (i.checked) out.grupos[i.name].checked++;
        return;
      }
      if (i.type === "checkbox") {
        out.checkboxes[i.name || "(sin name)"] = i.checked;
        return;
      }
      if (i.type === "file") {
        let field = "(desconocido)";
        let n = i;
        for (let k = 0; k < 6 && n; k++) {
          n = n.parentElement;
          if (!n) break;
          const t = (n.innerText || "").replace(/\s+/g, " ").trim();
          if (/^resume/i.test(t)) { field = "Resume"; break; }
          if (/^cover letter/i.test(t)) { field = "Cover Letter"; break; }
        }
        out.archivos.push({ campo: field, archivo: i.files?.[0]?.name || null });
        return;
      }
      const t = i._valueTracker;
      out.campos.push({
        name: (i.name || i.id || "").slice(0, 40),
        tipo: i.type,
        dom: String(i.value || "").slice(0, 34),
        react: t && t.getValue ? String(t.getValue()).slice(0, 34) : "",
        req: i.required,
      });
    });
    return out;
  });

  console.log("\n=== ESTADO (DOM vs estado de React) ===");
  state.campos.forEach((c) => {
    const ok = c.react ? (c.react === c.dom ? "ok" : "DIVERGE") : "s/tracker";
    console.log(
      `  [${ok.padEnd(7)}] ${String(c.name).padEnd(38)} dom=${JSON.stringify(c.dom).padEnd(20)} react=${JSON.stringify(c.react)}`
    );
  });
  console.log("  archivos:", JSON.stringify(state.archivos));
  console.log("  checkboxes:", JSON.stringify(state.checkboxes));
  let radiosOk = true;
  Object.entries(state.grupos).forEach(([n, g]) => {
    if (g.checked !== 1) radiosOk = false;
  });
  const divergentes = state.campos.filter((c) => c.react && c.react !== c.dom).length;
  console.log(`\n  RADIOS: ${radiosOk ? "OK" : "FALTAN"} | DIVERGENTES DOM/React: ${divergentes}`);

  await page.screenshot({ path: SHOT, fullPage: true });
  console.log("captura:", SHOT);

  if (SUBMIT) {
    console.log("\n>>> SUBMIT (envio real)...");
    await page.getByRole("button", { name: "Submit Application", exact: true }).first().click();
    await page.waitForTimeout(11000);
    const after = await page.evaluate(() => {
      // El recuadro de error de Ashby: el bloque con "Your form needs corrections"
      // o la lista de "Missing entry for required field: X".
      const faltantes = [...document.querySelectorAll("li, p, span")]
        .map((x) => (x.textContent || "").replace(/\s+/g, " ").trim())
        .filter((t) => /missing entry for required field/i.test(t) && t.length < 200);
      const exito = /application (was )?submitted|thank you for applying|we (have )?received your application|thanks for applying/i.test(
        document.body.innerText
      );
      const banner = [...document.querySelectorAll('[role="alert"], [class*="success"], [class*="error"]')]
        .map((x) => (x.textContent || "").replace(/\s+/g, " ").trim().slice(0, 200))
        .filter(Boolean);
      return {
        url: location.href,
        exito,
        faltantes: [...new Set(faltantes)],
        banner: banner.slice(0, 4),
        texto: document.body.innerText.replace(/\s+/g, " ").slice(0, 400),
      };
    });
    console.log("URL final:", after.url);
    console.log("EXITO:", after.exito);
    console.log("faltantes:", JSON.stringify(after.faltantes, null, 1));
    console.log("banner:", JSON.stringify(after.banner, null, 1));
    await page.screenshot({ path: SHOT.replace(".png", "-submitted.png"), fullPage: true });
  }

  await browser.close();
  process.exit(0);
})().catch((e) => {
  console.log("ERR", e.message.slice(0, 400));
  process.exit(1);
});
