const path = require('path');
const { chromium } = require('playwright-core');
const {
  parseColor,
  relativeLuminance,
  compositeOver,
  compositeStack,
  contrastRatio,
  requiredRatio,
  resolveContrast,
  measureContrast
} = require('../src/checks/contrast');

describe('contraste: matemática WCAG', () => {
  test('parsea rgb y rgba', () => {
    expect(parseColor('rgb(10, 20, 30)')).toEqual({ r: 10, g: 20, b: 30, a: 1 });
    expect(parseColor('rgba(10, 20, 30, 0.5)')).toEqual({ r: 10, g: 20, b: 30, a: 0.5 });
    expect(parseColor('rgba(10, 20, 30)')).toEqual({ r: 10, g: 20, b: 30, a: 1 });
    expect(parseColor('transparent')).toBeNull();
    expect(parseColor('var(--k-text-main)')).toBeNull();
  });

  test('luminancia relativa coincide con los anclajes de WCAG', () => {
    expect(relativeLuminance({ r: 255, g: 255, b: 255 })).toBeCloseTo(1, 5);
    expect(relativeLuminance({ r: 0, g: 0, b: 0 })).toBeCloseTo(0, 5);
    // Anclaje publicado: #808080 ≈ 0.2159
    expect(relativeLuminance({ r: 128, g: 128, b: 128 })).toBeCloseTo(0.2159, 3);
  });

  test('ratio extremo blanco/negro es 21:1', () => {
    const ratio = contrastRatio(
      { r: 255, g: 255, b: 255 },
      { r: 0, g: 0, b: 0 }
    );
    expect(ratio).toBeCloseTo(21, 1);
  });

  test('el ratio es simétrico y no depende del orden', () => {
    const a = { r: 13, g: 148, b: 136 };
    const b = { r: 255, g: 255, b: 255 };
    expect(contrastRatio(a, b)).toBeCloseTo(contrastRatio(b, a), 10);
  });

  test('umbral AA: 4.5 normal, 3 en texto grande', () => {
    expect(requiredRatio(16, 400)).toBe(4.5);
    expect(requiredRatio(23, 400)).toBe(4.5);
    expect(requiredRatio(24, 400)).toBe(3);
    expect(requiredRatio(18.66, 700)).toBe(3);
    expect(requiredRatio(18, 700)).toBe(4.5); // 18px bold NO es grande
    expect(requiredRatio(19, 700)).toBe(3);
  });

  test('compone fondos con alpha en el orden correcto', () => {
    // 50% negro sobre blanco = gris medio
    const over = compositeOver({ r: 0, g: 0, b: 0, a: 0.5 }, { r: 255, g: 255, b: 255, a: 1 });
    expect(Math.round(over.r)).toBe(128);
    expect(over.a).toBe(1);
  });

  test('compositeStack respeta el orden: [0] es el más interno', () => {
    const stack = [
      { r: 0, g: 0, b: 0, a: 0.5 },      // velo negro del elemento
      { r: 255, g: 255, b: 255, a: 1 }   // fondo blanco del contenedor
    ];
    const result = compositeStack(stack);
    expect(Math.round(result.r)).toBe(128);
  });

  test('resolveContrast detecta un par que falla y uno que pasa', () => {
    const bad = resolveContrast({
      color: 'rgb(153, 153, 153)',
      backgrounds: ['rgb(255, 255, 255)'],
      fontSizePx: 16,
      fontWeight: 400
    });
    expect(bad.ratio).toBeLessThan(4.5);
    expect(bad.required).toBe(4.5);

    const good = resolveContrast({
      color: 'rgb(0, 0, 0)',
      backgrounds: ['rgb(255, 255, 255)'],
      fontSizePx: 16,
      fontWeight: 400
    });
    expect(good.ratio).toBeCloseTo(21, 1);
    expect(good.ratio).toBeGreaterThan(good.required);
  });

  test('un fondo transparente hereda el del ancestro', () => {
    const result = resolveContrast({
      color: 'rgb(0, 0, 0)',
      backgrounds: ['rgba(0, 0, 0, 0)', 'rgb(255, 255, 255)'],
      fontSizePx: 16,
      fontWeight: 400
    });
    expect(result.ratio).toBeCloseTo(21, 1);
  });

  test('la opacidad del elemento reduce el contraste real', () => {
    const opaque = resolveContrast({
      color: 'rgb(0, 0, 0)',
      backgrounds: ['rgb(255, 255, 255)'],
      fontSizePx: 16,
      fontWeight: 400,
      opacity: 1
    });
    const faded = resolveContrast({
      color: 'rgb(0, 0, 0)',
      backgrounds: ['rgb(255, 255, 255)'],
      fontSizePx: 16,
      fontWeight: 400,
      opacity: 0.4
    });
    expect(faded.ratio).toBeLessThan(opaque.ratio);
    expect(faded.ratio).toBeLessThan(4.5);
  });
});

describe('contraste: medición en página real', () => {
  let browser;

  beforeAll(async () => {
    browser = await chromium.launch({ headless: true });
  }, 60000);

  afterAll(async () => {
    if (browser) await browser.close();
  });

  test('mide la página y separa fallos de aprobados', async () => {
    const page = await browser.newPage();
    await page.goto(
      'data:text/html;charset=utf-8,' +
      encodeURIComponent(`<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="background:#fff">
        <p id="bad" style="color:#999;background:#fff;font-size:16px">texto que falla</p>
        <p id="ok" style="color:#000;background:#fff;font-size:16px">texto que pasa</p>
        <h1 id="large" style="color:#767676;background:#fff;font-size:24px">titulo grande</h1>
      </body></html>`)
    );

    const result = await measureContrast(page, { states: false });

    expect(result.measurements.length).toBeGreaterThanOrEqual(3);

    const bad = result.violations.find(v => v.element.includes('#bad'));
    expect(bad).toBeTruthy();
    expect(bad.ratio).toBeLessThan(4.5);

    // #767676 sobre blanco ≈ 4.5: falla como texto normal, pasa como grande.
    const largeMeasurement = result.measurements.find(m => m.element.includes('#large'));
    expect(largeMeasurement.large).toBe(true);
    expect(largeMeasurement.required).toBe(3);
    const largeViolation = result.violations.find(v => v.element.includes('#large'));
    expect(largeViolation).toBeUndefined();

    expect(result.violations.find(v => v.element.includes('#ok'))).toBeUndefined();

    await page.close();
  }, 60000);

  test('no reporta nada cuando el contraste es correcto', async () => {
    const page = await browser.newPage();
    await page.goto(
      'data:text/html;charset=utf-8,' +
      encodeURIComponent(`<!DOCTYPE html><html><body style="background:#fff">
        <p style="color:#000;background:#fff;font-size:16px">todo bien</p>
      </body></html>`)
    );

    const result = await measureContrast(page, { states: false });
    expect(result.violations).toHaveLength(0);
    expect(result.measurements.length).toBeGreaterThanOrEqual(1);

    await page.close();
  }, 60000);
});
