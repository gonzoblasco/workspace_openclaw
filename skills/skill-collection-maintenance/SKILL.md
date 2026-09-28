---
name: "skill-collection-maintenance"
description: "Fix the weekly skill-collection-review cron failing on collection size; remove skills cleanly when asked."
---

# Skill collection maintenance

The Skill Workshop runs a weekly system-owned cron job per writable workspace named `skill-collection-review-<agent>` (declarationKey ``skill-collection-review:<agent>``). In `auto` mode it reviews the writable skill collection and proposes rewrites or drops. It fails only when the collection exceeds its admission limits, but the failure is silent: it shows only in the job's `lastRunError`.

This is the collection-review job and clean removal. For the model prompt budget (what reaches the model, the 18,000-char catalog limit, curating with `disable-model-invocation` instead of deleting), see the `skill-catalog-budget` skill.

## Diagnose (collection review failure)

1. List automations with `automations(action: "list", includeDisabled: true)` and find the job named `skill-collection-review-*`.
2. If `lastRunStatus: "error"` with `Writable skill collection is N bytes; the review limit is 240000`, the collection exceeds the byte limit.
3. Recompute the current total: sum `wc -c <skills/*/SKILL.md` over the workspace `skills/` dir (this equals the writable byte count).

## Hard limits (fixed constants, not configurable)

- Max 200 skills and max 240,000 bytes of `SKILL.md` content across the writable collection.
- No config raises these: `skills.workshop.autonomous.mode` (`auto`|`propose`|`off`) and `skills.workshop.allowSymlinkTargetWrites` are the only `skills.workshop.*` fields.

## Size math that rules out compaction alone

The 10,000-char SKILL.md cap still averages ~10 KB per skill, so 240 KB fits only ~24-30 skills. Compacting every oversized SKILL.md to 10K yields roughly 25% savings (measured: 546 KB total -> ~472 KB after cutting 22 skills to 10K). A large curated collection cannot pass the review by compaction alone.

## Decide the fix (in this order)

1. **Large collection stays large**: propose setting `skills.workshop.autonomous.mode` to `propose` (via the gateway config flow, operator approval required). Collection review stops and the job disables itself; normal skill proposals still go through approval. `off` stops everything.
2. **User is willing to prune**: shrink toward ~24-30 skills and re-measure the total byte count before expecting the review to pass.
3. **Leave it failing**: harmless, the job just records an error every 7 days; warn the user it only pollutes logs.

## Remove a skill cleanly (workspace conventions)

1. `trash skills/<slug>` (never `rm`). The mirror `.github/skills/` was removed on 2026-09-28 (ADR-079): there is no mirror copy to delete anymore.
2. Remove its row from `SKILLS-INDEX.md`, from docs tables (e.g. `docs/pipeline/kanam-product-pipeline.md`), and from other skills' Related Skills sections. **Scan the FULL workspace, not just `skills docs`:** `grep -rn "<slug>" --include="*.md" --include="*.bats" skills tests docs` and edit each live hit. Keep `memory/archive/` hits untouched (historical).
3. Run `python3 scripts/check_em_dash.py`; it must print "OK". Commit atomically in English, `git pull --rebase`, then push.
4. **Verify no stray references remain BEFORE closing the turn** - and never truncate the scan with `| head` (memory/archive hits can fill the output and hide live hits in `skills/` or `tests/`):
   - `grep -rn "<slug>" --include="*.md" --include="*.bats" skills tests | grep -v "memory/archive"` must be empty.
   - **Run the bats suite locally** (`npx bats tests/bash/`) - a deleted skill's script can orphan a test (e.g. `progress-tracker.bats` referenced `narrative-content/scripts/progress-tracker.sh` and broke CI with exit 127). Delete orphaned tests with the skill.

## Sync the index when skills are added

The index drifts when skills land without being documented (2026-09-03: 15 skills missing; index said 66, dir had 81).

1. Extract listed slugs: `grep -oE '\[[a-z0-9-]+\]\(skills/[a-z0-9-]+/' SKILLS-INDEX.md | sed -E 's/\[([a-z0-9-]+)\]\(skills\/[a-z0-9-]+\//\1/' | sort -u`.
2. Diff both directions against `ls -1 skills/ | grep -v -E 'CHANGELOG|\.zip' | sort` with `comm -23` (in dir, not listed) and `comm -13` (listed, not in dir).
3. For each missing skill, read its frontmatter `description:` and add a row in the matching category table; update the date line and the "Totales activas" count.
4. Verify both `comm` directions are empty (dir count == listed count) before closing. There is no mirror to sync (removed 2026-09-28, ADR-079); commit atomically in English, `git pull --rebase`, push.
