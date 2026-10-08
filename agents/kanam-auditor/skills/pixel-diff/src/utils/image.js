'use strict';

const fs = require('fs');
const path = require('path');
const { PNG } = require('pngjs');
const pixelmatch = require('pixelmatch');

/**
 * Carga un PNG (o cualquier formato soportado por pngjs: PNG) desde disco.
 * Devuelve un objeto pngjs {width, height, data}.
 */
function loadPng(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Imagen no encontrada: ${filePath}`);
  }
  return PNG.sync.read(fs.readFileSync(filePath));
}

function writePng(png, filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, PNG.sync.write(png));
  return filePath;
}

/** Crea un PNG en blanco (útil para tests / debug). */
function createPng(width, height, rgba = [255, 255, 255, 255]) {
  const png = new PNG({ width, height });
  for (let i = 0; i < png.data.length; i += 4) {
    png.data[i] = rgba[0];
    png.data[i + 1] = rgba[1];
    png.data[i + 2] = rgba[2];
    png.data[i + 3] = rgba[3];
  }
  return png;
}

/** Rellena la región [x0,y0,x1,y1) con un color. */
function fillRect(png, x0, y0, x1, y1, rgba) {
  for (let y = y0; y < y1; y++) {
    for (let x = x0; x < x1; x++) {
      const i = (y * png.width + x) * 4;
      png.data[i] = rgba[0];
      png.data[i + 1] = rgba[1];
      png.data[i + 2] = rgba[2];
      png.data[i + 3] = rgba[3] === undefined ? 255 : rgba[3];
    }
  }
  return png;
}

/**
 * Redimensiona a exactamente width x height con muestreo bilineal (nearest
 * para escalados donde no importa el antialias). Se usa para "normalizar"
 * una captura real contra la resolución de la spec antes de hacer pixelmatch.
 */
function resize(png, width, height) {
  if (png.width === width && png.height === height) return png;
  const out = new PNG({ width, height });
  const xRatio = (png.width - 1) / Math.max(1, width - 1);
  const yRatio = (png.height - 1) / Math.max(1, height - 1);

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const srcX = x * xRatio;
      const srcY = y * yRatio;
      const x0 = Math.floor(srcX);
      const y0 = Math.floor(srcY);
      const x1 = Math.min(x0 + 1, png.width - 1);
      const y1 = Math.min(y0 + 1, png.height - 1);
      const dx = srcX - x0;
      const dy = srcY - y0;

      for (let c = 0; c < 4; c++) {
        const v =
          png.data[(y0 * png.width + x0) * 4 + c] * (1 - dx) * (1 - dy) +
          png.data[(y0 * png.width + x1) * 4 + c] * dx * (1 - dy) +
          png.data[(y1 * png.width + x0) * 4 + c] * (1 - dx) * dy +
          png.data[(y1 * png.width + x1) * 4 + c] * dx * dy;
        out.data[(y * width + x) * 4 + c] = Math.round(v);
      }
    }
 }
  return out;
}

/**
 * Diff binario real con pixelmatch.
 * @returns {diffPixels, totalPixels, ratio, regions:[{x,y,width,height,pixels}]}
 */
function diffImages(imgA, imgB, options = {}) {
  const threshold = options.threshold !== undefined ? options.threshold : 0.1;
  const includeAA = options.includeAA !== false;
  const width = Math.min(imgA.width, imgB.width);
  const height = Math.min(imgA.height, imgB.height);

  const a = resize(imgA, width, height);
  const b = resize(imgB, width, height);
  const diff = new PNG({ width, height });

  const diffPixels = pixelmatch(a.data, b.data, diff.data, width, height, {
    threshold,
    includeAA,
    alpha: 0.35,
    diffColor: [255, 0, 60]
  });

  return {
    diff,
    diffPixels,
    totalPixels: width * height,
    ratio: width * height ? diffPixels / (width * height) : 0,
    regions: findDiffRegions(diff, width, height)
  };
}

/**
 * Agrupa los píxeles marcados en el diff (rojo) en regiones contiguas usando
 * un union-find sobre una grilla reducida (celdas de 8px) para no explotar.
 * Devuelve las regiones ordenadas por cantidad de píxeles.
 */
function findDiffRegions(diffPng, width, height, cell = 8) {
  const cols = Math.ceil(width / cell);
  const rows = Math.ceil(height / cell);
  const grid = new Array(cols * rows).fill(0);

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const i = (y * width + x) * 4;
      const isDiff = diffPng.data[i] === 255 && diffPng.data[i + 1] === 0 && diffPng.data[i + 2] === 60;
      if (isDiff) grid[Math.floor(y / cell) * cols + Math.floor(x / cell)]++;
    }
  }

  const visited = new Array(cols * rows).fill(false);
  const regions = [];
  const neighbors = [[1, 0], [-1, 0], [0, 1], [0, -1]];

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const idx = r * cols + c;
      if (visited[idx] || grid[idx] === 0) continue;

      const stack = [[c, r]];
      visited[idx] = true;
      let minC = c, maxC = c, minR = r, maxR = r, pixels = 0;

      while (stack.length) {
        const [cc, rr] = stack.pop();
        const ci = rr * cols + cc;
        pixels += grid[ci];
        minC = Math.min(minC, cc); maxC = Math.max(maxC, cc);
        minR = Math.min(minR, rr); maxR = Math.max(maxR, rr);
        for (const [dc, dr] of neighbors) {
          const nc = cc + dc, nr = rr + dr;
          if (nc < 0 || nc >= cols || nr < 0 || nr >= rows) continue;
          const ni = nr * cols + nc;
          if (!visited[ni] && grid[ni] > 0) { visited[ni] = true; stack.push([nc, nr]); }
        }
      }

      regions.push({
        x: minC * cell,
        y: minR * cell,
        width: Math.min(width, (maxC + 1) * cell) - minC * cell,
        height: Math.min(height, (maxR + 1) * cell) - minR * cell,
        pixels
      });
    }
  }

  return regions.sort((a, b) => b.pixels - a.pixels).slice(0, 20);
}

module.exports = { loadPng, writePng, createPng, fillRect, resize, diffImages, findDiffRegions };
