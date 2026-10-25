// ashby.mjs - Adaptador para formularios Ashby (Mural, etc.)
//
// POR QUÉ EXISTE (2026-10-23): Se extrajo la lógica de `submit-mural.js`
// a un adaptador genérico con la interfaz esperada por `apply.mjs`.

import { fillText, pickOption, pickRadio, uploadFile } from "../lib/react-form.mjs";

export default {
  name: "ashby",
  matches(url) {
    try {
      const u = new URL(url);
      return /ashbyhq\.com/.test(u.hostname);
    } catch {
      return false;
    }
  },
  async fill(page, { answers, files }) {
    // 0) ESPERAR A QUE HIDRATE EL FORMULARIO.
    //
    // BUG CORREGIDO 2026-10-25 (descubierto probando este adaptador): con
    // `domcontentloaded` el DOM de Ashby tiene 0 inputs: el formulario se
    // hidrata ~2s despues. Y el bug de gallina y huevo era que la espera
    // de 12s por el parseo del CV estaba DENTRO del `if` que encuentra el
    // input de CV - pero ese input solo existe despues de hidratar. Sin
    // CV no habia espera, y los textos se escribian contra un formulario
    // vacio: el reporte decia "5 campos faltantes" con la pagina llena.
    //
    // La espera va ACAS, antes de todo, y no depende de nada opcional.
    try {
      await page.waitForSelector('input[name="_systemfield_name"]', { timeout: 20000 });
    } catch (e) {
      throw new Error(
        "el formulario de Ashby no hidrato en 20s (no aparecio el campo de nombre)"
      );
    }

    // 1) Subir CV al panel de autofill (desencadena reCAPTCHA invisible).
    const cvInputHandle = await page.evaluateHandle(() => {
      const ins = [...document.querySelectorAll('input[type="file"]')];
      return ins.find((e) => {
        let n = e;
        for (let i = 0; i < 6 && n; i++) {
          n = n.parentElement;
          if (!n) break;
          if (/autofill from resume/i.test(n.innerText || "")) return true;
        }
        return false;
      }) || null;
    });
    const cvEl = cvInputHandle.asElement();
    if (cvEl) {
      await cvEl.setInputFiles(files.resume);
      // esperar al parseo del CV (aprox 12 s).
      await page.waitForTimeout(12000);
    } else {
      // Sin panel de autofill: no hay parseo que esperar, pero el
      // formulario ya hidrato (por el waitForSelector de arriba).
      await page.waitForTimeout(1500);
    }

    // 2) Rellenar textos por name usando type().
    const TEXTOS = {
      _systemfield_name: answers.firstName + " " + answers.lastName,
      _systemfield_email: answers.email,
      "2c6cb798-c815-4405-a439-f89427f47e6e": answers.phone,
      "d7ce58e9-6422-4759-b15c-3fb2c4759def": answers.linkedin,
      "6bb011c6-ca94-44ce-a0a1-41f0afec07a2": answers.salary,
    };
    for (const [name, value] of Object.entries(TEXTOS)) {
      const loc = page.locator(`input[name="${name}"]`).first();
      if ((await loc.count()) === 0) continue;
      await fillText(page, loc, value);
    }

    // 3) Location - combobox. Su autocomplete SOLO reconoce "Argentina" y
    // "Nunez" (NO "Buenos Aires": devuelve "No results"). Medido 2026-10-23.
    // BUG CORREGIDO 2026-10-23: se hacia click por JS dentro del listbox y
    // React no lo registra: el valor quedaba en "". Ahora se usa pickOption,
    // que hace click REAL de mouse sobre las coordenadas de la opcion.
    const combo = page.locator('input[role="combobox"]').first();
    if ((await combo.count()) > 0) {
      await pickOption(page, combo, { q: "Argentina", re: /^Argentina$/i }, '[role="listbox"]');
      await page.waitForTimeout(2500);
    }

    // 4) Radios y checkbox.
    const RADIOS = [
      ["_e7e51cb6", 0, "autorizado a trabajar: Yes"],
      ["_b3a08088", 1, "depende de patrocinio: No"],
      ["eeoc_gender", 2, "genero: Decline to self-identify"],
      ["eeoc_race", 7, "etnia: Decline to self-identify"],
      ["eeoc_veteran_status", 2, "veterano: I decline to self-identify"],
    ];
    for (const [key, idx] of RADIOS) {
      const loc = page.locator(`input[type="radio"][name*="${key}"]`).nth(idx);
      await pickRadio(page, loc);
    }
    // Checkbox "I agree"
    const agree = page.locator('input[type="checkbox"][name="I agree"]').first();
    if ((await agree.count()) > 0) {
      await agree.check({ force: true }).catch(() => {});
    }

    // 5) Adjuntar CV y Cover Letter (si existen).
    const attach = async (label, path) => {
      const handle = await page.evaluateHandle((txt) => {
        const ins = [...document.querySelectorAll('input[type="file"]')];
        for (const e of ins) {
          let n = e;
          for (let k = 0; k < 6 && n; k++) {
            n = n.parentElement;
            if (!n) break;
            const inner = (n.innerText || "").replace(/\s+/g, " ").trim();
            if (inner.toLowerCase().startsWith(txt.toLowerCase())) return e;
          }
        }
        return null;
      }, label);
      const el = handle.asElement();
      if (el) {
        await el.setInputFiles(path);
        await page.waitForTimeout(3000);
      }
    };
    await attach("Resume", files.resume);
    if (files.coverLetter) await attach("Cover Letter", files.coverLetter);

    // BUG CORREGIDO 2026-10-23: se devolvian filled/missing VACIOS, asi
    // que el reporte no decia que se lleno y la verificacion DOM-vs-React no
    // tenia contra que correr (el orquestador la pide por fieldSelectors).
    const fieldSelectors = [
      'input[name="_systemfield_name"]',
      'input[name="_systemfield_email"]',
      'input[name="2c6cb798-c815-4405-a439-f89427f47e6e"]',
      'input[name="d7ce58e9-6422-4759-b15c-3fb2c4759def"]',
      'input[name="6bb011c6-ca94-44ce-a0a1-41f0afec07a2"]',
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
    // Verificacion de los radios: no alcanza con que el click "no tirara
    // error". Se lee que opcion quedo marcada en cada grupo, por el texto
    // de su etiqueta. Es la unica forma de saber que se marco la que
    // correspondia y no otra del mismo grupo.
    const radios = await page.evaluate(() => {
      const out = {};
      document.querySelectorAll('input[type="radio"]').forEach((r) => {
        if (!r.checked) return;
        const lab = r.closest("label") || document.querySelector(`label[for="${r.id}"]`);
        const txt = (lab ? lab.textContent : r.value).replace(/\s+/g, " ").trim().slice(0, 50);
        // El name COMPLETO del grupo: Ashby le antepone el id del
        // formulario ("<uuid>_e7e51cb6-...") y truncarlo"_"-hacia que
        // "veteran_status" se confundiera con "eeoc_veteran_status" y el
        // gate creyera que faltaba un radio que estaba bien.
        out[r.name || "(sin name)"] = txt;
      });
      return out;
    });
    // Se busca el grupo por el fragmento que aparece en el name completo.
    const radioEsperados = [
      ["_e7e51cb6-", "Yes"],
      ["_b3a08088-", "No"],
      ["eeoc_gender", "Decline to self-identify"],
      ["eeoc_race", "Decline to self-identify"],
      ["eeoc_veteran_status", "I decline to self-identify for protected veteran status"],
    ];
    const radiosOk = radioEsperados.every(([k, v]) => {
      const marcado = Object.entries(radios).find(([g]) => g.includes(k));
      return marcado && marcado[1].startsWith(v.slice(0, 18));
    });
    if (!radiosOk) {
      missing.push("radios: alguna pregunta de opcion multiple quedo sin marcar como se pedia");
    }

    return {
      ok: missing.length === 0,
      filled,
      missing,
      fieldSelectors,
      evidence: "",
      radios,
      notes: [],
    };
  },
  async submit(page) {
    // BUG CORREGIDO 2026-10-23: el listener se registraba DESPUES del click
    // y del wait: la respuesta GraphQL ya habia llegado y el veredicto
    // salia vacio. Ahora se registra antes y se busca la accion de submit.
    const captured = [];
    const onResponse = async (r) => {
      if (!r.url().includes("ApiSubmitMultipleFormsAction")) return;
      try {
        captured.push({ status: r.status(), url: r.url(), body: (await r.text()).slice(0, 2000) });
      } catch {}
    };
    page.on("response", onResponse);

    const btn = await page.evaluate(() => {
      const b = document.querySelector('button[role="button"]');
      if (b && /submit/i.test(b.textContent || "")) { b.click(); return true; }
      return false;
    });
    await page.waitForTimeout(15000);
    page.off("response", onResponse);
    const verdict = captured.length ? captured[captured.length - 1].body : "";
    return { ok: btn, verdict, evidence: "", raw: captured[0] || null };
  },
};

