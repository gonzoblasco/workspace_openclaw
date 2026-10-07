---
name: "evidence-chain-audit"
metadata:
  category: "Research"
  tags:
    - evidence
    - audit
    - citations
    - review
description: "Audit a brief, memory entry, or handoff so every citation actually supports the conclusion beside it, and every link resolves. Use after producing research output and before publishing or handing it off - the check that a claim's evidence is as strong as it looks."
user-invocable: true
---

# evidence-chain-audit

Where `source-verification-gate` guards the moment of writing, this skill audits a **finished artifact**: does each link in the chain from raw source to stated conclusion actually hold?

## When to use it

- After a brief, memory entry, or handoff is written and before it is published or returned.
- When a conclusion "feels stronger than its evidence".
- When reviewing someone else's - or your own earlier - research output.

## The chain

```
source (opened, dated)
   └─ quote / datum (exact, located)
        └─ claim (what is asserted)
             └─ conclusion (why it matters)
```

A link is broken when any step does not actually carry the next one.

## Audit procedure

1. **Enumerate claims.** List every assertion in the artifact, labeled `[obs]`/`[inf]`/`[unk]`.
2. **Resolve each link.**
   - Does the cited source exist and open? (a link that 404s is a broken link)
   - Does the quoted datum sit where it is claimed to sit?
   - Does the datum support the claim, or merely sit near it?
   - Does the claim support the conclusion without a leap?
3. **Hunt orphan claims.** An `[obs]` with no source, an `[inf]` with no named observations, a conclusion with no supporting claim.
4. **Test the weakest link.** Find the claim carrying the most weight and interrogate it hardest. Conclusions usually hang on one.
5. **Record conflicts.** Any source disagreement must appear; if it was flattened, restore it.

## Findings format

| # | Claim | Link | Verdict | Fix |
|---|---|---|---|---|
| 1 | `<claim>` | datum→claim | HOLDS / BROKEN | `<what to do>` |

Verdicts: **HOLDS** (chain intact) · **BROKEN** (a link fails) · **ORPHAN** (no source/support).

## Rules

- A citation that merely *co-occurs* with a conclusion is not evidence for it. Proximity is not support.
- Do not repair by rewording the claim to match weak evidence unless the reworded claim is the honest one - sometimes the fix is dropping the claim.
- An artifact with any BROKEN or ORPHAN finding is not ready to hand off.

## Handoff

Report: findings table, the weakest link, the conflict status, and - if any finding remains - the artifact is returned as **not cleared**, with the exact fixes required.
