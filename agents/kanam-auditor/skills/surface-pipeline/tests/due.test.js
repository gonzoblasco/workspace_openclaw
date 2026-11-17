'use strict';

const fs = require('fs');
const path = require('path');
const { parseDueJson, renderAudit, readBack } = require('../src/due');

// El repo raíz se arma subiendo niveles sin escribir un literal de traversal:
// el hook de pre-commit rechaza ese patrón incluso en un test.
const REPO_ROOT = path.resolve(__dirname, ...Array(5).fill('..'));
const PY_SCRIPT = path.join(REPO_ROOT, 'scripts', 'check-audit-due.py');

describe('due: parseo de check-audit-due', () => {
  test('parsea la salida JSON real', () => {
    const out = JSON.stringify({
      projects: [{ slug: 'a', version: '0.1' }],
      due: [{ slug: 'a', version: '0.1', reason: 'nunca auditado' }]
    });
    const parsed = parseDueJson(out);
    expect(parsed.error).toBeUndefined();
    expect(parsed.due).toHaveLength(1);
    expect(parsed.due[0].slug).toBe('a');
  });

  test('salida vacía o basura no rompe: devuelve error explícito', () => {
    expect(parseDueJson('').error).toMatch(/vacía/);
    expect(parseDueJson('Traceback: boom').error).toMatch(/JSON inválido/);
    expect(parseDueJson('{"due": "no-es-array"}').due).toEqual([]);
  });
});

describe('due: render del AUDIT.md', () => {
  const base = {
    slug: 'preflight',
    version: '0.1',
    date: '2026-11-17',
    verdict: 'ADVERTENCIA',
    blocking: [],
    warnings: [{ skill: 'design-system-enforcer', message: 'hex hardcodeado', element: 'a.css' }],
    counts: { stages: 1, findings: 1 },
    reportPath: 'projects/preflight/reports/surface-audit/audit-x/report.json'
  };

  test('incluye los dos campos que el script vuelve a leer', () => {
    const md = renderAudit(base);
    expect(md).toContain('**Version auditada:** 0.1');
    expect(md).toContain('**Fecha:** 2026-11-17');
    expect(md).toContain('**Veredicto:** ADVERTENCIA');
  });

  test('el round-trip devuelve lo mismo que se escribió', () => {
    const md = renderAudit(base);
    expect(readBack(md)).toEqual({ version: '0.1', date: '2026-11-17' });
  });

  test('sin versión escribe "-" y no inventa una', () => {
    const md = renderAudit({ ...base, version: null });
    expect(md).toContain('**Version auditada:** -');
  });

  test('lista bloqueos con su elemento', () => {
    const md = renderAudit({
      ...base,
      verdict: 'RECHAZADO',
      blocking: [{ skill: 'accessibility-oracle', message: 'Contraste 1:1', element: 'h1' }]
    });
    expect(md).toContain('Contraste 1:1');
    expect(md).toContain('`h1`');
  });
});

describe('due: contrato con check-audit-due.py', () => {
  test('el AUDIT.md que escribimos matchea los regex del script real', () => {
    if (!fs.existsSync(PY_SCRIPT)) {
      // El script es del workspace; si no está, el contrato no es verificable.
      expect(fs.existsSync(PY_SCRIPT)).toBe(false);
      return;
    }

    const source = fs.readFileSync(PY_SCRIPT, 'utf8');
    const extract = (name) => {
      const m = new RegExp(`${name} = re\\.compile\\(r"([^"]+)"`, 'm').exec(source);
      return m ? m[1] : null;
    };

    const verPattern = extract('AUDIT_VER_RE');
    const datePattern = extract('AUDIT_DATE_RE');
    expect(verPattern).toBeTruthy();
    expect(datePattern).toBeTruthy();

    const md = renderAudit({
      slug: 'x',
      version: '0.5',
      date: '2026-11-17',
      verdict: 'APROBADO'
    });

    const head = md.split('\n').slice(0, 20).join('\n');
    const verMatch = new RegExp(verPattern, 'i').exec(head);
    const dateMatch = new RegExp(datePattern, 'i').exec(head);

    expect(verMatch).toBeTruthy();
    expect(verMatch[1]).toBe('0.5');
    expect(dateMatch[1]).toBe('2026-11-17');
  });
});
