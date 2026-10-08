const fs = require('fs');
const path = require('path');

// Test para validar la funcionalidad básica del enforcer
describe('DesignSystemEnforcer', () => {
  let enforcer;
  let tempDir;
  let configDir;
  let configPath;

  beforeEach(() => {
    tempDir = path.join(__dirname, 'temp-test');
    fs.mkdirSync(tempDir, { recursive: true });

    // Crear archivo de configuración temporal
    configDir = path.join(tempDir, '.kanam');
    fs.mkdirSync(configDir, { recursive: true });
    configPath = path.join(configDir, 'enforcer.config.yaml');

    const configContent = `
project:
  name: "test-project"
  design_system_path: "/Users/gonzoblasco/.openclaw/workspace/design"
rules:
  enforceTokens: true
  blockHardcoded: true
  aiLookVeto: true
whitelist:
  hex: []
`;

    fs.writeFileSync(configPath, configContent);

    enforcer = new (require('../src/enforcer').DesignSystemEnforcer)({
      configPath: configPath
    });
  });

  afterEach(() => {
    // Limpiar archivos temporales
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  });

  test('debe detectar un gradiente decorativo', async () => {
    const filePath = path.join(tempDir, 'gradient.css');
    fs.writeFileSync(filePath, `
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px;
    `);

    const result = await enforcer.analyze(tempDir);

    expect(result.blocked).toBe(true);
    expect(result.stats.violations).toBe(1);
    expect(result.report).toContain('Gradiente decorativo prohibido');
  });

  test('debe detectar color morado prohibido', async () => {
    const filePath = path.join(tempDir, 'purple.css');
    fs.writeFileSync(filePath, `
      color: #8B5CF6;
      padding: 16px;
    `);

    const result = await enforcer.analyze(tempDir);

    expect(result.blocked).toBe(true);
    expect(result.stats.violations).toBe(1);
    expect(result.report).toContain('Morado genérico prohibido');
  });

  test('debe advertir sobre valores hex hardcodeados', async () => {
    const filePath = path.join(tempDir, 'hardcoded.css');
    fs.writeFileSync(filePath, `
      color: #3B82F6;
      padding: 16px;
    `);

    const result = await enforcer.analyze(tempDir);

    expect(result.blocked).toBe(false);
    expect(result.stats.warnings).toBe(1);
    expect(result.report).toContain('Valor hexadecimal hardcodeado');
  });

  test('debe detectar padding inflado', async () => {
    const filePath = path.join(tempDir, 'inflated.css');
    fs.writeFileSync(filePath, `
      background: white;
      padding: 24px;
      color: black;
    `);

    const result = await enforcer.analyze(tempDir);

    expect(result.blocked).toBe(false);
    expect(result.stats.warnings).toBe(1);
    expect(result.report).toContain('Padding potencialmente inflado');
  });

  test('debe detectar radio exagerado', async () => {
    const filePath = path.join(tempDir, 'round.css');
    fs.writeFileSync(filePath, `
      border-radius: 12px;
      background: white;
      color: black;
    `);

    const result = await enforcer.analyze(tempDir);

    expect(result.blocked).toBe(true);
    expect(result.stats.violations).toBe(1);
    expect(result.report).toContain('Borde exagerado detectado');
  });
});
