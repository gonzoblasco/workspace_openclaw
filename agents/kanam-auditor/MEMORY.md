# MEMORY.md - The UI/UX Auditor 🎨

> Memoria durable **del agente**, en su propio workspace. El `MEMORY.md` de la raíz del workspace pertenece a `main`; este archivo es el mío. Si algo contradice a otro archivo, gana la fuente que corresponda a cada dominio: acá viven mis hechos de superficie, el estado de mi arsenal y mis disparadores. Nada de esto se copia al root.

## Qué soy y qué es mío

- **Rol:** guardián de la superficie. Audito coherencia con el Design System y accesibilidad WCAG 2.2 AA. No redefino tokens (eso es del dueño del DS), no escribo código de producto, no decido prioridad de producto.
- **Vara, no gusto:** `../../design/tokens.md` + `../../design/principles.md`. Lo hardcodeado es error arquitectónico, no preferencia estética.
- **Mi arsenal** (todo bajo `agents/kanam-auditor/skills/`):
  - `design-system-enforcer/` — `bin/design-enforcer`. Estático, sobre código fuente.
  - `accessibility-oracle/` — `bin/a11y-oracle`. Runtime, Playwright + axe-core, multi-ruta.
  - `pixel-diff/` — `bin/pixel-diff`. Render real vs captura/tokens.
  - `surface-pipeline/` — `bin/audit-surface`. Orquestador: un comando, un veredicto.
  - `surface-alignment-audit/` — ritual humano, sin código.
- **Fuente de verdad de mi estado:** `ROADMAP.md`. Si este archivo y el ROADMAP discrepan sobre madurez, gana el ROADMAP.

## Hitos de mi evolución

- **2026-11-17:** el oracle dejó de delegar el contraste en axe. `src/checks/contrast.js` mide el ratio WCAG (luminancia relativa, composición de fondos, umbral por rol) y el estado `:focus`. Hallazgo inmediato: `--k-brand-primary` con blanco da 3.74:1, bajo el 4.5:1 de texto normal — anotado para el dueño del DS, no lo corregí yo.
- **2026-11-06 (v0.1 → arranque de v0.2):** corrí el Flujo A (Portero) en un PR real de preflight-a11y. Publicado y probado en las dos direcciones: aprueba y rechaza (4 runs, 1 comentario).
- **2026-11-06:** descubrí el falso verde del pipeline (0 archivos → APROBADO en CI), tapado con el guard `stage-no-files`.
- **2026-11-06:** definí la frontera de a11y en ADR-111 (medición / política / orquestación).
- **2026-11-06:** aprendí por la fuerza que los heredocs inline dentro de `run: |` se pliegan al parsear `action.yml` y matan el step sin mensaje. Regla: lo que tiene heredoc o comillas anidadas vive en un script con test.

## Hechos verificados que no quiero volver a descubrir

<!-- observed: 2026-11-06 | status: active -->

- **`projects/` está gitignored** (`.gitignore:58`). Un stage apuntado ahí escanea **0 archivos** en CI y devuelve APROBADO. Es el falso verde más barato de producir. Por eso existe el guard `stage-no-files` (`surface-pipeline/src/stages.js`): 0 archivos escaneados = finding `critical`, nunca aprobado.
- **Los repos de producto NO viven en el workspace.** `projects/preflight` y `projects/kanam-fixer` son sus propios repos (`gonzoblasco/preflight-a11y`, `gonzoblasco/kanam-fixer`). Un gate instalado en el workspace no cubre ningún PR de producto. El Portero va en cada repo de producto.
- **El Portero está publicado:** `gonzoblasco/surface-audit-action@v1`. Tres líneas de YAML, autodetecta `src/`, emite veredicto en ~10 s. Verificado en `preflight-a11y#1`, en las dos direcciones.
- **Un linter de design system necesita `exclude`.** El motor del enforcer contiene las cadenas que busca (`linear-gradient(`, tabla de morados, tabla de colores nombrados) y los tests contienen fixtures que disparan a propósito. Sin `exclude`, el auto-scan reporta sus propias definiciones de reglas como violaciones: 5 bloqueos medidos, los 5 falso positivo (2026-11-06).
- **El browser de Playwright** se instala con el CLI del paquete local, no con el global. `npx playwright install` baja la revisión del playwright global (1254) y `pixel-diff` pide la 1248 de `playwright-core@1.64.0`. Correcto: `node node_modules/playwright-core/cli.js install chromium-headless-shell` desde el skill.
- **Frontera de a11y (ADR-111, `../../docs/adr/ADR-111-*.md`):** tres capas con dueño distinto. Medición (`oracle` / `scripts/a11y-scan.mjs`), política (`scripts/check-a11y-trigger.py`, decide cuándo hace falta validación manual con AT) y orquestación (`audit-surface`, único que emite veredicto). No se fusionan: absorber `a11y-scan.mjs` en el oracle metería Playwright en la lane de CI que hoy corre con cero dependencias.
- **Los steps inline con heredoc** se pliegan al parsear `action.yml`. `cat > f <<EOF` a columna 0 dentro de un `run: |` rompe el YAML del action. Todo heredoc o comilla anidada va a un script con test.
- **Los steps inline con heredoc** se pliegan al parsear `action.yml`. `cat > f <<EOF` a columna 0 dentro de un `run: |` rompe el YAML del action. Todo heredoc o comilla anidada va a un script con test.

## Red lines del agente

- No emito veredicto sin evidencia reproducida desde el reporte emitido (archivo, no consola efímera).
- No inflo la versión. El número se gana con el criterio de listo cumplido.
- No invento tokens, versiones ni hechos. Lo no implementado falla explícito.
- No apruebo una superficie por gusto personal.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
