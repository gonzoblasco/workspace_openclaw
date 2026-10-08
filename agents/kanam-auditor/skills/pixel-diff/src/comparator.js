'use strict';

const { deltaE2000 } = require('./utils/color');

/**
 * Comparador de specs declaradas (tokens o captura con specs) contra la
 * realidad medida en el DOM. Toda magnitud se reporta con su valor numérico
 * real: nada de "casi bien".
 */

/** "16px" -> 16 ; "1.5rem" -> 24 ; "0.5em" -> 8 ; null si no es medible. */
function toPx(value, rootFontSize = 16) {
  if (value === null || value === undefined) return null;
  if (typeof value === 'number') return value;
  const str = String(value).trim();
  if (str.includes('var(')) return null;
  if (str === '0') return 0;

  const m = /^(-?[\d.]+)\s*(px|rem|em|pt)?$/.exec(str);
  if (!m) return null;
  const n = parseFloat(m[1]);
  switch (m[2]) {
    case 'rem':
    case 'em': return n * rootFontSize;
    case 'pt': return (n * 96) / 72;
    case 'px':
    default: return n;
  }
}

function parseRadiusCorners(borderRadius) {
  if (!borderRadius) return null;
  const first = String(borderRadius).trim().split(/\s+/)[0];
  return toPx(first);
}

function compareSpacing(metric) {
  const { expected, actual, tolerance } = metric;
  const e = toPx(expected);
  const a = toPx(actual);
  if (e === null || a === null) {
    return { status: 'unmeasurable', metric, note: 'Valor no resoluble a px (¿token sin resolver?)' };
  }
  const diff = Math.abs(e - a);
  return {
    status: diff <= tolerance ? 'aligned' : 'misaligned',
    metric,
    expectedPx: e,
    actualPx: a,
    difference: Math.round(diff * 100) / 100
  };
}

function compareColor(metric) {
  const { expected, actual, tolerance } = metric;
  if (typeof expected === 'string' && typeof actual === 'string' &&
      expected.includes('var(') && actual.includes('var(')) {
    return {
      status: expected === actual ? 'aligned' : 'misaligned',
      metric, note: 'Comparación por igualdad de token'
    };
  }
  const { deltaE } = deltaE2000(expected, actual);
  return {
    status: deltaE <= tolerance ? 'aligned' : 'misaligned',
    metric,
    deltaE,
    expectedHex: require('./utils/color').rgbToHex(require('./utils/color').parseColor(expected) || { r: 0, g: 0, b: 0 }),
    actualHex: require('./utils/color').rgbToHex(require('./utils/color').parseColor(actual) || { r: 0, g: 0, b: 0 })
  };
}

/**
 * Compara un spec completo contra la realidad medida.
 * @param {object} spec {spacing,radius,colors,typography}
 * @param {object} reality idem
 * @param {object} thresholds
 * @param {object} checks flags por tipo
 */
function compareSpecs(spec, reality, thresholds = {}, checks = {}) {
  const t = {
    spacing: thresholds.spacing_tolerance ?? thresholds.spacing ?? 1,
    radius: thresholds.radius_tolerance ?? thresholds.radius ?? 0.5,
    color: thresholds.color_delta_e ?? thresholds.color ?? 2.3,
    typography: thresholds.typography_scale ?? 0.1
  };

  const critical = [];
  const warnings = [];
  const aligned = [];
  const skipped = [];
  let totalChecks = 0;
  let alignedCount = 0;

  const record = (result, kind, severity, suggestion) => {
    totalChecks++;
    const entry = {
      type: kind,
      property: result.metric.property,
      expected: result.metric.expected,
      actual: result.metric.actual,
      ...result
    };
    if (result.status === 'aligned') {
      alignedCount++;
      aligned.push(entry);
    } else if (result.status === 'unmeasurable') {
      skipped.push(entry);
    } else if (severity === 'critical') {
      critical.push({ ...entry, suggestion });
    } else {
      warnings.push({ ...entry, suggestion });
    }
  };

  if (checks.spacing_alignment !== false) {
    for (const [prop, pair] of Object.entries({
      padding_internal: [spec.spacing?.padding_internal, reality.spacing?.padding_internal],
      margin_between: [spec.spacing?.margin_between, reality.spacing?.margin_between]
    })) {
      if (pair[0] == null || pair[1] == null) continue;
      record(
        compareSpacing({ property: prop, expected: pair[0], actual: pair[1], tolerance: t.spacing }),
        'spacing', 'warning',
        'Ajustar el valor para que coincida con el token de espaciado.'
      );
    }
  }

  if (checks.radius_consistency !== false) {
    for (const [prop, pair] of Object.entries({
      card: [spec.radius?.card, reality.radius?.card],
      button: [spec.radius?.button, reality.radius?.button]
    })) {
      if (pair[0] == null || pair[1] == null) continue;
      record(
        compareSpacing({ property: `radius_${prop}`, expected: pair[0], actual: pair[1], tolerance: t.radius }),
        'radius', 'critical',
        'El radio es exacto: usar el token de radius declarado.'
      );
    }
  }

  if (checks.color_accuracy !== false) {
    for (const [prop, pair] of Object.entries({
      primary: [spec.colors?.primary, reality.colors?.primary],
      background: [spec.colors?.background, reality.colors?.background],
      text: [spec.colors?.text, reality.colors?.text]
    })) {
      if (pair[0] == null || pair[1] == null) continue;
      record(
        compareColor({ property: prop, expected: pair[0], actual: pair[1], tolerance: t.color }),
        'color', 'critical',
        'Revisar el token semántico de color.'
      );
    }
  }

  if (checks.typography_scale !== false) {
    if (spec.typography?.title_size != null && reality.typography?.title_size != null) {
      record(
        compareSpacing({
          property: 'title_size',
          expected: spec.typography.title_size,
          actual: reality.typography.title_size,
          tolerance: t.typography
        }),
        'typography', 'warning',
        'Revisar la escala tipográfica.'
      );
    }
    if (spec.typography?.font_family != null && reality.typography?.font_family != null) {
      const normalize = (f) => String(f).split(',')[0].trim().replace(/['"]/g, '').toLowerCase();
      const match = normalize(spec.typography.font_family) === normalize(reality.typography.font_family);
      totalChecks++;
      const entry = {
        type: 'typography', property: 'font_family',
        expected: spec.typography.font_family, actual: reality.typography.font_family
      };
      if (match) { alignedCount++; aligned.push(entry); }
      else warnings.push({ ...entry, suggestion: 'Verificar si el font-family es intencional.' });
    }
  }

  return {
    alignment: totalChecks > 0 ? (alignedCount / totalChecks) * 100 : 100,
    totalChecks,
    alignedCount,
    misaligned: totalChecks - alignedCount,
    critical,
    warnings,
    aligned,
    skipped
  };
}

module.exports = { toPx, parseRadiusCorners, compareSpacing, compareColor, compareSpecs };
