# Code Review Checklist — Review & Quality Reference

Checklist detallada para code review.

## Structural

- [ ] PR is small and focused (one concern per PR)
- [ ] Branch name follows convention: `fix/`, `feat/`, `refactor/`
- [ ] Commits are atomic and well-described
- [ ] No unrelated changes

## Code Quality

- [ ] No dead code or commented code
- [ ] No console.log/debugger
- [ ] Functions are focused (single responsibility)
- [ ] No magic numbers/strings (use constants)
- [ ] Error handling is explicit
- [ ] Edge cases are handled

## Types

- [ ] No `any` types
- [ ] Exported types/interfaces are documented
- [ ] Generic types are constrained
- [ ] Type inference is used where appropriate

## Testing

- [ ] Tests exist for new code
- [ ] Tests cover edge cases
- [ ] Tests are readable and maintainable
- [ ] No tests that test implementation details
- [ ] Existing tests still pass

## Security

- [ ] No secrets in code
- [ ] Input validation exists
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (escaping, CSP)
- [ ] Auth checks in place
- [ ] Rate limiting considered

## Performance

- [ ] No N+1 queries
- [ ] No unnecessary re-renders
- [ ] Bundle size impact considered
- [ ] Lazy loading where appropriate

## Accessibility

- [ ] Semantic HTML used
- [ ] Keyboard navigation works
- [ ] Focus management correct
- [ ] ARIA attributes correct
- [ ] Color contrast sufficient

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Security Audit](./security-audit.md) — Auditoría de seguridad
- [Testing Strategy](./testing-strategy.md) — Estrategia de testing
