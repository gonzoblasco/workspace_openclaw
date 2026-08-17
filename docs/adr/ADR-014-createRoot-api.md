# ADR-014: createRoot API for React Entry Point

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Extracted from Full-Stack GraphQL + React book processing
**Scope:** Global - all new React projects

## Context

`ReactDOM.render()` was the standard React entry point for years. It was deprecated in React 18 and removed in React 19.

## Decision

Always use `createRoot` from `react-dom/client` as the React entry point.

## Rationale

- `ReactDOM.render` is removed in React 19 - code using it will not compile
- `createRoot` enables React 18+ concurrent features (automatic batching, transitions, Suspense)
- Supports `StrictMode` for development-time side-effect detection
- Standard pattern in all modern React projects and frameworks (Next.js, Remix, Vite templates)

## Pattern

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

## Consequences

- Import `createRoot` from `react-dom/client` (not `react-dom`)
- Single `root.render()` call replaces `ReactDOM.render()`
- `StrictMode` wrapping is recommended for development

## References

- https://react.dev/reference/react-dom/client/createRoot
- ADR-013: Vite as Default Bundler Over webpack
