# ADR-014: TypeScript en Archivos de Test

**Estado:** Aceptado
**Fecha:** 2026-08-05
**Actualizado:** 2026-10-15
**Decisores:** Gonzo / Kanam
**Origen:** workspace (generalizado desde libro "Simplify Testing with React Testing Library")

## Contexto

Muchos tutoriales y libros de testing aún usan JavaScript para archivos de test. El desarrollo React moderno es predominantemente TypeScript, y los archivos de test se benefician de la misma type safety.

## Decisión

Todos los archivos de test en nuevos proyectos React/TypeScript deben ser **TypeScript** (`.test.ts` / `.test.tsx`).

## Alternativas consideradas
- **JavaScript con JSDoc:** Menos estricto, más difícil de mantener a escala
- **JavaScript plano:** Más rápido de escribir pero pierde type safety

## Consecuencias

- Mejor soporte IDE (autocomplete, refactoring, type checking)
- Captura errores de tipos en compile-time antes de correr tests
- Vitest maneja `.tsx` nativamente con cero configuración
- Ligeramente más verboso pero la seguridad supera la verbosidad
- Consistencia con el resto del codebase

## Verificación en proyectos actuales
- kanam-spec: tests en `.test.ts` (node:test runner)
- Proyectos React: tests en `.test.tsx` con Vitest

## Referencias
- [ADR-013](./ADR-013-vitest-over-jest.md): Vitest como test runner