---
name: "skill-workshop-proposals"
description: "Apply pending skill workshop proposals; rebase stale update chains in chronological order so each change accumulates on the previous."
---

# Skill workshop proposals

The Skill Workshop queues `update` proposals for workspace skills. Multiple proposals for the same skill accumulate: each was created against the live skill at its time, so apply them in chronological order (oldest first) so changes stack on each other.

## Apply a chain

1. List proposals: `openclaw skills workshop list`. Group pending `update` proposals by target skill and sort each group by proposal date, oldest first.
2. Apply the oldest first: `openclaw skills workshop apply <proposal-id>`. Completion: output says `Applied <id> -> <path>`.
3. If apply fails with `Target skill changed after proposal creation; proposal marked stale`, the proposal is stale: rebase its content onto the current live skill before it can apply.
4. Rebase a stale proposal: `openclaw skills workshop propose-update <skill> --proposal-dir <generation-dir> --description "<note>"`, where `<generation-dir>` is the directory containing the stale proposal's `PROPOSAL.md` (under `~/.openclaw/skill-workshop/proposals/<proposal-id>/generations/<gen>/`). Completion: it prints a new proposal id.
5. Apply the new id: `openclaw skills workshop apply <new-id>`. Then continue the chain with the next oldest proposal.
6. After the chain, sync the mirror and commit: `rsync -a --delete skills/ .github/skills/`, `cp SKILLS-INDEX.md .github/skills/SKILLS-INDEX.md`, run `python3 scripts/check_em_dash.py` (must print "OK"), commit atomically in English, `git pull --rebase`, then push.

## Stale lifecycle

- Only `pending` proposals can be revised, applied, rejected, or quarantined. `revise`, `reject`, and `quarantine` on a `stale` proposal fail with "Only pending proposals can be ...".
- Stale proposals are terminal records: they never touch the live skill and stay listed as `stale`. Leave them; do not try to clean them up.
- A single pending proposal for a skill applies directly; only chains hit stale.
