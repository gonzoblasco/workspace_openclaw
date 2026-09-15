# SETUP.md - Cheat Sheet del Entorno

> Migrado desde la seccion `## Tools` de `AGENTS.md` (2026-09-14) para bajar AGENTS.md bajo el limite de bootstrap (20K chars) sin perder nada. Esto es **referencia de entorno**, no reglas de conducta: las reglas viven en `AGENTS.md`, el detalle de proceso en `docs/AGENTS-DETALLE.md`, las decisiones en `docs/adr/`.
>
> **Nota:** los subagentes solo reciben `AGENTS.md` (no MEMORY.md ni este archivo). Por eso AGENTS.md conserva un resumen operativo minimo y este archivo es la referencia ampliada.

Notas específicas del entorno de Gonzo. Los detalles de los modelos/agentes en profundidad viven en `MEMORY.md` y las skills; acá está el resumen operativo para usar sin re-descubrir.

---

## Máquinas

- **Mac Mini** - máquina principal (donde corre el gateway de OpenClaw por defecto).
- **MacBook Air** - segunda máquina, misma config. Workspace sincronizado por git.
- **Regla de merge:** cuando venga algo del workspace (pull/rebase con conflictos), hacer merge, no reset. El soft reset descarta commits de la otra máquina.
- **Siempre `git pull --rebase` antes del push** (evita pisar cambios de la otra máquina).

## Modelos (Ollama local + cloud)

- **Modelo de trabajo (2026-08-30):** Default de OpenClaw: `deepseek-v4-flash:cloud` (revert 2026-08-30, decisión explícita de Gonzo: la diferencia de calidad vs GLM 5.3 Flash es muchísima). Kanam en thinking **max**; agentes A/B del pipeline SIEMPRE en **high** con `deepseek-v4-flash:cloud`. Config: `agents.defaults.thinkingDefault = "max"`. Pipeline en cadena A/B: Kanam planifica en max, agentes ejecutan en high. Regla de niveles: agentes de codigo siempre high, max solo para diseño dificil puntual (el max no fue driver de calidad en la comparativa; DeepSeek en max filosofa, ADR-040).
- **GLM-5.3-Flash (2026-08-29):** primer GLM nativamente multimodal: imagen, video y archivos (PDFs) como input. 1M de contexto, 131k output, 320B params totales / 18B activos (MoE), licencia MIT. En el backend soporta `reasoning_effort` (low/high/max, default max) pero Ollama no expone el knob: se le pasa CERO parametros, default del servidor (ADR-041). Ex "ox-alpha" (stealth en OpenRouter/OpenCode, probado en batalla con agentes de codigo). Ficha verificada en docs.z.ai + Hugging Face. Manual completo: `docs/adr/ADR-041-motor-llm-glm-5.3-flash.md`.
- **web_search provider:** `DuckDuckGo Search (experimental)` (key-free, no consume créditos). El provider `ollama` usaba `glm-5.2:cloud` y consumía requests del presupuesto sin pedirlo - NO usar.
- **Modelos disponibles (Ollama):**
  - Local: `qwen3-embedding:0.6b` (embeddings, 1024 dims - unico modelo de embeddings del workspace), `nomic-embed-text:latest` (768 dims, legacy: ya no se usa), `gemma4:e4b-mlx` (vision + tono/voz).
  - Cloud (8 en config desde 2026-08-30): `deepseek-v4-flash:cloud` (default OpenClaw + motor del pipeline A/B), `glm-5.3-flash:cloud` (multimodal + escalada iter 3), `glm-5.3:cloud` (escalada intra-familia), `gemma4:cloud` (vision + tono/voz), `kimi-k2.7-code:cloud` (nivel superior, iter 4), `minimax-m3:cloud` (variante costo similar a GLM, opcional). FUERA del ecosistema (2026-08-30): `kimi-k3`, `deepseek-v4-pro`, `qwen3.5:cloud`, `nemotron-3-nano`, `gemma4:31b-cloud` - sacados de la config; para emergencia, restaurar desde el backup `~/.openclaw/openclaw.json.bak-20260830-pipeline-glm`

## Pipeline de agentes (programación)

- **Motor estándar (ADR-049):** Claude Code (embebido en Claude Desktop 3p, >= 2.x) apuntando al gateway Ollama, con el modelo dinámico de Ollama. Comando:
  - `ANTHROPIC_BASE_URL=http://127.0.0.1:11434` (o 11435) + `ANTHROPIC_AUTH_TOKEN=<cualquier valor>` + `claude -p "<tarea>" --model <modelo>` headless.
  - El ejecutable: `~/Library/Application Support/Claude-3p/claude-code/2.1.260/claude.app/Contents/MacOS/claude` (fragil a cambios de version, verificar con `ls`).
  - NO usar `ollama launch claude --model` (bug: rechaza el flag como "unknown option").
  - Requiere Claude Code >= 2.x (la 0.2.18 no maneja el bloque thinking de los modelos de razonamiento).
  - Warnings de `unrecognized_model` por modelos custom = ruido, no bloquean.
- **Qwen Code:** queda como fallback o segundo par de ojos, no como estandar (ADR-049). Para SIGKILL/sesiones largas, Claude maneja mejor que Qwen.
- **El modelo que carga el harness** se elige por tipo de tarea (ADR-040): `deepseek-v4-flash:cloud` default/motor, `glm-5.3-flash` escalada multimodal, `kimi-k2.7-code` nivel superior.
- **Claude Code ignora AGENTS.md** (verificado ADR-049): no lo lee en absoluto. El `CLAUDE.md` de la raiz del workspace hace `@import` de su `AGENTS.md`, y eso cubre todo el arbol incluidos `projects/x/` (el import se resuelve relativo al `CLAUDE.md`, y el discovery sube directorios). NO crear `CLAUDE.md` por proyecto: solo si un proyecto introduce su propio `AGENTS.md` (nada lo tiene hoy).
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
| `scripts/check_em_dash.py` | Escanear texto por guiones largos (U+2014/U+2013) antes de publicar a GitHub. Regla obligatoria. |
| `scripts/init-project.sh` | Scaffold de proyecto con triple git: crea `projects/<slug>/.knowledge/` + repo en gh (privado por defecto) + lo registra en el repo agregado `projects_openclaw` |
| `scripts/aggregate-sync.sh` | Sincroniza el repo agregado (`projects/` ↔ `projects_openclaw`): status/commit/pull/push del archivo completo. Uso: `aggregate-sync.sh [status|commit|push|pull]` |
| `scripts/initial-setup.sh` | Setup one-shot para máquina nueva (laptop/Mac nuevo): clona workspace + arma `projects/` como agregado (preservando `.knowledge/`) + attacha/clona los subrepos + verifica. Idempotente, con `--dry-run` y `--pull`. Uso: `initial-setup.sh [--dry-run|--pull|--workspace <dir>]` |
| `scripts/oss-tracker.js` | Tracker de contribuciones OSS |
| `scripts/pr-dashboard.sh` | Dashboard de PRs (para el batch check del ritual de inicio de sesión) |
| `scripts/github-pr-risk.sh` | Detector de risk signals de un PR (schema/auth/deps/API/secrets) + preguntas de review. Uso bajo demanda en el cross-review del pipeline. Portado del plugin github-workflow. Solo lectura |
| `scripts/safe-fetch.sh` | URL pre-flight check local antes de web_fetch: esquema https, typosquatting de dominios confiables, payload prompt injection. Exit: 0 ALLOW / 1 DENY / 2 CAUTION. Portado del concepto PreClick, 100% local |
| `scripts/skill-router.py` | Sugiere que skill usar para una tarea (matching local keyword + embeddings Ollama `qwen3-embedding:0.6b`). Portado del concepto skill-ai-inject. Uso: `skill-router.py "<tarea>"` |
| `scripts/project-closure.sh` | Cierra/immortaliza un proyecto terminado: crea ADR template, registra en memory.db (daily_notes + sessions_relacional), devuelve resumen para daily. Reproducible. Uso: `--name <slug> --title <t> --summary <s> [--complexity T] [--model m] [--tag t] [--create-adr]`. Skill: `project-closure` |
| `scripts/pipeline-track.sh` | Estado durable del pipeline A/B: init/start/review/done/status/resume/note. Sobrevive a SIGKILL/restarts (crash recovery). Portado del concepto Pipeline Architect. Acepta `--score T` en init (integrado con complexity-scorer) |
| `scripts/complexity-scorer.sh` | Evalua objetivo en 4 dimensiones (A/B/C/D), devuelve T-score 1-20 + bucket + modelo + thinking. Prueba gemma4:e4b-mlx local primero (6.7x mas rapido que qwen3.5), luego fallbacks cloud. `--score T` para forzar. T>=17 requiere confirmacion de Gonzo. Cablea complexity-driven-pipeline. Parser externo: `scripts/complexity-parse.py`. Integrado en `session-start.sh` (corre al iniciar sesion y persiste T en el log) |
| `scripts/pdf-tool.sh` | Toolkit PDF/OCR local: text, info, pages, search, ocr (tesseract), pdfimages, md2pdf (exportar MD a PDF). 100% local. Requiere poppler + tesseract + npx (brew). Portado de la familia PDF/OCR de ClawHub |
| `scripts/model-router.sh` | Router de modelo Ollama por tipo de tarea (code/review/long/cheap/writing/pipeline_ab) + overrides sticky. Pipeline A/B: DeepSeek (1-2) → GLM 5.3 Flash (3) → Kimi K2.7 Code (4). Consulta `model <tipo>` para decidir el --model. Portado del concepto ToggleLogic sin licencia |
| `scripts/task-notify.sh` | Notificacion desktop macOS cuando un agente termina tarea. Uso en pipeline A/B. Portado del concepto Task Notifier |
| `scripts/pre-commit.template` | Template de pre-commit hooks (lint → test → build) |
| `scripts/test-skills.sh` | Verifica que las skills estén bien formadas |

## Memoria (SQLite + espejos)

- **Fuente de verdad:** `memory/memory.db` (tablas: `daily_notes`, `todos`, `inbox`, `contributions`).
- **Busqueda semantica (2026-08-30):** `session_vectors` con embeddings reales de Ollama (768 dims) + `chunk_text`. Usar `scripts/semantic-search-json.js` para recuperar sesiones por significado. Re-catalogar con `scripts/memory-catalog-simple.sh` si se agregan dailies nuevos.
- **Espejos MD** (regenerar con `./scripts/memory-db.sh export-all`):
  - `memory/todos.md` ← tabla todos
  - `memory/inbox.md` ← tabla inbox
  - `docs/OSS-TRACKER.md` ← tabla contributions
- **Dailies:** viven en `memory/YYYY-MM-DD.md`; los viejos se archivan a la DB + `memory/archive/`.

## Red / remoto

- **Webchat remoto:** Tailscale Serve + PWA en iPhone. No hay app nativa iOS. Device pairing necesario la primera vez.
- **OpenClaw Control UI:** requiere secure context (HTTPS o localhost) - Tailscale Serve lo resuelve.
- **Cron de refresh token MeLi (SoporteML v4):** cron OpenClaw `soporteml-meli-token-refresh` dispara `POST /meli/refresh-token` en `localhost:3001` cada 5h (access tokens de MeLi duran ~6h). Credenciales admin: userId `521a68d2-f0dd-48c7-94fb-a07c7afccbc0` + companyId `4dd8ea5d-f1e5-4bd6-a59d-6f9bc4656798`. Si se reconecta OAuth con empresa nueva, actualizar el cron. Solo corre con el backend levantado.

---

_Actualizado 2026-09-14 (migrado desde AGENTS.md). Si algo cambia en el setup, actualizá este archivo - es mi cheat sheet._
