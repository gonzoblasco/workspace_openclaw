# Alerting — Referencia

## Clasificación de Alertas

| Nivel | Descripción | Acción |
|---|---|---|
| **Critical** | Servicio caído, pérdida de datos, seguridad comprometida | Respuesta inmediata, 24/7 |
| **Major** | Degradación severa, funcionalidad crítica afectada | Respuesta en horas hábiles |
| **Minor** | Degradación leve, funcionalidad no crítica afectada | Próximo sprint |
| **Informational** | Tendencia, umbral próximo, dato relevante | Monitoreo pasivo |

## Reglas

- Toda alerta crítica debe tener un runbook asociado
- Evitar alert fatigue: si una alerta no genera acción, eliminarla o degradarla
- Las alertas deben ser accionables: si no se puede responder, no es una alerta
- Documentar umbrales y justificación de cada alerta

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Metrics](./metrics.md) — Métricas mínimas
