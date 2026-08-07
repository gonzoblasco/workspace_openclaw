# ADR-010: Data Fetching Moderno con TanStack Query

## Contexto

El patron clasico de `useState` + `useEffect` para data fetching en React, aunque funcional, es considerado un anti-patron porque no maneja race conditions, caching, deduplicacion, retry, ni stale-while-revalidate. Es boilerplate manual que cada equipo termina reimplementando.

## Decision

Usar **TanStack Query (React Query)** como capa de data fetching en proyectos React. Reemplazar los patrones de `useState` + `useEffect` para llamadas asincronicas a APIs.

## Alternativas consideradas

- **use() + Suspense (React 19):** Nativo, pero sin el ecosistema de caching, retry, y devtools de TanStack Query.
- **RTK Query:** Overhead de Redux para casos que no lo requieren.
- **SWR:** Similar pero con menos features de cache y mutations.

## Consecuencias

- Positivas: Menos boilerplate, caching automatico, retry, stale-while-revalidate, devtools, mutations optimistas.
- Positivas: Separacion clara entre fetching y presentacion.
- Negativas: Dependencia externa adicional.
- Negativas: Curva de aprendizaje inicial.

## Estado

Aceptado.
