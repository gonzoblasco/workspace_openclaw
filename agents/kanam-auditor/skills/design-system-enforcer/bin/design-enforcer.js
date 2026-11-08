#!/usr/bin/env node
const { program } = require('commander');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { DesignSystemEnforcer } = require('../src/enforcer');

const SUPPORTED_EXT = ['.jsx', '.tsx', '.css', '.scss', '.js'];

// Mapeo 1:1 verificado. Solo esto hace que --fix sea deterministico.
// El resto (sin mapeo) queda como warning para decision humana.
const TOKEN_MAP = {
  '#f3f4f6': 'var(--k-bg-main)',
  '#ffffff': 'var(--k-bg-surface)',
  '#1f2937': 'var(--k-text-main)',
  '#6b7280': 'var(--k-text-muted)',
  '#3b82f6': 'var(--k-interactive-primary)',
  '#10b981': 'var(--k-success)',
  '#f59e0b': 'var(--k-warning)',
  '#dc2626': 'var(--k-danger)',
};

function normalizeHex(hex) {
  let h = hex.replace('#', '').toLowerCase();
  if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
  return '#' + h;
}

function fixFile(filePath, apply) {
  const original = fs.readFileSync(filePath, 'utf8');
  const edits = []; // { line, old, token }
  const lines = original.split('\n');
  const replacedLines = lines.map((line, i) => {
    return line.replace(/#(?:[a-f0-9]{6}|[a-f0-9]{3})\b/gi, (hex, offset) => {
      const clean = normalizeHex(hex);
      const token = TOKEN_MAP[clean];
      if (!token) return hex;
      edits.push({ line: i + 1, old: hex, token });
      return token;
    });
  });
  const output = replacedLines.join('\n');
  const changed = output !== original;
  if (changed && apply) fs.writeFileSync(filePath, output, 'utf8');
  return { changed, edits };
}

program
  .name('design-enforcer')
  .description('Guardian preventivo del Design System')
  .version('1.0.0')
  .argument('[path]', 'Ruta a analizar', './src')
  .option('-c, --config <path>', 'Ruta al archivo de configuracion', '.kanam/enforcer.config.yaml')
  .option('-f, --format <type>', 'Formato de salida', 'console')
  .option('--fix', 'Intenta auto-corregir valores hardcodeados con mapeo 1:1 (dry-run por defecto)', false)
  .option('--apply', 'Aplica los cambios sugeridos por --fix (sin esto, solo muestra diff)', false)
  .option('--staged', 'Analiza solo archivos staged en git (fast lane de pre-commit)', false)
  .option('--watch', 'Re-audita cuando un archivo se guarda', false)
  .option('--debounce <ms>', 'Debounce ms', (v) => Number(v), 300)
  .parse();

const options = program.opts();

function resolveTargets(staged) {
  if (!staged) return [path.resolve(process.cwd(), program.args[0] || './src')];
  try {
    const raw = execFileSync('git', ['diff', '--cached', '--name-only', '--diff-filter=ACM'], {
      encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']
    }).trim();
    return raw.split('\n').filter(Boolean)
      .map((p) => path.resolve(process.cwd(), p))
      .filter((p) => SUPPORTED_EXT.includes(path.extname(p)));
  } catch (err) {
    console.error('Error consultando git (staged):', err.message);
    process.exit(1);
  }
}

async function main() {
  const enforcer = new DesignSystemEnforcer({
    configPath: path.resolve(process.cwd(), options.config),
    format: options.format,
    autoFix: options.fix
  });

  // --fix: operacion deterministica en 1:1. Dry-run por defecto.
  if (options.fix) {
    const wantApply = !!options.apply;
    const targets = options.staged
      ? (function () {
          const raw = execFileSync('git', ['diff', '--cached', '--name-only', '--diff-filter=ACM'], {
            encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']
          }).trim();
          return raw.split('\n').filter(Boolean)
            .map((p) => path.resolve(process.cwd(), p))
            .filter((p) => SUPPORTED_EXT.includes(path.extname(p)));
        })()
      : [path.resolve(process.cwd(), program.args[0] || './src')];

    // expandir directorios
    let files = [];
    const { findFiles } = enforcer;
    // patched: enforcer.findFiles es metodo, usarlo
    for (const t of targets) {
      const stat = fs.statSync(t);
      if (stat.isDirectory()) files.push(...enforcer.findFiles(t));
      else if (stat.isFile()) files.push(t);
    }

    console.log(`\n🔍 Design System Auto-fix (deterministico 1:1) — ${wantApply ? 'APLICAR' : 'DRY-RUN'}\n`);
    let changedCount = 0, editCount = 0, skipped = 0;
    for (const f of files) {
      const { changed, edits } = fixFile(f, wantApply);
      if (!changed) continue;
      changedCount++;
      editCount += edits.length;
      const rel = path.relative(process.cwd(), f);
      console.log(`  ${rel}`);
      for (const e of edits) console.log(`    ${e.line}: ${e.old}  ->  ${e.token}`);
    }
    console.log(`\nArchivos que se tocaron: ${changedCount} · Reemplazos: ${editCount} · Sin mapeo: ${files.length - changedCount}\n`);
    console.log(wantApply
      ? 'Cambios aplicados. Re-ejecuta `design-enforcer` para verificar.\n'
      : 'DRY-RUN: sin cambios en disco. Para aplicar: --fix --apply.\n');
    process.exit(0);
  }

  // Fast lane staged
  if (options.staged) {
    const targets = resolveTargets(true);
    if (targets.length === 0) {
      console.log('\n🔍 Design System Enforcement Report (fast lane)\n0 archivos staged. Nada que auditar.\n');
      process.exit(0);
    }
    const results = await enforcer.analyzeFiles(targets);
    console.log(results.report);
    process.exit(results.blocked ? 1 : 0);
  }

  // Watch
  if (options.watch) {
    const target = path.resolve(process.cwd(), program.args[0] || './src');
    async function audit() {
      const r = await enforcer.analyze(target);
      console.log(`\n[${new Date().toISOString()}] re-auditoria\n` + r.report);
      // runToken debug removed
    }
    await audit();
    try {
      const w = fs.watch(target, { recursive: true }, (_e, f) => {
        if (!f) return;
        const ext = path.extname(f).toLowerCase();
        if (!SUPPORTED_EXT.includes(ext)) return;
        if (path.basename(f).startsWith('.#')) return;
        clearTimeout(w._t);
        w._t = setTimeout(() => audit(), Math.max(16, options.debounce));
        if (w._t.unref) w._t.unref();
      });
      w.on('error', (err) => console.error('watch error:', err.message));
      if (w.unref) w.unref();
    } catch (err) {
      console.error('No se pudo activar watch:', err.message);
      process.exit(1);
    }
    process.on('SIGINT', () => { console.log('\nbye'); process.exit(0); });
    await new Promise(() => {});
  }

  const targetPath = program.args[0] || './src';
  const results = await enforcer.analyze(path.resolve(process.cwd(), targetPath));
  console.log(results.report);
  process.exit(results.blocked ? 1 : 0);
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
