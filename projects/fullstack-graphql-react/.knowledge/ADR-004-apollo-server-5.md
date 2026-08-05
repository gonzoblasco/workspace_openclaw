# ADR-004: Apollo Server 5 with @as-integrations/express5

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 2
**Scope:** Project

## Context

The book uses `apollo-server-express` v3 with `applyMiddleware()` to bind Apollo to Express. Apollo Server 4+ restructured the integration pattern, and Apollo Server 5 (current) has further changes.

## Decision

Use `@apollo/server` v5 with `@as-integrations/express5` for Express 5 integration.

## Rationale

- `apollo-server-express` v3 is deprecated and incompatible with Express 5
- Apollo Server 4+ uses `expressMiddleware()` instead of `applyMiddleware()`
- Apollo Server 5 requires calling `server.start()` before applying middleware
- Express 5 integration is provided by the separate `@as-integrations/express5` package
- The `@as-integrations/express5` package handles Express 5's new routing semantics

## Consequences

- Import `ApolloServer` from `@apollo/server` (not `apollo-server-express`)
- Import `expressMiddleware` from `@as-integrations/express5`
- Must call `await server.start()` before `app.use('/graphql', ...)`
- Context is passed as an option to `expressMiddleware()`, not to `ApolloServer` constructor
- The `applyMiddleware()` method no longer exists

## References

- https://github.com/apollo-server-integrations/apollo-server-integration-express5
- https://www.apollographql.com/docs/apollo-server/
