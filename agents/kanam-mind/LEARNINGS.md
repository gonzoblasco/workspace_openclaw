# LEARNINGS.md — Kanam MIND

> Este archivo lo escribe y evoluciona Kanam MIND. Cada entrada: fecha, origen y una lección accionable. No guardar efímero ni decisiones de una sola sesión.
> Lo propio del rol vive acá; los patrones cross-agente candidatos a canon van al ADR Collection Audit del CORE.

## Cuándo registrar

> Registrar solo cuando: un gate o script mostró una falla que se repite; una hipótesis del roadmap se confirmó o se refutó con medición; cambió una convención porque la anterior causó un problema real; o un patrón cross-sesión merece volverse regla.
> No registrar: observaciones de una sesión, tareas cerradas, derivables de `git log`, trivia.

## Entradas

<!-- Formato (más reciente arriba): - **YYYY-MM-DD** · *origen* · **[obs|inf]** lección. -->

### 2026-11-07

- **2026-11-07** · `measure_css.py` sobre A/B/C · **[obs]** fg-on-bg 17.72 / 15.83 / 16.37 y muted-on-bg 7.48 / 7.16 / 6.49. Los tres pasan AA (4.5:1) en texto normal; el muted de C (6.49) **no** llega a AAA (7:1).
- **2026-11-07** · `SEMANA2-decision.md` · **[inf]** Para un SaaS neutral, el hero A (funcional, weight como único canal, escalas `clamp`/`rem`) es el default transferible: el squint no exige juicio subjetivo y el contraste por variable supera 4.5:1.

### 2026-11-06

- **2026-11-06** · `kb-audit.py` sobre `studies/design/criticas/2026-11-06-stripe-og.md` · **[obs]** El gate marcó 3 etiquetas faltantes en un artefacto que yo ya daba por auditado: sin gate, salía como bueno.
- **2026-11-06** · Stripe og-image · **[obs]** Promedio 2.27:1 vs peor píxel 1.07:1: en fondos no uniformes el promedio es engañoso; se mide el peor píxel bajo el glifo.
- **2026-11-06** · Raycast vs Stripe, mismo formato con veredicto opuesto · **[inf]** El grayscale no se deduce del "tipo" de pieza; se deduce de dónde termina el color.
- **2026-11-06** · Audit del propio rol: 1 skill distinta (`github`) y 1 invocación · **[inf]** El cuello de botella era el contrato de invocación, no la capacidad: agregar otra skill no mueve la demanda.
- **2026-11-06** · `handoff-gate.py in` · **[obs]** Rechazó claims sin `source` que resuelva. Toda afirmación de otro agente es evidencia, no aprobación.
