'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

const { computeVerdict, matches } = require('../src/verdict');
const { loadConfig } = require('../src/config');
const { consoleReport, jsonReport, htmlReport, writeReport } = require('../src/report');

// ────────────────────────────────── verdict ──────────────────────────────────

describe('verdict gate', () => {
  const gate = { block_on: ['critical', 'accessibility-violation'], warn_on: ['warning', 'misaligned'] };

  test('matchea por severidad y por código', () => {
    expect(matches(gate.block_on, { severity: 'critical' })).toBe(true);
    expect(matches(gate.block_on, { severity: 'warning', code: 'accessibility-violation' })).toBe(true);
    expect(matches(gate.block_on, { severity: 'warning', code: 'other' })).toBe(false);
  });

  test('RECHAZADO cuando hay bloqueos', () => {
    const v = computeVerdict([
      { skill: 'a', findings: [{ severity: 'critical', message: 'boom' }] }
    ], gate);
    expect(v.verdict).toBe('RECHAZADO');
    expect(v.exitCode).toBe(1);
    expect(v.counts.blocking).toBe(1);
  });

  test('ADVERTENCIA cuando solo hay warnings', () => {
    const v = computeVerdict([
      { skill: 'a', findings: [{ severity: 'warning', code: 'misaligned', message: 'off by 2px' }] }
    ], gate);
    expect(v.verdict).toBe('ADVERTENCIA');
    expect(v.exitCode).toBe(0);
    expect(v.strictExitCode).toBe(1);
  });

  test('APROBADO sin hallazgos', () => {
    const v = computeVerdict([{ skill: 'a', findings: [] }], gate);
    expect(v.verdict).toBe('APROBADO');
    expect(v.exitCode).toBe(0);
    expect(v.counts.total).toBe(0);
  });

  test('block_on gana sobre warn_on', () => {
    const v = computeVerdict([
      { skill: 'a', findings: [{ severity: 'critical', code: 'misaligned' }] }
    ], gate);
    expect(v.verdict).toBe('RECHAZADO');
    expect(v.blocking).toHaveLength(1);
    expect(v.warnings).toHaveLength(0);
  });
});

// ────────────────────────────────── config ───────────────────────────────────

describe('config', () => {
  test('usa defaults cuando no hay archivo', () => {
    const cfg = loadConfig(path.join(os.tmpdir(), 'does-not-exist-pipeline.yaml'));
    expect(cfg.project.name).toBe('unknown');
    expect(cfg.stages.length).toBe(3);
    expect(cfg.gate.block_on).toContain('critical');
  });

  test('mergea config parcial', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'sp-cfg-'));
    const file = path.join(dir, 'pipeline.yaml');
    fs.writeFileSync(file, `project:\n  name: "x"\ngate:\n  block_on: ["critical"]\n`);
    const cfg = loadConfig(file);
    expect(cfg.project.name).toBe('x');
    expect(cfg.gate.warn_on).toContain('misaligned'); // default preservado
    fs.rmSync(dir, { recursive: true, force: true });
  });
});

// ────────────────────────────────── report ───────────────────────────────────

describe('report', () => {
  const model = {
    generatedAt: '2026-10-07T00:00:00.000Z',
    config: { project: { name: 'kanam-core' } },
    verdict: {
      verdict: 'RECHAZADO', exitCode: 1, strictExitCode: 1,
      counts: { blocking: 1, warnings: 0, infos: 0, total: 1 },
      blocking: [{ skill: 'accessibility-oracle', message: 'contrast fail', route: '/' }],
      warnings: []
    },
    results: [
      {
        skill: 'design-system-enforcer', status: 'pass', blocked: false,
        stats: { files: 3, violations: 0, warnings: 0 }, findings: []
      },
      {
        skill: 'accessibility-oracle', status: 'failed', blocked: true,
        stats: { routes: 1, violations: 1, warnings: 0 },
        findings: [{ skill: 'accessibility-oracle', severity: 'critical', code: 'accessibility-violation', route: '/', message: 'contrast fail' }]
      }
    ]
  };

  test('console incluye veredicto y stage numbering', () => {
    const out = consoleReport(model);
    expect(out).toContain('SURFACE AUDIT PIPELINE');
    expect(out).toContain('RECHAZADO');
    expect(out).toContain('[1/2] Design System Enforcer');
  });

  test('json es parseable y estable', () => {
    const parsed = JSON.parse(jsonReport(model));
    expect(parsed.verdict).toBe('RECHAZADO');
    expect(parsed.exitCode).toBe(1);
    expect(parsed.stages).toHaveLength(2);
  });

  test('html embebe veredicto y secciones', () => {
    const html = htmlReport(model);
    expect(html).toContain('<!doctype html>');
    expect(html).toContain('RECHAZADO');
    expect(html).toContain('Accessibility Oracle');
  });

  test('writeReport crea el archivo', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'sp-rep-'));
    const f = writeReport('hi', dir, 'r.txt');
    expect(fs.readFileSync(f, 'utf8')).toBe('hi');
    fs.rmSync(dir, { recursive: true, force: true });
  });
});

// ──────────────────────── guard de cobertura (stage vacío) ────────────────────

describe('guard stage-no-files', () => {
  const { runEnforcerStage } = require('../src/stages');

  test('un path inexistente NO aprueba: emite stage-no-files y bloquea', async () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'sp-empty-'));
    const stage = {
      skill: 'design-system-enforcer',
      path: path.join(dir, 'does-not-exist'),
      config: path.join(dir, 'cfg.yaml')
    };
    fs.writeFileSync(stage.config, 'project:\n  name: "x"\n');

    const r = await runEnforcerStage(stage, { cwd: dir, stampDir: dir, config: {} });

    const guard = r.findings.find((f) => f.code === 'stage-no-files');
    expect(guard).toBeDefined();
    expect(guard.severity).toBe('critical');
    expect(r.status).toBe('error');
    expect(r.blocked).toBe(true);
    fs.rmSync(dir, { recursive: true, force: true });
  });
});
