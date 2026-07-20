---
name: "workflow-review-quality"
description: "Workflow de Review & Quality: revisión pre-merge y auditoría. Reemplaza pr-review, po-review, security-audit, agent-review."
---

# Workflow: Review & Quality

## Skills que reemplaza
- `pr-review`
- `po-review`
- `security-audit`
- `agent-review`

## Qué hace
Revisión de calidad antes de mergear o cerrar un ciclo.

## Fases
1. **Análisis de diff** — cambios, archivos tocados, impacto
2. **Linter cognitivo** — convenciones, naming, estructura, tests. Verificar que el PR incluya tests, que pasen, que cubran edge cases, que haya cobertura para el cambio
3. **Auditoría de seguridad** — multi-tenant, auth, secrets, data leaks, RLS. Si el proyecto no es multi-tenant, saltar a auditoría básica (secrets, data leaks) sin el checklist completo de RLS/auth multi-tenant
4. **Revisión de producto** — ¿cumple con la spec? ¿satisface la necesidad?
5. **Reporte** — hallazgos, bloqueantes, sugerencias
6. **Gate** — bloquea cierre si hay hallazgos críticos

## Outputs
- Reporte de revisión
- Hallazgos de seguridad
- Decisión: approve / changes requested / blocked
