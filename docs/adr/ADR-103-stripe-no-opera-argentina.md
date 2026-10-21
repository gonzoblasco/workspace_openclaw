# ADR-103: Stripe no opera en Argentina - Mercado Pago vuelve a ser proveedor válido

**Fecha:** 2026-10-21
**Estado:** Aceptado (corrige una premisa falsa de ADR-042)
**Decisores:** Gonzo / Kanam
**Origen:** verificación de disponibilidad para el producto OnWheels, que cobra a dealers argentinos en pesos
**Relacionado:** ADR-042 (superseded en su premisa) y `docs/ecosystem/CONSOLIDACION-PRODUCTO-DEALER.md` (las decisiones de producto que dependen de este ADR)
**Supersede:** ADR-042, secciones "Contexto" punto 1, "Decisión" puntos 1-2, y "Consecuencias"

---

## Contexto

El ADR-042 (2026-08-29, reescrito 2026-10-06) declara **Stripe como proveedor de pagos único reconocido**
del ecosistema, y para justificarlo afirma en su Contexto:

> "**Stripe ya opera en Argentina** (integración reciente). La premisa de indisponibilidad dejó de ser
> cierta."

**Esa premisa es falsa.** Verificado el 2026-10-21:

| Verificación | Resultado |
|---|---|
| `stripe.com/global` - grep de "Argentina" en el HTML servido | **0 ocurrencias** |
| La misma página - Brasil y México | **sí figuran** |
| `startglobal.co` (consulta 2026) | "No. Stripe does not currently support accounts registered in Argentina." |
| `getpaidatlas.com/stripe-alternatives/argentina` (chequeado 2026-10-20) | "Stripe is not available for businesses based in Argentina (not on stripe.com/global)" |
| `lupapago.com/fichas/stripe` (auditoría 2026-08-23) | "No hay merchant account local en Arg" - solo cross-border vía entidad extranjera |

El ADR-042 se apoyó en dos hechos, y **solo uno era cierto**:

1. ~~Stripe opera en Argentina~~ - **falso**. Stripe procesa pagos *hacia* clientes argentinos y permite
   *payouts* cross-border (agregado en marzo 2026, según su changelog), pero **no permite que una empresa
   argentina abra una cuenta de comercio**. Cobrar con Stripe desde Argentina exige una entidad en otro
   país (típicamente una LLC en EE. UU. vía Atlas).
2. En Lovable, Stripe es la única integración de pago disponible - **cierto**, y sigue siendo cierto.
   Pero es una restricción de **una plataforma**, no una razón para prohibir los medios de pago locales
   en todo el ecosistema.

### Por qué la distinción importa y no es semántica

El ADR-042 no dice "usemos Stripe porque funciona"; dice que el resto *no se reconoce como opción*. Con
la premisa falsa, esa regla produce un resultado absurdo: **un producto que le vende a comercios
argentinos, en pesos, con factura argentina, no puede cobrar** sin montar una sociedad en el exterior.
Eso no es una preferencia de proveedor: es un bloqueante de negocio disfrazado de estándar técnico.

---

## Decisión

**1. Stripe deja de ser el proveedor único. Se reconoce a Mercado Pago como proveedor válido y, para
productos que le venden a comercios argentinos, como el proveedor por defecto.**

**2. El criterio de elección pasa a ser dónde está el comprador, no qué plataforma se usó para
construir:**

| Dónde está el comprador | Proveedor | Motivo |
|---|---|---|
| **Argentina** (comercios, pymes, profesionales) | **Mercado Pago** | Merchant account local, cobro en ARS, medios locales, factura consistente |
| Fuera de Argentina, o cobro en USD a terceros | **Stripe** | Multi-moneda, suscripciones maduras, requiere entidad en país soportado |
| Proyecto construido en Lovable | **Stripe** | Única integración disponible en la plataforma; la excepción se mantiene |

**3. Un proyecto declara su proveedor y el motivo en su propio ADR.** No hay default impuesto: hay una
regla de encaje. Lo que no se acepta es elegir un proveedor que **no puede cobrar** en el país del
comprador.

**4. Se mantiene del ADR-042 lo que sigue siendo correcto:** una sola decisión transversal registrada,
sin alternativas flotando, y sin `if provider == "..."` disperso en el código. La abstracción de billing
(modelo de datos con `provider`, `external_customer_id`, `subscription_status`) es la misma; cambia qué
proveedor la implementa.

---

## Consecuencias

- **Positivas:** el producto de OnWheels puede cobrarle a un dealer argentino sin estructuras
  societarias en el exterior. Mercado Pago tiene suscripciones (`preapproval` / planes) con cobro
  recurrente en **ARS**, reintentos automáticos, período de prueba y medios locales (Rapipago, Pago
  Fácil, tarjeta, saldo en cuenta) - verificado en su documentación el 2026-10-21.
- **Costo asumido:** dos integraciones distintas según el mercado. La de Mercado Pago tiene su propio
  modelo (preapproval por suscripción, no por customer como Stripe) y **cobra en ARS**: un precio
  expresado en USD exige definir la política de conversión y de ajuste, que es una decisión de negocio
  aparte.
- **Riesgo nuevo, explícito:** un precio en USD cobrado en ARS queda expuesto al tipo de cambio. Las
  plataformas locales lo resuelven con **ajuste periódico de precios** (Tiendanube lo hace trimestral y
  lo publica en sus términos). Sin esa política escrita, el margen se licúa sola.
- **Lo que NO cambia:** SoporteML se construyó sobre Lovable y cobra con Stripe; esa excepción sigue
  vigente y no se toca (el proyecto además está dormido).

---

## Alternativas

- **Mantener ADR-042 y cobrar vía LLC en EE. UU.** - rechazada. Resuelve el cobro creando un problema
  fiscal y societario (constitución, EIN, obligaciones anuales, residencia fiscal) para un producto que
  le vende a comercios de la misma ciudad. Costo desproporcionado al beneficio.
- **Stripe + Mercado Pago en simultáneo desde el día uno** - rechazada para el MVP. Duplica superficie
  de integración, webhooks y conciliación sin un comprador que lo justifique. Se suma cuando haya
  clientes fuera de Argentina (ver tabla de encaje).
- **Cobro manual por transferencia** - rechazada como diseño. No es una suscripción: el mes 2 no se
  cobra solo. Válida solo como excepción temporal con fecha de corte.
- **Reescribir ADR-042 borrando la premisa falsa** - rechazada. Los ADR son append-only: el error queda
  registrado con su corrección, que es la única forma de que no se repita.
