# BRIEF.md — Quedamos

> App PWA para armar salidas de desconocidos con matching por personalidad.
> Inspirada en Timeleft, pero abierta, transparente y gratuita.

## El Problema en Una Frase

Hacer amigos de adulto es difícil. Las apps de citas están saturadas, Meetup es frío, y los grupos de WhatsApp requieren conocer a alguien primero. No existe una plataforma gratuita y transparente que te conecte con desconocidos afines para salir en persona.

## La Solución

**Quedamos** es una PWA donde:
1. Completás un test de personalidad (Big Five reducido)
2. Explorás salidas disponibles (cine, bares, café, baile, almuerzo, caminata — lo que sea)
3. Ves un **compatibility score** con cada persona anotada
4. Te sumás a la que te cope
5. Un día antes recibís la confirmación con los detalles
6. Post-salida, dejás feedback anónimo que mejora el matching

## Diferenciación vs Timeleft

| Timeleft | Quedamos |
|---|---|
| Matching automático y opaco | Matching semi-automático, score visible |
| Solo miércoles, solo cenas | Cualquier día, cualquier actividad |
| Depende de restaurantes partners | Cualquier lugar público |
| Pago por cena (~$12-15 USD) | Gratuito |
| Código cerrado | Código visible (licencia restrictiva) |
| VC-backed, presión de crecimiento | Comunitario, sin presión |

## Público Objetivo (Persona Primaria)

**Santiago, 25-45, Buenos Aires**
- Profesional, labura remoto o híbrido
- Llegó a CABA hace unos años, su círculo social se achicó post-pandemia
- Quiere conocer gente nueva pero no sabe por dónde arrancar
- Está podrido de apps de citas
- Tiene hobbies (cine, música, birra artesanal, caminar) pero no con quién compartirlos

## Features Core (MVP)

1. **Auth** — registro con email/Google, apodo obligatorio, sin foto requerida
2. **Test de personalidad** — Big Five reducido (~20 preguntas), genera perfil de compatibilidad
3. **Explorar salidas** — feed de salidas disponibles con filtro por actividad, ubicación, fecha
4. **Compatibility score** — al ver una salida, muestra % de afinidad con cada participante
5. **Unirse a salida** — con un tap, quedás anotado
6. **Crear salida** — cualquier usuario puede crear una salida (actividad, lugar, fecha, cupo)
7. **Notificaciones push** — recordatorio 24h antes, cambios de último momento
8. **Feedback post-salida** — rating anónimo de compatibilidad con cada persona
9. **Perfil** — apodo, bio corta, actividades favoritas, score de confiabilidad

## Métricas de Éxito (MVP)

- **Retención Semana 1:** >40% de usuarios que crearon cuenta vuelven a la semana
- **Salidas concretadas:** >50% de las salidas creadas tienen al menos 3 asistentes
- **Feedback rate:** >60% de asistentes dejan feedback post-salida
- **NPS:** >40 (los usuarios recomiendan la app)

## Stack Asumido

- **Frontend:** Next.js 15 + Tailwind + shadcn/ui (PWA)
- **Backend:** Supabase (Auth, DB, Realtime, Edge Functions)
- **Matching engine:** Edge Function con algoritmo de compatibilidad Big Five + feedback loop
- **Notificaciones:** Supabase Realtime + Web Push API
- **Hosting:** Vercel o Coolify
- **Licencia:** Código visible con licencia restrictiva (BUSL o similar)

## Preguntas Abiertas (para Fase 0.2)

- ¿Algoritmo de matching exacto? (distancia coseno entre vectores Big Five + peso de feedback)
- ¿Moderación de salidas? (reportes, bloqueos, sistema de confianza)
- ¿Cómo se maneja el "no show"? (gente que se anota y no aparece)
- ¿Escalado a otras ciudades? (¿Buenos Aires primero y después?)
- ¿Notificaciones push en iOS PWA? (limitado, quizá necesitar service worker + push API)
