// submit-meli.js v3 - Postulacion a Mercado Pago (UX Expert - Software).
//
// CANAL: el boton "Postularme" del portal abre el ATS real (Eightfold):
//   https://mercadolibre.eightfold.ai/careers/apply?pid=44891701
// La vacante se localiza via https://careers-meli.mercadolibre.com/api/positions?country=AR
// (id=44891701, displayJobId 127795).
//
// QUE APRENDI EN LAS v1/v2 (todas verificadas, no supuestas):
//  1. Los campos se identifican por `id`, NO por `name` (name=null en todos).
//  2. Un modal de "Acuerdo de privacidad de datos" bloquea el formulario al
//     inicio: hay que aceptar "Estoy de acuerdo" antes de nada.
//  3. Los desplegables (combobox) NO se llenan con click sintetico: React no
//     lo registra. Hay que elegir la opcion con CLICK REAL DE MOUSE sobre sus
//     coordenadas.
//  4. Los inputs controlados no se limpian con Backspace (el valor se
//     concatena): hay que seleccionar todo con Meta+A y borrar.
//  5. El campo de telefono NO acepta '+' ni espacios. Y con el codigo de
//     pais en +54 espera el numero NACIONAL.
//  6. Al elegir el Pais aparece un campo nuevo: "Estado" (CABA, Cordoba...).
//     Si el pais no queda elegido, ese campo ni existe y el envio falla con
//     "Error: selecciona un Estado".
//  7. El footer sticky tapa los ultimos campos: el click normal da timeout;
//     hay que hacer scrollIntoView y usar click forzado.
//  8. No hay area de texto libre para la presentacion: la presentacion viaja
//     en el CV. Los dos ultimos campos (input-13, input-16) son SI/NO.
//
// Uso: node tmp/job-search-2026-10-22/submit-meli.js [--submit]
const { chromium } = require("/Users/gonzoblasco/.openclaw/workspace/projects/a11y-fixer/node_modules/playwright");

const EXE = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const APPLY = "https://mercadolibre.eightfold.ai/careers/apply?pid=44891701";
const BASE = "/Users/gonzoblasco/.openclaw/workspace";
const CV = `${BASE}/docs/entrevistas/mercadopago-ux-expert/Gonzalo_Blasco_UX_Expert_Software_MercadoPago.pdf`;
const SHOT = `${BASE}/tmp/job-search-2026-10-22/meli-form-filled.png`;
const SUBMIT = process.argv.includes("--submit");

const TEXTO = {
  Informaci_n_de_contacto_email: "gonzoblasco@icloud.com",
  Informaci_n_de_contacto_firstname: "Gonzalo",
  Informaci_n_de_contacto_lastname: "Blasco",
  // Con el codigo de pais en +54, el telefono va NACIONAL: sin '+', sin
  // espacios. (El validador de Eightfold lo rechaza si no.)
  Informaci_n_de_contacto_phone: "1149374656",
  Informaci_n_de_contacto_city: "Buenos Aires",
  Preguntas_sobre_la_solicitud_LinkedIn: "linkedin.com/in/gonzalo-blasco",
};

// Desplegables: query a tipear + texto exacto de la opcion.
const COMBO = {
  "input-10": { q: "Argentina", re: /^Argentina$/i, que: "pais" },
  "input-7": { q: "Argentina", re: /\(\+54\)/i, que: "codigo de pais" },
  "input-13": { q: "Si", re: /^Si$/i, que: "confirmacion de privacidad" },
  "input-16": { q: "No", re: /^No$/i, que: "conflicto de interes" },
};

const typeReal = async (page, el, value) => {
  await el.scrollIntoViewIfNeeded().catch(() => {});
  await el.click({ force: true, timeout: 8000 }).catch(async () => {
    await el.evaluate((e) => e.click());
  });
  await el.evaluate((e) => e.focus());
  await el.evaluate((e) => e.select && e.select());
  await el.press("Meta+A").catch(() => {});
  await el.press("Delete").catch(() => {});
  await el.type(value, { delay: 12 }).catch(async () => {
    await el.fill(value);
  });
  await el.press("Tab").catch(() => {});
  await page.waitForTimeout(250);
  const got = await el.inputValue().catch(() => "?");
  return got === value;
};

// Elige una opcion de un combobox con CLICK REAL DE MOUSE.
const pick = async (page, id, cfg) => {
  const el = page.locator(`#${id}`).first();
  if ((await el.count()) === 0) return { ok: false, msg: "no existe" };
  await el.scrollIntoViewIfNeeded().catch(() => {});
  await el.click({ force: true, timeout: 8000 }).catch(async () => {
    await el.evaluate((e) => e.click());
  });
  await el.press("Delete").catch(() => {});
  await el.type(cfg.q, { delay: 40 }).catch(() => {});
  await page.waitForTimeout(2800);

  const handle = await page.evaluateHandle(
    ({ src }) => {
      const re = new RegExp(src, "i");
      const opts = [...document.querySelectorAll('[role="option"], li, [class*="option"]')].filter((o) => {
        const r = o.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
      });
      const texts = opts.map((o) => (o.textContent || "").replace(/\s+/g, " ").trim());
      const i = texts.findIndex((t) => re.test(t));
      return i >= 0 ? opts[i] : null;
    },
    { src: cfg.re.source }
  );
  const opt = handle.asElement();
  if (!opt) return { ok: false, msg: "opcion no encontrada" };
  const txt = (await opt.innerText().catch(() => "")).replace(/\s+/g, " ").trim();
  await opt.scrollIntoViewIfNeeded().catch(() => {});
  await page.waitForTimeout(400);
  const box = await opt.boundingBox();
  if (box) {
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 6 });
    await page.waitForTimeout(200);
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
  } else {
    await opt.click({ force: true }).catch(() => {});
  }
  await page.waitForTimeout(1800);
  const val = await el.inputValue().catch(() => "");
  return { ok: !!val, msg: txt, val };
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
    locale: "es-AR",
    viewport: { width: 1200, height: 2000 },
  });
  const page = await ctx.newPage();

  const respuestas = [];
  page.on("response", async (r) => {
    if (r.request().method() !== "POST") return;
    if (!/eightfold|apply|application/i.test(r.url())) return;
    if (/vslog/.test(r.url())) return;
    try {
      respuestas.push({ status: r.status(), url: r.url().slice(-70), body: (await r.text()).slice(0, 900) });
    } catch (e) {}
  });

  await page.goto(APPLY, { waitUntil: "domcontentloaded", timeout: 40000 });
  await page.waitForTimeout(10000);
  console.log("->", page.url());

  // 1) modal de privacidad
  const modalOk = await page.evaluate(() => {
    const b = [...document.querySelectorAll("button,a")].find(
      (e) => /estoy de acuerdo/i.test((e.textContent || "").trim()) && e.getBoundingClientRect().width > 0
    );
    if (!b) return false;
    b.click();
    return true;
  });
  await page.waitForTimeout(3500);
  console.log("[1] modal de privacidad:", modalOk ? "aceptado" : "no estaba");

  // 2) CV
  console.log("[2] subiendo CV...");
  const fi = await page.$('input[type="file"]');
  if (fi) {
    await fi.setInputFiles(CV);
    await page.waitForTimeout(9000);
    console.log("    CV:", await fi.evaluate((e) => e.files?.[0]?.name || "(sin archivo)"));
  }

  // 3) PAIS PRIMERO (habilita el campo Estado y el codigo de pais)
  console.log("[3] pais:");
  const rPais = await pick(page, "input-10", COMBO["input-10"]);
  console.log(`    [${rPais.ok ? "ok" : "FALLO"}] ${rPais.msg} -> ${JSON.stringify(rPais.val)}`);
  await page.waitForTimeout(2000);

  // 4) codigo de pais
  console.log("[4] codigo de pais:");
  const rCod = await pick(page, "input-7", COMBO["input-7"]);
  console.log(`    [${rCod.ok ? "ok" : "FALLO"}] ${rCod.msg} -> ${JSON.stringify(rCod.val)}`);

  // 5) ESTADO (aparece al elegir el pais; puede ser id dinamico)
  console.log("[5] estado:");
  const rEstado = await pick(page, "input-11", {
    q: "Ciudad Aut",
    re: /Ciudad Aut[oó]noma de Buenos Aires/i,
  });
  if (rEstado.ok) {
    console.log(`    [ok] ${rEstado.msg} -> ${JSON.stringify(rEstado.val)}`);
  } else {
    // el id del estado puede no ser input-11: se busca el combobox nuevo
    const nuevo = await page.evaluate(() => {
      const cbs = [...document.querySelectorAll('input[role="combobox"]')];
      // el de "Estado" es el que aparece DESPUES de elegir el pais: no esta
      // en la lista fija y suele ser el ultimo de la seccion de contacto.
      const c = cbs.find((x) => !/^input-(7|10|13|16)$/.test(x.id) && x.value === "");
      return c ? c.id : null;
    });
    if (nuevo) {
      const r2 = await pick(page, nuevo, { q: "Ciudad Aut", re: /Ciudad Aut[oó]noma de Buenos Aires/i });
      console.log(`    [${r2.ok ? "ok" : "FALLO"}] ${nuevo} -> ${r2.msg}`);
    } else {
      console.log("    [?] no hay campo de Estado extra");
    }
  }

  // 6) textos
  console.log("[6] textos:");
  for (const [id, value] of Object.entries(TEXTO)) {
    const el = page.locator(`#${id}`).first();
    if ((await el.count()) === 0) {
      console.log(`    [?] no existe ${id}`);
      continue;
    }
    const ok = await typeReal(page, el, value);
    console.log(`    [${ok ? "ok" : "REVISAR"}] ${id} = ${JSON.stringify(await el.inputValue().catch(() => ""))}`);
  }

  // 7) las dos preguntas SI/NO
  console.log("[7] preguntas especificas:");
  for (const id of ["input-13", "input-16"]) {
    const r = await pick(page, id, COMBO[id]);
    console.log(`    [${r.ok ? "ok" : "FALLO"}] ${id} (${COMBO[id].que}) -> ${JSON.stringify(r.msg)}`);
  }

  // 8) WhatsApp
  const wa = await page.evaluate(() => {
    const c = [...document.querySelectorAll('input[type="checkbox"]')].find((x) => /whatsapp/i.test(x.name || ""));
    if (!c) return null;
    if (!c.checked) c.click();
    return c.checked;
  });
  console.log("[8] WhatsApp:", wa === null ? "(no encontrado)" : wa ? "marcado" : "no");

  // 9) estado final
  const estado = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll("input:not([type=file]):not([type=hidden]), textarea, select").forEach((e) => {
      const r = e.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      out.push({
        id: (e.id || e.name || "").slice(0, 44),
        type: e.type || e.tagName,
        val: String(e.value || "").slice(0, 40),
        invalid: e.getAttribute("aria-invalid") === "true",
      });
    });
    return out;
  });
  console.log("\n=== ESTADO ===");
  estado.forEach((c) =>
    console.log(`  ${c.id.padEnd(46)} ${c.type.padEnd(8)} ${JSON.stringify(c.val).padEnd(28)}${c.invalid ? "  <-- INVALIDO" : ""}`)
  );

  const errs = await page.evaluate(() =>
    [...document.querySelectorAll('[role="alert"], [class*="error"]')]
      .map((x) => (x.textContent || "").replace(/\s+/g, " ").trim())
      .filter((t) => t && t.length < 300 && !/^\s*$/.test(t))
      .slice(0, 6)
  );
  console.log("errores visibles:", JSON.stringify(errs, null, 1));

  await page.screenshot({ path: SHOT, fullPage: true });
  console.log("captura:", SHOT);

  if (SUBMIT) {
    console.log("\n>>> SUBMIT (envio real)...");
    const clicked = await page.evaluate(() => {
      const b = [...document.querySelectorAll("button,input[type=submit]")].find((e) => {
        const r = e.getBoundingClientRect();
        const t = (e.textContent || e.value || "").replace(/\s+/g, " ").trim().toLowerCase();
        return r.width > 0 && r.height > 0 && (t === "enviar solicitud" || t === "enviar" || t === "submit");
      });
      if (!b) return false;
      b.click();
      return true;
    });
    console.log("    click:", clicked);
    await page.waitForTimeout(15000);

    console.log("\n=== RESPUESTAS ===");
    respuestas.forEach((r) => console.log(`  [${r.status}] ${r.url}\n    ${r.body.slice(0, 600)}`));

    const fin = await page.evaluate(() => ({
      url: location.href,
      exito:
        /gracias|thank you|postulaci[oó]n (enviada|recibida)|your application has been|recibimos tu|thanks for applying/i.test(
          document.body.innerText
        ),
      alerts: [...document.querySelectorAll('[role="alert"], [class*="error"]')]
        .map((x) => (x.textContent || "").replace(/\s+/g, " ").trim().slice(0, 300))
        .filter(Boolean)
        .slice(0, 5),
      texto: document.body.innerText.replace(/\s+/g, " ").slice(0, 600),
    }));
    console.log("\nURL final:", fin.url);
    console.log("EXITO:", fin.exito);
    console.log("ALERTS:", JSON.stringify(fin.alerts, null, 1));
    console.log("TEXTO:", fin.texto);
    await page.screenshot({ path: SHOT.replace(".png", "-submitted.png"), fullPage: true });
  }

  await browser.close();
  process.exit(0);
})().catch((e) => {
  console.log("ERR", e.message.slice(0, 400));
  process.exit(1);
});
