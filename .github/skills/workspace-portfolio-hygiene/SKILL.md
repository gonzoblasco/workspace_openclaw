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

## Real triple-git pattern (2026-09-02, differs from the old init script)

Three layers coexist since 2026-09-02:

- **Workspace git** (`workspace_openclaw`): tracks `projects/**/.knowledge/` as loose blobs (mode `100644`). Root `.gitignore` ignores `/projects/*/.git/`.
- **Aggregate git** (`projects/` -> `projects_openclaw`, PRIVATE): tracks the full source of all projects as plain files. Root `.gitignore` ignores `*/.git/` (the trick that avoids gitlinks) + node_modules/.env/*.db safety net + `PROYECTOS.md`/`.gitignore-template` (workspace files). It is the "see everything" archive, NOT the source of truth.
- **Individual repo** (`gonzoblasco/<slug>`): source of truth for working. Own history, branches, PRs. Its `.gitignore` is respected by the aggregate and workspace.

Rules:
- No `.gitmodules` anywhere (no submodules ever).
- `.knowledge/` is NOT ignored in project `.gitignore` (exclusion lives in `.git/info/exclude`).
- Never commit `.git/` dirs into the aggregate (would become gitlinks).
- Sync the aggregate explicitly with `scripts/aggregate-sync.sh` (status|commit|push|sync|check). It refuses to run if `projects/` points to a remote other than `projects_openclaw`.
- `git reset --hard` in `projects/` can delete `.knowledge/` dirs from disk (project gitignores exclude them) - restore with `git restore --worktree -- projects/` from the workspace.
- Verify: `git ls-files --stage projects/<slug>/` shows `100644 .../HANDOFF.md` (blob), not `160000` (gitlink).
- `scripts/initial-setup.sh` fails on machines that once used submodules: a project's `.git` there is a gitfile (a 47-byte file containing `gitdir: ...`, not a directory), and repos armed with `init+fetch+reset` have no upstream tracking. Recovery that works: detect repos by `[[ "$(git -C dir rev-parse --show-toplevel)" == "$dir" ]]` (covers dir + gitfile and avoids the false positive of resolving to the parent aggregate), and pull with explicit `git pull --rebase origin main` instead of relying on tracking. Local dirty changes (uncommitted source, `.knowledge/` the workspace owns) are respected - the script must never pull over or stash them. Before a real run, probe the existing machine with `--dry-run` to see which projects resolve as real repos vs "would clone" (memory-only).

Old scripts (`init-project.sh` pre-2026-09-02) generated a `.gitignore` ignoring `.knowledge/` and registered submodules - that is obsolete; the script was rewritten.

## Workflow

1. Read-only first: `git status --short`, `git ls-files --stage projects/*` to classify gitlinks (160000) vs blobs (100644) vs untracked.
2. Classify each project. Respect the ADR: excluded/archived projects are NOT candidates - do not touch, do not ask.
3. Archive repos that need it:
   `gh repo archive <owner>/<repo> --yes` (repo becomes read-only, no more pushes).
4. Clean tracked cruft (e.g. `.DS_Store`): `git rm --cached <path>` + `trash` from disk, commit + push (skip push if repo archived).
5. Promote a folder to triple git (see references/workspace-double-git.md):
   - `git init && git branch -m main`
   - Project `.gitignore` WITHOUT ignoring `.knowledge/` (exclusion in `.git/info/exclude`)
   - `gh repo create <owner>/<slug> --private --source=. --push`
   - Workspace tracks `.knowledge/` as blob (NOT `git submodule add`).
   - Register the folder in the aggregate (`git -C projects add <slug>` + commit + `aggregate-sync.sh push`).
   - **Order is critical**: track `.knowledge/` in the workspace. If the internal `.git` is created first and `.knowledge/` is not yet tracked (and `/projects/*/.git/` not ignored), the workspace treats the folder as an embedded repo and will not track it (even with `-f`). Once tracked, the internal `.git` does not interfere.
6. Sync the aggregate repo when project code changes: `./scripts/aggregate-sync.sh sync [msg]` (status/commit/push/check available). The aggregate is NOT automatic.
7. Commit atomically + push workspace with `git pull --rebase` first.
8. Verify final state clean: `git status --short` only intentional changes.

## Pitfalls

- Do NOT use `git submodule add` for workspace projects (breaks the pattern: creates `.gitmodules`, which the rest do not have).
- To undo a mistakenly created submodule: `git rm --cached -f projects/<slug>` + `git config --remove-section submodule.projects/<slug>` + remove `.gitmodules`, and clean the stage entries.
- Archived repos are read-only on GitHub; a local commit will not push (expected).
- Dangling `.knowledge` symlinks (e.g. ai-developer-stack) are findings, not hygiene tasks - repairing a live project's structure needs explicit user go-ahead.

## References

- references/workspace-double-git.md - full verified command set and the real double-git pattern.
