---
name: "workflow-task-execution"
description: "Workflow de ejecución de tareas: planificar, implementar, verificar, PR y cerrar epic. Basado en patrones del AI Developer Stack."
---

# Workflow: Task Execution

## Qué hace
Ejecución día a día de tareas: desde que se define una tarea hasta que se cierra el epic con PR, merge y CHANGELOG. Se relaciona con `workflow-build-scaffold` (post-scaffold) y `workflow-review-quality` (pre-merge).

## Fases

### 1. Intake
Leer contexto del epic activo, criterios de aceptación, archivos de `.knowledge/` relevantes. No empezar a escribir código sin entender las restricciones.

### 2. Planificación
Desglosar tarea en subtareas de 2-5 minutos, cada una con verificación clara ("¿cómo sé que está hecho?"). Máximo 10 subtareas por plan. Si son más, dividir en múltiples planes.

### 3. Branch
```bash
git checkout main && git pull origin main
git checkout -b task/E[N]-T[NN]-[descripcion-corta]
```

### 4. Implementación
Código + tests + tipos. Commits atómicos: un cambio por commit, no acumular todo al final.

### 5. Verificación
```bash
npm run build    # debe pasar sin errores
npm run dev      # probar flujo principal manualmente
```

### 6. PR
PR estructurado con:
- Título: `feat|fix|refactor(scope): descripción`
- Body: qué hace, cambios principales, cómo testear, checklist
- Review automático antes de mergear

### 7. Merge
Merge a main preservando historial (`--no-ff`). No eliminar la branch (referencia histórica).

### 8. Cierre de Epic (cuando todas las tasks están completas)
- CHANGELOG: mover `[Unreleased]` a nueva versión semver
- Tags: `git tag -a E[N]-complete`
- Lecciones aprendidas documentadas
- STATUS.md actualizado

## Outputs
- Plan de tarea en `{task-slug}.md`
- Branch con commits atómicos
- PR con descripción estructurada
- Epic cerrado con CHANGELOG y tags
