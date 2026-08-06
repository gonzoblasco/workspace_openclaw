---
name: "handoff-matrix"
description: "Handoff documentation explícita entre etapas del pipeline de desarrollo"
---

# handoff-matrix

## Descripción
Documenta explícitamente los handoffs entre etapas del pipeline de desarrollo. Cada agente sabe de quién recibe, qué formato espera, y a quién pasa. Los reportes se guardan versionados bajo reports/v[X.X.X]/ para trazabilidad completa.

## Handoff Matrix
| Agent | Recibe de | Formato de entrada | Pasa a | Formato de salida |
|-------|-----------|-------------------|--------|-------------------|
| @researcher | User/Orchestrator | Pregunta de investigación | @architect | Research report con fuentes |
| @architect | User/@researcher | Requerimiento o research | @api-guardian o @builder | Architecture decision con opciones |
| @api-guardian | @architect | Especificación de API | @builder | Impact report + migration checklist |
| @builder | @architect/@api-guardian | Spec + checklist | @validator + @tester | Implementation report |
| @validator | @builder | Código implementado | SYNC POINT | Validation report |
| @tester | @builder | Código implementado | SYNC POINT | Test report + screenshots |
| @scribe | Quality gates approved | Reportes de todas las etapas | @github-manager | CHANGELOG + VERSION update |

## Estructura de Reportes
```
reports/
└── v[VERSION]/
    ├── 00-researcher-report.md    (opcional)
    ├── 01-architect-report.md
    ├── 02-api-guardian-report.md  (si aplica)
    ├── 03-builder-report.md
    ├── 04-validator-report.md
    ├── 05-tester-report.md
    └── 06-scribe-report.md
```

## Formato de Handoff
Cada handoff incluye:
1. **Resumen** — Qué se logró en esta etapa
2. **Decisiones** — Trade-offs y opciones descartadas
3. **Archivos afectados** — Lista de archivos creados/modificados
4. **Pendientes** — Cosas que la siguiente etapa debe saber
5. **Riesgos** — Potenciales issues identificados

## Notas
- Sin dependencias externas
- Los reportes son markdown, fáciles de leer y versionar
- La estructura versionada permite trazabilidad completa

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `session-lifecycle/scripts/session-start.sh` | Cargar HANDOFF previo al inicio de una nueva etapa. |
| `session-lifecycle/scripts/session-end.sh` | Generar/actualizar HANDOFF al cerrar una etapa. |
| `background-execution` | Ejecutar etapas en background cuando no requieren interaccion. |
| `agent-workflow` | Multi-agent orchestration con handoffs explicitos. |
| `tech-docs/scripts/update-changelog.sh` | Actualizar CHANGELOG cuando @scribe entrega la version. |
