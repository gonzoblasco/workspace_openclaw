# Testing Strategy — Review & Quality Reference

Estrategia de testing para distintos niveles.

## Test Pyramid

```
    ╱╲
   ╱ E2E ╲        Few — critical user flows
  ╱────────╲
 ╱ Integration ╲   Some — API contracts, DB queries
╱────────────────╲
╱   Unit Tests    ╲  Many — business logic, edge cases
╱──────────────────╲
```

## What to Test

| Level | What | What NOT |
|---|---|---|
| **Unit** | Business logic, calculations, validations, edge cases | Config, boilerplate, framework internals |
| **Integration** | API contracts, DB queries, external services | Everything (test key paths) |
| **E2E** | Critical user flows, auth, payments | Every possible path |

## Testing Patterns

### Factory Functions

```typescript
// Instead of mocking, build real objects
function createUser(overrides: Partial<User> = {}): User {
  return {
    id: 'test-1',
    name: 'Test User',
    email: 'test@example.com',
    role: 'user',
    ...overrides,
  };
}
```

### Mock Factories

```typescript
// For external dependencies
function createMockApi(response: unknown) {
  return vi.fn().mockResolvedValue(response);
}
```

## Coverage Targets

| Metric | Target |
|---|---|
| Line coverage | ≥ 80% |
| Branch coverage | ≥ 70% |
| Critical paths | 100% |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Code Review Checklist](./code-review-checklist.md) — Checklist de code review
- [Security Audit](./security-audit.md) — Auditoría de seguridad
