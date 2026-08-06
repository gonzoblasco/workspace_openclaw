# Git Bisect Guide — Debug Investigation Reference

Guía práctica para usar `git bisect` en la investigación de bugs.

## Quick Start

```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark a known-good commit
git bisect good <commit-hash>

# Git will checkout a commit halfway. Test it:
npm run test  # or your reproduction script

# Mark:
git bisect good   # if bug is not present
git bisect bad    # if bug is present

# Repeat until Git identifies the first bad commit
# Output: <hash> is the first bad commit
```

## Automation

```bash
# If you have a reproduction script that exits 0 for good, non-0 for bad:
git bisect run npm run test -- --run

# Or a custom script:
git bisect run ./scripts/reproduce.sh
```

## Common Patterns

### Finding a regression

```bash
git bisect start
git bisect bad HEAD
git bisect good <tag-or-hash-before-regression>
git bisect run npm run test:e2e
```

### Finding when a file was introduced

```bash
git log --diff-filter=A --follow -- path/to/file
# Then bisect on the commit range
```

### Finding when behavior changed

```bash
git bisect start
git bisect bad HEAD
git bisect good <last-known-working-commit>
git bisect run bash -c "node scripts/check-behavior.js"
```

## Tips

- **Start with a wide range** (last known good → current) to avoid false positives
- **Use a script** for `git bisect run` — it's faster than manual
- **Skip commits that don't build:** `git bisect skip`
- **Visualize:** `git bisect visualize` shows the remaining range
- **Abort if stuck:** `git bisect reset`

## Script Template

```bash
#!/usr/bin/env bash
# reproduce.sh — Exit 0 if bug is NOT present, non-0 if bug IS present
set -euo pipefail

# 1. Install dependencies
npm ci 2>/dev/null

# 2. Build
npm run build 2>/dev/null

# 3. Run reproduction
node scripts/reproduce-bug.js
```

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Techniques](../references/techniques.md) — Técnicas de debugging
- [Experiments](../references/experiments.md) — Diseño de experimentos
