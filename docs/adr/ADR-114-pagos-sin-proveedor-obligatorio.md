# ADR-114: Pagos sin proveedor obligatorio - eleccion por proyecto

**Status:** Accepted (2026-11-18)
**Supersedes:** ADR-042
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-11-18
**Origen:** instruccion directa de Gonzo en sesion ("quitemos toda restriccion al seleccionar Pagos")

---

## Contexto

ADR-042 (2026-08-29, revisado 2026-10-06) fijo **Stripe como proveedor unico reconocido** del
ecosistema y dejo a Mercado Pago explicitamente afuera como intencion. Esa regla nacio de dos
hechos de 2026-10-06:

1. Stripe opera en Argentina (su premisa original -que no operaba- era falsa).
2. Lovable solo integra Stripe, asi que limitar Stripe no tenia sentido.

Ninguno de los dos hechos **obliga** a excluir a los demas. El primer hecho derriba el motivo de la
version original (Mercado Pago obligatorio), pero no dice nada sobre prohibir Mercado Pago. El
segundo hecho es una restriccion **de plataforma**, no una razon de negocio: aplica a los productos
que viven en Lovable, no a cualquier proyecto.

Al mismo tiempo, ADR-042 ya tenia una valvula: su punto 2 permitia que un proyecto evaluara otro
proveedor y lo registrara (OnWheels lo hizo con Mercado Pago). O sea: la regla ya no era universal
en la practica, solo decia que otros caminos no estaban "previstos". Una regla que se excepciona por
proyecto no necesita ser una regla: necesita ser una decision de cada proyecto.

En Argentina/LATAM la cobertura de medios locales (cuenta/CBU/CVU, QR, Rapipago, Pago Facil, MODO) y
el cobro en ARS sin conversion son argumentos reales que Stripe no cubre del todo, y el cliente lo
siente. Impedir por decreto esa evaluacion obliga a justificar un default cada vez que aparece un
caso donde el otro proveedor encaja mejor.

## Decision

**No hay proveedor de pagos obligatorio ni excluido por regla global.**

1. **La eleccion es del proyecto**, y se decide con criterio explicito: mercados y medios de pago del
   cliente, moneda de cobro, pais donde opera la entidad, plataforma donde vive el producto (Lovable
   solo permite Stripe) y costo/complejidad de integracion.
2. **Stripe y Mercado Pago son ambos caminos validos**, sin jerarquia preestablecida. Ninguno
   requiere ADR de excepcion.
3. **La decision se registra en el ADR del proyecto** (ADR-067), con el motivo. No se eleva al
   corpus global salvo que cambie una regla transversal.
4. **`billing_provider` es un dato, no una rama:** el modelo de datos de un producto multi-proveedor
   guarda el proveedor por cuenta y la logica de features no ramifica por proveedor (patron ya
   validado en `memory/onwheels-producto.md`).
5. **ADR-042 queda Superseded.** Su contenido permanece como registro de por que se decidio cada
   version; no se cita como regla vigente.

## Consecuencias

- **Positivas:** el proyecto elige el proveedor que le sirve, con el criterio escrito al lado. Se
  elimina una regla global que ya se excepcionaba en la practica. Los productos que cobran en ARS con
  medios locales no tienen que pedir permiso.
- **Costo asumido:** se pierde la ventaja de "no decidir cada vez". Se mitiga con el punto 3 (la
  decision vive en el ADR del proyecto) y con el punto 4 (el dato, no la rama).
- **Riesgo:** fragmentacion de integraciones. Se acepta: es el mismo costo que ya existia, solo que
  ahora esta declarado en vez de escondido como excepcion.
- **Historial no se borra:** el trabajo hecho con Mercado Pago (SoporteML v1, OnWheels) y con Stripe
  (SoporteML, actual) sigue documentado.

## Estado actual de la eleccion

| Proyecto | Proveedor | Por que |
|---|---|---|
| **SoporteML** | Stripe | Producto sobre Lovable (unica integracion disponible) y cobro operativo en Argentina. Sin cambio por este ADR. |
| **OnWheels** | Mercado Pago | Ya registrado en su doc de producto (§10 bis). Cobro recurrente en ARS con medios locales. |

## Alternativas

- **Mantener ADR-042 (Stripe unico):** rechazada. Excluia un camino valido por un motivo de
  plataforma y obligaba a excepcionar proyecto por proyecto.
- **Mercado Pago como default:** rechazada (y ya lo estaba desde 2026-10-06). Repetiria el error de
  imponer un proveedor que no aplica a los proyectos que viven en Lovable.
- **Proveedor por rol de proyecto (ej. Lovable=Stripe, resto=MP):** rechazada. Convierte un criterio
  de negocio en un automatismo y vuelve a decidir por el proyecto.
