const { AccessibilityOracle } = require('../src/oracle');
const fs = require('fs');
const path = require('path');

describe('AccessibilityOracle', () => {
  let oracle;
  let tempDir;

  beforeEach(() => {
    tempDir = path.join(__dirname, 'temp-test');
    fs.mkdirSync(tempDir, { recursive: true });
    
    // Create temp config
    const configDir = path.join(tempDir, '.kanam');
    fs.mkdirSync(configDir, { recursive: true });
    
    const configContent = `
project:
  name: "test-project"
  base_url: "http://localhost:3000"
paths:
  - route: "/"
    critical: true
rules:
  contrast: "wcag22-aa"
  keyboard_navigation: true
  focus_visible: true
  target_size: true
  skip_rules: []
report:
  format: ["console"]
  screenshot_on_violation: true
`;
    
    fs.writeFileSync(path.join(configDir, 'a11y-oracle.config.yaml'), configContent);
    
    oracle = new AccessibilityOracle({
      configPath: path.join(configDir, 'a11y-oracle.config.yaml'),
      outputDir: tempDir
    });
  });

  afterEach(() => {
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  });

  test('debe inicializar con config por defecto', () => {
    expect(oracle.config.project.name).toBe('test-project');
    expect(oracle.config.rules.contrast).toBe('wcag22-aa');
  });

  test('debe generar reporte con formato correcto', () => {
    const report = oracle.generateReport(
      [{ rule: 'test', message: 'test violation', element: 'div' }],
      [{ rule: 'warn', message: 'test warning', element: 'span' }],
      [{ route: '/', message: 'passed' }]
    );
    
    expect(report).toContain('🔍 Accessibility Oracle Report');
    expect(report).toContain('✓ PASS');
    expect(report).toContain('✗ FAIL');
    expect(report).toContain('🟡 WARNINGS');
  });
});
