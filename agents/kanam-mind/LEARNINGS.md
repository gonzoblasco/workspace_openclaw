# LEARNINGS.md — Kanam MIND

_Este archivo lo escribe y evoluciona Kanam MIND. Cada entrada: fecha, origen, una lección accionable. No guardar efímero ni decisiones efímeras de una sesión._ <!-- project: github.com/gonzoblasco/workspace_openclaw -->

## Sólo cuando haya aprendizaje durable

Registrar aquí cuando:
- Un gate o script me mostró que algo fallaba y la causa se repite.
- Una hipótesis del roadmap se confirmó o se refutó con medición.
- Cambio una convención porque el anterior causó problema real.
- Un patrón cross-sesión merece volverse regla.

No registrar: observaciones de una sesión, tareas cerradas, derivables de git log, trivia.

## Entradas

<!-- Formato (más reciente arriba):
- **YYYY-MM-DD** · *origen* · **Lección**.
-->

### 2026-11-06

- **2026-11-06** · `kb-audit.py` flaggeó 3 etiquetas faltantes en `criticas/2026-11-06-stripe-og.md` ya auditado · Sin gate, un artefacto mío salía como bueno.
- **2026-11-06** · Stripe og-image: promedio 2.27:1 vs peor píxel 1.07:1 · En fondos no uniformes el "promedio" es engañoso; medir siempre el peor píxel bajo el glifo.
- **2026-11-06** · Raycast vs Stripe (mismo formato, veredicto opuesto) · El grayscale no se deduce del "tipo" de pieza; se deduce de dónde termina el color.
- **2026-11-06** · Audit del propio MIND: 1 skill distinta (`github`) y 1 invocación · La demanda del rol no es capacidad ausente sino contrato de invocación; agregar skill no mejora la demanda.
- **2026-11-06** · `handoff-gate.py in` rechazó claims sin `source` válido · Toda afirmación de otro agente es evidencia, no aprobación; sin fuente resoluble no entra al brief.
