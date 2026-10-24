// eightfold.mjs - Adaptador para formularios Eightfold (Mercado Pago)
//
// POR QUÉ EXISTE (2026-10-23): similar a `ashby.mjs` pero los campos se
// identifican por `id` (no por `name`).  Se implementa la lógica mínima
// requerida por `apply.mjs` para rellenar y enviar.

import { fillText, pickOption, pickRadio, uploadFile } from "../lib/react-form.mjs";

export default {
  name: "eightfold",
  matches(url) {
    try {
      const u = new URL(url);
      return /eightfold\.ai/.test(u.hostname);
    } catch {
      return false;
    }
  },
  async fill(page, { answers, files }) {
    // Modal de privacidad - aceptar si existe.
    const modalOk = await page.evaluate(() => {
      const btn = [...document.querySelectorAll('button,a')].find((e) => /estoy de acuerdo/i.test((e.textContent || "").trim()) && e.getBoundingClientRect().width > 0);
      if (btn) btn.click();
      return !!btn;
    });
    if (modalOk) await page.waitForTimeout(3500);

    // Subir CV (trigger de parseo).
    // BUG CORREGIDO 2026-10-23 (tercera ronda): el CV NO se adjuntaba.
    // El input[type=file] de Eightfold es `display: none` (es el input de un
    // dropzone) y hay VARIOS en el DOM: uno pertenece al modal de privacidad
    // y otro al campo CV. La secuencia que funciona (medida contra el
    // script de referencia, que si adjunto el CV) es: aceptar el modal
    // PRIMERO, esperar a que se desmonte el modal, y recien ahi tomar el
    // input de archivo y adjuntar. Antes se tomaba el input antes de tiempo
    // (o se filtraba por "visible", y con display:none no hay ninguno).
    // BUG CORREGIDO 2026-10-23 (cuarta ronda): el CV seguia sin adjuntar.
    // La diferencia con el script de referencia (que SI lo adjunta) es el
    // TIPO de handle: `page.$()` devuelve un ElementHandle y
    // `locator.setInputFiles()` no. El input de Eightfold es `display: none`
    // (es el input de un dropzone) y el Locator lo descarta por visibilidad.
    // Con ElementHandle el adjunto funciona.
    const cvHandle = await page.$('input[type="file"]');
    if (cvHandle) {
      await cvHandle.setInputFiles(files.resume);
      await page.waitForTimeout(9000);
    } else {
      const first = page.locator('input[type="file"]').first();
      if ((await first.count()) > 0) {
        await first.setInputFiles(files.resume);
        await page.waitForTimeout(9000);
      }
    }

    // 0) CODIGO DE PAIS (input-7, aria-label "Codigo del pais"): es el
    //    prefijo del TELEFONO ("(+54) Argentina"), NO el pais de la vacante.
    //    BUG CORREGIDO 2026-10-23: estaban al reves, y por eso el telefono
    //    quedaba sin prefijo ("1149374656" suelto) y el pais nunca se
    //    elegia. Son dos comboboxes distintos.
    //    Los desplegables de Eightfold NO toman el valor con click sintetico
    //    (React no lo registra): pickOption hace click REAL de mouse.
    const codeCfg = { q: "Argentina", re: /\(\+54\)/i, que: "codigo de pais" };
    await pickOption(page, page.locator("#input-7"), codeCfg, "#input-7");
    await page.waitForTimeout(2500);

    // 1) PAIS (input-10): dispara la aparicion del campo "Estado".
    const countryCfg = { q: "Argentina", re: /^Argentina$/i, que: "pais" };
    await pickOption(page, page.locator("#input-10"), countryCfg, "#input-10");
    await page.waitForTimeout(2500);


    // 2) Estado - el id del input aparece dinámicamente.
    const stateId = await page.evaluate(() => {
      const cbs = [...document.querySelectorAll('input[role="combobox"]')];
      const c = cbs.find((x) => x.value === "" && !/^input-(7|10|13|16)$/.test(x.id));
      return c ? c.id : null;
    });
    if (stateId) {
      const stateCfg = { q: "Ciudad Aut", re: /Ciudad Aut[oó]noma de Buenos Aires/i, que: "estado" };
      await pickOption(page, page.locator(`#${stateId}`), stateCfg);
    }

    // 3) Textos básicos (ids fijados por el ATS).
    const map = {
      Informaci_n_de_contacto_email: answers.email,
      Informaci_n_de_contacto_firstname: answers.firstName,
      Informaci_n_de_contacto_lastname: answers.lastName,
      // BUG CORREGIDO 2026-10-23: la regex anterior `^\+?\d+\s*` sacaba
      // "+54 " y dejaba "11 4937 4656" CON ESPACIOS, que el validador de
      // Eightfold rechaza ("Utiliza solo digitos (0-9), guiones (-) o
      // parentesis ()"). Con el codigo de pais en +54 espera el numero
      // NACIONAL: solo digitos, guiones o parentesis.
      // BUG CORREGIDO 2026-10-23 (cuarta ronda): el campo de telefono de
      // Eightfold es un COMBOBOX con el prefijo embebido ("(+54) Argentina"
      // pegado al input del numero). Por eso el input lleva SOLO el numero
      // local, sin el 54, sin espacios y sin el 0 inicial (ese 0 es del
      // prefijo internacional). El prefijo lo pone el select que esta al
      // lado, y se elige en el paso 1.
      Informaci_n_de_contacto_phone: String(answers.phone || "")
        .replace(/[^0-9]/g, "")
        .replace(/^54/, "")
        .replace(/^0+/, ""),
      Informaci_n_de_contacto_city: answers.city,
      Preguntas_sobre_la_solicitud_LinkedIn: answers.linkedin,
    };
    for (const [id, value] of Object.entries(map)) {
      const loc = page.locator(`#${id}`).first();
      if ((await loc.count()) > 0) {
        await fillText(page, loc, value);
      }
    }

    // 4) Preguntas específicas Sí/No.
    const SPECIFIC = {
      "input-13": { q: "Si", re: /^Si$/i },
      "input-16": { q: "No", re: /^No$/i },
    };
    for (const [id, cfg] of Object.entries(SPECIFIC)) {
      await pickOption(page, page.locator(`#${id}`), cfg);
    }

    // BUG CORREGIDO 2026-10-23: filled/missing vacios (mismo bug).
    const fieldSelectors = [
      "#Informaci_n_de_contacto_email",
      "#Informaci_n_de_contacto_firstname",
      "#Informaci_n_de_contacto_lastname",
      "#Informaci_n_de_contacto_phone",
      "#Informaci_n_de_contacto_city",
      "#Preguntas_sobre_la_solicitud_LinkedIn",
    ];
    const filled = [];
    const missing = [];
    // El CV: MEDIDA 2026-10-23, no se puede verificar antes del envio.
    // Eightfold CONSUME el archivo del input (lo saca de `input.files` al
    // leerlo) y su widget NO re-pinta el nombre: el dropzone se ve vacio
    // aunque el archivo este cargado. Por eso `input.files.length` da 0
    // SIEMPRE, y usarlo como "falta el CV" es un FALSO POSITIVO (una
    // corrida dio `ok: false` con el CV perfectamente adjunto). La prueba
    // real de que el CV viaja es la respuesta del servidor al enviar.
    // Aca se verifica lo unico verificable: que exista el input y que se
    // le haya pasado el archivo (que es lo que dispara el parseo).
    const cvState = await page.evaluate(() => {
      const inp = document.querySelector('input[type="file"]');
      return { existe: !!inp, accept: inp ? inp.getAttribute("accept") : null };
    });
    if (!cvState.existe) {
      missing.push("CV (no hay input[type=file] en el formulario)");
    }
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
    // BUG CORREGIDO 2026-10-23: el checkbox de WhatsApp NO se llamaba
    // "I agree" (eso era de Ashby): en Eightfold su name real es
    // "Preguntas_espec_ficas_sobre_el_puesto_q_whatsapp_a...". Se busca por
    // el fragmento "whatsapp" en vez de por el nombre exacto.
    // BUG CORREGIDO 2026-10-23: `c.click()` desde evaluate no lo registra
    // React, y el checkbox quedaba sin marcar. Ahora se usa pickRadio, que
    // hace click REAL de mouse sobre la etiqueta (el input es transparente).
    // BUG CORREGIDO 2026-10-23 (sexta ronda): el checkbox de WhatsApp
    // seguia sin marcarse. pickRadio hace `locator.check({force:true})` y, si
    // falla, click en la etiqueta; pero el input de Eightfold es
    // transparente y su etiqueta no es un <label for>: el click no cae
    // sobre el control. Se hace click de mouse real sobre el CUERPO del
    // checkbox, que es lo que un humano clickea.
    let wa = null;
    const waLoc = page.locator('input[type="checkbox"][name*="whatsapp"]').first();
    if ((await waLoc.count()) > 0) {
      await waLoc.scrollIntoViewIfNeeded().catch(() => {});
      const box = await waLoc.boundingBox();
      if (box) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 5 });
        await page.waitForTimeout(200);
        await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
      } else {
        await waLoc.click({ force: true }).catch(() => {});
      }
      await page.waitForTimeout(600);
      wa = await waLoc.isChecked().catch(() => null);
      // Si sigue sin marcarse, se hace click sobre el texto visible.
      if (!wa) {
        await page.evaluate(() => {
          const c = [...document.querySelectorAll('input[type="checkbox"]')].find((x) =>
            /whatsapp/i.test(x.name || "")
          );
          if (!c) return;
          const lab = c.closest("label") || c.parentElement;
          if (lab) {
            const r = lab.getBoundingClientRect();
            lab.dispatchEvent(
              new MouseEvent("click", {
                bubbles: true,
                clientX: r.x + 4,
                clientY: r.y + r.height / 2,
              })
            );
          }
        });
        await page.waitForTimeout(500);
        wa = await waLoc.isChecked().catch(() => null);
      }
    }

    return {
      ok: missing.length === 0,
      filled,
      missing,
      fieldSelectors,
      evidence: "",
      notes: [
        ...(wa === null ? ["no se encontro el checkbox de WhatsApp (opcional)"] : []),
        ...(wa === false ? ["el checkbox de WhatsApp no quedo marcado (opcional)"] : []),
      ],
    };
  },
  async submit(page) {
    // BUG CORREGIDO 2026-10-23: el listener de 'response' se registraba
    // DESPUES del click: la respuesta 201 {"success": true} ya habia
    // llegado y el veredicto salia vacio. Ahora se registra antes.
    const captured = [];
    const onResponse = async (r) => {
      if (!/eightfold|apply|application/i.test(r.url())) return;
      if (r.request().method() !== "POST") return;
      try {
        captured.push({ status: r.status(), url: r.url(), body: (await r.text()).slice(0, 1200) });
      } catch {}
    };
    page.on("response", onResponse);

    // Botón de envío típico: <button type="submit">Send</button>
    const btn = await page.evaluate(() => {
      const b = [...document.querySelectorAll('button')].find((e) => {
        const r = e.getBoundingClientRect();
        const t = (e.textContent || e.value || "").replace(/\s+/g, " ").trim().toLowerCase();
        return r.width > 0 && r.height > 0 && (t.includes('enviar') || t.includes('submit'));
      });
      if (b) b.click();
      return !!b;
    });
    await page.waitForTimeout(16000);
    page.off("response", onResponse);
    // La respuesta que prueba el envio es el POST de submit (201).
    const post = captured.find((c) => /submit|application\/v2/i.test(c.url)) || captured[0];
    const verdict = post ? post.body : "";
    return { ok: btn, verdict, evidence: "", raw: post || null };
  },
};

