# Gateway Manager — Skill

## Scope & Capabilities
- Service discovery, API routing, and gateway configuration
- Protocol translation (HTTP ↔ gRPC ↔ WebSocket)
- Load balancing, rate limiting, and circuit breaker management
- Infrastructure orchestration and deployment coordination

## Key Principles
- **Abstraction over detail** — gateways should hide complexity, not amplify it.
- **Resilience by design** — graceful degradation, fallbacks, and self-healing.
- **Observability first** — every gateway must be fully traceable and measurable.

## Boundary Constraints
- Do not manage application business logic; gateways are infrastructure only.
- Keep gateway configs declarative and version-controlled.

## Sub-skills / Related Skills
- `gateway-config` (merged)
- `gateway-restart-helper` (merged)
