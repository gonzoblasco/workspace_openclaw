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

    // 2) Rellenar textos.
    //
    // BUG CORREGIDO 2026-10-25: los `name` de Ashby NO son estables entre
    // puestos. En Mural el telefono es `2c6cb798-c815-...` y en XBOW es otro
    // UUID: el adaptador de Ashby, que solo servia para Mural, fallaba
    // con XBOW (timeout esperando un input que no existe).
    //
    // La forma que SI es estable es la ETIQUETA visible del campo. Se
    // resuelve por etiqueta y se usa el `name` como fallback (para los
    // casos donde la etiqueta no este en el DOM).
    const TEXTOS = [
      { label: /first and last name/i, valor: answers.firstName + " " + answers.lastName, name: "_systemfield_name" },
      { label: /^email/i, valor: answers.email, name: "_systemfield_email" },
      { label: /telephone|phone/i, valor: answers.phone, name: "2c6cb798-c815-4405-a439-f89427f47e6e" },
      { label: /^location/i, valor: answers.location, name: "" },
      { label: /linkedin/i, valor: answers.linkedin, name: "d7ce58e9-6422-4759-b15c-3fb2c4759def" },
      { label: /salary|compensation|expectation/i, valor: answers.salary, name: "6bb011c6-ca94-44ce-a0a1-41f0afec07a2" },
    ];
    const escrito = {};
    for (const campo of TEXTOS) {
      if (!campo.valor) continue;
      // 1) por etiqueta
      const porEtiqueta = await page.evaluateHandle((re) => {
        const rx = new RegExp(re, "i");
        const labels = [...document.querySelectorAll("label, [class*='label']")];
        const l = labels.find((x) => {
          const t = (x.textContent || "").replace(/\s+/g, " ").trim();
          return rx.test(t) && t.length < 70;
        });
        if (!l) return null;
        const id = l.getAttribute("for");
        if (id) {
          const el = document.getElementById(id);
          if (el && el.tagName !== "LABEL") return el;
        }
        const scope = l.closest("div") || document;
        const inp = scope.querySelector("input:not([type=file]):not([type=radio]), textarea");
        return inp || null;
      }, campo.label.source);
      let el = porEtiqueta.asElement();
      // 2) fallback: por name
      if (!el && campo.name) {
        el = await page.locator(`input[name="${campo.name}"], textarea[name="${campo.name}"]`).first();
        if ((await el.count()) === 0) el = null;
      }
      if (!el) {
        console.error(`[ashby] no se encontro el campo: ${campo.label.source}`);
        continue;
      }
      await fillText(page, el, campo.valor);
      // Se captura el `name` REAL del campo (el de este puesto, no el de
      // Mural): es lo unico estable para verificar despues.
      const nameReal = await el.evaluate((e) => e.name || e.id || "");
      escrito[campo.label.source] = { valor: campo.valor, name: nameReal };
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
    // Radios: resueltos por el TEXTO DE LA PREGUNTA, no por el name.
    //
    // BUG CORREGIDO 2026-10-25: los `name` de los radios de Ashby son
    // UUIDs POR PUESTO (en Mural el de autorizacion laboral es
    // "<uuid>_e7e51cb6-..."; en XBOW es otro). El adaptador solo servia para
    // Mural: en XBOW no marcaba ninguno, y la verificacion de radios (que
    // si funciona) lo detectaba.
    //
    // La regla es semantica y no depende del puesto:
    //   - "autorizado a trabajar" -> Yes
    //   - "sponsorship / visa"    -> No
    //   - genero / etnia / veteran status -> la opcion de no identificarse
    // Dos criterios, en este orden:
    //  1) el FRAGMENTO del `name` del grupo: es estable por tipo de pregunta
    //     en Ashby (autorizacion, patrocinio, genero, etnia, veteran status)
    //     y es lo unico que funciona para la ETNIA, cuya pregunta visible es
    //     el encabezado del bloque EEO y no "Hispanic or Latino".
    //  2) el TEXTO de la pregunta, para los puestos que usan el fragmento
    //     del nombre pero con otra nomenclatura, y para el caso boton.
    const REGLAS_RADIO = [
      { name: /_e7e51cb6/, opcion: /^yes$/i },
      { name: /_b3a08088/, opcion: /^no$/i },
      { name: /eeoc_gender/, opcion: /decline|prefer not|not to self/i },
      { name: /eeoc_race/, opcion: /decline|prefer not|not to self/i },
      { name: /eeoc_veteran/, opcion: /decline|prefer not|not to self/i },
      { pregunta: /authoriz|s\.?autoriz/i, opcion: /^yes$/i },
      { pregunta: /sponsorship|visa|permiso de trabajo/i, opcion: /^no$/i },
      { pregunta: /gender|sexo|genero|género/i, opcion: /decline|prefer not|not to self/i },
      { pregunta: /ethnic|race|raza|etnia|origen/i, opcion: /decline|prefer not|not to self/i },
      { pregunta: /veteran/i, opcion: /decline|prefer not|not to self/i },
    ];
    const reglaPara = (g) =>
      REGLAS_RADIO.find((r) => (r.name && r.name.test(g.name)) || (r.pregunta && r.pregunta.test(g.pregunta)));

    const gruposRadio = await page.evaluate(() => {
      const out = [];
      const vistos = new Set();
      document.querySelectorAll('input[type="radio"]').forEach((r) => {
        const n = r.name || "";
        if (!n || vistos.has(n)) return;
        vistos.add(n);
        // el texto de la pregunta: el contenedor del grupo, sin las etiquetas
        // de opcion.
        let cont = r.closest("div");
        let q = "";
        for (let k = 0; k < 6 && cont; k++) {
          const t = (cont.innerText || "").replace(/\s+/g, " ").trim();
          if (t.length > 12) {
            q = t;
            break;
          }
          cont = cont.parentElement;
        }
        // las opciones con su texto
        const opciones = [...document.querySelectorAll(`input[type="radio"][name="${CSS.escape(n)}"]`)].map(
          (x) => {
            const lab = x.closest("label") || document.querySelector(`label[for="${CSS.escape(x.id)}"]`);
            return { valor: x.value, texto: (lab ? lab.textContent : x.value).replace(/\s+/g, " ").trim() };
          }
        );
        out.push({ name: n, pregunta: q.slice(0, 220), opciones });
      });
      return out;
    });

    for (const g of gruposRadio) {
      const regla = reglaPara(g);
      if (!regla) continue; // pregunta que no es de las nuestras
      const opcion = g.opciones.find((o) => regla.opcion.test(o.texto));
      if (!opcion) continue;

      // El radio concreto: dentro del grupo, el que su etiqueta coincide con
      // la opcion elegida. BUG CORREGIDO 2026-10-25: se usaba
      // `.filter({hasText})` sobre un input - un input no tiene texto, asi
      // que el locator no filtraba nada y el check de "quedo marcado" era
      // sobre el elemento equivocado (decia FALLO con el radio marcado).
      const radioId = await page.evaluate(
        ({ name, texto }) => {
          const rx = new RegExp(`^${texto.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`, "i");
          const xs = [...document.querySelectorAll(`input[type="radio"][name="${CSS.escape(name)}"]`)];
          const hit = xs.find((x) => {
            const l = x.closest("label") || document.querySelector(`label[for="${CSS.escape(x.id)}"]`);
            return l && rx.test((l.textContent || "").replace(/\s+/g, " ").trim());
          });
          return hit ? hit.id : null;
        },
        { name: g.name, texto: opcion.texto }
      );
      if (!radioId) continue;
      // BUG CORREGIDO 2026-10-25: `CSS.escape` es API del BROWSER (vive
      // dentro de page.evaluate). Acá se esta usando en contexto de Node, y
      // reventaba con "CSS is not defined". Los ids de Ashby son UUID, que
      // no necesitan escape en un selector de atributo.
      const radio = page.locator(`#${radioId}`).first();
      let clicked = false;
      try {
        await radio.check({ force: true, timeout: 4000 });
        clicked = await radio.isChecked();
      } catch (e) {
        clicked = false;
      }
      if (!clicked) {
        // fallback: click en la etiqueta visible (el input suele ser opaco)
        await page.evaluate(
          ({ id }) => {
            const x = document.getElementById(id);
            const l = x && (x.closest("label") || document.querySelector(`label[for="${CSS.escape(id)}"]`));
            if (l) l.click();
          },
          { id: radioId }
        );
        await page.waitForTimeout(400);
        clicked = await radio.isChecked().catch(() => false);
      }
      // BUG CORREGIDO 2026-10-25: el log decia "FALLO" con el radio
      // PERFECTAMENTE marcado. `isChecked()` se leia en el mismo tick del
      // click, antes de que React re-renderizara el estado. Se relee con
      // espera: un log que miente es peor que no tener log.
      if (!clicked) {
        await page.waitForTimeout(700);
        // BUG CORREGIDO 2026-10-25: `radio.isChecked()` miente en Ashby
        // porque Ashby DUPLICA los ids: `locator('#id').first()` resuelve a
        // otro elemento con el mismo id, y ese no esta marcado. La
        // verificacion correcta es la del GRUPO (cuantos de sus radios
        // estan checked), que es la que usa el gate final.
        clicked = await page.evaluate(
          ({ name, texto }) => {
            const rx = new RegExp(`^${texto.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`, "i");
            const xs = [...document.querySelectorAll(`input[type="radio"][name="${CSS.escape(name)}"]`)];
            return xs.some((x) => {
              const l = x.closest("label") || document.querySelector(`label[for="${CSS.escape(x.id)}"]`);
              return x.checked && l && rx.test((l.textContent || "").replace(/\s+/g, " ").trim());
            });
          },
          { name: g.name, texto: opcion.texto }
        );
      }
      console.error(
        `[ashby] radio "${g.pregunta.slice(0, 44)}" -> ${opcion.texto} ${clicked ? "ok" : "FALLO"}`
      );
    }
    // Opciones que NO son inputs de radio sino BOTONES con type=submit.
    //
    // BUG CORREGIDO 2026-10-25 (medido en XBOW): hay puestos de Ashby donde
    // las opciones Yes/No y las de identificacion son <button type="submit">
    // no hay ni un input[type=radio] en todo el formulario. Con el
    // detector por input, no se marcaba NINGUNA y la verificacion de radios
    // (que funciona) lo detectaba como falla.
    //
    // Se resuelve por la PREGUNTA (el texto del contenedor) y la opcion, y
    // se hace click real de mouse sobre el boton.
    const botonesOpcion = await page.evaluate(() => {
      const out = [];
      // BUG CORREGIDO 2026-10-25: el selector era `button[type="submit"]`
      // y no matcheaba NADA. Los botones de opcion de Ashby NO tienen
      // atributo `type` (se que `e.type` reporta "submit" porque es el
      // default del DOM, pero el atributo no esta en el HTML). El selector
      // correcto es `button`, y se filtra por el texto.
      let gi = 0;
      document.querySelectorAll("button").forEach((btn) => {
        const t = (btn.textContent || "").replace(/\s+/g, " ").trim();
        if (!/^(yes|no|si|sí|decline to self-identify|prefer not to self-identify|i decline to self-identify for protected veteran status)$/i.test(t)) return;
        // la pregunta: el contenedor del boton, subiendo hasta que aparezca
        // un texto que no sea solo la opcion.
        let cont = btn.parentElement;
        let q = "";
        for (let k = 0; k < 6 && cont; k++) {
          const ct = (cont.innerText || "").replace(/\s+/g, " ").trim();
          if (ct.length > t.length + 4) {
            q = ct;
            break;
          }
          cont = cont.parentElement;
        }
        // Se identifica el grupo para poder acotar el click a SU grupo.
        // Sin esto, `locator('button[data-option="no"]').first()` elige el
        // primer "No" del documento: en un formulario con dos preguntas
        // (autorizacion y patrocinio) se marcaba el de la primera cuando
        // se queria el de la segunda.
        if (!cont.hasAttribute("data-oc-group")) {
          cont.setAttribute("data-oc-group", String(gi));
          gi++;
        }
        const grupo = cont.getAttribute("data-oc-group");
        out.push({ texto: t, pregunta: q.slice(0, 200), grupo });
      });
      return out;
    });

    for (const b of botonesOpcion) {
      // BUG CORREGIDO 2026-10-25: `r.pregunta.test(...)` reventaba con
      // "Cannot read properties of undefined" porque hay reglas que solo
      // tienen `name` (los radios reales) y las de boton no lo tienen. Para
      // los botones solo aplican las reglas por TEXTO de pregunta.
      const regla = REGLAS_RADIO.find(
        (r) => r.pregunta && r.pregunta.test(b.pregunta)
      );
      if (!regla) continue;
      if (!regla.opcion.test(b.texto)) continue;
      // BUG CORREGIDO 2026-10-25: el click por COORDENADAS (mouse.move +
      // mouse.click) no registraba en estos botones: seguian con
      // aria-pressed="false". Medido con tres vias: `locator.click()` SI
      // funciona (deja aria-pressed="true"), `dispatchEvent` no, y el
      // click en el checkbox oculto tambien.
      // Se usa `locator.click()`, que es el click real de Playwright.
      const opcion = b.texto.toLowerCase();
      // ACOTADO al grupo: sin esto se marca el primer boton del documento.
      const btn = page
        .locator(`[data-oc-group="${b.grupo}"] button[data-option="${opcion}"]`)
        .first();
      let ok = false;
      if ((await btn.count()) > 0) {
        await btn.scrollIntoViewIfNeeded().catch(() => {});
        await btn.click({ timeout: 6000 }).catch(() => {});
        await page.waitForTimeout(500);
        ok = await btn.getAttribute("aria-pressed").catch(() => null);
        ok = ok === "true";
      }
      if (!ok) {
        // fallback: el checkbox oculto del grupo, que es el control real.
        const group = page.locator(`.ashby-application-form-input-yesno:has(button[data-option="${opcion}"])`).first();
        const cb = group.locator('input[type="checkbox"]').first();
        if ((await cb.count()) > 0) {
          await cb.check({ force: true, timeout: 5000 }).catch(() => {});
          await page.waitForTimeout(500);
          ok = (await btn.getAttribute("aria-pressed").catch(() => null)) === "true";
        }
      }
      console.error(
        `[ashby] boton-opcion "${b.pregunta.slice(0, 40)}" -> ${b.texto} ${ok ? "ok" : "FALLO"}`
      );
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
    // Los selectores de verificacion son los de los campos REALMENTE
    // llenados, resueltos en runtime. BUG CORREGIDO 2026-10-25: estaban
    // hardcodeados a los de Mural, y en otro puesto (XBOW) no existen: la
    // verificacion daba timeout esperando un input inexistente.
    // Los selectores de verificacion son los `name` REALES de los campos
    // que se llenaron. BUG CORREGIDO 2026-10-25: estaban hardcodeados a
    // los de Mural, y en otro puesto (XBOW) no existen: la verificacion
    // daba timeout esperando un input inexistente.
    const fieldSelectors = Object.values(escrito)
      .map((c) => c.name)
      .filter(Boolean)
      .map((n) => `input[name="${n}"], textarea[name="${n}"]`);
    const filled = [];
    const missing = [];
    for (const [etiqueta, campo] of Object.entries(escrito)) {
      const loc = page.locator(`input[name="${campo.name}"], textarea[name="${campo.name}"]`).first();
      if ((await loc.count()) === 0) {
        missing.push(etiqueta);
        continue;
      }
      const v = await loc.inputValue().catch(() => "");
      if (v && v.trim()) filled.push(etiqueta);
      else missing.push(etiqueta);
    }
    // Verificacion de las opciones de opcion multiple: no alcanza con que
    // el click "no tirara error". Se lee que opcion quedo marcada.
    //
    // Hay DOS variantes en Ashby, y por eso esto mira las dos:
    //   a) input[type=radio] con name "<uuid>_<slug>" (Mural, y los
    //      formularios de Ashby con radios reales)
    //   b) <button data-option="yes|no" aria-pressed="true"> (XBOW: no hay
    //      ni un input de radio, las opciones son botones)
    //
    // BUG CORREGIDO 2026-10-25: la verificacion solo miraba los radios, asi
    // que en XBOW reportaba "falta un radio" con las dos opciones YA
    // marcadas. Un gate que no mira lo que acaba de hacer da falsos
    // negativos.
    // Verificacion de las opciones de opcion multiple: no alcanza con que
    // el click "no tirara error". Se lee que opcion quedo marcada.
    //
    // Hay DOS variantes en Ashby:
    //   a) input[type=radio] con name "<uuid>_<slug>" (Mural)
    //   b) <button data-option="yes|no" aria-pressed="true"> (XBOW: no hay
    //      ni un input de radio, las opciones son botones)
    //
    // BUG CORREGIDO 2026-10-25: la verificacion solo miraba los radios, asi
    // que en XBOW reportaba "falta un radio" con las dos opciones YA
    // marcadas. Y despues un parche dejo el `missing.push` vacio: el gate
    // se_volvio un no-op que daba `ok: true` sin verificar nada. Un gate que
    // no mira lo que acaba de hacer no verifica nada.
    const grupos = await page.evaluate(() => {
      const out = [];
      // a) radios reales, agrupados por name
      const porName = new Map();
      document.querySelectorAll('input[type="radio"]').forEach((r) => {
        const n = r.name || "";
        if (!n) return;
        if (!porName.has(n)) porName.set(n, { name: n, opciones: [], marcada: null, pregunta: "" });
        const g = porName.get(n);
        const lab = r.closest("label") || document.querySelector(`label[for="${CSS.escape(r.id)}"]`);
        const texto = (lab ? lab.textContent : r.value).replace(/\s+/g, " ").trim();
        g.opciones.push({ texto, valor: r.value, checked: r.checked });
        if (r.checked) g.marcada = texto;
      });
      porName.forEach((g) => {
        // la pregunta: el label/legend del contenedor, que es la de verdad
        let cont = g.opciones.length ? null : null;
        let c = document.querySelector(`input[type="radio"][name="${CSS.escape(g.name)}"]`);
        for (let k = 0; k < 6 && c; k++) {
          const l = c.closest("div")?.querySelector("label, legend, [class*='questionLabel']");
          if (l && (l.textContent || "").trim().length > 4) {
            g.pregunta = l.textContent.replace(/\s+/g, " ").trim().slice(0, 120);
            break;
          }
          c = c.parentElement;
        }
        out.push(g);
      });
      // b) botones de opcion, agrupados por su contenedor .yesno
      const porGrupo = new Map();
      let gi = 0;
      document.querySelectorAll("button[data-option]").forEach((btn) => {
        const cont = btn.closest(".ashby-application-form-input-yesno") || btn.parentElement;
        if (!cont) return;
        if (!porGrupo.has(cont)) {
          // Se marca el grupo con un data attribute: hace falta para
          // ACOTAR el click a SU grupo.
          //
          // BUG CORREGIDO 2026-10-25: el click se hacia con
          // `page.locator('button[data-option="no"]').first()`, y `.first()`
          // elige el PRIMER "no" del documento: en un formulario con dos
          // preguntas (autorizacion y patrocinio) se marcaba el "No" de la
          // PRIMERA cuando se queria el de la segunda. El resultado era un
          // formulario con la autorizacion en "No" (mal) y el patrocinio
          // sin marcar.
          cont.setAttribute("data-oc-group", String(gi));
          gi++;
          porGrupo.set(cont, { name: "", grupo: gi - 1, opciones: [], marcada: null, pregunta: "" });
        }
        const g = porGrupo.get(cont);
        const texto = (btn.textContent || "").replace(/\s+/g, " ").trim();
        g.opciones.push({ texto, valor: btn.getAttribute("data-option"), checked: btn.getAttribute("aria-pressed") === "true" });
        if (btn.getAttribute("aria-pressed") === "true") g.marcada = texto;
      });
      porGrupo.forEach((g, cont) => {
        // BUG CORREGIDO 2026-10-25: la pregunta se calculaba consultando
        // SIEMPRE el primer `.ashby-application-form-input-yesno` del
        // documento, no el contenedor de cada grupo. Con dos preguntas
        // (autorizacion y patrocinio) las dos terminaban con la pregunta
        // de la primera, y el gateVF pedia "Yes" en un grupo que tenia
        // "No" -> falso negativo.
        // Ahora se sube desde el contenedor REAL de cada grupo.
        const opcionesTxt = g.opciones.map((o) => o.texto).join(" ");
        let c = cont;
        for (let k = 0; k < 6 && c; k++) {
          const t = (c.innerText || "").replace(/\s+/g, " ").trim();
          if (t.length > opcionesTxt.length + 4) {
            g.pregunta = t.slice(0, 120);
            break;
          }
          c = c.parentElement;
        }
        out.push(g);
      });
      return out;
    });

    // Para cada grupo que sea NUESTRO, la opcion marcada tiene que ser la
    // esperada. Los grupos que no son nuestros (otras preguntas del ATS) se
    // ignoran: no es asunto nuestro.
    const radioEsperados = [
      { nombre: /authoriz|s\.?autoriz/i, opcion: /^yes$/i },
      { nombre: /sponsorship|visa|permiso de trabajo/i, opcion: /^no$/i },
      { nombre: /gender|sexo|genero|género/i, opcion: /decline|prefer not|not to self/i },
      { nombre: /ethnic|race|raza|etnia|origen/i, opcion: /decline|prefer not|not to self/i },
      { nombre: /veteran/i, opcion: /decline|prefer not|not to self/i },
    ];
    const OurRadios = [];
    const radiosOk = grupos.every((g) => {
      // el criterio de busqueda: primero el name (estable en Ashby), luego
      // el texto de la pregunta.
      const esperada = radioEsperados.find(
        (r) =>
          r.nombre.test(g.name || "") || r.nombre.test(g.pregunta || "")
      );
      if (!esperada) return true; // no es una pregunta nuestra
      const ok = !!g.marcada && esperada.opcion.test(g.marcada);
      OurRadios.push({
        pregunta: (g.pregunta || g.name || "").slice(0, 50),
        marcada: g.marcada,
        esperada: esperada.opcion.source,
        ok,
      });
      return ok;
    });
    if (!radiosOk) {
      missing.push(
        "radios: alguna pregunta de opcion multiple quedo sin marcar como se pedia: " +
          JSON.stringify(OurRadios.filter((r) => !r.ok))
      );
    }

    return {
      ok: missing.length === 0,
      filled,
      missing,
      fieldSelectors,
      evidence: "",
      radios: OurRadios,
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

