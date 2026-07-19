# Kanam Security Audit (Threat Model & Hardening)

> **Universal threat model**: Multi-tenancy, auth guards, secrets, data leaks — applies to ALL Kanam projects regardless of framework

---

## Purpose

Perform deep, focused analysis of attack surface for code developed during Kanam cycles. Unlike general linters, this skill operates under specific backend threat model guaranteeing absolute data isolation (**Multi-Tenancy**) and system key integrity.

**Fusion source:** `workflow-kit/security-audit` + `antigravity/security-audit`

---

## Critical Inspection Vectors (Universal)

### 1. Multi-Tenancy Data Leaks (Client Isolation)

| Danger | Rule | Invalid Code | Secure Code |
|--------|------|---------------|-------------|
| Improper DB client use with service role/superuser (`service_role`, `admin_client`) bypasses RLS | Every query via bypass client **must** include explicit tenant/company filter in `WHERE` clause | `db.from('records').select('*')` ❌ (Potential mass leak) | `db.from('records').select('*').eq('company_id', current_company)` ✅ (Isolated) |

### 2. Authentication Verification on Endpoints (Auth Guards)

| Rule | Enforcement |
|------|-------------|
| Every file inside API route directories (`/api/v1/`, `/api/routes/`) must explicitly verify requesting user's active session at method's start, unless documented as controlled public endpoint | Auto-blob in Kanam copilot if guard missing on new endpoint |

### 3. Internal Communication Secrets Validation

| Rule | Example |
|------|---------|
| Endpoints designed for exclusive consumption between microservices, internal middlewares, or external webhooks (e.g., n8n automations, message queue triggers) **must** mandatorily validate presence and accuracy of secret keys in request headers | Validate `x-internal-secret` or `x-webhook-signature` header on all internal endpoints |

### 4. Sensitive Data Exposure in Client Layers (Frontend Leak)

| Rule | Enforcement |
|------|-------------|
| Verify data models returned to web client don't carry credential columns, refresh tokens, password hashes, or raw third-party integration data | All serialization to frontend **explicitly bounded** — strip PII before return |

### 5. Supply Chain & Dependency Leaks

| Rule | Check |
|------|-------|
| Every npm package in `package.json` must have: valid semver range, active maintainer (last commit <1yr), no known CVEs (npm audit --depth=3) | Reject packages with known vulnerabilities in critical deps |

### 6. Environment Secret Leakage (Local/Remote)

| Rule | Check |
|------|-------|
| `.env` files in production repos, `.env.example` must NEVER contain real secrets — only placeholders or env:variable references | Hardcoded AWS_SECRET_ACCESS_KEY = "sk-xxx" → RED FLAG |

---

## Universal Blocking Criteria

| Category | Block Level | Impact |
|----------|-------------|--------|
| **Multi-Tenancy leaks** | 🔴 CRITICAL | System-wide data breach |
| **Auth guard failures** | 🔴 CRITICAL | Account takeover, session hijacking |
| **Internal secret exposure** | 🟠 HIGH | Internal API compromise, unauthorized access |
| **Sensitive data frontend leak** | 🟡 MEDIUM | Credential stuffing, user PII exposure |
| **Dependency vulnerabilities** | 🟡 MEDIUM | Supply chain attack, code injection |

---

## Invocation

```bash
kanam-security-audit --target "[project or file path]" [--depth <number>]

# Auto-detect when no arguments provided (scans entire project)
kanam-security-audit
```

**Auto-mode defaults:**
- No arguments: Full security audit across entire project + all open PRs in Epic
- With `--target`: Deep dive on specific file or codebase path
- With `--depth <N>`: Reduce depth from default 3 to N (1=high, 2=medium, 3=default)

---

## Output Format

When executed via CLI or IDE analysis, skill generates unified security findings list. Any finding in **Multi-Tenancy** or **Auth Guards** category triggers automatic **CRITICAL FAILURE** status, blocking any attempt to execute `kanam-close-epic` without remediation:

```markdown
## 🔒 KANAM SECURITY AUDIT REPORT — [Project/Epic Name]

### ✅ Secure Areas Identified

- [List of secure patterns found and validated]

### 🔴 Critical Findings (CRITICAL FAILURE - Block Epic Closure)

| File | Line | Severity | Description | Risk Level |
|------|------|----------|-------------|------------|
| `src/routes/api/users/route.ts` | 42 | CRITICAL | Multi-tenancy leak: user queries lack company_id filter | HIGH |
| `.env.local` | N/A | CRITICAL | Hardcoded AWS_SECRET_ACCESS_KEY found | HIGH |

### 🟡 High Findings (Block before production deploy)

| File | Line | Severity | Description | Risk Level |
|------|------|----------|-------------|------------|
| `src/services/auth.ts` | 89 | HIGH | Missing auth guard on /api/v1/protected routes | MEDIUM |

### 🟢 Medium Findings (Address before security audit close)

- [List of medium-priority findings]

### 🛠️ REMEDIATION PLAN REQUIRED

**BLOCKER:** Critical findings require immediate fix before `kanam-close-epic` can succeed.

1. Fix multi-tenancy leak: Add company_id filter to all queries
2. Remove hardcoded secrets from .env.local; use env:variable references or Kubernetes Secrets mount
3. Implement auth guards on protected endpoints
4. Re-run audit after fixes with `kanam-security-audit --fix`

**VERIFICATION:** Run security audit again post-fix and confirm **ALL CRITICAL findings cleared**.

---

## Integration Points

When Kanam security audit is active in workflow:

1. **Pre-epic closure mandatory**: Never close Epic without running `kanam-security-audit` first
2. **CRITICAL findings block epic**: Any multi-tenancy or auth guard failure blocks `kanam-close-epic` execution
3. **Auto-fix loop**: `kanam-security-audit --fix` applies basic fixes (remove hardcoded secrets, add tenant filters)

---

## Anti-Patterns (Do Not Do)

- ❌ Don't skip security audit for "speed" — multi-tenancy leaks cost orders of magnitude more than dev time
- ❌ Don't assume .env files are safe in production repos
- ❌ Don't deploy with hardcoded secrets anywhere (local, staging, or production)

---

*Last updated: 2026-07-19 • Kanam AI System v0.1 • Fusion source documented in MANIFESTO.md*
