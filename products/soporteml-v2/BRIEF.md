# Product Brief: SoporteML v2

**Fecha:** 2026-07-15
**Autor de la idea:** Gonzalo
**Producto de referencia:** SoporteML (v1, en Lovable Cloud)

---

## Raw Idea (Phase 0)

Gonzo quiere crear un producto igual en concepto a SoporteML — un CRM multi-tenant para vendedores de Mercado Libre — pero reconstruido desde cero, sin ninguna relación con Lovable ni su código actual. 

**Puntos clave:**
- No se reutiliza código de SoporteML v1. Solo se aprovecha el conocimiento adquirido (arquitectura, features, lecciones) y potencialmente se crean skills reutilizables de lo aprendido.
- Debe poder correr localmente desde el inicio (a diferencia de v1 que está atrapado en Lovable Cloud).
- El deploy viene después — primero se avanza a pasos calculados.
- Antes de escribir código, se debe definir el producto a la perfección (ciclo de Product Owner).

## Contexto conocido (de SoporteML v1)

Lo que ya sabemos del producto original:
- **Stack v1:** React+Vite+TS+Tailwind+shadcn/ui+Supabase+pgvector+OpenAI (en Lovable)
- **24 tablas, 25 Edge Functions, 54 migraciones SQL**
- **Features implementadas en v1:** Inbox centralizado, agrupación por hilo, SLA tracking, AI Copilot con RAG (pgvector), tono configurable, instrucciones custom, sugerencias CRM, billing con Mercado Pago (código existe pero NUNCA operativo), hilos unificados, resumen IA con cache, Analytics, Settings consolidado, hardening de seguridad
- **Problemas de v1:** atrapado en Lovable Cloud (no corre local), billing nunca funcionó real, depende de `@lovable.dev/cloud-auth-js`, secrets inaccesibles
- **Specs as-built escritos:** inbox, ai-copilot, billing-mp, thread-summary (4 specs en OpenSpec)
- **3 clientes en Beta** usando la versión de Lovable

## Respuestas de contexto (Phase 0 → cerrada)

1. **¿Para quién?** — vendedores de Mercado Libre (mismo target que v1)
2. **¿Qué problema resuelve?** — gestión de preguntas/mensajes/post-venta de vendedores MeLi
3. **¿Desde cero o existe?** — desde cero en código, con conocimiento profundo del dominio
4. **¿Reemplazo o convive?** — **REEMPLAZO TOTAL**. Los 3 clientes Beta migran a v2 cuando esté lista. v1 se deprecia.
5. **¿Qué tan "igual"?** — mismo concepto, mismas features, pero billing MP debe estar **realmente operativo** desde el inicio (en v1 nunca funcionó). Todo lo necesario, sin recortar.
6. **¿Stack?** — **create-stack-next** como base metodológica, pero **React + Vite** (no Next.js) para mantener compatibilidad con Lovable como opción de deploy futuro. No nos casamos con Lovable, pero no lo descartamos.
7. **¿Para usar o vender?** — ambos. Producto SaaS con billing, clientes reales desde día 1 (los 3 Beta heredados de v1).

---

## Notas

- Este producto reemplaza a SoporteML v1 a mediano/largo plazo
- Los 3 clientes Beta de v1 son candidatos naturales para migrar a v2
- **Stack decidido:** React + Vite + TS + Tailwind + shadcn/ui + Supabase + pgvector + OpenAI (mismo stack que v1, pero sin Lovable Cloud)
- **create-stack-next** provee la estructura metodológica (OpenSpec, ADRs, HANDOFF, CHANGELOG, AGENTS.md) pero el scaffold técnico será React+Vite, no Next.js
- Las skills que se pueden extraer del conocimiento de v1: specs, arquitectura multi-tenant, integración MeLi, RAG con pgvector, billing MP