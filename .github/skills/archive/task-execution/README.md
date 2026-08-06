# Task Execution

Ejecución día a día de tareas.

## ¿Para qué sirve?

Para **implementar features, fixear bugs y cerrar epics** de forma estructurada. Desde que se define una tarea hasta que se cierra el epic con PR, merge y CHANGELOG. Es el workflow que más vas a usar en el día a día.

## ¿Cuándo usarlo?

- Cuando implementás una feature
- Cuando fixeás un bug
- Cuando cerrás un epic
- Básicamente, siempre que escribís código

## ¿Cómo se usa?

### Workflow completo

1. **Intake** — leer contexto del epic, criterios de aceptación, `.knowledge/`
2. **Planificación** — desglosar en subtareas de 2-5 min con verificación
3. **Branch** — `git checkout -b task/E1-T03-descripcion`
4. **Implementación** — código + tests + tipos, commits atómicos
5. **Verificación** — `npm run build`, probar flujo manualmente
6. **PR** — título convencional, body estructurado, review automático
7. **Merge** — `--no-ff`, no eliminar branch
8. **Cierre de Epic** — CHANGELOG, tags, lessons learned

### Scripts útiles

```bash
# Planificar tarea
./scripts/plan-task.sh --epic E1 --task T03 --title "Implementar login con Google"

# Cerrar epic
./scripts/close-epic.sh --epic E1 --version 1.2.0
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/task-planning.md` | Template de desglose, guía de tamaño, ejemplos de verificación |
| `references/branch-convention.md` | Branch naming, commit messages, PR template |

## Skills relacionadas

- [Build & Scaffold](../build-scaffold) — Para scaffolding inicial del proyecto
- [Review & Quality](../review-quality) — Para revisar antes de mergear
