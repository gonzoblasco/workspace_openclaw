---
name: "trust-vocabulary-report"
description: "Reportar trabajo de agentes sin inflarlo: cuando hay que cerrar una tanda delegada, cuando un informe mezcla lo verificado con lo que solo dijo el agente, o cuando 'todo bien' convive con escenarios que nunca se corrieron."
metadata:
  category: "Hermes SDD"
  tags:
    - hermes-sdd
    - imported
    - reporting
---

# trust-vocabulary-report

Estandar de reporte extraido de `mcabreradev/hermes-sdd-agency`
(`templates/final-report.md`, `rules/orchestration.md`). Reemplaza el reporte narrativo por
un contrato: cada afirmacion cita donde esta su evidencia, y la profundidad de verificacion
se declara.

## Cuando usarla

- Hay que cerrar una tanda de trabajo delegado.
- Un informe mezcla lo verificado con lo que solo dijo un agente.
- Aparece un "todo bien" junto a escenarios que nunca se corrieron.

## El vocabulario de confianza

Cada etapa se cierra con uno de estos cuatro niveles. No son adjetivos: son el resultado de
haber intentado reproducir la afirmacion.

| Nivel | Significado |
|---|---|
| `verified` | Se volvio a correr en el repo real. La afirmacion esta reproducida |
| `partially_verified` | Se verifico parte; el hueco esta declarado explicitamente |
| `self_reported` | Solo lo dijo el agente; no se reprodujo todavia |
| `blocked` | No se pudo verificar, y se dice por que |

**Una etapa critica (review, QA, release) nunca cierra en `self_reported`.** Si la unica
fuente es el relato del agente, la etapa no esta cerrada.

## La estructura del reporte

1. **Estado:** completado / parcial / bloqueado / escalado al humano.
2. **Que se hizo:** una fila por etapa cerrada, con su artefacto y su ruta. Sin narrar el proceso.
3. **Artefactos:** archivos creados o modificados, con rutas.
4. **Verificacion:** los gates reales que se corrieron y su salida. Lo que no se corrio, se dice.
5. **Nivel de confianza por etapa** (la tabla de arriba).
6. **Defectos, deuda y huecos:** hallazgos abiertos con severidad, deuda declarada,
   escenarios `NO CORRIDO`. Si no hay nada, se dice "ninguno".
7. **Decisiones tomadas**, con su path.
8. **Proximo paso:** exactamente uno, accionable.

## Las reglas

- **Ninguna afirmacion sin evidencia.** Cada fila cita donde esta el resultado.
- **La deuda se declara.** "Todo bien" con escenarios `NO CORRIDO` es un reporte falso.
- **Un solo proximo paso**, concreto.
- **El reporte no reemplaza los gates.** Es la superficie de auditoria, no la prueba.

## Medido en Kanam

El 2026-09-28 el patron fallo dos veces seguidas por no tener este contrato: sub-agents
cerraron en `done` con tablas de exito; el disco mostro cifras distintas. El runtime valida
que el proceso termino limpio, no que el resultado sea cierto. Aplicar este vocabulario
habria dejado ambas etapas en `self_reported`, que es un estado incomodo pero honesto.

## Origen

`templates/final-report.md` (estructura y tabla de confianza) y `rules/orchestration.md`
(vocabulario de confianza). Se conserva el contrato; se descartan las referencias a
`bin/run-trace` y `reports/<runId>.jsonl`, que son de Hermes.
