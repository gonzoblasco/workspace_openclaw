'use strict';

const { chromium } = require('playwright-core');

/**
 * Captura real de un elemento/página con Playwright.
 *
 * Reemplaza al `captureReality()` simulado que devolvía objetos hardcodeados.
 * Devuelve el PNG en memoria + bounding boxes de las regiones relevantes del
 * DOM para poder muestrear color/spacing sobre la imagen real.
 */
async function captureElement(options) {
  const {
    url,
    route = '/',
    selector,
    viewport = { width: 1280, height: 800 },
    deviceScaleFactor = 1,
    waitUntil = 'networkidle',
    timeout = 30000,
    headless = true,
    fullPage = false
  } = options;

  const targetUrl = url.endsWith('/') && route.startsWith('/')
    ? `${url.slice(0, -1)}${route}`
    : `${url}${route}`;

  const browser = await chromium.launch({ headless });
  try {
    const context = await browser.newContext({ viewport, deviceScaleFactor });
    const page = await context.newPage();
    await page.goto(targetUrl, { waitUntil, timeout });

    let buffer;
    if (selector) {
      const locator = page.locator(selector).first();
      await locator.waitFor({ state: 'visible', timeout });
      buffer = await locator.screenshot({ type: 'png' });
    } else {
      await page.waitForLoadState('load', { timeout }).catch(() => {});
      buffer = await page.screenshot({ type: 'png', fullPage: !!fullPage });
    }

    // Extrae geometría real del DOM para las regiones que se van a medir.
    const geometry = await extractGeometry(page, selector);

    return { buffer, targetUrl, geometry, viewport };
  } finally {
    await browser.close();
  }
}

/**
 * Extrae estilos computados y bounding boxes de elementos clave. Es la fuente
 * "realidad" del DOM: color de fondo, color de texto, radios, paddings, etc.
 */
async function extractGeometry(page, rootSelector) {
  return page.evaluate((root) => {
    const pick = (el) => {
      const cs = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return {
        tag: el.tagName.toLowerCase(),
        classes: el.className && typeof el.className === 'string' ? el.className : '',
        text: (el.textContent || '').trim().slice(0, 60),
        rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
        styles: {
          backgroundColor: cs.backgroundColor,
          color: cs.color,
          borderRadius: cs.borderRadius,
          paddingTop: cs.paddingTop,
          paddingRight: cs.paddingRight,
          paddingBottom: cs.paddingBottom,
          paddingLeft: cs.paddingLeft,
          marginBottom: cs.marginBottom,
          fontSize: cs.fontSize,
          fontFamily: cs.fontFamily,
          fontWeight: cs.fontWeight,
          borderTopColor: cs.borderTopColor,
          borderTopWidth: cs.borderTopWidth
        }
      };
    };

    const scope = root ? document.querySelector(root) : document.body;
    const effectiveScope = scope || document.body;
    const nodes = [];
    const interesting = ['button', 'a', 'input', 'h1', 'h2', 'h3', 'p', 'div', 'section', 'article', 'header', 'nav', 'span', 'label'];

    const all = effectiveScope.querySelectorAll(interesting.join(','));
    let count = 0;
    for (const el of all) {
      if (count >= 200) break;
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) continue;
      nodes.push(pick(el));
      count++;
    }

    const rootRect = effectiveScope.getBoundingClientRect();
    return {
      root: {
        rect: { x: rootRect.x, y: rootRect.y, width: rootRect.width, height: rootRect.height },
        styles: pick(effectiveScope).styles
      },
      nodes
    };
  }, rootSelector || null);
}

module.exports = { captureElement, extractGeometry };
