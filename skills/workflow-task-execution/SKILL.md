---
name: "workflow-task-execution"
description: "Workflow de ejecución de tareas: planificar, implementar, verificar, PR y cerrar epic. Basado en patrones del AI Developer Stack."
---

# Propuesta: workflow-task-execution

## Problema

OpenClaw tiene workflows para discovery y scaffold, pero no para la ejecución día a día: tomar una tarea, planificarla, implementarla, verificar calidad, crear PR y cerrar el epic.

## Inspiración

Del AI Developer Stack (gonzoblasco/ai-developer-stack):
- `plan-writing` — task planning con criterios de aceptación
- `new-task` — inicializar tarea con contexto y precondiciones
- `pr` — PR estructurado con build check + review + merge
- `close-epic` — ritual de cierre con CHANGELOG, tags y lecciones

## Propuesta de Workflow

### Fases

1. **Intake** — leer contexto del epic activo, AGENT_TASKS.md, criterios de aceptación
2. **Planificación** — desglosar tarea en subtareas de 2-5 min con verificación
3. **Branch** — crear branch desde main actualizado
4. **Implementación** — código + tests + tipos
5. **Verificación** — build, lint, typecheck, test
6. **PR** — PR estructurado con descripción, review automático
7. **Merge** — merge a main
8. **Cierre de Epic** — CHANGELOG, tags, lecciones aprendidas

### Outputs

- Plan de tarea en `{task-slug}.md`
- Branch con commits atómicos
- PR con descripción estructurada
- Epic cerrado con CHANGELOG y tags

### Skills que reemplazaría

Ninguna — es nuevo. Pero se relaciona con `workflow-build-scaffold` (post-scaffold) y `workflow-review-quality` (pre-merge).

## Próximos pasos

1. Aprobar propuesta
2. Escribir SKILL.md
3. Probar en un proyecto real
