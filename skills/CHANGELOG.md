# SKILLS CHANGELOG.md

Registro de cambios de skills del workspace. Los cambios estructurales del workspace (no skills) van en `CHANGELOG.md` raiz; los aprendizajes en `docs/LEARNINGS.md`; la actividad diaria en `memory/`.

**Regla:** cada vez que se cree, modifique, fusione o elimine una skill, registrar aca en el mismo commit.

---

## [2026-09-24] - memory-wiki-workflow: la trampa de la capa de claims

### Contexto
Al activar `memory-wiki` (ADR-064) y probarlo end-to-end, la skill describia el flujo pero **no advertia la trampa central**: ingerir fuentes no alimenta los reports analiticos, porque estos leen la capa de **claims**, no el texto crudo. Ingeste 3 fuentes y los reports siguieron diciendo "no issues" en todos los casos. Casi se reporto como fallo del plugin; era un paso faltante del flujo. Un report que dice "No structured claims yet" no es un fallo, es una instruccion sobre el paso que falta.

### Changed
- **`memory-wiki-workflow`:** se documenta el flujo completo como secuencia explicita (`ingest` -> `entities con claims` -> `compile/lint`) y se advierte que sin el paso intermedio el vault queda con fuentes y analisis vacio.
- **Setup:** se corrige "luego `openclaw gateway restart`" -> verificado 2026-09-24 que `plugins enable` devolvio `restartRequired: false` y el `config patch` aplico sin reinicio. Se agregan los grants que pide el plugin (`allowConversationAccess`, `allowPromptInjection`) y la via oficial de activacion con `reviewToken`.

### Added
- **Paso de verificacion de detectores:** como saber que los reports funcionan de verdad (crear una entity con claims deliberadamente malos y confirmar que `claim-health`, `low-confidence` y `stale-pages` reportan exactamente esos defectos). Un detector esta probado recien cuando se le sembro el defecto; "no issues" sobre datos limpios no prueba nada.
- **Politica de ingesta:** `memory/` y `docs/entrevistas/` no se ingestan sin decision explicita; `bridge` y `unsafe-local` se dejan apagados.
- **Nota de durabilidad:** el vault vive fuera del workspace git y no tiene backup por versionado.

### Notes
- La description del frontmatter cambio (ahora nombra la trampa), asi que se actualizo `SKILLS-INDEX.md` y el mirror `.github/skills/`.

---

## [2026-09-24] - Nueva skill: cross-engine-css-measurement

### Contexto
En el cierre del PR adobe/react-spectrum #10517 (anchor positioning en el input hidden de RAC Checkbox/Radio), CI fallo en WebKit (6 tests) y Firefox (1) despues de que el run local en chromium pasara 6/6. La causa era medible, pero el metodo para llegar a ella estaba en ningun lado: hubo que construir sondas, aislar variables y hacer un A/B contra el commit anterior para saber si la regresion era nuestra o el test era fragil.

### Added
- **`cross-engine-css-measurement`:** metodo para el caso "funciona en Chrome, falla en WebKit". Ocho pasos: nombrar el motor y la assertion que falla, reproducir con la geometria real del componente, aislar una variable por sonda, usar el mismo tipo de elemento (incluidos controles reemplazados), A/B contra el commit anterior, correr la matriz de motores del CI, medir layout esperando un frame, y provisionar el motor con `scripts/playwright-provision.sh`.

### Notes
- Los aprendizajes que la sostienen ya estaban registrados en la DB: `inset` posiciona pero no dimensiona (a11y #179), assertion fuera del guard de soporte (oss #180), medir esperando un frame (infraestructura #181).
- Las sondas reproducibles viven en `docs/pr-10517-probes/`, no en `/tmp`.
- El paso decisivo es el A/B (paso 5): "el test es muy estricto" y "rompimos algo" piden arreglos opuestos, y solo el run con el codigo viejo los separa.

---

## [2026-09-22] - Curación del catálogo: presupuesto del prompt (47k -> 17.7k chars)

### Contexto
El catálogo de skills visible al modelo excedía el presupuesto del prompt en ~2.9x. Evidencia: 126 visibles, ~47.473 chars contra el límite real de 18.000 (`DEFAULT_MAX_SKILLS_PROMPT_CHARS` en `dist/skill-prompt-limits-*.mjs`). El banner del propio prompt lo confirmaba: "included 117 of 126 (compact format, descriptions omitted)". Fuente primaria: [arXiv 2605.24050](https://arxiv.org/abs/2605.24050), "skill shadowing" degrada hasta 21 puntos de pass-rate; el costo de contexto es indistinguible de cero.

### Changed
- **26 skills del workspace ocultas del prompt** con `disable-model-invocation: true`: sin uso registrado en 2 semanas Y con más de 3 días de antigüedad. Siguen invocables con `$nombre`. Incluye las del bloque de ingeniería de Addy Osmani (api-and-interface-design, ci-cd-and-automation, context-engineering, doubt-driven-development, security-and-hardening, shipping-and-launch, etc.).
- **31 skills del workshop ocultas** por el mismo criterio.
- **11 descripciones compactadas** preservando triggers (468 -> 200 chars la más larga).

### Added
- **18 overrides en `~/.openclaw/skills/`** (managed dir) para ocultar skills bundled/custodian de OpenClaw sin editar el install: `clawhub`, `cloud-image-bake`, `configure-channel`, `control-ui`, `diagram-maker`, `gh-issues`, `healthcheck`, `meme-maker`, `node-connect`, `node-inspect-debugger`, `notion`, `python-debugpy`, `spike`, `taskflow`, `taskflow-inbox-triage`, `visualize`, `weather`. El managed dir tiene precedencia sobre bundled, así que el override no se pierde en updates.

### Removed
- **Duplicado `engram-project-memory` en el workshop** (existía en workspace y workshop con contenido distinto; el de git es el canónico).

### Resultado
- Visibles: **126 -> 53**. Presupuesto: **47.473 -> 17.713 chars** (dentro de 18.000).
- Ninguna skill perdió invocabilidad: las 74 ocultas conservan `commandVisible`/`userInvocable`, salvo las que ya lo tenían en `false` por diseño propio.

### Notes
- Backup completo del workshop: `~/.openclaw/backups/workshop-skills-20260922-2041`.
- Fuente de uso: tabla `skill_usage` en `~/.openclaw/state/openclaw.sqlite` (65 filas, tracking desde 2026-09-08).
- Lección: NO editar archivos bundled/custodian de OpenClaw (se sobrescriben en updates). Para ocultarlos, usar el managed dir `~/.openclaw/skills/`.

---

## [2026-09-22] - Limpieza: directorios huerfanos e indice sincronizado

### Removed
- **19 directorios vacios en `skills/`:** `ai`, `archive`, `automation`, `code`, `communication`, `data`, `devops`, `docs`, `document`, `graphics`, `infra`, `learning`, `operations`, `productivity`, `router.py` (directorio, no archivo), `search`, `security`, `session-context`, `test`. Todos con 0 archivos (ni `SKILL.md` ni `.gitkeep`); scaffolding de categorias que nunca se poblo. Timestamps 14:52-14:55 (19 de golpe), 18:42 (`archive`), 19:03 (`session-context`, fusionada a `session-lifecycle`). Borrados con `trash`. No estaban trackeados en git (git ignora dirs vacios).
- **24 entradas stale en `SKILLS-INDEX.md`:** apuntaban a skills ya eliminadas en la reestructuracion previa.

### Changed
- **`SKILLS-INDEX.md`:** sincronizado contra `openclaw skills list --json` (fuente `openclaw-workspace`). Total real: **60 skills** (antes declaraba 82). Se documento `publish-skills`, que existia sin figurar.
- **Mirror `.github/skills/`:** sincronizado (61 entradas, solo `_proposals` queda vacio por diseno: es el output de `scripts/post-task-reflection.sh`).

### Notes
- Verificacion de contaminacion entre fuentes: el workspace NO tiene skills mezcladas de OpenClaw. Comparadas por nombre contra bundled/custodian/plugin/workshop: la unica coincidencia es `github` (y es la propia, con metadata Kanam). Sin duplicados por contenido (md5 de los 159 `SKILL.md` del sistema).
- **13 de las 24 stale siguen existiendo en `projects/kanam-skills/skills`** (repo publico, 70 skills). Ese es un estado distinto del workspace y no se toco.
- `_proposals` se preservo: es dependencia viva de `scripts/post-task-reflection.sh --propose-skill`.

---

## [2026-09-22] - Nueva skill: engram-project-memory

### Added
- **`skills/engram-project-memory/SKILL.md`:** memoria persistente de proyecto para los agentes de pipeline (Qwen Code / Claude Code) via MCP de Engram. Documenta el protocolo: orientar antes de escribir (`mem_current_project`, `mem_context`, `mem_search`), cuando guardar con `mem_save` y su formato (What/Why/Where/Learned), topic_keys para temas que evolucionan, que nunca guardar (secrets, `.env`, output crudo de tools), handoff con `mem_session_summary` y recovery pos-compaction. Decision en ADR-052. Verificada end-to-end con `ollama launch qwen`.

### Notes
- Engram standalone v2.0.0 (`brew install gentleman-programming/tap/engram`), integrado con `engram setup qwen`. No se adopta Gentle-AI completo.

---

## [2026-09-19] - Skill consolidation Phase 1: create + delete

### Added (consolidated skills)
- **`skills/dev-inspector/SKILL.md`:** nueva skill consolidada que fusiona `code-review-and-quality`, `debugging-and-error-recovery` y `code-simplification`. Enfocada en análisis estático, calidad de código y puertas de calidad. Regla clave: "Inspect, don't rewrite".
- **`skills/focus-planner/SKILL.md`:** nueva skill consolidada que fusiona `study-tracker` y `planning-and-task-breakdown`. Enfocada en planificación de tareas, sprint planning y seguimiento de progreso. Regla clave: "Actionable first".
- **`skills/content-crafting/SKILL.md`:** nueva skill consolidada que fusiona `copy-editing`, `tech-docs` y `support-response-writer`. Enfocada en escritura, edición y pulido de contenido textual. Regla clave: "Clarity over cleverness".
- **`skills/knowledge-keeper/SKILL.md`:** nueva skill consolidada que fusiona `knowledge-management`, `memory-agent` y `memory-wiki-workflow`. Enfocada en gestión de conocimiento, recuperación de información y mantenimiento de bases de conocimiento personal. Regla clave: "Source-first".
- **`skills/gateway-manager/SKILL.md`:** nueva skill consolidada que fusiona `gateway-config` y `gateway-restart-helper`. Enfocada en descubrimiento de servicios, enrutamiento de APIs y gestión del gateway. Regla clave: "Abstraction over detail".
- **`skills/monitoring-suite/SKILL.md`:** nueva skill consolidada que fusiona `health-check-dashboard` y `observability-and-instrumentation`. Enfocada en health checks, monitoreo de disponibilidad y análisis de incidentes. Regla clave: "Signal over noise".

### Removed (zombie/redundant skills)
- **`skills/code-review-and-quality/`:** absorbida por `dev-inspector`. Eliminada del workspace (2026-09-19).
- **`skills/debugging-and-error-recovery/`:** absorbida por `dev-inspector`. Eliminada del workspace (2026-09-19).
- **`skills/code-simplification/`:** absorbida por `dev-inspector`. Eliminada del workspace (2026-09-19).
- **`skills/adhd-assistant/`:** absorbida por `focus-planner`. Eliminada del workspace (2026-09-19).
- **`skills/adhd-output/`:** absorbidas por `focus-planner`. Eliminada del workspace (2026-09-19).
- **`skills/study-tracker/`:** absorbida por `focus-planner`. Eliminada del workspace (2026-09-19).

### Why
- **Duplicidad detectada:** skills solapaban funcionalidad. `code-review-and-quality`, `debugging-and-error-recovery` y `code-simplification` solapaban en análisis estático y calidad de código. `study-tracker`, `planning-and-task-breakdown` y `adhd-assistant/adhd-output` solapaban en planificación de tareas.
- **Fase 1 (done):** se crearon las carpetas y `SKILL.md` estandarizados. Se eliminaron los zombies.
- **Fase 2 (pending):** migrar scripts duplicados, eliminar skills sin scripts propios y reentrenar `skill-router.py`.

---

## [2026-08-27] - Nueva skill: anti-ai (propuesta)

### Added
- **`skills/anti-ai/SKILL.md`:** nueva skill para eliminar el "olor a IA" de cualquier texto antes de publicarlo (posts, feedback, PRs, docs). 6 categorias de deteccion: muletillas de transicion, estructuras predecibles, adverbios de relleno, falsas precisiones, cierres genericos, y guiones largos (U+2014/U+2013). Regla base obligatoria: guion comun con escaneo `scripts/check_em_dash.py`. Integracion: paso obligatorio en el flujo de posts de LinkedIn (`docs/linkedin/linkedin-*.md`).
- **Estado:** PROPUESTA pendiente de aprobacion de Gonzo (skill_workshop `anti-ai-20260827-e07fa24549`). No aplicada aun.

### Why
- Gap detectado al comparar nuestro stack con un workflow de prompt engineering que incluia un skill Anti-AI. No existia equivalente en el workspace (copy-editing es para conversion de marketing, no para quitar modismos de IA). Gonzo lo pidio explicitamente: "el Anti AI es como mi clasico 'no guiones largos'... este lo quiero".

## [2026-08-26] - Fusion study-tracker + learning-tracker en "study-tracker"

### Changed
- **`skills/study-tracker/SKILL.md`:** reescrita por completo como "One Skill to Rule Them All". Fusiona las dos skills de estudio en una sola fuente de verdad bajo `studies/<slug>/`.
  - Aporta de la vieja study-tracker: estructura de cursos (`notes/`, `quiz/`, `exercises/`), índice maestro `studies/README.md`.
  - Aporta de learning-tracker: gamificacion (3 capas: PLAN-MAESTRO + nivel-N + PROGRESO, XP/badges/streak), modo preparacion de entrevista/JD (Input A/B, dos pasadas, URL de índice de libro).
  - Regla dura nueva: TODO estudio vive en `studies/<slug>/`. NUNCA `study/` (singular).

### Removed / Deprecated
- **`skills/learning-tracker/`:** absorbida por `study-tracker` y **eliminada** del workspace (decidido por Gonzo 2026-08-26). Quitada del SKILLS-INDEX.md. Referencias históricas en `memory/` y changelogs se mantienen como registro del cambio.

### Why
- Inconsistencia real (2026-08-26): el curso Codecademy quedó en `studies/` y el libro Packt en `study/` (singular) porque study-tracker definía `studies/` y learning-tracker era agnóstica de rutas (creó `study/` en la sesión del 25/08). La fusión elimina la ambigüedad: una skill, una ruta (`studies/`), un índice maestro.
- Migración: libro Packt movido de `study/openclaw-ai-in-production/` a `studies/openclaw-ai-in-production/`; `study/` eliminado.

### Nota de migración
- `learning-tracker` fue eliminada (2026-08-26) tras confirmar que `study-tracker` cubre todos los casos (estructura de cursos + gamificación + preparación de entrevista/JD).
