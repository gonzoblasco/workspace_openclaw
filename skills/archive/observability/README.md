# Engineering Observability

Observabilidad del sistema y del AI Engineering OS.

## ¿Para qué sirve?

Para **hacer observable** el estado del producto, la infraestructura y el AI Engineering OS. No corrige problemas, no optimiza. Responde "¿qué está ocurriendo?", "¿por qué ocurrió?" y "¿cómo lo sabemos?".

**Filosofía:** You can't improve what you can't observe.

## ¿Cuándo usarlo?

- Antes de optimizaciones
- Después de incidentes
- Antes de retrospectivas
- Después de releases
- Periódicamente (health checks)
- Cuando un workflow parece ineficiente

## ¿Cómo se usa?

### Workflow completo

1. **Instrumentation Audit** — verificar cobertura de observabilidad
2. **Metrics** — definir KPIs (ingeniería, calidad, performance, agentes)
3. **Logging** — logs estructurados, correlation IDs, sin datos sensibles
4. **Tracing** — seguir operación completa (usuario → frontend → API → LLM → DB)
5. **Alerting** — clasificar alertas, evitar alert fatigue
6. **Dashboard Review** — verificar dashboards existentes
7. **Trend Analysis** — comparar semana/mes/trimestre
8. **Recommendations** — generar acciones

### Scripts útiles

```bash
# Health check de endpoints
./scripts/health-check.sh --url https://tusitio.com

# Recolectar métricas del proyecto
./scripts/metrics-report.sh

# Verificar cobertura de dashboards
python3 scripts/dashboard-check.py
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/metrics.md` | Métricas mínimas: ingeniería, app, AI, calidad |
| `references/alerting.md` | Clasificación de alertas y reglas |
| `references/dashboards.md` | Dashboards mínimos recomendados |
| `references/logging-standards.md` | Formato de log estructurado, qué loguear y qué no |
| `references/tracing-guide.md` | OpenTelemetry: setup, custom spans, propagación |

## Skills relacionadas

- [Performance Optimization](../performance-optimization) — Para optimizar basado en métricas
- [Incident Response](../incident-response) — Para detectar y responder a incidentes
