---
name: "engram-project-memory"
metadata:
  category: "Governance"
  tags:
    - memory
    - engram
    - pipeline
    - mcp
description: "Engram: memoria persistente de proyecto para los agentes de pipeline (Qwen Code / Claude Code). Cuando guardar, cuando buscar, que nunca guardar, y handoff al cerrar."
user-invocable: false
---

# Workflow: Engram Project Memory

## Purpose

Dar a los agentes de pipeline (Qwen Code, Claude Code) memoria de proyecto que sobreviva entre sesiones y compactions. Cubre el hueco de ADR-052: esos agentes arrancan de cero, solo con `AGENTS.md`.

**Alcance:** Engram es memoria **de proyecto de codigo**. La memoria de Kanam (daily, `MEMORY.md`, `memory.db`) sigue siendo la fuente de verdad del workspace y no se reemplaza.

## Prerequisites

- Engram instalado: `brew install gentleman-programming/tap/engram`
- Integracion activa: `engram setup qwen` (escribe `mcpServers.engram` en `~/.qwen/settings.json` y el bloque Memory Protocol en `~/.qwen/QWEN.md`)
- Verificar salud: `engram doctor` (read-only)
- Store: `~/.engram/engram.db`

## Protocolo

### 1. Orientar antes de escribir

Al empezar trabajo relacionado, antes de asumir nada:

1. `mem_current_project`: confirmar el proyecto resuelto y su fuente.
2. `mem_context`: recuperar historia reciente de sesiones.
3. `mem_search "terminos"`: buscar la decision, bug o convencion puntual.

Buscar es barato; re-descubrir es caro. Los resultados de busqueda son previews: usar `mem_get_observation` antes de apoyarse en el contenido completo.

### 2. Guardar con criterio (deliberado, no automatico)

Guardar con `mem_save` **despues** de:

- Bug fix cerrado (que estaba mal, por que, como se resolvio)
- Decision de arquitectura o diseno
- Descubrimiento no obvio del codebase
- Cambio de configuracion o setup de entorno
- Patron o convencion establecida
- Preferencia o constraint del usuario

Formato del contenido:

```
**What**: que se hizo, en una frase
**Why**: que lo motivo
**Where**: archivos o paths afectados
**Learned**: gotchas, casos borde
```

Title corto y buscable. Type: `bugfix | decision | architecture | discovery | pattern | config | preference`.

**Topic keys para temas que evolucionan:** usar `topic_key` estable (ej. `architecture/auth-model`) y reusarlo para actualizar el mismo tema en vez de crear observaciones competidoras. Si no esta claro, `mem_suggest_topic_key` primero.

### 3. Nunca guardar

- Output crudo de tools ni cada turno de conversacion
- Secrets, tokens, credenciales
- Contenido de `.env`
- Datos personales

### 4. Handoff al cerrar

Antes de terminar una sesion de trabajo, `mem_session_summary` con la estructura:

```
## Goal / ## Instructions / ## Discoveries / ## Accomplished / ## Next Steps / ## Relevant Files
```

**Discoveries es la seccion mas valiosa:** gotchas y aprendizajes no obvios. Luego `mem_session_end`.

### 5. Recuperar despues de compaction

1. Persistir primero el handoff con `mem_session_summary`.
2. Luego `mem_context` para recuperar historia reciente.
3. Continuar desde ahi.

## Verification

- `engram stats`: sessions, observations, projects.
- `engram search "<query>"`: confirmar que lo guardado es recuperable.
- `engram projects list`: detectar drift de nombres (si aparece, `engram projects consolidate`).
- `engram doctor`: diagnostico operativo read-only.

## Pitfalls

- **`engram setup` NO hace backup de configs.** Tomar copia de `~/.qwen/settings.json` y `~/.qwen/QWEN.md` antes de correrlo.
- **Ollama tambien escribe `~/.qwen/settings.json`** (backup propio en `~/.ollama/backup/qwen/`). Despues de reconfigurar la integracion Qwen desde Ollama, verificar que `mcpServers.engram` siga presente.
- **Claude Code** requiere su CLI instalado para `engram setup claude-code` (delega el registro MCP al CLI). Si el binario no esta en PATH, el setup no procede.
- **Sync a git deshabilitado por defecto** (ADR-052): `engram sync` exporta memoria a `.engram/` en el repo. Solo con decision explicita por proyecto.
- **No conectar Engram al Gateway de OpenClaw**: fuera de alcance de ADR-052.
