---
name: "context-anchor"
description: "Briefing estructurado post-compactación desde archivos de memoria"
---

# context-anchor

## Descripción
Script que escanea archivos de memoria y contexto locales para producir un briefing estructurado sobre dónde se quedó el trabajo. Diseñado para usar después de compactación de contexto o al inicio de sesión cuando la working memory se perdió.

## Cuándo usarlo
- Después de una compactación de contexto
- Al orientar un agente fresco en un proyecto en progreso
- Para revisar decisiones tomadas en daily logs recientes
- Para handoff de estado actual a otro agente
- Para verificar open loops antes de empezar trabajo nuevo

## Workflow
1. Ejecutar context-anchor
2. El script escanea memory/*.md y archivos de contexto
3. Produce un briefing estructurado: proyecto actual, última tarea, decisiones recientes, open loops
4. Usar el briefing para retomar el trabajo

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `knowledge-management/scripts/discover.sh` | Escanear archivos de conocimiento y generar Knowledge Map. |
| `knowledge-management/scripts/freshness.sh` | Clasificar documentos por vigencia. |
| `knowledge-management/scripts/check-refs.sh` | Verificar que links internos del briefing no estén rotos. |
| `session-lifecycle/scripts/session-start.sh` | Cargar HANDOFF previo al inicio de sesión. |

## Notas
- Lee archivos que sobreviven a la compactación
- No depende de in-context memory
- Complementa el startup ritual de AGENTS.md
