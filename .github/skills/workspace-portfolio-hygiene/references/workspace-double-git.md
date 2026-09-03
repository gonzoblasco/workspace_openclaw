# Workspace triple-git pattern (updated 2026-09-02)

Observed on live projects: create-stack, kanam-mind, a11y-fixer. The template `init-project.sh` was rewritten on 2026-09-02 to match the real pattern AND the new aggregate repo.

## The three layers (2026-09-02+)

```
workspace/                  -> workspace_openclaw   (our essence: memory, skills, docs, scripts)
└── projects/               -> projects_openclaw    (aggregate: full source of all 20 projects, PRIVATE)
    └── <slug>/             -> gonzoblasco/<slug>   (individual repo: source of truth for working)
        ├── .knowledge/     # institutional memory - tracked ONLY by the workspace git
        └── <code>          # tracked by the individual repo; mirrored by the aggregate
```

- **Workspace tracks `.knowledge/` as loose blobs** (mode `100644`), NOT as gitlink. Its root `.gitignore` has `/projects/*/.git/` so the embedded repos do not become gitlinks.
- **Aggregate (projects/) tracks the full source as plain files.** Its root `.gitignore` has `*/.git/` (the trick that makes git descend into content instead of creating gitlinks), plus `PROYECTOS.md` and `.gitignore-template` (those belong to the workspace). It also has the root safety net (node_modules, .next, dist, .env, *.db).
- **Individual project repo** keeps its own `.git`, history, branches, PRs. Its `.gitignore` is respected by both the aggregate and the workspace in subdirectories.
- `.knowledge/` is NOT ignored in project `.gitignore` files (both workspace and project repo track it - double tracking, and the aggregate skips it where the project gitignore excludes it).
- No `.gitmodules` anywhere (no submodules ever).

## The gitlink-avoidance trick

Git refuses to descend into a directory that has a `.git/` (it becomes a gitlink/submodule-ish pointer). When the `.git/` is **ignored** by the parent repo's `.gitignore`, git treats the folder as plain content and descends. This is how:
- workspace sees `projects/<slug>/.knowledge/` as blobs (its `.gitignore` ignores `/projects/*/.git/`),
- aggregate sees `projects/<slug>/` full content (its `.gitignore` ignores `*/.git/`).

## Verify

```bash
# Aggregate: no gitlinks (all content as plain files)
git -C projects ls-files -s | grep '^160000' || echo "no gitlinks"

# Workspace: .knowledge tracked as blob, not gitlink
git -C workspace ls-files --stage projects/a11y-fixer/.knowledge/

# Both repos healthy and pointing at the right remotes
git -C workspace remote get-url origin          # workspace_openclaw
git -C projects remote get-url origin           # projects_openclaw
git -C projects/a11y-fixer remote get-url origin # gonzoblasco/a11y-fixer
```

## Promote a folder to triple git (verified steps)

1. `git init && git branch -m main` in the project folder.
2. Create project `.gitignore` WITHOUT ignoring `.knowledge/` (exclusion goes to `.git/info/exclude`).
3. `gh repo create <owner>/<slug> --private --source=. --push`.
4. Workspace tracks `.knowledge/` as blob (NOT `git submodule add`, NO `.gitmodules`).
5. Register the folder in the aggregate: `git -C projects add <slug> && git -C projects commit` (needs `*/.git/` already ignored - it is, since 2026-09-02).
6. **Order is critical** (workspace): the `.knowledge/` must be tracked in the workspace while the folder has NO `.git` in it, OR while `/projects/*/.git/` is ignored. If the internal `.git` exists and the `.gitignore` does not cover it, the workspace sees an embedded repo and refuses to track its contents (even with `-f`).

Use `scripts/init-project.sh <slug>` - it does all of this.

## Sync the aggregate

The aggregate is NOT automatic: a change inside `projects/<slug>/` is visible to both the individual repo and the aggregate. Keep it in sync with:

```bash
./scripts/aggregate-sync.sh status   # what changed
./scripts/aggregate-sync.sh sync     # commit (default msg) + pull --rebase + push
./scripts/aggregate-sync.sh check    # no gitlinks
```

Never push the aggregate from inside a project repo, never commit the `.git/` dirs, and never make `projects/` push to anything but `projects_openclaw` (the script refuses if the remote is wrong).

## Dangerous: `git reset --hard` inside projects/

Many project `.gitignore` files exclude their own `.knowledge/` (correct double-git). The aggregate respects that, so a `git reset --hard origin/main` in `projects/` DELETES those `.knowledge/` dirs from disk. They are committed in the workspace git - restore with:

```bash
cd workspace && git restore --worktree -- projects/
```

## Verified commands

```bash
# State of a submodule/gitlink (should not exist anymore)
git ls-files --stage projects/<slug>/

# Archive a repo on GitHub (read-only afterward)
gh repo archive <owner>/<repo> --yes

# Check archive state of a repo
gh repo view <owner>/<repo> --json isArchived

# Undo a mistakenly created submodule/gitlink
git rm --cached -f projects/<slug>
git config --remove-section submodule.projects/<slug> 2>/dev/null || true
rm -f .gitmodules
```

## Audit classification (2026-08-28 reference, kept for history)

- **BLOB(.knowledge) - correct pattern:** a11y-fixer, create-stack, kanam-forge, kanam-mind, kanam-solitaires, kanam-story, portfolio-strategy, quedamos, soporteml-v3, soporteml, ultimo-turno
- **GITLINK (resolved 2026-09-02):** accessible-ui, ai-developer-stack, create-with-ai, soporteml-v4 - were gitlinks in the workspace index; cloned and converted to plain embedded repos (gitlinks removed from index, `.git/` ignored).
- **REPO-PROPIO/other:** kanam-skills (standalone skills repo on GitHub, no .knowledge needed)

## Findings to respect

- Accessible-ui and create-with-ai: archived, do not touch.
- SOPORTEML (v3/v4): closed decision (excluded from public portfolio), do not touch.
- ai-developer-stack: `.knowledge` is a broken symlink in its GitHub repo (target dir missing locally and on GitHub). Live agent-skills project. Repair needs explicit user go-ahead.
