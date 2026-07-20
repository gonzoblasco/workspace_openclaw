---
name: "workflow-vibe-code-cleanup"
description: "Workflow de limpieza de código generado por IA/vibe coding: diagnosticar, limpiar, refactorizar y endurecer para producción."
---

# Propuesta: workflow-vibe-code-cleanup

## Problema

OpenClaw no tiene un workflow para limpiar código generado por IA o vibe coding. El workflow más cercano es `workflow-review-quality` pero es code review pre-merge, no diagnóstico y limpieza de deuda técnica.

## Inspiración

Del AI Developer Stack (gonzoblasco/ai-developer-stack):
- `vibe-code-auditor` — framework de auditoría con dimensiones: estructura, tipos, seguridad, performance, mantenibilidad
- `vibe-code-cleanup` — proceso quirúrgico: reconocimiento → imports muertos → archivos huérfanos → env vars → dependencias → release hygiene
- `refactor` — refactorización incremental con commits atómicos, sin cambiar comportamiento

## Propuesta de Workflow

### Fases

1. **Diagnóstico** — escanear codebase: estructura, tipos, seguridad, performance, mantenibilidad. Identificar patrones de deuda técnica.
2. **Reconocimiento** — mapear rutas, APIs, componentes, dependencias. Identificar imports muertos, archivos huérfanos, código comentado.
3. **Limpieza** — remover dead code, consolidar duplicación, estandarizar imports, limpiar env vars.
4. **Refactor** — refactorización incremental: extraer helpers, dividir componentes grandes, unificar manejo de errores.
5. **Endurecimiento** — typescript estricto (sin any), tests, dependencias actualizadas, release hygiene.
6. **Verificación** — build, typecheck, test, lint. Confirmar que nada se rompió.

### Filosofía

> Surgery, not demolition. Remove only what is provably dead. Preserve everything else.

- Commits atómicos (un cambio por commit)
- Validar después de cada batch
- Nunca cambiar comportamiento observable
- Preferir helpers compartidos sobre código duplicado

### Outputs

- Reporte de diagnóstico con issues priorizados
- Commits de limpieza y refactor
- Build + typecheck + tests verdes
- CHANGELOG actualizado

## Próximos pasos

1. Aprobar propuesta
2. Escribir SKILL.md
3. Probar en un proyecto real
