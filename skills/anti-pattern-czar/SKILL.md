---
name: "anti-pattern-czar"
description: "Detecta y corrige anti-patrones de error handling en TypeScript"
---

# anti-pattern-czar

## Descripción
Escanea codebases TypeScript en busca de anti-patrones de error handling: empty catch blocks, swallowed promises, unlogged errors. Opera en 5 modos: scan, review, auto, resume, report. El estado de sesión persiste entre ejecuciones para codebases grandes.

## Cuándo usarlo
- Antes de un release para encontrar silent catch blocks
- Para batch-fix de issues de error handling de baja severidad antes de un code review
- Para revisar interactivamente error handling en paths críticos (auth, DB)
- Para reanudar una auditoría después de cambiar de branch
- Para verificar progreso y conteo de issues restantes

## Workflow
1. Ejecutar anti-pattern-czar en modo scan sobre el directorio del proyecto
2. Revisar los hallazgos (modo review)
3. Aprobar fixes individuales o en batch (modo auto con approval)
4 Si queda trabajo pendiente, el estado persiste para la próxima sesión
5. Generar reporte final

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `vibe-code-cleanup/scripts/diagnose-codebase.sh` | Scan general de deuda técnica antes de enfocarse en error handling. |
| `vibe-code-cleanup/scripts/verify-cleanup.sh` | Validar que los fixes pasen build, typecheck, lint y tests. |
| `review-quality/scripts/review-pr.sh` | Revisión automática del PR resultante. |
| `engineering-governance/scripts/workflow-audit.sh` | Detectar otros anti-patrones a nivel de workflow. |

## Notas
- Solo cubre TypeScript
- El approval workflow previene cambios no deseados
- La persistencia entre sesiones permite auditar codebases grandes incrementalmente
