# ADR-011 - Use `userEvent` Over `fireEvent` for User Simulations

**Status:** Accepted  
**Date:** 2026-08-05  
**Context:** React Testing Library provides two APIs for simulating user interactions: `fireEvent` (lower-level, synchronous) and `userEvent` (higher-level, async). Many older examples use `fireEvent`, but `@testing-library/user-event` is the recommended replacement.  
**Decision:** Use `userEvent` from `@testing-library/user-event` instead of `fireEvent` for all user interaction simulations.  
**Consequences:**
- More realistic event simulation (keyboard events, focus/blur chains, pointer events)
- Slightly different API (async by default, needs `await`)
- Catches more edge cases that `fireEvent` misses (e.g., a button that's disabled via `pointer-events: none` but not the `disabled` attribute)
- `fireEvent` still available for edge cases where `userEvent` doesn't apply (e.g., testing low-level event handlers directly)
- Requires `userEvent.setup()` call before each test or test group

**Key differences:**
- `fireEvent.click(element)` → `await user.click(element)`
- `fireEvent.change(input, { target: { value } })` → `await user.type(input, value)`
- `fireEvent` dispatches a single event; `userEvent` dispatches the full chain (focus, keydown, input, keyup, blur, etc.)

**Alternatives considered:**
- `fireEvent`: Simpler API but less realistic; misses real browser behavior
- Playwright's component testing: Overkill for unit/integration tests

**Origin:** Simplify Testing with React Testing Library (Packt)
