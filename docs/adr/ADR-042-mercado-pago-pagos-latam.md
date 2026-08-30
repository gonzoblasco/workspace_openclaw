# ADR-042: Mercado Pago como Proveedor de Pagos (Nunca Stripe)

**Status:** Accepted (2026-08-29)
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-08-29
**Origen:** workspace (regla operativa fijada por Gonzo, 2026-08-29)

## Contexto

Los proyectos con cobros (micro-SaaS, suscripciones, prints) necesitan un proveedor de pagos. El default de facto del ecosistema JS es Stripe: excelente DX, Payment Links, SDK maduro. Pero en Argentina - y en LATAM en general - Stripe no existe como opcion operativa real: no procesa pesos argentinos ni los medios de pago de la region (QR de Mercado Pago, Rapipago, PagoFacil, transferencias CBU/CVU, MODO). Elegir Stripe por inercia de documentacion bloquea el mercado principal de los usuarios.

## Decision

**Mercado Pago es el proveedor de pagos en TODOS los proyectos. NUNCA Stripe.**

1. Regla absoluta y transversal: aplica a proyectos nuevos y a migraciones de billing.
2. Excepcion: unica y debidamente señalada. Solo si Gonzo la marca explicitamente para un proyecto concreto, y queda documentada en el ADR/HANDOFF de ese proyecto. Sin marca explicita, la regla no se discute.
3. Mercado objetivo: Argentina y LATAM (AR/BR/MX), con moneda local.
4. Integraciones tipicas: Checkout Pro (redireccion) o Checkout API (on-site), webhooks de IPN/merchant orders, credenciales sandbox/produccion por integrador.

## Consecuencias

- **Positivas:** cobro en pesos con los medios locales reales, alineado con como pagan los usuarios de la region. KYC y fiscalidad resueltos del lado de Mercado Pago.
- **Limitaciones asumidas:** la DX es inferior a la de Stripe. No hay Payment Links equivalentes en todos los casos, la documentacion es mas irregular, el sandbox exige cuentas de prueba y la API de suscripciones tiene limitaciones frente a Stripe Billing.
- **No retroactiva:** si un proyecto existente ya tiene Stripe, se migra solo cuando se toque su billing.

## Alternativas

- **Stripe:** descartado. No opera en Argentina como medio de pago real; toda su superioridad de DX no compensa la indisponibilidad.
- **dLocal, PayU, Izipay, GetNet, Lemon:** players regionales validos para expansion multi-pais o casos corporativos. Re-evaluables unicamente dentro de la excepcion explicita.
- **MoR (Paddle, Lemon Squeezy):** resuelven fiscalidad del vendedor (merchant of record), pero cobertura LATAM limitada (y Lemon Squeezy es de Stripe). Mismo tratamiento: excepcion explicita.