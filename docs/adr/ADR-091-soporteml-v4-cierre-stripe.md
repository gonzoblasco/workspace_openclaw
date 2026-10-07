# ADR-091: SoporteML v4 se cierra; el producto sigue por la version funcional de Lovable con cobro por Stripe

**Fecha:** 2026-10-06
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** instruccion de Gonzo (2026-10-06): *"cerramos soporteml 4, ya he agregado sistema de cobro por Stripe en la version funcional de lovable"*
**Relacionado:** ADR-068 (greenfield basado en v1 - superado), ADR-067, ADR-042 (pagos: eleccion por proyecto), ADR-001 de portfolio-strategy (seccion 7)

---

## Contexto

El 2026-09-24, ADR-068 reabrio SoporteML como una generacion **greenfield** basada en v1 (la version de Lovable, la mas completa de las cuatro), con alcance ampliado a "SaaS CRM y contable para pymes". Ese ADR quedo **incompleto por diseno**: dejo 6 pendientes explicitos y sin responder la pregunta central de cuatro generaciones (**¿por que esta vez tendra usuarios?**).

El 2026-10-06 Gonzo dio el cierre: **SoporteML v4 se cierra**, y en su lugar **agrego el sistema de cobro por Stripe a la version funcional de Lovable**, habilitado en Argentina.

Esto es coherente con la medicion de ADR-068: v4 era una **poda** de v1, no una sucesora. En vez de un greenfield, el producto avanza sobre la version que ya funciona.

## Decision

1. **SoporteML v4 se cierra.** El reinicio v4 no continua. Supera los pendientes de *generacion* de ADR-068: el greenfield CRM+contable no se construye como estaba planteado.
2. **El producto sigue por la version funcional de Lovable (v1)**, que ahora incorpora **cobro por Stripe**, habilitado en Argentina.
3. **Pagos (ADR-042):** **Stripe es el proveedor único** del ecosistema, sea o no con Lovable. SoporteML cobra con Stripe porque es el proveedor reconocido (y ademas es la unica integracion disponible en Lovable).
4. **La regla de narrativa publica no cambia:** SoporteML sigue fuera de la narrativa publica / del CV (ADR-001 seccion 7) y fuera de barridos automaticos de limpieza.

## Consecuencias

### Positivas
- Cierra una etapa de cuatro generaciones sin demanda probada. El producto deja de "reiniciarse".
- **El primer proyecto del ecosistema con billing real y operativo:** v1 tenia el billing escrito y jamas operativo (secrets sin configurar, plan de preapproval sin crear en MP).

### Decision de alcance (cerrada)
- **La version se queda en Lovable.** No se migra a stack propio: la "Fase 4 - salir de Lovable" de v1 **no se persigue** (decision de Gonzo, 2026-10-06). Las dependencias de Lovable (auth y AI gateway de Lovable, Supabase BaaS) son el entorno elegido, no deuda a saldar.
- **SoporteML no deja pendientes abiertos.** El proyecto avanza sobre la version funcional de Lovable tal como esta.

## Alternativas consideradas
1. **Continuar el greenfield de ADR-068.** Descartada por instruccion de Gonzo.
2. **Cerrar SoporteML por completo.** No es lo que se decidio: el producto sigue vivo por la version funcional.
3. **Migrar a stack propio (Fase 4 de v1).** Descartada: la version se queda en Lovable.

## Notas de mantenimiento
- La propagacion del 2026-10-06 toco: `MEMORY.md`, `AGENTS.md`, `docs/NORTH.md`, `docs/ROADMAP.md` (entonces tambien el registro de apuestas, hoy retirado), `memory/user-profile.md`, `docs/adr/ADR-042` (revisado a eleccion por proyecto), este ADR, y la DB (`memory/memory.db`, tabla `learnings`).
- El cambio a Stripe ya habia asomado el 2026-10-01 en superficies de CV (`docs/entrevistas/mercadolibre-cards-nfc-aplicacion.md`) y en `DREAMS.md`, pero **no se habia propagado a las fuentes durables**. Este ADR cierra ese hueco.
