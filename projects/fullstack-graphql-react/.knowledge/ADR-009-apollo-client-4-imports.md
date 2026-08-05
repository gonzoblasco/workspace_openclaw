# ADR-009: Apollo Client 4 with Separate React Hooks Import

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 4
**Scope:** Global

## Context

The book imports Apollo Client hooks (`useQuery`, `useMutation`, `ApolloProvider`) directly from `@apollo/client`. Apollo Client 4+ restructured its exports, moving React-specific hooks to `@apollo/client/react`.

## Decision

Import React hooks from `@apollo/client/react` instead of `@apollo/client`. Core utilities (`gql`, `ApolloClient`, `InMemoryCache`) remain imported from `@apollo/client`.

## Rationale

- Apollo Client 4+ no longer exports React hooks from the main package
- `@apollo/client/react` exports: `ApolloProvider`, `useQuery`, `useMutation`, `useSubscription`, `useFragment`, etc.
- Core package (`@apollo/client`) exports: `gql`, `ApolloClient`, `InMemoryCache`, `HttpLink`, `from`, `onError`
- This separation allows tree-shaking for non-React environments

## Pattern

```jsx
// Core utilities
import { gql, ApolloClient, InMemoryCache } from '@apollo/client';

// React hooks
import { ApolloProvider, useQuery, useMutation } from '@apollo/client/react';
```

## Consequences

- All React components using Apollo hooks must import from `@apollo/client/react`
- `ApolloProvider` is also in `@apollo/client/react`
- `main.jsx` imports `ApolloProvider` from `@apollo/client/react`
- No change to the Apollo Client setup file (it doesn't use React hooks)

## References

- https://www.apollographql.com/docs/react
