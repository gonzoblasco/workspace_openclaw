# ADR-012: React Router v7 with Component-Based Routing

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 8
**Scope:** Global

## Context

The book uses React Router v5 with `Switch`, `BrowserRouter`, `Route`, `Redirect`, and `withRouter` HOC. React Router has evolved significantly since v5.

## Decision

Use React Router v7 in SPA mode with component-based routing (`BrowserRouter`, `Routes`, `Route`, `Navigate`, `useNavigate`, `useParams`).

## Rationale

- React Router v5 is outdated (2019)
- React Router v7 supports both SPA and framework modes
- Component-based routing is simpler than HOC-based (`withRouter`)
- `useNavigate` replaces `history.push()`
- `useParams` replaces `match.params`
- `Navigate` replaces `Redirect`
- `Routes` replaces `Switch`

## Key API Changes

| React Router v5 | React Router v7 | Reason |
|---|---|---|
| `Switch` | `Routes` | Renamed |
| `Redirect` | `Navigate` | Renamed, uses `replace` prop |
| `withRouter` HOC | `useNavigate`, `useParams`, `useLocation` hooks | Hooks are simpler |
| `history.push()` | `navigate()` | Hook-based |
| `match.params` | `useParams()` | Hook-based |
| `component={...}` | `element={...}` | JSX-based |
| `exact` prop | Default behavior | Routes are exact by default |

## Pattern

```jsx
// React Router v7
import { BrowserRouter, Routes, Route, useParams, useNavigate } from 'react-router-dom';

function UserPage() {
  const { username } = useParams();
  const navigate = useNavigate();
  return <button onClick={() => navigate('/app')}>Home</button>;
}

<BrowserRouter>
  <Routes>
    <Route path="/user/:username" element={<UserPage />} />
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
</BrowserRouter>
```

## References

- https://reactrouter.com
