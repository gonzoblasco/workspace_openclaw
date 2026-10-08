'use strict';

const { PNG } = require('pngjs');
const { averageRegionColor, parseColor, deltaE2000, rgbToHex } = require('./utils/color');

/**
 * Construye la "realidad" a partir de una captura real + geometría del DOM.
 *
 * Dos fuentes complementarias, y se declara de dónde salió cada valor:
 *  - PÍXEL: muestreo del color realmente renderizado en la región del elemento.
 *  - DOM:   estilos computados (spacing/radius/font) que no son medibles de
 *           forma fiable píxel a píxel sin mucho ruido.
 *
 * Cuando un valor no es medible, se devuelve null (no un valor inventado).
 */

function toAbsoluteRect(rect, rootRect) {
  return {
    x: rect.x - rootRect.x,
    y: rect.y - rootRect.y,
    width: rect.width,
    height: rect.height
  };
}

/** Media de color de la región central de un elemento (evita bordes/AA). */
function sampleElementColor(png, rect, insetRatio = 0.2) {
  const insetX = rect.width * insetRatio;
  const insetY = rect.height * insetRatio;
  const x0 = Math.round(rect.x + insetX);
  const y0 = Math.round(rect.y + insetY);
  const x1 = Math.round(rect.x + rect.width - insetX);
  const y1 = Math.round(rect.y + rect.height - insetY);
  if (x1 <= x0 || y1 <= y0) return null;
  return averageRegionColor(png, x0, y0, x1, y1);
}

function isNeutralColor(hex, satThreshold = 18) {
  const c = parseColor(hex);
  if (!c) return true;
  const max = Math.max(c.r, c.g, c.b);
  const min = Math.min(c.r, c.g, c.b);
  return max - min < satThreshold;
}

function findRootNode(geometry) {
  return geometry.root;
}

/**
 * Selecciona el elemento "primario" (acción principal): primer botón visible;
 * si no hay, el primer <a> con fondo no neutro.
 */
function findPrimaryNode(nodes) {
  const buttons = nodes.filter((n) => n.tag === 'button');
  for (const b of buttons) {
    const bg = b.styles.backgroundColor;
    if (bg && bg !== 'rgba(0, 0, 0, 0)' && !isNeutralColor(rgbToHex(parseColor(bg) || { r: 0, g: 0, b: 0 }))) {
      return b;
    }
  }
  if (buttons.length) return buttons[0];
  const anchors = nodes.filter((n) => n.tag === 'a' && n.styles.backgroundColor !== 'rgba(0, 0, 0, 0)');
  return anchors[0] || null;
}

/** Elemento tipo card/superficie: bloque con fondo opaco y radio visible. */
function findCardNode(nodes) {
  const opaque = (node) => {
    const bg = node.styles.backgroundColor;
    if (!bg || bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') return false;
    const c = parseColor(bg);
    return !!c && (c.a === undefined || c.a > 0.9);
  };

  const candidates = nodes
    .filter((n) => ['div', 'article', 'section'].includes(n.tag))
    .filter((n) => n.rect.width >= 80 && n.rect.height >= 60)
    .filter((n) => n.styles.paddingTop && n.styles.paddingTop !== '0px')
    .filter(opaque)
    .filter((n) => (parseFloat(n.styles.borderRadius) || 0) > 0);

  return candidates.sort((a, b) => b.rect.width * b.rect.height - a.rect.width * a.rect.height)[0] || null;
}

/** Margen vertical entre dos hermanos del contenedor del card. */
function measureSiblingGap(node, nodes) {
  if (!node) return null;
  const siblings = nodes
    .filter((n) => n !== node && Math.abs(n.rect.x - node.rect.x) < 4 && n.rect.height > 20)
    .filter((n) => n.rect.y >= node.rect.y + node.rect.height - 2)
    .sort((a, b) => a.rect.y - b.rect.y);
  if (!siblings.length) return null;
  const next = siblings[0];
  const gap = next.rect.y - (node.rect.y + node.rect.height);
  return gap >= 0 ? Math.round(gap) : null;
}

function extractReality(geometry, pngBuffer) {
  const png = PNG.sync.read(pngBuffer);
  const root = findRootNode(geometry);
  const rootRect = root.rect;
  const nodes = geometry.nodes.map((n) => ({ ...n, absRect: toAbsoluteRect(n.rect, rootRect) }));

  const primary = findPrimaryNode(nodes);
  const card = findCardNode(nodes);
  const heading = nodes.find((n) => ['h1', 'h2'].includes(n.tag)) || nodes.find((n) => parseFloat(n.styles.fontSize) >= 22) || null;

  const primarySample = primary ? sampleElementColor(png, primary.absRect) : null;
  const cardSample = card ? sampleElementColor(png, card.absRect, 0.5) : null;
  const headingSample = heading ? sampleElementColor(png, heading.absRect, 0.3) : null;
  const body = nodes.find((n) => n.tag === 'p') || null;
  const bodySample = body ? sampleElementColor(png, body.absRect, 0.3) : null;

  const evidence = [];
  const noteIf = (label, sampled, computed) => {
    if (!sampled) return;
    const { deltaE } = deltaE2000(sampled.average, computed);
    evidence.push({
      label,
      sampledPx: sampled.average,
      computedStyle: rgbToHex(parseColor(computed) || { r: 0, g: 0, b: 0 }),
      deltaE,
      note: deltaE > 2.3 ? 'El render no coincide con el estilo computado (posible overlays/AA)' : 'coherente'
    });
  };
  if (primary) noteIf('primary', primarySample, primary.styles.backgroundColor);
  if (card) noteIf('surface', cardSample, card.styles.backgroundColor);

  const paddingTop = card ? card.styles.paddingTop : null;
  const titleSize = heading ? heading.styles.fontSize : null;

  return {
    source: 'rendered',
    capture: { width: png.width, height: png.height },
    spacing: {
      padding_internal: paddingTop,
      margin_between: measureSiblingGap(card, nodes) !== null ? `${measureSiblingGap(card, nodes)}px` : null
    },
    radius: {
      card: card ? normalizeRadius(card.styles.borderRadius) : null,
      button: primary ? normalizeRadius(primary.styles.borderRadius) : null
    },
    colors: {
      primary: primarySample ? primarySample.dominant || primarySample.average : (primary ? rgbToHex(parseColor(primary.styles.backgroundColor) || { r: 0, g: 0, b: 0 }) : null),
      background: cardSample ? (cardSample.dominant || cardSample.average) : (card ? rgbToHex(parseColor(card.styles.backgroundColor) || { r: 255, g: 255, b: 255 }) : null),
      text: body ? rgbToHex(parseColor(body.styles.color) || { r: 0, g: 0, b: 0 }) : (heading ? rgbToHex(parseColor(heading.styles.color) || { r: 0, g: 0, b: 0 }) : null)
    },
    typography: {
      title_size: titleSize,
      font_family: heading ? heading.styles.fontFamily : null
    },
    elements: {
      primary: primary ? { tag: primary.tag, classes: primary.classes, rect: primary.absRect } : null,
      card: card ? { tag: card.tag, classes: card.classes, rect: card.absRect } : null,
      heading: heading ? { tag: heading.tag, classes: heading.classes, rect: heading.absRect } : null
    },
    sampledEvidence: evidence
  };
}

/** "8px" o "8px 8px 8px 8px" -> "8px". */
function normalizeRadius(borderRadius) {
  if (!borderRadius) return null;
  return String(borderRadius).trim().split(/\s+/)[0];
}

module.exports = { extractReality, sampleElementColor, isNeutralColor, findPrimaryNode, findCardNode, normalizeRadius };
