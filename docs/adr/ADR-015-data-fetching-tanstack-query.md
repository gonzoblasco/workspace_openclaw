# ADR-015: Data Fetching con TanStack Query

**Estado:** Aceptado
**Fecha:** 2026-08-05
**Actualizado:** 2026-10-15
**Decisores:** Gonzo / Kanam
**Origen:** workspace (generalizado desde libro "Testing React Library")

## Contexto

El patrón clásico de `useState` + `useEffect` para data fetching en React, aunque funcional, es considerado un anti-patrón porque no maneja race conditions, caching, deduplicación, retry, ni stale-while-revalidate. Es boilerplate manual que cada equipo termina reimplementando.

## Decisión

Usar **TanStack Query (React Query)** como capa de data fetching por defecto en proyectos React. Reemplazar los patrones de `useState` + `useEffect` para llamadas asincrónicas a APIs.

## Alternativas consideradas
- **`use()` + Suspense (React 19):** Nativo, pero sin el ecosistema de caching, retry y devtools de TanStack Query
- **RTK Query:** Overhead de Redux para casos que no lo requieren
- **SWR:** Similar pero con menos features de cache y mutations

## Consecuencias

### Positivas
- Menos boilerplate, caching automático, retry, stale-while-revalidate, devtools, mutations optimistas
- Separación clara entre fetching y presentación

### Negativas
- Dependencia externa adicional
- Curva de aprendizaje inicial

## Verificación en proyectos actuales
- soporteml: `@tanstack/react-query@5.83.0`

## Referencias
- [ADR-011](./ADR-011-nextjs-fullstack-platform.md): Next.js full-stack (Server Actions para mutaciones simples, TanStack Query para client fetching)
- [ADR-012](./ADR-012-supabase-baas.md): Supabase (PostgREST + TanStack Query)