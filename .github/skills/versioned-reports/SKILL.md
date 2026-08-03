---
name: "versioned-reports"
description: "Estructura de reportes versionados por release para trazabilidad"
---

# versioned-reports

## Descripción
Crea y gestiona la estructura de reportes versionados bajo `reports/v[X.X.X]/`. Cada etapa del pipeline guarda su reporte en la carpeta de la versión correspondiente. Proporciona trazabilidad completa de decisiones, archivos afectados, y resultados de calidad.

## Estructura
```
reports/
└── v[VERSION]/
    ├── 00-researcher-report.md    (opcional - solo si hubo research)
    ├── 01-architect-report.md     (decisiones de arquitectura)
    ├── 02-api-guardian-report.md  (opcional - solo si hubo API changes)
    ├── 03-builder-report.md       (archivos creados/modificados)
    ├── 04-validator-report.md     (resultados de code quality)
    ├── 05-tester-report.md        (resultados de UX quality + screenshots)
    └── 06-scribe-report.md       (CHANGELOG, VERSION, README updates)
```

## Formato de cada reporte
```markdown
# [Etapa] Report - v[X.X.X]

## Resumen
[Qué se hizo en esta etapa]

## Decisiones
- [Decisión 1]: [Rationale]
- [Decisión 2]: [Rationale]

## Archivos afectados
- `path/to/file.ts` — [acción: created/modified/deleted]

## Pendientes para la siguiente etapa
- [ ] [Pendiente 1]
- [ ] [Pendiente 2]

## Riesgos identificados
- [Riesgo 1]: [Mitigación]
```

## Cuándo usarlo
- Al inicio de un nuevo feature/bug fix/release
- Cuando se necesita trazabilidad de decisiones
- Para auditoría de cambios
- Para handoff entre sesiones o agentes

## Workflow
1. Al iniciar un workflow, determinar la versión target
2. Crear carpeta `reports/v[VERSION]/`
3. Cada etapa guarda su reporte al completar
4. Al finalizar, todos los reportes están disponibles para @scribe
5. @scribe usa los reportes para actualizar CHANGELOG

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `tech-docs/scripts/update-changelog.sh` | Inserta `[Unreleased]` en CHANGELOG.md. Usar al finalizar. |
| `release-management/scripts/generate-release-notes.sh` | Genera notas de release desde los reportes versionados. |
| `handoff-matrix` | Documentar handoffs entre etapas del pipeline. |
| `session-lifecycle/scripts/session-end.sh` | Guardar resumen y reportes al cerrar sesión. |

## Notas
- Sin dependencias externas
- Markdown, fácil de leer y versionar
- La estructura numérica (00, 01, 02...) preserva el orden del pipeline
