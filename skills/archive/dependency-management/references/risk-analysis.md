# Risk Analysis de Dependencias — Referencia

## Factores de Riesgo

| Factor | Bajo | Medio | Alto |
|---|---|---|---|
| **Breaking changes** | Patch | Minor | Major |
| **CVEs conocidas** | 0 | 1-3 | 4+ o crítica |
| **Compatibilidad** | Misma major | Major anterior | Framework diferente |
| **Lock-in** | Fácil de reemplazar | Migración posible | Dependencia crítica sin alternativa |
| **Riesgo de abandono** | Equipo activo, funding | Equipo pequeño | Un solo mantenedor, sin funding |
| **Dependencia transitiva** | 0-5 | 5-20 | 20+ |

## Matriz de Decisión

| Riesgo | Impacto | Acción |
|---|---|---|
| Bajo | Bajo | Monitorear |
| Bajo | Alto | Evaluar alternativa |
| Medio | Bajo | Planificar migración |
| Medio | Alto | Migrar ASAP |
| Alto | Bajo | Buscar reemplazo |
| Alto | Alto | Migración urgente |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Health Assessment](./health-assessment.md) — Evaluación de salud
