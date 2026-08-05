# ADR-003: Use createRoot instead of ReactDOM.render

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 1
**Scope:** Global

## Context

The book uses `ReactDOM.render(<App />, document.getElementById('root'))`. This API was deprecated in React 18 and removed in React 19.

## Decision

Use `createRoot` from `react-dom/client` as the standard entry point.

## Rationale

- `ReactDOM.render` is removed in React 19
- `createRoot` enables React 18+ concurrent features
- Supports StrictMode for development-time double-invocation to detect side effects
- Standard pattern in all modern React projects

## Consequences

- Import `createRoot` from `react-dom/client` instead of `ReactDOM` from `react-dom`
- Single `root.render()` call replaces `ReactDOM.render()`
- Enables StrictMode wrapping for development

## References

- https://react.dev/reference/react-dom/client/createRoot
