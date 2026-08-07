# ADR-026 — Concurrent Mode como Default (React 19)

**Status:** Accepted
**Date:** 2026-08-05
**Source:** React 18 Design Patterns — Chapter 10 (Concurrent mode section)
**Scope:** Global — aplica a cualquier proyecto React 18+

## Context

React 18 introdujo concurrent mode como un opt-in. Habia que configurarlo explicitamente:

```tsx
const root = ReactDOM.createRoot(document.getElementById('root'), {
  mode: 'concurrent'
})
```

Esto generaba confusion: muchos proyectos no lo activaban y perdian las mejoras de rendimiento (automatic batching en setTimeout/promesas, time slicing, transitions).

## Decision

En React 18.3+ y React 19, concurrent mode es el **default**. No se necesita configuracion especial.

```tsx
// React 19 — concurrent mode activo por defecto
import { createRoot } from 'react-dom/client'
import App from './App'

createRoot(document.getElementById('root')!).render(<App />)
```

### Implicaciones

1. **Automatic Batching:** todas las actualizaciones de estado se agrupan, incluso fuera de event handlers (setTimeout, promesas, callbacks nativos).
2. **Transitions disponibles:** `useTransition` y `useDeferredValue` funcionan sin configuracion extra.
3. **Suspense en el servidor:** SSR con streaming y Suspense boundaries funciona out-of-the-box.
4. **`ReactDOM.render` removido:** en React 19, solo `createRoot`.

### Lo que NO cambio

- `useState` y `useReducer` siguen funcionando igual
- Los componentes existentes no requieren cambios
- `StrictMode` sigue siendo opt-in (y recomendado)

## Rationale

1. **Mejor rendimiento sin esfuerzo:** automatic batching reduce renders innecesarios sin cambiar codigo.
2. **Preparacion para el futuro:** React 19 y React Compiler asumen concurrent mode como base.
3. **Menos configuracion:** una API de entry point unica (`createRoot`) en vez de dos (`render` vs `createRoot` con mode).

## Consequence

- Proyectos nuevos usan `createRoot` sin opciones
- Proyectos existentes migrando de `ReactDOM.render` a `createRoot` obtienen concurrent mode automaticamente
- `useTransition` y `useDeferredValue` funcionan sin configuracion
- `ReactDOM.render` debe ser reemplazado (removido en React 19)

## Referencias

- React 18 — Concurrent mode: https://react.dev/blog/2022/03/29/react-v18
- React 19 — createRoot: https://react.dev/reference/react-dom/client/createRoot
- React 19 — Automatic batching: https://react.dev/blog/2022/03/29/react-v18#new-feature-automatic-batching
