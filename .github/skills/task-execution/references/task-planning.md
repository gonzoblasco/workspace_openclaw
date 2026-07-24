# Task Planning — Task Execution Reference

Guía para desglosar tareas en subtareas verificables.

## Task Breakdown Template

```markdown
# Task: [Title]

## Context
- **Epic:** E[N]
- **Task:** T[NN]
- **Priority:** P0/P1/P2
- **Complexity:** S/M/L/XL

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Plan

### Subtask 1: [Name] (~5 min)
**Verification:** [how to know it's done]
- [ ] Step 1
- [ ] Step 2

### Subtask 2: [Name] (~5 min)
**Verification:** [how to know it's done]
- [ ] Step 1
- [ ] Step 2
```

## Subtask Size Guidelines

| Size | Time | Max Subtasks |
|---|---|---|
| **S** | < 30 min | 3-5 |
| **M** | 30-60 min | 5-8 |
| **L** | 1-2 h | 8-10 |
| **XL** | > 2 h | Split into multiple tasks |

## Verification Examples

| Task | Verification |
|---|---|
| Add API endpoint | `curl` returns expected response |
| Fix bug | Reproduction script exits 0 |
| Add component | Storybook renders, tests pass |
| Refactor | Build + tests pass, same behavior |
| Add types | `tsc --noEmit` passes |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Branch Convention](./branch-convention.md) — Convención de branches
- [PR Template](./pr-template.md) — Template de PR
