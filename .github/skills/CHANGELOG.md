# SKILLS CHANGELOG.md

Registro de cambios de skills del workspace. Los cambios estructurales del workspace (no skills) van en `CHANGELOG.md` raiz; los aprendizajes en `docs/LEARNINGS.md`; la actividad diaria en `memory/`.

**Regla:** cada vez que se cree, modifique, fusione o elimine una skill, registrar aca en el mismo commit.

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
