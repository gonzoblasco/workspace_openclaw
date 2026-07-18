---
name: "workspace-scaffold"
description: "Generate OpenClaw projects with modern React/Vite stack. Scaffold defaults: React 19 + Vitest + Storybook + TypeScript, npm package scoping support."
---

# Workspace Scaffold Skill

## Purpose

Generates complete OpenClaw project scaffolds with modern tooling defaults (React 19/Vite/Vitest/Storybook). Includes package.json configuration and docs framework structure.

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--stack` | react | Target framework: {react, vue, svelte} |
| `--test-runner` | vitest | Test runner: {vitest, jest} default: vitest |
| `--docs-tool` | storybook | Docs tool: {storybook, marko, docgen} default: storybook |
| `--package-scope` | @username/slug | npm scope for packages (e.g., @gonzoblasco/accessible-ui) |

## Output Files

### docs/ (mandatory)
- `BRIEF.md` — Product definition with stakeholder analysis
- `EVALUATION.md` — Competitor comparison matrix  
- `DEFINITION.md` — Technical API contracts and specs
- `ROADMAP.md` — 6-phase timeline from v1.0 to v2.0
- `STATUS.md` — Current project state tracking
- `HANDOFF.md` — This handoff file for next session

### code/ (mandatory)
- `.gitignore` — Standard Node patterns (node_modules, dist, .DS_Store)
- `.github/workflows/ci.yml` — Test + lint pipeline configuration
- `.github/workflows/release.yml` — Semantic versioning release workflow
- `.github/workflows/docs.yml` — Storybook deployment to public repo
- `tsconfig.json` — Modern TS config with ES2022 target, module: "ESNext"
- `tsconfig.app.json` — App build specific configuration  
- `tsconfig.node.json` — Node build specific configuration
- `package.json` — Complete package with deps and scripts

## Related Skills

- `adr-framework` — Create decision documents during scaffold generation
- `project-regeneration` — Regenerate existing projects when debt exists

## Example Use Case

**accessible-ui regeneration**:
```bash
# Scaffold generated workspace structure with:
# - React 19 + TypeScript + Vite + Vitest stack
# - Storybook 10 integration with addon-docs
# - GitHub Actions CI/CD workflows (ci, release, docs)
# - Modern TS config with ES2022 target
```

## Constraints

- Must generate all required docs folder structure before component implementation
- Scaffold must include npm package.json with proper scope configuration  
- Always includes ADR framework documentation capability
