# Dependency Management

Gestión de dependencias del proyecto.

## ¿Para qué sirve?

Para **mantener el ecosistema de dependencias saludable, seguro y sostenible**. Evalúa, actualiza y gobierna dependencias sin instalarlas automáticamente. Cada dependencia es un compromiso a largo plazo.

## ¿Cuándo usarlo?

- Cuando querés agregar una nueva librería
- Cuando llega el momento de actualizar dependencias
- Cuando querés revisar vulnerabilidades
- Antes de una release importante
- Para auditorías periódicas

## ¿Cómo se usa?

### Workflow completo

1. **Inventory** — construir inventario de dependencias con versión, uso, tipo, tamaño
2. **Health Assessment** — evaluar salud: 🟢 Healthy / 🟡 Watch / 🔴 Risk
3. **Risk Analysis** — calcular nivel de riesgo (bajo/medio/alto)
4. **Update Strategy** — clasificar actualizaciones (patch/minor/major)
5. **Dependency Review** — antes de agregar algo nuevo, responder 7 preguntas
6. **Compatibility Check** — framework, Node, TS, bundler, testing, CI/CD
7. **Migration Planning** — si hay actualización importante, generar plan
8. **Knowledge Capture** — actualizar CHANGELOG, ADRs, README

### Scripts útiles

```bash
# Generar reporte completo
./scripts/dependency-report.sh

# Ver qué está outdated con clasificación
./scripts/check-outdated.sh --risk high

# Comparar dependencias entre dos commits
./scripts/audit-compare.sh <commit-a> <commit-b>
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/health-assessment.md` | Criterios de salud: releases, mantenimiento, contributors |
| `references/risk-analysis.md` | Factores de riesgo y matriz de decisión |
| `references/npm-audit-guide.md` | Cómo interpretar npm audit, CVSS, Snyk, Dependabot |
| `references/migration-patterns.md` | Codemods, dual publish, breaking change detection, rollback |

## Skills relacionadas

- [Release Management](../release-management) — Para coordinar actualizaciones en releases
- [Task Execution](../task-execution) — Para implementar actualizaciones
