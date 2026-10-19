# ADR-013: Vitest como Test Runner por Defecto

**Estado:** Aceptado
**Fecha:** 2026-08-05
**Actualizado:** 2026-10-15
**Decisores:** Gonzo / Kanam
**Origen:** workspace (generalizado desde libro "Simplify Testing with React Testing Library")

## Contexto

Jest ha sido el test runner estándar para proyectos React, pero tiene tiempos de arranque lentos, soporte ESM débil y una superficie de configuración pesada comparada con alternativas modernas.

## Decisión

Usar **Vitest** como test runner por defecto para nuevos proyectos React/TypeScript. Vitest provee API compatible (describe/it/expect), es significativamente más rápido (native ESM, transform esbuild) e integra nativamente con tooling basado en Vite.

## Alternativas consideradas
- **Jest con `@swc/jest`:** Más rápido que Jest default pero sigue siendo más pesado que Vitest
- **Node native test runner (`node:test`):** Falta el ecosistema rico de matchers y soporte de entorno DOM

## Consecuencias

- Imports Jest-specific (`@jest/globals`) reemplazados por Vitest globals
- jest-dom setup funciona idéntico (`import '@testing-library/jest-dom/vitest'`)
- Archivos de test usan extensión `.test.tsx` / `.test.ts`, Vitest auto-descubre
- No configuración jsdom necesaria - Vitest la maneja via `environment: 'jsdom'`
- Migración trivial: Vitest soporta Jest globals out of the box
- CI pipelines benefician de arranque rápido (Vitest ~200ms vs Jest ~2s)

## Verificación en proyectos actuales
- a11y-fixer: `vitest` + `@vitest/coverage-v8`
- kanam-fixer: `vitest run`
- kanam-onwheels: `vitest run` / `vitest` watch

## Referencias
- [ADR-014](./ADR-014-typescript-for-tests.md): TypeScript en archivos de test
- [ADR-028](./ADR-028-biome-toolchain.md): Toolchain unificado (Biome + Vitest)