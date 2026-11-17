'use strict';

/**
 * Puente entre la política ("¿a quién le toca?") y la medición ("¿cómo salió?").
 *
 * `scripts/check-audit-due.py` decide qué proyectos cruzaron un hito sin auditar.
 * `audit-surface` produce el veredicto. Hasta ahora nadie los conectaba: el
 * script existía desde el 2026-11-04 y no lo llamaba nadie (C.3 del ROADMAP).
 *
 * Este módulo no mide nada: compone el puente y renderiza el AUDIT.md que el
 * propio script sabe leer de vuelta.
 */

const FORMATO_VERSION = /\*\*(?:Version|Versi[oó]n) auditada:?\*\*:?\s*(\S+)/i;
const FORMATO_FECHA = /\*\*Fecha:?\*\*:?\s*(\d{4}-\d{2}-\d{2})/i;

/** Parsea la salida de `check-audit-due.py --json`. Nunca lanza por basura. */
function parseDueJson(stdout) {
  if (typeof stdout !== 'string' || !stdout.trim()) {
    return { projects: [], due: [], error: 'salida vacía de check-audit-due.py' };
  }
  try {
    const data = JSON.parse(stdout);
    return {
      projects: Array.isArray(data.projects) ? data.projects : [],
      due: Array.isArray(data.due) ? data.due : []
    };
  } catch (error) {
    return { projects: [], due: [], error: `JSON inválido: ${error.message}` };
  }
}

/**
 * Renderiza el AUDIT.md del proyecto.
 *
 * Los dos campos que `check-audit-due.py` vuelve a leer son **Version auditada**
 * y **Fecha**: si no están, el proyecto sigue "TOCA AUDITAR" para siempre y el
 * puente no cierra el ciclo.
 */
function renderAudit({
  slug,
  version,
  date,
  verdict,
  blocking = [],
  warnings = [],
  counts = {},
  reportPath,
  configPath
}) {
  const lines = [];
  lines.push(`# AUDIT — ${slug}`);
  lines.push('');
  lines.push(`**Version auditada:** ${version || '-'}`);
  lines.push(`**Fecha:** ${date}`);
  lines.push(`**Veredicto:** ${verdict}`);
  lines.push('');
  lines.push('## Resumen');
  lines.push('');
  lines.push('| Dato | Valor |');
  lines.push('|---|---|');
  lines.push(`| Bloqueos | ${blocking.length} |`);
  lines.push(`| Advertencias | ${warnings.length} |`);
  lines.push(`| Stages | ${counts.stages != null ? counts.stages : '-'} |`);
  lines.push(`| Hallazgos | ${counts.findings != null ? counts.findings : '-'} |`);
  lines.push('');

  if (reportPath) {
    lines.push(`**Reporte:** \`${reportPath}\``);
    lines.push('');
  }
  if (configPath) {
    lines.push(`**Config:** \`${configPath}\``);
    lines.push('');
  }

  if (blocking.length) {
    lines.push('## Bloqueos');
    lines.push('');
    for (const f of blocking) {
      const where = f.element ? ` (\`${f.element}\`)` : '';
      lines.push(`- **[${f.skill}]** ${f.message}${where}`);
    }
    lines.push('');
  }

  if (warnings.length) {
    lines.push('## Advertencias');
    lines.push('');
    for (const f of warnings) {
      const where = f.element ? ` (\`${f.element}\`)` : '';
      lines.push(`- **[${f.skill}]** ${f.message}${where}`);
    }
    lines.push('');
  }

  lines.push('---');
  lines.push('');
  lines.push('_Generado por `surface-pipeline/bin/audit-due` a partir del pipeline ejecutado._');
  lines.push('');

  return lines.join('\n');
}

/** Verifica el round-trip: el AUDIT.md renderizado se puede leer de vuelta. */
function readBack(markdown) {
  const head = String(markdown || '').split('\n').slice(0, 20).join('\n');
  const version = FORMATO_VERSION.exec(head);
  const date = FORMATO_FECHA.exec(head);
  return {
    version: version ? version[1] : null,
    date: date ? date[1] : null
  };
}

module.exports = { parseDueJson, renderAudit, readBack };
