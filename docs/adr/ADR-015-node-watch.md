# ADR-015: Node --watch for Development Server Reload

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Extracted from Full-Stack GraphQL + React book processing
**Scope:** Global - all Node.js projects

## Context

The standard pattern for development auto-reload has been `nodemon` with various exec runners (`babel-node`, `ts-node`, `tsx`). Node 22 introduced a built-in `--watch` flag.

## Decision

Use `node --watch` as the default development server runner. Only fall back to `nodemon` or `tsx` when `--watch` is insufficient (e.g., TypeScript projects that need transpilation).

## Rationale

- Built into Node 22+ - no extra dependency
- Restarts the process on any file change in the watched path
- Works with native ESM (`"type": "module"`) without transpilation
- Eliminates `nodemon` dependency for pure Node.js/ESM projects
- Same behavior: file change → server restart

## Pattern

```json
{
  "scripts": {
    "server": "node --watch src/server/index.js"
  }
}
```

## When to Use Alternatives

- **TypeScript:** Use `tsx watch src/server/index.ts` (tsx wraps --watch)
- **Legacy CommonJS:** `node --watch` works, but ensure no Babel transform is needed
- **Complex watch patterns:** `nodemon` still useful for custom ignore/include patterns

## References

- https://nodejs.org/en/blog/release/v22.0.0
- ADR-005: Node --watch Instead of nodemon + babel-node
