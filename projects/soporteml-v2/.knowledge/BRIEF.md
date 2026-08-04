# BRIEF — SoporteML v2

> Fecha: 2026-08-03
> Estado: En planificación (Fase 1 arrancando)
> Decisores: Gonzo (PO/Arquitecto), Kanam (Arquitecta/Implementación)

---

## Qué es

SoporteML es una plataforma multi-tenant para que vendedores y equipos de Mercado Libre gestionen las preguntas de los compradores con ayuda de IA. Unifica el flujo fragmentado de soporte: preguntas dispersas, respuestas inconsistentes, tiempos lentos, poca trazabilidad, dificultad para operar varias empresas.

## Por qué v2 (motivación del rewrite)

La v1 fue construida en Lovable (React + Vite + TS + shadcn/ui + Supabase + Edge Functions en Lovable Cloud). Decisión estratégica: **salir de Lovable por completo y tener control total del stack**.

**Camino AB (adoptado):**
- **Fase 1 (ahora):** Frontend reescrito de cero con stack propio, consumiendo el backend actual (Supabase + Edge Functions que viven en Lovable Cloud y siguen funcionando). Sale de Lovable como editor/host de la UI.
- **Fase 2 (después):** Backend propio progresivo (Supabase Cloud propio + Node según convenga), migrando feature por feature hasta que nada dependa de Lovable. Al final, apagado de Lovable.

**Meta final:** todo bajo control de Gonzo. La combinación de ecosistemas (Supabase + Node) está permitida y es deseable — cada feature vive donde se hace mejor.

## Stack objetivo (Fase 1)

- Frontend: Vite + React + TypeScript + React Router + Tailwind + shadcn/ui
- Tooling: Biome (lint+format), simple-git-hooks (pre-commit), Vitest
- Metodología: OpenSpec specs, ADRs, CHANGELOG, .knowledge/ para memoria institucional
- Backend (Fase 1): consumir el Supabase existente vía `supabase.functions.invoke()` + RPCs + RLS

## Alcance del frontend (Fase 1)

**Conservar:**
- Auth (email/password + Google) + multi-company
- Inbox (tabs, agrupación por hilo, búsqueda, navegación por teclado)
- Copiloto IA con RAG (KB + contexto producto + source chips, tonos configurables)
- Autopilot (auto-respuesta con umbral de confianza configurable)
- Knowledge Base (artículos, chunking, búsqueda semántica, realtime)
- Integración Mercado Libre (OAuth, estado de conexión, sync)
- Analytics (KPIs, deltas, volumen, distribución, export CSV)
- Settings (2 paneles, autopilot, prompt/tono, modelo/RAG, equipo, plan, MeLi, danger zone)
- Templates, Customers (CRM liviano)

**Cortar (candidatos, no reconstruir en v2 inicial):**
- Admin multi-tenant (super admin)
- Catálogo de productos con enriquecimiento IA / detección de duplicados

> Nota: el corte es de Fase 1. Si se necesitan después, se agregan con specs propias.

## Restricciones duras del backend (heredadas de la v1, NO romper)

- `company_id` siempre se deriva de la DB (memberships), nunca del body del cliente.
- `user_belongs_to_company(company_id)` es el check estándar de membership.
- `currentCompanyId` sale de `memberships` (nunca de `profiles.company_id` — deprecated).
- RLS activo en todas las tablas por `company_id`.
- `meli_tokens` nunca se expone al frontend (solo RPC `get_meli_connection_status`).
- JWT validado manualmente en todas las Edge Functions.

## Decisiones abiertas (a resolver antes de escribir código)

1. ~~MCP de plataforma de Lovable~~ → Bloqueado (Lovable solo admite ChatGPT/Claude/Cursor/VS Code; OpenClaw no es partner aprobado). No es crítico: el objetivo es salir de Lovable, no editarlo.
2. Google OAuth: configurar credenciales propias de Gonzo en Supabase (requisito para salir de Lovable en login con Google).
3. Env vars frontend: `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`, `VITE_SUPABASE_PROJECT_ID` (valores locales, no commitear).
4. Nombre de repo/carpeta: `soporteml-v2` (la v1 queda como referencia/origen de verdad durante Fase 1).

## Métricas de éxito

- Fase 1: frontend v2 corriendo local contra backend real, con login (email/password) funcionando.
- Fase 2: al menos una feature (ej: Inbox) migrada a backend propio con datos reales.
- Meta final: cero dependencia de Lovable (UI + backend + secrets bajo control propio).
