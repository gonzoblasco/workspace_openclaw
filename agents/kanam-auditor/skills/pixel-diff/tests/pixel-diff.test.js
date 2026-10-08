'use strict';

const fs = require('fs');
const path = require('path');
const http = require('http');
const { PNG } = require('pngjs');

const { PixelDiff } = require('../src/pixel-diff');
const color = require('../src/utils/color');
const image = require('../src/utils/image');
const tokens = require('../src/utils/tokens');
const { compareSpecs, toPx } = require('../src/comparator');
const { extractReality, findPrimaryNode, findCardNode } = require('../src/reality');

const FIXTURES = path.join(__dirname, 'fixtures');
const PAGE = path.join(FIXTURES, 'page.html');
const TOKENS_JSON = path.join(FIXTURES, 'kanam.tokens.json');
const TOKENS_CSS = path.join(FIXTURES, 'tokens.css');

const RUN_BROWSER = process.env.PIXELDIFF_NO_BROWSER !== '1';
const maybe = RUN_BROWSER ? test : test.skip;

let tempDir;
let server;
let baseUrl;

function startServer() {
  return new Promise((resolve) => {
    server = http.createServer((req, res) => {
      const file = req.url === '/card' || req.url === '/' ? PAGE : PAGE;
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(fs.readFileSync(file));
    });
    server.listen(0, '127.0.0.1', () => {
      baseUrl = `http://127.0.0.1:${server.address().port}`;
      resolve();
    });
  });
}

beforeAll(async () => {
  tempDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'pixel-diff-'));
  if (RUN_BROWSER) await startServer();
});

afterAll(async () => {
  if (server) await new Promise((r) => server.close(r));
  if (tempDir) fs.rmSync(tempDir, { recursive: true, force: true });
});

// ────────────────────────────── color utils ──────────────────────────────

describe('color utils', () => {
  test('parseColor soporta hex, rgb(), rgba() y nombres', () => {
    expect(color.parseColor('#fff')).toEqual({ r: 255, g: 255, b: 255, a: 1 });
    expect(color.parseColor('#0d9488')).toEqual({ r: 13, g: 148, b: 136, a: 1 });
    expect(color.parseColor('rgb(10, 20, 30)')).toEqual({ r: 10, g: 20, b: 30, a: 1 });
    expect(color.parseColor('rgba(10,20,30,0.5)').a).toBeCloseTo(0.5);
    expect(color.parseColor('white')).toEqual({ r: 255, g: 255, b: 255, a: 1 });
    expect(color.parseColor('bogus')).toBeNull();
  });

  test('Delta E es real: idénticos = 0, negro/blanco ≈ 100', () => {
    const same = color.deltaE2000('#0d9488', '#0d9488');
    expect(same.deltaE).toBe(0);

    const bw = color.deltaE2000('#000000', '#ffffff');
    expect(bw.deltaE).toBeGreaterThan(99);
    expect(bw.deltaE).toBeLessThan(101);
  });

  test('Delta E distingue diferencias perceptuales sutiles', () => {
    // teal-600 (#0d9488) vs un teal levemente distinto
    const near = color.deltaE2000('#0d9488', '#0d9c8c');
    expect(near.deltaE).toBeGreaterThan(0);
    expect(near.deltaE).toBeLessThan(5);

    const far = color.deltaE2000('#0d9488', '#2563eb'); // teal vs azul
    expect(far.deltaE).toBeGreaterThan(10);
  });

  test('averageRegionColor promedia y detecta dominante', () => {
    const png = image.createPng(10, 10, [255, 255, 255, 255]);
    image.fillRect(png, 0, 0, 5, 10, [0, 0, 0, 255]);
    const res = color.averageRegionColor(png, 0, 0, 10, 10);
    expect(res.samples).toBe(100);
    expect(res.average).toBe('#808080');
  });
});

// ────────────────────────────── image utils ──────────────────────────────

describe('image utils', () => {
  test('diffImages detecta cambio real de píxeles', () => {
    const a = image.createPng(40, 40, [255, 0, 0, 255]);
    const b = image.createPng(40, 40, [255, 0, 0, 255]);
    image.fillRect(b, 10, 10, 30, 30, [0, 0, 255, 255]);
    const diff = image.diffImages(a, b, { threshold: 0.1 });
    expect(diff.diffPixels).toBeGreaterThan(0);
    expect(diff.ratio).toBeGreaterThan(0.1);
    expect(diff.regions.length).toBeGreaterThan(0);
  });

  test('diffImages devuelve 0 para imágenes idénticas', () => {
    const a = image.createPng(20, 20, [10, 20, 30, 255]);
    const b = image.createPng(20, 20, [10, 20, 30, 255]);
    const diff = image.diffImages(a, b, { threshold: 0.1 });
    expect(diff.diffPixels).toBe(0);
    expect(diff.ratio).toBe(0);
  });

  test('resize normaliza dimensiones', () => {
    const a = image.createPng(100, 50, [0, 0, 0, 255]);
    const r = image.resize(a, 50, 25);
    expect(r.width).toBe(50);
    expect(r.height).toBe(25);
  });
});

// ────────────────────────────── tokens ──────────────────────────────

describe('tokens', () => {
  test('flatten + resolve referencias DTCG', () => {
    const json = JSON.parse(fs.readFileSync(TOKENS_JSON, 'utf8'));
    const flat = tokens.resolveReferences(tokens.flattenTokens(json));
    expect(flat['primitive.color.teal.600']).toBe('#0d9488');
    expect(flat['semantic.brand.primary']).toBe('#0d9488');
    expect(flat['semantic.text.primary']).toBe('#111318');
  });

  test('loadTokenSource desde CSS resuelve variables', () => {
    const map = tokens.loadTokenSource(TOKENS_CSS);
    expect(map['--k-brand-primary']).toBe('#0d9488');
    expect(map['--k-radius-lg']).toBe('16px');
  });

  test('buildTokensSpec produce spec comparable', () => {
    const spec = tokens.buildTokensSpec(tokens.loadTokenSource(TOKENS_JSON));
    expect(spec.colors.primary).toBe('#0d9488');
    expect(spec.radius.button).toBe('12px');
    expect(spec.spacing.padding_internal).toBe('16px');
    expect(spec.typography.font_family).toBe('Inter');
  });
});

// ────────────────────────────── comparator ──────────────────────────────

describe('comparator', () => {
  test('toPx convierte unidades', () => {
    expect(toPx('16px')).toBe(16);
    expect(toPx('1.5rem')).toBe(24);
    expect(toPx('8')).toBe(8);
    expect(toPx('var(--x)')).toBeNull();
  });

  test('detecta desalineación de color y radio con magnitud real', () => {
    const spec = {
      spacing: { padding_internal: '16px', margin_between: '32px' },
      radius: { card: '16px', button: '999px' },
      colors: { primary: '#2563eb', background: '#ffffff', text: '#111318' },
      typography: { title_size: '22px', font_family: 'Inter' }
    };
    const reality = {
      spacing: { padding_internal: '16px', margin_between: '24px' },
      radius: { card: '16px', button: '4px' },
      colors: { primary: '#0d9488', background: '#ffffff', text: '#111318' },
      typography: { title_size: '22px', font_family: 'Inter' }
    };
    const res = compareSpecs(spec, reality, { spacing_tolerance: 1, radius_tolerance: 0.5, color_delta_e: 2.3, typography_scale: 0.1 });
    expect(res.totalChecks).toBe(9);
    expect(res.critical.length).toBeGreaterThanOrEqual(2); // radius button + color
    expect(res.warnings.some((w) => w.property === 'margin_between')).toBe(true);
    const radiusCrit = res.critical.find((c) => c.property === 'radius_button');
    expect(radiusCrit.difference).toBe(995);
  });

  test('reporta no medible en vez de inventar valor', () => {
    const spec = { spacing: { padding_internal: 'var(--k-space-4)' }, radius: {}, colors: {}, typography: {} };
    const reality = { spacing: { padding_internal: '16px' }, radius: {}, colors: {}, typography: {} };
    const res = compareSpecs(spec, reality, {}, {});
    expect(res.skipped.length).toBe(1);
    expect(res.aligned.length).toBe(0);
  });
});

// ────────────────────────────── reality extractor ──────────────────────────────

describe('reality extractor', () => {
  test('selecciona primary y card desde geometría y muestrea color del PNG', () => {
    const geometry = {
      root: { rect: { x: 0, y: 0, width: 400, height: 300 }, styles: { backgroundColor: 'rgb(250, 249, 245)' } },
      nodes: [
        {
          tag: 'article', classes: 'card', text: 'Tarjeta',
          rect: { x: 40, y: 24, width: 320, height: 180 },
          styles: { backgroundColor: 'rgb(255,255,255)', borderRadius: '16px', paddingTop: '16px', color: 'rgb(17,19,24)', fontSize: '15px', fontFamily: 'Inter, sans-serif', marginBottom: '0px' }
        },
        {
          tag: 'button', classes: '', text: 'Acción',
          rect: { x: 56, y: 160, width: 120, height: 40 },
          styles: { backgroundColor: 'rgb(13,148,136)', borderRadius: '12px', paddingTop: '10px', color: 'rgb(255,255,255)', fontSize: '15px', fontFamily: 'Inter, sans-serif', marginBottom: '0px' }
        },
        {
          tag: 'h1', classes: '', text: 'Tarjeta Kanam',
          rect: { x: 56, y: 40, width: 200, height: 30 },
          styles: { backgroundColor: 'rgba(0,0,0,0)', borderRadius: '0px', paddingTop: '0px', color: 'rgb(17,19,24)', fontSize: '22px', fontFamily: 'Inter, sans-serif', marginBottom: '8px' }
        }
      ]
    };
    const png = image.createPng(400, 300, [255, 255, 255, 255]);
    image.fillRect(png, 40, 24, 360, 204, [255, 255, 255, 255]);
    image.fillRect(png, 56, 160, 176, 200, [13, 148, 136, 255]);
    const buf = PNG.sync.write(png);

    const reality = extractReality(geometry, buf);
    expect(reality.colors.primary.toLowerCase()).toBe('#0d9488');
    expect(reality.radius.button).toBe('12px');
    expect(reality.radius.card).toBe('16px');
    expect(reality.spacing.padding_internal).toBe('16px');
    expect(reality.typography.title_size).toBe('22px');
  });
});

// ────────────────────────────── PixelDiff integration ──────────────────────────────

describe('PixelDiff', () => {
  test('carga config y default threshold', () => {
    const cfgDir = path.join(tempDir, '.kanam');
    fs.mkdirSync(cfgDir, { recursive: true });
    const cfgPath = path.join(cfgDir, 'pixel-diff.config.yaml');
    fs.writeFileSync(cfgPath, 'project:\n  name: "test-project"\nthresholds:\n  color_delta_e: 2.3\n');

    const pd = new PixelDiff({ configPath: cfgPath, mode: 'comp' });
    expect(pd.config.project.name).toBe('test-project');
    expect(pd.config.thresholds.color_delta_e).toBe(2.3);
  });

  test('colorDeltaE (CIE76) y colorDeltaE2000 (perceptual)', () => {
    const pd = new PixelDiff({ configPath: path.join(tempDir, 'nope.yaml') });
    expect(pd.colorDeltaE('#000000', '#ffffff').deltaE).toBeGreaterThan(99);
    expect(pd.colorDeltaE2000('#000000', '#ffffff').deltaE).toBeGreaterThan(99);
  });

  maybe('modo tokens: valida el render real contra el DS', async () => {
    const pd = new PixelDiff({
      configPath: path.join(tempDir, 'nope.yaml'),
      mode: 'tokens',
      format: 'json',
      outputDir: path.join(tempDir, 'reports')
    });
    const res = await pd.run({ tokenSource: TOKENS_JSON, url: baseUrl, route: '/' });
    expect(res.stats.totalChecks).toBeGreaterThan(0);
    // La fixture está alineada con los tokens -> sin críticos
    expect(res.stats.critical).toBe(0);
    expect(res.stats.alignment).toBeGreaterThanOrEqual(80);
  });

  maybe('modo comp: detecta desalineación real contra spec declarada', async () => {
    const specsPath = path.join(tempDir, '.kanam', 'pixel-diff.specs.yaml');
    fs.mkdirSync(path.dirname(specsPath), { recursive: true });
    fs.writeFileSync(specsPath, [
      'specs:',
      '  "page.png":',
      '    name: page',
      '    spacing: { padding_internal: "16px", margin_between: "32px" }',
      '    radius: { card: "16px", button: "999px" }',
      '    colors: { primary: "#2563eb", background: "#ffffff", text: "#111318" }',
      '    typography: { title_size: "22px", font_family: "Inter" }',
      ''
    ].join('\n'));

    const pd = new PixelDiff({
      configPath: path.join(tempDir, 'nope.yaml'),
      mode: 'comp',
      format: 'console',
      outputDir: path.join(tempDir, 'reports'),
      specPath: specsPath
    });

    const res = await pd.run({ designPath: 'page.png', url: baseUrl, route: '/' });
    expect(res.stats.critical).toBeGreaterThan(0); // button pill + color
    expect(res.shouldBlock).toBe(true);
    expect(res.report).toContain('CRÍTICO');
  });

  maybe('modo comp sin spec -> error NO_SPEC', async () => {
    const pd = new PixelDiff({
      configPath: path.join(tempDir, 'nope.yaml'),
      mode: 'comp',
      specPath: path.join(tempDir, 'missing-specs.yaml')
    });
    await expect(pd.run({ designPath: 'x.png', url: baseUrl, route: '/' }))
      .rejects.toThrow(/No hay spec/);
  });

  test('modo baseline: regresión visual real', () => {
    const base = path.join(tempDir, 'baseline');
    const curr = path.join(tempDir, 'current');
    fs.mkdirSync(base, { recursive: true });
    fs.mkdirSync(curr, { recursive: true });

    const same = image.createPng(30, 30, [200, 200, 200, 255]);
    fs.writeFileSync(path.join(base, 'home.png'), PNG.sync.write(same));
    fs.writeFileSync(path.join(curr, 'home.png'), PNG.sync.write(same));

    const changed = image.createPng(30, 30, [200, 200, 200, 255]);
    image.fillRect(changed, 5, 5, 25, 25, [0, 0, 0, 255]);
    fs.writeFileSync(path.join(base, 'card.png'), PNG.sync.write(same));
    fs.writeFileSync(path.join(curr, 'card.png'), PNG.sync.write(changed));

    const pd = new PixelDiff({ configPath: path.join(tempDir, 'nope.yaml'), mode: 'baseline' });
    const res = pd.run({ baselineDir: base, currentDir: curr });
    return res.then((r) => {
      expect(r.stats.totalChecks).toBe(2);
      expect(r.stats.misaligned).toBe(1);
      expect(r.misaligned).toBe(1);
      expect(r.report).toContain('card.png');
    });
  });
});
