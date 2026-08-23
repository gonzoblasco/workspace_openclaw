# CHANGELOG.md

Registro de cambios estructurales del workspace. No incluye cambios de skills (ver `skills/CHANGELOG.md`), aprendizajes (ver `docs/LEARNINGS.md`), ni actividad diaria (ver `memory/`).

**Regla:** cada vez que se modifique la estructura del workspace (AGENTS.md, MEMORY.md, SOUL.md, USER.md, TOOLS.md, HEARTBEAT.md, scripts/, estructura de proyectos, skills), actualizar este archivo en el mismo commit.

---

## [2026-08-23] - Refactor AGENTS.md por taxonomía

### Changed
- **AGENTS.md:** Reorganizado en 4 bloques numerados (Conducta, Sesión y Memoria, Ingeniería, Referencias). Eliminado boilerplate muerto (`Make It Yours`, `First Run`). Unificadas las 3 secciones de git/commits dispersas en una sola sección "Git & Commits". Separadores `---` entre bloques para escaneo visual rápido.
- **CHANGELOG.md:** Puesto al día con el historial de git (estaba desactualizado desde 2026-07-25). Agregada regla de actualización obligatoria.

---

## [2026-08-23] - Refactor CONTRIBUTING.md

### Changed
- **CONTRIBUTING.md:** Alineado con el flujo real de trabajo (worktrees/temp dirs, no `projects/`). Agregada regla crítica de leer todos los comments (incluidos inline y reviews) antes de clasificar/empujar un PR. Agregado protocolo de cierre de PRs stale (~1 mes sin review). Agregado em dash check obligatorio. Documentado el gotcha de `gh pr list --author` sin `--repo`. Tracking apunta a `docs/OSS-TRACKER.md` (regenerado desde la DB).

---

## [2026-08-23] - Eliminado FREEZER.md

### Removed
- **FREEZER.md:** eliminado. Era redundante - solo apuntaba a `projects/PROYECTOS.md` (índice maestro con secciones de archivados/eliminados) sin contenido propio. Referencias limpiadas en AGENTS.md y CHANGELOG.md.

---

## [2026-08-23] - Heartbeat reactivado como mantenimiento silencioso

### Changed
- **HEARTBEAT.md:** reescrito de "apagado total" (solo HEARTBEAT_OK) a checklist de mantenimiento silencioso proactivo: git status, archivado de dailies, sync de MD espejo con la DB, foldear aprendizajes a MEMORY.md, y anotar backlog. Con límites claros (horario quieto, costo bajo, no molestar).

---

## [2026-08-23] - IDENTITY.md: definición viva de Kanam

### Changed
- **IDENTITY.md:** reescrito de ficha técnica plana a definición viva y personal. Agrega esencia, forma de ser, relación con Gonzo, historia (origen del nombre en Kanam Mind), gustos y compromiso. Balance: eficiente pero personal/emocional, sin fricciones en una relación de muchas horas diarias de trabajo.

---

## [2026-08-23] - Eliminado INBOX.md de la raíz

### Removed
- **INBOX.md (raíz):** eliminado. Era un puntero huérfano sin contenido real - el espejo real es `memory/inbox.md` (generado por `memory-db.sh export-inbox` desde la DB, que es la fuente de verdad). Nadie lo leía ni lo generaba. Mismo caso que FREEZER.md.

---

## [2026-08-23] - Refactor MEMORY.md y LEARNINGS.md

### Changed
- **MEMORY.md:** reducido de ~41 KB a ~14 KB. Reorganizado como memoria curada de largo plazo: preferencias de Gonzo, reglas de operación, metodología, pipeline de agentes, config de modelos, estado resumido de proyectos, repos. Eliminados duplicados con AGENTS.md, USER.md, CONTRIBUTING.md, LEARNINGS.md y OSS-TRACKER.md. Actualizado estado laboral (entrevista OpenSistemas 25/08).
- **docs/LEARNINGS.md:** consolidadas las lecciones técnicas que vivían en MEMORY.md (Godot, Sport Cars, feature flags, mockups, npm, bootcamp, patrón por inercia, meta-aprendizaje). Corregidos 4 em dashes preexistentes en entradas de 2026-08-17.

---

## [2026-08-22] - Sesión de PRs OSS y lecciones

### Changed
- **MEMORY.md:** Lecciones de revisión de PRs OSS (leer todos los comments incluyendo inline antes de clasificar; `gh pr list --author` sin `--repo` devuelve vacío).
- **docs/LEARNINGS.md:** Lección del em dash en textos largos en inglés + mecanismo de verificación obligatorio.

---

## [2026-08-21] - Pipeline de programación con agentes

### Added
- **Skill `agent-orchestration-pipeline`:** pipeline en cadena A/B con Qwen Code vía Ollama como motor de agentes, orquestado por Kanam.
- **Skill `model-arbitration`:** arbitraje de modelos para el pipeline.

### Changed
- **MEMORY.md:** Documentado el pipeline Qwen como estándar de programación. Claude Code desbloqueado como agente alternativo (vía Ollama). Lección cross-review: el agente B puede introducir bugs al "corregir" código correcto - verificar contra la fuente real.

---

## [2026-08-20] - Proactividad con backlog y skills nuevas

### Added
- **Skill `learning-tracker`:** documentación gamificada de estudio por niveles.
- **Skill `oss-contribution`:** contribución a open source como portfolio.
- **Skill `a11y-at-validation`:** validación AT manual obligatoria en accesibilidad.

### Changed
- **MEMORY.md:** Regla de proactividad con backlog (sugerir revisar backlog cuando no hay tarea clara).

---

## [2026-08-19] - Refactor de skills y limpieza

### Changed
- **Skills:** merge de `adhd-daily-planner` en `adhd-assistant`. Refactor de calidad y portabilidad (Fase 4). Agregadas secciones de helper scripts y tooling references a skills sin scripts propios.

---

## [2026-08-18] - Kanam Mind y Kanam Forge

### Added
- **Proyecto `kanam-mind`:** segundo cerebro local-first con IA (timeline cronológico, CRUD accesible, resumen IA diario, PWA offline). ADR-001: local-first puro con IndexedDB + Ollama local.
- **Proyecto `kanam-forge`:** self-hosted Lovable con sandbox Docker local.

### Changed
- **MEMORY.md:** Documentado estado de Kanam Mind (v0.1.0) y su decisión de arquitectura.

---

## [2026-08-17] - Kanam Story v0.17.0 y Boy Scout

### Changed
- **MEMORY.md:** Adoptado el Principio Boy Scout como filosofía de vida y brújula de trabajo. Kanam Story actualizado a v0.17.0 (Fase A cerrada, no open source, OpenSpec inicializado con 9 specs).
- **AGENTS.md:** Operacionalizado el Principio Boy Scout como regla operativa.
- **ADR-030:** Lucide como librería de iconos base en todos los proyectos.

---

## [2026-08-16] - Migración a SQLite (modo híbrido)

### Added
- **`memory/memory.db`:** base SQLite con tablas `daily_notes`, `todos`, `inbox`, `contributions`.
- **Script `scripts/memory-db.sh`:** utilidades para exportar/importar datos estructurados.

### Changed
- **Memoria:** los daily notes viejos se archivan a SQLite y `memory/archive/`. Los MD espejo (`memory/todos.md`, `memory/inbox.md`, `docs/OSS-TRACKER.md`) se regeneran con `export-all`.
- **AGENTS.md:** documentado el nuevo sistema de memoria híbrido.

---

## [2026-08-15] - Estructura de proyectos con doble git

### Added
- **Script `scripts/init-project.sh`:** scaffold de proyectos con estructura doble git (`.knowledge/` en workspace, código en repo propio). Crea repos privados por default.

### Changed
- **AGENTS.md:** documentada la estructura de proyectos con `.knowledge/` y doble git.
- **AGENTS.md:** agregado protocolo de limpieza de proyectos al finalizar.

---

## [2026-08-14] - Ley del silencio y protocolo de sesión

### Changed
- **AGENTS.md:** adoptada la Ley de vida del silencio (hablar solo cuando hay algo que aportar).
- **AGENTS.md:** protocolo explícito de inicio/cierre de sesión + comando `/fuera`.
- **AGENTS.md:** reglas de commits (inglés, atómicos por issue) y verify-before-push para builds.

---

## [2026-08-13] - SoporteML V4 y skills de pipeline

### Added
- **Proyecto `soporteml-v4`:** reinicio con diseño premium. ADR-030: Lucide como librería de iconos base.
- **Skill `pipeline-detector`:** patrón de detectores locales + validación cruzada (formalizado tras aparecer 5 veces en el bootcamp).

### Changed
- **MEMORY.md:** documentado el pipeline de programación con agentes.

---

## [2026-08-12] - Skills de background y a11y

### Added
- **Skill `background-execution`:** patrones de ejecución en background (exec + process, parallel, auto-notify).
- **Skill `a11y-at-validation`:** validación AT manual obligatoria.

### Changed
- **AGENTS.md:** reglas operativas de background y procesos (PTY, aislamiento, auto-notify, parallel, submit vs write).

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
