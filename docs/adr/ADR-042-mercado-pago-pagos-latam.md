# ADR-042: Pagos - el proveedor se elige por proyecto y se justifica

**Status:** Accepted (2026-08-29) - revisado a fondo 2026-10-06
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-08-29
**Origen:** workspace (regla operativa fijada por Gonzo, 2026-08-29; revisada 2026-10-06)

---

## Contexto

Los proyectos con cobros (micro-SaaS, suscripciones, prints) necesitan un proveedor de pagos. La version original de este ADR (2026-08-29) fijo **Mercado Pago como proveedor obligatorio y prohibio Stripe**, con un unico motivo: se creia que Stripe no operaba en Argentina.

Dos hechos cambiaron (2026-10-06):

1. **Stripe ya opera en Argentina** (integracion reciente). La premisa de indisponibilidad dejo de ser cierta.
2. **Restriccion de plataforma:** en **Lovable**, Stripe es la **unica integracion de pago disponible**. Un proyecto construido en Lovable no puede cobrar con Mercado Pago sin salir de la plataforma.

Un proveedor unico obligatorio choca con ambas: prohibir Stripe bloquea todo proyecto construido en Lovable; obligar Mercado Pago bloquea lo mismo por el otro lado. **La regla anterior ya no describe el mundo.**

## Decision

**No hay un proveedor de pagos obligatorio en el ecosistema. Cada proyecto elige el suyo y lo justifica.**

1. **La eleccion se justifica por proyecto**, en su ADR/HANDOFF: que proveedor, por que, para que mercado. "Porque ya estaba" o "porque el ADR viejo lo decia" no es justificacion.
2. **Proyectos sobre Lovable -> Stripe.** Es la unica integracion de pago de la plataforma. No es una excepcion ni un fallback: es la **opcion natural del entorno**. Cualquier proyecto Lovable cobra por Stripe.
3. **Proyectos fuera de Lovable -> proveedor a eleccion, justificado.** **Mercado Pago es una opcion fuerte (no la unica)** por la cobertura de medios de pago locales en Argentina/LATAM (QR de Mercado Pago, Rapipago, PagoFacil, transferencias CBU/CVU, MODO) y moneda local. **Stripe es igualmente valido** cuando el proyecto lo justifica (y ya opera en Argentina).
4. **Otros proveedores** (dLocal, PayU, Izipay, GetNet, MoR tipo Paddle/Lemon Squeezy): validos segun el caso, con la misma exigencia de justificacion.
5. **Mercado objetivo:** Argentina y LATAM, con moneda local.

## Consecuencias

- **Positivas:** cada proyecto cobra con lo que mejor le sirve a su entorno y su mercado; ninguna regla transversal bloquea un proyecto por estar construido sobre una plataforma distinta. La decision se toma y se registra donde corresponde.
- **Costo asumido:** hay que **justificar** la eleccion por proyecto (mas trabajo de decision que un default impuesto), y no hay un "proveedor por defecto" memorizable. Es deliberado: preferimos la decision justificada al automatismo.
- **Registro:** la version original de este ADR (Mercado Pago obligatorio, Stripe prohibido) queda como **registro de origen**; no es la regla vigente.

## Estado actual de la eleccion

| Proyecto | Proveedor | Justificacion |
|---|---|---|
| **SoporteML** | **Stripe** | Construido sobre Lovable (unica integracion disponible). La version funcional de Lovable ya tiene cobro con Stripe operativo, habilitado en Argentina. Ver ADR-091. |

## Alternativas

- **Mercado Pago obligatorio (version original):** rechazada. Bloquea Lovable (donde MP no es integrable) y era un default impuesto, no una decision por proyecto.
- **Stripe obligatorio:** rechazada. Ignora la cobertura de medios de pago locales en Argentina/LATAM fuera de Lovable.
- **Default + excepcion (version intermedia):** rechazada por Gonzo (2026-10-06). Decir "Stripe solo por excepcion" **limita** Stripe sin motivo, cuando en realidad es la unica opcion en Lovable y una opcion valida en el resto.
