# ADR-049: Claude Code como motor del pipeline A/B (Qwen Code a fallback)

**Fecha:** 2026-09-15
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** workspace (Fase 0 de la cola durable; la deriva se detecto al auditar el motor)
**Relacionado:** ADR-040 (seleccion por tipo de tarea), ADR-041 (motor LLM GLM-5.3), ADR-045/046 (motor del pipeline v4.1/v4)
**Supersede parcialmente:** la seccion de motor de la skill `agent-orchestration-pipeline` y `docs/SETUP.md`

---

## Contexto

La documentacion operativa (`docs/SETUP.md` linea 29, skill `agent-orchestration-pipeline` linea 10 y 55) dice que **Qwen Code es el motor estandar** de los agentes A/B del pipeline, y que **Claude Code es una alternativa** para SIGKILL o tareas largas.

La practica es otra. Verificado el 2026-09-15 con fuentes reales:

| Ciclo | Harness real | Fuente |
|---|---|---|
| kanam-tetris v0.2 (2026-09-11) | Claude Code vía Ollama | `docs/learnings/pipeline-agentes.md` |
| Duelos de codigo atoi (2026-09-13) | Claude Code headless (Claude-3p 2.1.260) | `memory/2026-09-13.md` |
| Prueba de harness (2026-09-15) | Claude Code 2.1.260, `HARNESS_OK` | verificacion directa de esta sesion |

Ademas, `ollama launch` ya lista **claude** como integracion de primera clase (junto a qwen, codex, kimi, etc.), y no hay binario global `qwen`/`claude` (Claude Code vive embebido en `Claude-3p/`).

**Resultado:** la documentacion y la practica divergen desde ~2026-09-11. Un doc desactualizado es una deuda: el que lea que "Qwen es el estandar" va a intentar el comando `ollama launch qwen` que ya no es el camino usado.

---

## Decision

**`Claude Code` (embebido en Claude Desktop 3p, version >= 2.x) es el motor estandar de los agentes A/B del pipeline**, apuntando al gateway Ollama (`ANTHROPIC_BASE_URL=http://127.0.0.1:11434` o `11435`) con el modelo dinamico de Ollama.

**`Qwen Code` queda como fallback o segundo par de ojos**, no como estandar.

El modelo que ambos cargan se sigue eligiendo por tipo de tarea (ADR-040): `deepseek-v4-flash:cloud` como default/motor, `glm-5.3-flash` escalada multimodal, `kimi-k2.7-code` nivel superior.

### Comando estandar

```bash
ANTHROPIC_BASE_URL=http://127.0.0.1:11434 \
ANTHROPIC_AUTH_TOKEN=<token> \
<ruta-al-claude-de-Claude-3p>/claude -p "<tarea>" --model <modelo> \  # headless
  --dangerously-skip-permissions
```

- NO usar `ollama launch claude --model` (bug: rechaza el flag como "unknown option").
- Requiere Claude Code >= 2.x (la 0.2.18 no maneja el bloque `{type:thinking}` de los modelos de razonamiento).
- `ANTHROPIC_AUTH_TOKEN`: cualquier valor no vacio cuando el base url es el gateway local de Ollama.

---

## Consecuencias

### Positivas
- **La documentacion refleja la practica**: quien retome una sesion encuentra el camino que de verdad se usa.
- Claude Code maneja mejor sesiones largas que Qwen (menos SIGKILL), que era la motivacion original para tenerlo como alternativa.
- Una sola forma de lanzar los agentes A/B, con el mismo modelo dinamico de Ollama.

### Negativas
- Claude Code no tiene binario global en el PATH; la ruta al ejecutable de Claude-3p es frágil a cambios de version. Se mitiga documentandola en `docs/SETUP.md`.
- Claude Code emite warnings cosmetidos por modelos custom (`unrecognized_model`); son ruido, no bloquean.

### Regla de actualizacion
- **Este ADR es la fuente de la verdad.** Cualquier doc/skill que describa el motor del pipeline se actualiza para reflejarlo cuando se toque ese archivo. Si mañana el estandar vuelve a cambiar, se escribe ADR-052+ (supersede a este), no se edita la practica por debajo del ADR.

### Consecuencia: Claude Code ignora AGENTS.md (verificado empiricamente 2026-09-15)

Claude Code no lee AGENTS.md por defecto - **no lo prioriza, lo ignora**. Verificado con el binario 2.1.260:

| Escenario | Resultado |
|---|---|
| `CLAUDE.md` + `AGENTS.md` juntos | Responde al de `CLAUDE.md` (lo prioriza) |
| Solo `AGENTS.md` | *"I'm not instructed to reply with any specific token"* - no se lee (issue antrhopics/claude-code #6235) |
| `CLAUDE.md` con `@./AGENTS.md` | Las reglas del AGENTS.md se aplican |
| Import con ruta absoluta | Funciona |
| cwd en subdir + `CLAUDE.md` en el padre | Auto-discovery sube directorios y lo lee |

**Mecanismo adoptado:** **cada directorio raiz de proyecto (o workspace) lleva el PAR** `AGENTS.md` + `CLAUDE.md`. El `AGENTS.md` es la **unica fuente de verdad** de las reglas del proyecto; el `CLAUDE.md` es su **espejo que se dirige a el** (`@import` del `AGENTS.md`), no lo reemplaza. Asi nada se duplica y Claude Code carga las convenciones.

**Prioridad verificada empiricamente (2026-09-15, binario 2.1.260):** con cwd dentro de un proyecto que tiene su par propio Y la raiz con el suyo, Claude Code obedece **el par del proyecto** (respondio al marker del AGENTS.md del proyecto, no al de la raiz). El paquete de reglas mas especifico (el del proyecto) gana sobre el global.

**Contenido del par:** el `AGENTS.md` del proyecto es **especializado y personalizado para la tarea en curso** (que es el proyecto, su stack, su dominio y sus decisiones vivas), no una copia del global. El `CLAUDE.md` hace `@import` de ese `AGENTS.md` para que Claude Code lo cargue.

**Regla:** se crea el par en un proyecto **cuando ese proyecto entra al flujo de pipeline** (se trabaja con agentes Claude Code sobre el). El clon de un proyecto para pipeline agrega su par si no lo tiene. Hoy estan en el workspace raiz y en kanam-fixer (piloto 2026-09-15).

---

## Alternativas consideradas

1. **Mantener Qwen como estandar** (no documentar el cambio): ignoraria la practica real y dejaria el doc mintiendo. Rechazado.
2. **Dual estandar** (Qwen y Claude al mismo nivel): agrega complejidad sin beneficio; los ciclos reales ya usan Claude. Rechazado.
3. **Esto no es una decision de modelo**: ADR-040/041/045/046 siguen definiendo *que* modelo carga el harness. Este ADR solo decide *en que harness* corre. No pisa esas decisiones.
