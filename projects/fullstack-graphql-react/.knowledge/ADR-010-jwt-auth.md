# ADR-010: JWT Authentication with localStorage

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 6
**Scope:** Project

## Context

The book implements JWT authentication with localStorage for the client and a custom `@auth` directive for the server. The book also discusses cookies vs localStorage tradeoffs.

## Decision

Use JWT stored in localStorage with Bearer token in Authorization header. Use a custom `@auth` GraphQL directive for server-side authentication.

## Rationale

- localStorage is simpler for SPA development
- JWT is stateless — no server-side session storage needed
- `@auth` directive allows per-field/query authentication without modifying resolvers
- Bearer token is the standard for JWT transport

## Changes from Book

| Book (2020) | Modern (Aug 2026) | Reason |
|---|---|---|
| `withApollo` HOC | `useApolloClient` hook | `withApollo` removed in Apollo Client 4 |
| `ApolloConsumer` | `useApolloClient` | `ApolloConsumer` removed in Apollo Client 4 |
| Sequelize `Op.like` | Drizzle `like()` | ORM change |
| Sequelize `User.findAll` | Drizzle `db.select().from(users).where(...)` | ORM change |
| `bcrypt.compare` (async) | `bcrypt.compareSync` | better-sqlite3 is sync |
| `User.create` | `db.insert(users).values(...).returning().get()` | ORM change |

## ADRs Created
- ADR-010: JWT Authentication with localStorage
