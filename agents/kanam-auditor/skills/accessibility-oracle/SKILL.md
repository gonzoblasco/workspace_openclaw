---
name: "accessibility-oracle"
description: "Auditoría automatizada de accesibilidad en runtime. Ejecuta páginas reales con Playwright + axe-core, simula navegación por teclado, verifica foco visible y genera reportes con evidencia visual. Multi-tenant: cualquier proyecto puede declarar sus rutas críticas y reglas WCAG."
metadata:
  category: "Crew"
  tags:
    - crew
    - auditor
    - accessibility
    - wcag
    - automation
    - ci-cd
---

# accessibility-oracle

Ritual de auditoría accesible en runtime. No opina sobre código - ejecuta, navega y mide
comportamiento real contra WCAG 2.2.

La diferencia con `surface-alignment-audit`: el Auditor revisa lo que ve; el Oracle verifica
lo que **funciona**.

## Cuándo usarla

- CI pipeline: validación automática en cada PR o deploy.
- Pre-release: auditoría completa de rutas críticas antes de publicar.
- Revisión de accesibilidad: segundo par de ojos automatizado contra WCAG 2.2.
- Multi-proyecto: cualquier sitio, cualquier framework, cualquier design system.

## Protocolo de auditoría accesible

### 1. Declaración del sistema

Cada proyecto declara sus rutas críticas y reglas en `.kanam/a11y-oracle.config.yaml`:

```yaml
project:
  name: "mi-proyecto"
  base_url: "http://localhost:3000"

paths:
  - route: "/"
    critical: true
  - route: "/checkout"
    critical: true
    requires_auth: false
  - route: "/settings"
    critical: false

rules:
  contrast: "wcag22-aa"
  keyboard_navigation: true
  focus_visible: true
  target_size: true
  skip_rules: []

report:
  format: ["html", "json", "junit"]
  screenshot_on_violation: true
  video_record: false
```

### 2. Ejecución de verificaciones

El oracle ejecuta en secuencia:

| Check | Herramienta | Qué mide |
|-------|-------------|----------|
| **axe-core** | axe-core/playwright | 50+ reglas WCAG automáticas (contrast, ARIA, labels, etc.) |
| **Contraste medido** | `src/checks/contrast.js` | Ratio real WCAG 1.4.3 sobre pares texto/fondo computados, incluido el estado `:focus` |
| **Keyboard** | Playwright keyboard | Tab order, Enter/Space activation, Escape, focus trapping |
| **Focus Visible** | Screenshot + bounding box | Indicador de foco ≥2px² o contraste ≥3:1 |
| **Target Size** | Bounding box | Elementos interactivos ≥24x24px (WCAG 2.2 AA) |
| **Semantic** | axe-core + manual | ARIA roles, live regions, form labels, headings |

### 2.1 Contraste medido, no delegado

axe-core deja como `incomplete` lo que no puede resolver: fondos con imagen, estados de
foco/hover y pares compuestos. El oracle calcula el ratio él mismo con la fórmula de
luminancia relativa de WCAG sobre los estilos computados:

- Compone la pila de fondos (alpha incluido) hasta el primero opaco; si no hay ninguno, asume
  el canvas blanco.
- Aplica la opacidad del elemento al color del texto: un `opacity: .5` reduce el contraste
  aunque el color sea opaco.
- Umbral por rol del texto: **4.5:1** normal, **3:1** si es grande (≥24px, o ≥18.66px en
  negrita).
- Mide además el estado `:focus` de los interactivos. Un fallo que ya existe en reposo se
  reporta una vez, no dos: el hallazgo es del par base.
- Un fondo con imagen no se declara aprobado: se emite `contrast-indeterminate` como warning
  con el ratio calculado, para que alguien lo verifique con captura.

Configuración (todas opcionales, bajo `rules`):

```yaml
rules:
  contrast_max_elements: 300        # tope de pares medidos por ruta
  contrast_states: true             # medir :focus en interactivos
  contrast_max_state_elements: 12   # cuántos interactivos se enfocan
```

El reporte imprime **cuántos pares midió**, no solo cuántos fallaron: un check que no puede
mostrar su muestra no prueba nada.

### 3. Veredicto de accesibilidad

```
✓ PASS: Página cumple WCAG 2.2 AA. Sin violaciones automáticas ni de teclado.
✗ FAIL: Página tiene violaciones. Se listan con evidencia visual y sugerencia de corrección.
🟡 WARNING: Problemas menores de UX accesible que no bloquean WCAG.
```

### 4. Salida de ejemplo

```bash
$ npx a11y-oracle --config .kanam/oracle.config.yaml

🔍 Accessibility Oracle Report
Target: http://localhost:3000
Pages: 3 critical, 1 optional
Rules: WCAG 2.2 Level AA

─────────────────────────────────────

✓ PASS  / (Home)
  - 0 axe violations
  - Keyboard: All interactive elements reachable
  - Focus: Visible on 100% of focusable elements

✗ FAIL  /checkout (Critical)

  🔴 CONTRAST VIOLATION
  Element: .submit-button
  Foreground: #FFFFFF / Background: #3B82F6
  Ratio: 2.8:1 (required: 4.5:1)
  Screenshot: violations/checkout-submit-button.png

  🔴 FOCUS NOT VISIBLE
  Element: #card-number input
  Issue: Focus ring removed with outline: none
  Screenshot: violations/focus-card-number.png

  ⌨️  KEYBOARD TRAP
  Element: .modal-overlay
  Issue: Focus escapes modal on Tab, no Escape handler

─────────────────────────────────────

Summary:
  Critical pages passing: 1/3
  Total violations: 3 (contrast: 1, focus: 1, keyboard: 1)
  Warnings: 1 (target size)
  Exit code: 1 (CI will fail)
```

## Integración con herramientas existentes

| Herramienta | Relación |
|-------------|----------|
| `design-system-enforcer` | Enforcer valida código fuente estático; Oracle valida runtime accesible. Complementarios. |
| `surface-alignment-audit` | Auditor revisa visual post-render; Oracle verifica comportamiento funcional. |
| `scripts/a11y-scan.mjs` | a11y-scan es un chequeo puntual; Oracle es una auditoría completa con rutas, teclado y evidencia. |
| `agents/kanam-dev/skills/a11y-at-validation` | a11y-at cubre lectores de pantalla; Oracle cubre navegación por teclado y contraste. |

## Estructura de archivos

```
accessibility-oracle/
├── SKILL.md                 # Este archivo
├── src/
│   ├── oracle.js            # CLI principal
│   ├── runner.js            # Orquesta Playwright + axe
│   ├── checks/
│   │   ├── axe.js           # axe-core injection
│   │   ├── keyboard.js      # Tab/Enter/Escape simulation
│   │   ├── focus-visible.js # Screenshot + bounding box
│   │   └── target-size.js   # Bounding box measurement
│   ├── reporters/
│   │   ├── html.js          # Reporte visual con screenshots
│   │   ├── json.js          # Datos estructurados
│   │   └── junit.js         # CI integration
│   └── utils/
│       ├── screenshot.js    # Captura con timestamp
│       └── contrast.js      # Cálculo de ratio de contraste real
├── tests/
│   ├── fixtures/
│   │   ├── accessible.html
│   │   └── inaccessible.html
│   └── oracle.test.js
├── examples/
│   ├── .kanam/oracle.config.yaml
│   └── reports/             # Ejemplos de salida
└── bin/
    └── a11y-oracle          # Entry point
```

## Red Lines

- **No aflojar umbrales WCAG.** Si falla AA, falla. No hay "casi cumple".
- **No ignorar critical paths.** Una página crítica con violación = CI rojo.
- **No reportar sin evidencia.** Cada violación lleva screenshot o video.
- **No depender solo de axe-core.** El keyboard testing es manual scriptado, no opcional.

---

_La accesibilidad no se opina, se verifica._
