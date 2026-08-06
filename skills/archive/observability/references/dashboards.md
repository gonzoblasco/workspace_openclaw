# Dashboards — Referencia

## Dashboards Mínimos Recomendados

| Dashboard | Contenido | Audiencia |
|---|---|---|
| **Producto** | Uso, conversión, errores de usuario, features más usadas | Producto / PM |
| **Backend** | Latencia, throughput, error rate, recursos | Backend / Infra |
| **Frontend** | Core Web Vitals, JS errors, bundle size, carga | Frontend |
| **Infraestructura** | CPU, RAM, disco, red, DB, cache | Infra / SRE |
| **AI** | Tokens, costos, latencia de LLM, reintentos, halluncination rate | AI / ML |
| **Workflows** | Tiempo por workflow, tasa de éxito, cuellos de botella | Engineering |
| **Releases** | Frecuencia, tasa de fallo, MTTR, change failure rate | Engineering / Management |

## Principios

- Cada dashboard debe responder una pregunta concreta
- Si un dashboard no se usa en 30 días, eliminarlo
- Preferir 3 dashboards útiles a 10 dashboards ignorados
- Los dashboards deben tener contexto: qué significan los números, no solo los números

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Metrics](./metrics.md) — Métricas mínimas
- [Alerting](./alerting.md) — Clasificación de alertas
