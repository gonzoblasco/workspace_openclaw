---
name: "workspace-portfolio-hygiene"
description: "Auditar projects/* por limpieza: decidir que archivar, promover una carpeta a proyecto double-git, y limpiar restos de git (.DS_Store, symlinks rotos, gitlinks)."
disable-model-invocation: true
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
- When adding a project folder to the aggregate, `git add <slug>/` on a dir that ALREADY has a `.git/` inside creates a gitlink (mode `160000`, one line) even though `*/.git/` is gitignored - the aggregate already has most projects as plain files because they were added before their `.git/` existed. To force flat-file tracking for a project that has `.git/`: `mv <slug>/.git /tmp/backup`, `git add <slug>/` (now resolves to individual blobs via the project's own `.gitignore`), verify `git ls-files -s <slug>/ | grep -c 160000` == 0, then `mv /tmp/backup <slug>/.git`. Confirm no node_modules/build output got staged. No `.knowledge/` to preserve for this case (the workspace repo tracks it and the project's `.git/` is restored before commit).
- `scripts/initial-setup.sh` fails on machines that once used submodules: a project's `.git` there is a gitfile (a 47-byte file containing `gitdir: ...`, not a directory), and repos armed with `init+fetch+reset` have no upstream tracking. Recovery that works: detect repos by `[[ "$(git -C dir rev-parse --show-toplevel)" == "$dir" ]]` (covers dir + gitfile and avoids the false positive of resolving to the parent aggregate), and pull with explicit `git pull --rebase origin main` instead of relying on tracking. Local dirty changes (uncommitted source, `.knowledge/` the workspace owns) are respected - the script must never pull over or stash them. Before a real run, probe the existing machine with `--dry-run` to see which projects resolve as real repos vs "would clone" (memory-only).

Old scripts (`init-project.sh` pre-2026-09-02) generated a `.gitignore` ignoring `.knowledge/` and registered submodules - that is obsolete; the script was rewritten.

## Post-pull verification (after a machine ran initial-setup.sh)

After `git pull --rebase` from a machine that just ran the setup, inspect every dirty subrepo and repair the two expected residues; then verify the memory DB was cataloged.

1. Classify each dirty state (`git -C projects/<slug> status --porcelain`):
   - `?? .knowledge/` (untracked, not in repo history): add the triple-git exclude - `printf '\n# Triple-git: .knowledge/ belongs to the workspace git\n.knowledge/\n' >> projects/<slug>/.git/info/exclude` - and the repo goes clean.
   - `D <tracked file>` (deleted, exists in HEAD): the aggregate checkout excluded it (e.g. `.vscode/`, `.env`) and reset left it out - restore with `git -C projects/<slug> restore <path>` after confirming it is in HEAD (`git show HEAD:<path>`). For a tracked `.env` in a public repo, DO NOT auto-restore - record a todo (possible historical secrets) and ask Gonzo whether to restore or purge history.
   - `M .knowledge/*` (modified, tracked in repo history): known double-tracking debt - the workspace version is the authority; do NOT touch.
2. After repairs, one repo may still carry a real blocker (e.g. archived target) - record it as a todo, never leave it silent.
3. Sync the workspace daily to the DB (DB-first): write the post-pull section with `scripts/memory-end-session.py --project <name> --summary <text> --date <today>`, then run `scripts/memory-db.sh catalog`. If catalog crashes with `IndexError` in topic-centroid math, the DB mixes embedding dimensions (old 32-dim vectors vs current 768-dim) - fix `compute_topic_centroids` to only sum vectors of equal length per topic, then re-run.

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
- Archived repos are read-only on GitHub; a local commit will not push and stays `ahead=1` locally (expected - report it, do not unarchive without explicit go-ahead).
- Cascading pushes across machines: when a project push is rejected non-fast-forward and you had local commits, `git pull --rebase origin main` may discard them with "contenidos del parche ya están en upstream" - the remote already has those changes (the other machine pushed them), so the local copies were redundant, not lost. Confirm `status -sb` shows "Everything up-to-date", not missing work. After the cascade, re-check the workspace git and aggregate: if a project repo tracks old `.knowledge/`, its rebase checkout overwrites the workspace's correct copies on disk - restore with `git restore --worktree -- projects/` (workspace memory wins).
- Dangling `.knowledge` symlinks (e.g. ai-developer-stack) are findings, not hygiene tasks - repairing a live project's structure needs explicit user go-ahead.

## References

- references/workspace-double-git.md - full verified command set and the real double-git pattern.
