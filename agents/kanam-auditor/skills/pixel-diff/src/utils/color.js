'use strict';

/**
 * Utilidades de color: parseo, conversión y distancia perceptual (Delta E).
 *
 * A diferencia de la versión simulada anterior, acá NO se devuelve 0 para
 * tokens ni se usa distancia euclídea RGB cruda como si fuese Delta E.
 * Se implementa CIE76 (euclídea en Lab) y CIEDE2000 (perceptual real),
 * que es el estándar contra el que se fija `color_delta_e: 2.3`.
 */

const NAMED_COLORS = {
  white: '#ffffff',
  black: '#000000',
  red: '#ff0000',
  green: '#008000',
  blue: '#0000ff',
  transparent: null // sin color
};

/** Normaliza #rgb/#rrggbb/rgb(...)/rgba(...)/nombre -> {r,g,b,a}. */
function parseColor(input) {
  if (input === null || input === undefined) return null;
  if (typeof input !== 'string') return null;
  const value = input.trim().toLowerCase();

  if (value === 'transparent') return { r: 0, g: 0, b: 0, a: 0 };
  if (NAMED_COLORS[value]) return parseColor(NAMED_COLORS[value]);

  let m = /^#?([a-f\d])([a-f\d])([a-f\d])$/i.exec(value);
  if (m) {
    return {
      r: parseInt(m[1] + m[1], 16),
      g: parseInt(m[2] + m[2], 16),
      b: parseInt(m[3] + m[3], 16),
      a: 1
    };
  }

  m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})?$/i.exec(value);
  if (m) {
    return {
      r: parseInt(m[1], 16),
      g: parseInt(m[2], 16),
      b: parseInt(m[3], 16),
      a: m[4] !== undefined ? parseInt(m[4], 16) / 255 : 1
    };
  }

  m = /^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)$/.exec(value);
  if (m) {
    return {
      r: Math.round(parseFloat(m[1])),
      g: Math.round(parseFloat(m[2])),
      b: Math.round(parseFloat(m[3])),
      a: m[4] !== undefined ? parseFloat(m[4]) : 1
    };
  }

  return null;
}

function rgbToHex({ r, g, b }) {
  const toHex = (n) => Math.max(0, Math.min(255, Math.round(n))).toString(16).padStart(2, '0');
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`.toLowerCase();
}

/** sRGB -> Lab (D65). Necesario para Delta E real. */
function rgbToLab({ r, g, b }) {
  const pivotRgb = (c) => {
    const v = c / 255;
    return v > 0.04045 ? Math.pow((v + 0.055) / 1.055, 2.4) : v / 12.92;
  };
  const pivotXyz = (c) => (c > 0.008856 ? Math.cbrt(c) : 7.787 * c + 16 / 116);

  const rl = pivotRgb(r);
  const gl = pivotRgb(g);
  const bl = pivotRgb(b);

  // D65, escalados a 0..1
  const x = (rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375) / 0.95047;
  const y = rl * 0.2126729 + gl * 0.7151522 + bl * 0.072175;
  const z = (rl * 0.0193339 + gl * 0.119192 + bl * 0.9503041) / 1.08883;

  const fx = pivotXyz(x);
  const fy = pivotXyz(y);
  const fz = pivotXyz(z);

  return {
    l: 116 * fy - 16,
    a: 500 * (fx - fy),
    b: 200 * (fy - fz)
  };
}

/** CIE76: distancia euclídea en espacio Lab. */
function deltaE76(c1, c2) {
  const rgb1 = parseColor(c1);
  const rgb2 = parseColor(c2);
  if (!rgb1 || !rgb2) return { deltaE: 999, rgb1, rgb2, formula: 'CIE76', note: 'color inválido' };
  const lab1 = rgbToLab(rgb1);
  const lab2 = rgbToLab(rgb2);
  const d = Math.sqrt(
    Math.pow(lab1.l - lab2.l, 2) +
    Math.pow(lab1.a - lab2.a, 2) +
    Math.pow(lab1.b - lab2.b, 2)
  );
  return { deltaE: round2(d), rgb1, rgb2, lab1, lab2, formula: 'CIE76' };
}

/** CIEDE2000: distancia perceptual real (Sharma et al.). */
function deltaE2000(colorA, colorB) {
  const rgb1 = parseColor(colorA);
  const rgb2 = parseColor(colorB);
  if (!rgb1 || !rgb2) return { deltaE: 999, rgb1, rgb2, formula: 'CIEDE2000', note: 'color inválido' };

  const lab1 = rgbToLab(rgb1);
  const lab2 = rgbToLab(rgb2);

  const kL = 1, kC = 1, kH = 1;
  const rad = (degree) => (degree * Math.PI) / 180;
  const toDeg = (r) => (r * 180) / Math.PI;

  const c1 = Math.sqrt(lab1.a * lab1.a + lab1.b * lab1.b);
  const c2 = Math.sqrt(lab2.a * lab2.a + lab2.b * lab2.b);
  const cBar = (c1 + c2) / 2;

  const g = 0.5 * (1 - Math.sqrt(Math.pow(cBar, 7) / (Math.pow(cBar, 7) + Math.pow(25, 7))));
  const a1p = (1 + g) * lab1.a;
  const a2p = (1 + g) * lab2.a;
  const c1p = Math.sqrt(a1p * a1p + lab1.b * lab1.b);
  const c2p = Math.sqrt(a2p * a2p + lab2.b * lab2.b);

  const hp = (a, b) => {
    if (a === 0 && b === 0) return 0;
    const angle = toDeg(Math.atan2(b, a));
    return angle >= 0 ? angle : angle + 360;
  };
  const h1p = hp(a1p, lab1.b);
  const h2p = hp(a2p, lab2.b);

  const dLp = lab2.l - lab1.l;
  const dCp = c2p - c1p;

  let dhp;
  if (c1p * c2p === 0) dhp = 0;
  else if (Math.abs(h2p - h1p) <= 180) dhp = h2p - h1p;
  else if (h2p - h1p > 180) dhp = h2p - h1p - 360;
  else dhp = h2p - h1p + 360;
  const dHp = 2 * Math.sqrt(c1p * c2p) * Math.sin(rad(dhp / 2));

  const lBarP = (lab1.l + lab2.l) / 2;
  const cBarP = (c1p + c2p) / 2;

  let hBarP;
  if (c1p * c2p === 0) hBarP = h1p + h2p;
  else if (Math.abs(h1p - h2p) <= 180) hBarP = (h1p + h2p) / 2;
  else if (h1p + h2p < 360) hBarP = (h1p + h2p + 360) / 2;
  else hBarP = (h1p + h2p - 360) / 2;

  const t = 1 -
    0.17 * Math.cos(rad(hBarP - 30)) +
    0.24 * Math.cos(rad(2 * hBarP)) +
    0.32 * Math.cos(rad(3 * hBarP + 6)) -
    0.20 * Math.cos(rad(4 * hBarP - 63));

  const dTheta = 30 * Math.exp(-Math.pow((hBarP - 275) / 25, 2));
  const rc = 2 * Math.sqrt(Math.pow(cBarP, 7) / (Math.pow(cBarP, 7) + Math.pow(25, 7)));
  const sl = 1 + (0.015 * Math.pow(lBarP - 50, 2)) / Math.sqrt(20 + Math.pow(lBarP - 50, 2));
  const sc = 1 + 0.045 * cBarP;
  const sh = 1 + 0.015 * cBarP * t;
  const rt = -Math.sin(rad(2 * dTheta)) * rc;

  const dE = Math.sqrt(
    Math.pow(dLp / (kL * sl), 2) +
    Math.pow(dCp / (kC * sc), 2) +
    Math.pow(dHp / (kH * sh), 2) +
    rt * (dCp / (kC * sc)) * (dHp / (kH * sh))
  );

  return { deltaE: round2(dE), rgb1, rgb2, lab1, lab2, formula: 'CIEDE2000' };
}

function round2(n) {
  return Math.round(n * 100) / 100;
}

/**
 * Media de color en una región de imagen (objeto pngjs con .data RGBA).
 * Ignora píxeles transparentes. Devuelve el promedio y el color dominante.
 */
function averageRegionColor(png, x0, y0, x1, y1) {
  const { width, height, data } = png;
  const clamp = (v, max) => Math.max(0, Math.min(max, Math.round(v)));
  const ax0 = clamp(x0, width - 1);
  const ay0 = clamp(y0, height - 1);
  const ax1 = clamp(x1, width);
  const ay1 = clamp(y1, height);

  let r = 0, g = 0, b = 0, n = 0;
  const buckets = new Map();

  for (let y = ay0; y < ay1; y++) {
    for (let x = ax0; x < ax1; x++) {
      const i = (y * width + x) * 4;
      const a = data[i + 3];
      if (a === 0) continue;
      r += data[i]; g += data[i + 1]; b += data[i + 2]; n++;
      const key = `${data[i] >> 4},${data[i + 1] >> 4},${data[i + 2] >> 4}`;
      buckets.set(key, (buckets.get(key) || 0) + 1);
    }
  }

  if (n === 0) return { average: null, dominant: null, samples: 0 };

  let domKey = null, domCount = -1;
  for (const [k, count] of buckets) if (count > domCount) { domKey = k; domCount = count; }

  // Recalcular el promedio exacto del bucket dominante
  let dr = 0, dg = 0, db = 0, dn = 0;
  for (let y = ay0; y < ay1; y++) {
    for (let x = ax0; x < ax1; x++) {
      const i = (y * width + x) * 4;
      if (data[i + 3] === 0) continue;
      const key = `${data[i] >> 4},${data[i + 1] >> 4},${data[i + 2] >> 4}`;
      if (key === domKey) { dr += data[i]; dg += data[i + 1]; db += data[i + 2]; dn++; }
    }
  }

  return {
    average: rgbToHex({ r: r / n, g: g / n, b: b / n }),
    dominant: dn ? rgbToHex({ r: dr / dn, g: dg / dn, b: db / dn }) : null,
    samples: n
  };
}

module.exports = {
  parseColor,
  rgbToHex,
  rgbToLab,
  deltaE76,
  deltaE2000,
  averageRegionColor,
  round2
};
