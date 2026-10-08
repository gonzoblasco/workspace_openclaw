'use strict';

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const readline = require('readline');

const DEFAULT_SPEC_FILE = '.kanam/pixel-diff.specs.yaml';

/**
 * Specs declaradas manualmente por captura. Cuando no hay Figma ni tokens
 * suficientes, el humano declara los valores esperados una vez y quedan
 * versionados en `.kanam/pixel-diff.specs.yaml`. Esto reemplaza la "visión
 * mágica": no se inventan specs, se declaran y se persisten.
 */

function loadSpecs(specPath = DEFAULT_SPEC_FILE) {
  const abs = path.resolve(specPath);
  if (!fs.existsSync(abs)) return { specs: {} };
  try {
    const loaded = yaml.load(fs.readFileSync(abs, 'utf8'));
    return loaded && typeof loaded === 'object' ? loaded : { specs: {} };
  } catch (e) {
    throw new Error(`Specs inválidas en ${abs}: ${e.message}`);
  }
}

function saveSpecs(data, specPath = DEFAULT_SPEC_FILE) {
  const abs = path.resolve(specPath);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, yaml.dump(data, { lineWidth: 120 }), 'utf8');
  return abs;
}

function getSpec(specs, key) {
  if (!specs || !specs.specs) return null;
  const byKey = specs.specs[key];
  if (byKey) return byKey;
  // Match por basename de la captura
  const base = path.basename(key);
  for (const [k, v] of Object.entries(specs.specs)) {
    if (path.basename(k) === base) return v;
  }
  return null;
}

async function prompt(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => rl.question(question, (answer) => { rl.close(); resolve(answer.trim()); }));
}

/**
 * Modo interactivo: pregunta los valores esperados y devuelve el spec a
 * persistir. No se usa cuando no hay TTY.
 */
async function collectInteractive(designPath, presets = {}) {
  const ask = async (label, fallback) => {
    const answer = await prompt(`${label}${fallback ? ` [${fallback}]` : ''}: `);
    return answer || fallback || null;
  };

  return {
    name: path.basename(designPath || 'spec'),
    spacing: {
      padding_internal: await ask('Padding interno (px)', presets.padding_internal),
      margin_between: await ask('Margen entre elementos (px)', presets.margin_between)
    },
    radius: {
      card: await ask('Radio de card (px)', presets.radius_card),
      button: await ask('Radio de botón (px)', presets.radius_button)
    },
    colors: {
      primary: await ask('Color primario (hex)', presets.color_primary),
      background: await ask('Color de fondo (hex)', presets.color_background),
      text: await ask('Color de texto (hex)', presets.color_text)
    },
    typography: {
      title_size: await ask('Tamaño de título (px)', presets.title_size),
      font_family: await ask('Font family', presets.font_family)
    }
  };
}

module.exports = { DEFAULT_SPEC_FILE, loadSpecs, saveSpecs, getSpec, collectInteractive };
