---
name: "publish-skills"
metadata:
  category: "Automation"
  tags:
    - skills
    - repo
    - publish
    - public
    - sanitization
description: "Publishes workspace skill changes to the public kanam-skills repository safely, ensuring sanitization and verification before committing."
user-invocable: true
---

# Publish Skills

## Purpose

When workspace skill files are updated, they must be synchronized to the public `kanam-skills` repository. This skill automates the process, ensuring:

1. **Sanitization** – personal data and internal project references are removed (via `scripts/sanitize-skills.py`).
2. **Verification** – no remaining personal references, em‑/en‑dashes, or missing `SKILL.md` files.
3. **Controlled publishing** – optional allow‑list for new skills and explicit confirmation before committing.

## When to use

- After modifying existing skill files or adding new ones.
- Before creating a release or sharing the skill collection with other agents.
- When the workspace workflow requires a repeatable, auditable publish step.

## Procedure

1. **Dry‑run check** (no changes written):
   ```bash
   cd $WORKSPACE/skills
   ./scripts/publish-skills.sh --check
   ```
   Review the output: it lists unchanged, updated, and new skills. Ensure no unexpected diffs.
2. **Apply with explicit intent**:
   - To update only existing skills:
     ```bash
     ./scripts/publish-skills.sh --apply
     ```
   - To add new skills (must be allowed explicitly):
     ```bash
     ./scripts/publish-skills.sh --apply --only skill‑a,skill‑b --new
     ```
   *Never run `--apply` without `--only` for new skills; the script aborts otherwise.*
3. **Sanitization verification** – the script runs `scripts/sanitize-skills.py` automatically. After it finishes, run:
   ```bash
   ./scripts/check_em_dash.py
   ```
   The script must print `OK`. Fix any reported issues before proceeding.
4. **Commit and push**:
   ```bash
   cd $WORKSPACE/projects/kanam-skills
   git add -A
   git commit -m "chore: publish updated skills"
   git push
   ```
5. **Mirror sync** (if a mirror repository exists):
   ```bash
   rsync -a --delete $WORKSPACE/projects/kanam-skills/ $WORKSPACE/.github/skills/
   ```

## Decision Rules

- **Do not publish** if the `--check` output shows personal data, internal project names, or missing `SKILL.md` files.
- **Only allow new skills** when the operator explicitly approves the list via `--only … --new`.
- **Abort** on any non‑zero exit code from `scripts/check_em_dash.py`.
- **Rollback**: if after pushing a mistake is discovered, revert the commit with `git revert <hash>` and re‑run the skill after fixing the issue.

## Related Skills

- `skill-collection-maintenance` – monitors collection size limits.
- `skill-workshop-proposals` – handles pending workshop updates before publishing.

---
