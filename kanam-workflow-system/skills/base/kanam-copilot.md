# Kanam Copilot (Universal Workflow Orchestrator)

> **Master skill**: Orquestor universal de workflows + Pre-Flight checklist + 5 Gates

---

## Purpose

Act as the definitive workflow authority for ANY repository. This skill governs every task's lifecycle and prevents disordered execution without structural validation. Ensures total consistency across terminal, IDE environments, and AI agent implementations.

**Fusion source:** `workflow-kit/copilot` + `copilot-skills/copilot` + `antigravity/copilot`

---

## Philosophy

A Kanam copilot reads instruments before every maneuver, warns before errors occur (not after), stops until receiving explicit pilot confirmation, and reports every state transparently.

> "The machine does not decide. The pilot confirms."

---

## Pre-Flight Checklist (Mandatory before coding)

Before modifying or creating any file, the agent must validate this state and communicate it to the user:

```text
KANAM PRE-FLIGHT [Epic Name]
══════════════════════════════
[ ] SKILL.md / Base instructions read.
[ ] .kanam/AGENT_TASKS.md reviewed for current Epic.
[ ] Style guide and architecture assimilated.
[ ] Mockups or API contracts located.
[ ] Epic/Task branch created correctly (`e[Epic]/t[N-Task]-[short-desc]`).
[ ] 'main' branch clean and up to date.
[ ] Epic dependencies and prerequisites confirmed.

FIRST TASK SELECTED: T0X · [Name]
AWAITING DEVELOPER CONFIRMATION TO START.
```

**CRITICAL:** If any Pre-Flight item fails, DO NOT PROCEED. Report findings before continuation.

---

## Task Lifecycle (The 5 Hybrid Gates)

### Gate 0: Isolated Branching

| Action | Format | Note |
|--------|--------|-------|
| Create or switch branch | `e[Epic]/t[N-Task]-[short-description]` (e.g., `e4/t10-ai-copilot-drawer`) | If working from IDE UI, request branch creation or warn if editing directly on `main` |

### Gate 1: Atomic, Scoped Implementation

| Action | Restriction |
|--------|-------------|
| Write code exclusively to fulfill current task's scope (`T0X`) | **Feature creep strictly forbidden** — solve next task's problems or refactoring out-of-scope code |

### Gate 2: Strict Build Check (Safety Box)

| Action | Block |
|--------|-------|
| Run real production command (`npm run build`, `cargo build` etc.) | Dev mode only insufficient | If build fails due to types, broken references, or compilation errors — STOP immediately, fix error, re-run build |

### Gate 3: CHANGELOG Registration

| Action | Format |
|--------|--------|
| Immediately document change in `CHANGELOG.md` under `[Unreleased]` section | One precise bullet point per substantially modified file |

### Gate 4: Formatted Commit and PR-Review

| Action | Delegate to | Block if fails |
|--------|-------------|----------------|
| Commit message generation → `@kanam-pr-review` | `@kanam-copilot` + `@kanam-pr-review` | If review returns `REQUEST CHANGES` — fix code before send/merge |

---

## Invocation

```bash
# Activate Kanam copilot with project context
kanam-copilot --project "[Epic Name]" --task T0X:[Task Short Description]

# Auto-detect mode when no arguments provided
kanam-copilot
```

**Auto-mode defaults:**
- No arguments: Pre-Flight validation + ask project scoping questions
- With `--project`: Read `.kanam/PROJECT.md` for current Epic context
- With `--task`: Initialize task if branch not yet created

---

## Agent Compatibility

| Agent | Location | Status |
|-------|----------|--------|
| Claude Code | `.kanam/skills/<name>/SKILL.md` | ✅ Tested |
| Codex | `.kanam/skills/<name>/SKILL.md` | ✅ Compatible |
| Cursor | `.cursor/skills/<name>/SKILL.md` | ⚠️ Needs symlink/copy |
| OpenClaw | Workspace skills via `skill_workshop` | ✅ Compatible |
| qwen3.5:4b-mlx | Local workspace skills | ✅ Compatible (local) |
| deepseek-v4-flash | Cloud workspace skills | ✅ Compatible (cloud) |

> **Rule:** Kanam copilot SKILL.md must be readable by ANY compatible AI agent in `.kanam/skills/` location. This is the universal interface contract.

---

## Output Format

When executed via CLI or IDE analysis, the skill generates a unified workflow state:

```markdown
## 🔍 KANAM PRE-FLIGHT STATUS
### Gate Status
[✓] Base instructions read: CLAUDE.md (or qwen3.5 system prompt)
[ ] Agent tasks reviewed: `.kanam/AGENT_TASKS.md`
[ ] Branch created: `e4/t10-ai-copilot-drawer` pending
### First Task Confirmed
T0X · AI Copilot Drawer — awaiting confirmation to proceed

## 🚧 ACTION REQUIRED
Confirm or modify task scope before proceeding with implementation.
```

---

## Integration Points

When Kanam copilot is active in your workflow:

1. **Pre-Flight always mandatory**: No code without reading `SKILL.md` and `.kanam/AGENT_TASKS.md`
2. **5 Gates are real blocks**: If build fails at Gate 2, agent stops and fixes before continuing
3. **Commit message delegated**: `/commit` skill handles formatting after copilot confirms changes

---

## Anti-Patterns (Do Not Do)

- ❌ Don't skip Pre-Flight for "speed" — this guarantees later rework
- ❌ Don't advance without explicit confirmation — auto-mode asks, don't assume
- ❌ Don't write outside task scope — feature creep is strictly forbidden

---

*Last updated: 2026-07-19 • Kanam AI System v0.1 • Fusion source documented in MANIFESTO.md*
