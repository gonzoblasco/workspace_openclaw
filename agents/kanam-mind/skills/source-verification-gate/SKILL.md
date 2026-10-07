---
name: "source-verification-gate"
metadata:
  category: "Research"
  tags:
    - verification
    - evidence
    - gate
    - honesty
description: "Block any claim that lacks an opened source and a checked date before it leaves the agent. Use before writing a conclusion, a memory entry, a brief, or a handoff - the internal gate that stops unverified assertions and invented tool results."
user-invocable: true
---

# source-verification-gate

A gate, not a workflow. It runs **at the moment before an assertion leaves the agent** and either passes it or blocks it. Its only job is to make it impossible to state something that was not checked.

## When to use it

- Before writing any conclusion, brief, memory entry, or handoff.
- Immediately after producing a result that "looks right" - that is exactly when fabrication happens.
- Whenever a tool call, a citation, or a datum is about to be presented as fact.

## The failure it exists to stop

The canonical failure: reporting a tool result, a quotation, or a command outcome that **was never actually executed or opened**. It feels like a report; it is a fabrication. This gate treats "I ran it" as an unverified claim until the raw output is in hand.

## Checklist - all must pass

1. **Opened, not recalled.** Every cited source was opened in this task. A source remembered from training is not a source.
2. **Raw output in hand.** Every claimed tool execution has its actual result, not a reconstructed one. If the call errored, the gate reports the error - never a plausible substitute.
3. **Date on the mutable.** Prices, versions, dates, PR/issue states, and similar carry the date they were observed.
4. **Label matches reality.** An `[obs]` points to a concrete location; an `[inf]` is not dressed as an `[obs]`.
5. **Conflict surfaced.** Any disagreement between sources is present in the output, not smoothed away.
6. **Unknown stays unknown.** What was not established is declared, not padded with a guess.

## Verdicts

- **PASS** - every claim satisfies the checklist. Release it.
- **BLOCK** - at least one claim fails. Do not soften it into prose. Either:
  - open the missing source and re-verify, or
  - downgrade the claim to `[inf]`/`[unk]` with its real support, or
  - drop it and say why.

Blocking is a success, not a delay. A blocked fabrication is the gate working.

## Anti-patterns the gate refuses

- A fabricated tool call, result, or citation.
- "Verificado" with no path/URL and no date.
- Silently repairing a failed step so the story stays clean.
- Confirming a datum from memory when it changes over time.

## Output

When gating a piece of work, state the verdict explicitly:

```
GATE: PASS | BLOCK
Failed item(s): <none | the claim + why it fails>
Action: <released | source opened and re-verified | downgraded to [inf]/[unk] | dropped>
```
