---
name: "security-audit"
description: "Auditar seguridad multi-tenant, auth guards, secrets, y fugas de datos en proyectos Supabase/PostgreSQL. Bloquea cierre de epics si hay hallazgos críticos."
---

# Security Audit — Threat Model & Hardening

Use when you need to audit the attack surface of code developed in a cycle — especially for multi-tenant Supabase projects. This skill operates under a specific backend threat model.

## When to use

- **Mandatory** before closing any epic or major feature in a multi-tenant project
- After implementing new API endpoints or data flows
- Before deploying to production
- When reviewing PRs that touch auth, data access, or external integrations

## How to invoke

```
@security-audit — audit the current branch's changes
@security-audit full — audit the entire project
```

Or reference this skill in a task prompt:
```
Read @security-audit and audit the new endpoints in this PR.
```

---

## Audit Vectors

### 1. Multi-Tenancy Data Leaks (Client Isolation)

**The Danger:** Using database clients with service role or superuser access (`service_role`, `admin_client`) bypasses Row-Level Security (RLS).

**Audit Rule:** Every query made through a bypass client _must_ include an explicit tenant/company filter in the `WHERE` clause.

**Invalid Code:**
```typescript
const { data } = await supabaseAdmin.from("records").select("*");
// ❌ Potential mass data leak — no tenant filter
```

**Secure Code:**
```typescript
const { data } = await supabaseAdmin
  .from("records")
  .select("*")
  .eq("company_id", currentCompany);
// ✅ Isolated to one tenant
```

### 2. Authentication Verification on Endpoints (Auth Guards)

**Audit Rule:** Every file inside API route directories must explicitly verify the requesting user's active session at the method's start, unless documented as a controlled public endpoint.

**Check for:**
- Missing `auth.uid()` or `getUser()` calls in protected routes
- Endpoints that accept `user_id` from the request body instead of deriving it from the session
- Public endpoints that should be protected

### 3. Internal Communication Secrets

**Audit Rule:** Endpoints for microservice communication, internal middlewares, or external webhooks must validate secret keys in request headers.

**Check for:**
- Missing `x-internal-secret` or `x-webhook-signature` validation
- Hardcoded secrets in source code
- Secrets in environment variables without validation

### 4. Sensitive Data Exposure in Client Layers (Frontend Leak)

**Audit Rule:** Data models returned to the web client must not carry credential columns, refresh tokens, password hashes, or raw third-party integration data.

**Check for:**
- Supabase queries that `select("*")` on tables with sensitive columns
- API responses that include `password_hash`, `refresh_token`, `stripe_secret_key`
- Over-fetching in TanStack Query or React Query

---

## Output Format

```markdown
## 🔒 Security Audit Report — [Scope]

### ✅ Passed Vectors
- [Vector name] — OK

### 🔴 Critical Findings (Blocking)
- **[File:Line]** — [Description]
  - **Vector:** [multi-tenancy | auth-guards | secrets | data-leak]
  - **Fix:** [What to do]

### 🟡 Warnings
- **[File:Line]** — [Description]

### 🛠️ FINAL VERDICT
[PASS / CRITICAL FAILURE]
```

## Blocking Rules

- Any finding in **Multi-Tenancy** or **Auth Guards** → **CRITICAL FAILURE**
- Critical failure blocks epic closure and deployment
- Warnings should be addressed but don't block

## Integration

This skill integrates with:
- **product-orchestrator** — called during Phase 4 (Orchestration) gate checks
- **agent-review** — supplements the review checklist with security-specific items
- **sdd-brownfield** — security specs should be documented in delta specs
