'use strict';

const fs = require('fs');
const path = require('path');
const { loadPng, diffImages } = require('../utils/image');

/**
 * Adapter modo BASELINE: regresión visual real contra baselines versionados.
 * Compara 1:1 por nombre de archivo baseline/<name>.png vs current/<name>.png.
 */
function runBaseline(options) {
  const { baselineDir, currentDir, threshold = 0.1, tolerance = 0 } = options;

  if (!baselineDir || !currentDir) {
    throw new Error('Modo baseline requiere --baseline <dir> y --current <dir>.');
  }
  if (!fs.existsSync(baselineDir)) throw new Error(`Baseline no encontrado: ${baselineDir}`);
  if (!fs.existsSync(currentDir)) throw new Error(`Current no encontrado: ${currentDir}`);

  const images = listPngs(baselineDir);
  if (!images.length) throw new Error(`Baseline vacío: ${baselineDir}`);

  const results = [];
  const critical = [];
  const warnings = [];
  const missing = [];

  for (const name of images) {
    const currentPath = path.join(currentDir, name);
    if (!fs.existsSync(currentPath)) {
      missing.push(name);
      critical.push({ type: 'baseline', property: name, message: 'Falta la captura actual (no se puede verificar regresión)' });
      continue;
    }

    const base = loadPng(path.join(baselineDir, name));
    const curr = loadPng(currentPath);
    const diff = diffImages(base, curr, { threshold });

    const entry = {
      name,
      diffPixels: diff.diffPixels,
      ratio: diff.ratio,
      regions: diff.regions,
      diff
    };
    results.push(entry);

    if (diff.ratio > tolerance) {
      critical.push({
        type: 'baseline',
        property: name,
        message: `${diff.diffPixels}px de diferencia (${(diff.ratio * 100).toFixed(2)}%)`,
        regions: diff.regions
      });
    }
  }

  const totalChecks = results.length + missing.length;
  const misaligned = critical.length;

  return {
    alignment: totalChecks ? ((totalChecks - misaligned) / totalChecks) * 100 : 100,
    totalChecks,
    alignedCount: totalChecks - misaligned,
    misaligned,
    critical,
    warnings,
    aligned: results.filter((r) => !critical.find((c) => c.property === r.name)).map((r) => ({
      type: 'baseline', property: r.name,
      message: r.diffPixels === 0 ? 'idéntica' : `${r.diffPixels}px bajo tolerancia`
    })),
    skipped: [],
    diffs: results,
    missing
  };
}

function listPngs(dir) {
  return fs.readdirSync(dir).filter((f) => /\.png$/i.test(f)).sort();
}

module.exports = { runBaseline };
