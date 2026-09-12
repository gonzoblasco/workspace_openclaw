# ADR-046: Revert del Motor del Pipeline A/B - DeepSeek V4 Flash (por costo)

**Status:** Accepted (2026-09-11)
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-09-11
**Origen:** workspace (revert por costo, analisis de uso semanal de Ollama Cloud)
**Revierte:** ADR-045 (Motor del Pipeline A/B - DeepSeek V4.1 Flash)
**Complementa:** ADR-041 (Motor LLM del Sistema - GLM-5.3-Flash)

## Decision

**`deepseek-v4-flash:cloud` vuelve a ser el motor de los agentes A/B del pipeline** (via Claude Code o Qwen Code apuntando al gateway Ollama `127.0.0.1:11434`).

`deepseek-v4.1-flash:cloud` sale del rol de motor del pipeline: queda como **fase de escalada** para analisis complejo, cuando ni v4 ni glm resuelven.

| Plano | Motor |
|---|---|
| Agentes A/B del pipeline (escritura + review) | `deepseek-v4-flash:cloud` (este ADR) |
| Default de OpenClaw / sesiones | `deepseek-v4-flash:0731` |
| Fallback + vision | `glm-5.3-flash:cloud` |
| Escalada (analisis complejo) | `deepseek-v4.1-flash:cloud` |

## Context

**11/09, 14:00-14:20:** ADR-045 establecio `deepseek-v4.1-flash` como motor del pipeline, tras el primer ciclo real sobre kanam-tetris v0.2. La calidad se validó con evidencia: el Agente A se autocazo un bug propio (comparacion case-sensitive en el keydown de Escape) y el Agente B reproduce bugs por ejecucion con un harness instrumentado (guard del estado `clearing`, lookup de wall kicks CCW espejado preexistente desde v0.1).

**11/09, 19:15:** el analisis del uso semanal de Ollama Cloud (capturas de Gonzo) midio el costo real de los tres modelos:

| Modelo | Requests | Consumo |
|---|---|---|
| `deepseek-v4-flash:0731` | 1.631 | bajo (el mas eficiente por request) |
| `glm-5.3-flash` | 1.518 | moderado |
| `deepseek-v4.1-flash` | 1.348 | el MAS consumidor (menos requests, mas barra) |

v4.1 consume mas por request de forma intrinseca (no es contexto ni thinking: los tres corren HIGH + 1M). La mejora de calidad de v4.1 sobre v4, medida en la cata del 11/09, no es grande.

**Decision de Gonzo:** el pipeline tambien vuelve a v4. La nueva es costosa y no justifica el gasto como motor de TODOS los ciclos.

## Reglas de uso

1. **Agentes A/B del pipeline corren en `deepseek-v4-flash:cloud`.** Se invocan via Claude Code o Qwen Code con `ANTHROPIC_BASE_URL` / `ollama launch` apuntando al gateway Ollama. **El router (`model-router.sh model pipeline_ab`) debe devolver v4-flash** - al promover v4.1 quedaron overrides sticky (`code`, `review`, `pipeline_ab`) apuntandole; reseteados el 11/09.
2. **v4.1 sigue disponible para escalada:** cuando ni v4 ni glm resuelven un analisis complejo. Se invoca puntualmente, no como motor por defecto.
3. **Las reglas operativas de ADR-045 sobre v4.1 siguen vigentes SOLO al escalar a v4.1:** `think:false` para roles mecanicos (con `num_predict` bajo agota el presupuesto en thinking y emite `content` vacio), consumir via API `/api/chat` con `stream:false` (no `ollama run` CLI, que mezcla el thinking en stdout), y presupuesto generoso (8000+) para roles de analisis.
4. **La pausa obligatoria del AGENTS.md se mantiene:** Kanam planifica (MAX), A escribe (HIGH), B revisa (HIGH), iterar, revision final de Kanam (MAX), push.
5. **El review debe EJECUTAR cuando el bug depende de tiempo.** Regla nacida en el ciclo v0.2 y vigente con cualquier motor: timers, ventanas de input y estado transitorio son invisibles a la lectura del codigo.

## Consecuencias

### Positivas

- Motor del pipeline alineado con el default de OpenClaw: menos superficie de configuracion (un motor + una escalada, en vez de dos motores paralelos).
- El costo por request del pipeline baja al nivel de v4, el mas eficiente de los tres medidos.
- Se conserva la escalada a v4.1 sin pagarla en cada ciclo.

### Negativas

- **Nombres no intercambiables:** el motor del pipeline debe correr con `--model deepseek-v4-flash:cloud`. La entrada de OpenClaw quedo como `deepseek-v4-flash:0731`, que **no resuelve** en Ollama (`ollama show` falla). Verificado el 11/09.
- **v4 esta anunciado para dejar de existir en unas semanas** (reemplazo por 4.1). Este ADR hay que reevaluarlo cuando el retiro llegue: es el mismo pendiente abierto en ADR-041 y en el daily del 2026-09-11.
- **El ciclo v0.2 se valido con v4.1.** El primer ciclo con v4 como motor conviene tratarlo como re-validacion: no asumir la misma calidad de review sin comprobarla.

## Referencias

- ADR-045 (revertido): motor del pipeline en DeepSeek V4.1 Flash
- ADR-041: motor LLM del sistema - GLM-5.3-Flash
- ADR-043: complexity-driven pipeline
- Ciclo v0.2 y analisis de costo: `memory/2026-09-11.md` (secciones 14:00-14:20 y 19:15-19:30)
- Learnings: `docs/learnings/pipeline-agentes.md` (regla de review por ejecucion)
