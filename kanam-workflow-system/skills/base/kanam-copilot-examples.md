# Kanam Copilot — Examples & Usage Patterns

> Neutral LLM context examples: qwen3.5-4b-mlx, deepseek-v4-flash, Claude Code

---

## Example 1: First Task Initialization with qwen3.5-4b-mlx

```markdown
### KANAM WORKFLOW INITIALIZATION — qwen3.5 Context

**Project**: brainweb (AI notes app)
**Model**: qwen3.5-4b-mlx (local, macOS 27.0)
**Task**: T0X — AI Copilot Drawer feature integration

### Pre-Flight Validation Report

```text
KANAM PRE-FLIGHT [brainweb]
══════════════════════════════
[✓] SKILL.md read: kanam-workflow-system/README.md
[✓] .kanam/AGENT_TASKS.md reviewed: brainweb tasks list
[✓] Style guide assimilated: tailwind v4 + shadcn components
[✓] Mockups/API contracts located: API spec at docs/api-contracts.md
[✓] Epic/Task branch created correctly: e4/t11-ai-copilot-drawer
[✓] main branch clean and up to date: confirmed via git pull
[✓] Dependencies confirmed: kanam-copilot v0.1, deepseek integration ready

FIRST TASK SELECTED: T0X · AI Copilot Drawer
AWAITING DEVELOPER CONFIRMATION TO START.
```

### First Steps for qwen3.5-4b-mlx Implementation

**Step 1**: Create isolated branch for task implementation
```bash
git checkout -b "e4/t11-ai-copilot-drawer"
```

**Step 2**: Run kanam-copilot auto-mode to confirm scoping
```bash
kanam-copilot --task T0X:"AI Copilot Drawer feature"
```

**Expected qwen3.5 response**: 
- "Branch created at e4/t11-ai-copilot-drawer ✓"
- "Pre-flight validation complete, ready to implement"

**Step 3**: Implement with atomic scope restrictions
```typescript
// Only work on files related to T0X task scope:
// - src/components/DrawingPanel.tsx
// - src/hooks/useDrawingState.ts
// Do NOT refactor unrelated components (feature creep violation)
```

---

## Example 2: Deepseek-v4 Flash Integration with CRITICAL Security Findings

```markdown
### KANAM SECURITY AUDIT — deepseek-v4-flash Context

**Project**: kanam-workflow-system (base skills)
**Model**: deepseek-v4-flash (cloud, API integration)
**Audit Target**: base skill fusion migration PR #127

### CRITICAL Findings Report

| Severity | File | Line | Issue | Block Level |
|----------|------|------|-------|-------------|
| CRITICAL | src/security/multi-tenancy.ts | 89 | Missing company_id filter on all DB queries | 🔴 MERGE BLOCKED |
| HIGH | package.json | N/A | Vulnerability: express@4.18.2 has CVE-2024-XXXX | 🟠 REVIEW REQUIRED |

### Security Audit Block Status

```markdown
## 🔍 DEEPSEEK KANAM SECURITY AUDIT REPORT — kanam-workflow-system PR #127

### 🔴 CRITICAL Findings (MERGE BLOCKED - Must Fix)

| File | Line | Severity | Issue Description | Risk Level |
|------|------|----------|------------------|-------------|
| src/security/multi-tenancy.ts | 89 | CRITICAL | Missing company_id filter on all queries via service_role client | HIGH |

**VERDICT**: MERGE BLOCKED — CRITICAL security finding requires immediate fix.
```

### Required Fix Before Deepseek-v4 Integration

```typescript
// BEFORE (vulnerable):
const records = await db.from('records').select('*'); // ❌ Exposes all company data

// AFTER (secure, qwen3.5-4b-mlx compatible):
const records = await db.from('records')
  .select('*')
  .eq('company_id', current_user.company_id); // ✅ Isolated per tenant

// Run security audit after fix:
kanam-security-audit --target "src/security/multi-tenancy.ts" --fix
```

### qwen3.5 Integration Workflow

After fixing critical findings:

1. **qwen3.5 auto-mode triggers**: `kanam-copilot` confirms scoping changes
2. **Security audit pass**: `kanam-security-audit --quiet` returns no CRITICAL findings
3. **PR review approved**: `kanam-pr-review` returns APPROVED verdict
4. **Safe to merge**: Both security and functional reviews passed

---

## Example 3: Full Workflow from qwen3.5 Task Init to Epic Closure

```markdown
### COMPLETE KANAM WORKFLOW — qwen3.5-4b-mlx End-to-End

**Project**: brainweb (AI notes app)
**Model**: qwen3.5-4b-mlx (local workspace, macOS 27.0)
**Epic**: T04 — AI Assistant Features
**Task Lifecycle**: T0X through to v1.0.0 release

---

### Phase 1: Task Initialization (kanam-new-task)

```bash
# qwen3.5-4b-mlx reads SKILL.md and asks scoping questions:
> What Epic context should I initialize the task for?
brainweb — T04 AI Assistant Features

> What's the short description of this task?
AI Copilot Drawer feature integration with draft state tracking

> Are there any dependencies or blockers I should be aware of?
T08 completed (base auth), need access to existing draft storage schema
```

**Branch created**: `e4/t11-ai-copilot-drawer`

---

### Phase 2: Pre-Flight & Gate Execution (kanam-copilot)

```bash
# qwen3.5 auto-mode with pre-flight validation
> Pre-flight checklist items:
[✓] SKILL.md read — workflow rules understood
[✓] .kanam/AGENT_TASKS.md reviewed — current Epic context clear
[✓] Branch structure validated — e4/t11-ai-copilot-drawer exists
[✓] Dependencies confirmed — draft storage schema accessible

> Ready to implement T0X. What should I focus on first?
```

**qwen3.5 implementation**: 
- Create atomic drawing panel component
- Implement useDrawingState hook with localStorage integration
- Connect to kanam-copilot API endpoint for draft storage

---

### Phase 3: Security Audit (kanam-security-audit)

```bash
# qwen3.5 security scanning before merge
> Run full security audit on task changes?
yes — deepseek-v4 flash auto-integration available for CRITICAL findings check

KANAM SECURITY AUDIT REPORT — brainweb T0X task

✅ Secure Areas Identified:
- Proper multi-tenancy isolation with company_id filter
- Auth guards implemented on all drawing routes
- No sensitive data exposed to frontend layer

🟢 Low-Priority Findings:
- Could add additional logging for security audit trail (not critical)

**VERDICT**: SAFE TO PROCEED — no CRITICAL findings requiring merge block
```

---

### Phase 4: PR Review & Closure (kanam-pr-review, kanam-close-epic)

```bash
# qwen3.5 pre-merge review
> Run pre-merge cognitive review on branch?
yes

KANAM PR REVIEW REPORT — brainweb T0X task closure

✅ Positive Findings:
- Excellent modularization with separation of drawing logic and storage layer
- Strong security guards implemented, no hardcoded secrets found
- Clear documentation in docs/patterns/drawing-patterns.md

🔒 Security Status Check: 
Security audit passed — all CRITICAL findings cleared

VERDICT: APPROVED — PR ready to merge without additional requirements
```

**Epic closure (kanam-close-epic)**:

```bash
# qwen3.5 final release preparation
> Release versioning strategy?
v1.0.0 — initial stable release of AI Copilot feature

> Auto-tag and coordinate team notification?
yes — create tag vX.Y.Z with commit message

KANAM EPIC CLOSURE REPORT — brainweb v1.0.0

✅ Closure Steps Completed:
- Pre-closure validation passed (all gates cleared)
- CHANGELOG updated with all changed files
- Version tag created: v1.0.0
- Security audit found no CRITICAL findings
- PR merge method confirmed: "merge" (preserves task history)

🛡️ Security Status Check: 
No CRITICAL multi-tenancy or auth guard issues found

**Action**: Epic closure complete. Version v1.0.0 tagged and ready for distribution.
```

---

## Integration Notes for qwen3.5-4b-mlx Users

### What Makes This Work with qwen3.5?

| Feature | Why qwen3.5 Handles Well | Kanam Integration |
|---------|--------------------------|-------------------|
| Pre-flight validation | Strong reasoning, asks clarifying questions | Auto-mode scoping questions |
| Security analysis | Pattern matching for critical vulnerabilities | CRITICAL finding detection |
| Code quality assessment | Detailed code review with line references | Gate-level verification |
| Workflow orchestration | Task management with state tracking | Multi-gate lifecycle management |

### Deepseek-v4 Integration Notes

If using deepseek-v4-flash:

```bash
# Cloud integration workflow
kanam-copilot --model "deepseek-v4-flash" --project "brainweb"

# CRITICAL security findings get immediate deepseek analysis:
> qwen3.5 auto-detect triggered security audit?
yes — cloud API integration with deepseek for real-time CRITICAL finding detection

kanam-security-audit --target "src/service/critical-finding-check.ts" --deepseek-v4-integration
```

**Note**: deepseek-v4 provides faster API response but qwen3.5-4b-mlx gives better local reasoning for detailed code inspection. Use both where possible.

---

*Last updated: 2026-07-19 • Kanam AI System v0.1 • Examples from workflow-kit + antigravity fusion source*
