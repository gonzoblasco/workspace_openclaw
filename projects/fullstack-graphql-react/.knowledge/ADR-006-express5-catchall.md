# ADR-006: Express 5 Catch-All with app.use Instead of app.get('*')

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 2
**Scope:** Global

## Context

The book uses `app.get('*', ...)` as a catch-all route for SPA fallback. Express 5 uses `path-to-regexp` v8 which no longer supports bare `'*'` as a valid path pattern.

## Decision

Use `app.use((req, res) => ...)` as the catch-all fallback instead of `app.get('*', ...)`.

## Rationale

- Express 5's `path-to-regexp` v8 throws `PathError: Missing parameter name at index 1: *`
- `app.use` without a path matches all routes regardless of HTTP method
- For SPA fallback, we want to serve `index.html` for any unmatched route
- `app.use` is method-agnostic, which is correct for a fallback handler

## Consequences

- Replace `app.get('*', handler)` with `app.use(handler)`
- The fallback handler must be registered after all other routes
- Only one catch-all handler should exist (last in middleware chain)

## References

- https://expressjs.com/en/guide/migrating-5.html
- https://github.com/pillarjs/path-to-regexp
