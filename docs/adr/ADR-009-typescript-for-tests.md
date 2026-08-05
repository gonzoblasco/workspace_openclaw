# ADR-009 — Use TypeScript for All Test Files

**Status:** Accepted  
**Date:** 2026-08-05  
**Context:** Many testing tutorials and books still use JavaScript for test files. Modern React development is predominantly TypeScript, and test files benefit from the same type safety.  
**Decision:** All test files in new React projects should be TypeScript (.test.ts / .test.tsx).  
**Consequences:**
- Better IDE support (autocomplete, refactoring, type checking)
- Catches type errors at compile time before tests run
- Vitest handles .tsx natively with zero configuration
- Slightly more verbose but the safety outweighs the verbosity
- Consistent with the rest of the codebase

**Alternatives considered:**
- JavaScript with JSDoc: Less strict, harder to maintain at scale
- Plain JavaScript: Faster to write but loses type safety

**Origin:** Simplify Testing with React Testing Library (Packt)
