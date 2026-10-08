'use strict';

const { captureElement } = require('../utils/capture');
const { extractReality } = require('../reality');
const { compareSpecs } = require('../comparator');
const { getSpec, loadSpecs } = require('../utils/specs');
const { buildTokensSpec, loadTokenSource } = require('../utils/tokens');
const { diffImages, loadPng } = require('../utils/image');

/**
 * Adapter modo COMP: una captura de diseño es la spec declarada; la realidad
 * se captura con Playwright y se compara. Opcionalmente también corre un
 * pixelmatch directo entre la captura de diseño y el render (solapamiento de
 * imagen) para detectar desalineación global.
 */
async function runComp(options) {
  const {
    designPath, url, route = '/', selector,
    config = {}, specPath, tokenSource
  } = options;

  // 1. Spec: declarada (specs.yaml) > tokens del DS > error.
  let spec = null;
  let specOrigin = null;

  if (designPath && specPath) {
    const specs = loadSpecs(specPath);
    spec = getSpec(specs, designPath);
    if (spec) specOrigin = `specs declaradas (${specPath})`;
  }
  if (!spec && tokenSource) {
    spec = buildTokensSpec(loadTokenSource(tokenSource));
    specOrigin = `tokens (${tokenSource})`;
  }
  if (!spec) {
    const err = new Error(
      'No hay spec para comparar. Declarala en .kanam/pixel-diff.specs.yaml ' +
      '(modo --interactive) o pasá una fuente de tokens con --tokens <path>.'
    );
    err.code = 'NO_SPEC';
    throw err;
  }

  // 2. Realidad: captura real + geometría.
  const capture = await captureElement({
    url, route, selector,
    viewport: config.viewport,
    deviceScaleFactor: config.deviceScaleFactor,
    fullPage: config.fullPage,
    headless: config.headless !== false,
    waitUntil: config.waitUntil || 'networkidle'
  });

  const reality = extractReality(capture.geometry, capture.buffer);

  // 3. Comparación métrica.
  const comparison = compareSpecs(spec, reality, config.thresholds || {}, config.checks || {});
  comparison.specOrigin = specOrigin;
  comparison.targetUrl = capture.targetUrl;

  // 4. Pixelmatch (si la captura de diseño es una imagen real comparable).
  let imageDiff = null;
  if (designPath && config.imageDiff !== false) {
    try {
      const designPng = loadPng(designPath);
      const renderPng = require('pngjs').PNG.sync.read(capture.buffer);
      imageDiff = diffImages(designPng, renderPng, {
        threshold: config.imageThreshold ?? 0.1,
        includeAA: config.includeAA !== false
      });
    } catch (e) {
      comparison.warnings.push({ type: 'image', message: `No se pudo comparar imagen: ${e.message}` });
    }
  }

  return { ...comparison, reality, imageDiff, capture: { buffer: capture.buffer, geometry: capture.geometry } };
}

module.exports = { runComp };
