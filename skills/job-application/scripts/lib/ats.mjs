// ats.mjs - Registro de adaptadores de ATS y detección automática
//
// POR QUÉ EXISTE (2026-10-23): los scripts de referencia ya tenían los
// adapters (lever, ashby, eightfold) replicados en cada script individual.
// Para evitar duplicación y facilitar la orquestación (apply.mjs) se centraliza
// la lista de adapters y una función de detección que devuelve el nombre del
// ATS a usar o null si no se reconoce.

import lever from "../ats/lever.mjs";
import ashby from "../ats/ashby.mjs";
import eightfold from "../ats/eightfold.mjs";

export const ADAPTERS = { lever, ashby, eightfold };

/**
 * Detecta automáticamente cuál adaptador corresponde a una URL dada.
 *
 * @param {string} url URL a inspeccionar.
 * @returns {'lever'|'ashby'|'eightfold'|null}
 */
export function detectAdapter(url) {
  if (lever.matches(url)) return "lever";
  if (ashby.matches(url)) return "ashby";
  if (eightfold.matches(url)) return "eightfold";
  return null;
}

