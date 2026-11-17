/**
 * Medición de contraste WCAG 2.2 (1.4.3 / 1.4.11).
 *
 * axe-core no ve todo: estados :hover/:focus, texto sobre imagen, canvas y
 * elementos dentro de shadow roots quedan fuera o incompletos. Este módulo
 * mide el par texto/fondo real desde los estilos computados y calcula el ratio
 * con la fórmula de luminancia relativa de WCAG, en Node, para que la cuenta
 * sea testeable sin browser.
 */

// --- Matemática pura (testeable sin browser) --------------------------------

/**
 * Parsea `rgb(r, g, b)` / `rgba(r, g, b, a)` a componentes 0-255 + alpha 0-1.
 * Devuelve null si no es un color RGB (p. ej. `transparent` ya viene como rgba).
 */
function parseColor(value) {
  if (typeof value !== 'string') return null;
  const match = value.match(/rgba?\(([^)]+)\)/i);
  if (!match) return null;
  const parts = match[1].split(/[,\s/]+/).filter(Boolean).map(Number);
  if (parts.length < 3 || parts.some(n => Number.isNaN(n))) return null;
  return {
    r: parts[0],
    g: parts[1],
    b: parts[2],
    a: parts.length > 3 ? parts[3] : 1
  };
}

/** Canal sRGB linealizado según WCAG. */
function linearize(channel) {
  const c = channel / 255;
  return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}

/** Luminancia relativa WCAG de un color opaco. */
function relativeLuminance({ r, g, b }) {
  return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b);
}

/** Compone `top` sobre `bottom` (alpha compositing, sRGB no premultiplicado). */
function compositeOver(top, bottom) {
  const a = top.a;
  return {
    r: top.r * a + bottom.r * (1 - a),
    g: top.g * a + bottom.g * (1 - a),
    b: top.b * a + bottom.b * (1 - a),
    a: a + bottom.a * (1 - a)
  };
}

/**
 * Compone una pila de fondos: `stack[0]` es el fondo del propio elemento y el
 * último el más externo. Devuelve el color efectivo detrás del texto.
 */
function compositeStack(stack, canvas = { r: 255, g: 255, b: 255, a: 1 }) {
  let result = canvas;
  for (let i = stack.length - 1; i >= 0; i--) {
    const layer = stack[i];
    if (!layer) continue;
    result = compositeOver(layer, result);
  }
  return result;
}

/** Ratio de contraste WCAG entre dos colores ya opacos. */
function contrastRatio(fg, bg) {
  const l1 = relativeLuminance(fg);
  const l2 = relativeLuminance(bg);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Umbral WCAG AA para un texto: 3:1 si es grande (>=24px, o >=18.66px en
 * negrita), 4.5:1 en el resto.
 */
function requiredRatio(fontSizePx, fontWeight) {
  const large = fontSizePx >= 24 || (fontSizePx >= 18.66 && fontWeight >= 700);
  return large ? 3 : 4.5;
}

/** Resuelve el contraste real de un texto dadas sus capas de fondo. */
function resolveContrast({ color, backgrounds, fontSizePx, fontWeight, opacity = 1 }) {
  const fgRaw = parseColor(color);
  if (!fgRaw) return null;

  const bg = compositeStack(
    backgrounds.map(b => parseColor(b)).filter(Boolean)
  );

  // La opacidad del elemento reduce el contraste del texto aunque el color sea opaco.
  const fg = compositeOver({ ...fgRaw, a: fgRaw.a * opacity }, bg);

  return {
    ratio: contrastRatio(fg, bg),
    foreground: fg,
    background: bg,
    required: requiredRatio(fontSizePx, fontWeight),
    large: requiredRatio(fontSizePx, fontWeight) === 3
  };
}

// --- Extracción en el browser ----------------------------------------------

/**
 * Recorre el DOM y devuelve los pares texto/fondo candidatos. No decide nada:
 * devuelve datos crudos para que la cuenta se haga en Node.
 */
function collectCandidates(maxElements) {
  const label = (el) => {
    const tag = el.tagName.toLowerCase();
    const id = el.id ? `#${el.id}` : '';
    const cls = el.classList && el.classList.length ? `.${el.classList[0]}` : '';
    return `${tag}${id}${cls}`;
  };

  const isVisible = (el, styles) => {
    if (!el.getClientRects().length) return false;
    if (styles.visibility === 'hidden' || styles.display === 'none') return false;
    if (parseFloat(styles.opacity) === 0) return false;
    return true;
  };

  const backgroundChain = (el) => {
    const chain = [];
    let node = el;
    let hasImage = false;
    while (node && node.nodeType === 1) {
      const s = window.getComputedStyle(node);
      if (s.backgroundImage && s.backgroundImage !== 'none') hasImage = true;
      const color = s.backgroundColor;
      const parsed = color && color !== 'transparent';
      if (parsed) {
        chain.push(color);
        // Si ya es opaco, no hace falta seguir subiendo.
        const alphaMatch = color.match(/rgba?\(([^)]+)\)/i);
        if (alphaMatch) {
          const parts = alphaMatch[1].split(/[,\s/]+/).filter(Boolean).map(Number);
          const alpha = parts.length > 3 ? parts[3] : 1;
          if (alpha >= 1) break;
        } else {
          break;
        }
      }
      node = node.parentElement;
    }
    return { chain, hasImage };
  };

  const results = [];
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);

  let el = walker.currentNode;
  while (el && results.length < maxElements) {
    if (el.nodeType === 1) {
      const tag = el.tagName.toLowerCase();
      const skip = tag === 'script' || tag === 'style' || tag === 'svg' ||
        el.closest('[aria-hidden="true"]') || el.closest('svg');

      if (!skip) {
        const styles = window.getComputedStyle(el);
        // Solo elementos con texto propio (nodo de texto no vacío).
        const ownText = Array.from(el.childNodes)
          .filter(n => n.nodeType === 3)
          .map(n => n.textContent.trim())
          .join(' ')
          .trim();

        if (ownText && isVisible(el, styles)) {
          const key = label(el) + '|' + ownText.slice(0, 24);
          if (!seen.has(key)) {
            seen.add(key);
            const { chain, hasImage } = backgroundChain(el);
            results.push({
              selector: label(el),
              text: ownText.slice(0, 60),
              color: styles.color,
              backgrounds: chain,
              fontSizePx: parseFloat(styles.fontSize) || 16,
              fontWeight: parseInt(styles.fontWeight, 10) || 400,
              opacity: parseFloat(styles.opacity) || 1,
              hasBackgroundImage: hasImage
            });
          }
        }
      }
    }
    el = walker.nextNode();
  }

  return results;
}

// --- Check integrado -------------------------------------------------------

/**
 * Mide contraste en la página. Devuelve violations (bajo el umbral),
 * warnings (indeterminado: fondo con imagen) y measurements (todos los pares
 * medidos, para que el reporte pueda mostrar qué se midió y no solo qué falló).
 */
async function measureContrast(page, options = {}) {
  const maxElements = options.maxElements || 300;
  const checkStates = options.states !== false;
  const violations = [];
  const warnings = [];
  const measurements = [];
  const defaultFailures = new Set();

  let candidates = [];
  try {
    candidates = await page.evaluate(collectCandidates, maxElements);
  } catch (error) {
    warnings.push({
      rule: 'contrast-error',
      message: `No se pudo extraer la muestra de texto: ${error.message}`
    });
    return { violations, warnings, measurements };
  }

  for (const candidate of candidates) {
    const result = resolveContrast(candidate);
    if (!result) {
      warnings.push({
        rule: 'contrast-unparsed',
        element: candidate.selector,
        message: `Color no parseable (${candidate.color}); contraste indeterminado.`
      });
      continue;
    }

    const entry = {
      element: candidate.selector,
      text: candidate.text,
      ratio: Math.round(result.ratio * 100) / 100,
      required: result.required,
      foreground: candidate.color,
      backgrounds: candidate.backgrounds,
      fontSizePx: candidate.fontSizePx,
      fontWeight: candidate.fontWeight,
      large: result.large
    };
    measurements.push(entry);

    if (candidate.hasBackgroundImage) {
      warnings.push({
        rule: 'contrast-indeterminate',
        element: candidate.selector,
        message: `Fondo con imagen: el ratio ${entry.ratio}:1 no considera la imagen. Verificar a ojo o con captura.`,
        ratio: entry.ratio
      });
      continue;
    }

    if (result.ratio + 1e-6 < result.required) {
      defaultFailures.add(candidate.selector);
      violations.push({
        rule: 'contrast',
        impact: 'serious',
        element: candidate.selector,
        message: `Contraste ${entry.ratio}:1, bajo el mínimo ${result.required}:1 (WCAG 1.4.3 AA).`,
        text: candidate.text,
        ratio: entry.ratio,
        required: result.required
      });
    }
  }

  // Estados :focus — axe no los evalúa y es donde más se rompe el contraste.
  if (checkStates) {
    const focusables = await page.$$('button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    const limit = Math.min(focusables.length, options.maxStateElements || 12);
    for (let i = 0; i < limit; i++) {
      const handle = focusables[i];
      try {
        await handle.focus();
        const stateCandidate = await page.evaluate(() => {
          const el = document.activeElement;
          if (!el) return null;
          const styles = window.getComputedStyle(el);
          const ownText = Array.from(el.childNodes)
            .filter(n => n.nodeType === 3)
            .map(n => n.textContent.trim())
            .join(' ')
            .trim() || el.value || el.getAttribute('aria-label') || '';
          if (!ownText) return null;
          const chain = [];
          let node = el;
          while (node && node.nodeType === 1) {
            const s = window.getComputedStyle(node);
            chain.push(s.backgroundColor);
            const m = s.backgroundColor.match(/rgba?\(([^)]+)\)/i);
            if (m) {
              const parts = m[1].split(/[,\s/]+/).filter(Boolean).map(Number);
              const alpha = parts.length > 3 ? parts[3] : 1;
              if (alpha >= 1) break;
            }
            node = node.parentElement;
          }
          return {
            selector: el.tagName.toLowerCase() +
              (el.id ? '#' + el.id : '') +
              (el.classList && el.classList.length ? '.' + el.classList[0] : ''),
            text: ownText.slice(0, 60),
            color: styles.color,
            backgrounds: chain.filter(Boolean),
            fontSizePx: parseFloat(styles.fontSize) || 16,
            fontWeight: parseInt(styles.fontWeight, 10) || 400,
            opacity: parseFloat(styles.opacity) || 1
          };
        });

        if (stateCandidate) {
          const stateResult = resolveContrast(stateCandidate);
          if (
            stateResult &&
            stateResult.ratio + 1e-6 < stateResult.required &&
            // Si ya fallaba en reposo, el hallazgo es del par base, no del estado.
            !defaultFailures.has(stateCandidate.selector)
          ) {
            violations.push({
              rule: 'contrast-focus-state',
              impact: 'serious',
              element: `${stateCandidate.selector}:focus`,
              message: `En foco el contraste cae a ${Math.round(stateResult.ratio * 100) / 100}:1, bajo el mínimo ${stateResult.required}:1.`,
              text: stateCandidate.text,
              ratio: Math.round(stateResult.ratio * 100) / 100,
              required: stateResult.required
            });
          }
        }
      } catch (error) {
        // Un elemento que no se deja enfocar no es un hallazgo de contraste.
      }
    }
  }

  return { violations, warnings, measurements };
}

module.exports = {
  parseColor,
  relativeLuminance,
  compositeOver,
  compositeStack,
  contrastRatio,
  requiredRatio,
  resolveContrast,
  measureContrast
};
