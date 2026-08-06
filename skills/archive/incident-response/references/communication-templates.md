# Communication Templates — Incident Response Reference

Templates de comunicación durante y después de incidentes.

## Incident Acknowledgment

```
🔴 INCIDENT DETECTED
Severity: SEV-[1-4]
Time: [timestamp]
Service: [service name]
Impact: [what's affected]
Status: Investigating
Handler: [name]
```

## Status Update

```
🟡 INCIDENT UPDATE
Time: [timestamp]
Service: [service name]
Status: [Investigating / Containment / Resolution / Monitoring]
Progress: [what's been done]
Next step: [what's next]
ETA: [if known]
```

## Resolution

```
🟢 INCIDENT RESOLVED
Time: [timestamp]
Service: [service name]
Duration: [total time]
Root cause: [brief]
Action: [rollback / fix / scale]
Monitoring: [until when]
Postmortem: [link when ready]
```

## Postmortem Summary

```
📋 POSTMORTEM: [incident title]
Date: [date]
Severity: SEV-[1-4]
Duration: [time]
Impact: [users affected, data lost, $ cost]

Root Cause: [1-2 sentences]

Key Lessons:
- [lesson 1]
- [lesson 2]

Actions:
- [ ] [action 1] — owner, deadline
- [ ] [action 2] — owner, deadline
```

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Severity](../references/severity.md) — Clasificación de severidad
- [Runbooks](./runbooks.md) — Runbooks para incidentes comunes
