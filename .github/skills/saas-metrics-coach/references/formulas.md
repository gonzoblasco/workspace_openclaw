# SaaS Formulas — SaaS Metrics Coach Reference

Fórmulas de métricas SaaS con ejemplos.

## Core Metrics

| Metric | Formula | Example |
|---|---|---|
| **ARR** | MRR × 12 | $50,000 × 12 = $600,000 |
| **MRR Growth %** | ((MRR this month - MRR last month) / MRR last month) × 100 | (($55k - $50k) / $50k) × 100 = 10% |
| **Monthly Churn Rate** | Churned customers / Total customers × 100 | 5 / 100 × 100 = 5% |
| **CAC** | Sales & Marketing spend / New customers | $15,000 / 10 = $1,500 |
| **LTV** | ARPA × Gross Margin % / Monthly Churn Rate | $500 × 0.7 / 0.05 = $7,000 |
| **LTV:CAC** | LTV / CAC | $7,000 / $1,500 = 4.67:1 |
| **CAC Payback** | CAC / (ARPA × Gross Margin %) | $1,500 / ($500 × 0.7) = 4.3 months |
| **NRR** | (Starting MRR + Expansion - Churned - Contraction) / Starting MRR × 100 | ($50k + $5k - $3k - $1k) / $50k × 100 = 102% |
| **Quick Ratio** | (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR) | ($10k + $2k) / ($3k + $500) = 3.43 |

## Benchmarks by Segment

| Metric | Enterprise | Mid-Market | SMB/PLG |
|---|---|---|---|
| Monthly Churn | < 2% | 2-5% | 5-7% |
| LTV:CAC | > 5:1 | > 3:1 | > 3:1 |
| CAC Payback | < 12 months | < 12 months | < 6 months |
| NRR | > 120% | > 110% | > 100% |
| Quick Ratio | > 4 | > 2 | > 2 |

## Benchmarks by Stage

| Metric | Early (<$1M ARR) | Growth ($1-10M) | Scale ($10M+) |
|---|---|---|---|
| MRR Growth | > 15% monthly | > 10% monthly | > 5% monthly |
| Gross Margin | > 60% | > 70% | > 75% |
| Churn | < 10% | < 5% | < 3% |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Scripts](../scripts/) — Calculadoras de métricas
