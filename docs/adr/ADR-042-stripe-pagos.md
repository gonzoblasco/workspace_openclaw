# ADR-042: Stripe como proveedor de pagos unico reconocido

**Status:** Accepted (2026-08-29) - revisado a fondo 2026-10-06
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-08-29
**Origen:** workspace (regla operativa fijada por Gonzo, 2026-08-29; revisada varias veces el 2026-10-06)

---

## Contexto

Los proyectos con cobros (micro-SaaS, suscripciones, prints) necesitan un proveedor de pagos.

La version original de este ADR (2026-08-29) fijo **Mercado Pago como proveedor obligatorio y prohibio Stripe**, con un solo motivo: se creia que Stripe no operaba en Argentina. Dos hechos derribaron esa regla (2026-10-06):

1. **Stripe ya opera en Argentina** (integracion reciente). La premisa de indisponibilidad dejo de ser cierta.
2. **Restriccion de plataforma:** en **Lovable**, Stripe es la **unica integracion de pago disponible**. Un proyecto construido en Lovable no puede cobrar con Mercado Pago sin salir de la plataforma.

Una version intermedia del mismo dia ("Stripe solo por excepcion") tambien quedo mal: **limitar Stripe no tiene sentido** cuando es la unica opcion en Lovable y una opcion valida en cualquier otro proyecto.

## Decision

**Stripe es el proveedor de pagos unico reconocido del ecosistema.**

1. **Stripe es el proveedor por defecto y el unico reconocido**, sea o no un proyecto sobre Lovable. Un proyecto que cobre usa Stripe.
2. **No hay proveedor obligatorio alternativo.** Otros proveedores (Mercado Pago, dLocal, PayU, etc.) **no se reconocen como opcion** en la regla del ecosistema. Si en el futuro un proyecto necesita otro, se evalua y se decide ahi (y se registra), pero no esta reconocido hoy como camino previsto.
3. **Mercado Pago queda fuera como intencion.** No se elimina su existencia (el know-how, el registro historico y lo que ya se construyo con el), se elimina la **intencion** de usarlo: deja de figurar como opcion fuerte, como default alternativo o como plan.
4. **Registro:** las versiones previas de este ADR (Mercado Pago obligatorio; luego eleccion por proyecto) quedan como **registro de origen**. No son la regla vigente.

## Consecuencias

- **Positivas:** una sola regla transversal, memorizable y sin ambiguedad. Cualquier proyecto que cobre lo hace con Stripe, sin tener que decidir proveedor cada vez. Alineado con la plataforma donde realmente se construye (Lovable) y con el hecho de que hoy no se usan otros modos de pago.
- **Costo asumido:** se pierde la cobertura explicita de medios de pago locales de Mercado Pago (QR, Rapipago, PagoFacil, CBU/CVU, MODO) como camino previsto. Si un proyecto futuro la necesita, sera una decision nueva a registrar, no un default disponible.
- **Registro historico:** el trabajo previo con Mercado Pago (p. ej. el billing de SoporteML v1) existe y no se borra; lo que cambia es que no se vuelve a proponer como via.

## Estado actual de la eleccion

| Proyecto | Proveedor | Por que |
|---|---|---|
| **SoporteML** | **Stripe** | Version funcional sobre Lovable (unica integracion disponible) y cobro con Stripe ya operativo, habilitado en Argentina. Ver ADR-091. |

## Alternativas

- **Mercado Pago obligatorio (version original):** rechazada. Bloqueaba Lovable (donde MP no es integrable) y era un default impuesto.
- **Eleccion por proyecto (version intermedia, misma fecha):** rechazada por Gonzo. Mantenia a Mercado Pago como "opcion fuerte" y obligaba a justificar cada vez; Stripe queda como el unico reconocido.
- **Stripe solo por excepcion (version intermedia anterior, misma fecha):** rechazada por Gonzo. **Limitaba** Stripe sin motivo.
