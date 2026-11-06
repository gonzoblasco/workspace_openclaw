# ROADMAP.md - UI/UX Auditor 🎨

> De Arsenal a Pipeline de Élite. Documento vivo. Registra la evolución del agente desde herramientas sueltas hasta auditor autónomo.
> Última actualización: 2026-10-07

**Versión actual:** v0.1 - "Herramientas sueltas"
**Objetivo de ronda:** v0.5 - confiable sin supervisión línea por línea
**Visión:** v1.0 - "El Auditor Autónomo" (Fase 5)
**Última revisión:** 2026-10-07
**Dueño:** kanam-auditor (autoría) · Kanam CORE (gobierno)

---

## Retrato verificado de la versión actual (v0.1 - "Herramientas sueltas")

> **Validado 2026-10-07 contra fuentes reales** (código de cada `src/`, `package.json`, suites de tests). Los `tests` en verde NO implican funcionalidad real: los cuatro ejecutables pasan porque el test verifica el andamiaje, no el efecto.

| Skill | Tests | Madurez | Realidad (verificada en código) |
|-------|-------|---------|----------------------------------|
| `design-system-enforcer` | 7/7 ✅ | 🟡 MVP | **Regex a nivel línea, no AST.** `scss-parser`/`typescript` están en deps pero no se usan para walkear. Veto AI-look con `includes()` + `parseInt`. Tiene `exclude` (necesario: sin él se auto-reporta). Sin modo `--fix`. |
| `accessibility-oracle` | 2/2 ✅ | 🟢 Real | **Sustancia real** (Playwright + axe-core). **Corregido 2026-11-06:** sí itera `config.paths[]` (`src/oracle.js:150-235`) y sí escribe `report.json` + `report.html` en `outputDir`. Brechas reales: sin cálculo de ratio de contraste propio, sin auth. |
| `pixel-diff` | 20/20 ✅ | 🟢 Real | Captura y diff reales (Playwright + ΔE CIEDE2000 + `pixelmatch`). Modos `comp`/`baseline`/`tokens` operativos. Figma sigue como placeholder que falla explícito. |
| `surface-pipeline` | 12/12 ✅ | 🟢 Real | **Corregido 2026-11-06:** no fabrica veredictos; corre y emite HTML+JSON. El riesgo de falso verde se movió al *target* y ya está tapado con el guard `stage-no-files`. |
| `surface-alignment-audit` | - | 🟢 Completo (procedimental) | Ritual humano documentado, sin código. |

**Problema actual:** los tres skills ejecutables funcionan **en aislamiento**. No hay pipeline unificado, no hay CI, y `pixel-diff` opera en modo simulado (no captura screenshots reales). Un pipeline construido sobre estos skills hoy devolvería **veredictos fabricados** - exactamente el falso verde que el checklist de roadmap existe para evitar.

**Honestidad de versión:** la orquestación existe y no fabrica veredictos desde el
2026-11-06, pero no corre todavía sobre ningún PR de producto: los repos de producto
viven fuera de este workspace. Eso es lo que me sigue haciendo v0.1 — no el código,
la falta de un consumidor automático.

**Nota de autoría (2026-10-07):** no hay evidencia en el repo (commits, metadatos, comentarios) sobre con qué modelo LLM se generaron estas skills. La atribución a Kimi-K3 que circuló en sesión **no está documentada**; no citarla como hecho.

### Corrección de retrato (2026-11-06, reverificado contra código y runtime)

Dos filas de arriba quedaron viejas. No se borran: se corrigen con fecha, porque un retrato que no se actualiza es el mismo problema que el roadmap-foto que este documento rechaza.

| Skill | Antes (2026-10-07) | Verificado (2026-11-06) |
|---|---|---|
| `accessibility-oracle` | "solo consola; una sola ruta" | **Falso hoy.** `run()` itera `config.paths[]` cuando no se pasa `--route` y escribe `report.json` + `report.html` en `outputDir` (`src/oracle.js:150-235`). Sigue faltando cálculo de contraste propio y auth. |
| `pixel-diff` | 20/20 ✅ | 20/20 ✅ **solo con el browser correcto**. Fallaba 2/20 en este host porque `chromium_headless_shell-1248` no estaba instalado (el `npx playwright` global bajaba la 1254, que no es la que pide `playwright-core@1.64.0`). Se instaló con `node node_modules/playwright-core/cli.js install chromium-headless-shell`. |
| `surface-pipeline` | "devuelve veredictos fabricados" | **Corre y emite veredicto real** con `report.html` + `report.json` (`bin/audit-surface`, verificado 2026-11-06). El riesgo de verde fabricado se movió al **target**: la config apuntaba a `agents/kanam-auditor/skills`, o sea que se auditaba a sí mismo. |

---

## 🎯 Visión: v1.0 - "El Auditor Autónomo"

Un pipeline que corre en cada PR y devuelve **un veredicto único** con evidencia, listo para bloquear merges.

---

## Camino de madurez (v0.1 → v0.5 → v1.0)

> El trofeo v1.0 se gana por saltos con criterio de listo cumplido, no por edición del número. Las cinco fases de abajo son el camino: v0.1 → v0.5 (Fases 1-3) → v1.0 (Fases 4-5).

| Etapa | Qué es | Estado | Criterio de listo |
|---|---|---|---|
| v0.1 - "Herramientas sueltas" | Los cuatro skills existen y pasan sus tests, pero corren en aislamiento y parte de su funcionalidad es andamiaje. | ✅ | Retrato verificado contra código y runtime. |
| v0.5 - Arsenal real + un comando con evidencia | Los tres skills ejecutables son reales (no mocks) y un pipeline único devuelve un veredicto reproducible con evidencia. | 🟡 | `audit-surface` corre sobre una superficie real y su veredicto se reproduce desde el reporte emitido. |
| v1.0 - "El Auditor Autónomo" | El auditor corre solo en cada PR, bloquea merges y aprende del historial. | ⚪ | Auditoría automática en PR sin intervención humana, con memoria de hallazgos. |

---

## Fase 1 - Consolidación del Arsenal (ahora → +1 sesión)

**Objetivo:** que los tres skills ejecutables sean sólidos y reales.

### 1.1 `pixel-diff` → de simulado a real ✅ (2026-10-07)
- [x] Implementar captura real con Playwright (reemplazar `captureReality()` mock)
- [x] Implementar análisis de capturas manuales (modo `comp` real, specs declaradas)
- [x] Implementar `pixelmatch` para diff binario de imágenes
- [x] Añadir modo `--interactive` para que el humano declare specs de una captura
- [x] Resolución real de tokens (DTCG `.json` + CSS vars) - `extractTokensSpec` ya no devuelve `var(...)` sin resolver
- [x] Delta E perceptual real (CIEDE2000) - eliminado el stub que retornaba `0`
- [x] Reportes console/json/html con evidencia visual embebida
- [ ] Adapter Figma real (diferido a Fase 4; hoy falla explícito con `FIGMA_NOT_IMPLEMENTED`)

### 1.2 `accessibility-oracle` → endurecer
- [ ] Test de contraste real (calcular ratio, no solo confiar en axe)
- [ ] Soporte multi-página (recorrer todo el `paths[]` de config, no solo una ruta)
- [ ] Reportes HTML/JUnit reales (hoy solo console)
- [ ] Manejo de autenticación (`requires_auth`)

### 1.3 `design-system-enforcer` → extender
- [ ] Parser AST real de JSX/TSX (hoy usa regex)
- [ ] Detección de colores en styled-components y CSS-in-JS
- [ ] Modo `--fix` (auto-reemplazo de hex por tokens)

**Entregable Fase 1:** los tres skills con tests verdes y funcionalidad real, no mocks.

---

## Fase 2 - El Pipeline Unificado (+2 sesiones)

**Objetivo:** un comando, un veredicto.

### 2.1 Skill orquestador: `surface-pipeline`
```
skills/surface-pipeline/
├── SKILL.md
├── src/
│   └── pipeline.js          # Orquesta los 3 skills
└── bin/
    └── audit-surface        # Entry point único
```

**Comportamiento:**
```bash
$ npx audit-surface --config .kanam/pipeline.config.yaml

🔍 SURFACE AUDIT PIPELINE
═══════════════════════════════════════

[1/3] Design System Enforcer    ✓ 47 files, 0 blocks
[2/3] Accessibility Oracle      ✗ 3 violations (contrast, focus, keyboard)
[3/3] Pixel Diff                ⚠ 2 misaligned (radius, color)

───────────────────────────────────────
VEREDICTO: ❌ RECHAZADO
  - 3 violaciones críticas de accesibilidad
  - 2 desalineaciones visuales

Reporte: ./reports/audit-2026-10-07.html
```

### 2.2 Reporte unificado
- [ ] HTML consolidado con las 3 secciones
- [ ] Evidencia visual agregada (screenshots)
- [ ] Formato JUnit para CI
- [ ] Formato JSON para integraciones

### 2.3 Config unificada
```yaml
# .kanam/pipeline.config.yaml
project:
  name: "kanam-core"

stages:
  - skill: design-system-enforcer
    path: "./src"
    rules: { aiLookVeto: true }
  - skill: accessibility-oracle
    base_url: "http://localhost:3000"
    paths: ["/", "/checkout"]
  - skill: pixel-diff
    mode: "comp"
    captures: "./design-captures"

gate:
  block_on: ["critical", "accessibility-violation"]
  warn_on: ["misaligned"]
```

**Entregable Fase 2:** un comando que audita toda la superficie y devuelve veredicto único.

---

## Fase 3 - Integración CI/CD (+1 sesión)

**Objetivo:** automatizar en el flujo de trabajo.

- [ ] **GitHub Action** reutilizable (`.github/actions/surface-audit/`)
- [ ] **Pre-commit hook** (Husky) → corre solo `design-system-enforcer`
- [ ] **PR comment bot** → publica el reporte como comentario en el PR
- [ ] **Badge de estado** → "Surface Audit: passing"
- [ ] **Baseline storage** → guarda screenshots aprobados para regresión

```yaml
# .github/workflows/surface-audit.yml
name: Surface Audit
on: [pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./skills/surface-pipeline/action
        with:
          config: .kanam/pipeline.config.yaml
```

**Entregable Fase 3:** auditoría automática en cada PR sin intervención humana.

---

## Fase 4 - Figma & Visión (+futuro, cuando consigas trabajo)

**Objetivo:** activar la fuente de verdad que hoy es placeholder.

### 4.1 Adapter Figma real
- [ ] `pixel-diff/src/adapters/figma.js` (hoy placeholder)
- [ ] API token + file_id + node_id
- [ ] Extracción de specs desde Figma (spacing, radius, colors, typography)
- [ ] Comparación Figma → implementación

### 4.2 Comprensión de capturas con visión
- [ ] Analizar una captura y extraer specs aproximadas (usando el modelo visual)
- [ ] Modo `--interactive` para validar specs extraídas
- [ ] Cachear specs en `.kanam/pixel-diff.specs.yaml`

**Entregable Fase 4:** pipeline que acepta Figma, capturas manuales o tokens indistintamente.

---

## Fase 5 - Inteligencia y Memoria (+2 sesiones)

**Objetivo:** el auditor aprende del historial.

- [ ] **Historial de veredictos** → trackear desalineaciones recurrentes por componente
- [ ] **Detección de patrones** → "este botón falla contraste desde 3 sprints"
- [ ] **Sugerencias proactivas** → "según el historial, revisá el radio de las cards"
- [ ] **Métricas de tendencia** → dashboard de salud visual del producto
- [ ] **Integración con wiki-compiled** → alimentar `memory/` con hallazgos durables

**Entregable Fase 5:** auditor que no solo detecta, sino que **aconseja** con base en datos.

---

## 🧭 Plan v0.2 — "Cañería antes que arsenal" (propuesto 2026-11-06)

> **La versión no sube.** Este plan no gana v0.2: la gana cuando los tres flujos corran y se
> verifiquen. El diagnóstico que lo originó: no faltan skills, falta cañería. Cuatro CLIs
> funcionando, desconectados entre sí y de un flujo de trabajo real.
>
> Regla de oro del plan: **no se agrega ningún skill nuevo hasta que los tres flujos corran.**

### Diagnóstico medido (2026-11-06)

| Pieza | Estado | Evidencia |
|---|---|---|
| `design-enforcer` CLI | 🟢 | 5/5 tests |
| `accessibility-oracle` CLI | 🟢 | 2/2 tests, multi-ruta + reportes |
| `pixel-diff` CLI | 🟢 | 20/20 tras instalar el browser correcto |
| `audit-surface` | 🟢 | emite HTML+JSON con veredicto |
| `.kanam/pipeline.config.yaml` | 🟡→🟢 | **corregido**: apuntaba a sí mismo y luego a un path gitignored; ahora a la superficie trackeada (`agents/kanam-auditor/skills`) con guard de 0 archivos |
| `.github/workflows/surface-audit.yml` | 🔴→🟢 | **no existía** aunque la config lo citaba; creado 2026-11-06 |
| A11y | 🟠→🟢 | dos caminos compitiendo; borde definido en **ADR-111** |

### Fase 0 — Cerrar la grieta ✅ (2026-11-06)

- [x] **0.1** Browser correcto para `pixel-diff` → 20/20 (no era un bug de código: era la revisión 1248 vs 1254).
- [x] **0.2** Borde de a11y definido: **ADR-111** — medición (`oracle` / `a11y-scan.mjs`) ≠ política (`check-a11y-trigger.py`) ≠ orquestación (`audit-surface`). Se revisó la recomendación inicial: `oracle` **no** absorbe a `a11y-scan.mjs`, porque eso metería Playwright en la lane de CI que hoy corre con cero dependencias.
- [x] **0.3** Target real: `projects/preflight/src` (único producto con frontend vivo: Next.js, `app/` + `components/` + `globals.css`).
- [x] **0.4** Contrato de exit documentado en la config y verificado contra `bin/audit-surface`: `0` = aprobado/advertencia, `1` = rechazado o `--strict`, `1` = error de arranque.
- [x] **0.5** **Guard de cobertura `stage-no-files`** + soporte `exclude` en el enforcer. Descubierto al simular CI desde un checkout limpio: `projects/` está gitignored (`.gitignore:58`), así que el audit escaneaba **0 archivos** y devolvía **APROBADO**. El falso verde más barato de producir y el más caro de descubrir, y el pipeline lo tenía. Ahora 0 archivos escaneados es un finding `critical`. En el mismo barrido, el auto-scan reportaba 5 "violaciones" que eran las **definiciones de reglas del propio motor** (`linear-gradient(` dentro del detector, la tabla de morados): `exclude` las excluye, como `.eslintignore`. Tests: 7/7 enforcer + 12/12 pipeline.

**Primer veredicto real sobre código real:** `ADVERTENCIA — 0 bloqueantes, 34 advertencias` sobre `agents/kanam-auditor/skills` (20 archivos). Las advertencias son reales: los generadores de reporte HTML hardcodean hex en vez de consumir tokens. Antes de 0.5 ese mismo comando daba **APROBADO con 0 archivos leídos** en CI.

### Flujo A — "El Portero" (PR Gate) 🚧

- [x] **A.1** `.github/workflows/surface-audit.yml`: corre `--only design-system-enforcer` (única lane que no necesita browser), con path filter, `concurrency`, job summary, artifact y enforce de exit. Sintaxis validada localmente; **pendiente de probar en un PR real**.
- [x] **A.2** PR comment bot con marcador `<!-- surface-audit -->`: un comentario que se **actualiza**, no se multiplica.
- [ ] **A.3** Verificar el path filter contra un PR real (no dispara en docs, sí en `**/*.css`).
- [ ] **A.4** Medir tiempo hasta el comentario (`<3 min` es el criterio).

### Flujo B — "El Compañero" (Dev Loop) ⚪

- [ ] **B.1** Pre-commit fast lane: solo `design-enforcer` sobre staged, presupuesto **<2s p95**.
- [ ] **B.2** `audit-surface --watch` sin browser.
- [ ] **B.3** `--fix` **solo** con mapeo hex→token 1:1 verificable, `--dry-run` por defecto. El rechazo original (sin AST) sigue vigente para el caso heurístico.

### Flujo C — "El Arquitecto" (Cadencia) ⚪

- [ ] **C.1** Onboarding de 3 productos (hoy solo `preflight` tiene frontend real: `abya-yala` y `kanam-fixer` no tienen `.tsx/.jsx/.css`).
- [ ] **C.2** Baseline de capturas en `.kanam/baselines/<producto>/`. Sin baseline, `pixel-diff` mide una opinión.
- [ ] **C.3** Enganchar `scripts/check-audit-due.py` (ya existe) al pipeline: hito cruzado → auditoría completa → `.knowledge/AUDIT.md`.
- [ ] **C.4** Score de superficie por producto. Recién con C.1-C.3 hay datos.

### Lo que este plan NO hace

| Rechazado | Razón |
|---|---|
| Cualquier skill nueva | Cuatro skills con la cañería rota = cinco problemas |
| Figma | Sin `file_id`/token sigue siendo placeholder |
| `--fix` con AST | Requiere parser JSX/TSX real; primero regex acotada y medir falsos positivos |
| Dashboard | Sin historial es decoración |
| Un tercer medidor de a11y | El problema era el borde, no la cantidad (ADR-111) |
| Subir a v0.2 ahora | Los flujos no corrieron todavía. La versión se gana |

## 📊 Resumen visual del roadmap

```
v0.1 (hoy)          v1.0              v1.1              v1.2+
─────────────       ─────────────     ─────────────     ─────────────
3 skills sueltos    + pipeline        + CI/CD           + Figma
tests mock          unificado         + PR bot          + visión
                    veredicto único   + baseline        + memoria
─────────────       ─────────────     ─────────────     ─────────────
FASE 1              FASE 2            FASE 3            FASE 4-5
Consolidación       Orquestación      Automatización    Inteligencia
```

---

## 🎯 Criterio de "Trofeo Ganado"

El auditor gana el trofeo cuando:

1. **Un solo comando** audita toda la superficie ✅ (Fase 2)
2. **Se ejecuta solo** en cada PR ✅ (Fase 3)
3. **Da un veredicto claro** con evidencia visual ✅ (Fase 2)
4. **No depende de revisión humana** para lo automático ✅ (Fase 3)
5. **Aprende** del historial ✅ (Fase 5)

---

## ⏱️ Prioridad recomendada

| # | Fase | Esfuerzo | Impacto | Prioridad |
|---|------|----------|---------|-----------|
| 1 | Consolidación | Media | Alto | 🔴 **Ahora** |
| 2 | Pipeline unificado | Media | **Máximo** | 🔴 **Ahora** |
| 3 | CI/CD | Baja | Alto | 🟡 Pronto |
| 4 | Figma & Visión | Alta | Medio | 🟢 Cuando toque |
| 5 | Inteligencia | Alta | Medio | 🔵 Futuro |

---

## 💡 Recomendación de arranque (revisada 2026-10-07)

**Corregida:** arrancar por la **Fase 1 (consolidación)**, no por la Fase 2. Un pipeline (Fase 2) montado sobre `pixel-diff` simulado y `oracle` con salida incompleta devolvería **veredictos fabricados** - el peor tipo de falso verde. Primero, que cada skill sea real y verificable; recién entonces orquestarlas.

Orden concreto sugerido:
1. **1.1 `pixel-diff` real** - ✅ **Completado 2026-10-07.** Captura real (Playwright) + `pixelmatch` + eliminados los stubs de `extractDesignSpec`/`captureReality`/`colorDeltaE`. 20/20 tests verdes (incluyen captura de navegador real y diff binario).
2. **1.2 `oracle` endurecer** - escribir el reporte a archivo (html/json) y recorrer todo el `paths[]`.
3. **1.3 `enforcer`** - decidir: ¿parser AST real o asumir el límite regex? Documentar la decisión antes de construir encima.
4. **Fase 2** - recién con 1.1-1.3 cerradas y con tests que prueben *efecto*, no andamiaje.

---

## Lo que rechacé (y por qué)

Hitos que evalué y **no** entraron. Un roadmap sin rechazos es una lista de compras; esto es lo que prueba que se pensó.

| Hito rechazado | Por qué no entró |
|---|---|
| **Arrancar por el pipeline unificado (Fase 2)** antes de consolidar (Fase 1) | Un orquestador montado sobre skills simulados o con salida incompleta devolvería **veredictos fabricados** - el peor falso verde. La capacidad que desbloquea (un comando) no paga el costo de la credibilidad que quema. |
| **Adapter Figma real ahora** | Hoy no hay token ni `file_id`/`node_id` con los que probarlo: sería un placeholder que finge funcionar. Diferido a Fase 4, donde la fuente existe y el placeholder falla explícito (`FIGMA_NOT_IMPLEMENTED`). |
| **Modo `--fix` del enforcer** (auto-reemplazo hex → token) | Auto-editar sin parser AST real puede romper código en silencio. Primero decidir si el límite regex es aceptable y documentarlo; recién después construir encima. |
| **Declarar modelo/autoría de las skills (p. ej. Kimi-K3)** | No hay evidencia en el repo (commits, metadatos, comentarios). Un dato no verificado no entra ni como nota histórica. |
| **Métricas de tendencia y sugerencias proactivas (Fase 5) ahora** | Dependen de un historial de veredictos que todavía no existe. Sin datos, la "inteligencia" sería una corazonada bien redactada. |
| **Marcar v0.2-v0.4 por optimismo** | El número se gana con la señal de listo cumplida y evidencia, no se edita. Saltar de número sin poder probarlo es usar el roadmap como foto. |
| **Usar el roadmap como backlog de tareas** | Lo concreto y fechado vive en `memory/memory.db`; acá va el estado de madurez, no la lista de tareas del sprint. |

---

## Red lines y criterio de cierre

**Red lines de mi evolución** - lo que este rol **no** va a hacer aunque parezca un avance:

- **No cruzo el dominio de otro rol.** Audito coherencia y accesibilidad; no redefino tokens ni el Design System (eso es del rol dueño), no escribo código de producto y no decido prioridad de producto.
- **No emito un veredicto sin evidencia reproducida.** Toda violación viene con el archivo, la captura o el log que la prueba; nunca con un auto-reporte.
- **No inflo la versión.** No subo de número sin el criterio de listo cumplido; no declaro "operativo" un skill cuyo test prueba andamiaje, no efecto.
- **No invento tokens, versiones ni hechos.** Si no está en la fuente, no se cita; si algo no está implementado, falla explícito en vez de simular.

**Cómo se mide el éxito** - si no se cumplen estas tres condiciones, la versión declarada es propaganda:

1. **El veredicto se reproduce.** Cualquiera puede volver a correr la auditoría y obtener el mismo resultado desde el reporte emitido (archivo, no consola efímera).
2. **Cada ✅ tiene prueba contra fuente real.** La versión declarada se verifica contra el filesystem, el código o el runtime - nunca contra la memoria del agente.
3. **El pipeline no fabrica verde.** Ningún componente simulado (mock, stub, placeholder) participa de un veredicto: si una etapa no es real, el resultado se marca como incompleto, no como aprobado.

---

_La consistencia es la forma más alta de profesionalismo visual._

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
