# ADR-019 - Convención de Nomenclatura TypeScript: Sin Prefijos I/T

**Status:** Accepted
**Date:** 2026-08-05
**Source:** React 18 Design Patterns - Chapter 2 (Types vs Interfaces section)
**Scope:** Global - aplica a cualquier proyecto TypeScript

## Context

El libro recomienda usar prefijos `I` para interfaces (`IUser`) y `T` para types (`TUser`), conocida como notación húngara. Esta convención fue popular en los primeros años de TypeScript pero fue abandonada por la comunidad.

## Decision

No usar prefijos `I`/`T` en types o interfaces. El nombre refleja el concepto directamente:

```ts
// Bien
type User = { ... }
interface User { ... }

// Mal
type TUser = { ... }
interface IUser { ... }
```

## Rationale

1. **TypeScript tiene sintaxis para distinguir:** `type User = ...` vs `interface User = ...` ya es suficiente contexto.
2. **Colisión con React:** `IProps` / `IState` se confunde con componentes. `Props` / `State` es más limpio.
3. **Refactoring:** cambiar de `type` a `interface` (o viceversa) no debería requerir renombrar.
4. **Estándar de la comunidad:** React, TypeScript core, y librerías populares no usan prefijos.
5. **Sin beneficio real:** el prefijo no agrega información que el editor/IDE no muestre con hover.

## Exceptions

- Código legacy que ya usa la convención (no romper consistencia sin migración planificada).
- Proyectos que explicitamente decidan usarla por convención de equipo (no recomendado).

## Consequence

- Código más limpio y alineado con la comunidad TypeScript
- Sin fricción al cambiar entre `type` e `interface`
- Consistencia con React, Next.js, Vite, y librerías modernas

## Referencias

- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html
- React TypeScript cheatsheet: https://react-typescript-cheatsheet.netlify.app/
- Prettier + ESLint + Biome: todos usan la convención sin prefijos por defecto
