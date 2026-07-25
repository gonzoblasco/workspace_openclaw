---
name: "gh-issue-planner"
metadata:
  category: "Project Management"
  tags:
    - github
    - issues
    - planificacion
    - project-management
description: "Planificar y desglosar un proyecto en epics, stories y subtasks de GitHub Issues. Fase 0.4 del Product Discovery. SOLO para repos personales."
user-invocable: false
---

# Workflow: GitHub Issue Planner

## Propósito
Desglosar el ROADMAP de un proyecto en issues de GitHub (epics → stories → subtasks) para sincronizar el equipo de desarrollo.

## ⚠️ REGLA INAMOVIBLE
Este workflow SOLO se ejecuta en **repos personales/propios**. NUNCA en repos ajenos (forks, contribuciones, PRs a terceros).

En repos ajenos, la planificación queda en los docs locales (`.knowledge/ROADMAP.md`) o en el HANDOFF de la sesión. Si se necesita trackear progreso, usar `.knowledge/TRACKER.md` local.

## Prerrequisitos
- `gh` CLI autenticado con permisos de repo
- Repo creado en GitHub
- ROADMAP.md completado (Fase 0.2 de Product Discovery)

## Rutina

### Paso 1: Configurar labels

```bash
# Labels base
gh label create epic --color "1D76DB" --description "Epic: gran bloque de trabajo"

# Labels por sprint
gh label create sprint-1 --color "0E8A16" --description "Sprint 1"
gh label create sprint-2 --color "0E8A16" --description "Sprint 2"
# ... tantos sprints como haya

# Labels auxiliares
gh label create good-first-issue --color "7057FF" --description "Buena para arrancar"
```

### Paso 2: Crear Epics

Por cada epic del ROADMAP, crear un issue con label `epic`:

```bash
gh issue create --label epic --title "Epic N: Nombre — Descripción corta" --body "$(cat templates/epic-template.md)"
```

**Template de Epic:** (ver `templates/epic-template.md`)

### Paso 3: Crear Stories

Por cada feature del sprint, crear un issue con label del sprint correspondiente:

```bash
gh issue create --label sprint-N --title "Nombre de la story" --body "$(cat templates/story-template.md)"
```

**Template de Story:** (ver `templates/story-template.md`)

### Paso 4: Crear Subtasks

Por cada subtarea de una story, crear un issue que referencie a la story padre:

```bash
gh issue create --label sprint-N --title "[#ID_PADRE] Nombre de la subtask" --body "$(cat templates/subtask-template.md)"
```

El body debe incluir `**Padre:** #[ID_PADRE]` para mantener la jerarquía.

### Paso 5: Marcar good-first-issues

Identificar 2-3 issues ideales para nuevos contribuidores y marcar con label:

```bash
gh issue edit ISSUE_ID --add-label good-first-issue
```

### Paso 6: Actualizar descripciones de Epics

Una vez creados todos los issues, actualizar las descripciones de los epics para que sean auto-contenidas:

```bash
gh issue edit EPIC_ID --body "$(cat templates/epic-description.md)"
```

La descripción del epic debe incluir:
- **Qué se logra** (visión general del epic)
- **Qué incluye** (lista de lo que se construye)
- **Quién puede agarrar estos issues** (perfil sugerido)
- **Criterios de éxito** (cómo saber si está terminado)

## Templates

### epic-template.md
```
## 🏗️ Epic N: Nombre

### ¿Qué se logra en este epic?
[Descripción general]

### ¿Qué incluye?
- [Lista de features]

### Criterios de éxito
- [Criterio 1]
- [Criterio 2]
```

### story-template.md
```
## [Nombre de la story]

**Epic:** #[ID_EPIC]

### Qué hay que hacer
[Descripción de una línea]

### Subtasks
- [#ID] [Nombre subtask]
- [#ID] [Nombre subtask]

### Detalle técnico
[Comandos, snippets, config, referencias a .knowledge/]

### Criterios de éxito
- [Criterio 1]
- [Criterio 2]
```

### subtask-template.md
```
**Padre:** #[ID_PADRE]

### Qué hay que hacer
[Descripción de una línea]

### Detalle técnico
[Comandos, snippets, referencias]

### Criterios de éxito
- [Criterio 1]
```

### epic-description.md
```
## 🏗️ Epic N: Nombre — Descripción corta

### ¿Qué se logra en este epic?
[Visión general: qué puede hacer el usuario/admin cuando este epic esté completo]

### ¿Qué incluye?
- [Feature 1]
- [Feature 2]
- [Feature 3]

### ¿Quién puede agarrar estos issues?
[Perfil sugerido: frontend, backend, fullstack, etc.]

### Criterios de éxito
- [Criterio 1]
- [Criterio 2]
- [Criterio 3]
```

## Scripts de Referencia

### `scripts/create-sprint.sh`
Script para crear todos los issues de un sprint de una sola vez. Recibe:
- Número de sprint
- Archivo CSV/JSON con las stories y subtasks

(No implementado aún — pendiente para cuando el patrón se repita 3+ veces)

## Jerarquía de Issues

```
Epic (label: epic)
  └── Story (label: sprint-N, body: "**Epic:** #[epic_id]")
        └── Subtask (label: sprint-N, title: "[#story_id] nombre", body: "**Padre:** #[story_id]")
```

## Convenciones de Nomenclatura

- **Epic:** `Epic N: Nombre — Descripción corta`
- **Story:** `Nombre descriptivo de la feature`
- **Subtask:** `[#ID_PADRE] Acción concreta a realizar`

## Related

- [Product Discovery](../product-discovery): Fase 0.4 de la cual este skill es parte
- [Build & Scaffold](../build-scaffold): Para construir el proyecto post-planificación
