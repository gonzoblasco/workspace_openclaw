const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');
const AxeBuilder = require('@axe-core/playwright').default;

class AccessibilityOracle {
  constructor(options = {}) {
    this.configPath = options.configPath;
    this.baseUrl = options.baseUrl || 'http://localhost:3000';
    this.format = options.format || 'console';
    this.outputDir = options.outputDir || './reports';
    this.headless = options.headless !== false;
    this.screenshot = options.screenshot !== false;
    this.config = this.loadConfig();
  }

  loadConfig() {
    const defaultConfig = {
      project: { name: 'unknown', base_url: this.baseUrl },
      paths: [{ route: '/', critical: true }],
      rules: {
        contrast: 'wcag22-aa',
        keyboard_navigation: true,
        focus_visible: true,
        target_size: true,
        skip_rules: []
      },
      report: {
        format: ['html', 'json'],
        screenshot_on_violation: true,
        video_record: false
      }
    };

    const defaultConfigPath = path.resolve(process.cwd(), '.kanam/a11y-oracle.config.yaml');
    
    if (!fs.existsSync(this.configPath || defaultConfigPath)) {
      console.warn('⚠️ No config found, using defaults');
      return defaultConfig;
    }

    try {
      const content = fs.readFileSync(this.configPath || defaultConfigPath, 'utf8');
      const loaded = require('js-yaml').load(content);
      return { ...defaultConfig, ...loaded };
    } catch (e) {
      console.error('Error loading config:', e.message);
      return defaultConfig;
    }
  }

  /**
   * Run the accessibility audit.
   *
   * If a `route` is explicitly provided, only that route is audited.
   * If `route` is omitted or falsy, the method will iterate over all routes
   * defined in the configuration (`this.config.paths`).
   *
   * The method aggregates results across routes and writes report files
   * according to the `report.format` configuration (JSON, HTML). Files are
   * placed in `this.outputDir` (default `./reports`). The console output is
   * always printed (format `console`).
   */
  async run(route) {
    // Helper that performs a single‑route audit and returns the raw result
    const runSingle = async (singleRoute) => {
      const browser = await chromium.launch({ headless: this.headless });
      const context = await browser.newContext();
      const page = await context.newPage();

      const violations = [];
      const warnings = [];
      const passed = [];

      const targetUrl = `${this.config.project.base_url}${singleRoute}`;
      console.log(`🔍 Auditing: ${targetUrl}`);

      try {
        await page.goto(targetUrl, { waitUntil: 'networkidle' });

        // 1. axe-core scan
        const axeResults = await this.runAxeCheck(page);
        // 2. Keyboard navigation test
        const keyboardResults = await this.runKeyboardCheck(page);
        // 3. Focus visible test
        const focusResults = await this.runFocusVisibleCheck(page);
        // 4. Target size test
        const targetSizeResults = await this.runTargetSizeCheck(page);

        const allViolations = [
          ...axeResults.violations,
          ...keyboardResults.violations,
          ...focusResults.violations,
          ...targetSizeResults.violations
        ];
        const allWarnings = [
          ...axeResults.warnings,
          ...keyboardResults.warnings,
          ...focusResults.warnings,
          ...targetSizeResults.warnings
        ];

        if (allViolations.length === 0 && allWarnings.length === 0) {
          passed.push({
            route: singleRoute,
            message: 'All accessibility checks passed'
          });
        } else {
          violations.push(...allViolations);
          warnings.push(...allWarnings);
        }

        // Capture screenshots for any violations if configured
        if (this.screenshot && allViolations.length > 0) {
          await this.captureViolationScreenshots(page, allViolations, singleRoute);
        }
      } catch (error) {
        violations.push({
          route: singleRoute,
          rule: 'page-load',
          message: `Failed to load page: ${error.message}`,
          severity: 'critical'
        });
      } finally {
        await browser.close();
      }

      return {
        route: singleRoute,
        violations,
        warnings,
        passed,
        report: this.generateReport(violations, warnings, passed),
        failed: violations.length > 0
      };
    };

    // Determine the set of routes to process
    let routesToRun;
    if (route) {
      routesToRun = [{ route }];
    } else {
      // Use the array defined in configuration. Fallback to root if missing.
      routesToRun = (Array.isArray(this.config.paths) && this.config.paths.length > 0)
        ? this.config.paths.map(p => ({ route: p.route }))
        : [{ route: '/' }];
    }

    const perRouteResults = [];
    const aggregatedViolations = [];
    const aggregatedWarnings = [];
    const aggregatedPassed = [];

    for (const { route: r } of routesToRun) {
      const result = await runSingle(r);
      perRouteResults.push(result);
      aggregatedViolations.push(...result.violations);
      aggregatedWarnings.push(...result.warnings);
      aggregatedPassed.push(...result.passed);
    }

    // Build a combined report for all routes
    const combinedReport = this.generateReport(
      aggregatedViolations,
      aggregatedWarnings,
      aggregatedPassed
    );

    // Ensure the output directory exists
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }

    // Write report files according to configuration (HTML / JSON)
    const formats = Array.isArray(this.config.report.format)
      ? this.config.report.format
      : [];
    for (const fmt of formats) {
      if (fmt === 'json') {
        const jsonPath = path.join(this.outputDir, 'report.json');
        const jsonContent = JSON.stringify({
          perRoute: perRouteResults,
          aggregated: {
            violations: aggregatedViolations,
            warnings: aggregatedWarnings,
            passed: aggregatedPassed,
            stats: {
              routes: routesToRun.length,
              passed: aggregatedPassed.length,
              violations: aggregatedViolations.length,
              warnings: aggregatedWarnings.length
            }
          }
        }, null, 2);
        fs.writeFileSync(jsonPath, jsonContent, 'utf8');
      } else if (fmt === 'html') {
        const htmlPath = path.join(this.outputDir, 'report.html');
        const escaped = combinedReport
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;');
        const htmlContent = `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Accessibility Report</title></head><body><pre>${escaped}</pre></body></html>`;
        fs.writeFileSync(htmlPath, htmlContent, 'utf8');
      }
    }

    // Return the aggregated result (mirroring the original shape)
    return {
      report: combinedReport,
      failed: aggregatedViolations.length > 0,
      stats: {
        routes: routesToRun.length,
        passed: aggregatedPassed.length,
        violations: aggregatedViolations.length,
        warnings: aggregatedWarnings.length
      },
      perRoute: perRouteResults
    };
  }

  async runAxeCheck(page) {
    const violations = [];
    const warnings = [];

    try {
      const axe = new AxeBuilder({ page });
      
      // Configure WCAG 2.2 rules
      axe.withTags(['wcag22aa', 'wcag21aa', 'wcag2aa', 'best-practice']);
      
      const results = await axe.analyze();

      for (const violation of results.violations) {
        for (const node of violation.nodes) {
          violations.push({
            rule: violation.id,
            impact: violation.impact,
            message: violation.help,
            element: node.target.join(' '),
            html: node.html,
            failureSummary: node.failureSummary,
            url: violation.helpUrl
          });
        }
      }

      for (const incomplete of results.incomplete) {
        for (const node of incomplete.nodes) {
          warnings.push({
            rule: incomplete.id,
            message: incomplete.help,
            element: node.target.join(' '),
            html: node.html
          });
        }
      }

    } catch (error) {
      violations.push({
        rule: 'axe-error',
        message: `Axe-core failed: ${error.message}`,
        severity: 'critical'
      });
    }

    return { violations, warnings };
  }

  async runKeyboardCheck(page) {
    const violations = [];
    const warnings = [];

    try {
      // Test Tab navigation
      const focusableElements = await page.$$('button, a, input, select, textarea, [tabindex]');
      
      if (focusableElements.length === 0) {
        warnings.push({
          rule: 'keyboard',
          message: 'No focusable elements found on page'
        });
        return { violations, warnings };
      }

      // Test focus trapping (basic)
      const modals = await page.$$('.modal, [role="dialog"], [aria-modal="true"]');
      for (const modal of modals) {
        await modal.click();
        await page.waitForTimeout(500);
        
        // Check if focus is trapped
        const focusedElement = await page.evaluate(() => document.activeElement?.tagName);
        if (!['BUTTON', 'INPUT', 'A', 'SELECT', 'TEXTAREA'].includes(focusedElement)) {
          violations.push({
            rule: 'keyboard-trap',
            message: 'Focus escapes modal on Tab',
            element: 'modal'
          });
        }

        // Test Escape key
        await page.press('body', 'Escape');
        await page.waitForTimeout(500);
        
        const modalStillVisible = await modal.isVisible().catch(() => false);
        if (modalStillVisible) {
          warnings.push({
            rule: 'keyboard-escape',
            message: 'Modal does not close on Escape key',
            element: 'modal'
          });
        }
      }

    } catch (error) {
      warnings.push({
        rule: 'keyboard-error',
        message: `Keyboard check failed: ${error.message}`
      });
    }

    return { violations, warnings };
  }

  async runFocusVisibleCheck(page) {
    const violations = [];
    const warnings = [];

    try {
      // Check for outline: none or outline: 0
      const noOutline = await page.$$('style:not([data-a11y-ignore])');
      
      // Look for focus styles via computed styles
      const focusableElements = await page.$$('button, a, input, select, textarea, [tabindex]');
      
      for (const element of focusableElements.slice(0, 10)) { // Sample first 10
        await element.focus();
        await page.waitForTimeout(100);
        
        const focusInfo = await page.evaluate((el) => {
          const styles = window.getComputedStyle(el);
          const outlineWidth = parseInt(styles.outlineWidth);
          const outlineStyle = styles.outlineStyle;
          const outlineColor = styles.outlineColor;
          const boxShadow = styles.boxShadow;
          
          return {
            hasOutline: outlineWidth > 0 && outlineStyle !== 'none',
            hasBoxShadow: boxShadow !== 'none' && boxShadow.includes('rgb'),
            outlineOffset: styles.outlineOffset,
            outlineWidth: styles.outlineWidth,
            outlineColor: styles.outlineColor
          };
        }, element);

        if (!focusInfo.hasOutline && !focusInfo.hasBoxShadow) {
          violations.push({
            rule: 'focus-visible',
            message: 'Focus ring removed or not visible (outline: none without alternative)',
            element: await element.evaluate(el => el.tagName + (el.id ? '#' + el.id : '') + (el.className ? '.' + el.className.split(' ')[0] : ''))
          });
        }
      }

    } catch (error) {
      warnings.push({
        rule: 'focus-error',
        message: `Focus visible check failed: ${error.message}`
      });
    }

    return { violations, warnings };
  }

  async runTargetSizeCheck(page) {
    const violations = [];
    const warnings = [];

    try {
      // WCAG 2.2 AA: minimum 24x24px for interactive elements
      const interactiveElements = await page.$$('button, a, input[type="checkbox"], input[type="radio"], [role="button"], [role="link"]');
      
      for (const element of interactiveElements.slice(0, 20)) { // Sample first 20
        const box = await element.boundingBox();
        
        if (box) {
          const width = box.width;
          const height = box.height;
          
          if (width < 24 || height < 24) {
            warnings.push({
              rule: 'target-size',
              message: `Interactive element too small (${Math.round(width)}x${Math.round(height)}px, minimum 24x24px)`,
              element: await element.evaluate(el => el.tagName + (el.id ? '#' + el.id : '') + (el.className ? '.' + el.className.split(' ')[0] : '')),
              size: { width, height }
            });
          }
        }
      }

    } catch (error) {
      warnings.push({
        rule: 'target-size-error',
        message: `Target size check failed: ${error.message}`
      });
    }

    return { violations, warnings };
  }

  async captureViolationScreenshots(page, violations, route) {
    const violationsDir = path.join(this.outputDir, 'violations');
    if (!fs.existsSync(violationsDir)) {
      fs.mkdirSync(violationsDir, { recursive: true });
    }

    for (let i = 0; i < violations.length; i++) {
      const violation = violations[i];
      try {
        const filename = `${route.replace(/\//g, '_')}_${violation.rule}_${i + 1}.png`;
        const filepath = path.join(violationsDir, filename);
        
        if (violation.element) {
          const element = await page.$(violation.element).catch(() => null);
          if (element) {
            await element.screenshot({ path: filepath });
            violation.screenshot = filepath;
          }
        } else {
          await page.screenshot({ path: filepath, fullPage: true });
          violation.screenshot = filepath;
        }
      } catch (error) {
        console.warn(`Could not capture screenshot: ${error.message}`);
      }
    }
  }

  generateReport(violations, warnings, passed) {
    const separator = '─'.repeat(50);
    
    let output = `\n\n🔍 Accessibility Oracle Report\n\n`;
    output += `Target: ${this.config.project.base_url}\n`;
    output += `Format: ${this.format}\n\n`;
    output += `${separator}\n\n`;

    if (passed.length > 0) {
      output += `✓ PASS ${passed.length} route(s)\n`;
      for (const p of passed) {
        output += `  - ${p.route}: ${p.message}\n`;
      }
      output += '\n';
    }

    if (violations.length > 0) {
      output += `✗ FAIL  ${violations.length} violation(s)\n\n`;
      
      const criticalViolations = violations.filter(v => v.severity === 'critical' || v.impact === 'critical');
      const seriousViolations = violations.filter(v => v.impact === 'serious');
      
      for (const v of violations) {
        const icon = v.impact === 'critical' || v.severity === 'critical' ? '🔴' : '🔴';
        output += `${icon} ${v.rule.toUpperCase()}\n`;
        output += `  Element: ${v.element || 'unknown'}\n`;
        output += `  Message: ${v.message}\n`;
        if (v.screenshot) {
          output += `  Screenshot: ${v.screenshot}\n`;
        }
        output += '\n';
      }
    }

    if (warnings.length > 0) {
      output += `🟡 WARNINGS  ${warnings.length} warning(s)\n\n`;
      for (const w of warnings) {
        output += `🟡 ${w.rule}\n`;
        output += `  Element: ${w.element || 'unknown'}\n`;
        output += `  Message: ${w.message}\n\n`;
      }
    }

    output += `${separator}\n\n`;
    output += `Summary:\n`;
    output += `  Passed: ${passed.length}\n`;
    output += `  Violations: ${violations.length}\n`;
    output += `  Warnings: ${warnings.length}\n`;
    output += `  Exit code: ${violations.length > 0 ? 1 : 0}\n`;

    return output;
  }
}

module.exports = { AccessibilityOracle };
