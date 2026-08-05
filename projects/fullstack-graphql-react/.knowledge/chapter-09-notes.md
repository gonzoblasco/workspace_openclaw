# Chapter 9: Implementing Server-Side Rendering

## Core Concepts

1. **SSR vs CSR:** Server pre-renders HTML on first request, client hydrates
2. **Universal rendering:** Same React code runs on server and client
3. **renderToStringWithData:** Apollo function that waits for all GraphQL queries
4. **StaticRouter:** React Router for stateless server-side rendering
5. **hydrateRoot:** React 19 API that reuses server HTML instead of replacing it
6. **__APOLLO_STATE__:** Serialized Apollo cache injected into HTML
7. **httpOnly cookies:** Secure auth for SSR (not accessible by JavaScript)
8. **Vite SSR:** `vite.createServer({ server: { middlewareMode: true } })`

## Key Changes from Book

| Book (2020) | Modern (Aug 2026) | Reason |
|---|---|---|
| webpack-dev-middleware | Vite middleware mode | Vite handles HMR |
| webpack.server.config.js | Same vite.config | Vite SSR uses single config |
| @babel/cli for server | Native ESM | Node 22+ |
| ReactDOM.renderToString | renderToStringWithData | Waits for Apollo queries |
| ReactDOM.hydrate | hydrateRoot | React 19 API |
| react-helmet | react-helmet-async | Unmaintained |
| node-fetch polyfill | Not needed | Native fetch in Node 22 |

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Express.js                     │
│  ┌──────────────┐  ┌────────────────────────┐  │
│  │ Cookies      │  │ Vite SSR Middleware     │  │
│  │ Middleware   │  │  ┌──────────────────┐   │  │
│  └──────┬───────┘  │  │ ssrLoadModule()  │   │  │
│         │          │  │ → ServerApp      │   │  │
│         ▼          │  │ → renderToString  │   │  │
│  ┌──────────────┐  │  │   WithData()     │   │  │
│  │ JWT Verify   │  │  │ → HTML + State   │   │  │
│  └──────┬───────┘  │  └──────────────────┘   │  │
│         │          └────────────────────────┘  │
│         ▼                                      │
│  ┌──────────────────────────────────────────┐   │
│  │ SSR Route: GET *                         │   │
│  │ 1. Check cookie → loggedIn?              │   │
│  │ 2. Create SSR Apollo Client              │   │
│  │ 3. Render React (StaticRouter)           │   │
│  │ 4. renderToStringWithData                 │   │
│  │ 5. Extract cache → __APOLLO_STATE__      │   │
│  │ 6. Send HTML + state to client           │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

## New/Modified Files

- `ssr/server.js` — SSR Express server with Vite
- `ssr/entry.jsx` — Server React entry with StaticRouter
- `ssr/apollo.js` — SSR Apollo Client factory
- `ssr/template.js` — HTML template with state injection
- `src/main.jsx` — Changed to hydrateRoot
- `src/apollo/index.js` — Restores cache from __APOLLO_STATE__
- `src/router.jsx` — Exports RoutesConfig for SSR reuse
- `src/App.jsx` — Accepts loggedInProp from SSR
- Backend: cookies in login/signup, logout mutation

## Running

```bash
# Terminal 1: Backend API
cd projects/fullstack-graphql-react/chapter-03
JWT_SECRET="***" npm run server

# Terminal 2: SSR Server
cd projects/fullstack-graphql-react/chapter-04
JWT_SECRET="***" npm run ssr
```

Visit http://localhost:3000 — the HTML is pre-rendered on the server.
