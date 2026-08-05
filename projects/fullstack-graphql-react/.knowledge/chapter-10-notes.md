# Chapter 10: Real-Time Subscriptions

## Core Concepts

1. **WebSockets:** Bidirectional communication channel (ws:// instead of http://)
2. **PubSub:** Publish-subscribe pattern for broadcasting events
3. **graphql-ws:** Modern WebSocket library for GraphQL
4. **GraphQLWsLink:** Apollo Client link for subscriptions
5. **subscribeToMore:** Subscribe to updates and merge with existing query data
6. **withFilter:** Filter subscription events per-user (authorization)
7. **useSubscription:** React Hook for subscription data
8. **react-toastify:** Toast notifications for new messages

## Key Changes from Book

| Book (deprecated) | Modern (Aug 2026) | Reason |
|---|---|---|
| `subscriptions-transport-ws` | `graphql-ws` | Deprecated |
| `SubscriptionServer` | `useServer` from `graphql-ws/use/ws` | New API |
| `WebSocketLink` from `@apollo/client/link/ws` | `GraphQLWsLink` from `@apollo/client/link/subscriptions` | New package |
| `SubscriptionClient` | `createClient` from `graphql-ws` | New API |
| Sequelize `findOne` | Drizzle `db.select().where().get()` | ORM change |

## Architecture

```
┌──────────┐     HTTP (queries/mutations)     ┌──────────┐
│  Client  │ ──────────────────────────────▶  │  Server  │
│          │                                  │          │
│  Apollo  │     WebSocket (subscriptions)    │  Apollo  │
│  Client  │ ◀══════════════════════════════  │  Server  │
│          │     ws://host/subscriptions      │          │
│  wsLink  │                                  │  PubSub  │
└──────────┘                                  └──────────┘
```

## Subscription Flow

```
1. Client connects to ws://host/subscriptions with JWT
2. Server verifies JWT in onConnect → sets ctx.user
3. Client subscribes to messageAdded channel
4. User sends message → addMessage mutation
5. Mutation publishes to 'messageAdded' via pubsub.publish()
6. Server sends WebSocket frame to all subscribed clients
7. withFilter checks if client should receive the message
8. Client's subscribeToMore updateQuery merges new data
9. UI updates in real-time
```

## New/Modified Files

### Backend (chapter-03)
- `services/subscriptions/index.js` — WebSocket server with graphql-ws
- `services/index.js` — Added subscriptions service
- `server/index.js` — Uses createServer + switch for services
- `schema.js` — Added RootSubscription type
- `resolvers.js` — Added PubSub, messageAdded subscription, publish in addMessage

### Frontend (chapter-04)
- `apollo/index.js` — Added GraphQLWsLink + split for subscriptions
- `apollo/subscriptions/messageAdded.js` — Subscription query + hook
- `Chats.jsx` — subscribeToMore for real-time chat updates
- `apollo/mutations/addMessage.js` — Exported NEW_MESSAGE fragment

## Running

```bash
# Terminal 1: Backend
cd projects/fullstack-graphql-react/chapter-03
JWT_SECRET="***" npm run server

# Terminal 2: Frontend
cd projects/fullstack-graphql-react/chapter-04
npm run dev
```

Open two browser windows with different users — messages appear in real-time.
