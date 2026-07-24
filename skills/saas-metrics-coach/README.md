# SaaS Metrics Coach

Asesor financiero de salud SaaS.

## ¿Para qué sirve?

Para **evaluar la salud financiera de tu SaaS**. Tomás números crudos de negocio y te devuelve métricas clave calculadas (ARR, MRR, churn, LTV, CAC, NRR), benchmarkeadas contra estándares de industria, con recomendaciones accionables priorizadas.

**Filosofía:** If a metric is bad, say it's bad. Contexto cambia benchmarks.

## ¿Cuándo usarlo?

- Cuando querés saber cómo está tu SaaS
- Cuando compartís números de revenue o customers
- Cuando preguntás por métricas específicas (churn, LTV, CAC)
- Cuando querés proyectar escenarios de crecimiento

## ¿Cómo se usa?

### Conversacional

> "Tengo $50k MRR, 100 customers, pierdo 5 por mes. ¿Cómo estoy?"

Te calcula todo, benchmarkea, y te dice las 2-3 prioridades.

### Scripts

```bash
# Calcular métricas core
python3 scripts/metrics_calculator.py --mrr 50000 --customers 100 --churned 5

# Quick Ratio (eficiencia de crecimiento)
python3 scripts/quick_ratio_calculator.py --new-mrr 10000 --expansion 2000 --churned 3000 --contraction 500

# Proyectar 12 meses
python3 scripts/unit_economics_simulator.py --mrr 50000 --growth 10 --churn 3 --cac 2000
```

### Output

```
# SaaS Health Report

| Metric | Your Value | Benchmark | Status |
|--------|------------|-----------|--------|
| ARR | $600,000 | | |
| Monthly Churn | 5% | 5-7% (SMB) | 🟡 WATCH |
| LTV:CAC | 4.67:1 | > 3:1 | 🟢 HEALTHY |

## Priority Issues
### 1. Churn Rate
What: Perdiendo 5% de customers por mes
Why: Cada punto de churn cuesta $6k ARR
Fix: Implementar onboarding flow, check-in a los 30 días
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/formulas.md` | Fórmulas con ejemplos, benchmarks por segmento y stage |

## Skills relacionadas

- [Product Discovery](../product-discovery) — Para definir métricas de éxito de producto
- [Observability](../observability) — Para monitorear métricas del sistema
