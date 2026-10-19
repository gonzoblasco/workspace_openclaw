# ADR-011: Next.js como Plataforma Full-Stack por Defecto

**Estado:** Aceptado
**Fecha:** 2026-08-05
**Actualizado:** 2026-10-15
**Decisores:** Gonzo / Kanam
**Origen:** workspace (extraído de evaluación sportcars, generalizado)

## Contexto

Proyectos web con interacción dinámica (chatbots, formularios, APIs externas, paneles admin) necesitan backend para webhooks, APIs y persistencia. La pregunta recurrente es si separar frontend y backend en repos/proyectos distintos o unificarlos.

## Decisión

Usar **Next.js (App Router)** como plataforma full-stack por defecto para proyectos web de complejidad media:
- Frontend: React Server Components + Client Components
- APIs: Route Handlers (`app/api/*`)
- Mutaciones simples: Server Actions
- Hosting: Vercel (u otra plataforma que soporte Next.js)

## Consecuencias

### Positivas
- Un solo repo, un solo deploy
- Menor costo y complejidad que frontend + backend separados
- Optimizado para SSR/SSG y SEO
- Escalado automático en Vercel

### Negativas
- Acoplamiento de frontend y backend
- Lógica de negocio puede mezclarse con UI si no se organiza bien
- Vercel tiene límites en execution time para funciones

## Mitigaciones
- Arquitectura limpia obligatoria: `lib/services/`, `lib/repositories/`, `lib/domain/`
- No colocar lógica de negocio en componentes de UI
- Supabase Edge Functions como respaldo si alguna tarea excede límites de Vercel

## Alternativas consideradas
1. **Next.js frontend + Express/NestJS backend:** más potente pero más costoso y complejo. Para proyectos que ya anticipan necesitar separación.
2. **Astro + backend separado:** buen SEO pero más fricción para interacciones dinámicas.
3. **WordPress headless:** cuando el sitio actual ya es WordPress y no satisface.

## Alcance
Aplica a proyectos web de complejidad media donde el backend **no requiere** su propio ciclo de vida, escalado independiente, o equipo separado. Para proyectos donde el backend **es el producto** (API-first), reconsiderar.

## Referencias
- [ADR-012](./ADR-012-supabase-baas.md): BaaS recomendado para el stack
- [ADR-020](./ADR-020-vite-default-bundler.md): Vite para proyectos no-Next.js
- [ADR-048](./ADR-048-shadcn-radix-stack-ui.md): Capa de UI sobre Next.js