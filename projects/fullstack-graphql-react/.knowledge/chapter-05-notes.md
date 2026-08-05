# Chapter 5: Reusable React Components and React Hooks

## Core Concepts

1. **Controlled vs Uncontrolled components:** State-driven vs DOM-ref inputs
2. **Functional components:** Hooks enable state in function components
3. **Conditional rendering:** `{condition && <Component />}` pattern
4. **Children pattern:** `{children}` for composable components
5. **GraphQL Fragments:** Reusable field selections across queries
6. **Custom Hooks:** Wrapping `useQuery`/`useMutation` with pre-configured options
7. **React Context API:** Global state without prop drilling
8. **Apollo Consumer:** Access Apollo cache directly
9. **PropTypes:** Runtime type checking for component props
10. **React Styleguidist:** Auto-generated component documentation

## Key Refactorings Applied

| Pattern | Before | After |
|---|---|---|
| GraphQL queries | Inline in components | `apollo/queries/*.js` with fragments |
| GraphQL mutations | Inline `useMutation` | `apollo/mutations/*.js` with custom hooks |
| Loading state | `return 'Loading...'` | `<Loading />` component |
| Error state | `return 'Error! ...'` | `<ErrorMessage>` component |
| Post rendering | Raw JSX in map loop | `<Post>` component with `<PostHeader>` + `<PostContent>` |
| Dropdown menu | Not implemented | `<Dropdown>` helper component |
| Delete post | Not implemented | `deletePost` mutation + cache update |
| User search | Not implemented | `usersSearch` query + `<SearchBar>` + `<SearchList>` |
| Top bar | Not implemented | `<Bar>` component |
| Global user | Not implemented | `UserProvider` + `UserConsumer` (Context API) |

## New Backend Features Added (chapter-03)

- `deletePost(postId: Int!): Response` mutation
- `usersSearch(page, limit, text): UsersSearch` query with LIKE search
- `Response` type with `success: Boolean`

## ADRs Created
- (No new ADRs — this chapter is about code organization patterns, not tooling changes)

## Running the Chapter 4/5 Project

```bash
# Terminal 1: Start backend (chapter 3)
cd projects/fullstack-graphql-react/chapter-03
npm run seed
npm run server

# Terminal 2: Start frontend (chapter 4)
cd projects/fullstack-graphql-react/chapter-04
npm run dev
```

## File Structure (after refactoring)

```
src/
├── apollo/
│   ├── fragments/
│   │   └── userAttributes.js
│   ├── queries/
│   │   ├── getPosts.js
│   │   ├── getChats.js
│   │   ├── getChat.js
│   │   └── searchQuery.js
│   ├── mutations/
│   │   ├── addPost.js
│   │   ├── deletePost.js
│   │   └── addMessage.js
│   └── index.js
├── components/
│   ├── bar/
│   │   ├── index.jsx
│   │   ├── search.jsx
│   │   └── searchList.jsx
│   ├── post/
│   │   ├── index.jsx
│   │   ├── header.jsx
│   │   └── content.jsx
│   ├── Dropdown.jsx
│   ├── ErrorMessage.jsx
│   ├── Loading.jsx
│   └── fontawesome.js
├── context/
│   └── user.jsx
├── App.jsx
├── Feed.jsx
├── Chat.jsx
├── Chats.jsx
└── main.jsx
```
