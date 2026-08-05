# ADRs — Simplify Testing with React Testing Library

## Project-Specific ADRs

These decisions are specific to this project's structure and context. General-purpose ADRs have been migrated to `docs/adr/` (see references below).

### ADR-001 — Use React 19 + @testing-library/react Latest

**Status:** Accepted  
**Date:** 2026-08-05  
**Context:** The book was written for an earlier React version. React 19 is current LTS as of August 2026.  
**Decision:** Use React 19 and the latest compatible @testing-library/react.  
**Consequences:**
- `act()` wrapping is less necessary in React 19 (automatic batching improvements)
- `render` and `screen` APIs remain stable
- No breaking changes expected for the patterns in this book

### ADR-002 — Monorepo Structure per Chapter

**Status:** Accepted  
**Date:** 2026-08-05  
**Context:** Each chapter of the book has independent examples. A monorepo structure keeps everything in one place while maintaining isolation.  
**Decision:** Each chapter gets its own directory under `chapters/` with its own source and test files. A single root `package.json` manages dependencies.  
**Consequences:**
- Single `npm install` for all chapters
- Shared Vitest config and setup
- Chapters can share utilities as the book progresses
- Easy to run all tests at once or per-chapter

## References to Global ADRs

These general decisions were migrated to `docs/adr/` in the workspace root:

| Global ADR | Title | File |
|---|---|---|
| ADR-008 | Replace Jest with Vitest | [docs/adr/ADR-008-vitest-over-jest.md](../../../docs/adr/ADR-008-vitest-over-jest.md) |
| ADR-009 | TypeScript for test files | [docs/adr/ADR-009-typescript-for-tests.md](../../../docs/adr/ADR-009-typescript-for-tests.md) |
| ADR-010 | Prefer screen queries over render destructuring | [docs/adr/ADR-010-screen-queries-over-destructuring.md](../../../docs/adr/ADR-010-screen-queries-over-destructuring.md) |
| ADR-011 | Use userEvent over fireEvent | [docs/adr/ADR-011-userevent-over-fireevent.md](../../../docs/adr/ADR-011-userevent-over-fireevent.md) |
| ADR-012 | Use jest-dom matchers for DOM assertions | [docs/adr/ADR-012-jest-dom-matchers.md](../../../docs/adr/ADR-012-jest-dom-matchers.md) |
