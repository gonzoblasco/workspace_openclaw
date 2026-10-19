# ADR-052: Engram como memoria persistente de los agentes de pipeline (standalone, no gentle-ai)

**Fecha:** 2026-09-22
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** evaluacion de gentlemanprogramming.com + gentle-ai (2026-09-22); auditoria de codigo en quarantine y pilot con Qwen Code
**Relacionado:** ADR-049 (Claude Code motor del pipeline), ADR-050 (memoria SQLite local)

---

## Contexto

Gonzo recibio el sitio `gentlemanprogramming.com` para evaluar si servia al ecosistema. El producto es **Gentle-AI**: un binario Go que escribe configuracion (system prompts, skills, personas, entradas MCP) en los agentes de codigo que ya existen, mas un componente de memoria llamado **Engram**.

El analisis contra el ecosistema actual arrojo que ~80% de Gentle-AI ya esta implementado aca y con mas madurez (AGENTS.md, skills, OpenSpec como SDD, verify-before-push como evidencia, guardrails en red lines, SOUL/IDENTITY como persona). Adoptar el paquete completo implicaba dejar que un tercero reescriba configs afinadas a mano y pise decisiones documentadas en ADRs.

**El hueco real es otro:** los agentes de pipeline (Qwen Code / Claude Code lanzados desde OpenClaw via `ollama launch`) arrancan de cero. Solo reciben `AGENTS.md`; no tienen acceso a `docs/SETUP.md`, a `MEMORY.md` ni a `memory.db`. Cada sesion re-descubre lo que la anterior ya resolvio. Ese es exactamente el problema que Engram ataca.

---

## Decision

**Se adopta Engram standalone. No se adopta Gentle-AI.**

1. **Alcance:** Engram se instala como memoria de los **agentes de pipeline** (Qwen Code hoy; Claude Code cuando vuelva a estar operativo). **No** se conecta al Gateway de OpenClaw en esta fase: la memoria de Kanam sigue siendo `memory/memory.db` + `MEMORY.md` + daily (ADR-050 vigente, sin cambios).
2. **Via de instalacion:** Homebrew (`gentleman-programming/tap/engram`), version 2.0.0. Binario Go unico, SQLite + FTS5 en `~/.engram/engram.db`. Sin Node, Python ni Docker.
3. **Integracion:** `engram setup qwen` escribe `mcpServers.engram` en `~/.qwen/settings.json` y el bloque "Memory Protocol" delimitado por markers en `~/.qwen/QWEN.md`. Los markers hacen la operacion idempotente y preservan el contenido existente.
4. **Alcance de sync:** local-only. `engram sync` (export a `.engram/` para git) queda **deshabilitado por defecto**. Se habilita por proyecto solo con decision explicita. No se usa Engram Cloud.

---

## Evidencia del pilot (2026-09-22)

- **Auditoria (Fase 0, quarantine en `mktemp`):** sin telemetria ni SDKs de analytics en el codigo local; los unicos paths de red son cloud sync (opt-in explicito por proyecto, con `ReasonBlockedUnenrolled` para proyectos no inscriptos) y el listener Unix local. Dependencias limpias: stdlib de Go + `modernc.org/sqlite`, `mcp-go`, `bubbletea`, `templ`. Licencia MIT.
- **`engram doctor`:** 9/9 checks ok.
- **Round-trip CLI:** `engram save` + `engram search` verificados.
- **Round-trip via pipeline real:** Qwen lanzado con `ollama launch qwen` (no el binario directo) escribio la observacion #5 en Engram y la recupero por busqueda. **Esto valida la via que usa el pipeline de verdad.**
- **Proyecto detectado:** `workspace_openclaw`, derivado del git remote.

---

## Consecuencias

**Positivas:**

- Los agentes de pipeline retoman contexto de decisiones, bug fixes y convenciones sin re-explicar. El handoff entre sesiones deja de reconstruirse desde cero.
- Local-first: el estado autoritativo es un SQLite en la maquina. Nada sale salvo activacion explicita.
- Reversible: `brew uninstall engram` + restaurar los backups de config.

**Riesgos y mitigaciones:**

- **`engram setup` NO hace backup de las configs que escribe.** El marketing de backups pertenece a Gentle-AI, no a Engram standalone. El diseño con markers mitiga (no borra contenido ajeno), pero el backup es responsabilidad nuestra: se tomo copia de `~/.qwen/settings.json` y `~/.qwen/QWEN.md` antes del setup, en `~/.openclaw/backups/engram-fase1/`.
- **Ollama tambien gestiona `~/.qwen/settings.json`** (hace su propio backup en `~/.ollama/backup/qwen/`). Las dos escrituras coexisten hoy (la config de Ollama y el bloque `mcpServers.engram` conviven en el mismo archivo), pero una reconfiguracion de la integracion Qwen desde Ollama podria pisar el bloque. **Verificar `mcpServers.engram` despues de cualquier `ollama launch qwen` reconfigurado.**
- **Claude Code no esta instalado en la Mac Mini** (el binario no esta en PATH y `~/.claude.json` tiene `mcpServers: {}`). `engram setup claude-code` requiere el CLI de Claude para delegar el registro MCP, asi que queda bloqueado hasta que se instale. Pendiente cuando Claude Code vuelva a la rotacion.
- **Sin disciplina, la store se llena de ruido.** Mitigacion: el protocolo (skill `engram-project-memory`) prohibe guardar output crudo de tools, secrets, `.env` y datos personales.

**Alcance explicito:**

- No se instala Gentle-AI. Si en el futuro se reconsidera, requiere ADR nuevo.
- No se toca la config del Gateway de OpenClaw en esta fase.
- No se adopta Engram Cloud ni el RDD de Gentle-AI (nuestro equivalente es verify-before-push).

---

## Alternativas consideradas

1. **Adoptar Gentle-AI completo.** Descartado: pisaria configs, skills y ADRs propios, y la mayor parte de su valor ya esta implementado aca.
2. **No hacer nada.** Descartado: el costo de sesion fresca en los agentes de pipeline es real y medible (re-descubrimiento de decisiones cada sesion).
3. **Exponer Engram al Gateway de OpenClaw ahora.** Descartado por alcance: la memoria de Kanam ya funciona (ADR-050); mezclar dos sistemas de memoria sin necesidad agrega riesgo sin beneficio.
4. **Usar `memory.db` como memoria de los subagentes.** Descartado: los subagentes no tienen acceso a la DB ni al workspace de memoria; requeriria construir un servidor MCP propio.
