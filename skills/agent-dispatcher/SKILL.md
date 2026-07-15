---
name: "agent-dispatcher"
description: "Decompose complex objectives into sub-tasks, assign each to the right skill/agent/model, delegate with structured briefs, and consolidate results."
---

# Agent Dispatcher / Router

Use when a complex objective needs to be broken down and delegated across multiple specialized agents/skills. The dispatcher does not do the work — it decomposes, assigns, delegates, and consolidates.

## When to use

- "Fix issue #123 and open a PR" (multi-step: investigate → code → test → PR)
- "Audit this project for accessibility issues and fix the top 3" (investigate → prioritize → fix → verify)
- "Set up OpenSpec in this project and write specs for all existing features" (init → read code → write specs → validate)
- Any objective that involves 2+ distinct phases or requires different skills/agents

## When NOT to use

- Single-skill tasks (just use that skill directly)
- Tasks that fit in one prompt/response
- When you (the orchestrator) can do it faster yourself than explaining the decomposition

## Loop

1. **Analyze** — understand the objective, classify its type and complexity
2. **Decompose** — break into sub-tasks with clear deliverables
3. **Assign** — match each sub-task to a skill, agent, model, and context type using the catalog
4. **Build briefs** — write a structured brief for each sub-task
5. **Delegate** — spawn subagents with the briefs
6. **Consolidate** — collect results, detect conflicts, report to the orchestrator

## Step 1 — Analyze

Before decomposing, understand what you're dealing with:

- **Type:** investigation, implementation, documentation, ops, review, or mixed
- **Complexity:** trivial (1 agent), moderate (2-3 agents), complex (4+ agents or pipeline)
- **Dependencies:** are sub-tasks independent (parallel) or sequential (pipeline)?
- **External constraints:** needs auth, needs network, needs specific repo access, needs secrets
- **Context available:** what does the dispatcher already have access to? (workspace files, memory, project state)

Output of this step: a short analysis block, not delegated.

```
## Analysis
- Type: implementation + review
- Complexity: moderate (3 sub-tasks)
- Dependencies: sequential (investigate → implement → review)
- Constraints: needs gh CLI auth, repo access
- Context: workspace MEMORY.md, project HANDOFF.md
```

## Step 2 — Decompose

Break the objective into sub-tasks. Rules:

- Each sub-task must have a **clear deliverable** (not a verb — a noun: "a list of issues", "a fix", "a spec", "a PR")
- Each sub-task must be **assignable to one agent** (not "write tests AND fix the bug" — split it)
- Each sub-task must have **measurable completion** (the agent knows when it's done)
- If a sub-task is itself complex, decompose further or flag it for recursive dispatch

```
## Sub-tasks
1. Investigate codebase → deliverable: list of relevant files + root cause analysis
2. Implement fix → deliverable: code change in branch
3. Write tests → deliverable: test file with passing tests
4. Open PR → deliverable: PR URL
```

## Step 3 — Assign

Match each sub-task to the right resources using the catalog below. The catalog is the living knowledge of what works for what. It grows with use.

### Assignment fields

Each sub-task gets:

- **Skill:** which skill applies (or "none" for generic work)
- **Model:** what reasoning level / model suits this task
- **Context:** `isolated` (clean slate) or `fork` (needs current transcript)
- **Mode:** `parallel` (can run alongside others) or `sequential` (waits for dependency)
- **Depends on:** which previous sub-task's output this one needs (if any)

### Catalog (initial version — extend with experience)

| Task type | Skill | Reasoning | Context | Notes |
|---|---|---|---|---|
| Investigate codebase | — (read + search) | medium | fork | Needs transcript context |
| Validate feasibility | spike | high | isolated | Throwaway prototype |
| Write spec | sdd-brownfield | high | fork | Needs project context |
| Implement feature | — (coding) | low-medium | isolated | Clean slate for code |
| Fix bug | — (coding) | medium | fork | Needs investigation output |
| Write tests | — (coding) | low | fork | Needs the fix as context |
| Review code | — (review, future skill) | high | fork | Needs brief + output |
| Open PR | github, oss-contribute | low | isolated | Mechanical |
| Triage issues | gh-issues | medium | isolated | Reads repo only |
| Write docs | — (writing) | medium | isolated | Clean slate |
| Audit accessibility | — (future skill) | high | fork | Needs to see the UI |

### How to extend the catalog

After each dispatch, note:
- Did the assignment work well? (agent completed the task)
- Was the model right? (too slow = lower reasoning, too dumb = higher)
- Was the context right? (agent lacked info = fork, had too much noise = isolated)
- Should this task type be added to the catalog?

## Step 4 — Build briefs

Each sub-task gets a brief. The brief is what the subagent receives as its task. A good brief is the difference between useful output and garbage.

### Brief format

```
## Objective
<one sentence: what to achieve>

## Deliverable
<concrete output: what the agent must produce>

## Context
- <what the agent needs to know to do the job>
- <links to files, previous outputs, specs>

## Constraints
- <what NOT to do>
- <boundaries: don't touch X, don't change Y>

## Acceptance criteria
- <how to know the deliverable is good>
- <checkable conditions>

## Dependencies (if sequential)
- <output from previous sub-task that this one needs>
```

### Brief rules

- **Be specific.** "Fix the bug" is not a brief. "Fix the race condition in `useSearchParam` where the cleanup runs before the effect sets the value, causing stale reads" is a brief.
- **Include the why.** The agent needs to understand intent to make good decisions.
- **Exclude the how.** Don't prescribe the solution unless there's a reason (e.g., repo conventions).
- **Set boundaries.** If the agent shouldn't touch certain files or shouldn't make certain changes, say so.
- **Make acceptance checkable.** "Works correctly" is not checkable. "Tests pass, lint passes, build succeeds" is.

## Step 5 — Delegate

Use `sessions_spawn` to launch subagents:

```
sessions_spawn({
  task: <brief content>,
  taskName: <stable identifier>,
  mode: "run",
  context: "isolated" | "fork",
  model: <optional model override>,
  thinking: <optional thinking level>
})
```

### Delegation rules

- **Parallel sub-tasks:** spawn all at once, then `sessions_yield`
- **Sequential sub-tasks:** spawn one, yield, check result, spawn next with previous output
- **Always set taskName** for traceability
- **Never assume success** — check the output against acceptance criteria before proceeding

## Step 6 — Consolidate

When all subagents return:

1. **Collect** — gather all deliverables
2. **Verify** — check each against its acceptance criteria
3. **Detect conflicts** — did two agents produce contradictory outputs? Did one agent's output break another's assumptions?
4. **Report** — summarize what was done, what succeeded, what failed, what needs follow-up

### Consolidation report format

```markdown
## Dispatch result

### Objective
<original objective>

### Sub-tasks completed
1. ✅ <sub-task> — <deliverable summary>
2. ✅ <sub-task> — <deliverable summary>
3. ❌ <sub-task> — <failure reason>

### Conflicts
<none, or list them>

### Follow-up
<what still needs to happen, if anything>
```

## Anti-patterns

- **Over-decomposition:** don't split a 5-minute task into 3 subagents. If you can do it faster yourself, do it.
- **Vague briefs:** "make it better" is not a brief. Go back to Step 4.
- **Wrong context:** if an agent needs to see the codebase, don't give it `isolated`. If it needs a clean slate, don't give it `fork`.
- **Blind delegation:** always check outputs. Subagents lie (or get confused, which is the same thing).
- **Catalog rigidity:** the catalog is a starting point, not law. If a task doesn't fit, invent the assignment and note it for catalog update.

## Lessons learned

(this section will be populated with real lessons from dispatches)

## Context files

- `MEMORY.md` (workspace) — dev profile, project context
- `projects/PROYECTOS.md` — project state
- Project-specific `HANDOFF.md` — current state of the project being worked on
- `CONTRIBUTING.md` (workspace) — OSS contribution rules
