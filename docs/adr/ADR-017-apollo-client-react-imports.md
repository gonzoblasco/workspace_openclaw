# ADR-017: Apollo Client React Hooks from @apollo/client/react

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Extracted from Full-Stack GraphQL + React book processing
**Scope:** Global — all React projects using Apollo Client 4+

## Context

Apollo Client 4+ restructured its package exports. React-specific hooks (`useQuery`, `useMutation`, `useSubscription`) and `ApolloProvider` are no longer exported from the main `@apollo/client` package.

## Decision

Always import React hooks and ApolloProvider from `@apollo/client/react`. Import core utilities (`gql`, `ApolloClient`, `InMemoryCache`, `HttpLink`) from `@apollo/client`.

## Pattern

```jsx
// ✅ Correct
import { gql } from '@apollo/client';
import { useQuery, useMutation, ApolloProvider } from '@apollo/client/react';

// ❌ Wrong (Apollo Client 4+)
import { gql, useQuery, useMutation, ApolloProvider } from '@apollo/client';
```

## Consequences

- Two import lines instead of one for Apollo Client in React components
- Clearer separation: core vs React-specific APIs
- Better tree-shaking for non-React environments

## References

- https://www.apollographql.com/docs/react
- ADR-009: Apollo Client 4 with Separate React Hooks Import
