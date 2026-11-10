---
name: debugging-and-error-recovery
description: Locates and fixes the real cause of a failure instead of the nearest symptom. Use when something is broken and the cause is not yet proven (a stack trace, a red build, a failing test, a production error, "works locally, crashes in prod"). Use when a fix must be justified by evidence, not by a plausible story. Use when a check passes but you are not sure it proved anything.
disable-model-invocation: true
metadata:
  owner: kanam-dev
  status: active
---

# Debugging and Error Recovery

## Overview

A bug is a question with exactly one right answer and many plausible wrong ones. Debugging is the
discipline of replacing the plausible story with the proven cause: localize where it breaks,
reproduce it on demand, falsify hypotheses until one survives, fix, and prove the fix with the same
evidence that reproduced the bug.

The failure mode this skill exists to prevent is not "couldn't fix it". It is **fixing the wrong
thing and declaring victory**: the first error in the log is almost never the root cause, a green
check is not proof it tested anything, and a fix without a reproduction is a guess that happens to
compile. "Seems fixed" is not done.

## When to Use

- A stack trace, red build, failing test, or production error needs a root cause.
- "It works locally, it crashes in production" (or "in CI", or "on WebKit").
- A bug was reported but not yet reproduced.
- A fix is proposed and you need to prove it addresses the cause, not a symptom.
- A check went green but you cannot say what it actually proved.

**NOT for:**
- Instrumenting code so failures are diagnosable in the first place - that is
  `observability-and-instrumentation`, which makes this skill fast next time.
- Reviewing a finished change for defects - that is `hermes-reviewer` / the `review-team` fleet.
- Verifying behavior against a spec end-to-end - that is `hermes-qa`.

## The Non-Negotiables

These come from failures this workspace has actually paid for. They are not advice.

1. **Reproduce before you fix.** A fix without a failing reproduction is unfalsifiable. The
   reproduction is also your proof of done: it fails before, passes after. (See `test-driven-development`,
   the Prove-It pattern.)
2. **The first error in the log is a symptom, not the cause.** Read down the chain, not the top line.
   The cause is often several calls earlier, or in a different environment.
3. **A green check is not proof it tested anything.** Zero cases run is not green; a SKIP is not a PASS;
   a missing input file is not "empty". (See `verification-gates`.) A gate run to "confirm the fix" can
   itself be the thing lying to you.
4. **Do not fix by masking.** Widening an assertion, disabling a validation, swallowing the exception,
   or catching-and-logging is not a fix unless the *cause* is that the check was wrong. Relaxing the
   proof hides the defect.
5. **The diagnosis is a claim until proven.** State it as a hypothesis you are trying to break, not a
   story you are trying to confirm.

## Process

### 1. Localize: where does it actually break?

Start from the real artifact, not the report of it. Read the actual error output, not a summary.

- **The stack trace:** read the whole frame chain. The line that *throws* is rarely the line that is
  *wrong*; the wrong line is usually the nearest frame inside your code.
- **The log:** a single error is a symptom. Look for the first anomaly, the last successful step, and
  what changed between them.
- **The diff:** `git log --oneline -1 -- <path>`, `git blame -L <range> <path>`, `git bisect` when a
  change is suspected. Recent deploys and merges are the first suspects for a regression.
- **The boundary:** failures cluster at trust boundaries - parsing external input, calling an external
  service, reading from disk/network, deserializing. Check there first.

Completion: you can name the exact file and line where behavior diverges from expectation, with the
output that shows it.

### 2. Reproduce: make it fail on demand

A bug you cannot reproduce is a bug you cannot fix, only guess at.

- Find the **smallest** input and the **shortest** path that still fail. Minimal reproduction removes
  confounders and doubles as a regression test.
- For a reported bug, write the failing test **first** - that is the Prove-It pattern. It must fail for
  the right reason (assert the bug, not a typo).
- If it only fails in one environment, capture the environment: `node --version`, lockfile state, env
  vars present, the browser/engine. "Only in prod" is a reproduction you have not finished.

Completion: a command that fails, deterministically, and would pass if the bug were fixed.

### 3. Hypothesize, then falsify

Generate candidate causes, then design the cheapest test that would **disprove** each one - not the
cheapest test that confirms the one you like.

```
What happened?   error, symptom, blast radius
When did it start?  timestamp vs last deploy / merge / config change
Where in the code?  stack frame, file, line, function
Why did it happen?  root cause, not the proximate throw
How to fix?      immediate fix + preventive measure
```

Rank by likelihood but test by cost: run the one-second check before the ten-minute one. Add a
temporary log or a focused assertion rather than re-reading code and "reasoning" about it. Re-reading
is doubt; a probe is evidence.

Completion: one hypothesis survives a real disproof attempt and explains every observed fact
(including the ones that did not fit the first story).

### 4. Fix the cause

- Change the minimum that resolves the proven cause. Resist fixing the symptoms you passed on the way.
- If the cause is a **wrong assumption**, fix the assumption and find its other users - the same bug
  usually lives in more than one place (grep for the pattern, not just the line).
- If the cause is a **missing guard** at a trust boundary, add the guard where untrusted data enters,
  and add a test that fails without it.

Completion: the reproduction from step 2 now passes, and the change is the smallest that does so.

### 5. Prove the fix - and prove the proof

- Re-run the reproduction: it passes. Run the **full** gate (project test suite + lint + build): no
  regressions.
- Re-run the gate **the way it fails**: neutralize your fix and confirm the test goes red. A regression
  test that passes with the fix reverted is testing nothing.
- Read the gate's **verdict**, not its heading: the exit code (`echo $?`) and the summary line
  (`Found N errors`, `N passed`). A quoted excerpt that stops before the verdict is not evidence.
- If the environment cannot run the gate, say so as `blocked` with the reason - never "assumed".

Completion: reproduction fails→passes; gate green with its exit code and summary cited; the test
demonstrably detects the bug.

### 6. Dev vs prod divergence (the "works on my machine" case)

When it only breaks outside your machine, walk this list before touching code:

- **Missing or different env vars** - diff them, don't assume they are set.
- **Different runtime version** - check `engines` / the CI matrix against local.
- **Build vs dev mode** - minification, tree-shaking, and dynamic `require()`/import behave differently
  in a production build. Reproduce with the production build locally.
- **Local service vs remote** - localhost DB vs external connection string, SSL, read replicas.
- **Data** - prod has rows your fixture doesn't, including the nulls and the boundary values.

Completion: the divergence is named and reproduced in the matching environment, or explicitly declared
unreproducible with the evidence of what was tried.

### 7. Recover, don't just patch

When the failure is live, recovery and repair are two different jobs:

- **Stop the bleeding first** (rollback, feature flag off, circuit-break) if users are affected.
- **Separate the mitigation from the fix.** A rollback resolves the incident; it does not find the
  cause. Do not let "it's green again" end the investigation.
- **Write the cause down.** The post-mortem / learning entry is the durable output; the next person
  starts from your steps, not from zero.

Completion: service restored (or declared), cause identified, and the finding recorded where the next
debugger will find it.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The error message says X, so the cause is X" | The message names where it threw, not why. Read the chain. |
| "It's probably the network / a flake" | "Probably" is a hypothesis. Prove it or drop it. A flake you have not explained is a bug with a schedule. |
| "I changed something and it works now" | Did the change fix the cause, or move the symptom? Re-run the reproduction and the gate; state which. |
| "The test passes, so it's fixed" | The test passes - did it ever fail? A test that never went red proves nothing (step 5). |
| "CI is green" | Read the exit code and the summary line. Jobs go green having run zero cases. |
| "I'll just catch the error so it stops crashing" | Swallowing converts a visible bug into silent data corruption. Fix the cause or fail loudly. |
| "Locally it works, it's a prod issue, nothing I can do" | Step 6 exists. Build prod locally, diff the env, reproduce the data. |
| "I don't have time to reproduce, let me just fix it" | A guess that compiles costs more later than the ten minutes to reproduce now. |

## Red Flags

- A fix with no reproduction and no test that fails without it.
- The commit message describes the *fix* but the diff touches symptoms.
- An assertion loosened, a validation disabled, or a `try/catch` added to make a test pass.
- "Should be fixed now" / "looks like it works" as the closing statement.
- A stack trace read top-to-bottom and the top frame declared the cause.
- A gate cited by its heading (`Checked 55 files`) without its verdict line or exit code.
- A regression declared resolved with "CI green" and no exit code.
- A flaky test marked "known flake" with no explanation of *why* it is flaky.
- A production incident closed by rollback with no root cause written down.

## Verification

Before declaring a bug fixed:

- [ ] The failure was reproduced on demand (a command that fails, and why it fails)
- [ ] The reproduction is a test that goes red without the fix and green with it
- [ ] The named cause explains every observed fact, not just the loudest one
- [ ] The fix is the minimum that resolves the cause; no symptom was masked
- [ ] The full gate ran: exit code and summary line cited, not the heading
- [ ] No assertion was weakened or validation disabled to reach green
- [ ] If environment-specific, the divergence is named and reproduced in the matching env
- [ ] The reproduction command and its failing output are archived in `debug/repro.txt`, with the exit code before and after the fix
- [ ] The cause and the recovery step are recorded where the next debugger will look
- [ ] El comando que reproduce el bug esta escrito, y su salida quedo archivada antes y despues del fix.

## Interaction with Other Skills

- **`test-driven-development`**: the Prove-It pattern is this skill's step 2. Write the failing test
  first; that test is the reproduction *and* the regression guard.
- **`observability-and-instrumentation`**: when you cannot tell what happened, the gap is missing
  telemetry. Fixing it here is one-off; instrumenting it is the durable fix.
- **`doubt-driven-development`**: when a failure mode is surfaced by a review, drop in here to localize
  and prove it; the adversarial review finds the crack, this skill finds the cause.
- **`verification-gates`**: the honesty rules for step 5 - zero cases is not green, a SKIP is not a
  PASS, a missing input is not empty.
- **`compatibility-testing` / `cross-engine-css-measurement`**: the multi-engine case of step 6.
- **`hermes-qa`**: verifies behavior against the spec with real execution; this skill verifies a *fix*
  against a *cause*.

## References

- Prove-It pattern and RED step: `agents/kanam-dev/skills/test-driven-development/SKILL.md`
- Gate honesty (false green): `skills/verification-gates/SKILL.md`
- Evidence vocabulary (verified / partial / self-reported / blocked): `skills/trust-vocabulary-report/SKILL.md`
- Adversarial review of a finished change: `agents/kanam-dev/skills/hermes-reviewer/SKILL.md`

---

_No fix is done until the bug reproduces without it and disappears with it._
