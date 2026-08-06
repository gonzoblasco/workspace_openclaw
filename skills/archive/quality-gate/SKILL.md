---
name: "quality-gate"
description: "Quality gates paralelos: code quality + UX quality con sync point"
---

# quality-gate

## Descripción
Ejecuta quality gates en paralelo: @validator (code quality) y @tester (UX quality) simultáneamente, con un sync point que decide el siguiente paso según una decision matrix. 40% más rápido que ejecución secuencial.

## Gates

### Gate 1: @validator (Code Quality)
- TypeScript compila (tsc --noEmit)
- Tests unitarios pasan
- Linter pasa
- No hay issues de seguridad
- Todos los consumidores actualizados (para API changes)

### Gate 2: @tester (UX Quality)
- E2E tests pasan
- Screenshots en 3 viewports (mobile, tablet, desktop)
- WCAG 2.1 AA compliant
- Core Web Vitals OK (LCP, CLS, INP, FCP)
- Sin console errors

## Decision Matrix
| @validator | @tester | Action |
|------------|---------|--------|
| ✅ APPROVED | ✅ APPROVED | → @scribe |
| ✅ APPROVED | 🔴 BLOCKED | → @builder (fix UX concerns) |
| 🔴 BLOCKED | ✅ APPROVED | → @builder (fix code concerns) |
| 🔴 BLOCKED | 🔴 BLOCKED | → @builder (merged feedback) |

## Flow
```
@builder
    │
    ├────────────────────┐
    ▼                    ▼
@validator           @tester
(Code Quality)     (UX Quality)
    │                    │
    └────────┬───────────┘
             │
        SYNC POINT
             │
    ┌────────┴────────┐
    │                 │
BOTH APPROVED     ANY BLOCKED
    │                 │
    ▼                 ▼
@scribe          @builder (fix)
```

## Output
```markdown
## Quality Gate Results

### @validator (Code Quality)
- TypeScript: ✅ PASS
- Tests: ✅ PASS
- Lint: ✅ PASS
- Security: ✅ PASS

### @tester (UX Quality)
- E2E: ✅ PASS
- Screenshots: ✅ 3 viewports
- A11y: ✅ WCAG 2.1 AA
- Performance: ✅ All metrics within thresholds

### Verdict: ✅ APPROVED → @scribe
```

## Notas
- Sin dependencias externas
- Corre en paralelo para velocidad
- Decision matrix clara para cada combinación de resultados

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `review-quality/scripts/review-pr.sh` | Build, tests, lint, typecheck, y busqueda de `console.log`. Usar para @validator. |
| `review-quality/scripts/security-scan.sh` | Security scan del diff. Usar para @validator. |
| `accessibility-studio/scripts/a11y-audit.sh` | Auditoria WCAG. Usar para @tester. |
| `performance-optimization/scripts/lighthouse-check.sh` | Core Web Vitals. Usar para @tester. |
| `pre-deploy-qa/scripts/pre-deploy-check.sh` | Validacion post-merge pre-deploy. |
| `engineering-governance/scripts/test-skills.sh` | Si el gate modifica scripts de skill del workspace. |
