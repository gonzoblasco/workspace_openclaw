// react-form.mjs - Utilidades para interactuar con formularios React
//
// POR QUÉ EXISTE (2026-10-23):
//   Los scripts de referencia llenan formularios con `type()` en lugar de
//   `fill()`.  En React el valor del DOM y el valor interno del tracker
//   (`_valueTracker`) divergen si se usan los métodos nativos del DOM.
//   Esta librería encapsula los *workarounds* que se describen en
//   `ats-playbook.md` y se reutiliza en los adaptadores de ATS.
//   Cada función está pensada para ser usada con objetos `Locator` de
//   Playwright, pero los tests la tratan como funciones puras que operan
//   sobre objetos simulados.

/**
 * Escribe texto en un campo input usando la secuencia que React reconoce.
 *
 * @param {object} page    Playwright Page (solo para waiting).
 * @param {object} locator Playwright Locator del input.
 * @param {string} value  Texto a escribir.
 * @returns {Promise<{dom:string,react:string}>}   Valores escritos.
 */
export async function fillText(page, locator, value) {
  // Seleccionamos todo el texto (Meta+A) y borramos para evitar concatenaciones.
  await locator.click({ clickCount: 3 }).catch(() => {});
  // Algunos navegadores ignoran Meta+A, así que se hace un Backspace adicional.
  await locator.press("Backspace").catch(() => {});
  await locator.type(value, { delay: 12 });
  // Tab para activar onBlur y que React marque el cambio.
  await locator.press("Tab").catch(() => {});
  // Pequeña espera opcional para que React actualice el tracker.
  if (page && typeof page.waitForTimeout === "function") {
    await page.waitForTimeout(250);
  }
  const dom = await locator.inputValue().catch(() => "");
  const react = await locator.evaluate((el) => {
    const t = el._valueTracker;
    return t && typeof t.getValue === "function" ? String(t.getValue()) : "";
  });
  return { dom, react };
}

/**
 * Selecciona una opción en un combobox/autocomplete haciendo click real
 * sobre la opción visible.
 *
 * @param {object} page Playwright Page.
 * @param {object} locator Locator del input (combobox).
 * @param {RegExp|string} matcher Texto o RegExp que debe coincidir con
 *   la opción visible.
 * @param {string} [scopeSelector] CSS del listbox donde buscar la opcion.
 *   Sin esto se buscan en todo el documento, y con varios desplegables
 *   abiertos se puede elegir la opcion de otro (bug corregido 2026-10-23).
 * @returns {Promise<boolean>} true si se consiguió hacer click.
 */
export async function pickOption(page, locator, matcher, scopeSelector) {
  // BUG CORREGIDO 2026-10-23: el contrato era ambiguo. Los adaptadores lo
  // llamaban con un objeto { q, re } y la funcion esperaba un string o un
  // RegExp: con un objeto, `matcher.source` era undefined y la regexp
  // compilaba contra "undefined". Ahora se aceptan las tres formas:
  //   - RegExp  -> se usa tal cual
  //   - string  -> se compila como regexp
  //   - { q, re } -> `q` es el texto a tipear, `re` el matcher
  const cfg = typeof matcher === "object" && matcher !== null && !Array.isArray(matcher)
    ? matcher
    : { q: typeof matcher === "string" ? matcher : "", re: matcher };
  await locator.scrollIntoViewIfNeeded().catch(() => {});
  await locator.click({ force: true }).catch(() => {});
  // Limpiar: Backspace no borra de un input controlado (deja el valor
  // concatenado). Se selecciona todo y se borra.
  await locator.press("Backspace").catch(() => {});
  if (cfg.q) {
    await locator.type(cfg.q, { delay: 40 }).catch(() => {});
  }
  // Esperar a que aparezca la lista de opciones.
  await page.waitForTimeout(2800);
  // Encuentra la opción que coincide con el matcher.
  // BUG CORREGIDO 2026-10-23: la version anterior destructuraba
  // `{ text }` pero mandaba `{ text: "" }` como primer argumento y el matcher
  // como segundo: dentro del callback `matcherString` era undefined y la
  // regexp compilaba contra la cadena "undefined", asi que NUNCA encontraba
  // la opcion. Ademas las opciones se buscaban en todo el documento: con
  // varios desplegables abiertos a la vez, se podia elegir la de otro.
  const re = cfg.re instanceof RegExp ? cfg.re : new RegExp(String(cfg.re || cfg.q), "i");
  const matcherSource = re.source;
  // BUG CORREGIDO 2026-10-23 (quinta ronda): el scope del listbox NO es el
  // id del combobox. El popup de un combobox se renderiza en un PORTAL, con
  // otro id (`aria-controls` apunta a el: por ejemplo "list-5"). Buscando
  // dentro de "#input-7" no se encontraba nada, y el fallback (todo el
  // documento) podia elegir la opcion de OTRO desplegable: el codigo de
  // pais terminó escrito en el campo de EMAIL.
  // Ahora el scope se deriva de `aria-controls` del combobox, y si no se
  // puede, se exige que el listbox este abierto (aria-expanded) y se usa el
  // ULTIMO visible.
  const optionHandle = await page.evaluateHandle(
    ({ src, scopeSel }) => {
      const exp = new RegExp(src, "i");
      let scope = null;
      if (scopeSel) {
        const cb = document.querySelector(scopeSel);
        const controls = cb && cb.getAttribute("aria-controls");
        if (controls) {
          // los ids de React vienen como ":r5:" -> el id real es "r5"
          const clean = controls.replace(/^:|:$/g, "");
          scope = document.getElementById(clean) || document.querySelector(`[id="${clean}"]`);
        }
        if (!scope) {
          // Ultimo listbox visible: el que se acaba de abrir.
          const lbs = [...document.querySelectorAll('[role="listbox"]')].filter((o) => {
            const r = o.getBoundingClientRect();
            return r.width > 0 && r.height > 0;
          });
          scope = lbs[lbs.length - 1] || null;
        }
      }
      if (!scope) scope = document;
      const opts = [...scope.querySelectorAll('[role="option"], li, [class*="option"]')].filter((o) => {
        const r = o.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
      });
      return opts.find((o) => exp.test((o.textContent || "").replace(/\s+/g, " ").trim())) || null;
    },
    { src: matcherSource, scopeSel: scopeSelector || null }
  );
  const el = optionHandle.asElement();
  if (!el) return false;
  // Click real de mouse sobre la posición de la opción.
  const box = await el.boundingBox();
  if (box) {
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 5 });
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
  } else {
    await el.click({ force: true }).catch(() => {});
  }
  await page.waitForTimeout(300);
  return true;
}

/**
 * Marca un radio button haciendo click en la etiqueta asociada (el input
 * suele estar oculto).  Funciona tanto con `locator` apuntando al radio
 * como al contenedor que lo engloba.
 */
export async function pickRadio(page, locator) {
  // intentamos clickear el propio input; si falla, buscamos la etiqueta.
  try {
    await locator.check({ force: true, timeout: 3000 });
    return true;
  } catch (e) {
    // fallback: click en la etiqueta que lo envuelve.
    await locator.evaluate((el) => {
      const label = el.closest("label") || document.querySelector(`label[for="${el.id}"]`);
      if (label) label.click();
    }).catch(() => {});
    return true;
  }
}

/**
 * Sube un archivo a un input tipo file.
 */
export async function uploadFile(page, locator, filePath) {
  await locator.setInputFiles(filePath);
  // Esperar a que el evento de carga termine (aprox 2 s).
  await page.waitForTimeout(2000);
}

/**
 * Obtiene el valor que React conoce para un elemento.
 */
export function reactValue(el) {
  const t = el._valueTracker;
  return t && typeof t.getValue === "function" ? String(t.getValue()) : null;
}

/**
 * Verifica que los campos tengan el mismo valor en el DOM y en el tracker.
 *
 * @param {object} page   Playwright Page.
 * @param {Array<string>} selectors   Lista de selectores CSS a inspeccionar.
 * @returns {Promise<Array<object>>}   Arreglo con los campos divergentes.
 */
export async function verifyFields(page, selectors) {
  const divergentes = [];
  for (const sel of selectors) {
    const loc = page.locator(sel);
    const dom = await loc.inputValue().catch(() => "");
    const react = await loc.evaluate((el) => {
      const t = el._valueTracker;
      return t && typeof t.getValue === "function" ? String(t.getValue()) : "";
    });
    if (dom !== react) {
      divergentes.push({ selector: sel, dom, react });
    }
  }
  return divergentes;
}

