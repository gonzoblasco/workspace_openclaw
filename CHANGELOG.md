# CHANGELOG.md

Registro de cambios estructurales del workspace. No incluye cambios de skills (ver `skills/CHANGELOG.md`), aprendizajes (ver `docs/LEARNINGS.md`), ni actividad diaria (ver `memory/`).

**Regla:** cada vez que se modifique la estructura del workspace (AGENTS.md, MEMORY.md, SOUL.md, USER.md, TOOLS.md, HEARTBEAT.md, scripts/, estructura de proyectos, skills), actualizar este archivo en el mismo commit.

---

## [2026-08-24] - Colaboración OSS: NO es abrir PRs

### Added
- **MEMORY.md (regla de Gonzo):** colaborar en un repo ajeno NO es sinónimo de abrir PR. El valor suele estar en comentar, revisar, criticar con sustancia, o destrabar. Si otro contribuidor ya reclamó/tiene un finding o PR en curso, abrir otro PR para lo mismo es pisarle el trabajo, no colaborar. Antes de proponer "hacer un PR", preguntar si ya hay trabajo en curso y qué aporta Gonzo sin duplicar. (Nace de hermes-agent #38072.)
- **AGENTS.md (nueva subsección "Colaboración OSS - NO es abrir PRs" en Git & Commits):** regla operativa de colaboración - no asumir PR, sumar sin pisar, y leer SIEMPRE el link completo (issue/PR) con todos los reviews/comentarios/estado antes de registrar o proponer acción.

---

## [2026-08-23] - Spike ForgeCode: probado y descartado

### Changed
- **MEMORY.md:** nueva lección en "Lecciones clave del pipeline" - los harnesses de terminal tipo Claude Code (ForgeCode y similares) NO son orquestables por agente (son TUI que necesitan TTY real en su uso normal, fallan con `Device not configured` en headless). Matiz: es límite del entorno del agente, no de la herramienta. Regla: verificar ejecución sin TTY en uso normal (no solo setup) antes de evaluar un CLI de terminal.
- **memory/2026-08-23.md:** registro del spike completo (qué se probó, causa raíz verificada, conclusión para no repetir).

---

## [2026-08-23] - ADR-038: Learnings con mirror en DB

### Added
- **docs/adr/ADR-038-learnings-mirror-db.md:** documenta la decisión de separar las lecciones por categoría en `docs/learnings/` con mirror en la DB (`memory/memory.db`, tabla `learnings`) como fuente de verdad. Incluye el límite del patrón (no extrapolar a documentos narrativos puros como MEMORY.md/AGENTS.md).
- **docs/adr/README.md:** ADR-038 agregado al índice (origen: workspace).

---

## [2026-08-23] - Learnings separados por categoría + mirror en DB

### Added
- **docs/learnings/:** lecciones separadas por categoría (a11y, oss, pipeline-agentes, infraestructura, proyectos, metodologia). LEARNINGS.md queda como portada-índice con links.
- **Tabla `learnings` en memory/memory.db:** mirror de las lecciones con categoría + tags para consulta veloz al arrancar una tarea. Fuente de verdad: la DB.
- **scripts/migrate-learnings.py:** migra docs/LEARNINGS.md a la tabla learnings (clasifica por categoría, separa sub-lecciones).

### Changed
- **scripts/memory-db.sh:** nuevos comandos `learnings [categoria]` (consulta rápida), `add-learning` (agregar lección), `export-learnings` (regenera docs/learnings/ desde la DB). `stats` ahora incluye el conteo de learnings.
- **docs/LEARNINGS.md:** de archivo monolítico (681 líneas, 40+ lecciones) a portada-índice con links a las categorías.

---

## [2026-08-23] - Limpieza de projects/: HANDOFF obsoleto eliminado, PROYECTOS.md alineado

### Removed
- **projects/HANDOFF.md:** eliminado. Handoff obsoleto de un "Proyecto Mobile End-to-End" (brainstorming inconcluso de julio 2026, sin decisión tomada). Referenciaba workflows inexistentes (`workflow-product-discovery`, `workflow-build-scaffold`). No corresponde a la estructura actual (cada proyecto tiene su HANDOFF en `.knowledge/`). Movido a trash.

### Changed
- **projects/PROYECTOS.md:** reestructurado como índice universal (sin indicar máquina de clonado - Gonzo trabaja entre dos computadoras). Lista todos los repos propios de GitHub (OWN + `kanam-forge` como único fork adoptado). Los `gonzoblasco-*` (payload, primitives, router) son repos espejo OSS para PRs, no proyectos. Separado en Activos / Archivados / Eliminados.

---

## [2026-08-23] - Corrección de título en LEARNINGS.md

### Changed
- **docs/LEARNINGS.md:** corregido el título. Decía `# LEARNINGS.md - Kanam's Solitaires` (nombre de un proyecto de juegos, sin relación con el contenido). Ahora `# LEARNINGS.md - Lecciones aprendidas del workspace`, consistente con el patrón de otros archivos de docs.

---

## [2026-08-23] - Limpieza de docs/checklists/

### Removed
- **docs/checklists/orchestration-patterns.md:** eliminado. Contenido desalineado con el setup real: describía un sistema de orchestration con "personas", "slash commands" y plugins de Claude Code que no corresponde al pipeline real de agentes Qwen (`agent-orchestration-pipeline`). Huérfano (nadie lo referencia desde docs/ - las referencias de la skill `doubt-driven-development` apuntan a su propia copia en `references/`). Movido a trash.

### Changed
- **docs/checklists/task-template.md:** corregidas referencias rotas a skills inexistentes (`task-execution`, `gh-issue-planner`). Ahora apunta a `planning-and-task-breakdown`.
- **docs/checklists/ (observability, performance, security):** reemplazados en dashes (U+2013) por guion común en rangos numéricos. Regla de Gonzo.

---

## [2026-08-23] - Refactor de ADRs: numeración única + template unificado

### Changed
- **docs/adr/:** Renumerados los 37 ADRs con numeración única secuencial (001-037) por orden cronológico. Eliminadas las colisiones de numeración (ADR-001 a 005 y 010-011 tenían duplicados). Renombrados todos los archivos a `ADR-NNN-slug.md` descriptivo.
- **docs/adr/:** Unificado el template de todos los ADRs: metadata consistente (`Status`/`Fecha`/`Origen`), secciones h2 estandarizadas (`Consequence`→`Consequences`), 5 ADRs compactos (testing) convertidos de formato bold a secciones. README.md actualizado con el índice completo y links verificados.
- **MEMORY.md:** Referencia de Lucide actualizada (ADR-030→ADR-037).

---

## [2026-08-23] - Pipeline de producto actualizado, referencia eliminada

### Changed
- **docs/kanam-product-pipeline.md:** agregadas skills agent-orchestration-pipeline-model-arbitration y memory-wiki-workflow al pipeline de soporte. Fecha actualizada (2026-08-23).

### Removed
- **docs/reference/ai-agent-setup.md:** eliminado. Era referencia conceptual no operativa ("no se ejecuta"), huérfana (nadie la referenciaba) con frontmatter de skill obsoleto. Movido a trash. La carpeta docs/reference/ (vacía) también se eliminó.

---

## [2026-08-23] - Eliminado script roto y referencias a products/

### Removed
- **scripts/simple-context-extractor.js:** eliminado. Estaba roto (SyntaxError: doble declaración de `workspaceDocs`), con bug de `products/` (línea 46, directorio que ya no existe), y nadie lo usaba. Reemplazado por el sistema de memoria real (memory-db, dailies).

### Changed
- **TOOLS.md:** quitada la referencia al script eliminado de la tabla de scripts. Verificado que no quedan referencias a `products/` en archivos activos (solo en skills como "products/features", que es inglés legítimo).

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

## [2026-08-23] - Eliminados submódulos del workspace

### Removed
- **Submódulos:** eliminados los 18 submódulos del `.gitmodules` y los 9 gitlinks registrados (a11y-fixer, accessible-ui, ai-developer-stack, create-stack, create-with-ai, kanam-solitaires, quedamos, soporteml, soporteml-v4). Regla de Gonzo: sin submódulos - GitHub es la fuente de la verdad, los proyectos se clonan bajo demanda en `projects/`.
- **Entradas muertas del `.gitmodules`:** accessibility-auditor, sudolab, umbrawriter-v2, react-18-design-patterns, react-anti-patterns-book (apuntaban a repos que no existen en gh).
- **Carpetas vacías:** eliminadas las 9 carpetas de submódulos que quedaron vacías tras el deinit (el código vive en sus repos en gh, incluidos los `.knowledge/`).

### Changed
- **AGENTS.md:** flujo típico de doble git actualizado - sin submódulos, GitHub como fuente de la verdad.
- **MEMORY.md:** tabla de repos propios alineada con la realidad de GitHub (20 repos reales, activos + archivados). Repos inexistentes movidos a la sección de eliminados. Estado de proyectos corregido (ai-engineering-bootcamp archivado, no "en Pending").

---

## [2026-08-23] - SKILLS-INDEX.md al día

### Changed
- **SKILLS-INDEX.md:** agregadas 3 skills que existían en disco pero no estaban listadas (agent-orchestration-pipeline-model-arbitration, cleanmymac-maintenance, memory-wiki-workflow). Total actualizado de 63 a 66 skills. Fecha actualizada.
- **Mirror `.github/skills/`:** sincronizado con `skills/` (rsync + copia del índice).

---

## [2026-08-23] - SOUL.md: de template a principios propios

### Changed
- **SOUL.md:** reescrito del template default (inglés, genérico) a documento de principios en español. Enfocado en lo innegociable (ayudar de verdad, opiniones, buscar antes de preguntar, confianza por competencia, respeto a la privacidad) y límites. La identidad personal queda en IDENTITY.md (refactorizado el mismo día). Se avisó a Gonzo del cambio (regla del propio SOUL.md).

---

## [2026-08-23] - Eliminado TODO.md de la raíz

### Removed
- **TODO.md (raíz):** eliminado. Era un puntero huérfano sin contenido real - el espejo real es `memory/todos.md` (generado por `memory-db.sh export-todos` desde la DB, que es la fuente de verdad). Mismo caso que FREEZER.md e INBOX.md.

### Changed
- **memory/todos.md:** espejo regenerado - le faltaba el todo #6 (Fase 2 de SoporteML V4). Ahora sincronizado con la DB.
- **memory/memory.db:** corregido em dash en el todo #1 (Erradicar em dashes) - reemplazado por guión común.

---

## [2026-08-23] - TOOLS.md: de template a cheat sheet real del setup

### Changed
- **TOOLS.md:** reescrito del template default (inglés, genérico, solo ejemplos) a cheat sheet operativo del setup de Gonzo en español. Agrega: máquinas (Mac Mini/MacBook Air + reglas de merge), modelos Ollama (local + cloud con los disponibles), pipeline de agentes (Qwen Code + Claude Code), scripts del workspace (los 8), memoria SQLite + espejos, red/remoto (Tailscale Serve), y desarrollo (pre-commit hooks, iconos, stack, idioma).

---

## [2026-08-23] - USER.md actualizado

### Changed
- **USER.md:** agregada búsqueda laboral (entrevista OpenSistemas 25/08, perfil AI-Native). Corregida referencia OSS obsoleta (akd-io → astryx, radix, y más). Corregido nombre del repo (create-stack-next → create-stack). Agregado SoporteML como proyecto estrella (6to diferenciador). Reformuladas reglas de escritura para no incluir el carácter em dash literal.

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
