---
name: "context-aware-delegation"
description: "Pasa contexto de sesión principal a subagentes y cron jobs"
---

# context-aware-delegation

## Descripción
Usa sessions_history para que sesiones aisladas (cron jobs, sub-agents) puedan leer el historial de la sesión principal antes de ejecutar su tarea. Permite usar modelos más baratos para tareas background manteniendo contexto completo.

## Cuándo usarlo
- Cuando un subagente necesita contexto de la conversación principal
- Para cron jobs que deben referenciar trabajo previo
- Para webhook handlers que actúan sobre decisiones previas
- Para tareas background que requieren orientación sin repetir contexto

## Workflow
1. Identificar la tarea que necesita contexto de la sesión principal
2. Usar context-aware-delegation para pasar el sessionKey
3. La sesión aislada lee el historial relevante via sessions_history
4. Ejecuta la tarea con contexto completo

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `session-lifecycle/scripts/session-start.sh` | Cargar contexto de inicio de sesión antes de delegar. |
| `session-lifecycle/scripts/session-end.sh` | Guardar resumen para que la sesión aislada lo recupere. |
| `background-execution` | Patrones para ejecutar subagentes en background. |
| `agent-workflow` | Multi-agent orchestration con handoffs explícitos. |

## Notas
- Usa APIs nativas de OpenClaw (sessions_history)
- No requiere dependencias externas
- Reduce costos al permitir modelos baratos para tareas background
