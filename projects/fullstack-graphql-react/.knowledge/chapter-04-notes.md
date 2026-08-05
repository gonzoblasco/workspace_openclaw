# Chapter 4: Hooking Apollo into React

## Core Concepts

1. **Apollo Client:** GraphQL client for React with caching, error handling, and request management
2. **ApolloProvider:** React context provider that makes Apollo Client available to all components
3. **useQuery Hook:** Fetch data declaratively with loading/error/data states
4. **useMutation Hook:** Send mutations with cache update and optimistic UI
5. **Cache updates:** `cache.modify()` and `cache.writeFragment()` for efficient UI updates
6. **Optimistic UI:** Show result before server confirms, then replace with real data
7. **Polling:** `pollInterval` for periodic refetching
8. **Pagination:** `fetchMore()` with `updateQuery` for infinite scroll
9. **Apollo Client Devtools:** Chrome extension for inspecting queries, mutations, and cache

## Key Changes from Book

| Book (2020) | Modern (Aug 2026) | Reason |
|---|---|---|
| `import { useQuery } from '@apollo/client'` | `import { useQuery } from '@apollo/client/react'` | Apollo Client 4+ restructured exports |
| `ApolloProvider` from `@apollo/client` | `ApolloProvider` from `@apollo/client/react` | Same reason |
| `ReactDOM.render` | `createRoot` | Removed in React 19 |
| webpack + Babel | Vite 8 | Faster, zero-config |
| `react-helmet` | `react-helmet-async` | Unmaintained since 2020 |

## Architecture

```
React App
  └─ ApolloProvider (client)
       ├─ App
       │    ├─ Helmet (title/meta)
       │    ├─ Feed
       │    │    ├─ useQuery(GET_POSTS) → postsFeed
       │    │    ├─ useMutation(ADD_POST) → addPost
       │    │    ├─ InfiniteScroll → fetchMore
       │    │    └─ PostForm → handleSubmit
       │    └─ Chats
       │         ├─ useQuery(GET_CHATS) → chats
       │         ├─ openChat/closeChat state
       │         └─ Chat (per open chat)
       │              ├─ useQuery(GET_CHAT) → messages
       │              └─ useMutation(ADD_MESSAGE) → send
       └─ Apollo Client
            ├─ HttpLink → http://localhost:8000/graphql
            ├─ onError link
            └─ InMemoryCache
```

## ADRs Created
- ADR-009: Apollo Client 4 with Separate React Hooks Import

## Running the Chapter 4 Project

```bash
# Terminal 1: Start backend (chapter 3)
cd projects/fullstack-graphql-react/chapter-03
npm run seed
npm run server

# Terminal 2: Start frontend (chapter 4)
cd projects/fullstack-graphql-react/chapter-04
npm run dev
```

## Key Apollo Client APIs Used

| API | Purpose |
|---|---|
| `useQuery(query, { variables, pollInterval })` | Fetch data with auto-refetch |
| `useMutation(mutation, { update, optimisticResponse })` | Send mutations with cache update |
| `fetchMore({ variables, updateQuery })` | Pagination / infinite scroll |
| `cache.modify({ id, fields })` | Update specific cache entries |
| `cache.writeFragment({ data, fragment })` | Write new data to cache |
| `cache.readQuery({ query })` | Read existing cache data |
| `cache.identify(object)` | Get cache ID for an object |
