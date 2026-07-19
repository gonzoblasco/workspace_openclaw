# Kanam AI System

> **"Un sistema, cuatro voces. Una fuente de verdad."**

Universal workflow and skills architecture for AI-assisted development. Fuses portable workflows from multiple sources into a single source of truth.

---

## 🌿 What Is This?

Kanam AI System is an architecture that unifies skills and workflows for AI-assisted development across ANY IDE/LLM (qwen3.5, Claude, Cursor, OpenClaw). 

It brings together the best practices from multiple sources into **one cohesive framework**:
- `workflow-kit`: Portable workflow skills
- `antigravity-developer-stack`: Encyclopedic patterns library
- `copilot-skills`: Reusable agent skills collection
- `chatgpt-project-architect`: Bulletproof project instruction methodology

**Result**: 3 unified skill layers + neutral branding = single source of truth.

---

## 🎯 Core Philosophy

> "The machine does not decide. The pilot confirms."

Kanam copilot reads instruments before every maneuver, warns before errors occur (not after), stops until receiving explicit pilot confirmation, and reports every state transparently.

### Kanam AI ≠ OpenClaw ≠ Claude ≠ Google

**Kanam is the framework that frames AIMS (AI Instruction & Memory System).**
- Skills with `kanam-*` prefix are properties of the KanamAI framework
- Examples reference LLMs (qwen3.5, deepseek-v4) as **contexts**, not definitions
- Neutral branding ensures portability across all AI agents

### The 3-Layer Architecture

```
kanam-workflow-system/
│
├── SKILL.md                        # Master orchestrator + pre-flight rules
├── MANIFESTO.md                   # System rules & decision records  
├── README.md                      # This document (v0.1)
│
├── docs/                          # Reference documentation
│    ├── workflow-structure.md     # Pre-Flight + 5 Gates explanation
│    ├── task-lifecycle.md         # Complete task lifecycle docs
│    └── frozen-repos.md           # Legacy repo migration tracking
│
├── skills/                       # Skills organized by domain
│    │
│    ├── base/                    # Universal skills (applies everywhere)
│    │    ├── kanam-copilot.md     # Master workflow orchestrator
│    │    ├── kanam-pr-review.md    # Cognitive pre-merge linter
│    │    └── kanam-security-audit.md  # Threat model + hardening
│    │
│    ├── workflow/                # Domain-specific workflows
│    │    ├── kanam-new-task.md    # Task initialization lifecycle
│    │    ├── kanam-close-epic.md   # Epic closure ritual
│    │    └── kanam-pr.md          # PR creation & merge coordination
│    │
│    └── library/                 # Curated patterns from legacy repos
│         └── (neutralized naming, no brand references)
│
└── LEGACY.md                     # History of why we unified
```

---

## 🚀 Quick Start

### Using Kanam Copilot

```bash
# Activate master copilot with project context
kanam-copilot --project "brainweb" --task T0X:"AI Copilot Drawer feature"

# Auto-detect mode (asks scoping questions)
kanam-copilot
```

**Auto-mode Pre-Flight Checklist:**
1. `SKILL.md` and `.kanam/AGENT_TASKS.md` read → ask project scoping questions
2. Confirm branch creation (`e[Epic]/t[N-Task]-[short-desc]`) before implementation
3. Run Gate 2 build verification (production command, not dev mode)
4. Document in CHANGELOG after implementation

### Task Lifecycle Workflow

```bash
# Initialize new task (auto-detect project and scoping questions)
kanam-new-task

# Full lifecycle with version control
kanam-new-task --project "brainweb" --task T0X:"Feature" --spec ".kanam/TASK_SPEC.md"

# Close epic after security audit passed
kanam-close-epic --version "1.0.0" --auto-tag
```

### Security Audit (Mandatory Before Closure)

```bash
kanam-security-audit --target "[project]" --depth 3

# Block CRITICAL findings before merge
kanam-security-audit --block-critical-only --fix
```

---

## 🏗️ Architecture Details

### Pre-Flight Checklist (Mandatory)

Before modifying or creating any file, verify these conditions:

| Item | Source | Required Action |
|------|--------|-----------------|
| Base instructions | `SKILL.md` | Read and understand workflow rules |
| Agent tasks | `.kanam/AGENT_TASKS.md` | Review current Epic context |
| Style guide | `docs/styleguide.md` | Assimilate formatting conventions |
| Mockups/contracts | `docs/api-contracts.md` | Locate API specifications |
| Branch structure | `e[Epic]/t[N-Task]-[desc]` | Create or validate branch exists |
| Main branch status | `git pull origin main` | Ensure up to date before feature work |
| Dependencies | Dependency graph | Confirm prerequisites met |

### The 5 Hybrid Gates

| Gate | Action | Block If Fails |
|------|--------|-----------------|
| **Gate 0: Isolated Branching** | Create/switch branch | If working from IDE without branch creation |
| **Gate 1: Atomic Implementation** | Write code for task scope | Feature creep, out-of-scope changes |
| **Gate 2: Strict Build Check** | Run production build command | Type errors, broken references, compilation errors |
| **Gate 3: CHANGELOG Registration** | Update CHANGELOG.md | Missing change documentation |
| **Gate 4: Commit + PR Review** | Submit formatted commit with review | `REQUEST_CHANGES` return from review skill |

---

## 📊 Current Status & Metrics

### Fusion Progress

| Original Skill | Current State | Merged Into | Progress |
|----------------|---------------|-------------|----------|
| workflow-kit `copilot` | ✅ Active | `kanam-copilot` | 100% |
| antigravity `pr-review` (x2) | ✅ Merged | `kanam-pr-review` | 95% |
| workflow-kit `security-audit` + antigravity | ✅ Merged | `kanam-security-audit` | 100% |
| chatgpt-project prompt patterns | 🟡 Curated | `prompt-systems/` docs | 45% |

### Go/No-Go Criteria for Legacy Closure

✅ **GO**: 
- Skills base merged ≥90% (currently: 85%)
- No active PRs in legacy repos (all dormant)
- Migration progress >70% (current checkpoint)
- KanamAI framework adopted as single source of truth

🛑 **NO-GO** if:
- Drift >10% between unified versions
- Blocking branches without resolution strategy

---

## 📚 Resources & Integration

### Agent Compatibility Matrix

| Agent | Location | Status | Notes |
|-------|----------|--------|-------|
| qwen3.5-4b-mlx | Local workspace skills | ✅ Compatible | Auto-detect mode |
| deepseek-v4-flash | Cloud workspace | ✅ Compatible | API integration ready |
| Claude Code | `.kanam/skills/` directory | ✅ Tested | Pre-flight rules enforced |
| Cursor IDE | `.cursor/skills/` | ⚠️ Needs symlink | Copy SKILL.md files |
| OpenClaw | `skill_workshop` integration | ✅ Compatible | Workspace orchestration |

### Integration Points

When Kanam copilot is active:

1. **Pre-Flight always mandatory**: No code without reading `SKILL.md` and `.kanam/AGENT_TASKS.md`
2. **5 Gates are real blocks**: If build fails at Gate 2, agent stops and fixes before continuing
3. **Commit message delegated**: `/commit` skill handles formatting after copilot confirms changes

---

## 🔄 Migration Status

See [frozen-repos.md](./frozen-repos.md) for detailed migration tracking of:
- Original repos (workflow-kit, antigravity-developer-stack, copilot-skills, chatgpt-project-architect)
- Go/No-Go criteria
- Cleanup timeline and milestones
- OSS contribution tracking

---

## 🎯 Vision

**Kanami Library Architecture** brings together the best from:
- `workflow-kit`: Portable workflow skills for ANY IDE
- `antigravity-developer-stack`: Encyclopedic patterns for AI-First engineering
- `copilot-skills`: Reusable agent skill collection
- `chatgpt-project-architect`: Bulletproof project instruction methodology

**Result**: Single source of truth, neutral branding, unified workflow lifecycle.

---

*Last updated: 2026-07-19 • Kanam AI System v0.1 • Neutral LLM Framework*
