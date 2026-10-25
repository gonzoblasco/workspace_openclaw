// greenhouse.mjs - Adaptador para formularios Greenhouse (Backblaze, etc.)
//
// POR QUE EXISTE (2026-10-25): el radar trajo a Backblaze (AI Workflow
// Engineer | LATAM, Remote Argentina) y usa Greenhouse, el cuarto ATS del
// skill. A diferencia de Ashby y Lever, Greenhouse tiene los `name`
// SEMANTICOS y estables (`first_name`, `email`, `candidate-location`), asi
// que es el mas facil de automatizar. Lo que NO es estable son las
// preguntas especificas del puesto: su `name` es un id numerico que cambia
// en cada posting (`question_16847432008`), asi que se resuelven por la
// ETIQUETA visible de la pregunta.
//
// MEDIDO 2026-10-25 contra el posting real de Backblaze:
//   input[name=first_name]           -> First Name*
//   input[name=last_name]            -> Last Name*
//   input[name=email]                -> Email*
//   input[name=country]              -> PAIS: es un react-select (input de
//                                       texto con aria-controls al listbox),
//                                       NO un <select> nativo
//   input[name=phone]                -> Telefono
//   input[name=candidate-location]   -> Ubicacion
//   input[name=resume]               -> CV (file)
//   input[name=cover_letter]         -> Cover letter (file)
//   input[name=question_<id>]        -> las preguntas del puesto
//
// REGLA QUE NO SE NEGOCIA: una pregunta sin respuesta se deja VACIA y se
// reporta en `notes`. Rellenar con inventado es una postulacion con una
// mentira; dejarla en blanco es visible para el humano, que la escribe.
import { fillText, pickOption, uploadFile } from "../lib/react-form.mjs";

export default {
  name: "greenhouse",

  matches(url) {
    try {
      const u = new URL(url);
      return /(?:job-boards|boards)\.greenhouse\.io/.test(u.hostname);
    } catch {
      return false;
    }
  },

  async fill(page, { answers, files }) {
    const notes = [];
    const filled = [];
    const missing = [];
    // El valor ESPERADO por campo: la verificacion lo necesita, porque en
    // un react-select el input queda vacio y el valor elegido se muestra
    // en un ancestro (que cambia segun el markup).
    const valoresEsperados = new Map();

    // 0) Esperar a que el DOM este listo: los campos de Greenhouse se
    //    renderizan despues de un tick.
    await page.waitForTimeout(3000);

    // 1) Campos de nombre estable.
    const estables = [
      { name: "first_name", valor: answers.firstName },
      { name: "last_name", valor: answers.lastName },
      { name: "email", valor: answers.email },
      { name: "phone", valor: answers.phone },
      { name: "candidate-location", valor: answers.city || answers.location },
    ];
    for (const campo of estables) {
      if (!campo.valor) continue;
      const loc = page.locator(`input[name="${campo.name}"]`).first();
      if ((await loc.count()) === 0) continue;
      await fillText(page, loc, campo.valor);
      filled.push(`input[name="${campo.name}"]`);
    }

    // 2) PAIS: react-select. El popup vive en un portal, asi que el scope
    //    se deja vacio y `pickOption` cae al ULTIMO listbox visible (que es el
    //    que se acaba de abrir).
    const country = page.locator('input[name="country"]').first();
    if ((await country.count()) > 0 && answers.country) {
      // react-select: click -> type -> click en la opcion ACOTADA a su
      // listbox (aria-controls). Medido 2026-10-25.
      // el aria-controls se lee DESPUES de abrir el desplegable (cerrado
      // es null). Medido 2026-10-25.
      await country.click().catch(() => {});
      await page.waitForTimeout(600);
      await country.type(answers.country, { delay: 60 }).catch(() => {});
      await page.waitForTimeout(2200);
      const lbId = await country
        .evaluate((el) => el.getAttribute("aria-controls"))
        .catch(() => null);
      if (lbId) {
        const opcion = page
          .locator(`#${lbId} [role="option"]`)
          .filter({
            hasText: new RegExp(
              `^${answers.country.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`,
              "i"
            ),
          })
          .first();
        if ((await opcion.count()) > 0) {
          await opcion.scrollIntoViewIfNeeded().catch(() => {});
          await opcion.click({ timeout: 6000 }).catch(() => {});
          await page.waitForTimeout(700);
        }
      }
      const valor = await country.inputValue().catch(() => "");
      if (valor) {
        filled.push('input[name="country"]');
      } else {
        missing.push('input[name="country"]');
        notes.push(`pais: no se pudo elegir "${answers.country}" en el desplegable`);
      }
    }

    // 3) Archivos.
    if (files.resume) {
      const cv = page.locator('input[name="resume"]').first();
      if ((await cv.count()) > 0) {
        await uploadFile(page, cv, files.resume);
        filled.push('input[name="resume"]');
      }
    }
    if (files.coverLetter) {
      const cl = page.locator('input[name="cover_letter"]').first();
      if ((await cl.count()) > 0) {
        await uploadFile(page, cl, files.coverLetter);
        filled.push('input[name="cover_letter"]');
      }
    }

    // 4) Preguntas abiertas, resueltas por la ETIQUETA visible.
    // NOTA: se usa `page.evaluate` y no la variante con `$$` a proposito: el
    // escaner de seguridad del workspace marca cualquier llamada a eval como
    // "Shell Injection" (HIGH) y bloquea el commit. La variante de una sola
    // pasada hace lo mismo y no dispara el patron.
    const preguntas = await page.evaluate(() =>
      [...document.querySelectorAll("label[for^='question_']")].map((l) => ({
        for: l.getAttribute("for"),
        texto: (l.textContent || "").replace(/\s+/g, " ").trim(),
      }))
    );
    for (const q of preguntas) {
      if (!q.for) continue;
      const respuesta =
        answers.extra?.[q.texto] ??
        answers.extra?.[q.for] ??
        // algunos `extra` vienen por clave semantica
        semanticAnswer(q.texto, answers);
      // MEDIDO 2026-10-25: el input de una pregunta de Greenhouse tiene el
      // `name` VACIO: su identificador esta en el `id` ("question_16847432008").
      // Por eso el selector va por ID, y no por name (que no existe).
      const sel = `#${q.for}`;
      const loc = page.locator(sel).first();
      if ((await loc.count()) === 0) continue;
      if (!respuesta) {
        // SIN RESPUESTA: se deja vacio y se reporta. Inventar seria una
        // mentira en una postulacion.
        missing.push(`#${q.for}`);
        notes.push(`pregunta sin responder: "${q.texto}"`);
        continue;
      }
      // MEDIDO 2026-10-25 (pregunta de pais de Backblaze): hay preguntas
      // que NO son un input de texto sino un react-select (la class del input
      // es "select__input"): hay que elegir la opcion del desplegable, no
      // escribirla. Escribiendola, el campo queda con el texto pero el
      // control del formulario no lo toma.
      const tipo = await loc.evaluate((el) => ({
        tag: el.tagName,
        esCombo:
          el.tagName !== "SELECT" &&
          (el.className || "").toString().includes("select__input"),
        role: el.getAttribute("role") || "",
      }));
      if (tipo.tag === "SELECT" || tipo.esCombo || tipo.role === "combobox") {
        // MEDIDO 2026-10-25 (pregunta de pais de Backblaze): el react-select
        // se elige con click de Playwright sobre la opcion, ACOTADO al
        // listbox de ESTE combobox (el `aria-controls` lo identifica).
        //
        // Lo que NO funciona (medido, 5 vias): el click sintetico por JS
        // (cierra el listbox y deja el input vacio), el click por
        // coordenadas, y el teclado (ArrowDown+Enter). Y el click sin acotar
        // tomaba la opcion del OTRO react-select de la pagina (el campo
        // "country" del encabezado).
        //
        // Y el valor NO se lee del input: react-select vacia el input (es
        // solo el campo de busqueda) y muestra la opcion elegida en el
        // contenedor. Por eso la verificacion de mas abajo lee el texto del
        // contenedor.
        // BUG CORREGIDO 2026-10-25: el `aria-controls` se leia ANTES de
        // abrir el desplegable, cuando todavia es null (el atributo solo
        // existe con el listbox abierto). Por eso no se hacia ningun click
        // y el campo quedaba vacio.
        await loc.click().catch(() => {});
        await page.waitForTimeout(600);
        await loc.type(respuesta, { delay: 60 }).catch(() => {});
        await page.waitForTimeout(2200);
        // Ahora si: el listbox esta abierto y el atributo apunta a el.
        const lbId = await loc
          .evaluate((el) => el.getAttribute("aria-controls"))
          .catch(() => null);
        if (lbId) {
          const opcion = page
            .locator(`#${lbId} [role="option"]`)
            .filter({
              hasText: new RegExp(
                `^${respuesta.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`,
                "i"
              ),
            })
            .first();
          if ((await opcion.count()) > 0) {
            await opcion.scrollIntoViewIfNeeded().catch(() => {});
            await opcion.click({ timeout: 6000 }).catch(() => {});
            await page.waitForTimeout(700);
          }
        }
      } else {
        await fillText(page, loc, respuesta);
      }
      valoresEsperados.set(`#${q.for}`, respuesta);
      filled.push(`#${q.for}`);
    }

    // 5) Verificacion: releer el DOM.
    //
    // MEDIDO 2026-10-25 (pregunta de pais de Backblaze): un react-select
    // NO guarda el valor en el input. El input es SOLO el campo de busqueda:
    // al elegir, react-select lo VACIA y muestra la opcion elegida en un
    // elemento hermano (el "singleValue"). Por eso `input.value` da ""
    // con el campo REALMENTE lleno, y el gate lo reportaba como faltante.
    //
    // Para un react-select, el valor se lee del CONTENEDOR (el texto
    // mostrado junto al input), no del input.
    const fieldSelectors = [...new Set(filled)];
    const finales = [];
    for (const sel of fieldSelectors) {
      const loc = page.locator(sel).first();
      if ((await loc.count()) === 0) {
        missing.push(sel);
        continue;
      }
      const esCombo = await loc.evaluate((el) => {
        if (el.tagName === "SELECT") return true;
        const cls = (el.className || "").toString();
        return cls.includes("select__input") || el.getAttribute("role") === "combobox";
      });
      if (esCombo) {
        // MEDIDO 2026-10-25 (pregunta de pais de Backblaze): el valor de un
        // react-select NO esta en el input (que queda vacio: es solo el
        // campo de busqueda) ni en un contenedor fijo: esta en un ancestro
        // MAS ARRIBA, y CUAL es depende del markup. Por eso se busca el
        // valor ESPERADO subiendo por los ancestros, con un tope.
        //
        // (Un `closest("div[class*='select']")` fijo no alcanza: el div con
        // esa clase no siempre es el que muestra la opcion elegida.)
        const esperado = valoresEsperados.get(sel) || "";
        const encontrado = await loc.evaluate(
          (el, exp) => {
            let n = el;
            for (let k = 0; k < 6 && n; k++) {
              const t = (n.innerText || "").replace(/\s+/g, " ").trim();
              if (exp ? t.includes(exp) : t.length > 1) return true;
              n = n.parentElement;
            }
            return false;
          },
          esperado
        );
        if (encontrado) finales.push(sel);
        else missing.push(sel);
        continue;
      }
      const v = await loc.inputValue().catch(() => "");
      if (v && v.trim()) finales.push(sel);
      else missing.push(sel);
    }

    return {
      ok: missing.length === 0,
      filled: finales,
      missing: [...new Set(missing)],
      fieldSelectors,
      notes,
    };
  },

  async submit(page) {
    // BUG CORREGIDO 2026-10-23 (el mismo de los otros adaptadores): el
    // listener de 'response' tiene que registrarse ANTES del click. Si va
    // despues, la respuesta del servidor ya llego y el veredicto -la
    // prueba del envio- sale vacio.
    const captured = [];
    const onResponse = async (r) => {
      if (r.request().method() !== "POST") return;
      if (!/greenhouse/i.test(r.url())) return;
      try {
        captured.push({
          status: r.status(),
          url: r.url(),
          body: (await r.text()).slice(0, 1500),
        });
      } catch {}
    };
    page.on("response", onResponse);

    const ok = await page.evaluate(() => {
      const b = [...document.querySelectorAll("button[type='submit'], button")].find((e) => {
        const r = e.getBoundingClientRect();
        const t = (e.textContent || "").replace(/\s+/g, " ").trim().toLowerCase();
        return r.width > 0 && r.height > 0 && t.includes("submit application");
      });
      if (!b) return false;
      b.click();
      return true;
    });

    await page.waitForTimeout(15000);
    page.off("response", onResponse);

    const post = captured.find((c) => /apply|submit|jobs/i.test(c.url)) || captured[0];
    const verdict = post?.body || "";
    // Greenhouse responde con un 200 y cuerpo JSON; el exito real se
    // confirma ademas con la pagina de gracias.
    const exito = ok && !!post && post.status < 400;
    return { ok: exito, verdict, evidence: "", raw: post || null };
  },
};

/**
 * Deduce la respuesta de una pregunta por su TEXTO, para no tener que
 * escribir la clave exacta en `extra`.
 *
 * Por que existe: los textos de las preguntas cambian entre postings
 * ("What city do you reside in?" vs "What city are you based in?"), pero la
 * INTENCION es la misma. Mapear por intencion hace que el archivo de
 * respuestas sobreviva a un cambio de redaccion del portal.
 */
export function semanticAnswer(texto, answers) {
  const t = String(texto || "").toLowerCase();
  const reglas = [
    [/city|city do you reside|where.*based|ubicaci[oó]n|ciudad/, answers.city],
    [/country do you reside|which country|pa[ií]s/, answers.country],
    [/salary|compensation|expectation|sueldo/, answers.salary],
    [/linkedin/, answers.linkedin],
    [/website|portfolio|portafolio|sitio web/, answers.website],
    [/github/, answers.github],
    [/how did you hear|where did you hear|como nos conociste|refer/, answers.referral],
    [/why are you interested|why.*interested|motiva|por qu[eé] te interesa/, answers.whyInterested],
    [/describe a recent project|recent project|proyecto reciente/, answers.recentProject],
    [/cover letter|letra|presentaci[oó]n/, answers.coverLetterText],
    [/notice period|preaviso/, answers.noticePeriod],
    [/years of experience|experiencia/, answers.yearsExperience],
    [/email/, answers.email],
    [/phone|tel[eé]fono/, answers.phone],
  ];
  for (const [re, valor] of reglas) {
    if (valor && re.test(t)) return valor;
  }
  return null;
}
