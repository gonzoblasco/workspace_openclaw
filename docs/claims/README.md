# Claims - knowledge with provenance

A **claim** is a single asserted fact about the workspace, its agents or its projects, written
so that a script can check it. It is the format that `memory-wiki` proposed (ADR-064) minus the
plugin: it lives in the repo, it travels in git, and it is checked by `scripts/check-claims.py`.

## Why this exists

ADR-064 activated `memory-wiki` as an analytics layer over memory, to catch the class of bug the
2026-09-22 ADR audit found by hand: `AGENTS.md` said thinking `max` while the runtime ran `high`,
one policy excluded `minimax-m2.7` while the config ran it, an ADR declared GLM and something else
ran. The plugin was enabled and the detectors worked, but they never had a substrate: after two
months the vault held 86 ingested sources, **one** entity with 4 claims, and every report said
"No issues right now" because there were 4 claims in the whole vault. Writing a well-formed claim
by hand was the expensive step, and nobody pays that price for a vault that lives outside git.

The idea was right, the vehicle was wrong. This directory keeps the idea: one markdown file per
topic, claims with evidence pointing at a real file, and a checker that fails when the claim and
the file disagree.

## Format

One file per topic, `docs/claims/<topic>.md`:

```markdown
---
pageType: claims
topic: models
owner: ADR-090            # the document that owns the fact
updatedAt: 2026-11-16T23:30:00-03:00
claims:
  - id: models.core-primary-model
    text: "El rol main corre deepseek-v4.1-flash:cloud como primario."
    status: active        # active | contested | retracted
    confidence: 0.95      # 0..1
    updatedAt: 2026-11-16T23:30:00-03:00
    evidence:
      - kind: settings    # settings | file | managed-block | adr
        key: model_by_agent
      - kind: file
        path: docs/adr/ADR-090-pensamiento-nivel-configuracion.md
        expect: "deepseek-v4.1-flash:cloud"   # optional: substring the file must contain
---

# Models

Prose is allowed here. The checker reads only the frontmatter.
```

`status: retracted` means the claim is kept for history but no longer governs; the checker
reports it without failing. `status: contested` fails: two sources disagree and nobody decided.

## Evidence kinds

| kind | what the checker does |
|---|---|
| `settings` | reads `memory.db` -> `settings` table, `key` must exist and be non-empty |
| `file` | `path` must exist; `expect` (optional) must appear in the file |
| `managed-block` | the `<!-- BEGIN MANAGED:key -->` block in `AGENTS.md` must exist and contain `expect` |
| `adr` | `path` must exist and its header must not say `Superseded` |

A claim with no evidence, or with evidence that does not resolve, **fails**. That is the whole
point: an unsourced claim is how the 2026-09-22 contradictions were born.

## Checks `scripts/check-claims.py` runs

1. **Every claim has evidence** that resolves (`claim-health`).
2. **`updatedAt` is recent** - default 180 days, `--max-age-days` to override (`stale-pages`).
3. **Confidence** below 0.5 fails, between 0.5 and 0.7 warns (`low-confidence`).
4. **Same topic, same subject, two values** - two active claims in the same topic whose `id`
   shares a prefix and whose `text` names different values for the same thing
   (`contradictions`). Explicit `contradicts: <claim-id>` fails harder.
5. **No `contested` status** without a decision.

Exit 0 clean, 1 findings, 2 no claims found.

## Adding a claim

1. Pick the topic file (`models.md`, `pipeline.md`, `todos.md`, ...) or create one.
2. Add the claim with `id: <topic>.<subject>`.
3. Point `evidence` at the file or setting that would have to change if the claim were false.
4. Run `python3 scripts/check-claims.py` and `python3 scripts/check-claims.py --negative`
   (the negative run seeds a broken claim, verifies every detector fires, and removes it).

## Rule

**A claim is not a source of truth.** The source of truth is what the evidence points at. When
`check-claims.py` fails, the fix is to decide which side is right and correct the other one -
never to soften the claim until the check passes.
