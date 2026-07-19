# Frozen Repos — Migration Status & Links

> **Status**: Active migration → Legacy repos archived with links → Cleanup pending (Q3-Q4 2026)

---

## Overview

Kanam AI System unifies skills from 4 legacy repositories into a single source of truth. This document tracks the migration status and provides links to preserved legacy content for reference purposes only (frozen, not active).

| Legacy Repo | Current Status | Migration Progress | Last Updated | Next Action |
|-------------|-----------------|--------------------|---------------|-------------|
| `gonzoblasco/workflow-kit` | 🔴 Frozen → Active merged | 85% | 2026-07-19 | Complete base skills fusion |
| `gonzoblasco/antigravity-developer-stack` | 🟡 Frozen → Curated library | 30% | 2026-07-19 | Curate patterns (70+ skills → neutral names) |
| `gonzoblasco/copilot-skills` | 🔴 Frozen → Active merged | 85% | 2026-02-15 | Complete base skills fusion |
| `gonzoblasco/chatgpt-project-architect` | 🟡 Frozen → Reference docs | 15% | 2026-07-19 | Curate prompt methodology patterns |

---

## Repose-by-Repose Migration Status

### 🔴 workflow-kit (85% complete)

**Original purpose**: Portable AI agent workflow skills for ANY IDE (Claude Code, Codex, Cursor, OpenClaw).

| Skill | Original Location | Current Status | Merged Into | Notes |
|-------|-------------------|-----------------|-------------|-------|
| `copilot` | `.agents/skills/copilot/SKILL.md` | ✅ Active merged | `kanam-copilot` | Universal workflow orchestrator + Pre-Flight + 5 Gates — base skill for ALL Kanam projects |
| `commit` | `.agents/commit/SKILL.md` | ✅ Merged (base) | N/A | Format commits with Conventional Commits + project scopes |
| `commit-formatter` | Auto-skilled from copilot | ✅ Active (auto) | `kanam-copilot` integration | Analyzes diff and writes formatted commit message |
| `pr` | `.agents/pr/SKILL.md` | ✅ Merged | `kanam-pr` lifecycle | Create structured PRs with description, review, merge — unified workflow |
| `pr-review` | Multiple sources (workflow-kit + antigravity) | ✅ Active merged | `kanam-pr-review` | Cognitive pre-merge linter — checks correctness, tests, conventions, security, performance |
| `new-task` | Not explicit in workflow-kit | ⚠️ In progress | N/A | Unified with antigravity and chatgpt-project patterns |
| `refactor` | Generic pattern reference | 🟡 Curated | `patterns-lifecycle/` | Extract logic to helper — neutralized naming |
| `doc-writer` | Generic pattern reference | 🟡 Curated | `prompt-systems/` | Generate and update technical documentation |
| `close-epic` | `.agents/close-epic/SKILL.md` | ⚠️ In progress | `kanam-close-epic` | Formal epic closure: security audit, CHANGELOG, tag, merge — unified with antigravity |
| `generic-docs-sync` | Generic pattern reference | 🟡 Curated | `prompt-systems/` | Detect and update out-of-sync docs when closing epics |
| `security-audit` | `.agents/security-audit/SKILL.md` | ✅ Active merged | `kanam-security-audit` | Threat model: multi-tenancy, auth guards, secrets, data leaks — base security skill |
| `product-reset` | `.agents/product-reset/SKILL.md` | ⚠️ In progress | N/A | Strategic reset: diagnose, visionary, plan, execute |

**Remaining work**: 
- Complete `kanam-new-task`, `kanam-close-epic`, and `kanam-pr` skills (unified with other repos)
- Curate generic patterns into `prompt-systems/` namespace
- Verify all base skills fully merged without drift

**Links to preserved content:**
- Original copilot: https://github.com/gonzoblasco/workflow-kit/blob/main/.agents/skills/copilot/SKILL.md
- Security audit original: https://github.com/gonzoblasco/workflow-kit/blob/main/.agents/skills/security-audit/SKILL.md
- PR lifecycle: https://github.com/gonzoblasco/workflow-kit/blob/main/.agents/pr/SKILL.md

---

### 🟡 antigravity-developer-stack (30% complete)

**Original purpose**: Encyclopedia of 70+ patterns, prompts, and workflows for AI-First engineering — from Architecture to Autonomous Agents.

| Skill Category | Original Skills | Current Status | Curated Into Kanam | Notes |
|----------------|-----------------|-----------------|--------------------|-------|
| **AI Agents** (12 skills) | ai-agents-architect, agent-tool-builder, rag-expert, mcp-builder, prompt-mastery, prompt-engineer, meta-skill-antigravity, elon-musk, prompt-systems... | 🟡 Curated 30% | `patterns-lifecycle/ai-workflows/` | Neutralized naming — patterns curated for lifecycle workflows |
| **Strategy Architecture** (12 skills) | senior-architect, architecture, architecture-patterns, saas-multi-tenant, brainstorming, design-orchestration, antigravity-workflows, app-builder, pricing-strategy... | 🟡 Curated 5% | `docs/strategy/architecture-patterns.md` | Most merged into base skill (senior-architect logic in kanam-copilot) |
| **Backend Infra** (12 skills) | nestjs-expert, prisma-expert, api-patterns, database-design, postgres-best-practices, docker-expert, mercadolibre-api, security-audit... | ✅ Security merged; others 🟡 | `patterns-lifecycle/backend/` + `docs/api/` | Security audit already in base skill; other backend patterns curated |
| **Frontend UI** (30+ skills) | frontend-dev-guidelines, senior-frontend, accessibility-audit, ui-a11y, wcag-audit-patterns, react-patterns... | 🟡 Curated 15% | `patterns-lifecycle/frontend/` | React patterns and a11y merged into base; UI guidelines curated |
| **Fullstack** (30+ skills) | vibe-code-cleanup, refactor, browser-automation-expert, linear-expert, pr-review... | 🟡 Curated 20% | `patterns-lifecycle/fullstack/` | PR review merged; automation patterns for tools namespace |

**Remaining work**:
- Complete curating of 70+ skills into neutral namespaced structure (`patterns-lifecycle/`, `docs/`)
- Extract multi-tenancy patterns and security requirements into base skill (already 85% complete)
- Convert examples to neutral naming (remove "antigravity-" prefix where possible)

**Links to preserved content:**
- Antigravity full library: https://github.com/gonzoblasco/antigravity-developer-stack/tree/main
- Specific skill example: https://github.com/gonzoblasco/antigravity-developer-stack/blob/main/frontend-ui/senior-frontend/SKILL.md

---

### 🔴 copilot-skills (85% complete)

**Original purpose**: Personal collection of reusable skills for Claude Code and Google Antigravity — each SKILL.md defines agent behavior.

| Skill | Original Location | Current Status | Merged Into | Notes |
|-------|-------------------|-----------------|-------------|-------|
| `copilot` | `.agents/skills/copilot/SKILL.md` | ✅ Active merged | `kanam-copilot` | Same as workflow-kit copilot — universal orchestrator |
| `commit` | `.agents/commit/SKILL.md` | ✅ Merged | N/A | Format commits with Conventional Commits + project scopes |
| `pr-review` | Not explicit in copilot-skills repo | ⚠️ In progress | `kanam-pr-review` | Unified with workflow-kit and antigravity versions |
| `new-task` | Generic pattern reference | ⚠️ In progress | N/A | Unified with antigratory and chatgpt-project patterns |
| `close-epic` | Not explicit | ⚠️ In progress | `kanam-close-epic` | Formal closure ritual unified |
| `pr` | Generic pattern reference | ⚠️ In progress | N/A | PR lifecycle skill unified |
| `security-audit` | `.agents/security-audit/SKILL.md` | ✅ Active merged | `kanam-security-audit` | Threat model base skill |
| `product-reset` | Not explicit | ⚠️ Curated | N/A | Strategic reset pattern in docs |

**Remaining work**:
- Finalize unified versions of `kanam-new-task`, `kanam-close-epic`, `kanam-pr-review` (already 85% complete from other repos)
- Verify all skills can be safely merged without drift

**Links to preserved content:**
- Original copilot-skills: https://github.com/gonzoblasco/copilot-skills/tree/main/.agents/skills/

---

### 🟡 chatgpt-project-architect (15% complete)

**Original purpose**: Skill for designing bulletproof project instructions/templates for ChatGPT with security patterns and TDD validation methodology.

| Content Type | Original Location | Current Status | Curated Into Kanam | Notes |
|--------------|-------------------|-----------------|--------------------|-------|
| **Project Templates** | `templates/` folder (5 templates) | ✅ Merged | N/A | Minimal, developer-assistant, content-creator, educator, consultant templates → neutralized in docs |
| **Security Patterns** | `references/security-patterns.md` | ✅ Curated | `docs/patterns/security.md` | Anti-injection patterns integrated into base skill security-audit |
| **Mode Architecture** | `references/mode-architecture.md` | 🟡 Curated 15% | `docs/patterns/modes.md` | Dual/multi-mode architecture patterns |
| **Command Design** | `references/command-design.md` | 🟡 Curated 10% | `docs/patterns/commands.md` | Naming, discovery, composability rules |
| **Response Structures** | `references/response-structures.md` | 🟡 Curated 20% | `docs/patterns/outputs.md` | Mandatory sections, layered structures |
| **Validation Methodology** | `tests/baseline-scenarios.md` + `references/validation-methodology.md` | 🟡 In progress | `docs/metrics/validation-strategy.md` | TDD for instructions methodology — partially merged into kanam-copilot pre-flight |

**Remaining work**:
- Complete curating of prompt engineering patterns into base skill (50% done)
- Convert template examples to neutral naming (remove "ChatGPT-" prefix where possible)
- Finalize validation strategy integration into `kanam-copilot` pre-flight section

**Links to preserved content:**
- Original chatgpt-project-architect: https://github.com/gonzoblasco/chatgpt-project-architect/tree/main
- Specific template example: https://github.com/gonzoblasco/chatgpt-project-architect/blob/main/templates/minimal-template.md

---

## Go/No-Go Criteria for Legacy Repo Closure

### ✅ GO when all conditions met:
- **Skills base merged ≥90%**: All duplicate skills from 4 repos unified in `skills/base/` and `skills/workflow/`
- **Legacy repos dormant**: No new PRs opened or pending review >30 days in legacy repos
- **Migration complete**: All skills curated into neutral namespaced structure (`patterns-lifecycle/`, `prompt-systems/`)
- **Kanam community consensus**: KanamAI framework adopted by team as single source of truth

### 🛑 NO-GO if any condition not met:
- **Critical features fragmented**: Different repos have incompatible versions or implementations (drift >10%)
- **Blocking PRs unresolved**: Conflicting branches block merge without resolution strategy
- **Momentum lost**: Community actively forked KanamAI to other frameworks (indicates acceptance issues)

---

## Cleanup Timeline

| Phase | Target | Action | Status |
|-------|--------|--------|--------|
| **Phase 1** | Q3 2026 | Finalize base skills merge, update OSS PR contributions to new repos | In Progress |
| **Phase 2** | Q4 2026 | Archive antigratory and chatgpt-project patterns as frozen-ref docs, final cleanup | Pending |
| **Phase 3** | Q1 2027 | Close all legacy repo branches/PRs, verify migration complete | Pending |

---

*Last updated: 2026-07-19 • Kanam AI System v0.1 • Frozen repos document auto-updating on next migration checkpoint*
