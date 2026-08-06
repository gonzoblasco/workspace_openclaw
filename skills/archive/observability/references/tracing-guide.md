# Tracing Guide — Observability Reference

Guía para instrumentar tracing distribuido.

## OpenTelemetry Setup

```bash
# Node.js
npm install @opentelemetry/api @opentelemetry/sdk-node
npm install @opentelemetry/instrumentation-http
npm install @opentelemetry/instrumentation-express
npm install @opentelemetry/exporter-otlp-grpc
```

## Basic Instrumentation

```typescript
// tracing.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter(),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

## Custom Spans

```typescript
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('my-service');

async function processOrder(orderId: string) {
  const span = tracer.startSpan('process-order', {
    attributes: { 'order.id': orderId },
  });

  try {
    // ... business logic
    span.setStatus({ code: SpanStatusCode.OK });
  } catch (error) {
    span.setStatus({
      code: SpanStatusCode.ERROR,
      message: error.message,
    });
    throw error;
  } finally {
    span.end();
  }
}
```

## Trace Context Propagation

```typescript
// HTTP headers for trace propagation
// traceparent: 00-<trace-id>-<span-id>-01
// tracestate: <vendor-specific-data>

// Automatic with OpenTelemetry instrumentation
// Manual for custom protocols
```

## Key Spans to Instrument

- HTTP request → response
- Database queries
- External API calls
- LLM calls
- File I/O
- Background jobs
- Authentication flows

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Metrics](../references/metrics.md) — Métricas mínimas
- [Logging Standards](./logging-standards.md) — Estándares de logging
