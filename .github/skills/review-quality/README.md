# Review & Quality

Revisión pre-merge, testing y auditoría.

## ¿Para qué sirve?

Para **revisar calidad antes de mergear** un PR o cerrar un ciclo. Incluye estrategia de testing, code review, auditoría de seguridad (OWASP Top 10) y validación pre-deploy opcional.

## ¿Cuándo usarlo?

- Antes de mergear un PR
- Para auditar seguridad de un cambio
- Para verificar que un cambio cumple con la spec
- Para validación pre-deploy post-merge

## ¿Cómo se usa?

### Workflow completo

1. **Estrategia de Testing** — TDD, unit, integration, E2E, cobertura
2. **Análisis de diff** — cambios, archivos tocados, impacto
3. **Linter cognitivo** — convenciones, naming, estructura, tests
4. **Auditoría de seguridad** — multi-tenant, auth, secrets, RLS, OWASP
5. **Revisión de producto** — ¿cumple con la spec?
6. **Validación Pre-Deploy** — build, rutas, SEO, API, performance
7. **Reporte** — hallazgos, bloqueantes, sugerencias
8. **Gate** — bloquea cierre si hay hallazgos críticos

### Scripts útiles

```bash
# Review automático de PR
./scripts/review-pr.sh

# Security scan de cambios staged
./scripts/security-scan.sh --diff
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/code-review-checklist.md` | Checklist: structural, code quality, types, testing, security, performance, a11y |
| `references/security-audit.md` | Multi-tenant, auth, secrets, data protection, API security |
| `references/testing-strategy.md` | Test pyramid, qué testear y qué no, factory functions, coverage |
| `references/owasp-top-10.md` | Checklist OWASP 2021 con risk classification y report template |

## Skills relacionadas

- [Task Execution](../task-execution) — Para implementar fixes post-review
- [Pre-Deploy QA](../pre-deploy-qa) — Para validación post-merge pre-deploy
