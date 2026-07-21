# ADR-001: Stack Tecnológico

**Fecha:** 2026-07-21
**Contexto:** Elegir stack para una app web de gestión de consultorio psicológico. MVP de 2-3 semanas, un solo dev fullstack.

**Decisión:** Next.js 15 (App Router) + Supabase + Tailwind + shadcn/ui + WhatsApp Cloud API

**Opciones consideradas:**
- **React + Vite + Express:** más control pero más boilerplate. Next.js da más out-of-the-box (ruteo, SSR, API routes).
- **Supabase vs Firebase:** Supabase es SQL (mejor para datos relacionales como pacientes/sesiones/agenda), Postgres nativo, mejor DX con TypeScript.
- **WhatsApp API:** Meta Cloud API es la opción más directa. Twilio es alternativa pero más cara.

**Consecuencias:**
- Positivas: desarrollo rápido, stack que Gonzo ya domina, escalabilidad horizontal con Postgres.
- Negativas: WhatsApp API requiere aprobación de Meta (puede demorar días). Alternativa: arrancar con un SMS placeholder y agregar WhatsApp después.

**Estado:** Aceptado
