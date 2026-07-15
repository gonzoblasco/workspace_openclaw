---
name: "skill-composition"
description: "Chain skills into ordered pipelines where each stage's output feeds the next. Stage gates prevent bad output from propagating downstream."
---

# Skill Composition

Use when a complex objective requires multiple skills executed in a specific order, where each stage's output feeds the next. Composition turns a sequence of skills into a repeatable pipeline with gates, handoffs, and failure handling.

## When to use

- "Fix issue #123 and open a PR" → spike → implement → review → github
- "Add a new feature to SoporteML" → sdd-brownfield (spec) → implement → review → merge
- "Audit and fix accessibility issues" → investigate → prioritize → fix → review → verify
- Any objective where you naturally think "first we do X, then Y, then Z"

## When NOT to use

- Single-skill tasks (just use that skill)
- Tasks where the order doesn't matter (use agent-dispatcher with parallel assignment instead)
- When stages are independent and don't feed each other (that's parallel dispatch, not composition)

## Core concept

A composition is a **pipeline**: an ordered list of stages. Each stage has:
- A **skill** (or manual procedure)
- An **agent** (subagent that executes it)
- An **input** (from previous stage or initial)
- An **output** (deliverable for next stage or final)
- A **gate** (criteria to pass before next stage)

The pipeline is not linear by default — stages can branch, parallelize, or loop. But the simplest form is linear and that's where you start.

## Loop

1. **Design** — map the pipeline: stages, order, gates, parallelism
2. **Prepare** — gather inputs for stage 1, confirm prerequisites
3. **Execute** — run each stage in order, gate-check between stages
4. **Handle** — on gate failure: retry, branch, or abort
5. **Deliver** — final output after all stages pass

## Step 1 — Design

Before spawning anything, design the pipeline. This is thinking work, not delegation.

### Pipeline design format

```markdown
## Pipeline: <name>

### Objective
<one sentence>

### Stages
1. **investigate** — skill: — / model: medium / context: fork
   - input: objective + codebase
   - output: root cause analysis + relevant files list
   - gate: analysis cites specific files and identifies a clear cause

2. **spec** — skill: sdd-brownfield / model: high / context: fork
   - input: investigation output
   - output: delta spec (proposal.md, design.md, spec.md, tasks.md)
   - gate: spec validates with `openspec validate`

3. **implement** — skill: — / model: low-medium / context: isolated
   - input: spec tasks list
   - output: code changes on branch
   - gate: build + lint + tests pass

4. **review** — skill: agent-review / model: high / context: fork
   - input: brief + implementation output
   - output: verdict (APPROVED / CHANGES_REQUESTED / REJECTED)
   - gate: verdict is APPROVED or APPROVED_WITH_NOTES

5. **pr** — skill: github / model: low / context: isolated
   - input: reviewed code on branch
   - output: PR URL
   - gate: PR created successfully
```

### Design rules

- **Start linear.** If you can design it as a straight line, do. Add branching only when needed.
- **Every stage needs a gate.** A stage without a gate is a stage where garbage propagates.
- **Gates must be checkable.** "Output is good" is not a gate. "Build passes, tests pass, spec validates" is.
- **Minimize fork context.** Only stages that need the transcript get fork. Isolated is cheaper and cleaner.
- **Match model to stage.** Investigation and spec need reasoning. Codeo needs precision. PR submission needs neither.

### Common pipeline patterns

**Feature implementation:**
```
spec → implement → review → merge
```

**Bug fix:**
```
investigate → implement → review → pr
```

**OSS contribution:**
```
triage → investigate → implement → review → pr → track
```

**Audit + fix:**
```
audit → prioritize → fix → review → verify
```

**Spec-driven brownfield:**
```
init-openspec → as-built-specs → delta-spec → implement → review → archive
```

## Step 2 — Prepare

Before stage 1:

1. **Confirm prerequisites** — do all skills exist? Is auth configured? Are repos cloned?
2. **Gather initial inputs** — what does stage 1 need? (files, issue numbers, context, access)
3. **Set up tracking** — where will state live between stages? (workspace file, flow state, memory)
4. **Plan failure** — what happens if stage N fails? Can you skip it? Retry? Abort?

### State tracking

For simple pipelines: use a workspace file.

```markdown
## Pipeline state: <name>

- [x] Stage 1: investigate — ✅ done, output in /tmp/pipeline-investigate.md
- [ ] Stage 2: spec — pending
- [ ] Stage 3: implement — pending
- [ ] Stage 4: review — pending
- [ ] Stage 5: pr — pending
```

For complex pipelines with waits and external dependencies: use TaskFlow (see taskflow skill).

## Step 3 — Execute

Run stages in order. After each stage:

1. **Check the gate** — did the output pass the stage's gate criteria?
2. **If pass:** capture output, pass to next stage
3. **If fail:** go to Step 4 (Handle)

### Execution with dispatcher

The composition defines WHAT runs in what order. The dispatcher defines HOW each stage is delegated. They compose:

```
composition designs pipeline
  → dispatcher spawns stage 1 agent with brief
    → stage 1 returns output
      → gate check
        → dispatcher spawns stage 2 agent with stage 1 output
          → stage 2 returns output
            → gate check
              → ...
```

### Execution without dispatcher

If you're running the pipeline yourself (not via dispatcher):

1. `sessions_spawn` for stage 1 with its brief
2. `sessions_yield` — wait for completion
3. Check output against gate
4. If pass: `sessions_spawn` for stage 2 with stage 1 output as input
5. Repeat until done

### Handoff format

When passing output from one stage to the next, use a structured handoff:

```markdown
## Handoff: <stage N> → <stage N+1>

### From
<stage name>

### Deliverable
<what was produced>

### Key decisions
- <decision 1>
- <decision 2>

### Files touched
- <file 1>
- <file 2>

### Notes for next stage
- <what stage N+1 needs to know>
- <gotchas, constraints, things to watch>
```

The handoff is not the full output — it's the **distilled context** the next agent needs. The full output lives in files; the handoff points to them.

## Step 4 — Handle failure

### Gate failure (output doesn't meet criteria)

- **Retry with feedback:** respawn the same stage with gate failure notes appended to the brief
- **Max retries per stage: 2.** After 2 failures, the problem is upstream (bad brief, wrong skill, wrong model)
- **Escalate after max retries:** either fix the brief and retry, or abort and report to orchestrator

### Stage failure (agent crashes, returns garbage, times out)

- **Check model fit:** was the model too weak for the task? Try higher reasoning.
- **Check context fit:** did the agent lack context it needed? Try fork instead of isolated.
- **Check brief quality:** was the brief clear enough? Vague briefs produce garbage.
- **Check prerequisites:** did the stage have everything it needed before starting?

### Branching on failure

Some pipelines branch on failure:
```
investigate → (bug found?) 
  → yes: fix → review → pr
  → no: report (no fix needed)
```

Design branches in Step 1, not on the fly.

## Step 5 — Deliver

After all stages pass:

1. **Collect final output** — the deliverable from the last stage
2. **Consolidation report** — what ran, what passed, what failed and was retried
3. **Update tracking** — mark pipeline complete, update memory/handoff/changelog
4. **Clean up** — temp files, branches, spawned sessions

### Pipeline completion report

```markdown
## Pipeline complete: <name>

### Objective
<original objective>

### Stages
1. ✅ investigate — <output summary>
2. ✅ spec — <output summary>
3. ✅ implement — <output summary>
4. ✅ review — APPROVED
5. ✅ pr — PR #<n> opened

### Final deliverable
<what was produced>

### Retries
<stages that needed retries, or "none">

### Follow-up
<what still needs to happen, or "none">
```

## Parallel stages

When stages are independent, run them in parallel:

```
         ┌→ write tests ─┐
implement ┤               ├→ review → pr
         └→ write docs  ─┘
```

### How to parallelize

1. Identify stages with no dependencies on each other
2. Spawn all parallel stages at once with `sessions_spawn`
3. `sessions_yield` — wait for all to complete
4. Gate-check each independently
5. If all pass: proceed to the dependent stage with all outputs combined
6. If any fail: handle each independently (retry that stage, keep the others)

## Nested pipelines

A stage can itself be a pipeline:

```
OSS contribution pipeline:
  triage → investigate → [implement pipeline: spec → code → review] → pr → track
```

When a stage is complex enough to warrant its own pipeline, use the composition skill recursively. The outer pipeline treats the inner pipeline as a single stage with its own gates.

## Anti-patterns

- **No gates:** a pipeline without gates is just a sequence of hopeful spawns. Bad output propagates silently.
- **Over-pipelining:** don't pipeline a 2-step task. If it's "investigate → fix", just do it. Pipelines are for 3+ stages with real gates.
- **Linear when parallel:** if stages are independent and you run them sequentially, you're wasting time. Check for parallelism in design.
- **Fixed pipelines:** the pipeline is a plan, not a contract. If stage 2 reveals that stage 4 is unnecessary, skip it. If stage 3 reveals a new stage is needed, add it.
- **Ignoring failures:** if a gate fails and you proceed anyway, the gate was decorative. Either enforce it or remove it.
- **Monolithic stages:** if a stage is doing 3 things, it's 3 stages. Split.

## Composition with dispatcher and review

The three skills form a system:

- **Composition** designs the pipeline (what stages, in what order, with what gates)
- **Dispatcher** executes each stage (which agent, what model, what brief)
- **Review** gates each stage (did the output meet criteria)

Typical flow:
```
orchestrator receives objective
  → composition designs pipeline
    → for each stage:
      → dispatcher spawns agent with brief
        → agent produces output
          → review verifies against gate
            → if pass: next stage
            → if fail: retry or abort
  → orchestrator receives final deliverable
```

## Lessons learned

(this section will be populated with real lessons from composed pipelines)
