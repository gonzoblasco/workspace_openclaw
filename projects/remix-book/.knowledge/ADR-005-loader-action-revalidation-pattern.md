# ADR-005 — Loader + Action + Revalidation Data Flow Pattern

**Fecha:** 2026-08-05
**Contexto:** Capitulo 5 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar el patron de data flow de Remix (loader para reads, action para writes, revalidation automatica post-mutation) como alternativa a patrones tradicionales de state management (React Query, Redux, Zustand) en aplicaciones fullstack.

## Detalle

### El patron

```
Browser                    Server
  |                          |
  |-- GET /expenses -------->| loader() → query DB → json(expenses)
  |<-- HTML + JSON ----------|
  |                          |
  |-- POST /expenses (Form)->| action() → validate → write DB → redirect()
  |<-- 302 /expenses/123 ----|
  |                          |
  |-- GET /expenses/123 ---->| loader() → query DB → json(expense)
  |<-- JSON -----------------|
  |                          |
  |-- revalidate ALL loaders | (automatico post-action)
  |<-- fresh data -----------|
```

### Principios

1. **Route-level data fetching** — los loaders viven en los route modules, no en componentes. Esto permite ejecucion en paralelo y evita fetch waterfalls.

2. **POST to mutate, GET to load** — actions manejan mutations, loaders manejan reads. Sigue el modelo HTTP.

3. **Revalidation automatica** — despues de cada action, Remix re-fetchea todos los loaders activos. No hay stale data ni necesidad de invalidacion manual.

4. **Progressive enhancement** — el HTML form nativo funciona sin JS. Remix `<Form>` lo mejora con fetch requests client-side.

### Cuando usar este patron

- Aplicaciones fullstack donde el server es la source of truth
- CRUD tradicional con formularios
- Cuando se quiere evitar boilerplate de state management
- Cuando progressive enhancement es un requisito

### Cuando NO usar este patron

- Cuando se necesita optimistic updates complejos (aunque Remix lo soporta, es mas trabajo)
- Cuando hay mucha interaccion en tiempo real (WebSockets, streaming)
- Cuando el cliente necesita mantener estado que no viene del server

## Consecuencias

**Positivas:**
- Cero boilerplate de state management (no React Query, no Redux, no Zustand)
- Revalidation automatica sin stale data
- Progressive enhancement out of the box
- Tipado inferido del loader al componente
- Loaders en paralelo = mejor performance

**Negativas:**
- Todo el data fetching depende de la navegacion (no hay fetch "a demanda" desde cualquier componente)
- Revalidation post-action puede ser excesiva si hay muchos loaders
- No hay cache client-side explicita (cada navegacion re-fetchea)
- Dependencia del framework (no es portable)

## Notas

Este patron es especifico de Remix pero el concepto de "server como source of truth + revalidation automatica" es transferible. Next.js App Router con Server Actions sigue un patron similar.
