# ADR-011: Nextjs Fullstack Platform

**Status:** Aceptado
**Origen:** sportcars ADR-004
**Fecha:** 2026-08-05

## Contexto

Proyectos web con interaccion dinamica (chatbots, formularios, APIs externas) necesitan un backend para webhooks, APIs y persistencia. La pregunta es si separar frontend y backend en repos/proyectos distintos o unificarlos.

## Decision

Usar Next.js como plataforma full-stack:
- Frontend con App Router (RSC + Client Components)
- Route Handlers (`app/api/*`) para APIs
- Server Actions para mutaciones simples
- Vercel como hosting (o cualquier plataforma que soporte Next.js)

## Consecuencias

### Positivas
- Un solo repo, un solo deploy.
- Menor costo y complejidad que tener frontend + backend separados.
- Optimizado para SSR/SSG y SEO.
- Escalado automatico en Vercel.

### Negativas
- Acoplamiento de frontend y backend.
- Logica de negocio puede mezclarse con UI si no se organiza bien.
- Vercel tiene limites en execution time para funciones.

## Mitigaciones
- Arquitectura limpia: `lib/services/`, `lib/repositories/`, `lib/domain/`.
- No colocar logica de negocio en componentes de UI.
- Supabase Edge Functions como respaldo si alguna tarea excede limites de Vercel.

## Alternativas consideradas
1. **Next.js frontend + Express/NestJS backend:** mas poderoso pero mas costoso y complejo. Recomendado para proyectos que ya anticipan necesitar separacion.
2. **Astro + backend separado:** buen SEO pero mas friction para interacciones dinamicas.
3. **WordPress headless:** cuando el sitio actual ya es WordPress y no satisface.

## Notas

Esta decision aplica a proyectos web de complejidad media donde el backend no requiere su propio ciclo de vida, escalado independiente, o equipo separado. Para proyectos donde el backend es el producto (API-first), reconsiderar.
