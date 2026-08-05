# ADR-014: GraphQL Subscriptions with graphql-ws Instead of subscriptions-transport-ws

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 10
**Scope:** Global

## Context

The book uses `subscriptions-transport-ws` (deprecated) and `SubscriptionServer` for WebSocket subscriptions. The package is no longer maintained.

## Decision

Use `graphql-ws` (server) + `@apollo/client/link/subscriptions` (client) for WebSocket subscriptions. Use `graphql-subscriptions` with PubSub for the publish-subscribe system.

## Rationale

- `subscriptions-transport-ws` is deprecated and unmaintained
- `graphql-ws` is the modern, maintained WebSocket library for GraphQL
- Apollo Client 4+ has built-in `GraphQLWsLink` for `graphql-ws` integration
- `graphql-subscriptions` with PubSub is still the standard for in-memory pub/sub
- Same concepts: subscribe, publish, filter — only the transport changed

## Key API Changes

| Book (deprecated) | Modern | Reason |
|---|---|---|
| `subscriptions-transport-ws` | `graphql-ws` | Deprecated |
| `SubscriptionServer` | `useServer` from `graphql-ws/use/ws` | New API |
| `WebSocketLink` from `@apollo/client/link/ws` | `GraphQLWsLink` from `@apollo/client/link/subscriptions` | New package |
| `SubscriptionClient` | `createClient` from `graphql-ws` | New API |
| `onConnect` returns object | `onConnect` sets `ctx.user` | Different context pattern |

## Pattern

```js
// Server
import { useServer } from 'graphql-ws/use/ws';
import { WebSocketServer } from 'ws';

const wsServer = new WebSocketServer({ server, path: '/subscriptions' });
useServer({ schema, execute, subscribe, onConnect, context }, wsServer);

// Client
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';

const wsLink = new GraphQLWsLink(createClient({
  url: 'ws://localhost:8000/subscriptions',
  connectionParams: { authToken: localStorage.getItem('jwt') },
}));
```

## References

- https://github.com/enisdenjo/graphql-ws
- https://www.apollographql.com/docs/react/data/subscriptions
