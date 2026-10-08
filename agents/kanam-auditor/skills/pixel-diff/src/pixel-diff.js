'use strict';

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const { runComp } = require('./adapters/comp');
const { runBaseline } = require('./adapters/baseline');
const { runTokens } = require('./adapters/tokens');
const { consoleReport, jsonReport, htmlReport, writeReport } = require('./report');
const { deltaE2000, deltaE76 } = require('./utils/color');
const { compareSpecs } = require('./comparator');
const specUtil = require('./utils/specs');

const DEFAULT_CONFIG = {
  project: { name: 'unknown' },
  sources: [],
  checks: {
    spacing_alignment: true,
    radius_consistency: true,
    color_accuracy: true,
    typography_scale: true
  },
  thresholds: {
    spacing_tolerance: 1,
    radius_tolerance: 0.5,
    color_delta_e: 2.3,
    typography_scale: 0.1
  }
};

class PixelDiff {
  constructor(options = {}) {
    this.configPath = options.configPath;
    this.mode = options.mode || 'comp';
    this.format = options.format || 'console';
    this.outputDir = options.outputDir || './reports';
    this.threshold = options.threshold !== undefined ? options.threshold : 1;
    this.specPath = options.specPath || specUtil.DEFAULT_SPEC_FILE;
    this.config = this.loadConfig();
  }

  loadConfig() {
    const defaultConfigPath = path.resolve(process.cwd(), '.kanam/pixel-diff.config.yaml');
    const target = this.configPath || defaultConfigPath;

    if (!fs.existsSync(target)) {
      console.warn('⚠️ No config found, using defaults');
      return DEFAULT_CONFIG;
    }

    try {
      const loaded = yaml.load(fs.readFileSync(target, 'utf8')) || {};
      return {
        ...DEFAULT_CONFIG,
        ...loaded,
        checks: { ...DEFAULT_CONFIG.checks, ...(loaded.checks || {}) },
        thresholds: { ...DEFAULT_CONFIG.thresholds, ...(loaded.thresholds || {}) }
      };
    } catch (e) {
      console.error('Error loading config:', e.message);
      return DEFAULT_CONFIG;
    }
  }

  /** Resuelve el tokenSource a usar: flag explícito > config sources[type=design-system]. */
  resolveTokenSource(explicit) {
    if (explicit) return explicit;
    const src = (this.config.sources || []).find((s) => s.type === 'design-system');
    if (src && src.path) return path.resolve(process.cwd(), src.path);
    // Fallback al DS del workspace Kanam si existe
    const candidate = path.resolve(process.cwd(), 'design/tokens');
    return fs.existsSync(candidate) ? candidate : null;
  }

  async run(params = {}) {
    const { designPath, baselineDir, currentDir, url, route, selector, tokenSource, interactive } = params;

    const config = {
      checks: this.config.checks,
      thresholds: { ...this.config.thresholds, spacing_tolerance: this.threshold },
      viewport: this.config.viewport,
      deviceScaleFactor: this.config.deviceScaleFactor,
      fullPage: this.config.fullPage,
      headless: this.config.headless,
      waitUntil: this.config.waitUntil,
      imageDiff: this.config.imageDiff,
      imageThreshold: this.config.imageThreshold,
      includeAA: this.config.includeAA
    };

    let result;

    switch (this.mode) {
      case 'comp':
        if (interactive) await this.maybeCollectInteractive(designPath);
        result = await runComp({
          designPath, url, route, selector,
          config, specPath: this.specPath,
          tokenSource: this.resolveTokenSource(tokenSource)
        });
        break;
      case 'baseline':
        result = runBaseline({
          baselineDir, currentDir,
          threshold: config.imageThreshold ?? 0.1,
          tolerance: this.config.baseline_tolerance ?? 0
        });
        break;
      case 'tokens':
        result = await runTokens({
          tokenSource: this.resolveTokenSource(tokenSource),
          url, route, selector, config
        });
        break;
      default:
        throw new Error(`Modo desconocido: ${this.mode}`);
    }

    const artifacts = await this.persistArtifacts(result);
    const report = this.generateReport(result, artifacts);

    return {
      report,
      misaligned: result.misaligned,
      shouldBlock: (result.critical || []).length > 0,
      mode: this.mode,
      artifacts,
      stats: {
        alignment: result.alignment,
        totalChecks: result.totalChecks,
        aligned: result.alignedCount ?? (result.aligned ? result.aligned.length : 0),
        misaligned: result.misaligned,
        critical: (result.critical || []).length
      }
    };
  }

  async maybeCollectInteractive(designPath) {
    if (!process.stdin.isTTY) {
      throw new Error('Modo --interactive requiere una terminal interactiva.');
    }
    const specs = specUtil.loadSpecs(this.specPath);
    const collected = await specUtil.collectInteractive(designPath);
    specs.specs = specs.specs || {};
    specs.specs[designPath || collected.name] = collected;
    const saved = specUtil.saveSpecs(specs, this.specPath);
    console.log(`✍️  Spec guardada en ${saved}`);
  }

  /** Guarda captura de render, diff y reportes según formato. */
  async persistArtifacts(result) {
    const artifacts = {};
    const stamp = new Date().toISOString().replace(/[:.]/g, '-');
    const dir = path.join(this.outputDir, stamp);

    try {
      if (result.capture && result.capture.buffer) {
        fs.mkdirSync(dir, { recursive: true });
        const renderPath = path.join(dir, 'render.png');
        fs.writeFileSync(renderPath, result.capture.buffer);
        artifacts.render = renderPath;
      }
      if (result.imageDiff && result.imageDiff.diff) {
        fs.mkdirSync(dir, { recursive: true });
        const diffPath = path.join(dir, 'diff.png');
        fs.writeFileSync(diffPath, require('pngjs').PNG.sync.write(result.imageDiff.diff));
        artifacts.diff = diffPath;
      }
      if (result.diffs) {
        fs.mkdirSync(dir, { recursive: true });
        for (const d of result.diffs) {
          const p = path.join(dir, `diff-${d.name}`);
          fs.writeFileSync(p, require('pngjs').PNG.sync.write(d.diff.diff));
          artifacts[`diff-${d.name}`] = p;
        }
      }
      if (this.format === 'json') {
        artifacts.report = writeReport(jsonReport(result, this.mode), dir, 'report.json');
      } else if (this.format === 'html') {
        artifacts.report = writeReport(
          htmlReport(result, this.mode, { design: result.designPath || null, render: artifacts.render, diff: artifacts.diff }),
          dir, 'report.html'
        );
      }
    } catch (e) {
      console.warn(`⚠️ No se pudieron persistir artefactos: ${e.message}`);
    }

    return artifacts;
  }

  generateReport(result, artifacts) {
    if (this.format === 'json') return jsonReport(result, this.mode);
    if (this.format === 'html') {
      const summary = consoleReport(result, this.mode);
      return artifacts && artifacts.report
        ? `${summary}\n📄 Reporte HTML: ${artifacts.report}\n`
        : summary;
    }
    let out = consoleReport(result, this.mode);
    if (artifacts && artifacts.report) out += `\n📄 Reporte: ${artifacts.report}\n`;
    return out;
  }

  /** Compatibilidad: Delta E (CIE76) sobre hex. */
  colorDeltaE(color1, color2) {
    return deltaE76(color1, color2);
  }

  /** Delta E perceptual (CIEDE2000) — el que usa el comparador. */
  colorDeltaE2000(color1, color2) {
    return deltaE2000(color1, color2);
  }

  compareSpecs(spec, reality) {
    return compareSpecs(spec, reality, this.config.thresholds, this.config.checks);
  }

  hexToRgb(hex) {
    const { parseColor } = require('./utils/color');
    return parseColor(hex);
  }
}

module.exports = { PixelDiff, DEFAULT_CONFIG };
