'use strict';

/**
 * Adapter FIGMA — placeholder explícito.
 *
 * No hay API de Figma configurada. Este adapter NO fabrica specs: falla con un
 * error claro para que el pipeline no devuelva un veredicto inventado.
 *
 * Cuando se active (Fase 4 del roadmap), debe:
 *  1. Autenticar con un token (env FIGMA_TOKEN / config).
 *  2. Descargar nodos por file_id + node_id.
 *  3. Extraer spacing/radius/colors/typography reales y devolver un spec
 *     con la misma forma que buildTokensSpec().
 */
async function runFigma() {
  const err = new Error(
    'Adapter Figma no implementado. La fuente de verdad actual son capturas ' +
    'manuales (specs.yaml) o tokens del Design System. Ver ROADMAP Fase 4.'
  );
  err.code = 'FIGMA_NOT_IMPLEMENTED';
  throw err;
}

module.exports = { runFigma };
