# Plan Maestro - OpenClaw AI in Production (Ken Huang)

> **Objetivo:** preparación para puesto AI-Native en OpenSistemas (perfil: harness engineering + context engineering + arquitectura de agentes en producción).
> **Fuente:** libro "OpenClaw AI in Production" (Ken Huang, Packt, 422 pag, junio 2026). ISBN 978-1-805-77800-0 (referencia editorial).
> **Método:** learning-tracker modo preparación de entrevista. Dos pasadas (mapa → dominio).
> **Ventaja diferencial:** corremos OpenClaw real - cada concepto se valida contra nuestro workspace en vivo, no solo contra el repo.

## Filosofía del curso

- No es "aprender OpenClaw" desde cero: es **formalizar el vocabulario de arquitectura** de un sistema que ya operamos a diario (gateway-centric, agentes aislados, memoria persistente, subagentes, policy en AGENTS.md).
- El valor en la entrevista: poder decir "operé esto en producción y entiendo la teoría que lo explica" - perfil AI-Native real, no teórico.
- Cada capítulo cierra con Implementation checklist + Hands-on project. Los hands-on se hacen de verdad contra nuestro Gateway.

## Estructura de niveles

```
Parte 1 - Fundamentos de Producción
├── Nivel 1 - Arquitectura del Gateway (Cap 1)
│   ├── Topic: Gateway como control plane (hub-and-spoke)
│   ├── Topic: Channel adapters como spokes desacoplados
│   ├── Topic: PluginRegistry (extensión sin tocar core)
│   ├── Topic: Routing de 7 tiers (agent-to-agent)
│   ├── Topic: Horizontal scaling topology
│   └── Topic: Token Exchange en el boundary
├── Nivel 2 - Request Traversal (Cap 2)
│   ├── Topic: Pipeline de 6 fases
│   ├── Topic: Context assembly + dedupe cache
│   ├── Topic: Tool execution + streaming + idempotency
│   ├── Topic: Access control gates + DM pairing
│   └── Topic: Retry con exponential backoff
├── Nivel 3 - Cascading Failures (Cap 3)
│   ├── Topic: Anatomía del cascade failure
│   ├── Topic: Bulkhead pattern
│   ├── Topic: Graceful degradation ladder
│   ├── Topic: Cross-layer error signaling
│   └── Topic: Sandboxing (Docker/network/fs/syscall)
├── Nivel 4 - Identity & Encryption (Cap 4) [CRITICO]
│   ├── Topic: Zero-trust identity model
│   ├── Topic: mTLS + cert rotation
│   ├── Topic: Token Exchange + credential store
│   ├── Topic: SOUL.md/AGENTS.md integrity signing
│   ├── Topic: Prompt injection como ataque de identidad
│   └── Topic: Lockout / challenge-response fallback
├── Nivel 5 - Policy-Based Access Control (Cap 5) [CRITICO]
│   ├── Topic: 7-layer policy precedence stack
│   ├── Topic: DM pairing (human-in-the-loop)
│   ├── Topic: Allowlist + glob patterns
│   ├── Topic: Per-session sandboxing
│   ├── Topic: Tool policy narrowing + owner-only
│   ├── Topic: Canvas/A2UI access control
│   └── Topic: Fail-closed defaults

Parte 2 - Runtime State, Hooks, Observabilidad
├── Nivel 6 - State Management distribuido (Cap 6)
│   ├── Topic: Append-only event log
│   ├── Topic: Compaction + memory flush
│   ├── Topic: Sticky routing + CRDT-friendly state
│   ├── Topic: SQLite-vec + BM25 hybrid search
│   ├── Topic: Session ID encoding seguro
│   └── Topic: Retry/fallback (crash reload)
├── Nivel 7 - Cross-Cutting Concerns (Cap 7)
│   ├── Topic: Hook system + lifecycle interception
│   ├── Topic: Sidecar pattern + rate limiting hook
│   ├── Topic: Billing/cost attribution
│   ├── Topic: Security hooks como interceptores
│   └── Topic: Timeouts y failure modes de hooks
├── Nivel 8 - Observability (Cap 8)
│   ├── Topic: 3 pillars extendidos para agentes
│   ├── Topic: Distributed tracing + semantic
│   ├── Topic: Cost dashboards + memory health
│   ├── Topic: Hook como telemetry injection point
│   ├── Topic: PII redaction
│   └── Topic: Async telemetry pipelines

Parte 3 - Self-Correction, Scale, Federated
├── Nivel 9 - Self-Correcting Stack (Cap 9)
│   ├── Topic: Circuit breaker (model providers)
│   ├── Topic: Health hooks + auto-remediation
│   ├── Topic: Watchdog + session self-repair
│   ├── Topic: Auto compaction + privilege-scoped
│   └── Topic: Retry/fallback patterns
├── Nivel 10 - API Gateway Patterns (Cap 10)
│   ├── Topic: Gateway como API gateway domain-specific
│   ├── Topic: Reverse proxy (Caddy/Nginx/TLS)
│   ├── Topic: Rate limiting tiers
│   ├── Topic: Multi-agent routing
│   ├── Topic: Webhooks + versioning
│   └── Topic: Auth federation + idempotency keys
├── Nivel 11 - Resilience Testing (Cap 11)
│   ├── Topic: Chaos engineering para agentes
│   ├── Topic: Fault injection targets
│   ├── Topic: Hook-based fault injectors
│   ├── Topic: Canary deployments
│   └── Topic: Runbook-driven recovery
├── Nivel 12 - High-Throughput / Low-Latency (Cap 12)
│   ├── Topic: Wake coalescing
│   ├── Topic: Backpressure + lane separation
│   ├── Topic: Context budget optimization
│   ├── Topic: Concurrency patterns (fan-out/in)
│   ├── Topic: Embedding cache
│   ├── Topic: Session affinity + consistent hashing
│   └── Topic: Rate limiting + load-shedding
└── Nivel 13 - Ecosystem / Decentralized (Cap 13)
    ├── Topic: Federated gateway topology
    ├── Topic: Edge agent deployments
    ├── Topic: Decentralized identity (DID)
    ├── Topic: Trust mesh + reputation routing
    ├── Topic: Agent marketplace
    └── Topic: Data sovereignty + eventual consistency
```

## Niveles críticos (core del objetivo OpenSistemas)

- **Nivel 4 (Identity & Encryption)** y **Nivel 5 (PBAC)**: seguridad de agentes = diferenciador AI-Native.
- **Nivel 8 (Observability)** y **Nivel 9 (Self-correction)**: produccion real, resiliencia.
- **Nivel 1 (Gateway)**: fundamento de todo.

## Recursos externos

- Libro (fuente principal) + repo OpenClaw live (para validar snippets vs pinned commit `E525957b4f99acfb9f57317f62f333760c48a92b`).
- Nuestro workspace real (la ventaja: podemos tocar la tecnologia).

## Gamificación

- XP por topic (dominio, no mapeo).
- Badge por nivel.
- Streak de práctica.
- Jefe final: mock interview completa estilo OpenSistemas.

## Tabla de progreso (resumen)

| Nivel | Estado |
|-------|--------|
| 1 - Arquitectura Gateway | 🚧 En estudio (Cap 1 mapeado) |
| 2 - Request Traversal | ⏳ |
| 3 - Cascading Failures | ⏳ |
| 4 - Identity & Encryption | ⏳ |
| 5 - PBAC | ⏳ |
| 6 - State Management | ⏳ |
| 7 - Cross-Cutting | ⏳ |
| 8 - Observability | ⏳ |
| 9 - Self-Correcting | ⏳ |
| 10 - API Gateway | ⏳ |
| 11 - Resilience Testing | ⏳ |
| 12 - High-Throughput | ⏳ |
| 13 - Ecosystem | ⏳ |
