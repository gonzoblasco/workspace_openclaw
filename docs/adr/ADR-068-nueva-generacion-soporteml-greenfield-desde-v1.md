# ADR-068: la nueva generacion de SoporteML es greenfield y se basa en v1, no en v4

**Fecha:** 2026-09-24
**Estado:** Aceptado (encuadre). Decisiones de stack, nombre y alcance contable: **pendientes**
**Decisores:** Gonzo / Kanam
**Origen:** pedido explicito de Gonzo de reabrir SoporteML ("reabramos soporteml, la version completa")
**Relacionado:** ADR-067 (verificar sujeto antes de borrar), ADR-001 de portfolio-strategy (seccion 7), ADR-001/002/003 de los repos v3/v4

> **Ubicacion:** este ADR vive en el workspace **temporalmente**. Por la regla 3 de ADR-067, al crearse el repo del proyecto debe migrarse ahi. No esta todavia porque el repo no existe.

---

## Contexto

Gonzo pidio reabrir SoporteML como producto nuevo, con una instruccion central y textual: **"NO BASARNOS EN SOPORTEML V4... DEBEMOS BASARNOS EXCLUSIVAMENTE EN SOPORTEML V1, la version de Lovable"**. Y precisó el alcance: *"las mismas features"*, extendido a *"una aplicacion saas crm y contable para pymes"*, considerando planes.

Esto reabre una decision **cerrada** en `portfolio-strategy/ADR-001` seccion 4, que declaraba SoporteML fuera de la narrativa con la instruccion **"NO TOCAR: este proyecto no se modifica, no se decide su destino"** y la salvedad *"no se vuelve a abrir salvo que Gonzo lo pida explicitamente"*. **Lo pidio explicitamente**, asi que la puerta prevista por ese ADR esta abierta. Ver seccion 7 de ese documento (enmienda).

### Por que v1 y no v4 (la medicion)

El inventario de las cuatro generaciones, medido sobre el codigo real:

| Gen | Migraciones | Tablas | Edge Functions | Componentes | Lineas `src/` | Estado |
|---|---|---|---|---|---|---|
| **v1** (Lovable) | **54** | **24** | **25** | **81** | **18.889** | Base elegida. Completa, nunca cobro |
| v3 | - | 20+ | - | - | - | Monorepo Node+Hono, backend verificado |
| v4 | - | hereda v3 | - | - | - | Reinicio del frontend, congelado 27/08 |

**v1 es la generacion mas completa de las cuatro**, no la mas chica. v3 y v4 no son sucesoras: son **podas** - al salir de Lovable se perdieron features en el camino. v4 declara conservar el backend de v3 y reconstruir solo el frontend.

### v1 tiene una deuda estructural que esta decision enfrenta

| Deuda | Detalle |
|---|---|
| Auth de Lovable | `@lovable.dev/cloud-auth-js` gestiona email/password + Google. **No corre local** |
| AI Gateway de Lovable | La IA llama al gateway de Lovable, no a un proveedor propio |
| Supabase como BaaS | Postgres + Auth + Realtime + Edge Functions + RLS + pgvector: un solo proveedor sostiene todo el backend |

**La ironia util:** v1 viola el principio que v1 misma declaro. Su `PRODUCT.md` dice *"el sistema es nuestro - no depende de un vendor para existir"*, y su propio `PLAN.md` tiene la **Fase 4 titulada "Migracion a stack propio - salir de Lovable"**. Nunca se hizo. Por eso esta generacion no es una copia de v1: es **la Fase 4 de v1, hecha y con alcance ampliado**.

### El precedente fabricado, materializado en archivos

v4 copio los 3 ADRs de v3 **de forma byte-identica** (mismo checksum `83022a062fdc` en ambos repos). De ahi que v4 heredara Node+Hono, SQLite y los tokens de Lovable **sin decidirlos**: no los eligio, los copio. Es la regla de `USER.md` (*"el precedente no es un motivo"*) manifestada en el arbol de archivos.

---

## Decision

### 1. Greenfield real: se re-decide todo

Ninguna decision tecnica de v3 ni v4 se hereda por existir. Cada una se toma o no se cita. El unico insumo de v3/v4 es **el aprendizaje**, no el stack.

### 2. v1 es la referencia funcional exclusiva

- **Inventario de features:** el de v1. Deben estar todas.
- **Especificacion funcional:** los specs as-built de OpenSpec de v1 (`openspec/specs/`: inbox, ai-copilot, billing-mp, thread-summary) son scenarios *WHEN/THEN* del comportamiento que ya funciona. No hay que inventar la especificacion; hay que **re-decidirla**.
- **Diseno:** la skill `UI-DESIGN-SKILL.md` de v1 documenta su sistema de tokens, escala de 8pt y reglas de contraste. Es insumo de diseno, no una decision de stack.

### 3. El alcance se amplia con el contable

v1 **no tiene nada contable**. El delta de esta generacion es CRM + contable para pymes, con modelo de planes. Ese delta **no es herencia**: es trabajo nuevo, y su alcance es la decision abierta mas importante del proyecto.

### 4. Planes se disenan antes de construir, no despues

v1 solo tenia `free` / `base` en `companies.plan`, sin limites, quotas ni features gateadas. Los planes **definen arquitectura** (limites por tenant, que se gatea, que se mide para cobrar). Disenarlos despues obliga a rehacer el modelo de datos.

---

## Lo que NO decide este ADR (pendiente de Gonzo)

Se registran explicitamente para que no se den por resueltas:

1. **Encuadre:** producto que busca facturar, o herramienta de uso propio. Cambia el criterio de exito y la vara de todo lo demas.
2. **Alcance contable de la v1:** nada / solo facturar la venta / facturacion + impuestos + cuentas corrientes / contabilidad completa.
3. **Nombre:** el nombre es el **ADR #1 del proyecto**. No se asume ninguno; las opciones discutidas (kanam-seller, kanam-management, kanam-copilot) tienen objeciones registradas. No hay ADR de convencion de nombres y la colision `kanam-fixer` / `kanam-fixer-v2` ya es evidencia del costo.
4. **App OAuth de MeLi:** reusar la de v1 (ya registrada en produccion, con sus permisos) o crear una nueva.
5. **Destino de los ADRs tecnicos de v3/v4** (archivar vs borrar): son de otros repos, requieren OK de Gonzo para pushear.
6. **La pregunta de demanda:** *¿por que esta vez va a tener usuarios?* Cuatro generaciones con trabajo tecnico bueno y **la demanda nunca probada**. v1 nunca cobro: su billing esta escrito y jamas fue operativo (secrets sin configurar, plan de preapproval sin crear en MP).

---

## Consecuencias

### Positivas
- La base elegida es la **mas completa** (v1), no la mas nueva. Se evita repetir la poda de features que hicieron v3 y v4.
- El precedente fabricado queda **nombrado y con evidencia** (checksum identico), asi que no se puede volver a heredar stack "porque ya estaba" sin chocar con este ADR.
- Los pendientes estan escritos. Un futuro "arranquemos con el stack" choca con la seccion de pendientes antes de repetir el patron de decidir tecnologia primero.

### Negativas
- **Greenfield sobre 18.889 lineas de referencia funcional** es mas trabajo que portar. Es deliberado: portar arrastraria las deudas de Lovable, que son exactamente el motivo por el que v1 se abandono.
- **El alcance es v1 x 2** (CRM + contable). El riesgo de "todo lo que podria requerir" es real y esta nombrado en la seccion de pendientes.
- Este ADR **queda incompleto por diseno** hasta que Gonzo responda los 6 pendientes.

### Fuera de alcance
- **No** se toca ni se borra ningun ADR del workspace (lo decide ADR-067).
- **No** se modifica el codigo de v1, v3 ni v4. Son referencia de lectura.
- **No** se define stack. Decide este ADR que se decide despues, con el nombre y el alcance primero.

---

## Alternativas consideradas

1. **Portar v1 y sacarle Lovable.** Rechazada: 25 Edge Functions de Deno + RLS de Supabase es una migracion de plataforma disfrazada de port, y arrastra las dependencias que causaron el abandono.
2. **Continuar v4** (que ya tiene identidad visual y pipeline A/B). Rechazada por instruccion explicita de Gonzo, y con fundamento medido: v4 es una poda de v1 - menos features, y su UI se diseno para un alcance que ahora cambia (CRM+contable, no solo bandeja MeLi).
3. **Construir sobre el backend verificado de v3.** Rechazada por instruccion explicita. Su backend **es** el de la linea Lovable portado a Node+Hono, con las mismas decisiones de modelo; y su ADR-002 (Node+Hono) es exactamente una decision tecnica que debe re-decider, no heredar.
4. **Empezar por el stack y el scaffolding.** Rechazada: es el movimiento que produjo cuatro generaciones sin validacion. Nombre, usuario y alcance van primero.
