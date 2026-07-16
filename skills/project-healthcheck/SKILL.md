---
name: "project-healthcheck"
description: "Auditar proyecto existente: correr build/tests/lint, identificar bugs y edge cases, escribir tests, fixear, documentar estado de salud"
compat: claude-code, codex, cursor, openclaw
---

# project-healthcheck

> Auditoría profunda de un proyecto existente. Correr, romper, identificar, fixear, documentar.

## Cuándo usarla

- Querés entender el estado real de un proyecto (no solo lo que dice el README)
- Querés encontrar bugs antes de que los encuentre un usuario
- Querés mejorar la calidad de un proyecto sin un objetivo específico
- Querés aprender cómo está construido un proyecto (código, tests, decisiones)

## No usar cuando

- El proyecto ya tiene cobertura de tests exhaustiva y CI verde (usar product-reset para replantear dirección)
- Necesitás agregar una feature específica (usar taskflow o new-task)
- El proyecto no existe (usar product-orchestrator)

## Fases

### Fase 0 — Preparación

1. Clonar/abrir el repo
2. Leer README, package.json, estructura general
3. Identificar stack, scripts, dependencias
4. Verificar que se puede correr localmente

**Output:** Contexto del proyecto (stack, scripts, estructura)

### Fase 1 — Diagnóstico automático

1. `npm run typecheck` (o equivalente)
2. `npm test` (o `vitest run`)
3. `npm run build`
4. `npm run lint`
5. Revisar coverage si existe

**Output:** Estado actual: qué pasa y qué no. Cada fallo es un bug o deuda técnica.

### Fase 2 — Análisis de código

1. Leer componentes/funciones principales
2. Identificar edge cases no cubiertos:
   - Arrays vacíos
   - Items únicos
   - Estados nulos/undefined
   - Wrapping en navegación
   - IDs duplicados
   - Desmontaje inesperado
   - Callbacks no llamados
3. Revisar manejo de errores
4. Revisar accesibilidad (roles ARIA, teclado, focus)

**Output:** Lista de bugs potenciales y edge cases sin testear

### Fase 3 — Tests de edge cases

1. Escribir tests para cada edge case identificado
2. Usar archivos `*.edge.test.ts` o `*.edge.test.tsx` para mantenerlos separados
3. Correr los tests nuevos
4. Clasificar resultados:
   - 🟢 Test pasa → edge case cubierto, no hay bug
   - 🔴 Test falla → bug real encontrado

**Output:** Tests nuevos + bugs confirmados

### Fase 4 — Fix

1. Para cada bug confirmado:
   - Identificar la causa raíz
   - Escribir el fix
   - Verificar que el test pase
   - Verificar que ningún test existente se rompa
2. Correr suite completa: typecheck + test + build

**Output:** Código fixeado, tests verdes

### Fase 5 — Documentación

1. Escribir resumen de lo encontrado:
   - Bugs fixeados (con causa raíz)
   - Tests agregados
   - Mejoras realizadas
   - Estado final (typecheck ✅ test ✅ build ✅)
2. Actualizar STATUS.md o HANDOFF.md del proyecto
3. Commit + push

**Output:** Documentación del healthcheck

## Outputs esperados

- Estado real del proyecto (typecheck, tests, build, lint)
- Bugs encontrados y fixeados
- Tests de edge cases agregados
- Documentación del healthcheck
- Proyecto en estado verde

## Ejemplo real

Ver sesión de accessible-ui (2026-07-16):
- Proyecto: 3 componentes headless (Combobox, Modal, Tabs), 68 tests
- Diagnóstico: 68 tests verdes, build ok, typecheck ok
- Edge cases identificados: 22 para Combobox, 13 para Modal, 17 para Tabs
- Bugs encontrados: 3 (ArrowUp wrap, defaultActiveId inválido, overflow en unmount)
- Tests agregados: 52
- Estado final: 120 tests, typecheck ✅ test ✅ build ✅
