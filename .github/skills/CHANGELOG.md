# SKILLS CHANGELOG.md

Registro de cambios de skills del workspace. Los cambios estructurales del workspace (no skills) van en `CHANGELOG.md` raiz; los aprendizajes en `docs/LEARNINGS.md`; la actividad diaria en `memory/`.

**Regla:** cada vez que se cree, modifique, fusione o elimine una skill, registrar aca en el mismo commit.

---

## [2026-08-26] - Fusion study-tracker + learning-tracker en "study-tracker"

### Changed
- **`skills/study-tracker/SKILL.md`:** reescrita por completo como "One Skill to Rule Them All". Fusiona las dos skills de estudio en una sola fuente de verdad bajo `studies/<slug>/`.
  - Aporta de la vieja study-tracker: estructura de cursos (`notes/`, `quiz/`, `exercises/`), indice maestro `studies/README.md`.
  - Aporta de learning-tracker: gamificacion (3 capas: PLAN-MAESTRO + nivel-N + PROGRESO, XP/badges/streak), modo preparacion de entrevista/JD (Input A/B, dos pasadas, URL de indice de libro).
  - Regla dura nueva: TODO estudio vive en `studies/<slug>/`. NUNCA `study/` (singular).

### Removed / Deprecated
- **`skills/learning-tracker/`:** absorbida por `study-tracker` y **eliminada** del workspace (decidido por Gonzo 2026-08-26). Quitada del SKILLS-INDEX.md. Referencias historicas en `memory/` y changelogs se mantienen como registro del cambio.

### Why
- Inconsistencia real (2026-08-26): el curso Codecademy quedo en `studies/` y el libro Packt en `study/` (singular) porque study-tracker definia `studies/` y learning-tracker era agnostica de rutas (creo `study/` en la sesion del 25/08). La fusion elimina la ambiguedad: una skill, una ruta (`studies/`), un indice maestro.
- Migracion: libro Packt movido de `study/openclaw-ai-in-production/` a `studies/openclaw-ai-in-production/`; `study/` eliminado.

### Nota de migracion
- `learning-tracker` fue eliminada (2026-08-26) tras confirmar que `study-tracker` cubre todos los casos (estructura de cursos + gamificacion + preparacion de entrevista/JD).
