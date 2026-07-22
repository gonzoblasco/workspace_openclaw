---
name: "vibe-code-cleanup"
description: "Workflow de limpieza de código generado por IA/vibe coding: diagnosticar, limpiar, refactorizar y endurecer para producción."
user-invocable: false
---

# Workflow: Vibe Code Cleanup

## Propósito
Tomar código generado por IA (vibe coding) y llevarlo a estado producible: sin deuda técnica, con tipos, tests y estructura sólida.

## Filosofía
> Surgery, not demolition. Remove only what is provably dead. Preserve everything else.

- Commits atómicos (un cambio por commit)
- Validar después de cada batch
- Nunca cambiar comportamiento observable
- Preferir helpers compartidos sobre código duplicado

## Cuándo usarlo
- Limpiar código generado por IA antes de llevarlo a producción
- Diagnosticar deuda técnica en una codebase generada
- Refactorizar componentes grandes, tipar `any`, consolidar duplicación
- Endurecer un proyecto generado con tests, types y build verde

## Fases

### 1. Diagnóstico
Escanear codebase y detectar patrones de deuda técnica:
- **Estructura** — archivos sin usar, imports muertos, código comentado
- **Tipos** — `any` sin tipar, tipos incorrectos, faltantes
- **Seguridad** — secrets hardcodeados, SQL injection, XSS
- **Performance** — bundles grandes, N+1 queries, sin lazy loading
- **Mantenibilidad** — funciones largas (>150 líneas), duplicación, nombres poco claros

Quick scan inicial (60 segundos): contar archivos y líneas, identificar lenguaje/framework, detectar red flags (hardcoded secrets, TODOs, commented code).

### 2. Reconocimiento
Mapear la codebase antes de tocar nada:
- Rutas y páginas
- APIs y endpoints
- Componentes y dependencias
- Variables de entorno
- Entry points y flujo de datos

### 3. Limpieza
- Remover imports muertos y archivos huérfanos
- Consolidar duplicación en helpers compartidos
- Estandarizar imports y exports
- Limpiar console.logs, commented code, archivos temporales
- Actualizar .gitignore si es necesario

### 4. Refactor
Refactorización incremental con commits atómicos:
- Extraer lógica repetida a `lib/utils/`
- Dividir componentes > 150 líneas en sub-componentes
- Unificar manejo de errores
- Reemplazar `any` por tipos explícitos
- Un refactor por commit

### 5. Endurecimiento
- TypeScript estricto (sin `any`)
- Tests para lógica de negocio core
- Dependencias actualizadas (npm outdated)
- Release hygiene (CHANGELOG, versionado)

### 6. Verificación
```bash
npm run build      # debe pasar sin errores
npx tsc --noEmit   # typecheck
npm test           # tests pasando
npm run lint       # sin errores
```

## Outputs
- Reporte de diagnóstico con issues priorizados
- Commits de limpieza y refactor
- Build + typecheck + tests verdes
- CHANGELOG actualizado
