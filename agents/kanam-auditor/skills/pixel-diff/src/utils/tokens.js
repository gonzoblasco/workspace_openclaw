'use strict';

const fs = require('fs');
const path = require('path');

/**
 * Resolución REAL de tokens del Design System.
 *
 * Antes `extractTokensSpec()` devolvía strings tipo "var(--k-space-4)" que
 * nunca se resolvían: la comparación contra la realidad era imposible. Acá se
 * cargan los tokens (DTCG `kanam.tokens.json` o un CSS de tokens) y se
 * resuelven las referencias `{primitive.color.teal.700}` / `var(--k-...)`.
 */

/** Aplana un árbol DTCG a un mapa de claves punto-separadas. */
function flattenTokens(obj, prefix = '', out = {}) {
  for (const [key, value] of Object.entries(obj)) {
    if (key.startsWith('$')) continue;
    const full = prefix ? `${prefix}.${key}` : key;
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      if ('$value' in value) {
        out[full] = value.$value;
      } else {
        flattenTokens(value, full, out);
      }
    } else if (typeof value === 'string') {
      out[full] = value;
    }
  }
  return out;
}

/** Resuelve referencias `{a.b.c}` con profundidad máxima. */
function resolveReferences(map, maxDepth = 10) {
  const resolved = { ...map };
  const refPattern = /\{([^}]+)\}/g;

  for (let depth = 0; depth < maxDepth; depth++) {
    let changed = false;
    for (const [key, value] of Object.entries(resolved)) {
      if (typeof value !== 'string' || !value.includes('{')) continue;
      const next = value.replace(refPattern, (_, ref) => {
        if (resolved[ref] !== undefined && !String(resolved[ref]).includes('{')) return resolved[ref];
        return resolved[ref] !== undefined ? resolved[ref] : `{${ref}}`;
      });
      if (next !== value) { resolved[key] = next; changed = true; }
    }
    if (!changed) break;
  }
  return resolved;
}

/** Lee variables CSS `--k-*: value;` de un archivo o varios. */
function parseCssVariables(cssContent) {
  const map = {};
  const re = /(--[\w-]+)\s*:\s*([^;]+);/g;
  let m;
  while ((m = re.exec(cssContent))) {
    map[m[1]] = m[2].trim();
  }
  return map;
}

/** Resuelve var(--x) dentro de un mapa CSS, con fallbacks --k-. */
function resolveCssVars(map, maxDepth = 10) {
  const resolved = { ...map };
  const re = /var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)/;
  for (let d = 0; d < maxDepth; d++) {
    let changed = false;
    for (const [key, value] of Object.entries(resolved)) {
      if (typeof value !== 'string' || !value.includes('var(')) continue;
      const next = value.replace(/var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)/g, (_, name, fb) => {
        if (resolved[name] !== undefined && !String(resolved[name]).includes('var(')) return resolved[name];
        return fb !== undefined ? fb.trim() : `var(${name})`;
      });
      if (next !== value) { resolved[key] = next; changed = true; }
    }
    if (!changed) break;
  }
  return resolved;
}

/**
 * Carga tokens desde una ruta: si es .json (DTCG) flatten+resolve; si es un
 * directorio busca *.tokens.json / dist/*.css; si es .css parsea variables.
 */
function loadTokenSource(sourcePath) {
  const abs = path.resolve(sourcePath);
  if (!fs.existsSync(abs)) {
    throw new Error(`Fuente de tokens no encontrada: ${abs}`);
  }

  const stat = fs.statSync(abs);
  let files = [];
  if (stat.isDirectory()) {
    const walk = (dir) => {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const p = path.join(dir, entry.name);
        if (entry.isDirectory()) walk(p);
        else if (/\.(tokens\.)?json$/.test(entry.name) || /\.css$/.test(entry.name)) files.push(p);
      }
    };
    walk(abs);
  } else {
    files = [abs];
  }

  let map = {};
  for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');
    if (file.endsWith('.json')) {
      const json = JSON.parse(content);
      Object.assign(map, resolveReferences(flattenTokens(json)));
    } else if (file.endsWith('.css')) {
      Object.assign(map, resolveCssVars(parseCssVariables(content)));
    }
  }
  return map;
}

/**
 * Normaliza el mapa de tokens a un "spec" comparable contra la realidad.
 * Expone tanto claves semánticas (--k-brand-primary) como de primitivas.
 */
function buildTokensSpec(tokenMap) {
  const get = (...candidates) => {
    for (const c of candidates) {
      if (tokenMap[c] !== undefined) return tokenMap[c];
    }
    return null;
  };

  const primary = get(
    'semantic.brand.primary', '--k-brand-primary', '--k-color-primary',
    'brand.primary'
  );

  return {
    source: 'design-system',
    resolved: tokenMap,
    spacing: {
      padding_internal: get('primitive.space.4', '--k-space-4', 'space.4') || '16px',
      margin_between: get('primitive.space.6', '--k-space-6', 'space.6', 'primitive.space.8') || '32px'
    },
    radius: {
      card: get('primitive.radius.lg', '--k-radius-lg', 'radius.lg') || '16px',
      button: get('primitive.radius.md', '--k-radius-md', 'radius.md') || '12px'
    },
    colors: {
      background: get('semantic.surface.background', '--k-bg-surface', '--k-bg-main', 'primitive.color.neutral.0') || '#ffffff',
      primary: primary || '#0d9488',
      text: get('semantic.text.primary', '--k-text-main', 'primitive.color.neutral.900') || '#111318'
    },
    typography: {
      title_size: get('primitive.font.size.xl', '--k-font-size-xl', 'font.size.xl') || '22px',
      font_family: (get('primitive.font.family.body', '--k-font-family-body') || 'Inter, sans-serif').split(',')[0].trim().replace(/['"]/g, '')
    }
  };
}

module.exports = {
  flattenTokens,
  resolveReferences,
  parseCssVariables,
  resolveCssVars,
  loadTokenSource,
  buildTokensSpec
};
