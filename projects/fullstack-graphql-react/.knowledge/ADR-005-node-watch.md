# ADR-005: Node --watch Instead of nodemon + babel-node

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 2
**Scope:** Global

## Context

The book uses `nodemon --exec babel-node` for development server with auto-reload. This requires both `nodemon` and `@babel/node` as dependencies, plus a `.babelrc` config.

## Decision

Use Node.js built-in `--watch` flag (available since Node 22) with native ESM. No transpilation needed.

## Rationale

- Node 22+ has native `--watch` flag that restarts on file changes
- Node 22+ has stable ESM support — no Babel needed for `import`/`export`
- Eliminates `nodemon`, `@babel/node`, `@babel/core`, and `.babelrc` dependencies
- Faster startup (no Babel transpilation step)
- Same behavior: file change → server restart

## Consequences

- Script: `"server": "node --watch src/server/index.js"` instead of `"server": "nodemon --exec babel-node --watch src/server src/server/index.js"`
- All source files use `.js` extension with `"type": "module"` in package.json
- No `.babelrc` file needed
- No `nodemon` or `@babel/node` in dependencies

## References

- https://nodejs.org/en/blog/release/v22.0.0
