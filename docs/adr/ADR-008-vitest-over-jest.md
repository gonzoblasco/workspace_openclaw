# ADR-008 — Replace Jest with Vitest

**Status:** Accepted  
**Date:** 2026-08-05  
**Context:** Jest has been the standard test runner for React projects, but it has slower startup times, weaker ESM support, and a heavier configuration surface compared to modern alternatives.  
**Decision:** Use Vitest instead of Jest for new React projects. Vitest provides a compatible API (describe/it/expect), is significantly faster (native ESM, esbuild transform), and integrates natively with Vite-based tooling.  
**Consequences:**
- All Jest-specific imports (`@jest/globals`) replaced with Vitest globals
- jest-dom setup works identically (`import '@testing-library/jest-dom/vitest'`)
- Test files use `.test.tsx` extension, Vitest auto-discovers them
- No jsdom configuration needed — Vitest handles it via `environment: 'jsdom'`
- Migration path: Vitest supports Jest globals out of the box, so test code is nearly identical
- CI pipelines benefit from faster startup (Vitest starts in ~200ms vs Jest's ~2s)

**Alternatives considered:**
- Jest with `@swc/jest`: Faster than default Jest but still heavier than Vitest
- Node native test runner: Lacks the rich matcher ecosystem and DOM environment support

**Origin:** Simplify Testing with React Testing Library (Packt)
