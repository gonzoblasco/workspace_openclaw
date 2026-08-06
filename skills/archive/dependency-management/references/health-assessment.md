# Health Assessment de Dependencias — Referencia

## Criterios de Evaluación

| Criterio | 🟢 Healthy | 🟡 Watch | 🔴 Risk |
|---|---|---|---|
| **Último release** | < 6 meses | 6-12 meses | > 12 meses |
| **Mantenimiento activo** | Commits semanales | Commits mensuales | Sin actividad > 6 meses |
| **Contributors** | 10+ | 3-9 | 1-2 |
| **Issues abiertos** | < 50 | 50-200 | > 200 sin respuesta |
| **Tiempo de respuesta** | < 1 semana | 1-4 semanas | > 1 mes |
| **Frecuencia de releases** | Mensual o más | Trimestral | Anual o menos |
| **Deprecada** | No | No oficialmente | Sí, anunciada |

## Fuentes de Información

- GitHub: `Insights → Contributors`, `Issues`, `Pulse`
- npm: `npm view <package>`, `npm outdated`
- Snyk / Dependabot: vulnerabilidades conocidas
- Libraries.io: métricas de mantenimiento
- BundlePhobia: tamaño y dependencias transitivas

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Risk Analysis](./risk-analysis.md) — Análisis de riesgo
