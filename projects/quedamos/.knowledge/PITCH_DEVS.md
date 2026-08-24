# Quedamos — Hagamos una app para hacer amigos de adulto

> TL;DR: Una app PWA gratuita para armar salidas de desconocidos con matching por personalidad. Como Timeleft, pero abierta, transparente, y sin pagar. Busco devs copados que se sumen al equipo.

---

## El problema

Hacer amigos de adulto es una paja.

Post-pandemia, la soledad es crisis de salud pública (la OMS, el US Surgeon General, todos lo dicen). Llegás a los 30, tu círculo se achicó, la gente se fue del país, y de repente tus únicos planes sociales son "¿pedimos delivery y vemos algo en Netflix?"

Las apps de citas están saturadas. Meetup es frío y corporativo. Los grupos de WhatsApp requieren conocer a alguien primero. Timeleft existe pero:
- Pagás ~$15 USD por cena
- Solo miércoles, solo cenas
- No sabés con quién vas hasta último momento
- El algoritmo es caja negra

No hay una plataforma **gratuita, transparente y pensada para hacer amigos de verdad**.

## La idea

**Quedamos** es una app donde:

1. Completás un test corto de personalidad
2. Explorás salidas disponibles — cine, bares, café, baile, almuerzo, caminata, lo que sea
3. Ves un **score de compatibilidad** con cada persona anotada
4. Te sumás a la que te cope
5. Un día antes recibís un aviso con los detalles
6. Post-salida, dejás feedback anónimo que mejora el algoritmo

Sin swipes, sin fotos obligatorias, sin pagar. Solo gente con ganas de conocer gente.

## Lo que la hace distinta

| Timeleft | Quedamos |
|---|---|
| Matching opaco (no sabés con quién vas) | Matching transparente (score visible) |
| Solo miércoles, solo cenas | Cualquier día, cualquier actividad |
| Pagás por cena | Gratis |
| Código cerrado | Código visible |
| VC-backed, presión de crecimiento | Proyecto de amigos, sin presión |

## ¿Para quién?

Para cualquiera de 20 a 45 que quiera ampliar su círculo social sin el peso de las apps de citas. Gente que labura remoto, que se mudó de ciudad, que extraña cuando conocer gente era natural.

## Stack

- **Frontend:** Next.js 15 + Tailwind + shadcn/ui (PWA — funciona en celular sin pasar por app stores)
- **Backend:** Supabase (auth, DB, realtime, edge functions)
- **Matching engine:** Edge Function con Big Five + feedback loop
- **Hosting:** Vercel / Coolify
- **Licencia:** Código visible con licencia restrictiva (no comercial sin permiso)

## Estado actual

Product discovery completo (BRIEF, DEFINITION, EVALUATION). Pasando a fase de arquitectura y plan de ataque. MVP estimado en 3-4 semanas de desarrollo enfocado.

## ¿Qué busco?

Devs copados que quieran sumarse a construir algo con propósito. No busco socios, no busco inversión, busco **gente con ganas de hacer**.

Especialmente si te copa:
- React / Next.js / TypeScript
- Supabase / backend en general
- UI/UX (la app tiene que ser LINDA, no funcional nomás)
- Algoritmos de matching / ML básico
- O simplemente tenés ganas de participar y opinar

No importa si nunca hiciste mobile. Es PWA, es web. Si sabés React, ya sabés.

## ¿Cómo sumarse?

Hablame y te paso el link al repo (cuando exista) y al grupo de WhatsApp/Telegram/Discord donde la vamos a charlar.

No hay compromiso, no hay deadlines de corporación. Es un proyecto para hacer algo copado entre amigos.

---

**Quedamos.** Nos vemos ahí.
