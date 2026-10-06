# ADR-042: Mercado Pago como Proveedor de Pagos por Defecto (Stripe solo por excepcion)

**Status:** Accepted (2026-08-29) - premisa de disponibilidad revalidada 2026-10-06; excepcion otorgada 2026-10-06
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-08-29
**Origen:** workspace (regla operativa fijada por Gonzo, 2026-08-29)

## Contexto

Los proyectos con cobros (micro-SaaS, suscripciones, prints) necesitan un proveedor de pagos. El default de facto del ecosistema JS es Stripe: excelente DX, Payment Links, SDK maduro. **Al escribir este ADR (2026-08-29), la premisa era que** en Argentina - y en LATAM en general - Stripe no existia como opcion operativa real: no procesaba pesos argentinos ni los medios de pago de la region (QR de Mercado Pago, Rapipago, PagoFacil, transferencias CBU/CVU, MODO). Elegir Stripe por inercia de documentacion bloqueaba el mercado principal de los usuarios.

> **Revalidacion (2026-10-06):** la premisa de disponibilidad cambio. **Stripe ya opera en Argentina** (integracion reciente; confirmado por Gonzo, que la usa en SoporteML, y por la documentacion publica de Stripe, que suma Argentina a sus destinos soportados). La regla de default por defecto se conserva -Mercado Pago sigue siendo el default por los medios de pago locales-, **pero la afirmacion "Stripe no opera en Argentina" ya no es cierta y no debe repetirse como razon**. El registro original se conserva arriba como decision de origen.

## Decision

**Mercado Pago es el proveedor de pagos por defecto en TODOS los proyectos. Stripe queda como alternativa por excepcion (ver punto 2).**

> Matiz (2026-10-06): la eleccion de Mercado Pago como default ya **no** se apoya en "Stripe no opera en Argentina" (dejo de ser cierto). Se apoya en la **cobertura de medios de pago locales** (QR de Mercado Pago, Rapipago, PagoFacil, transferencias CBU/CVU, MODO) y en la moneda local, que es como paga la mayoria del mercado objetivo. Un proyecto puede elegir Stripe por excepcion explicita.

1. Regla absoluta y transversal: aplica a proyectos nuevos y a migraciones de billing.
2. Excepcion: unica y debidamente señalada. Solo si Gonzo la marca explicitamente para un proyecto concreto, y queda documentada en el ADR/HANDOFF de ese proyecto. Sin marca explicita, la regla no se discute.
3. Mercado objetivo: Argentina y LATAM (AR/BR/MX), con moneda local.
4. Integraciones tipicas: Checkout Pro (redireccion) o Checkout API (on-site), webhooks de IPN/merchant orders, credenciales sandbox/produccion por integrador.

## Consecuencias
- **Positivas:** cobro en pesos con los medios locales reales, alineado con como pagan los usuarios de la region. KYC y fiscalidad resueltos del lado de Mercado Pago.
- **Limitaciones asumidas:** la DX es inferior a la de Stripe. No hay Payment Links equivalentes en todos los casos, la documentacion es mas irregular, el sandbox exige cuentas de prueba y la API de suscripciones tiene limitaciones frente a Stripe Billing.
- **No retroactiva:** si un proyecto existente ya tiene Stripe, se migra solo cuando se toque su billing.

## Excepcion otorgada (2026-10-06)

**SoporteML usa Stripe.** Gonzo marco explicitamente la excepcion del punto 2: agrego el sistema de cobro por **Stripe** a la version funcional de Lovable de SoporteML, habilitado en Argentina. Registrada en **ADR-091** (que tambien cierra SoporteML v4).

Esto no cambia la regla general: Mercado Pago sigue siendo el default del ecosistema. La excepcion es de un proyecto concreto y esta documentada (esta seccion + ADR-091). Contexto: la premisa original de este ADR ("Stripe no opera en Argentina") **dejo de ser cierta** -Stripe ya opera en Argentina-, asi que Stripe deja de ser "algo que no se puede" y pasa a ser "algo que no es default".

## Alternativas

- **Stripe:** al escribir el ADR, descartado por indisponibilidad en Argentina. **Esa razon ya no aplica (2026-10-06: Stripe opera en Argentina).** Sigue disponible solo por la excepcion del punto 2; su DX superior ya no esta contrapesada por falta de disponibilidad.
- **dLocal, PayU, Izipay, GetNet, Lemon:** players regionales validos para expansion multi-pais o casos corporativos. Re-evaluables unicamente dentro de la excepcion explicita.
- **MoR (Paddle, Lemon Squeezy):** resuelven fiscalidad del vendedor (merchant of record), pero cobertura LATAM limitada (y Lemon Squeezy es de Stripe). Mismo tratamiento: excepcion explicita.