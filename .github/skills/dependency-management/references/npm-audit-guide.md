# npm Audit Guide — Dependency Management Reference

Cómo interpretar auditorías de seguridad de dependencias.

## npm Audit

```bash
# Basic audit
npm audit

# Audit with JSON output
npm audit --json

# Audit only production dependencies
npm audit --production

# Fix automatically (only patches)
npm audit fix

# Fix even minor upgrades
npm audit fix --force

# Dry run
npm audit fix --dry-run
```

## Understanding Audit Output

```
# critical — Exploitation is trivial, widespread impact
# high — Significant risk, but requires some conditions
# moderate — Limited impact or requires specific conditions
# low — Minimal impact, unlikely to be exploited

# Example:
# ┌───────────────┬──────────────────────────────────┐
# │ Critical      │ Prototype Pollution in lodash     │
# │ High          │ XSS in serialize-javascript       │
# │ Moderate      │ DoS in minimist                   │
# │ Low           │ RegExp DoS in semver              │
# └───────────────┴──────────────────────────────────┘
```

## CVSS Scores

| Severity | CVSS Range | Action |
|---|---|---|
| None | 0.0 | No action |
| Low | 0.1-3.9 | Monitor |
| Medium | 4.0-6.9 | Plan update |
| High | 7.0-8.9 | Update ASAP |
| Critical | 9.0-10.0 | Immediate action |

## Snyk

```bash
# Install
npm install -g snyk

# Auth
snyk auth

# Test
snyk test

# Monitor (continuous)
snyk monitor

# Test with JSON
snyk test --json
```

## Dependabot (GitHub)

Configure in `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
    reviewers:
      - "gonzoblasco"
    ignore:
      - dependency-name: "typescript"
        versions: [">=6.0.0"]
```

## Vulnerability Response Protocol

1. **Critical/High:** Immediate PR, review within 24h
2. **Medium:** Include in next sprint
3. **Low:** Track in dependency backlog
4. **False positive:** Document and suppress

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Health Assessment](../references/health-assessment.md) — Evaluación de salud
- [Risk Analysis](../references/risk-analysis.md) — Análisis de riesgo
