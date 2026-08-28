# Workspace double-git pattern (verified 2026-08-28)

Observed on live projects: create-stack, kanam-mind, a11y-fixer. The template `init-project.sh` differs from what active projects actually do.

## How active projects track

- Workspace tracks `.knowledge/` as loose blobs (mode `100644`), NOT as gitlink.
- The project folder's git repo (`.git`) coexists: workspace tracks `.knowledge/`, the project tracks its code.
- `.knowledge/` is NOT ignored in the project `.gitignore` (both workspace and project repo track it - double tracking).
- No `.gitmodules` in the workspace (no submodules).

Verify: `git ls-files --stage projects/a11y-fixer/` shows `100644 .../HANDOFF.md`, not `160000`.

## Contrast with init-project.sh template

The template generates a `.gitignore` that ignores `.knowledge/` and registers a submodule (`git submodule add`). This is NOT what active projects use.

## Promote a folder to double git (verified steps)

1. `git init && git branch -m main` in the project folder.
2. Create project `.gitignore` WITHOUT ignoring `.knowledge/`.
3. `gh repo create <owner>/<slug> --private --source=. --push`.
4. Workspace tracks `.knowledge/` as blob (NOT `git submodule add`, NO `.gitmodules`).
5. **Order is critical**: the `.knowledge/` must be tracked in the workspace. If the internal `.git` is created first and `.knowledge/` is untracked, the workspace sees an embedded repo and refuses to track its contents (even with `-f`). Once tracked, the internal `.git` does not interfere.

## Verified commands

```bash
# State of a submodule/gitlink
# Shows modified content inside a project
# Ver si una carpeta es gitlink (160000) o blob suelto (100644) en el workspace
git ls-files --stage projects/<slug>/

# Archive a repo on GitHub (read-only afterward)
# (repo becomes read-only - no more pushes)
gh repo archive <owner>/<repo> --yes

# Check archive state of a repo
gh repo view <owner>/<repo> --json isArchived

# Undo a mistakenly created submodule
git rm --cached -f projects/<slug>
git config --remove-section submodule.projects/<slug>
rm -f .gitmodules
```

## Audit classification (2026-08-28 reference)

- **BLOB(.knowledge) - correct pattern:** a11y-fixer, create-stack, kanam-forge, kanam-mind, kanam-solitaires, kanam-story, portfolio-strategy, quedamos, soporteml-v3, soporteml, ultimo-turno
- **GITLINK - no .knowledge as blob:** accessible-ui (archived), ai-developer-stack, create-with-ai (archived), soporteml-v4 (has .knowledge on disk but not tracked by workspace)
- **REPO-PROPIO/other:** kanam-skills (standalone skills repo on GitHub, no .knowledge needed), kanam-forge / kanam-mind (dirty changes = in-progress user work, do not touch)

## Findings to respect

- Accessible-ui and create-with-ai: archived, do not touch.
- SOPORTEML (v3/v4): closed decision (excluded from public portfolio), do not touch.
- ai-developer-stack: `.knowledge` is a broken symlink (target dir missing locally and on GitHub). Live agent-skills project. Repair needs explicit user go-ahead.
