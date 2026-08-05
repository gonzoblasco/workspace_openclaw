# ADR-002: Replace react-helmet with react-helmet-async

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 1
**Scope:** Global

## Context

The book uses `react-helmet` for managing document head tags. `react-helmet` is unmaintained and has known issues with React 18+ strict mode (duplicate head tags, warnings).

## Decision

Replace `react-helmet` with `react-helmet-async`.

## Rationale

- `react-helmet` has not been updated since 2020
- `react-helmet-async` is the community-maintained fork with React 18+ support
- Works correctly with React StrictMode (no duplicate head tags)
- Supports server-side rendering via `HelmetProvider.renderStatic()`
- Same API surface: `<Helmet>` component with identical props
- Only difference: requires `<HelmetProvider>` wrapper at the app root

## Consequences

- Add `<HelmetProvider>` at the app root level
- Import from `react-helmet-async` instead of `react-helmet`
- Same `<Helmet>` usage for titles, meta tags, etc.
- SSR support available when needed later

## References

- https://github.com/staylor/react-helmet-async
