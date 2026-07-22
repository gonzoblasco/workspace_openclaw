---
name: "vibe-code-cleanup"
description: "Clean up AI-generated code for production: diagnose, clean, refactor, and harden."
---

# Workflow: Vibe Code Cleanup

## What it does

Take AI-generated code (vibe coding) and bring it to a production-ready state: no technical debt, with types, tests, and solid structure.

## Philosophy

> Surgery, not demolition. Remove only what is provably dead. Preserve everything else.

- Atomic commits (one change per commit)
- Validate after each batch
- Never change observable behavior
- Prefer shared helpers over duplicated code

## Phases

### 1. Diagnosis
Scan codebase and detect technical debt patterns:
- **Structure** — unused files, dead imports, commented code
- **Types** — untyped `any`, incorrect types, missing types
- **Security** — hardcoded secrets, SQL injection, XSS
- **Performance** — large bundles, N+1 queries, no lazy loading
- **Maintainability** — long functions (>150 lines), duplication, unclear names

Quick initial scan (60 seconds): count files and lines, identify language/framework, detect red flags (hardcoded secrets, TODOs, commented code).

### 2. Reconnaissance
Map the codebase before touching anything:
- Routes and pages
- APIs and endpoints
- Components and dependencies
- Environment variables
- Entry points and data flow

### 3. Cleanup
- Remove dead imports and orphaned files
- Consolidate duplication into shared helpers
- Standardize imports and exports
- Clean console.logs, commented code, temp files
- Update .gitignore if needed

### 4. Refactor
Incremental refactoring with atomic commits:
- Extract repeated logic to shared utilities
- Split components > 150 lines into sub-components
- Unify error handling
- Replace `any` with explicit types
- One refactor per commit

### 5. Hardening
- Strict type checking (no `any`)
- Tests for core business logic
- Updated dependencies
- Release hygiene (changelog, versioning)

### 6. Verification
```bash
npm run build      # must pass without errors
npx tsc --noEmit   # typecheck
npm test           # tests passing
npm run lint       # no errors
```

## Outputs
- Diagnosis report with prioritized issues
- Cleanup and refactor commits
- Build + typecheck + tests green
- Changelog updated
