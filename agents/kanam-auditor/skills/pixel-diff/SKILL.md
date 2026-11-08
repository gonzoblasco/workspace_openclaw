---
name: "pixel-diff"
description: "Comparación de desalineación visual entre especificación y realidad. Mide que el CSS realmente consuma los tokens, compara screenshots contra baseline CI, y permite usar capturas manuales como verdad de diseño temporal. Figma queda como placeholder hasta nuevo aviso."
metadata:
  category: "Crew"
  tags:
    - crew
    - auditor
    - design-system
    - visual-regression
    - pixel-diff
---

# pixel-diff

Ritual de alineación pixel-perfect. No mide solo código - mide que el CSS realmente se traduzca en los valores esperados.

La diferencia con `design-system-enforcer`: el Enforcer valida que uses tokens; el Pixel Diff verifica que **el resultado sea el correcto** en pantalla.

## Baseline storage (convención C.1) — local, reproducible

La verdad visual para regresión no se versiona en `git` por peso (PNGs) ni se
inventa sin captura. Convención dentro de un proyecto:

```text
.kanam/baselines/
├── manifest.json     # slug → png, fuente, fecha
├── home.png          # captura aprobada
└── card.png
```

Comando:
```bash
pixel-baseline --save <captura.png> --dir .kanam/baselines --name home
# luego: pixel-diff --mode baseline --baseline .kanam/baselines --current <current-dir>
```

Si no hay captura aprobada (sin baseline), `pixel-diff` solo puede emitir **opinión**, no regresión. No correrlo en modo bloqueo sin baseline real.

## Cuándo usarla

- Post-render: validar que los tokens aplicados producen el resultado visual esperado.
- CI/CD: detectar visual regression contra baselines.
- Multi-temporal: usar capturas manuales como spec cuando no hay Figma.
- Preparado para Figma: placeholder listo cuando cambie la fuente de verdad.

## Protocolo de pixel-diff

### 1. Declaración de fuentes

Cada proyecto define de dónde viene la verdad visual en `.kanam/pixel-diff.config.yaml`:

```yaml
project:
  name: "mi-proyecto"

sources:
  # Hoy: capturas manuales como spec (la fuente principal)
  - type: "comp"
    path: "./design-captures/"
    mapping:
      "./design-captures/card.png": "/card"
      "./design-captures/home.png": "/"
  
  # Mañana: Figma cuando esté disponible (placeholder)
  # - type: "figma"
  #   file_id: "..."
  
  # Siempre: tokens como fallback estructural
  - type: "design-system"
    path: "/design"

checks:
  spacing_alignment: true
  radius_consistency: true
  color_accuracy: true
  typography_scale: true

thresholds:
  spacing_tolerance: 1px      # ±1px permitido
  radius_tolerance: 0.5px     # Radios deben ser exactos
  color_delta_e: 2.3          # Diferencia perceptible mínima
  typography_scale: 0.1em     # Escala tipográfica flexible
```

### 2. Modos de operación

| Modo | Comando | Uso |
|------|---------|-----|
| **comp** | `pixel-diff --mode comp --design ./capturas/card.png --url http://localhost:3000/card` | Captura manual como spec (declarada en `specs.yaml`) + pixelmatch contra el render |
| **baseline** | `pixel-diff --mode baseline --baseline ./screenshots/baseline/ --current ./screenshots/current/` | Visual regression CI con pixelmatch real |
| **tokens** | `pixel-diff --mode tokens --tokens ./design/tokens --url http://localhost:3000` | Valida que el render consuma los tokens del DS |

> **Real, no simulado.** La captura usa Playwright (`playwright-core`) y el diff usa
> `pixelmatch` + `pngjs`. El Delta E es CIEDE2000 perceptual real. Si un valor no es
> medible (p. ej. un token sin resolver), se reporta como `NO MEDIBLE`, nunca se inventa.

### 2.1 Specs declaradas (modo comp)

Cuando no hay Figma, el humano declara la verdad visual una vez y queda versionada en
`.kanam/pixel-diff.specs.yaml`. Modo interactivo para generarla:

```bash
pixel-diff --mode comp --design ./design-captures/card.png \
  --url http://localhost:3000 --route /card --interactive
```

```yaml
# .kanam/pixel-diff.specs.yaml
specs:
  "design-captures/card.png":
    name: card
    spacing: { padding_internal: "16px", margin_between: "32px" }
    radius:  { card: "16px", button: "999px" }
    colors:  { primary: "#2563eb", background: "#ffffff", text: "#111318" }
    typography: { title_size: "22px", font_family: "Inter" }
```

Sin spec declarada ni tokens, el modo comp **falla con `NO_SPEC`** (exit 2). No se inventa.

### 3. Veredicto de alineación

```
ALINEADO: Todos los valores coinciden dentro de la tolerancia.
DESALINEADO: Hay desfasajes. Se listan con magnitud y sugerencia de corrección.
ESPECULATIVO: La fuente es una captura no verificada. Se marca para revisión humana.
```

## Salida de ejemplo (modo comp)

```bash
$ npx pixel-diff --mode comp --design ./capturas/card.png --url http://localhost:3000/card

🔍 Pixel Diff Report - Modo: COMP

Design source: ./capturas/card.png (captura manual)
Implementation: http://localhost:3000/card

SPACING
────────
✓ Padding interno: 16px (espec: 16px) - ALINEADO
✗ Margen entre cards: 24px (espec: 32px) - DESFASE de 8px ↓
  Sugerencia: Revisar margin-bottom del container
  
RADIUS
──────
✓ Card radius: 8px (espec: ~8px) - ALINEADO
✗ Button radius: 4px (espec: pill/999px) - DESFASE CRÍTICO
  Sugerencia: border-radius: 999px

COLOR
─────
✓ Background: #FFFFFF (espec: #FFFFFF) - MATCH
✗ Primary: #0D9488 (espec: #2563EB estimado) - DELTA E: 32.4
  ⚠️  Color muy diferente. ¿Es intencional o bug?

TYPOGRAPHY
──────────
✓ Font size title: ~24px - ALINEADO
✗ Font family: Inter (espec: parece system-ui) - REVISAR
  Nota: Spec de comp no siempre es tipografía final

Métricas:
  Alineamiento: 75% (6/8 checks)
  Desfasajes críticos: 2 (radius, color primary)
  Desfasajes menores: 1 (spacing)
```

## Integración con herramientas existentes

| Herramienta | Relación |
|-------------|----------|
| `design-system-enforcer` | Enforcer valida código fuente; Diff mide resultado renderizado. |
| `accessibility-oracle` | Oracle mide accesibilidad runtime; Diff mide alineación visual. |
| `surface-alignment-audit` | Auditor es humano y post-mortem; Diff es automatizado y pre-merge. |

## Estructura de archivos

```
pixel-diff/
├── SKILL.md                 # Este archivo
├── src/
│   ├── pixel-diff.js        # CLI principal / orquestador
│   ├── comparator.js        # Lógica de comparación (px + Delta E)
│   ├── reality.js           # Realidad: DOM geometry + muestreo de píxeles del render
│   ├── report.js            # Reportes console/json/html
│   ├── adapters/
│   │   ├── comp.js          # Captura manual como spec + pixelmatch
│   │   ├── baseline.js      # Regresión visual real (pixelmatch 1:1)
│   │   ├── tokens.js        # Spec desde tokens del DS (DTCG/CSS)
│   │   └── figma.js         # Placeholder para API Figma
│   └── utils/
│       ├── color.js         # parse, Lab, Delta E CIE76/CIEDE2000, muestreo
│       ├── image.js         # pngjs load/resize/diff + regiones
│       ├── capture.js       # Playwright: screenshot + geometría computada
│       ├── tokens.js        # Loader DTCG/JSON/CSS + resolución de referencias
│       └── specs.js         # Specs declaradas (.specs.yaml) + modo interactivo
├── tests/
│   ├── fixtures/
│   │   ├── page.html
│   │   ├── kanam.tokens.json
│   │   └── tokens.css
│   └── pixel-diff.test.js
├── examples/
│   └── .kanam/pixel-diff.config.yaml
└── bin/
    └── pixel-diff            # Entry point
```

## Dependencias reales

`playwright-core` (captura), `pixelmatch` + `pngjs` (diff binario), `commander`, `js-yaml`.
Requiere un navegador instalado: `node node_modules/playwright-core/cli.js install chromium-headless-shell`.

## Red Lines

- **No inventar specs.** Si no hay captura ni token, no hay verdad.
- **No tolerar desfasajes críticos.** Un radio pill cuando el diseño dice 4px es rechazo, no sugerencia.
- **No ignorar capturas manuales.** La verdad visual puede estar en una imagen, no solo en un archivo de tokens.
- **No aflojar tolerancias.** Un desfase de 1.1px es un error, no "casi bien".

---

_La verdad visual no es relativa. La pixel-diff no perdona._
