# ADR-013: El stack de testing - Vitest con TypeScript

**Fecha:** 2026-08-05 (unificado 2026-10-19)
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** workspace (generalizado desde libro "Simplify Testing with React Testing Library")
**Absorbe:** el viejo ADR de TypeScript en archivos de test (antes numerado 014, retirado al fusionarse) - dos decisiones gemelas del mismo origen, aplicables siempre juntas

---

## Decisión

### 1. Vitest como test runner por defecto

Para nuevos proyectos React/TypeScript: **Vitest** en lugar de Jest. API compatible (describe/it/expect), significativamente más rápido (native ESM, transform esbuild), integración nativa con tooling Vite.

- Imports Jest-specific (`@jest/globals`) reemplazados por Vitest globals; `jest-dom` setup idéntico (`import '@testing-library/jest-dom/vitest'`)
- Archivos auto-descubiertos; `environment: 'jsdom'` sin configuración extra
- Migración trivial (Vitest soporta Jest globals out of the box); CI arranca en ~200ms vs ~2s de Jest
- Alternativas descartadas: Jest con `@swc/jest` (más rápido que Jest puro, sigue pesado); `node:test` (sin matchers ricos ni entorno DOM)

### 2. TypeScript en los archivos de test

Todos los tests en `.test.ts` / `.test.tsx` (nunca JavaScript). La type safety del test acompaña a la del código que prueba: mejor IDE, errores de tipo detectados antes de correr, consistencia con el resto del codebase. Vitest maneja `.tsx` nativamente con cero configuración. La verbosidad adicional se paga sola.

**Es la misma decisión:** el runner y el idioma de los tests se adoptan juntos; separarlos no tiene caso práctico.

## Verificación en proyectos actuales

- Vitest: a11y-fixer (+ coverage-v8), kanam-fixer, kanam-onwheels; soporteml (vitest run)
- TypeScript tests: kanam-spec (`.test.ts`, node:test), proyectos React (`.test.tsx`)

## Referencias

- [ADR-028](./ADR-028-biome-toolchain.md): pre-commit con `biome check + vitest run`
- [ADR-020](./ADR-020-vite-default-bundler.md): Vitest usa Vite internamente