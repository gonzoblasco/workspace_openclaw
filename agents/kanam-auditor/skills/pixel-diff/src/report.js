'use strict';

const fs = require('fs');
const path = require('path');

const SEPARATOR = '─'.repeat(60);

/** Reporte de consola legible, con magnitud real de cada desfase. */
function consoleReport(result, mode) {
  let out = `\n\n🔍 Pixel Diff Report\n\n`;
  out += `Modo: ${String(mode).toUpperCase()}\n`;
  out += `Alineamiento: ${result.alignment.toFixed(1)}%\n`;
  out += `Checks: ${result.totalChecks} (alineados ${result.alignedCount ?? (result.aligned ? result.aligned.length : 0)}, desalineados ${result.misaligned})\n`;
  if (result.specOrigin) out += `Spec: ${result.specOrigin}\n`;
  if (result.targetUrl) out += `Target: ${result.targetUrl}\n`;

  if (result.critical && result.critical.length) {
    out += `\n🚨 CRÍTICO (bloquean merge):\n`;
    for (const c of result.critical) {
      out += formatItem(c);
    }
  }
  if (result.warnings && result.warnings.length) {
    out += `\n⚠️  ADVERTENCIAS:\n`;
    for (const w of result.warnings) {
      out += formatItem(w);
    }
  }
  if (result.skipped && result.skipped.length) {
    out += `\n❔ NO MEDIBLE (revisar spec/token):\n`;
    for (const s of result.skipped) {
      out += `  - ${s.property}: ${s.note || 'sin valor comparable'}\n`;
    }
  }
  if (result.imageDiff) {
    out += `\n🖼️  PIXELMATCH (captura vs render):\n`;
    out += `  - Diferencia: ${result.imageDiff.diffPixels}px de ${result.imageDiff.totalPixels} (${(result.imageDiff.ratio * 100).toFixed(2)}%)\n`;
    if (result.imageDiff.regions && result.imageDiff.regions.length) {
      out += `  - Regiones: ${result.imageDiff.regions.map((r) => `${r.width}x${r.height}@(${r.x},${r.y})`).slice(0, 5).join(', ')}\n`;
    }
  }
  if (result.diffs && result.diffs.length && mode === 'baseline') {
    out += `\n🖼️  BASELINE:\n`;
    for (const d of result.diffs) {
      out += `  - ${d.name}: ${d.diffPixels}px (${(d.ratio * 100).toFixed(2)}%)\n`;
    }
  }
  if (result.aligned && result.aligned.length) {
    out += `\n✅ ALINEADOS:\n`;
    for (const a of result.aligned) {
      out += `  - ${labelOf(a)}: ${describeActual(a)}\n`;
    }
  }

  out += `\n${SEPARATOR}\n`;
  if (result.misaligned === 0) out += `\n🎉 Alineado: todos los checks dentro de tolerancia.\n`;
  else if (result.critical && result.critical.length) out += `\n❌ DESALINEADO: hay desfasajes críticos.\n`;
  else out += `\n⚠️ DESALINEADO: desfasajes menores, sujeto a corrección.\n`;
  return out;
}

function labelOf(item) {
  return item.property ? `${item.type}/${item.property}` : item.type;
}

function describeActual(item) {
  const expected = item.expected !== undefined ? item.expected : item.expectedPx;
  const actual = item.actual !== undefined ? item.actual : item.actualPx;
  return `${actual} (espec: ${expected})`;
}

function formatItem(item) {
  let out = '';
  if (item.property) {
    out += `  - ${labelOf(item)}: ${describeActual(item)}`;
    if (item.difference !== undefined) out += ` — desfase ${item.difference}${item.type === 'typography' ? '' : 'px'}`;
    if (item.deltaE !== undefined) out += ` — ΔE ${item.deltaE}`;
    out += `\n`;
    if (item.suggestion) out += `    💡 ${item.suggestion}\n`;
  } else {
    out += `  - ${item.message || JSON.stringify(item)}\n`;
  }
  out += `\n`;
  return out;
}

/** JSON estable para integraciones/CI. */
function jsonReport(result, mode) {
  return JSON.stringify(
    {
      mode,
      alignment: result.alignment,
      totalChecks: result.totalChecks,
      aligned: result.alignedCount ?? (Array.isArray(result.aligned) ? result.aligned.length : 0),
      misaligned: result.misaligned,
      critical: result.critical || [],
      warnings: result.warnings || [],
      skipped: result.skipped || [],
      specOrigin: result.specOrigin || null,
      targetUrl: result.targetUrl || null,
      imageDiff: result.imageDiff
        ? {
            diffPixels: result.imageDiff.diffPixels,
            totalPixels: result.imageDiff.totalPixels,
            ratio: result.imageDiff.ratio,
            regions: result.imageDiff.regions
          }
        : null,
      diffs: result.diffs
        ? result.diffs.map((d) => ({ name: d.name, diffPixels: d.diffPixels, ratio: d.ratio }))
        : null,
      misalignedList: [...(result.critical || []), ...(result.warnings || [])].map((i) => ({
        type: i.type, property: i.property, expected: i.expected, actual: i.actual,
        difference: i.difference, deltaE: i.deltaE, message: i.message, suggestion: i.suggestion
      }))
    },
    null,
    2
  );
}

/** HTML autocontenido con evidencia visual embebida (base64). */
function htmlReport(result, mode, artifacts = {}) {
  const imgTag = (file) => {
    if (!file || !fs.existsSync(file)) return '<p class="muted">sin imagen</p>';
    const b64 = fs.readFileSync(file).toString('base64');
    return `<img src="data:image/png;base64,${b64}" alt="evidencia" />`;
  };

  const status = result.critical && result.critical.length ? 'rejected'
    : result.misaligned ? 'warn' : 'ok';

  const rows = [...(result.critical || []), ...(result.warnings || [])].map((i) => `
    <tr>
      <td>${escapeHtml(i.type)}</td>
      <td>${escapeHtml(i.property || '—')}</td>
      <td>${escapeHtml(String(i.expected ?? '—'))}</td>
      <td>${escapeHtml(String(i.actual ?? i.message ?? '—'))}</td>
      <td>${i.difference !== undefined ? i.difference + 'px' : (i.deltaE !== undefined ? 'ΔE ' + i.deltaE : '—')}</td>
      <td>${escapeHtml(i.suggestion || '')}</td>
    </tr>`).join('');

  return `<!doctype html>
<html lang="es"><head><meta charset="utf-8" />
<title>Pixel Diff Report</title>
<style>
  :root { --ok:#0d9488; --warn:#b7791f; --bad:#b03a2e; }
  body { font-family: Inter, system-ui, sans-serif; margin: 0; background:#faf9f5; color:#111318; }
  header { padding: 16px 32px; /* <= ceiling */ background:#111318; color:#faf9f5; }
  header h1 { margin:0; font-size:20px; }
  .badge { display:inline-block; padding:4px 10px; border-radius:6px; font-weight:600; margin-top:8px; }
  .badge.ok{ background:var(--ok); } .badge.warn{ background:var(--warn); } .badge.rejected{ background:var(--bad); }
  main { padding: 16px 32px; /* <= ceiling */ }
  table { border-collapse: collapse; width:100%; background:#fff; border:1px solid #e2dfd6; }
  th,td { padding:8px 10px; border-bottom:1px solid #efede6; text-align:left; font-size:13px; }
  th { background:#f4f4f2; }
  .evidence { display:flex; gap:16px; flex-wrap:wrap; margin-top:24px; }
  .evidence figure { margin:0; background:#fff; border:1px solid #e2dfd6; padding:8px; max-width:48%; }
  .evidence img { max-width:100%; display:block; }
  .muted { color:#78716c; font-size:12px; }
</style></head>
<body>
<header>
  <h1>🔍 Pixel Diff Report — Modo ${escapeHtml(String(mode).toUpperCase())}</h1>
  <div class="badge ${status}">${status === 'ok' ? 'ALINEADO' : status === 'warn' ? 'DESALINEADO (menor)' : 'RECHAZADO'}</div>
  <p class="muted">Alineamiento: ${result.alignment.toFixed(1)}% · Checks: ${result.totalChecks} · Desalineados: ${result.misaligned}</p>
  ${result.specOrigin ? `<p class="muted">Spec: ${escapeHtml(result.specOrigin)}</p>` : ''}
  ${result.targetUrl ? `<p class="muted">Target: ${escapeHtml(result.targetUrl)}</p>` : ''}
</header>
<main>
  <table>
    <thead><tr><th>Tipo</th><th>Propiedad</th><th>Spec</th><th>Real</th><th>Magnitud</th><th>Sugerencia</th></tr></thead>
    <tbody>${rows || '<tr><td colspan="6" class="muted">Sin desalineaciones.</td></tr>'}</tbody>
  </table>
  <div class="evidence">
    ${artifacts.design ? `<figure>${imgTag(artifacts.design)}<figcaption class="muted">Spec: ${escapeHtml(path.basename(artifacts.design))}</figcaption></figure>` : ''}
    ${artifacts.render ? `<figure>${imgTag(artifacts.render)}<figcaption class="muted">Render real</figcaption></figure>` : ''}
    ${artifacts.diff ? `<figure>${imgTag(artifacts.diff)}<figcaption class="muted">Diff (pixelmatch)</figcaption></figure>` : ''}
  </div>
</main>
</body></html>`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function writeReport(content, outputDir, basename) {
  fs.mkdirSync(outputDir, { recursive: true });
  const file = path.join(outputDir, basename);
  fs.writeFileSync(file, content, 'utf8');
  return file;
}

module.exports = { consoleReport, jsonReport, htmlReport, writeReport };
