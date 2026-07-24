# SKILLS-INDEX.md — Índice de Skills

> Skills disponibles en el workspace y el sistema. Actualizado: 2026-07-22.

## ¿Qué es una skill?

Una skill es un archivo `SKILL.md` con instrucciones que le dicen al agente **cómo y cuándo usar herramientas**. OpenClaw las carga al inicio de cada sesión y las inyecta en el prompt del sistema.

**Dónde se cargan** (de mayor a menor prioridad):

| Prioridad | Fuente | Ruta |
|---|---|---|
| 1 (más alta) | Workspace skills | `<workspace>/skills/` |
| 2 | Project agent skills | `<workspace>/.agents/skills/` |
| 3 | Personal agent skills | `~/.agents/skills/` |
| 4 | Managed / local skills | `~/.openclaw/skills/` |
| 5 | Bundled skills | shipped with install |
| 6 (más baja) | Extra directories + plugins | configurable |

Si dos skills tienen el mismo nombre, gana la de mayor prioridad.

**Invocación:** las skills se cargan automáticamente en el prompt. Algunas son invocables como slash command (ej: `/weather`, `/github`). Otras son workflows que el agente activa según el contexto.

---

## Skills del Workspace

Skills propias, creadas o instaladas en `~/.openclaw/workspace/skills/`. Son workflows de ingeniería y producto.

| Skill | Descripción | Reemplaza | Cuándo usarla |
|---|---|---|---|
| **accessibility-studio** | Diseño, auditoría, autofix y validación de accesibilidad | a11y-system-designer, ux-a11y-studio | Cuando necesites auditar, diseñar o corregir accesibilidad en componentes/UI |
| **build-scaffold** | Scaffolding y construcción de proyectos | 5 skills de scaffold | Al arrancar un proyecto nuevo desde cero |
| **debug-investigation** | Investigación sistemática de bugs hasta causa raíz | — | Cuando hay un bug, degradación o comportamiento inesperado |
| **dependency-management** | Evaluación, actualización, gobernanza y salud de dependencias | — | Para auditar, actualizar o gobernar dependencias del proyecto |
| **engineering-governance** | Evolución continua del AI Engineering OS. Audita workflows, consolida aprendizajes, elimina duplicaciones | — | Para mejorar el sistema de trabajo: revisar skills, consolidar lecciones, proponer mejoras |
| **incident-response** | Gestión estructurada de incidentes en producción | — | Cuando hay un incidente en producción: detectar, responder, aprender |
| **knowledge-management** | Gobernanza, sincronización y evolución de la base de conocimiento del proyecto | — | Para mantener la documentación del proyecto sincronizada y actualizada |
| **narrative-content** | Planificación y escritura de ficción, novelas, cuentos | story-planning, story-writing | Para escribir ficción: planificar, escribir, revisar narrativa |
| **observability** | Instrumentación, métricas, tracing y análisis del sistema | — | Para agregar monitoreo, métricas o tracing a un sistema |
| **oss-contribution** | Contribución estratégica a repos externos | oss-contribute, sdd-brownfield | Para contribuir a OSS: desde el análisis hasta el PR |
| **performance-optimization** | Análisis, profiling y optimización sistemática | — | Cuando hay problemas de performance: frontend, backend, DB, infra |
| **pre-deploy-qa** | Validación pre-deploy: build, rutas, SEO, API, performance, seguridad | — | Antes de deployar: verificar que todo esté bien |
| **product-discovery** | De idea a definición de producto | 4 skills de producto | Para definir un producto desde cero: investigación, validación, especificación |
| **release-management** | Planificación, coordinación y ejecución de releases | — | Para gestionar un release: versionado, changelog, deploy, rollback |
| **research-spike** | Investigación técnica para reducir incertidumbre | — | Cuando necesitás explorar una tecnología o enfoque antes de decidir |
| **review-quality** | Revisión pre-merge y auditoría | pr-review, po-review, security-audit, agent-review | Para revisar código, PRs, o hacer auditorías de seguridad/calidad |
| **session-lifecycle** | Ciclo de vida completo de sesión | 4 skills de sesión | Para sesiones estructuradas: inicio, desarrollo, cierre, handoff |
| **task-execution** | Ejecución de tareas: planificar, implementar, verificar, PR y cerrar epic | — | Para ejecutar una tarea de principio a fin con plan y verificación |
| **tech-docs** | Documentación técnica: ADRs, README, API docs, CHANGELOG, guías | adr-framework, adr-sync | Para escribir documentación técnica estructurada |
| **vibe-code-cleanup** | Limpieza de código generado por IA/vibe coding | — | Para diagnosticar, limpiar y endurecer código generado por IA |

---

## Skills del Sistema (Bundled)

Skills que vienen con OpenClaw en `~/.nvm/versions/node/v24.18.0/lib/node_modules/openclaw/skills/`. Se cargan automáticamente si se cumplen sus dependencias (binarios, env vars, config).

### Productividad & Organización

| Skill | Descripción | Dependencias |
|---|---|---|
| **apple-notes** | Crear, ver, editar, buscar, mover notas de Apple Notes | `memo` CLI |
| **apple-reminders** | Listar, agregar, editar, completar recordatorios de Apple | `remindctl` CLI |
| **bear-notes** | Crear, buscar y gestionar notas en Bear | `grizzly` CLI |
| **obsidian** | Leer, buscar, crear, editar notas en Obsidian vaults | `obsidian` CLI |
| **notion** | Pages, Markdown, data sources, files, comments, search, Workers, API | `notion` CLI |
| **things-mac** | Gestionar Things 3: inbox, today, projects, areas, tags | `things` CLI |
| **trello** | Gestionar boards, lists y cards vía API REST | — |
| **taskflow** | Coordinar tareas multi-step como un job durable con estado, waits y subtareas | — |
| **taskflow-inbox-triage** | Patrón de ejemplo: inbox triage, routing, esperar replies, resumir | — |

### Comunicación & Social

| Skill | Descripción | Dependencias |
|---|---|---|
| **xurl** | Posts, replies, reads/search, DMs, media upload, followers, API v2 | `xurl` CLI |
| **himalaya** | Email IMAP/SMTP: list, read, search, compose, reply, forward | `himalaya` CLI |
| **gog** | Google Workspace: Gmail, Calendar, Drive, Contacts, Sheets, Docs | `gog` CLI |
| **blogwatcher** | Monitorear blogs y feeds RSS/Atom | `blogwatcher` CLI |

### Desarrollo & GitHub

| Skill | Descripción | Dependencias |
|---|---|---|
| **github** | Issues, PRs, CI/check logs, comments, reviews, releases, repos, gh api | `gh` CLI |
| **gh-issues** | Fetch issues, seleccionar candidatos, spawn fix agents, abrir PRs | `gh` CLI |
| **coding-agent** | Delegar trabajo de coding a Codex, Claude Code u OpenCode | `claude`/`codex`/`opencode` CLI (opt-in) |
| **oracle** | Second-model review/debug/refactor/design con archivos seleccionados | `oracle` CLI |
| **node-inspect-debugger** | Debug Node.js con node inspect, --inspect, breakpoints, CDP, heap | `node` |
| **python-debugpy** | Debug Python con pdb, breakpoint(), post-mortem, debugpy remoto | `python` |
| **spike** | Prototipos descartables para validar factibilidad | — |
| **skill-creator** | Crear, editar, auditar, validar o reestructurar skills y SKILL.md | — |
| **clawhub** | Buscar, instalar, verificar, actualizar, publicar skills de ClawHub | — |
| **session-logs** | Buscar y analizar session logs propios con jq | — |
| **model-usage** | Resumir costos locales de CodexBar por modelo | `codexbar` CLI |
| **summarize** | Resumir o transcribir URLs, YouTube, podcasts, artículos, PDFs | — |

### AI & Media

| Skill | Descripción | Dependencias |
|---|---|---|
| **gemini** | Gemini CLI: prompts, summaries, generation, skills, hooks, MCP | `gemini` CLI |
| **sag** | Text-to-speech con ElevenLabs (UX tipo say de macOS) | `sag` CLI |
| **sherpa-onnx-tts** | Text-to-speech local offline (sherpa-onnx) | `sherpa-onnx` |
| **openai-whisper** | Speech-to-text local con Whisper CLI | `whisper` CLI |
| **openai-whisper-api** | Transcripciones vía API de OpenAI | `curl`, API key |
| **diagram-maker** | Crear diagramas SVG/HTML o Excalidraw | — |
| **meme-maker** | Buscar templates, generar memes locales o hosted | — |
| **songsee** | Generar espectrogramas y visualizaciones de audio | `songsee` CLI |
| **video-frames** | Extraer frames o clips de videos con ffmpeg | `ffmpeg` |

### Smart Home & IoT

| Skill | Descripción | Dependencias |
|---|---|---|
| **openhue** | Controlar luces y escenas Philips Hue | `openhue` CLI |
| **sonoscli** | Controlar parlantes Sonos: discover, status, play, volume, group | `sonos` CLI |
| **eightctl** | Controlar Eight Sleep pod: status, temperatura, alarms, schedules | `eightctl` CLI |
| **camsnap** | Capturar frames o clips de cámaras RTSP/ONVIF | `ffmpeg` |
| **blucli** | BluOS CLI: discovery, playback, grouping, volume | `blu` CLI |

### Utilidades

| Skill | Descripción | Dependencias |
|---|---|---|
| **weather** | Clima actual y pronóstico (web_fetch + wttr.in) | — |
| **gifgrep** | Buscar GIFs, descargar, extraer stills/sheets | `gifgrep` CLI |
| **spotify-player** | Reproducción en terminal vía spogo o spotify_player | `spogo`/`spotify_player` |
| **ordercli** | Consultar pedidos de Foodora | `ordercli` CLI |
| **goplaces** | Google Places: text search, place details, reviews | `goplaces` CLI |
| **nano-pdf** | Editar PDFs con instrucciones en lenguaje natural | `nano-pdf` CLI |
| **1password** | 1Password CLI: sign-in, desktop integration, inject secrets | `op` CLI |
| **peekaboo** | Capturar y automatizar UI de macOS | `peekaboo` CLI |
| **healthcheck** | Auditar/hardening del host: SSH, firewall, updates, backups | — |
| **node-connect** | Diagnosticar pairing de nodos Android/iOS/macOS | — |
| **browser-automation** | Control de navegador multi-step, login, tabs, recovery | browser plugin |
| **mcporter** | Listar, configurar, llamar e inspeccionar servidores MCP | `mcporter` CLI |
| **tmux** | Controlar sesiones/paneles de tmux | `tmux` |
| **ordercli** | Consultar pedidos de delivery | `ordercli` CLI |

---

## Cómo se usan

### Workflows (workspace skills)

Se activan por contexto. Si decís "investigá este bug", Kanam activa `debug-investigation`. Si decís "prepará un release", activa `release-management`. No necesitás invocarlos explícitamente.

Algunos tienen slash commands:
- `/accessibility-studio`
- `/build-scaffold`
- `/product-discovery`
- `/research-spike`
- `/session-lifecycle`
- `/task-execution`

### Skills del sistema

Se invocan por nombre o slash command:
- `/weather` — clima
- `/github` — GitHub CLI
- `/notion` — Notion API
- `/things` — Things 3
- `/diagram` — diagramas
- `/meme` — memes
- `/summarize` — resumir URLs/videos
- `/spike` — prototipos descartables
- `/taskflow` — tareas multi-step

---

## Notas

- Las skills del workspace tienen prioridad sobre las del sistema si hay conflicto de nombres.
- Las skills se cachean al inicio de la sesión. Cambios en `SKILL.md` se refrescan mid-session vía watcher.
- Para deshabilitar una skill: `skills.entries.<name>.enabled: false` en `openclaw.json`.
- Las skills de sistema con `requires.bins` se ocultan automáticamente si el binario no está instalado.
- `coding-agent` es opt-in: hay que habilitarlo explícitamente en config.

---

## Inventario de Skills del Workspace (33 skills)

Estado al 2026-07-23. 🟢 = completa (refs + scripts) · 🟡 = warnings (faltan refs o scripts)

### Accesibilidad y UX

| Skill | Ref | Scripts | Estado |
|---|---|---|---|
| [accessibility-studio](skills/accessibility-studio/) | 3 | 3 | 🟢 |
| [copy-editing](skills/copy-editing/) | 2 | 0 | 🟡 |
| [support-response-writer](skills/support-response-writer/) | 1 | 0 | 🟡 |
| [brand-name-forge](skills/brand-name-forge/) | 0 | 0 | 🟡 |

### Desarrollo

| Skill | Ref | Scripts | Estado |
|---|---|---|---|
| [build-scaffold](skills/build-scaffold/) | 3 | 3 | 🟢 |
| [task-execution](skills/task-execution/) | 2 | 2 | 🟢 |
| [review-quality](skills/review-quality/) | 4 | 2 | 🟢 |
| [pre-deploy-qa](skills/pre-deploy-qa/) | 2 | 2 | 🟢 |
| [release-management](skills/release-management/) | 3 | 2 | 🟢 |
| [debug-investigation](skills/debug-investigation/) | 5 | 4 | 🟢 |
| [performance-optimization](skills/performance-optimization/) | 4 | 2 | 🟢 |
| [vibe-code-cleanup](skills/vibe-code-cleanup/) | 2 | 2 | 🟢 |
| [dependency-management](skills/dependency-management/) | 4 | 3 | 🟢 |
| [sql-insight](skills/sql-insight/) | 2 | 1 | 🟢 |
| [i18n-expert](skills/i18n-expert/) | 2 | 1 | 🟢 |
| [tech-docs](skills/tech-docs/) | 3 | 3 | 🟢 |

### Producto y Negocio

| Skill | Ref | Scripts | Estado |
|---|---|---|---|
| [product-discovery](skills/product-discovery/) | 4 | 4 | 🟢 |
| [research-spike](skills/research-spike/) | 3 | 2 | 🟢 |
| [saas-metrics-coach](skills/saas-metrics-coach/) | 1 | 3 | 🟢 |
| [campaign-plan](skills/campaign-plan/) | 1 | 0 | 🟡 |
| [observability](skills/observability/) | 5 | 3 | 🟢 |

### Gobernanza y Conocimiento

| Skill | Ref | Scripts | Estado |
|---|---|---|---|
| [engineering-governance](skills/engineering-governance/) | 4 | 6 | 🟢 |
| [knowledge-management](skills/knowledge-management/) | 4 | 3 | 🟢 |
| [session-lifecycle](skills/session-lifecycle/) | 2 | 2 | 🟢 |
| [incident-response](skills/incident-response/) | 4 | 3 | 🟢 |

### Carrera y Crecimiento

| Skill | Ref | Scripts | Estado |
|---|---|---|---|
| [cv-tailor](skills/cv-tailor/) | 2 | 0 | 🟡 |
| [mock-interview-drill](skills/mock-interview-drill/) | 0 | 0 | 🟡 |
| [code-mentor](skills/code-mentor/) | 0 | 0 | 🟡 |
| [dev-guide-generator](skills/dev-guide-generator/) | 0 | 0 | 🟡 |

### Contenido y Creatividad

| Skill | Ref | Scripts | Estado |
|---|---|---|---|
| [narrative-content](skills/narrative-content/) | 3 | 3 | 🟢 |
| [timeline-builder](skills/timeline-builder/) | 0 | 1 | 🟡 |
| [adhd-assistant](skills/adhd-assistant/) | 2 | 0 | 🟡 |

### Open Source

| Skill | Ref | Scripts | Estado |
|---|---|---|---|
| [oss-contribution](skills/oss-contribution/) | 3 | 3 | 🟢 |

---

**Totales:** 33 skills · 85 referencias · 55 scripts
**🟢 22 completas · 🟡 11 con warnings**

*Mantené este archivo actualizado cuando agregues/saquies skills del workspace.*
