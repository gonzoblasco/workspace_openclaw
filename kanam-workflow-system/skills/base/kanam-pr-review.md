# Kanam PR Review (Cognitive Pre-Merge Linter)

> **Universal pre-merge cognitive linter**: Analyzes complete branch diff against conventions, correctness, test coverage, security, and performance — blocks merge if any critical finding found

---

## Purpose

Act as automated second pair of eyes before code consolidation. Analyzes complete branch diff (`git diff main...HEAD`) against repository conventions, software engineering best practices, security controls, and performance metrics to prevent production-impacting issues in merge.

**Fusion source**: `workflow-kit/pr-review` + `antigravity/pr-review` (both repos contributed versions)

---

## Review Dimensions & Scoring Matrix

| Dimension | Description | Weight | Block Level | Action Required |
|-----------|-------------|--------|-------------|-----------------|
| **1. Functional Correctness** | Unhandled error routes, race conditions, inconsistent states | 20% | 🔴 CRITICAL (merge blocked) | Fix unhandled async paths or state inconsistency; add missing try/catch guards |
| **2. Test Coverage** | Business logic files lacking tests, critical path coverage gaps | 15% | 🟠 HIGH (merge requires fix) | Add tests for new/modified core logic; target ≥70% coverage on changed files |
| **3. Conventions & Architecture** | Breaking architectural decisions, debug code left behind, TODO markers | 15% | 🟡 MEDIUM (review req review) | Clean up dead code, remove console.log, align with architecture decision records |
| **4. Security (Layered)** | Hardcoded secrets/injections, missing auth guards, SQL/NoSQL injection vectors | 30% | 🔴 CRITICAL (merge blocked) | Remove hardcoded keys; add input validation/sanitization; implement auth guards on new routes |
| **5. Performance & Optimization** | Redundant loops, main thread mutations, inefficient database queries (N+1 problems) | 20% | 🟡 MEDIUM (review req review) | Optimize query patterns; refactor redundant iterations; add caching where appropriate |

### Scoring Formula

```
PR Risk Score = Σ(Dimension_i × Weight_i × Finding_Severity_i)
```

**Block Thresholds:**
- **CRITICAL**: Score ≥ 50 → **MERGE BLOCKED** (security or correctness issues)
- **HIGH**: Score ≥ 30 → Review required before merge
- **MEDIUM**: Score ≥ 15 → Recommend review but not blocking
- **LOW**: Score < 15 → Can proceed with caution

---

## Universal Review Checklist

Before analyzing PR diff, run through these dimensions:

### Dimension 1: Functional Correctness & Edge Cases

| Check | Question | Why Block? |
|-------|----------|------------|
| Unhandled errors | Does the code handle promises/async without `.catch` or try/catch blocks? | Runtime crashes, unexpected failures in production |
| State consistency | Could concurrent state modifications lead to race conditions? | Data corruption, silent bugs only reproducible intermittently |
| Null safety | Does the code assume `null`/`undefined` are always present where they may not be? | Reference errors, null pointer exceptions in async paths |

**Example problematic patterns:**
```typescript
// ❌ BAD: No error handling
async function fetchData() {
  const data = await someApi.get(); // What if this fails?
  return process(data); // Can throw if API fails
}

// ✅ GOOD: Proper error handling
async function fetchData() {
  try {
    const data = await someApi.get();
    return await process(data);
  } catch (error) {
    logger.error('Data fetch failed', error);
    return null; // Return safe default or handle appropriately
  }
}
```

### Dimension 2: Test Coverage Assessment

| Metric | Threshold | Action |
|--------|-----------|--------|
| Core logic files test coverage | ≥70% | Add tests if below threshold |
| New/modified feature tests | 100% | Write comprehensive tests before merge |
| Critical path coverage | ≥90% | Address coverage gaps in main business flows |

**Test requirement matrix:**

| File Category | Min Coverage | Required Test Type |
|---------------|--------------|---------------------|
| Core business logic files | 70%+ | Unit tests + integration tests |
| New/modified features | 100% | Unit, E2E (if user-facing), mock factories |
| Database/API layer changes | 80%+ | Mock factories, service layer tests |
| Utility/helper functions | 40% | Unit tests only |

### Dimension 3: Conventions & Architecture Cleanup

| Pattern | Find | Resolution |
|---------|------|------------|
| Debug code left behind | `console.log()`, `TODO: remove this`, `// FIXME` comments | Remove or comment appropriately; document if intentional blocker |
| Breaking architectural decisions | Violates documented architecture decision records | Align with ADRs, update architecture documentation if needed |
| Dead code paths | Unused variables/functions, unreachable code branches | Extract to separate function/files for refactoring or removal |

### Dimension 4: Security Layer Assessment (Most Critical)

| Vector | Check | Block Level | Why Block? |
|--------|-------|-------------|------------|
| **Hardcoded secrets** | Are credentials/tokens/API keys embedded in source code? | 🔴 CRITICAL | Exposes all deployed applications to unauthorized access |
| **Injection attacks** | Does user input get passed directly to database without sanitization? | 🔴 CRITICAL | SQL/NoSQL injection, command injection vulnerabilities |
| **Missing auth guards** | Are new endpoints protecting sessions before accessing user data? | 🔴 CRITICAL | Account takeover, session hijacking, unauthorized access |
| **Secrets in frontend** | Is sensitive data (credentials, tokens) sent to client-side code? | 🔴 CRITICAL | Client-side compromise, credential stuffing attacks |

**Security example patterns:**

```typescript
// ❌ BAD: Hardcoded secret (CRITICAL)
const AWS_SECRET_ACCESS_KEY = 'sk-1234567890abcdef'; // Never deploy this!

// ✅ GOOD: Use environment variable (blocked from source control)
const AWS_SECRET_ACCESS_KEY = process.env.AWS_SECRET_ACCESS_KEY;
```

### Dimension 5: Performance & Optimization Checks

| Issue | Detection Method | Fix Required |
|-------|-----------------|--------------|
| Redundant iterations | Profile with benchmark tests, review logic flow | Remove redundant loops; optimize query patterns |
| Main thread mutations | Check async/await chain depth, event loop activity | Move heavy operations to worker threads or separate service layers |
| N+1 database queries | Query execution profile, count WHERE clauses in each iteration | Apply caching layer, use eager loading or batch queries |

**Example performance issue:**
```typescript
// ❌ BAD: N+1 problem — O(N) queries for N records
const users = await db.select('user:id:name').limit(10);
for (const user of users) {
  const post = await db.get(`users/${user.id}/posts`); // 10 more queries!
}

// ✅ GOOD: Eager loading via join — O(1) query
const usersWithPosts = await db.select('user{id,name,posts{id,title}}')
  .limit(10);
```

---

## Unified Output Report Format

The skill must output a structured report using this Markdown template for all reviews:

```markdown
## 🔍 KANAM PR REVIEW REPORT — [Branch Name/Task Identifier]

### ✅ Positive Findings (PR Strengths)

- [Document design patterns or conventions correctly applied here]
- [Good modularization or separation of concerns identified]
- [Security guards properly implemented for new endpoints]

---

## 🔴 Blocking Findings (MERGE BLOCKED - Must Fix Before Merge)

| File | Line | Severity | Issue Description | Risk Level | Why Block? |
|------|------|----------|------------------|-------------|------------|
| `src/services/auth.ts` | 89 | CRITICAL | Hardcoded AWS_SECRET_ACCESS_KEY found | HIGH | Exposes all deployed services to unauthorized access |

> **Action Required**: Remove hardcoded secret, use process.env or environment variable references instead. Run security audit with `kanam-security-audit`.

---

## 🟡 Recommendations (Review Before Merge - Not Blocking)

| File | Line | Severity | Recommendation | Risk Level |
|------|------|----------|----------------|------------|
| `components/Navbar.tsx` | 45 | MEDIUM | Add focus-visible state for keyboard navigation | LOW |
| `routes/api/users/route.ts` | 123 | HIGH | Add authentication guard to verify session token before access | MEDIUM |

> These findings should be addressed during review process but don't block immediate merge. Recommend following up in next review cycle.

---

## 🔵 Technical Observations & Future Debt

| File | Line | Observation | Notes |
|------|------|-------------|-------|
| `src/utils/format.ts` | 156 | Potential performance bottleneck detected during benchmark run | Consider using Web Worker for heavy formatting operations |

> This represents future technical debt but not immediately blocking. Track in future sprint planning.

---

## 🛠️ VERDICT (Final Decision)

[APPROVED / REQUEST CHANGES]

**Status**: ${status}

If APPROVED: PR ready to merge without additional requirements.
If REQUEST_CHANGES: Specific issues identified above need resolution before merge. Priority order: CRITICAL → HIGH → MEDIUM → LOW.

---

## 🔒 Security Status Check

**Security Audit Pass/Fail**: ${security_status}

Kanam security audit integrated with this review process. If CRITICAL findings exist in multi-tenancy or auth guard dimensions, VERDICT auto-becomes REQUEST_CHANGES regardless of other factors.

---

### 📊 Risk Score Summary

| Dimension | Weight | Findings | Severity | Contribution |
|-----------|--------|----------|----------|-------------|
| Functional Correctness | 20% | X findings | Medium | ${contrib} points |
| Test Coverage | 15% | Y gaps | High | ${contrib} points |
| Conventions | 15% | Z issues | Low | ${contrib} points |
| Security | 30% | A criticals, B high-severity | CRITICAL/HIGH | ${contrib} points |
| Performance | 20% | C optimizations | Medium | ${contrib} points |

**Total Risk Score**: ${total_score} points

**Block Threshold**: ≥50 points = MERGE BLOCKED, <50 points = REVIEW REQUIRED
---

## Integration Points & Auto-Detection

Kanam PR review skill integrates automatically with:

- **kanam-copilot workflow**: Review triggered before merge if task is ready for consolidation
- **kanam-security-audit integration**: Security findings cross-referenced from security audit results
- **Git diff comparison**: Automatically analyzes `git diff main...HEAD` or provided diff input
- **Automated test suite execution**: Optional integration with existing test runners (Vitest, Jest)

When auto-triggered during PR lifecycle:

1. Skill reads branch diff automatically via git commands
2. Cross-references security audit findings from kanam-security-audit skill
3. Runs local linter before requesting reviewer approval
4. Generates unified report for team coordination
```

---

## Invocation Methods

### CLI Mode

```bash
kanam-pr-review --branch "[git-branch-name]" [--output-file path]

# Auto-detect branch from context (default behavior)
kanam-pr-review
```

### Integration Mode (Auto-triggered)

When Kanam PR review is active during a workflow:

1. **Before merge**: Skill automatically triggers pre-merge review check
2. **During team review**: Skill provides feedback if findings deviate from guidelines
3. **Post-review**: Skill recommends VERDICT based on accumulated risk score

### Integration with Security Audit

Kanam PR review automatically integrates with security audit results:

```bash
kanam-security-audit --target "[project]" > security-findings.json
kanam-pr-review --branch "[branch]" --security-check file:///path/to/security-findings.json
```

**Integration flow:**
1. `kanam-security-audit` scans project for vulnerabilities
2. Security findings exported to structured JSON format (CRITICAL, HIGH, MEDIUM severity)
3. `kanam-pr-review` integrates security findings into PR analysis
4. CRITICAL security findings auto-trigger merge block regardless of other factors

---

## Anti-Patterns (Do Not Do)

- ❌ Don't approve PR with hardcoded secrets found — this exposes all deployed code to unauthorized access
- ❌ Don't merge code without proper auth guards if new endpoints introduced — account takeover is a real threat
- ❌ Don't ignore CRITICAL risk scores regardless of business priority — security vulnerabilities can be exploited before next sprint
- ❌ Don't approve PR with missing tests on core business logic features — test coverage represents insurance against future bugs

---

*Last updated: 2026-07-19 • Kanam AI System v0.1 • Fusion source documented in MANIFESTO.md*
