# Logging Standards — Observability Reference

Estándares para logging estructurado.

## Structured Log Format

```json
{
  "timestamp": "2026-07-23T22:00:00.000Z",
  "level": "info",
  "service": "api",
  "correlation_id": "req_abc123",
  "user_id": "usr_456",
  "message": "Order created successfully",
  "metadata": {
    "order_id": "ord_789",
    "amount": 29.99,
    "currency": "USD"
  }
}
```

## Log Levels

| Level | Usage | Example |
|---|---|---|
| **debug** | Development only, verbose | "Processing item 42 of 100" |
| **info** | Normal operations | "Order created", "User logged in" |
| **warn** | Unexpected but handled | "Rate limit approaching", "Retry attempt 2" |
| **error** | Operation failed | "Database connection failed", "Payment declined" |
| **fatal** | Service cannot continue | "Out of memory", "Config validation failed" |

## What to Log

### Always Log
- Request start/end (with duration)
- Errors and exceptions
- Authentication events
- Authorization failures
- Data mutations (create, update, delete)
- External API calls (with duration)
- Rate limiting events

### Never Log
- Passwords, tokens, secrets
- PII (email, phone, address)
- Credit card numbers
- Full request/response bodies (unless sanitized)
- Internal IPs in production logs

## Correlation IDs

```typescript
// Generate at request entry point
const correlationId = crypto.randomUUID();

// Pass through all services
// Include in all log entries
// Include in error responses
```

## Logging Libraries

```bash
# Node.js
npm install pino

# Python
pip install structlog
```

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Metrics](../references/metrics.md) — Métricas mínimas
- [Alerting](../references/alerting.md) — Clasificación de alertas
