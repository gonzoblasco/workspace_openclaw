---
name: "review-quality"
description: "Pre-merge review: testing strategy, code review, security audit, and optional pre-deploy validation."
---

# Workflow: Review & Quality

## What it does

Quality review before merging or closing a cycle. Includes testing strategy, code review, security audit, and optional pre-deploy validation.

## Phases

### 1. Testing Strategy
Before reviewing the diff, establish the strategy:
- **TDD** — write test first, implement after
- **Unit testing** — test behaviors, not implementations
- **Integration testing** — API mocking, contract tests
- **E2E** — critical user flows
- **Coverage** — what to test (business logic, edge cases) and what not to (config, boilerplate)

### 2. Diff Analysis
Changes, files touched, impact.

### 3. Cognitive Lint
Conventions, naming, structure, tests. Verify the PR includes tests, they pass, they cover edge cases, there's coverage for the change.

### 4. Security Audit
Authentication, authorization, secrets, data leaks, access control. If the project is not multi-tenant, skip to basic audit (secrets, data leaks).

### 5. Product Review
Does it meet the spec? Does it satisfy the need?

### 6. Pre-Deploy Validation (optional, post-merge)
If deploying immediately:
- Build check — build without errors
- Route regression — public routes (200), protected (401/403)
- SEO audit — meta tags, OG images, sitemap
- API health — endpoints respond, auth works
- Performance — Lighthouse, lazy loading, bundle size
- Security scan — vulnerabilities, secrets in diff
- Cleanup — console.logs, commented code, temp files

### 7. Report
Findings, blockers, suggestions.

### 8. Gate
Blocks close if critical findings exist.

## Outputs
- Review report with testing, security, and product findings
- Decision: approve / changes requested / blocked
- (Optional) Pre-deploy validation report with Go/No-Go
