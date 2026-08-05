# Chapter 6: Authentication with Apollo and React

## Core Concepts

1. **JWT (JSON Web Token):** Stateless authentication token with header, payload, and signature
2. **localStorage vs Cookies:** Tradeoffs between XSS vulnerability and CSRF protection
3. **bcrypt:** Password hashing with salt — never store plain passwords
4. **Auth directive:** `@auth` GraphQL directive for declarative authentication
5. **AuthLink:** Apollo Client link that attaches JWT to every request
6. **Context-based auth:** Server extracts user from JWT and adds to request context
7. **Conditional rendering:** Show login form or app based on auth state
8. **Logout:** Remove JWT, clear Apollo cache, reset store

## Key Changes from Book

| Book (2020) | Modern (Aug 2026) | Reason |
|---|---|---|
| `withApollo` HOC | `useApolloClient` hook | Removed in Apollo Client 4 |
| `ApolloConsumer` | `useApolloClient` | Removed in Apollo Client 4 |
| Sequelize `Op.like` | Drizzle `like()` | ORM change |
| `bcrypt.compare` (async) | `bcrypt.compareSync` | better-sqlite3 is sync |
| Sequelize `User.findAll` | Drizzle `db.select().from(users)` | ORM change |
| Sequelize `User.create` | Drizzle `db.insert(users).values()` | ORM change |

## Authentication Flow

```
1. User submits login form → login mutation
2. Server validates email + password → returns JWT
3. Client stores JWT in localStorage
4. AuthLink attaches JWT to every subsequent request
5. Server verifies JWT → adds user to context
6. @auth directive checks context.user → allows/denies access
7. On logout: remove JWT, clear cache, reset store
```

## Backend Changes (chapter-03)

- Added `email` and `password` fields to users table
- `login(email, password): Auth` mutation
- `signup(username, email, password): Auth` mutation
- `currentUser: User @auth` query
- `@auth` directive for schema-level authentication
- JWT verification in request context
- All queries/mutations now use `context.user` instead of first user

## Frontend Changes (chapter-04)

- `LoginRegisterForm` component with login/signup toggle
- `AuthLink` in Apollo Client setup
- `Logout` button in top bar
- Conditional rendering based on `loggedIn` state
- `useCurrentUserQuery` for fetching logged-in user
- `onClearStore` listener for auto-logout on token expiry
- Error handling for UNAUTHENTICATED responses

## Running

```bash
# Terminal 1: Backend
cd projects/fullstack-graphql-react/chapter-03
JWT_SECRET="your-secret-key" npm run seed
JWT_SECRET="your-secret-key" npm run server

# Terminal 2: Frontend
cd projects/fullstack-graphql-react/chapter-04
npm run dev
```

Test credentials: `test1@example.com` / `123456789`
