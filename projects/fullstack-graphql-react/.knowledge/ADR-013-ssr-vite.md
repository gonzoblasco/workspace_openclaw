# ADR-013: SSR with Vite + Apollo renderToStringWithData

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 9
**Scope:** Global

## Context

The book implements SSR with webpack + Babel for the server bundle, `StaticRouter` for React Router, `renderToStringWithData` for Apollo, and cookies for authentication.

## Decision

Use Vite SSR mode with Apollo's `renderToStringWithData`, React Router's `StaticRouter`, and httpOnly cookies for auth.

## Key Differences from Book

| Book (webpack SSR) | Vite SSR | Reason |
|---|---|---|
| `webpack-dev-middleware` + `webpack-hot-middleware` | `vite.createServer({ server: { middlewareMode: true } })` | Vite handles HMR and bundling |
| `webpack.server.config.js` | No separate config | Vite SSR uses the same vite.config |
| `@babel/cli` for server transpilation | Native ESM | Node 22+ supports ESM natively |
| `ReactDOM.renderToString` | `renderToStringWithData` from Apollo | Waits for GraphQL queries |
| `ReactDOM.hydrate` | `hydrateRoot` from React 19 | New React 19 API |
| `react-helmet` | `react-helmet-async` | react-helmet unmaintained |
| `cookies` package | Same | Still standard |
| `node-fetch` for Apollo SSR | Not needed | Apollo Client 4 uses native fetch |

## SSR Flow

```
1. Client requests URL → Express.js receives request
2. Read authorization cookie → verify JWT → determine loggedIn state
3. Create Apollo Client with ssrMode: true + AuthLink with cookie
4. Render React tree with StaticRouter (fixed location)
5. renderToStringWithData waits for all GraphQL queries
6. Extract Apollo cache state (client.extract())
7. Render HTML template with content + head tags + __APOLLO_STATE__
8. Client receives HTML + hydrates with hydrateRoot
9. Apollo Client restores cache from __APOLLO_STATE__
10. No unnecessary GraphQL requests on first load
```

## Key Files

- `ssr/server.js` — Express + Vite SSR server
- `ssr/entry.jsx` — Server-side React entry with StaticRouter
- `ssr/apollo.js` — Apollo Client factory for SSR
- `ssr/template.js` — HTML template with __APOLLO_STATE__ injection
- `src/main.jsx` — Client entry with hydrateRoot
- `src/apollo/index.js` — Restores cache from window.__APOLLO_STATE__

## References

- https://vite.dev/guide/ssr
- https://www.apollographql.com/docs/react/performance/server-side-rendering
