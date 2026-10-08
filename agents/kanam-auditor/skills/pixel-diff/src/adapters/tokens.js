'use strict';

const { captureElement } = require('../utils/capture');
const { extractReality } = require('../reality');
const { compareSpecs } = require('../comparator');
const { buildTokensSpec, loadTokenSource } = require('../utils/tokens');

/**
 * Adapter modo TOKENS: el Design System es la spec. Se valida que el render
 * consuma realmente los tokens declarados (color, spacing, radius, tipografía).
 */
async function runTokens(options) {
  const { tokenSource, url, route = '/', selector, config = {} } = options;

  if (!tokenSource) {
    throw new Error('Modo tokens requiere --tokens <path> al Design System (.json o .css).');
  }

  const tokenMap = loadTokenSource(tokenSource);
  const spec = buildTokensSpec(tokenMap);
  const resolvedCount = Object.keys(tokenMap).length;
  if (resolvedCount === 0) {
    throw new Error(`No se resolvieron tokens desde ${tokenSource}.`);
  }

  const capture = await captureElement({
    url, route, selector,
    viewport: config.viewport,
    deviceScaleFactor: config.deviceScaleFactor,
    fullPage: config.fullPage,
    headless: config.headless !== false,
    waitUntil: config.waitUntil || 'networkidle'
  });

  const reality = extractReality(capture.geometry, capture.buffer);
  const comparison = compareSpecs(spec, reality, config.thresholds || {}, config.checks || {});

  comparison.specOrigin = `tokens (${tokenSource}, ${resolvedCount} resueltos)`;
  comparison.targetUrl = capture.targetUrl;

  return { ...comparison, reality, spec, capture: { buffer: capture.buffer, geometry: capture.geometry } };
}

module.exports = { runTokens };
