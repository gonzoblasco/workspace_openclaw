# Incident Response

Gestión de incidentes en producción.

## ¿Para qué sirve?

Para **gestionar incidentes de producción** de forma rápida, ordenada y repetible. Prioridad: restaurar el servicio con el menor impacto posible. No busca culpables, busca minimizar impacto y generar aprendizaje.

**Filosofía:** Restore service first. Understand later. Improve forever.

## ¿Cuándo usarlo?

- Caída de producción
- Degradación severa
- Pérdida de datos
- Problema de seguridad
- Alertas críticas
- Rollback urgente

## ¿Cómo se usa?

### Workflow completo

1. **Detection** — qué ocurrió, cuándo, evidencia
2. **Classification** — severidad (SEV-1 a SEV-4), alcance, usuarios afectados
3. **Containment** — rollback, feature flag OFF, deshabilitar endpoint
4. **Service Restoration** — restaurar servicio, no optimizar, no refactorizar
5. **Root Cause Analysis** — five whys, timeline analysis
6. **Corrective Actions** — correcciones inmediatas y permanentes
7. **Knowledge Capture** — postmortem, lessons learned
8. **Prevention** — ¿cómo evitamos que vuelva?

### Scripts útiles

```bash
# Generar incident report
./scripts/incident-report.sh --title "API timeout" --severity SEV-2

# Generar postmortem
./scripts/postmortem.sh --title "Database connection pool exhaustion" --severity SEV-1

# Generar timeline desde logs
./scripts/timeline.sh /var/log/app.log
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/severity.md` | Clasificación SEV-1 a SEV-4 con tiempos de respuesta |
| `references/postmortem-template.md` | Template de postmortem |
| `references/runbooks.md` | Runbooks: database degradation, API latency, memory leak |
| `references/communication-templates.md` | Templates: acknowledgment, update, resolution, postmortem |

## Skills relacionadas

- [Debug Investigation](../debug-investigation) — Para investigar causa raíz post-incidente
- [Observability](../observability) — Para mejorar detección y alertas
