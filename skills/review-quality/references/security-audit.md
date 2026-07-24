# Security Audit — Review & Quality Reference

Checklist de auditoría de seguridad.

## Multi-Tenant

- [ ] RLS policies exist for all tables
- [ ] User isolation: users can't access other users' data
- [ ] Tenant isolation: tenants can't access other tenants' data
- [ ] Row-level security tested with multiple users
- [ ] No bypass of RLS in server-side code

## Authentication

- [ ] Session management is secure
- [ ] Token expiration is reasonable
- [ ] No hardcoded tokens
- [ ] Password requirements enforced
- [ ] MFA available (if applicable)
- [ ] Rate limiting on auth endpoints

## Secrets

- [ ] No secrets in source code
- [ ] No secrets in commit history
- [ ] Environment variables used for all secrets
- [ ] `.env.example` has no real values
- [ ] `.env` in `.gitignore`

## Data Protection

- [ ] PII is identified and protected
- [ ] Data encryption at rest
- [ ] Data encryption in transit (HTTPS)
- [ ] No sensitive data in logs
- [ ] No sensitive data in error messages
- [ ] Data retention policies documented

## API Security

- [ ] Input validation on all endpoints
- [ ] Output sanitization
- [ ] CORS configured correctly
- [ ] Rate limiting active
- [ ] Request size limits
- [ ] No stack traces in responses

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Code Review Checklist](./code-review-checklist.md) — Checklist de code review
- [Testing Strategy](./testing-strategy.md) — Estrategia de testing
