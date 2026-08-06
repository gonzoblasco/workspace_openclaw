# Runbook Templates — Incident Response Reference

Runbooks para incidentes comunes.

## SEV-1 Runbook Template

```markdown
# Runbook: [Incident Type]

## Detection
- **Alert:** [alert name]
- **Symptoms:**
- **Severity:** SEV-1

## Immediate Actions
1. [ ] Acknowledge incident
2. [ ] Notify team
3. [ ] Assess impact

## Containment
1. [ ] Rollback if recent deploy
2. [ ] Disable feature flag
3. [ ] Scale resources
4. [ ] Block traffic if needed

## Investigation
1. [ ] Check logs
2. [ ] Check metrics
3. [ ] Check recent changes
4. [ ] Reproduce if possible

## Resolution
1. [ ] Apply fix
2. [ ] Verify service restored
3. [ ] Monitor for 15 min

## Post-Incident
1. [ ] Document timeline
2. [ ] Create postmortem
3. [ ] Update runbook
```

## Common Runbooks

### Database Degradation

1. Check connection pool: `SELECT * FROM pg_stat_activity`
2. Check slow queries: `SELECT * FROM pg_stat_activity WHERE state = 'active'`
3. Check locks: `SELECT * FROM pg_locks WHERE granted = false`
4. Scale if needed: connection pool size, read replicas
5. Kill long-running queries if critical

### API Latency Spike

1. Check recent deploys
2. Check database response time
3. Check external API dependencies
4. Check rate limiting
5. Check CDN / cache hit ratio
6. Scale horizontally if needed

### Memory Leak

1. Take heap snapshot
2. Compare with baseline
3. Identify growing objects
4. Rollback to last known good version
5. Fix in development, deploy fix

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Severity](../references/severity.md) — Clasificación de severidad
- [Postmortem Template](../references/postmortem-template.md) — Plantilla de postmortem
