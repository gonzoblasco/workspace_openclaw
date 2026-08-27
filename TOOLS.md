# TOOLS.md - Cheat Sheet del Setup

Notas específicas del entorno de Gonzo. Los detalles de los modelos/agentes en profundidad viven en `MEMORY.md` y las skills; acá está el resumen operativo para usar sin re-descubrir.

---

## Máquinas

- **Mac Mini** - máquina principal (donde corre el gateway de OpenClaw por defecto).
- **MacBook Air** - segunda máquina, misma config. Workspace sincronizado por git.
- **Regla de merge:** cuando venga algo del workspace (pull/rebase con conflictos), hacer merge, no reset. El soft reset descarta commits de la otra máquina.
- **Siempre `git pull --rebase` antes del push** (evita pisar cambios de la otra máquina).

## Modelos (Ollama local + cloud)

- **Default de chat/pipeline:** `deepseek-v4-flash:cloud` con **thinking max** (2026-08-27). Antes medium. Si la latencia molesta, Kanam sugiere bajar a medium/low para tareas rápidas. Config: `agents.defaults.thinkingDefault = "max"`.
- **web_search provider:** `DuckDuckGo Search (experimental)` (key-free, no consume créditos). El provider `ollama` usaba `glm-5.2:cloud` y consumía requests del presupuesto sin pedirlo - NO usar.
- **Modelos disponibles (Ollama):**
  - Local: `qwen3.5:9b-mlx` (8.9 GB), `nomic-embed-text:latest` (embeddings)
  - Cloud: `deepseek-v4-flash:cloud` (default), `deepseek-v4-pro:cloud`, `kimi-k2.7-code:cloud` (código), `kimi-k3:cloud`, `gemma4:cloud`, `qwen3.5:cloud`, `minimax-m3:cloud`, `nemotron-3-nano:30b-cloud`

## Pipeline de agentes (programación)

- **Motor estándar:** Qwen Code vía Ollama. Comando: `ollama launch qwen --model deepseek-v4-flash:cloud -- -p "<tarea>" -y`
- **Claude Code** (alternativa para SIGKILL/casos largos):
  - `ANTHROPIC_BASE_URL=http://localhost:11434` + `ANTHROPIC_AUTH_TOKEN` + settings.json de permisos
  - `claude -p "<tarea>" --model <modelo>`
  - NO usar `ollama launch claude --model` (bug: rechaza el flag como "unknown option")
  - Requiere Claude Code >= 2.x (la 0.2.18 crashea con modelos de razonamiento)
- **SIGKILL:** los procesos de Qwen mueren en tareas largas (~3 min) - usar prompts cortos, relanzar si muere.
- Detalle en la skill `agent-orchestration-pipeline`.

## Scripts del workspace

| Script | Uso |
|---|---|
| `scripts/memory-db.sh` | DB de memoria: `export-all`, `export-todos`, `export-inbox`, `export-oss`, `add-todo`, `add-inbox`, `export-daily`, `stats` |
| `scripts/check_em_dash.py` | Escanear texto por guiones largos (U+2014/U+2013) antes de publicar a GitHub. Regla obligatoria. |
| `scripts/init-project.sh` | Scaffold de proyecto con doble git: crea `projects/<slug>/.knowledge/` + repo en gh (privado por defecto) |
| `scripts/oss-tracker.js` | Tracker de contribuciones OSS |
| `scripts/pr-dashboard.sh` | Dashboard de PRs (para el batch check del ritual de inicio de sesión) |
| `scripts/github-pr-risk.sh` | Detector de risk signals de un PR (schema/auth/deps/API/secrets) + preguntas de review. Uso bajo demanda en el cross-review del pipeline. Portado del plugin github-workflow. Solo lectura |
| `scripts/safe-fetch.sh` | URL pre-flight check local antes de web_fetch: esquema https, typosquatting de dominios confiables, payload prompt injection. Exit: 0 ALLOW / 1 DENY / 2 CAUTION. Portado del concepto PreClick, 100% local |
| `scripts/skill-router.py` | Sugiere que skill usar para una tarea (matching local keyword + embeddings Ollama nomic). Portado del concepto skill-ai-inject. Uso: `skill-router.py "<tarea>"` |
| `scripts/pipeline-track.sh` | Estado durable del pipeline A/B: init/start/review/done/status/resume/note. Sobrevive a SIGKILL/restarts (crash recovery). Portado del concepto Pipeline Architect |
| `scripts/pdf-tool.sh` | Toolkit PDF/OCR local: text, info, pages, search, ocr (tesseract), pdfimages, md2pdf (exportar MD a PDF). 100% local. Requiere poppler + tesseract + npx (brew). Portado de la familia PDF/OCR de ClawHub |
| `scripts/model-router.sh` | Router de modelo Ollama por tipo de tarea (code/review/long/cheap/writing) + overrides sticky. Consulta `model <tipo>` para decidir el --model. Portado del concepto ToggleLogic sin licencia |
| `scripts/task-notify.sh` | Notificacion desktop macOS cuando un agente termina tarea. Uso en pipeline A/B. Portado del concepto Task Notifier |
| `scripts/pre-commit.template` | Template de pre-commit hooks (lint → test → build) |
| `scripts/test-skills.sh` | Verifica que las skills estén bien formadas |

## Memoria (SQLite + espejos)

- **Fuente de verdad:** `memory/memory.db` (tablas: `daily_notes`, `todos`, `inbox`, `contributions`).
- **Espejos MD** (regenerar con `./scripts/memory-db.sh export-all`):
  - `memory/todos.md` ← tabla todos
  - `memory/inbox.md` ← tabla inbox
  - `docs/OSS-TRACKER.md` ← tabla contributions
- **Dailies:** viven en `memory/YYYY-MM-DD.md`; los viejos se archivan a la DB + `memory/archive/`.

## Red / remoto

- **Webchat remoto:** Tailscale Serve + PWA en iPhone. No hay app nativa iOS. Device pairing necesario la primera vez.
- **OpenClaw Control UI:** requiere secure context (HTTPS o localhost) - Tailscale Serve lo resuelve.
- **Cron de refresh token MeLi (SoporteML v4):** cron OpenClaw `soporteml-meli-token-refresh` dispara `POST /meli/refresh-token` en `localhost:3001` cada 5h (access tokens de MeLi duran ~6h). Credenciales admin: userId `521a68d2-f0dd-48c7-94fb-a07c7afccbc0` + companyId `4dd8ea5d-f1e5-4bd6-a59d-6f9bc4656798`. Si se reconecta OAuth con empresa nueva, actualizar el cron. Solo corre con el backend levantado.

## Desarrollo

- **Pre-commit hooks** (`simple-git-hooks`): lint (Biome) → test (Vitest) → build. Omitir con `SKIP_SIMPLE_GIT_HOOKS=1`.
- **Iconos:** Lucide (`lucide-react`) en todos los proyectos. Nunca emojis como iconografía de producto.
- **Stack opinado:** OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG.
- **Regla de idioma:** todo lo que se ve en GitHub va en INGLES; los strings de UI en ESPAÑOL.

---

_Actualizado 2026-08-23. Si algo cambia en el setup, actualizá este archivo - es mi cheat sheet._
