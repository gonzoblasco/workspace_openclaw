# ADR-010 - Prefer `screen` Queries Over `render` Destructuring

**Status:** Accepted  
**Date:** 2026-08-05  
**Context:** React Testing Library's `render` function returns query methods that can be destructured. Many examples use this pattern, but the Testing Library documentation recommends using the `screen` object for most cases.  
**Decision:** Always use `screen.getByRole`, `screen.getByText`, etc. over destructuring queries from `render`.  
**Consequences:**
- More readable tests (the source of the query is explicit - `screen` is always the DOM)
- Avoids stale references when adding queries after the render call
- Consistent with current Testing Library best practices
- No need to update destructuring when adding new queries
- `screen` automatically uses `document.body`, which is where RTL renders

**Rationale:** The `screen` object is a singleton bound to `document.body`. Since RTL cleans up between tests by unmounting from `document.body`, `screen` always points to the right place. Destructuring from `render` requires keeping the destructured variables in sync and can lead to subtle bugs when queries are added later.

**Alternatives considered:**
- `render` destructuring: Works but is more error-prone and less explicit
- Custom wrapper: Overkill for standard cases

**Origin:** Simplify Testing with React Testing Library (Packt)
