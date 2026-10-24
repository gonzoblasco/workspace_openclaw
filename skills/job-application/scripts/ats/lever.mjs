// lever.mjs - Adaptador para formularios Lever (ej. RYZ Labs)
//
// POR QUÉ EXISTE (2026-10-23): el script `submit-ryz.js` implementa todo el
// flujo de llenado y envío.  Para la arquitectura modular hicimos un adaptador
// que encapsula esa lógica y la expone con la interfaz genérica esperada por
// `apply.mjs`.

import { fillText, pickRadio, uploadFile } from "../lib/react-form.mjs";
import { hasCaptcha } from "../lib/real-browser.mjs";

export default {
  name: "lever",
  // Detecta URLs de Lever mediante dominio.
  matches(url) {
    try {
      const u = new URL(url);
      return /lever\.co/.test(u.hostname);
    } catch {
      return false;
    }
  },
  /**
   * Rellena el formulario sin enviar.
   * @param {object} page Playwright Page.
   * @param {object} param {answers, files}
   */
  async fill(page, { answers, files }) {
    // Campo de CV (auto‑parser). La lógica completa está en el script de referencia,
    // aquí simplemente subimos el archivo y esperamos.
    const cvInput = page.locator('input[type="file"]');
    await uploadFile(page, cvInput, files.resume);
    // Esperar a que el parser termine (aprox 12 s en producción).
    await page.waitForTimeout(12000);

    // Campos de texto básicos.
    const textMap = {
      name: answers.firstName + " " + answers.lastName,
      email: answers.email,
      phone: answers.phone,
      org: answers.company,
    };
    for (const [name, value] of Object.entries(textMap)) {
      const locator = page.locator(`input[name="${name}"]`).first();
      if ((await locator.count()) === 0) continue;
      await fillText(page, locator, value);
    }

    // Ubicación - usar la técnica de teclear + ArrowDown + Enter.
    const loc = page.locator('input[name="location"]').first();
    if ((await loc.count()) > 0) {
      await loc.click();
      await loc.press("Backspace").catch(() => {});
      await loc.type(answers.city, { delay: 70 });
      await page.waitForTimeout(3500);
      await page.keyboard.press("ArrowDown");
      await page.waitForTimeout(400);
      await page.keyboard.press("Enter");
    }

    // Salario (campo dinámico).
    const salaryLocator = page.locator('input[name*="[field0]"]').first();
    if ((await salaryLocator.count()) > 0) {
      await fillText(page, salaryLocator, answers.salary);
    }

    // Nivel de inglés - radios por texto.
    await page.evaluate((level) => {
      const r = [...document.querySelectorAll('input[type="radio"]')].find((e) => e.value === level);
      if (r) r.click();
    }, answers.englishLevel);

    // Información adicional.
    const add = page.locator('textarea[name*="[field2]"]').first();
    if ((await add.count()) > 0 && answers.coverLetterText) {
      await fillText(page, add, answers.coverLetterText);
    }

    // BUG CORREGIDO 2026-10-23: filled/missing vacios (mismo bug que en
    // Ashby): el reporte no mostraba nada y la verificacion no podia correr.
    const fieldSelectors = [
      'input[name="name"]',
      'input[name="email"]',
      'input[name="phone"]',
      'input[name="org"]',
      'input[name="location"]',
      'input[name*="[field0]"]',
    ];
    const filled = [];
    const missing = [];
    for (const sel of fieldSelectors) {
      const loc = page.locator(sel).first();
      if ((await loc.count()) === 0) {
        missing.push(sel);
        continue;
      }
      const v = await loc.inputValue().catch(() => "");
      if (v && v.trim()) filled.push(sel);
      else missing.push(sel);
    }
    return { ok: missing.length === 0, filled, missing, fieldSelectors, evidence: "", notes: [] };
  },
  /**
   * Envía el formulario y lee el veredicto del servidor.
   */
  async submit(page) {
    // BUG CORREGIDO 2026-10-23: el listener de 'response' se registraba
    // DESPUES del click y del waitForTimeout, o sea cuando la respuesta del
    // servidor ya habia llegado: el veredicto salia siempre vacio. Ahora se
    // registra ANTES de hacer nada, y se busca la respuesta del POST de
    // aplicacion (no la ultima respuesta cualquiera).
    const captured = [];
    const onResponse = async (r) => {
      if (!/lever|hcaptcha|recaptcha/i.test(r.url())) return;
      if (r.request().method() !== "POST") return;
      try {
        captured.push({ status: r.status(), url: r.url(), body: (await r.text()).slice(0, 1200) });
      } catch {}
    };
    page.on("response", onResponse);

    // Click en el botón visible que contiene el texto "Submit".
    const btn = await page.evaluate(() => {
      const b = [...document.querySelectorAll('button')].find((e) => {
        const r = e.getBoundingClientRect();
        const t = (e.textContent || "").replace(/\s+/g, " ").trim().toLowerCase();
        return r.width > 0 && r.height > 0 && t.includes("submit");
      });
      if (b) b.click();
      return b ? true : false;
    });
    await page.waitForTimeout(16000);
    page.off("response", onResponse);
    // El veredicto es el del POST de aplicacion, no la ultima respuesta.
    const post = captured.find((c) => /api|apply|posting|submit/i.test(c.url)) || captured[0];
    const verdict = post ? post.body : "";
    return { ok: btn, verdict, evidence: "", raw: post || null };
  },
};

