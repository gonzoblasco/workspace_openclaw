# OWASP Top 10 Security Review — Review & Quality Reference

Checklist OWASP Top 10 (2021) para revisión de seguridad en code review.

## Quick Reference

| ID | Category | Key Check |
|----|----------|-----------|
| A01 | Broken Access Control | ¿Cada endpoint verifica identidad? ¿IDOR? |
| A02 | Cryptographic Failures | ¿Passwords hasheadas con bcrypt/argon2? ¿Secrets hardcodeados? |
| A03 | Injection | ¿SQL concatenado? ¿shell=True? ¿Template sin escapar? |
| A04 | Insecure Design | ¿Rate limiting? ¿Flujos críticos bypassables? |
| A05 | Security Misconfiguration | ¿DEBUG en prod? ¿Stack traces en errores? |
| A06 | Vulnerable Components | ¿CVEs de `npm audit`? |
| A07 | Authentication Failures | ¿JWT signature verificada? ¿Tokens revocables? |
| A08 | Integrity Failures | ¿pickle.loads deserializando datos no confiables? |
| A09 | Logging Failures | ¿Passwords en logs? ¿Logins fallidos registrados? |
| A10 | SSRF | ¿URLs de usuario filtradas contra IPs internas? |

## Review Process

1. **Definir scope** — archivos, módulos a revisar
2. **Full coverage** — revisar A01-A10 secuencialmente. **Cada item debe aparecer en el reporte** (marcar como pass si no hay findings)
3. **Clasificar riesgo:**
   - 🔴 **High:** Directamente explotable (RCE, SQLi, SSRF, plaintext passwords)
   - 🟡 **Medium:** Explotable bajo condiciones específicas
   - 🟢 **Low:** Defense-in-depth gap sin exploit directo
4. **Cada finding debe incluir fix code listo para usar**
5. **Output reporte** con findings ordenados por severidad

## Report Template

```markdown
# OWASP Top 10 Security Review Report

## Summary
- Scope: [files/modules]
- Risk: RED x | YELLOW x | GREEN x | PASS x

## Findings

### [Severity] [A0X] — [Title]
- **Location:** file:line
- **Description:**
- **Impact:**
- **Fix:** (code)

### PASS A0X — [Category] — No issues found

## Remediation Priority
1. [Most urgent]
```

## Related

- [SKILL.md](../../review-quality/SKILL.md) — Workflow principal
- [Security Audit](../security-audit.md) — Auditoría de seguridad
- [Code Review Checklist](../code-review-checklist.md) — Checklist de code review
