# Cleanup Checklist — Vibe Code Cleanup Reference

Checklist para cada fase de limpieza.

## Phase 1: Safety

- [ ] No hardcoded secrets in source
- [ ] No SQL injection vectors
- [ ] No XSS vectors
- [ ] Input validation exists
- [ ] Auth checks in place

## Phase 2: Structure

- [ ] No functions > 150 lines
- [ ] No files > 500 lines
- [ ] No dead code or commented code
- [ ] No duplicated code blocks
- [ ] Imports are clean (no unused)
- [ ] Exports are explicit

## Phase 3: Types

- [ ] No `any` types
- [ ] Function signatures typed
- [ ] API responses typed
- [ ] Event handlers typed
- [ ] Generic types constrained

## Phase 4: Consistency

- [ ] Naming conventions consistent
- [ ] Error handling pattern consistent
- [ ] File organization consistent
- [ ] Import order consistent
- [ ] Export pattern consistent

## Phase 5: Polish

- [ ] No console.log/debugger
- [ ] No unresolved TODOs/FIXMEs
- [ ] Loading states present
- [ ] Error states present
- [ ] Empty states present
- [ ] Edge cases handled

## Verification

- [ ] `npm run build` passes
- [ ] `npx tsc --noEmit` passes
- [ ] `npm test` passes
- [ ] `npm run lint` passes
- [ ] Behavior unchanged

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Diagnostic Patterns](./diagnostic-patterns.md) — Patrones de diagnóstico
