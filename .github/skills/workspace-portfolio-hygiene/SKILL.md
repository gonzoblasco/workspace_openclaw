---
name: "workspace-portfolio-hygiene"
description: "Audit, clean, and structure workspace projects: classify gitlinks vs blobs, honor ADR decisions, archive repos, promote folders to double git."
---

# Workspace portfolio hygiene

Use when auditing `projects/*` for cleanliness, deciding what to archive, promoting a folder to a proper double-git project, or cleaning up git cruft (`.DS_Store`, dangling symlinks, gitlinks). Follows the ROADMAP items 0.2 (hygiene) and 2.1 (portfolio strategy).

## Hard rule: ADR is the authority

"Defined in ADR = resolved, do not re-open." If an ADR marks a project as EXCLUDED or ARCHIVED:
- Do NOT list it as a candidate in hygiene audits.
- Do NOT re-ask its fate unless the user explicitly requests it.
- Do NOT modify it. Ever.

Make it executable in the ADR text with an explicit clause:
> **DO NOT TOUCH**: this project is not modified, its fate is not re-decided, and it is not listed as a candidate in hygiene audits. The exclusion is closed.

## Real double-git pattern (differs from the init script)

The `init-project.sh` template ignores `.knowledge/` and registers a submodule. Active projects do NOT do that. The real pattern:

- **Workspace tracks `.knowledge/` as loose blobs** (mode `100644`).
- Project folder keeps its own git repo (`.git`) that coexists.
- `.knowledge/` is NOT ignored in the project `.gitignore` (both workspace and project repo track it - double tracking).
- No `.gitmodules` in the workspace (no submodules).
- Verify: `git ls-files --stage projects/<slug>/` shows `100644 .../HANDOFF.md` (blob), not `160000` (gitlink).

## Workflow

1. Read-only first: `git status --short`, `git ls-files --stage projects/*` to classify gitlinks (160000) vs blobs (100644) vs untracked.
2. Classify each project. Respect the ADR: excluded/archived projects are NOT candidates - do not touch, do not ask.
3. Archive repos that need it:
   `gh repo archive <owner>/<repo> --yes` (repo becomes read-only, no more pushes).
4. Clean tracked cruft (e.g. `.DS_Store`): `git rm --cached <path>` + `trash` from disk, commit + push (skip push if repo archived).
5. Promote a folder to double git (see references/workspace-double-git.md):
   - `git init && git branch -m main`
   - Project `.gitignore` WITHOUT ignoring `.knowledge/`
   - `gh repo create <owner>/<slug> --private --source=. --push`
   - Workspace tracks `.knowledge/` as blob (NOT `git submodule add`).
   - **Order is critical**: track `.knowledge/` in the workspace. If the internal `.git` is created first and `.knowledge/` is not yet tracked, the workspace treats the folder as an embedded repo and will not track it (even with `-f`). Once tracked, the internal `.git` does not interfere.
6. Commit atomically + push workspace with `git pull --rebase` first.
7. Verify final state clean: `git status --short` only intentional changes.

## Pitfalls

- Do NOT use `git submodule add` for workspace projects (breaks the pattern: creates `.gitmodules`, which the rest do not have).
- To undo a mistakenly created submodule: `git rm --cached -f projects/<slug>` + `git config --remove-section submodule.projects/<slug>` + remove `.gitmodules`, and clean the stage entries.
- Archived repos are read-only on GitHub; a local commit will not push (expected).
- Dangling `.knowledge` symlinks (e.g. ai-developer-stack) are findings, not hygiene tasks - repairing a live project's structure needs explicit user go-ahead.

## References

- references/workspace-double-git.md - full verified command set and the real double-git pattern.
