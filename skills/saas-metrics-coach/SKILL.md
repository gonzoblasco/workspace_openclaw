---
name: "saas-metrics-coach"
metadata:
  category: "Business"
  tags:
    - saas
    - metricas
    - finanzas
    - arr
    - mrr
    - churn
description: "Asesor financiero de salud SaaS: calcular ARR, MRR, churn, LTV, CAC, NRR y benchmarkear contra estándares de industria."
user-invocable: false
---

# Workflow: SaaS Metrics Coach

## Propósito

Tomar números crudos de negocio, calcular métricas clave de salud SaaS, benchmarkear contra estándares de industria y dar recomendaciones accionables priorizadas.

## Filosofía

> If a metric is bad, say it's bad.

Contexto cambia benchmarks. 5% churn es catastrófico para Enterprise SaaS pero normal para SMB/PLG.

---

# Cuándo usarlo

- Compartir números de revenue o customers
- Preguntar por ARR, MRR, churn, LTV, CAC, NRR
- Evaluar salud financiera del SaaS
- Planificar escenarios de crecimiento

---

# Fases

## 1. Collect Inputs

Si no están dados, pedir en un solo grupo:
- Revenue: current MRR, MRR last month, expansion MRR, churned MRR
- Customers: total active, new this month, churned this month
- Costs: sales and marketing spend, gross margin %

Trabajar con datos parciales. Ser explícito sobre lo que falta.

## 2. Calculate Metrics

Siempre computar: ARR, MRR growth %, monthly churn rate, CAC, LTV, LTV:CAC ratio, CAC payback period, NRR.

```bash
python3 scripts/metrics_calculator.py --mrr 50000 --customers 100 --churned 5
```

## 3. Benchmark

Para cada métrica mostrar:
- Valor calculado
- Benchmark range para el segmento y stage
- Status: 🟢 HEALTHY / 🟡 WATCH / 🔴 CRITICAL

## 4. Prioritize & Recommend

Identificar top 2-3 métricas en WATCH o CRITICAL. Para cada una:
- Qué está pasando (una oración)
- Por qué importa
- 2-3 acciones específicas para este mes

---

# Outputs

```
# SaaS Health Report — [Month Year]

## Metrics at a Glance
| Metric | Your Value | Benchmark | Status |

## Overall Picture
[2-3 sentences summary]

## Priority Issues
### 1. [Metric]
What: ...
Why: ...
Fix: ...

## What is Working
[1-2 strengths]

## 90-Day Focus
[Single metric + numeric target]
```

---

# Principios

- Ser directo. Si una métrica está mal, decirlo.
- Explicar cada métrica en una oración antes del número.
- Máximo 3 issues prioritarios. Más de 3 paraliza.
- Contexto cambia benchmarks. Confirmar target market antes de scorear.

---

# Related Skills

- [Product Discovery](../product-discovery): Para definir métricas de éxito de producto
- [Observability](../observability): Para monitorear métricas del sistema
