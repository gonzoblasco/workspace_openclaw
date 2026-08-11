# ADR-002 - Runtime del backend local

> **Estado:** ACEPTADO (2026-08-11)
> **Contexto:** SoporteML v3, Fase 0 (definición). Decisión de arquitectura que desbloquea el scaffold.

---

## Contexto

SoporteML v3 se construye con independencia de vendor: la primera alpha corre 100% local (SQLite + backend local), sin servicios cloud. Las edge functions del backend actual (25 funciones) corren en Supabase Edge Functions, que usan **Deno** como runtime.

Necesitamos decidir en qué runtime recrear esas edge functions para el backend local, que luego evolucionará a producción.

## Decisión

**Usar Node.js + Hono** para el backend local.

## Opciones consideradas

| Opción | Port desde Supabase | Ecosistema | Monorepo | Veredicto |
|---|---|---|---|---|
| **Deno** | Casi copy-paste (mismo runtime) | Menor que Node | Dos runtimes (Deno + Node/Vite) | Port directo, pero dos runtimes |
| **Node + Hono** ✅ | Reescribir patrón (funciones → handlers) | Enorme | Un solo runtime (Node) | **Elegido** |
| **Node + Fastify** | Igual que Hono | Enorme | Un solo runtime | Más pesado que Hono |
| **Next API routes** | Server web pesado, otro paradigma | Enorme | Un solo runtime | Overkill, descartado |

## Razones

1. **Un solo runtime en el monorepo.** El frontend es Vite/React/TS (Node). Con Node en el backend, todo el monorepo es Node/TS: una sola toolchain, un solo `node_modules`, un solo ecosistema de tooling (Biome, tests). Con Deno habría dos runtimes conviviendo, más fricción de la que vale.

2. **Hono es el framework correcto.** Liviano, tipado, y **tiene adaptador para Deno** — si mañana queremos deployar en Deno Deploy, el mismo código Hono corre ahí. No nos encerramos en Node.

3. **El "copy-paste" de Deno es menos real de lo que parece.** Las edge functions de Supabase no son solo Deno — usan `supabaseAdmin`, `@supabase/functions-js`, y dependen de la infraestructura de Supabase (RLS, PostgREST, pg_cron). Ese código no se copia tal cual a un backend local con SQLite — hay que reescribir la capa de datos igual. La ventaja de "copy-paste" de Deno se diluye cuando el backend local no usa Supabase.

4. **Ecosistema Node más grande** para lo que vamos a necesitar: web scraping (ficha proactiva), OAuth, integraciones. Node tiene librerías maduras; Deno menos.

## Consecuencias

- **Positivas:** un solo runtime, ecosistema completo, Hono portable a Deno si hace falta, framework liviano.
- **Negativas:** hay que reescribir el patrón de edge functions (funciones sueltas → handlers Hono), no es copy-paste.
- **Riesgo:** si a futuro decidimos que Deno Deploy es la plataforma ideal, el código Hono migra con adaptador (bajo costo).

## Alternativa futura

Si en la Fase 3 (decisión de despliegue) hay razones válidas para Deno Deploy, el código Hono migra con el adaptador de Deno. No se descarta, solo no es el default.

## Referencias

- `PRODUCT.md` - principio de independencia de vendor.
- `BACKEND-REFERENCE.md` - edge functions actuales (Deno/Supabase).
- `ROADMAP.md` - Fase 0 (definición) y Fase 3 (despliegue).
