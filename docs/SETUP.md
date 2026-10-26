# SETUP.md - Cheat Sheet del Entorno

> Migrado desde la seccion `## Tools` de `AGENTS.md` (2026-09-14) para bajar AGENTS.md bajo el limite de bootstrap (20K chars) sin perder nada. Esto es **referencia de entorno**, no reglas de conducta: las reglas viven en `AGENTS.md`, el detalle de proceso en `docs/AGENTS-DETALLE.md`, las decisiones en `docs/adr/`.
>
> **Nota:** los subagentes solo reciben `AGENTS.md` (no MEMORY.md ni este archivo). Por eso AGENTS.md conserva un resumen operativo minimo y este archivo es la referencia ampliada.

Notas específicas del entorno de Gonzo. Los detalles de los modelos/agentes en profundidad viven en `MEMORY.md` y las skills; acá está el resumen operativo para usar sin re-descubrir.

---

## Máquinas

- **Mac Mini** - unica maquina del workspace: corre el gateway de OpenClaw 24/7 y hospeda el repo. El workspace **ya no se sincroniza** con otra computadora (ADR-073).
- **Siempre `git pull --rebase` antes del push** (higiene de historial; ya no hay segunda maquina que pushee).

## Modelos (Ollama local + cloud)

<!-- BEGIN MANAGED:model-triple -->
- **Modelo de trabajo:** primario `minimax-m3.1-flash:cloud`, auxiliar `gemma4:cloud`, alternativo `glm-5.3-flash:cloud`. Thinking default: **off**.
<!-- END MANAGED:model-triple -->
<!-- BEGIN MANAGED:model-pipeline-ab -->
- **Pipeline A/B:** A escribe y corrige con `gpt-oss:120b-cloud`; B solo revisa con `deepseek-v4.1-flash:cloud` (ADR-077/ADR-088). Ruta del router: `scripts/model-router.sh model pipeline_ab`.
<!-- END MANAGED:model-pipeline-ab -->
<!-- BEGIN MANAGED:model-pipeline-abc -->
- **Pipeline A/B/C:** A escribe y corrige con `gpt-oss:120b-cloud`; B solo revisa con `deepseek-v4.1-flash:cloud`; C escribe la red de tests de regresión con `minimax-m3.1-flash:cloud` (ADR-077/ADR-088/ADR-105). Ruta del router: `scripts/model-router.sh model pipeline_abc`.
<!-- END MANAGED:model-pipeline-abc -->

> Los valores de arriba los mantiene `scripts/managed-blocks.py` desde la tabla `settings` de `memory.db`. Para cambiarlos: `managed-blocks.py set <key> <value>` y despues `apply`. No editar a mano.

- **Historial de motor y niveles:** `memory/model-history.md`. La política vigente es **ADR-090** y el bloque managed de arriba; nada en este archivo la reemplaza.
- **GLM-5.3-Flash (2026-08-29):** ex "ox-alpha". Multimodal nativo (imagen/video/PDF), ~1M contexto. Fue el motor del sistema hasta la consolidación de modelos por rol (hoy **ADR-090**); su ficha de capacidades ya no rige.
- **web_search provider:** `DuckDuckGo Search (experimental)` (key-free, no consume créditos). El provider `ollama` usaba `glm-5.2:cloud` y consumía requests del presupuesto sin pedirlo - NO usar.
- **Modelos disponibles (Ollama):**
  - Local: `qwen3-embedding:0.6b` (embeddings, 1024 dims - unico modelo de embeddings del workspace), `nomic-embed-text:latest` (768 dims, legacy: ya no se usa), `gemma4:e4b-mlx` (vision + tono/voz).
  - Cloud (estado 2026-09-29): `deepseek-v4.1-flash:cloud` (**motor del pipeline A/B**; reemplaza a `deepseek-v4-flash:cloud`, retirado por Ollama el 2026-09-25), `glm-5.3-flash:cloud` (multimodal + escalada iter 3), `glm-5.3:cloud` (escalada intra-familia), `gemma4:cloud` (vision + tono/voz), `kimi-k2.7-code:cloud` (nivel superior, iter 4), `minimax-m3:cloud` (variante costo similar a GLM, opcional), `minimax-m3.1-flash:cloud` (**primario del CORE desde 2026-10-20**; 428B, 1M ctx, vision + tools; elegido por cata de 8 roles x 5 clases - ver ADR-102). OJO: `think:false` NO apaga su razonamiento por API. FUERA del ecosistema (2026-08-30): `kimi-k3`, `deepseek-v4-pro`, `qwen3.5:cloud`, `nemotron-3-nano`, `gemma4:31b-cloud` - sacados de la config; para emergencia, restaurar desde el backup `~/.openclaw/openclaw.json.bak-20260830-pipeline-glm`

## Pipeline de agentes (programación)

- **Motor estándar (ADR-049):** Claude Code apuntando al gateway Ollama, con el modelo dinámico de Ollama. Camino recomendado (verificado 2026-09-22):
  - `ollama launch claude --model <tag> -- -p "<tarea>"` -> levanta el gateway y resuelve el enmascarado solo (verificado: `LAUNCH_OK`).
  - Alternativa headless directa: `ANTHROPIC_BASE_URL=http://127.0.0.1:11434` (o 11435) + `ANTHROPIC_AUTH_TOKEN=<cualquier valor>` + `claude -p "<tarea>" --model <modelo>`.
  - **`claude` ya está en el PATH (2026-09-22):** instalado global con `npm install -g --allow-scripts=@anthropic-ai/claude-code @anthropic-ai/claude-code`, versión 2.1.280 en `/opt/homebrew/bin/claude`. El embebido de Claude Desktop 3p (`~/Library/Application Support/Claude-3p/claude-code/<ver>/`) sigue como respaldo; ya no es el único camino.
  - **Config persistente:** `~/.claude/settings.json` acepta un bloque `env` con `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` + `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, así no hace falta exportar nada en el shell. Un install global NO hereda la config del 3p: sin ese bloque dice `Not logged in` e intenta api.anthropic.com.
  - **Aliases vs tags crudos:** los aliases (`claude-sonnet-5` -> deepseek-v4.1-flash:cloud) viven en `~/.ollama/config.json` (`integrations.claude-desktop.aliases`, editables desde la app de Ollama) y los resuelve el **gateway 11435**, que requiere Claude Desktop corriendo. El **daemon 11434** solo acepta tags crudos. Usar `ollama launch claude` evita tener que elegir a mano.
  - Requiere Claude Code >= 2.x (la 0.2.18 no maneja el bloque thinking de los modelos de razonamiento).
  - Warnings de `unrecognized_model` por modelos custom = ruido, no bloquean.
- **Qwen Code:** queda como fallback o segundo par de ojos, no como estandar (ADR-049). Para SIGKILL/sesiones largas, Claude maneja mejor que Qwen.
- **El modelo que carga el harness** se elige por tipo de tarea (ver `scripts/model-router.sh`). La política vigente de niveles de pensamiento y asignación de modelo por rol es **ADR-090** (cata 2026-10-06).
- **Claude Code ignora AGENTS.md** (verificado ADR-049): no lo lee en absoluto. Cada directorio raiz de proyecto (y el workspace) lleva el **PAR** `AGENTS.md` (fuente de verdad, reglas especializadas del proyecto) + `CLAUDE.md` espejo que hace `@import` de ese `AGENTS.md` (lo dirige, no lo reemplaza). Verificado: el par del proyecto gana sobre el de la raiz cuando el cwd esta dentro del proyecto. Se crea el par cuando un proyecto entra al flujo de pipeline; hoy estan la raiz y kanam-fixer (piloto).
- Detalle en la skill `agent-orchestration-pipeline` (que aun no refleja ADR-049; al tocarla, alinearla).

## Scripts del workspace

| Script | Uso |
|---|---|
| `scripts/memory-db.sh` | DB de memoria: `export-all`, `export-todos`, `export-inbox`, `export-oss`, `add-todo`, `add-inbox`, `export-daily`, `stats`, `catalog` (cataloga memoria en DB relacional + embeddings), `search "<query>" [n]` (busqueda semantica), `topics`, `recent [n]` |
| `scripts/memory-catalog-v2.py` | Cataloga dailies en DB relacional + embeddings semanticos (Ollama `qwen3-embedding:0.6b`, 1024 dims). Idempotente (upsert por date). Puebla sessions_relacional, session_vectors, topics, topic_sessions, learnings_enriquecido |
| `scripts/memory-search.py` | Busqueda semantica sobre la memoria: query -> embedding -> cosine similarity -> top N sesiones. Flags: `--topics`, `--recent [n]` |
| `scripts/memory-topics.py` | Descubre topics emergentes via K-means clustering sobre embeddings + recalcula topics fijos por keywords. Flags: `--refresh`, `--list`. Comandos memory-db: `topics-cluster`, `topics-list` |
| `scripts/memory-end-session.py` | Guarda el cierre de sesion DB-first: escribe directo a `daily_notes` (fuente de verdad) y regenera `memory/YYYY-MM-DD.md` como vista. Idempotente (no duplica por proyecto/fecha). Desde 2026-09-14 trae guard de reconciliacion: si el `.md` tiene secciones que la DB no, las mergea antes del export y respalda el `.md` en `/tmp`; `--no-reconcile` reproduce el comportamiento viejo. Integrado en session-end.sh |
| `scripts/semantic-search.js` | Busqueda semantica RAG-lite sobre `memory.db` (CLI legible). Uso: `node scripts/semantic-search.js "consulta"`. Requiere Ollama (`qwen3-embedding:0.6b`). |
| `scripts/memory-reembed.py` | Repara vectores cuyo dim no coincide con el modelo actual (fallbacks SHA-256 de 32 dims, o vectores de un modelo viejo). Sin fallback propio: si Ollama falla no escribe nada. Uso: `./scripts/memory-reembed.py [--dry-run] [--limit N]` |
| `scripts/semantic-search-json.js` | Version JSON de la busqueda semantica para integracion con herramientas/agentes. Uso: `node scripts/semantic-search-json.js "consulta" [topN]`. Retorna `{query, results:[{score, sessionId, title, text}]}`. |
| `scripts/check-adr-integrity.py` | Verifica que el corpus de ADRs y su indice esten reconciliados: ADR en disco sin fila, fila sin archivo, numero duplicado, ref cruzada rota. Los huecos de numeracion son informativos. Corre en el pre-commit cuando hay markdown staged. |
| `scripts/changelog-rotate.py` | Mantiene `docs/CHANGELOG.md` en una ventana activa de ~14 dias (ADR-092); lo viejo se acumula en `docs/archive/CHANGELOG-archive.md`. Idempotente. `--check` (exit 1 si hay drift) lo corre el pre-commit cuando el CHANGELOG esta staged; el cierre de sesion (`session-end.sh`) rota sin flags. Flags: `--days N`, `--dry-run`, `--today` (tests). |
| `scripts/dreams-rotate.py` | Mantiene `DREAMS.md` (Dream Diary del plugin `memory-core`, append-only) en el mes en curso; los meses viejos se archivan por mes en `memory/archive/dreaming/DREAMS-YYYY-MM.md`. Idempotente; solo toca el contenido entre los marcadores del diary. Sin gate en pre-commit (DREAMS.md esta gitignored); lo rota el cierre de sesion. Flags: `--check`, `--dry-run`, `--today`. |
| `scripts/security-scan.py` | Gate de seguridad (Kanam OS Etapa 2, ADOPTADO 2026-10-06). Escanea codigo/scripts contra patrones de riesgo (inyeccion, path traversal, ofuscacion, exfiltracion, secret leaks, prompt override). Modo gate: `--staged` escanea solo el codigo ejecutable staged bajo un arbol de skills (lo corre el pre-commit); el modo `<path>` sigue para uso manual. |
| `scripts/init-project.sh` | Scaffold de proyecto: crea `projects/<slug>/.knowledge/` + repo en gh (privado por defecto). **Deuda (2026-10-13):** todavia referencia la capa "agregado" (`projects_openclaw`) y el modelo de blob en el workspace, ambos retirados (ADR-098); su `git add projects/<slug>/.knowledge` aborta porque `/projects/` esta gitignoreado. No usar para un proyecto nuevo hasta reworkearlo. |
| `scripts/aggregate-sync.sh` | **RETIRADO (2026-10-13, ADR-098):** sincronizaba el repo agregado `projects_openclaw`, que no existe. `projects/` es carpeta plana ignorada; no hay capa agregada. |
| `scripts/initial-setup.sh` | Setup one-shot para maquina nueva (laptop/Mac nuevo): clona workspace + clona/attacha los subrepos en `projects/<slug>/` + verifica. **Deuda (2026-10-13):** su paso 2 todavia arma `projects/` como clon del agregado `projects_openclaw` (retirado, ADR-098); alinear al modelo sin capa agregada. |
| `scripts/oss-tracker.js` | Tracker de contribuciones OSS |
| `scripts/onyx-tool.py` | Onyx: `status` (sonda HTTP real), `up`, `down` (conserva volumenes), `restart`, `logs`, `provider`, `chat` (prueba de ida y vuelta al LLM), `json` |
| `scripts/cline-tool.sh` | Cline: `up` (dashboard + daemon, idempotente), `down`, `status` (puertos + salud HTTP), `run --cwd <dir> "<prompt>"` (turno headless), `logs` |
| `scripts/ai-toolbox.py` | Registro vivo de las herramientas IA de la maquina: `list` (estado real), `list --json`, `status <id>`, `health`, `up/down/restart <id>`, `catalog --write/--check`. Ver skill `ai-toolbox` |
| `scripts/pr-dashboard.sh` | Dashboard de PRs (para el batch check del ritual de inicio de sesión) |
| `scripts/github-pr-risk.sh` | Detector de risk signals de un PR (schema/auth/deps/API/secrets) + preguntas de review. Uso bajo demanda en el cross-review del pipeline. Portado del plugin github-workflow. Solo lectura |
| `scripts/safe-fetch.sh` | URL pre-flight check local antes de web_fetch: esquema https, typosquatting de dominios confiables, payload prompt injection. Exit: 0 ALLOW / 1 DENY / 2 CAUTION. Portado del concepto PreClick, 100% local |
| `scripts/skill-router.py` | Sugiere que skill usar para una tarea (matching local keyword + embeddings Ollama `qwen3-embedding:0.6b`). Portado del concepto skill-ai-inject. Uso: `skill-router.py "<tarea>"` |
| `scripts/project-closure.sh` | Cierra/immortaliza un proyecto terminado: crea ADR template, registra en memory.db (daily_notes + sessions_relacional), devuelve resumen para daily. Reproducible. Uso: `--name <slug> --title <t> --summary <s> [--complexity T] [--model m] [--tag t] [--create-adr]`. Skill: `project-closure` |
| `scripts/pipeline-track.sh` | Estado durable del pipeline A/B: init/start/review/done/status/resume/note. Sobrevive a SIGKILL/restarts (crash recovery). Portado del concepto Pipeline Architect. Acepta `--score T` en init (integrado con complexity-scorer) |
| `scripts/complexity-scorer.sh` | Evalua objetivo en 4 dimensiones (A/B/C/D), devuelve T-score 1-20 + bucket + modelo + thinking. Prueba gemma4:e4b-mlx local primero (6.7x mas rapido que qwen3.5), luego fallbacks cloud. `--score T` para forzar. T>=17 requiere confirmacion de Gonzo. Cablea complexity-driven-pipeline. Parser externo: `scripts/complexity-parse.py`. Integrado en `skills/session-lifecycle/scripts/session-start.sh` (corre al iniciar sesion y persiste T en el log) |
| `scripts/pdf-tool.sh` | Toolkit PDF/OCR local: text, info, pages, search, ocr (tesseract), pdfimages, md2pdf (exportar MD a PDF). 100% local. Requiere poppler + tesseract + npx (brew). Portado de la familia PDF/OCR de ClawHub |
| `scripts/model-router.sh` | Router de modelo Ollama por tipo de tarea (code/review/long/cheap/writing/pipeline_ab) + overrides sticky. La asignación A/B vigente la declara el bloque managed de `AGENTS.md`; el fundamento es ADR-077/ADR-089. Consulta `model <tipo>` para decidir el `--model`. Portado del concepto ToggleLogic sin licencia |
| `scripts/task-notify.sh` | Notificacion desktop macOS cuando un agente termina tarea. Uso en pipeline A/B. Portado del concepto Task Notifier |
| `scripts/pre-commit.template` | Template de pre-commit hooks (lint → test → build) |
| `scripts/test-skills.sh` | Verifica que las skills estén bien formadas |

## Memoria (SQLite + espejos)

- **Fuente de verdad:** la declara `AGENTS.md` (sección Tools); acá solo se listan los espejos.
- **Busqueda semantica (2026-08-30):** `session_vectors` con embeddings reales de Ollama (**1024 dims**, `qwen3-embedding:0.6b`) + `chunk_text`. Usar `scripts/semantic-search-json.js` para recuperar sesiones por significado. Re-catalogar con `scripts/memory-catalog-simple.sh` si se agregan dailies nuevos.
- **Espejos MD** (regenerar con `./scripts/memory-db.sh export-all`):
  - `memory/todos.md` ← tabla todos
  - `memory/inbox.md` ← tabla inbox
  - `docs/OSS-TRACKER.md` ← tabla contributions
- **Dailies:** viven en `memory/YYYY-MM-DD.md`; los viejos se archivan a la DB + `memory/archive/dailies/` (consolidados) y `memory/archive/sessions/` (logs con hora).

### Regla: DB-first vs doc-only (2026-09-24)

La memoria del workspace tiene **dos clases de superficie**, y confundirlas lleva a buscar en el lugar equivocado o a esperar un export que no existe. La distincion se reconstruyo a mano el 2026-09-24 (pregunta de Gonzo): vale tenerla explicita.

**1. DB-first (dentro del ciclo de `memory.db`):** el dato vive en la DB y el markdown es una **vista regenerable**. Si el `.md` y la DB discrepan, gana la DB.

| Documento | Tabla | Direccion |
|---|---|---|
| `memory/YYYY-MM-DD.md` (dailies) | `daily_notes` | ambos sentidos (el guardado reconcilia `.md` -> DB, y `export-daily` regenera) |
| `memory/todos.md` | `todos` | DB -> MD |
| `memory/inbox.md` | `inbox` | DB -> MD |
| `docs/OSS-TRACKER.md` | `contributions` | DB -> MD |
| `docs/learnings/*.md` | `learnings` | DB -> MD (portada `docs/learnings/README.md`) |

**2. Doc-only (fuera del ciclo):** el archivo **es** la fuente de verdad. No hay tabla, no hay export, no hay reconciliacion. Editarlo mal no se detecta contra nada.

`MEMORY.md`, `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `docs/NORTH.md`, `docs/ROADMAP.md`, `docs/AGENTS-DETALLE.md`, **el corpus de ADRs (`docs/adr/`)** y el resto de `docs/`.

**El caso de los ADR:** no hay tabla `adr` ni `decision`, y los ADR no se exportan ni se indexan como entidad. Solo aparecen en la DB como **texto incidental** (alguien los *nombra* en un daily, una sesion o una leccion), nunca como registro consultable. Consecuencia practica: para auditar el corpus hay que leer los archivos, no consultar la DB. El camino a un almacen de conocimiento para ADRs es el **wiki** (`openclaw wiki ingest`), no `memory.db`.

**Regla practica:** antes de buscar un dato, decidir si es DB-first o doc-only. Si es doc-only y se quiere consulta rapida, el camino es ingesta explicita (wiki) o indexacion, nunca asumir que un `export-*` lo va a regenerar.

### Engram (memoria de proyecto para agentes, 2026-09-22)

- **Binario:** `engram 2.0.0` (brew install gentleman-programming/tap/engram). Store: `~/.engram/engram.db`. Config Qwen: `~/.qwen/settings.json` (mcpServers.engram) + `~/.qwen/QWEN.md` (protocolo con markers).
- **Proposito:** memoria persistente para agentes del pipeline A/B (Qwen Code) que hoy arrancan de cero. Kanam usa `memory.db` (personal); Engram es memoria **de proyecto** compartida via MCP.
- **Nunca en Engram:** secrets, `.env`, tokens, datos personales, output crudo de tools.
- **Politica sync:** workspace NUNCA commitea `.engram/`; proyectos con equipo decide por ADR.
- **Comandos:** `engram doctor` (health check), `engram search`, `engram tui`, `engram projects list`.
- **Skill:** proposal `engram-project-memory-20260922-aebbba7411` pendiente de apply.

## Onyx (self-hosted, LLM via Ollama) - 2026-10-20

- **Repo:** `projects/onyx` (clone de `github.com/onyx-dot-app/onyx`). UI: **http://localhost:3000**.
- **Que es:** capa de contexto/RAG de equipo (OSS, MIT). Chat con memoria, agents, MCP server y sandbox de codigo.
- **Script:** `scripts/onyx-tool.py` (status, up, down, restart, logs, provider, chat).
  ```bash
  ./scripts/onyx-tool.py status      # estado real (sonda HTTP, no del container)
  ./scripts/onyx-tool.py up          # levantar (modo Lite)
  ./scripts/onyx-tool.py down        # parar (conserva volumenes)
  ./scripts/onyx-tool.py provider    # provider y modelo default
  ./scripts/onyx-tool.py chat        # prueba de ida y vuelta al LLM
  ```
- **Modo Lite:** 6 servicios (api_server, web_server, nginx, relational_db, mcp_server, code-interpreter), **~1 GB RAM**. Sin OpenSearch, sin Redis, sin model servers: Postgres hace de cache, file store y auth backend.
- **Por que Lite:** Docker Desktop tiene **8 GB de RAM asignados** (no los 24 GB de la maquina) y conviven otros stacks. El stack completo (OpenSearch con heap de 2 GB + 2 model servers con torch) no entra comodo. Un `docker compose up` a secas levanta el stack completo: hay que usar el script o los dos `-f` en orden.
- **LLM:** provider `ollama_chat` con `api_base=http://host.docker.internal:11434` (el Ollama del host, no un container). **Solo modelos cloud** (17 visibles), default `minimax-m3.1-flash:cloud`. Los modelos locales del host no estan en el provider: Onyx no los elige y no consumen RAM.
- **Credenciales:** `projects/onyx/.local/credentials.md` (excluido de git, NO versionar).
- **Estado y fricciones medidas:** `projects/onyx/.knowledge/STATUS.md`.
- **Trampas verificadas (no volver a tropezar):**
  - El email de registro **no puede usar dominio `.local`** (`email_validator` lo rechaza -> 422). Usar un dominio real.
  - El **login tarda 15-80 s** (bcrypt con la CPU de Docker saturada): los timeouts cortos cortan un login que si iba a completarse.
  - `DOCKER_SOCK_PATH=/Users/gonzoblasco/.docker/run/docker.sock` en `.env` (en macOS no existe `/var/run/docker.sock`).
  - `code-interpreter` puede marcar `unhealthy` por timeout del `docker image inspect` con el daemon saturado: se recupera solo.
  - `api_server` fue OOM-killed una vez (exit 137) por los containers ajenos: reinicia solo (`restart: unless-stopped`).
  - El tag de un modelo **no dice si es cloud**: el sufijo `:cloud` no alcanza (`gpt-oss:120b-cloud` y `mistral-large-3:675b-cloud` son cloud sin el). La fuente de verdad es el campo `remote_host` de `GET /api/tags`.
- **Lo que falta:** indexacion/RAG/conectores apagados en Lite. Para activarlos: embeddings por `litellm` contra el endpoint OpenAI-compatible de Ollama (`/v1/embeddings`, verificado con `qwen3-embedding:0.6b`, dim 1024) + stack completo con Redis y OpenSearch.

## Cline (agente de codigo open source) - 2026-10-20

- **Repo:** `projects/cline` (clone shallow de `github.com/cline/cline`, `main` @ `0870796`). Es upstream: no se commitea ni se pushea. Lo propio va en `projects/cline/LOCAL-SETUP.md`.
- **Que es:** agente de codigo con tres superficies: CLI (`cline`), Hub dashboard (web) y SDK. El dashboard es la UI; el daemon del hub ejecuta las sesiones.
- **Toolchain:** **Bun 1.4.2** (el repo prohibe npm/yarn/pnpm). `build:sdk` es obligatorio: los paquetes del SDK se referencian entre si por `dist/`, sin condition `development`.
- **Provider:** `ollama` contra `http://localhost:11434` (API **nativa** `/api/chat`, no `/v1`: el path OpenAI-compatible ignora `options.num_ctx` y todo modelo cargaria con 4096 tokens). Modelo por defecto `minimax-m3.1-flash:cloud`.
- **UI:** http://127.0.0.1:8787 - dashboard. **El chat del agente esta en `/chat`**, no en la home (`/` es el monitor del hub y no tiene composer).
- **Script:** `scripts/cline-tool.sh` (`up`, `down`, `status`, `run --cwd <dir> "<prompt>"`, `logs`).
  ```bash
  ./scripts/cline-tool.sh up          # dashboard + daemon (idempotente)
  ./scripts/cline-tool.sh status      # puertos, salud HTTP, config, workspace
  ./scripts/cline-tool.sh down        # parar (conserva config y sesiones)
  ./scripts/cline-tool.sh run --cwd <dir> "<prompt>"   # un turno headless
  ```
- **Config aislada:** `CLINE_DIR=projects/cline/.cline-local`. La config real del usuario (`~/.cline`, con su sesion OAuth de Cline) **no se toca**.
- **Registro:** entrada `cline` en `scripts/ai-toolbox.py` + ficha en `docs/tools/REGISTRY.md`.
- **Trampas verificadas (no volver a tropezar):**
  - Son **DOS procesos**: el dashboard (`:8787`, UI) y el daemon del hub (`:25466`, quien ejecuta las sesiones). Parar el dashboard no para el daemon.
  - El workspace del chat **no** sale de `WORKSPACE_ROOT` sino de la sesion mas reciente que el Hub conoce (`apps/cline-hub/src/server/providers.ts:38`). Si ya hay sesiones, su cwd gana. Para cambiar de proyecto: borrar las sesiones (UI: Sessions -> eliminar) y reiniciar.
  - `ENOENT: posix_spawn '/bin/bash'` **no** significa que falte el shell: `/bin/bash` existe. Lo que falta es el **cwd** de la sesion (un `posix_spawn` con cwd inexistente reporta ENOENT). El agente lo interpreta como "no hay shell" y deja de usar la terminal.
  - Las tools se auto-aprueban por default (`autoApproveTools` en `true`): el agente ejecuta comandos sin preguntar.
  - Los modelos descubiertos en Ollama vienen sin `contextWindow`, asi que Cline usa su default de **32768** (`OLLAMA_DEFAULT_CONTEXT_WINDOW`).

## Red / remoto

- **Canal remoto (2026-09-07, migrado desde USER.md el 2026-10-06):** bot de Telegram @kanam_ai_bot (DM, allowFrom user ID 7921100122). Reemplaza Tailscale Serve + PWA; solo el /dashboard requiere Tailscale. Telegram se migro Air -> Mini el 08/09 y vive solo aca.
- **Gateway 24/7 (2026-09-08):** corre como servidor fijo en la Mac Mini (LaunchAgent cargado).
- **Webchat remoto (historico):** Tailscale Serve + PWA en iPhone; sin app nativa iOS, device pairing la primera vez. Reemplazado por Telegram.
- **OpenClaw Control UI:** requiere secure context (HTTPS o localhost) - Tailscale Serve lo resuelve.
- **Cron de refresh token MeLi (SoporteML v4):** cron OpenClaw `soporteml-meli-token-refresh` dispara `POST /meli/refresh-token` en `localhost:3001` cada 5h (access tokens de MeLi duran ~6h). Credenciales admin: userId `521a68d2-f0dd-48c7-94fb-a07c7afccbc0` + companyId `4dd8ea5d-f1e5-4bd6-a59d-6f9bc4656798`. Si se reconecta OAuth con empresa nueva, actualizar el cron. Solo corre con el backend levantado.

---

_Actualizado 2026-10-06 (migrado desde AGENTS.md el 2026-09-14). Si algo cambia en el setup, actualizá este archivo - es mi cheat sheet._
