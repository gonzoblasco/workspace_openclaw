# Resumen de tasa de absorción del friction ledger

**Fecha:** 2026-11-19

## Métricas actuales

| Métrica | Valor |
|---|---|
| Total de fricciones | 27 |
| Absorbidas propias (6 del kit F1-F6 + 1 del disparador F15) | 7 |
| Absorbidas de autores ajenos | 0 |
| Fricciones abiertas | 20 |
| Tasa de absorción (absorbidas / total) | 25.9 % |

> **Nota:** El dato anterior en el ROADMAP (“20 fricciones / 7 absorbed / 13 open”) estaba desactualizado. Ahora el ledger muestra 27 fricciones, 7 absorbidas y 20 abiertas: +7 totales y +7 abiertas, con las absorbidas sin cambios.
>
> **Lectura honesta:** las 7 absorbidas son todas auto-corrección del propio Critic. La absorción por autores ajenos es **0** sobre 4 VETOs emitidos (`docs-ROADMAP-madurez`, `kanam-dev-ROADMAP`, `kanam-dev-inventario-skills`, `docs-NORTH`). Eso es exactamente lo que F9 marcaba como la métrica fácil.

## Salida cruda de `check‑kit.py`

```
[OK  ] identidad propia: AGENTS.md                          agents/kanam-critic/AGENTS.md
[OK  ] identidad propia: SOUL.md                            agents/kanam-critic/SOUL.md
[OK  ] identidad propia: IDENTITY.md                        agents/kanam-critic/IDENTITY.md
[OK  ] identidad propia: USER.md                            agents/kanam-critic/USER.md
[OK  ] identidad propia: MEMORY.md                          agents/kanam-critic/MEMORY.md
[OK  ] catalogo: evidence-hunter                            keep
[OK  ] catalogo: sharp‑adversarial‑review                   keep
[OK  ] promesas rotas: 'openclaw skill run'                 sin referencias vivas
[OK  ] lab evidence‑hunter                                  GLOBAL=aprobado  (6/6 casos en estado y cita esperados)
[OK  ] veredictos reales registrados                        10 real(es), 2 fixture(s)
[OK  ] veredictos con respaldo (verify‑verdict.py)          GLOBAL=aprobado  (8/8 veredictos reales validos con respaldo, 2 anulado(s))
[OK  ] disparador: heartbeat por agente                     agents.entries.kanam-critic.heartbeat
[OK  ] presupuesto: AGENTS.md                               2326 / 20000 caracteres
[OK  ] presupuesto: SOUL.md                                 2385 / 20000 caracteres
[OK  ] presupuesto: IDENTITY.md                             1316 / 20000 caracteres
[OK  ] presupuesto: USER.md                                 1150 / 4000 caracteres
[OK  ] presupuesto: MEMORY.md                               4527 / 20000 caracteres
[OK  ] presupuesto: total                                   11704 / 60000 caracteres
----------------------------------------------------------------------------------------------------
GLOBAL=aprobado  (18/18 checks verdes)
```