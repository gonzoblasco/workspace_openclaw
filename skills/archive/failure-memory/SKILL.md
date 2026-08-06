---
name: "failure-memory"
description: "Aprendizaje estructurado de errores con umbrales de evidencia"
---

# failure-memory

## Descripción
Detecta fallas durante sesiones del agente, las registra como observaciones con contadores de recurrencia, confirmación y desconfirmación, y promueve patrones a constraints cuando se alcanzan umbrales de evidencia. Todos los datos quedan en un directorio local `.learnings/` sin llamadas externas.

## Cuándo usarlo
- Para trackear fallas de tests que se repiten en un proyecto
- Para capturar patrones de timeout de API durante desarrollo activo
- Para buscar observaciones pasadas cuando un error familiar reaparece
- Para registrar correcciones del usuario al comportamiento del agente
- Para promover errores de lint recurrentes a constraints del agente

## Workflow
1. Corre en background durante sesiones normales
2. Cuando detecta una falla, la registra como observación
3. Si la falla se repite, incrementa el contador de recurrencia
4. Cuando se alcanza el umbral de evidencia, promueve el patrón a constraint
5. El constraint se aplica en adelante para prevenir la misma falla

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `memory-agent/scripts/consolidate.sh` | Ejecuta DREAMS consolidation para promover observaciones a MEMORY.md. |
| `memory-agent/scripts/discover.sh` | Escanear archivos de aprendizaje y memoria. |
| `knowledge-management/scripts/knowledge-audit.sh` | Auditar que las lecciones aprendidas estén actualizadas. |
| `engineering-governance/scripts/workflow-audit.sh` | Auditar que los constraints se apliquen en los workflows. |

## Notas
- Todo local en `.learnings/`
- Sin API calls externas
- Los umbrales de evidencia evitan falsos positivos
- Complementa knowledge-management (Learning Signals)
