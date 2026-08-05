# Chapter 8: Routing in React

## Core Concepts

1. **Client-side routing:** Navigation without page reloads using HTML5 History API
2. **React Router v7:** Component-based routing with `BrowserRouter`, `Routes`, `Route`
3. **Parameterized routes:** `/user/:username` captures URL parameters
4. **Private routes:** Conditionally render based on auth state
5. **Programmatic navigation:** `useNavigate()` hook for button-based navigation
6. **Catch-all routes:** `path="*"` for 404 handling
7. **Remembering redirect location:** Save `location.state.from` for post-login redirect

## Key Changes from Book

| React Router v5 | React Router v7 | Reason |
|---|---|---|
| `Switch` | `Routes` | Renamed |
| `Redirect` | `Navigate` | Renamed |
| `withRouter` HOC | `useNavigate`, `useParams`, `useLocation` | Hooks are simpler |
| `history.push()` | `navigate()` | Hook-based |
| `match.params` | `useParams()` | Hook-based |
| `component={...}` | `element={...}` | JSX-based |
| `exact` prop | Default | Routes are exact by default |

## Routes

| Path | Component | Auth Required |
|---|---|---|
| `/` | LoginRegisterForm | No (redirects to /app if logged in) |
| `/app` | Main (Feed + Chats + Bar) | Yes |
| `/user/:username` | User (Profile + Feed + Chats) | Yes |
| `*` | Redirect to `/` | — |

## New Components

- `router.jsx` — Route definitions with PrivateRoute and LoginRoute guards
- `Main.jsx` — Logged-in layout (Bar + Feed + Chats)
- `User.jsx` — User profile page with `useParams`
- `UserProfile` — Fetches user data + filtered posts
- `UserProfileHeader` — Avatar + username display
- `FeedList` — Reusable infinite scroll post list
- `Home` — Navigation button using `useNavigate`

## Backend Changes (chapter-03)

- `user(username: String!): User @auth` query
- `postsFeed` now accepts optional `username` parameter for filtering

## Running

```bash
# Terminal 1: Backend
cd projects/fullstack-graphql-react/chapter-03
JWT_SECRET="***" npm run server

# Terminal 2: Frontend
cd projects/fullstack-graphql-react/chapter-04
npm run dev
```

Visit `/user/Test%20User` to see the profile page.
