# Branch & PR Conventions — Task Execution Reference

Convenciones para branches y PRs.

## Branch Naming

```bash
# Feature
git checkout -b feat/add-user-profile

# Fix
git checkout -b fix/login-error-401

# Refactor
git checkout -b refactor/extract-auth-middleware

# Task tracking
git checkout -b task/E1-T03-implement-auth-flow
```

## Commit Messages

```text
feat(scope): description

fix(scope): description

refactor(scope): description

test(scope): description

docs(scope): description

chore(scope): description
```

## PR Template

```markdown
## Description

[What does this PR do?]

## Related

Closes #[issue]
Related to #[issue]

## Changes

- [Change 1]
- [Change 2]

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing done

## Checklist

- [ ] Build passes
- [ ] Type check passes
- [ ] Lint passes
- [ ] Tests pass
- [ ] No console.log/debugger
- [ ] No unresolved TODOs
```

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Task Planning](./task-planning.md) — Planificación de tareas
