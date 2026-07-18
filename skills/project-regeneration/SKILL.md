---
name: "project-regeneration"
description: "Clean rebuild when legacy debt > refactor value. Pipeline: ADR → Scaffold → Impl → Test → Publish"
---

# Project Regeneration Skill

## Purpose

Rebuilds projects from scratch when technical debt exceeds incremental refactor value. Strategic decision pattern for modernization.

## Trigger Conditions

All must be true:
- [ ] >6 commits with decisions never implemented
- [ ] Stack outdated (e.g., React 18 → 19)
- [ ] Build system causes issues (Webpack vs Vite)
- [ ] Stakeholder agrees to start fresh
- [ ] No active users on existing version

## Execution Pipeline

```
[Start] → ADR-001 Regeneration Decision → Scaffold Selection → Component Impl → Test Suite → Storybook Stories → npm Publish
```

## Stack Defaults

| Category | Choice | Rationale |
|----------|--------|-----------|
| Framework | React 19.x | Latest FC model |
| TS | ^5.6+ | Best generics |
| Build | Vite 6.x | Zero-config, fast |
| Tests | Vitest 2.x | Similar to JSDT |
| Docs | Storybook 10 + @storybook/addon-docs | Auto-generate from source |

## Example Case Study

**accessible-ui regeneration**:
- Legacy: 12 commits, Webpack + React 18 + axe-core standalone
- Regenerated: Vite 6 + React 19 + TS + Vitest + Storybook
- Result: Zero debt, fast builds, full WAI-APG compliance

## Constraints

- Cannot apply with active users needing feature parity
- Require ADR-001 approval before deletion
- Document in memory after successful regeneration
