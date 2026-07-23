# ADR-004 — Next.js como plataforma full-stack sin backend separado

## Estado
Aceptado

## Contexto
El proyecto es un sitio web con interacción dinámica (chatbot, formularios, inventario externo) y necesita un backend para webhooks, APIs y persistencia. Se busca minimizar infraestructura y costo operativo.

## Decisión
Usar Next.js como plataforma full-stack:
- Frontend con App Router (RSC + Client Components)
- Route Handlers (`app/api/*`) para APIs
- Server Actions para mutaciones simples
- Vercel como hosting

## Consecuencias

### Positivas
- Un solo repo, un solo deploy.
- Menor costo y complejidad que tener frontend + backend separados.
- Optimizado para SSR/SSG y SEO.
- Escalado automático en Vercel.

### Negativas
- Acoplamiento de frontend y backend.
- Lógica de negocio puede mezclarse con UI si no se organiza bien.
- Vercel tiene límites en execution time para funciones (pero suficientes para este caso).

## Mitigaciones
- Arquitectura limpia: `lib/services/`, `lib/repositories/`, `lib/domain/`.
- No colocar lógica de negocio en componentes de UI.
- Supabase Edge Functions como respaldo si alguna tarea excede límites de Vercel.

## Alternativas consideradas
1. **Next.js frontend + Express/NestJS backend:** más poderoso pero más costoso y complejo. Rechazado por MVP.
2. **Astro + backend separado:** buen SEO pero más fricción para interacciones dinámicas. Rechazado.
3. **WordPress headless:** el sitio actual ya es WordPress y no satisface. Rechazado.