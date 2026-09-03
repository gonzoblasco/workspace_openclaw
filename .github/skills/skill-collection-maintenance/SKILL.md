---
name: "skill-collection-maintenance"
description: "Fix the weekly skill-collection-review cron failing on collection size; remove skills cleanly when asked."
---

# Skill collection maintenance

The Skill Workshop runs a weekly system-owned cron job per writable workspace named `skill-collection-review-<agent>` (declarationKey ``skill-collection-review:<agent>``). In `auto` mode it reviews the writable skill collection and proposes rewrites or drops. It fails only when the collection exceeds its admission limits, but the failure is silent: it shows only in the job's `lastRunError`.

## Diagnose

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

1. `trash skills/<slug>` and `trash .github/skills/<slug>` (never `rm`; the `.github/skills` dir is the mirror).
2. Remove its row from `SKILLS-INDEX.md`, from docs tables (e.g. `docs/pipeline/kanam-product-pipeline.md`), and from other skills' Related Skills sections: `grep -rn "<slug>" --include="*.md" skills docs` and edit each live hit. Keep `memory/archive/` hits untouched (historical).
3. Resync the mirror: `rsync -a --delete skills/ .github/skills/` and `cp SKILLS-INDEX.md .github/skills/SKILLS-INDEX.md`.
4. Run `python3 scripts/check_em_dash.py`; it must print "OK". Commit atomically in English, `git pull --rebase`, then push.
5. Verify no stray references remain with the same grep before closing the turn.
