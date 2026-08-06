# OpenSpec Guide — Product Discovery Reference

Guía para escribir especificaciones formales (OpenSpec).

## OpenSpec Structure

```markdown
# Feature: [Name]

## Context
- **Epic:** [epic name]
- **Priority:** P0/P1/P2
- **Complexity:** S/M/L/XL

## Problem
[What problem does this solve?]

## Solution
[High-level approach]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes
[Architecture, dependencies, risks]

## Design
[Links to designs, wireframes, mockups]

## Out of Scope
[What we're explicitly NOT doing]
```

## Delta vs As-Built

| Mode | When | Content |
|---|---|---|
| **Delta** | Project exists, adding features | Only the change, not the whole system |
| **As-Built** | New project | Full specification |

## Spec Review Checklist

- [ ] Problem clearly stated
- [ ] Acceptance criteria testable
- [ ] Edge cases considered
- [ ] Dependencies identified
- [ ] Risks documented
- [ ] Out of scope explicit

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Brainstorming](./brainstorming.md) — Técnicas de brainstorming
- [Market Analysis](./market-analysis.md) — Análisis de mercado
