---
name: "agent-workflow"
description: "Add multi-agent orchestration with specialized roles, acceptance criteria, and consolidated deliverables inspired by Agency Orchestrator."
metadata:
  version: 1.1.0
  author: Kanam
  tags: ["workflow", "tdd", "planning", "code-review", "subagents", "superpowers", "discipline", "orchestration", "multi-agent"]
allowed-tools:
  - exec
  - read
  - write
  - edit
  - skill_workshop
  - sessions_spawn
  - sessions_yield
  - subagents
---

# Agent Workflow

This skill adapts proven agentic software-development discipline (inspired by Jesse's Superpowers for Claude Code) to OpenClaw's native tools, memory system, and skill workshop.

It now also includes multi-agent orchestration patterns inspired by Agency Orchestrator: decompose a goal into specialized subagent roles, run them with acceptance criteria, and consolidate the outputs into a single deliverable.

## When to use

Use this skill for any non-trivial coding task:
- New features
- Bug fixes
- Refactors
- UI/UX work
- Integration work
- Any task that touches more than one file
- Complex decisions where multiple expert perspectives are valuable

Skip only for:
- One-line config changes
- Pure documentation edits
- Throwaway experiments

## Core principles

1. **Design before code** — present a spec and get approval.
2. **Plan before execution** — decompose into 2-5 minute tasks.
3. **Test first, code second** — RED/GREEN/REFACTOR.
4. **Review before proceeding** — subagent code review after each task.
5. **Root cause before fix** — systematic debugging.
6. **Evidence over claims** — verify before declaring success.
7. **DRY, YAGNI, small files** — prefer focused files over god objects.
8. **Atomic commits** — one task, one commit.

## Workflow

### Phase 1: Design Gate (Hard)

Before writing any code:

1. Read project context (README, AGENTS.md, MEMORY.md, ROADMAP, ADRs, recent commits).
2. Ask clarifying questions one at a time.
3. Propose 2-3 approaches with trade-offs and your recommendation.
4. Present the design in sections scaled to complexity. Get explicit user approval.
5. Save the approved design doc to `.knowledge/specs/YYYY-MM-DD-<feature>.md`.

**Do not proceed to Phase 2 until the user approves the design.**

### Phase 2: Implementation Plan

After design approval:

1. Map files to create/modify.
2. Break work into bite-sized tasks (2-5 minutes each).
3. Each task must include:
   - Exact file(s)
   - What to change
   - How to test
   - Expected outcome
4. Save plan to `.knowledge/plans/YYYY-MM-DD-<feature>.md`.

Use language appropriate for a skilled but context-poor engineer:
- Exact file paths
- Complete code snippets
- Test commands
- Edge cases to cover

### Phase 3: TDD Execution

For each task in the plan:

1. **RED** — Write or update the failing test first.
2. **Verify RED** — Run the test, confirm it fails for the right reason.
3. **GREEN** — Write the minimal code to pass the test.
4. **Verify GREEN** — Run tests + lint + build. All must pass.
5. **REFACTOR** — Clean up with tests still green.
6. **Review** — Dispatch code-reviewer subagent (see Phase 4).
7. **Commit** — Atomic commit, one per task.

**If you wrote implementation code before the test, delete it and start over.**

Exceptions (ask user first):
- Throwaway prototypes
- Generated/config-only changes

### Phase 4: Code Review

After each task and before continuing:

1. Get `BASE_SHA` (commit before the task) and `HEAD_SHA` (current).
2. Spawn a subagent using the code-reviewer prompt below.
3. Fix Critical issues immediately. Fix Important issues before proceeding. Note Minor issues.
4. Re-run tests/lint/build after fixes.

### Phase 5: Multi-Agent Orchestration (Optional)

For complex goals where multiple expert lenses are useful, spawn a panel of subagents with specific roles and acceptance criteria.

Example roles:

| Role | Responsibility | When to use |
|---|---|---|
| Architect | System design, tech choices, trade-offs | New subsystem, major refactor |
| Security | Threat model, secure defaults, OWASP | Auth, payments, external input |
| Frontend | UI/UX, components, accessibility, responsive | Any UI work |
| Backend | API design, DB schema, edge functions | Server-side work |
| Tester | Test plan, edge cases, coverage | Before implementation |
| Reviewer | Final code review, plan compliance | Before merge |

Workflow:

1. **Define goal and deliverable** — what does success look like?
2. **Select roles** — auto-select based on task type, or ask user.
3. **Spawn subagents in parallel** — each role receives the same context plus its specific lens.
4. **Collect outputs** — each subagent returns findings, risks, recommendations.
5. **Consolidate** — synthesize conflicting views, highlight open questions, propose a unified plan.
6. **Present to user** — get approval before implementation.

Use this pattern for:
- Architecture decisions
- Security reviews
- Product requirements
- Design direction
- Code audits
- Research synthesis

### Phase 6: Merge/Handoff

When all tasks complete:

1. Run full test suite, lint, build.
2. Present options: merge, PR, keep branch, discard.
3. Update `.knowledge/STATUS.md`, `CHANGELOG.md`, and `memory/YYYY-MM-DD.md`.
4. Clean up temp dirs or worktrees if used.

## Code reviewer subagent prompt

```markdown
You are a strict code reviewer. Review the changes between BASE_SHA and HEAD_SHA.

Context:
- Project: {project_name}
- Feature: {feature_description}
- Plan requirements: {requirements}

Instructions:
1. Run `git diff BASE_SHA..HEAD_SHA`.
2. Check correctness, edge cases, test coverage, naming, file size, DRY, YAGNI.
3. Verify no implementation was written before tests (TDD).
4. Flag issues by severity: Critical / Important / Minor.
5. For Critical/Important issues, suggest exact fixes.
6. Return a concise report in markdown.

Do not run git commands that modify history. Read-only review.
```

## Multi-agent panel prompt

```markdown
You are {role} reviewing this goal: {goal}.

Context:
- Project: {project_name}
- Constraints: {constraints}
- Deliverable: {deliverable}

Instructions:
1. Analyze the goal from your role's perspective.
2. Identify risks, open questions, and recommendations.
3. Provide concrete acceptance criteria if applicable.
4. Keep your output focused and actionable.

Return your findings in markdown.
```

## Systematic debugging

When any bug, test failure, or unexpected behavior appears:

1. **Stop proposing fixes.**
2. **Reproduce** — make the failure happen reliably.
3. **Isolate** — find the smallest input/state that triggers it.
4. **Hypothesize** — list possible root causes.
5. **Test hypotheses** — add logging, run targeted experiments, read relevant code.
6. **Confirm root cause** — explain why the failure happens.
7. **Fix once** — fix the root cause, not the symptom.
8. **Verify** — run tests/lint/build.
9. **Prevent** — add regression test if missing.

## Anti-patterns

- "This is too simple to need a design"
- Writing implementation code before a failing test
- Skipping code review because "I know this code"
- Fixing symptoms without root cause
- Monolithic commits that mix tasks
- Ignoring failing tests or lint errors
- Writing code that future-you will hate
- Spawning subagents without clear roles or acceptance criteria
- Letting subagents duplicate work instead of dividing by expertise

## File locations

- Design docs: `.knowledge/specs/YYYY-MM-DD-<feature>.md`
- Plans: `.knowledge/plans/YYYY-MM-DD-<feature>.md`
- Status: `.knowledge/STATUS.md`
- Changelog: `CHANGELOG.md`
- Daily notes: `memory/YYYY-MM-DD.md`

## Tool usage

- `sessions_spawn` — dispatch code reviewer, tester, researcher, or panel subagents.
- `sessions_yield` — wait for subagent results.
- `exec` — run tests, lint, build, git commands.
- `read/write/edit` — manage docs and code.
- `skill_workshop` — if a reusable workflow pattern emerges, capture it as a skill.

## Integration with other skills

- `gh-issue-planner` — create implementation plans from GitHub issues.
- `code-review-agent` — alternative/reusable reviewer if available.
- `debug-investigation` — deep debugging with structured escalation.
- `release-management` — merge/PR/release workflows.
- `build-discipline` — enforce pre-commit hooks and green builds.
- `architecture-designer` — produce ADRs for architect role outputs.
- `spec-miner` — reverse engineer code before planning changes.

## Notes

- This skill is adapted from Superpowers (obra/superpowers), MIT licensed, and customized for OpenClaw's skill system.
- Multi-agent orchestration patterns are inspired by Agency Orchestrator (jnMetaCode/agency-orchestrator), MIT licensed.
- It does not auto-trigger; you must invoke it explicitly for each task by loading it.
- Pair with AGENTS.md project conventions. If AGENTS.md conflicts, AGENTS.md wins.
- Be pragmatic. The gate exists to prevent wasted work, not to block urgent fixes. For true emergencies, document why you skipped a phase.
