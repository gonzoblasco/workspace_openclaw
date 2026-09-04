# ADR-044: Methodology Audit - Marco de 8 Fases como Lente de Auditoría

**Status:** Proposed (borrador)
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-09-03
**Origen:** workspace (sesión 2026-09-03, framework traído por Gonzo)

## Contexto

Gonzo trajo un framework de adopción de IA en 8 fases, usado por consultoras para organizaciones:

> Identify Objectives → Map Processes → Prioritize Opportunities → Activate Training → Construct Pilots → Trace Governance → Accelerate Adoption → Iterate and Scale

La pregunta inicial fue si esto debía convertirse en workflow, pipeline, hook o lista de tareas. El riesgo de malinterpretarlo era real: forzarlo como pipeline (como el A/B o el complexity-driven) lo haría competir con mecanismos de ejecución que ya existen y funcionan, creando solapamiento y fricción en lugar de valor.

El sistema ya tiene pipelines de ejecución sólidos (ADR-041 selección de modelo por tarea, ADR-043 complexity-driven pipeline). Lo que NO tiene es un mecanismo periódico para auditar sus propias metodologías: las skills nacen reactivas (de un incendio puntual), la gobernanza de procesos depende de memoria (a diferencia de la de código, que está en hooks), y no hay momento sistemático de pregunta "¿qué metodología está obsoleta, cuál falta, cuál dimensión descuidamos?".

## Decision

**El framework de 8 fases NO es un pipeline. Es un lente de auditoría periódica sobre el ecosistema de metodologías del workspace.**

### Qué es

1. **Termómetro de madurez:** mapea las 8 fases contra lo que el sistema ya tiene (docs, scripts, skills, rituales), puntúa cada fase 0-2, y devuelve un total 0-16 con banda de estado. Vive en `docs/METHODOLOGY-AUDIT.md`.
2. **Check rápido (guardado de sesión):** 8 casillas que se corren al guardar sesión SOLO si la sesión tocó metodología (skills, AGENTS.md, scripts, docs de proceso, lecciones nuevas). 3+ casillas sin marcar = deuda metodológica, se registra como pendiente. No es gate de cada sesión: si la sesión no tocó metodología, se saltea (sería ruido).
3. **Auditoría profunda:** trimestral o a pedido de Gonzo. Puntaje 0-16, identifica las 2 fases más bajas como objetivo del próximo trimestre.

### Qué NO es

1. **NO reemplaza al pipeline A/B** (ADR-041/043): estos deciden CÓMO ejecutar una tarea (modelo, thinking, agentes). El framework decide CÓMO MADURAR las metodologías. Complementarios, planos distintos.
2. **NO es gate diario:** no se corre en cada sesión ni en cada tarea. Solo en guardado con toque metodológico, y en auditoría profunda.
3. **NO es lista de tareas operativa:** no genera backlog de features ni de código. Genera deuda metodológica y acciones de madurez.

### Relación con otros mecanismos

| Mecanismo | Pregunta que responde | Frecuencia |
|---|---|---|
| Pipeline A/B + complexity-driven (ADR-041/043) | ¿Cómo ejecuto esta tarea? | Por tarea |
| Skill workshop (propose) + post-task-reflection | ¿Qué aprendí y qué skill falta? | Por tarea/lección |
| **Methodology Audit (este ADR)** | ¿El ecosistema de metodologías está sano? | Guardado con toque metodológico + trimestral |
| Guardado de sesión (session-lifecycle) | ¿Quedó todo registrado? | Por sesión |

## Consecuencias

- **Positivas:** las metodologías dejan de ser reactivas; hay momento y criterio para preguntar qué mejorar. El mapeo obliga a que cada fase tenga evidencia concreta (docs, scripts, hooks), lo que expone gaps reales.
- **Positivas (posicionamiento):** el framework es vocabulario presentable en entrevistas/consultoría. Cada fila del mapeo es un claim verificable con links a docs, skills y commits reales - no humo.
- **Coste:** una auditoría profunda cuesta una sesión (estimado 30-60 min). El check rápido agrega ~1 min al guardado cuando corresponde.
- **Riesgo de mal uso:** que se convierta en burocracia (correrlo en cada sesión) o en competidor del pipeline (usarlo para decidir ejecución). El ADR lo previene con la sección "Qué NO es".

## Alternativas

- **Convertirlo en pipeline (rechazado):** competiría con ADR-041/043 en el plano de ejecución. Ya existen mecanismos buenos para eso; duplicar es fricción.
- **Solo lista de tareas (rechazado):** perdería la función de diagnóstico. Una lista sin puntaje ni mapeo no destapa qué dimensión está descuidada.
- **No hacer nada (rechazado):** los gaps detectados (skills reactivas, gobernanza de procesos sin automatizar, falta de auditoría periódica) son reales y no se cierran solos.

## Nota de evolución

El mapeo de fases y la tabla de puntajes no son estáticos: cada auditoría profunda puede ajustar señales de salud, bandas o el mapeo mismo si el ecosistema cambia. La regla de oro del ADR aplica: si una decisión de este documento queda obsoleta por evidencia nueva, se modifica este ADR - no se re-pregunta en cada sesión.
