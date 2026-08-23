# ADR-027: Tsconfig Moderno Vite

**Status:** Accepted
**Fecha:** 2026-08-05
**Origen:** react-18-design-patterns
**Source:** React 18 Design Patterns - Chapter 2 (TypeScript configuration file section)
**Scope:** Global - aplica a cualquier proyecto React + Vite + TypeScript

## Context

El libro propone separar `tsconfig.common.json` + `tsconfig.json` con opciones como `module: "commonjs"`, `experimentalDecorators: true`, `noEmit: false`, y `outDir: "dist"`. Esta configuración refleja prácticas de 2020-2022 que ya no son óptimas con el stack moderno.

## Decision

Usar una configuración mínima de tsconfig para proyectos React + Vite + TypeScript en 2026:

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true
  },
  "include": ["src"]
}
```

## Rationale

| Opción del libro | Problema | Solución 2026 |
|---|---|---|
| `module: "commonjs"` | No aprovecha ESM nativo | `module: "ESNext"` |
| `moduleResolution: "node"` | No resuelve correctamente con bundlers | `moduleResolution: "bundler"` (TS 5+) |
| `experimentalDecorators: true` | Obsoleto, no recomendado | Eliminar |
| `noEmit: false` | TypeScript emite JS que Vite va a re-compilar | `noEmit: true` (Vite compila) |
| `outDir: "dist"` | Vite define su propio output | Eliminar |
| `declaration: true` + `declarationMap: true` | Solo necesario para librerías | Opcional, Vite las genera si es necesario |
| `sourceMap: true` | Vite maneja sourcemaps | Opcional |
| `downlevelIteration: true` | No necesario con target ESNext | Eliminar |
| `strictNullChecks` + `strictFunctionTypes` | Redundante con `strict: true` | Solo `strict: true` |
| `tsconfig.common.json` separado | Mono-repo pattern válido pero no necesario para proyectos simples | Un solo `tsconfig.json` |

## Consequences

- Configuración más simple y mantenible
- Aprovecha ESM nativo y moduleResolution bundler
- Sin opciones obsoletas que puedan causar confusión
- Vite maneja la compilación, TypeScript solo type-checking

## Referencias

- TypeScript 5.x - `moduleResolution: "bundler"`: https://devblogs.microsoft.com/typescript/announcing-typescript-5-0/#moduleresolution-bundler
- Vite + TypeScript: https://vitejs.dev/guide/features.html#typescript
- React + TypeScript: https://react.dev/learn/typescript
