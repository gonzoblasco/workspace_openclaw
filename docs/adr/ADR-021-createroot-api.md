# ADR-021: createRoot API

**Estado:** Aceptado
**Fecha:** 2026-08-05
**Actualizado:** 2026-10-15
**Decisores:** Gonzo / Kanam
**Origen:** workspace (generalizado desde libro "Full-Stack GraphQL + React")

## Contexto

`ReactDOM.render()` fue el entry point estándar de React por años. Fue deprecado en React 18 y removido en React 19.

## Decisión

Siempre usar `createRoot` de `react-dom/client` como entry point de React.

## Rationale

- `ReactDOM.render` removido en React 19 - código que lo use no compila
- `createRoot` habilita features concurrentes de React 18+ (automatic batching, transitions, Suspense)
- Soporta `StrictMode` para detección de side-effects en desarrollo
- Patrón estándar en todos los proyectos/frameworks modernos (Next.js, Remix, Vite templates)

## Patrón

```jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

## Consecuencias

- Import `createRoot` desde `react-dom/client` (no `react-dom`)
- Una sola llamada `root.render()` reemplaza `ReactDOM.render()`
- `StrictMode` wrapping recomendado para desarrollo

## Verificación en proyectos actuales
- kanam-spec: `createRoot` en `src/main.tsx`
- soporteml: `createRoot` en `src/main.tsx`

## Referencias
- https://react.dev/reference/react-dom/client/createRoot
- [ADR-020](./ADR-020-vite-default-bundler.md): Vite como bundler por defecto