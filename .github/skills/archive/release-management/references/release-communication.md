# Release Communication — Release Management Reference

Templates de comunicación para releases.

## Release Notes Template

```markdown
# Release v[version] — [name]

**Date:** YYYY-MM-DD

## What's New

### ✨ Features
- [Feature 1]
- [Feature 2]

### 🐛 Bug Fixes
- [Fix 1]
- [Fix 2]

### ⚠️ Breaking Changes
- [Change 1] — Migration: [how to migrate]

## Installation

```bash
npm install package@latest
```

## Migration Guide

[If breaking changes, describe migration steps]

## Full Changelog

[Link to CHANGELOG.md]
```

## Rollback Plan Template

```markdown
## Rollback Plan: v[current] → v[previous]

### Trigger Conditions
- Error rate > 5%
- P95 latency > 2s
- Critical bug found

### Steps
1. `git revert <release-commit>`
2. `npm run build`
3. Deploy previous version
4. Verify health checks
5. Monitor for 15 min

### Verification
- [ ] Health endpoint returns 200
- [ ] Error rate back to baseline
- [ ] No active incidents
```

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Release Checklist](../references/checklist.md) — Checklist de release
- [Deployment Strategies](../references/strategies.md) — Estrategias de deploy
