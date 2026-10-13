# Workspace + projects git pattern (updated 2026-10-13, ADR-098)

Two layers, not three. `projects/` is a flat container folder, ignored 100% by the
workspace git; each `projects/<slug>/` is its own repo (source of truth), and it
tracks its own `.knowledge/` - the memory travels with the project.

## The two layers (2026-10-13+)

```
workspace/                  -> workspace_openclaw   (memory, skills, docs, scripts)
└── projects/               (flat container folder - NOT a repo; ignored by workspace git)
    └── <slug>/             -> gonzoblasco/<slug>   (the project's own repo: source of truth)
        ├── .knowledge/     # institutional memory - tracked by the project repo, travels with it
        └── <code>          # tracked by the same project repo
```

- **Workspace git** (`workspace_openclaw`): its root `.gitignore` has `/projects/`,
  so it ignores the whole container. It does NOT track project code or `.knowledge/`.
- **Individual project repo** keeps its own `.git`, history, branches, PRs, and its
  `.knowledge/`. It is the only source of truth.
- **No aggregate layer.** The old private `projects_openclaw` aggregate (a flat mirror
  of `projects/`) is retired and archived on GitHub. `scripts/aggregate-sync.sh` is a
  stub that fails with the reason.
- No `.gitmodules` anywhere (no submodules ever).

## Why `git -C projects ...` shows a remote

`projects/` has **no `.git` of its own**. Running `git -C projects ...` walks up to the
workspace `.git` and reports *its* remote (`workspace_openclaw`). That is expected - it
is NOT evidence of an aggregate repo. Confirm a project is its own repo with:

```bash
[[ "$(git -C projects/<slug> rev-parse --show-toplevel)" == "$PWD/projects/<slug>" ]] && echo "own repo"
```

## Verify

```bash
# Each project resolves to itself (own repo), not the workspace
git -C projects/a11y-fixer rev-parse --show-toplevel    # .../projects/a11y-fixer
git -C projects/a11y-fixer remote get-url origin         # gonzoblasco/a11y-fixer

# projects/ must NOT be a repo
[ -e projects/.git ] && echo "WRONG: projects/ has .git" || echo "ok: flat folder"
```

## Create a project

Use `scripts/init-project.sh <slug>` - it creates `projects/<slug>/` with its
`.knowledge/` (BRIEF + STATUS), scaffolds the code, and initializes the project's own
repo (creating the private GitHub repo if needed). Code and `.knowledge/` commit
together to the project repo.

## Promote an existing folder

1. `git init && git branch -m main` in the project folder.
2. Project `.gitignore` may leave `.knowledge/` tracked (preferred) - the memory
   travels with the project. Historical repos that exclude it do so via
   `.git/info/exclude`; they still work but their memory is local-only.
3. `gh repo create <owner>/<slug> --private --source=. --push`.
4. No aggregate registration step (the layer is gone).

## Dangerous: `git reset --hard` inside a project

A project's `git reset --hard` only affects that project. There is no aggregate
checkout that could wipe sibling `.knowledge/` dirs. Local uncommitted `.knowledge/`
in a project that excludes it is at risk as with any repo - back it up first.

## Verified commands

```bash
# Archive a repo on GitHub (read-only afterward)
gh repo archive <owner>/<repo> --yes

# Check archive state of a repo
gh repo view <owner>/<repo> --json isArchived

# Undo a mistakenly created submodule/gitlink in the workspace (should not happen)
git rm --cached -f projects/<slug>
git config --remove-section submodule.projects/<slug> 2>/dev/null || true
rm -f .gitmodules
```

## Audit classification (2026-08-28 reference, kept for history)

- **BLOB(.knowledge) - historical pattern:** a11y-fixer, create-stack, kanam-forge,
  kanam-mind, kanam-solitaires, kanam-story, portfolio-strategy, quedamos, soporteml-v3,
  soporteml, ultimo-turno. (Under the current model the project repo tracks its own
  `.knowledge/`; these predate that.)
- **GITLINK (resolved 2026-09-02):** accessible-ui, ai-developer-stack, create-with-ai,
  soporteml-v4 - were gitlinks in the workspace index; converted to plain embedded repos.
- **REPO-PROPIO/other:** kanam-skills (standalone skills repo on GitHub).

## Findings to respect

- Accessible-ui and create-with-ai: archived, do not touch.
- SOPORTEML (v3/v4): closed decision (excluded from public portfolio), do not touch.
- ai-developer-stack: `.knowledge` is a broken symlink in its GitHub repo. Repair needs
  explicit user go-ahead.
