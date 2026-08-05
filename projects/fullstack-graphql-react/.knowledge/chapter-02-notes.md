# Chapter 2: Setting Up GraphQL with Express.js

## Core Concepts

1. **Express.js routing:** `app.get()`, `app.post()`, `app.use()` for handling HTTP requests
2. **Middleware pattern:** Functions that receive `(req, res, next)` and can pre/post-process requests
3. **Helmet:** Security headers (CSP, XSS protection, referrer policy)
4. **CORS:** Cross-Origin Resource Sharing for API access from different domains
5. **Compression:** Gzip/brotli response compression
6. **Apollo Server:** GraphQL server that integrates with Express
7. **GraphQL Schema:** Type definitions for the API (queries, mutations, types, inputs)
8. **Resolvers:** Functions that implement schema fields
9. **GraphQL Mutations:** Operations that modify data (POST/PUT/DELETE equivalent)
10. **Winston:** Structured logging with file and console transports
11. **Postman/HTTP clients:** Testing GraphQL APIs

## Key Changes from Book

| Book (2020) | Modern (Aug 2026) | Reason |
|---|---|---|
| `apollo-server-express` v3 | `@apollo/server` v5 + `@as-integrations/express5` | Apollo restructured integrations; Express 5 support |
| `applyMiddleware()` | `expressMiddleware()` + `await server.start()` | New Apollo Server API |
| `nodemon --exec babel-node` | `node --watch` | Node 22+ native file watching; ESM without Babel |
| `app.get('*', ...)` | `app.use(...)` | Express 5 path-to-regexp v8 breaks bare `*` |
| `.babelrc` with presets | Not needed | Native ESM in Node 22+ |
| `@babel/node` | Not needed | No transpilation required |
| GraphQL schema as string | Same (still valid) | GraphQL SDL hasn't changed |
| `winston` | Same | Still actively maintained |

## Architecture

```
Client → Express.js → Apollo Server → GraphQL Schema → Resolvers → Data (in-memory)
                ↓
         Static files (dist/client/, uploads/)
```

## ADRs Created
- ADR-004: Apollo Server 5 with @as-integrations/express5
- ADR-005: Node --watch Instead of nodemon + babel-node
- ADR-006: Express 5 Catch-All with app.use Instead of app.get('*')

## Running the Chapter 2 Project

```bash
cd projects/fullstack-graphql-react/chapter-02
npm run server    # Development server with auto-reload
```

Test GraphQL:
```bash
# Query
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ posts { id text } }"}'

# Mutation
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { addPost(post: {text: \"Hello\"}, user: {username: \"Test\", avatar: \"/a.png\"}) { id text } }"}'
```
