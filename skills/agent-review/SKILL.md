---
name: "agent-review"
description: "Checklist-driven review where a second agent verifies a producer agent's output against the original brief. Catches gaps before output propagates."
---

# Agent Review

Use when an agent has produced work (code, spec, docs, investigation) and a second agent needs to verify quality before the output is accepted, merged, or passed to the next pipeline stage.

## When to use

- After a coding agent delivers a fix → review before opening PR
- After a spec-writing agent delivers a spec → review before archiving
- After an investigation agent delivers analysis → review before acting on it
- Any pipeline stage where bad output propagates downstream
- When the orchestrator says "review this" or "verify this"

## When NOT to use

- Trivial changes where you can eyeball the result
- When you (the orchestrator) can review faster than spinning up a reviewer
- When the producing agent already self-verified against the same checklist (unless trust is low)

## Core principle

The reviewer does NOT produce work. The reviewer verifies work. It reads, checks, and reports — it does not fix, rewrite, or improve. If something fails review, it goes back to the producer with feedback.

## Loop

1. **Receive** — get the brief (what was asked) and the output (what was delivered)
2. **Load criteria** — use the brief's acceptance criteria or the default checklist for the task type
3. **Verify** — run through each criterion, pass/fail each one
4. **Probe** — look for gaps the producer might have missed (edge cases, implicit assumptions, consistency)
5. **Report** — structured verdict with specific feedback

## Step 1 — Receive

The reviewer needs two things:

- **The brief:** what the producer was asked to do (objective, deliverable, constraints, acceptance criteria)
- **The output:** what the producer actually delivered (code, spec, file, analysis)

Without the brief, the reviewer can only check internal quality (does it compile, is it readable). With the brief, the reviewer checks intent alignment (does it solve the actual problem).

If the brief is missing → flag it. Reviewing without a brief is guessing.

## Step 2 — Load criteria

### Default checklists by task type

**Code:**
- [ ] Does it build? (run build command)
- [ ] Does it pass lint? (run linter)
- [ ] Does it pass existing tests? (run test suite)
- [ ] Are there new tests for the change?
- [ ] Does it handle edge cases? (empty input, null, concurrent access, error states)
- [ ] Is it consistent with the codebase style? (naming, patterns, structure)
- [ ] Does it touch files outside the scope of the brief?
- [ ] Are there implicit decisions that should be documented?
- [ ] Does it introduce new dependencies? If so, are they justified?

**Spec:**
- [ ] Does it have `## Purpose`?
- [ ] Does every requirement use SHALL or MUST?
- [ ] Does every requirement have at least one `#### Scenario:`?
- [ ] Do scenarios use WHEN/THEN format?
- [ ] For MODIFIED requirements: are all existing scenarios included?
- [ ] Does it validate? (`npx @fission-ai/openspec validate <name>`)
- [ ] Does it reference real names from the codebase?
- [ ] Are there unstated assumptions?

**Investigation / Analysis:**
- [ ] Does it answer the original question?
- [ ] Does it cite evidence (file names, line numbers, command output)?
- [ ] Are conclusions supported by the evidence?
- [ ] Are there alternative explanations not considered?
- [ ] Does it distinguish fact from speculation?

**Documentation:**
- [ ] Is it accurate against the current code?
- [ ] Is it in the right language (Spanish for CSN, English for international repos)?
- [ ] Is it clear enough for the target audience?
- [ ] Are there broken links or stale references?
- [ ] Does it follow the project's doc structure?

**PR:**
- [ ] Does the PR body reference the issue (`Closes #N`)?
- [ ] Does it explain what, why, and how?
- [ ] Is it one concern per PR (no mixed concerns)?
- [ ] Does CI pass?
- [ ] Are commit messages semantic?
- [ ] Did it read the repo's CONTRIBUTING.md?

### Custom criteria

If the brief includes explicit acceptance criteria, those take priority over defaults. The reviewer combines:
1. Custom criteria from the brief (always)
2. Default checklist for the task type (if not already covered by custom)

## Step 3 — Verify

For each criterion:

- **Run the check** — don't assume. If it says "build passes", run the build. If it says "tests pass", run the tests.
- **Record the result** — pass / fail / unclear
- **If fail:** note the exact failure (error message, file, line)
- **If unclear:** note what needs human judgment

```
## Verification

### Build
✅ PASS — `npm run build` succeeded

### Lint
✅ PASS — `npm run lint` clean

### Tests
❌ FAIL — `useSearchParam.test.ts` line 42: expected "abc" got "undefined"
  → test expects cleanup to preserve value, but cleanup runs before effect

### Edge cases
❌ FAIL — no handling for empty string input (`useSearchParam("")` throws)
  → brief required "handle empty input"

### Style consistency
✅ PASS — naming and patterns match codebase

### Scope
✅ PASS — only touched `useSearchParam.ts` and test file

### Implicit decisions
⚠️ UNCLEAR — chose `useRef` instead of `useState` for storing previous value. Reasonable but should be documented.
```

## Step 4 — Probe

Beyond the checklist, look for things the producer might have missed:

- **Implicit assumptions:** the producer assumed X — is X always true?
- **Side effects:** does this change break something in a different file/module?
- **Pre-existing issues:** was the test already flaky on main? (stash the change, run tests, compare)
- **Breaking changes:** does this change a public API, type signature, or behavior that consumers depend on?
- **Security:** does this introduce injection vectors, expose secrets, or weaken auth?
- **Performance:** does this add O(n²) inside a loop, unnecessary re-renders, or unbounded queries?

Probe rules:
- Only flag real issues, not stylistic preferences
- If you flag something, provide evidence (command output, file reference)
- Distinguish "this is wrong" from "I would have done it differently"

## Step 5 — Report

### Verdict

One of:
- **APPROVED** — all criteria pass, no critical issues found
- **APPROVED_WITH_NOTES** — all criteria pass, but there are non-blocking observations
- **CHANGES_REQUESTED** — one or more criteria fail, specific fixes needed
- **REJECTED** — fundamental approach is wrong, needs rework from scratch

### Report format

```markdown
## Review: <task name>

### Verdict: APPROVED | APPROVED_WITH_NOTES | CHANGES_REQUESTED | REJECTED

### Criteria results
<verification block from Step 3>

### Probe findings
<probe block from Step 4, or "none">

### Feedback to producer (if not APPROVED)
1. <specific fix needed, with file/line reference>
2. <specific fix needed>

### Notes (non-blocking)
1. <observation>
2. <observation>
```

### Feedback rules

If the verdict is CHANGES_REQUESTED or REJECTED:
- **Be specific:** "Fix line 42" not "fix the test"
- **Reference the brief:** "Brief required edge case handling for empty input — this is missing"
- **Don't prescribe the solution:** describe the problem, let the producer figure out the fix
- **Prioritize:** order feedback by severity (blocking first, nice-to-have last)
- **Don't be polite at the cost of clarity:** "This is wrong" is more useful than "Have you considered maybe possibly looking at this?"

## Integration with dispatcher

When used as part of a dispatch pipeline:

1. The dispatcher spawns the producer agent with a brief
2. The producer delivers output
3. The dispatcher spawns the reviewer agent with: the brief + the output
4. The reviewer returns a verdict
5. If APPROVED → dispatcher proceeds to next stage
6. If CHANGES_REQUESTED → dispatcher respawns the producer with the review feedback appended to the brief
7. If REJECTED → dispatcher escalates to the orchestrator (human or higher-level agent)

Max review rounds: 3. After 3 rounds of CHANGES_REQUESTED on the same task, escalate. Something is fundamentally wrong with the brief, not the output.

## Anti-patterns

- **Reviewer fixes things:** no. The reviewer reports. The producer fixes. If the reviewer starts writing code, it's no longer a review.
- **Reviewing without the brief:** if you don't know what was asked, you can't verify intent alignment. Always require the brief.
- **Opinion-based review:** "I don't like this pattern" is not a finding. "This violates the repo's convention in CONTRIBUTING.md line 15" is.
- **Running every check every time:** if the brief is trivial, don't run the full checklist. Match the depth to the risk.
- **Endless review loops:** cap at 3 rounds. If it keeps failing, the problem is upstream (bad brief, wrong task decomposition, wrong agent).

## Lessons learned

(this section will be populated with real lessons from reviews)
