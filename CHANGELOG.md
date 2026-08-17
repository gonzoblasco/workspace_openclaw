# CHANGELOG.md

Registro de cambios estructurales del workspace. No incluye cambios de skills (ver `skills/CHANGELOG.md`), aprendizajes (ver `docs/LEARNINGS.md`), ni actividad diaria (ver `memory/`).

---

## [2026-07-25] - Refactor AGENTS.md: single source of truth

### Changed
- **AGENTS.md:** Reducido de ~23.5 KB a ~13 KB. Metodología detallada movida a skills correspondientes. Eliminados duplicados con SOUL.md, USER.md y MEMORY.md. Agregada tabla de referencia a skills con links directos.
- **CHANGELOG.md:** Separado en raíz (cambios del workspace) y `skills/CHANGELOG.md` (cambios de skills). Eliminados aprendizajes y next steps.

---

## [2026-07-25] - Limpieza de repositorios

### Removed
- **Moderno-Access-Virtual-Plate** - eliminado de GitHub
- **antigravity-developer-stack** - eliminado de GitHub (contenido migrado a ai-developer-stack)
- **copilot-skills** - eliminado de GitHub (reemplazado por workflow-kit)
- **projects/ local:** TanStack-router, ai-developer-stack-knowledge, nomad, pro-motors, radix-ui-primitives
- **Archivados:** 11 carpetas movidas a `.archive/`

### Changed
- **MEMORY.md:** Actualizada lista de repos propios (15 total). Regla: solo mostrar repos propios, no forks.

---

## [2026-07-24] - Git Workflow Fix

### Changed
- **AGENTS.md:** Added `git pull --rebase` before push in workspace git workflow.

---

## [2026-07-23] - Skills Workspace Overhaul: 20 → 33 Skills

### Added
- 13 nuevas skills (ver `skills/CHANGELOG.md` para detalle)
- 44 reference files, 49 scripts

### Changed
- Workspace skills count: 20 → 33
- Skills mirror synced to `.github/skills/`
