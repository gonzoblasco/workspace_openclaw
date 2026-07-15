---
name: "pr-review"
description: "Cognitive pre-merge linter — analiza el diff completo contra convenciones, seguridad, tests, y performance antes de mergear."
---

# PR Review — Cognitive Pre-Merge Linter

Use as a second pair of eyes before merging any PR. Analyzes the full branch diff against repository conventions and engineering best practices.

## When to use

- **Mandatory** before merging any PR to `main`
- After implementing a feature or fix
- When reviewing PRs from other contributors
- As a gate in the product-orchestrator workflow

## How to invoke

```
@pr-review — review the current branch diff
@pr-review --full — review including all files (not just diff)
```

Or reference in a task prompt:
```
Run @pr-review on this PR before merging.
```

---

## Audit Dimensions

### 1. Functional Correctness and Edge Cases

- Unhandled error paths: promises without `.catch` or `try/catch`
- `null`/`undefined` values that could break the flow
- Potential race conditions or inconsistent client/server states
- Missing loading, empty, and error states in UI components

### 2. Test Coverage

- Core business logic or new endpoints should have corresponding tests
- Lack of coverage in critical components is **blocking**
- Tests should cover: happy path, error path, edge cases

### 3. Conventions, Architecture, and Cleanliness

- Code follows project conventions (naming, folder structure, patterns)
- No residual `console.log`, debug comments, or dead code
- No commented-out code blocks
- Imports are clean (no unused imports, no wildcard imports where specific ones suffice)

### 4. Security (Early Layer)

- **Secrets:** No hardcoded credentials, tokens, or API keys
- **Injections:** User inputs are typed, validated, or sanitized before touching databases or system operations
- **Auth guards:** Every new route has its corresponding middleware or session validation
- **RLS:** Supabase queries respect Row-Level Security

### 5. Performance

- No unnecessary iterations or heavy main-thread mutations
- No N+1 database queries (check for loops with individual queries)
- No large bundle additions without code splitting
- Memoization where appropriate (React: `useMemo`, `useCallback`)

---

## Output Format

```markdown
## 🔍 Code Review Report — [Branch/Task]

### ✅ Positives
- [Design strengths, modularity, or good practices applied]

### 🔴 Blocking Findings (Require Mandatory Fix)
- **[File:Line]** — [Description of security, build, or severe logic issue]

### 🟡 Suggested Improvements (Do Not Block Merge)
- **[File:Line]** — [Readability recommendation, minor optimization, or future refactor]

### 🔵 Technical Notes / Debt
- [Contextual notes on architecture or long-term behavior]

### 🛠️ FINAL VERDICT
[APPROVED / REQUEST CHANGES]
```

## Blocking Rules

- **Secrets in code** → always blocking
- **Missing auth guards on protected routes** → always blocking
- **Build-breaking changes** → always blocking
- **Missing test coverage on critical logic** → blocking
- **Console.log / debug artifacts** → warning (non-blocking)
- **Style nits** → suggestion (non-blocking)

## Integration

This skill integrates with:
- **agent-review** — supplements the review checklist with PR-specific items
- **product-orchestrator** — called during Phase 4 gate checks before phase completion
- **oss-contribute** — used for self-review before submitting PRs to external repos
