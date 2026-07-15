# Product Evaluation: SoporteML v2

**Fecha:** 2026-07-15

---

## Problem

Los vendedores de Mercado Libre manejan cientos de preguntas y mensajes diarios dispersos en la plataforma. No tienen un CRM centralizado, pierden ventas por tiempos de respuesta lentos, no pueden aplicar conocimiento de su producto a las respuestas, y no hay post-venta organizada. MeLi ofrece la infraestructura (APIs de preguntas, mensajes post-venta, webhooks) pero no las herramientas de gestión.

## Audience

Vendedores de Mercado Libre con volumen medio-alto (50+ publicaciones, múltiples preguntas/día). En Argentina hay cientos de miles de vendedores activos; el segmento target son los que ya tienen operación seria y necesitan herramientas profesionales. Estimación: decenas de miles en AR, más en resto LATAM.

## Existing solutions

| Competidor | Qué hace | Gap |
|---|---|---|
| **MeliBoost** | Gestión pedidos/preguntas/mensajes, IA, multi-cuenta | Generalista, no foca en CRM + KB personalizada |
| **MercadoBot** | 25 herramientas pre/post-venta, IA auto-respuestas | Bundle amplio pero poco profundo en CRM |
| **Parrot CRM** | CRM MeLi con IA (ChatGPT) | Solo México |
| **Dashlo** | Automatización mensajes, campañas, reseñas | Foco en automatización, no en gestión humana asistida |
| **Renata IA** | Agente IA para MeLi, auto-respuestas | Puro IA, sin gestión humana ni KB personalizada |
| **MercadoliderPro** | Automatización pre/post-venta | Similar a MercadoBot, bundle amplio |
| **SELLERP** | Órdenes, publicaciones, preguntas, posventa, publicidad, conciliación SAT | Más ERP que CRM, foca en operaciones no en relaciones |
| **Nova Smartselling** | IA preventa, respuestas automáticas | Solo preventa, sin post-venta ni CRM |

**Gap principal:** ninguno combina CRM real (gestión de relaciones, no solo mensajes) + KB personalizada con RAG + IA copiloto que asiste al humano (no lo reemplaza) + billing integrado LATAM. SoporteML v1 ya probó el concepto con 3 clientes Beta.

## Differentiation

1. **IA copiloto, no autopiloto** — la IA asiste al vendedor, no reemplaza su juicio. El vendedor mantiene control. Esto es diferenciador real: la mayoría de competidores apuestan por auto-respuesta total.
2. **KB personalizada con RAG** — cada empresa carga su conocimiento (fragilidad de producto, policies de envío, FAQ específicas) y la IA lo usa para responder mejor. Ningún competidor hace esto bien.
3. **Multi-tenant real** — cada empresa tiene su espacio aislado, su KB, su tono, sus operadores. No es una cuenta compartida.
4. **Stack propio, sin lock-in** — v1 probó que el concepto funciona. v2 lo reconstruye sin Lovable, corrible local, deployable en cualquier lado.
5. **Billing MP operativo** — v1 tenía el código pero nunca funcionó. v2 lo hace real desde el inicio. Suscripción mensual, integración nativa LATAM.

## Revenue model

- **Suscripción mensual via Mercado Pago Preapproval** — el mismo medio de pago que los vendedores ya usan. Sin fricción.
- **Pricing a definir** (sugerencia: tiers por volumen de preguntas/operadores, o plan único simple). v1 nunca cobró porque billing no funcionó.
- **3 clientes Beta heredados** — son los primeros pagadores cuando billing esté operativo.

## Technical feasibility

**Stack:** React + Vite + TS + Tailwind + shadcn/ui + Supabase + pgvector + OpenAI
**Estructura metodológica:** create-stack-next (OpenSpec, ADRs, HANDOFF, CHANGELOG, AGENTS.md)
**Complejidad:** alta — multi-tenant, realtime (Supabase Realtime), integración API MeLi (OAuth, webhooks), RAG con pgvector, billing con MP, Edge Functions en Deno.
**Lo que ya sabemos hacer (de v1):** todo. Los 4 specs as-built son la prueba. 24 tablas, 25 Edge Functions, 54 migraciones — ya pasamos por este problema.
**Lo que cambia en v2:** sin `@lovable.dev/cloud-auth-js` (Supabase Auth directo), sin Lovable Cloud (deploy propio), correr local desde día 1, billing realmente operativo.
**Estimación MVP:** 2-3 semanas (es una reconstrucción con conocimiento total del dominio, no un producto nuevo).

## Time to MVP

**2-3 semanas** para un MVP con: auth Supabase directa, multi-tenant, inbox, AI copilot con RAG, billing MP operativo, y sync con API MeLi. Es rápido porque el conocimiento del dominio es total — solo estamos reconstruyendo con mejor infraestructura.

## Strategic fit

- **Reemplaza SoporteML v1** — prioridad #1 del ecosistema Kanam, ahora con stack propio
- **Compite directamente con 8+ competidores** — el mercado está activo, hay demanda probada
- **3 clientes Beta listos para migrar** — revenue desde día 1 cuando billing funcione
- **create-stack-next como base** — come su propia comida (dogfooding), valida la herramienta
- **Skills extraíbles** — lo aprendido puede convertirse en skills reutilizables (integración MeLi, multi-tenant Supabase, RAG pgvector, billing MP)
- **KanamAI se integra** — el copiloto puede usar KanamAI para enrutamiento de modelos en el futuro

## Risks

| Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|
| API MeLi cambia o limita acceso | Alto | Baja-media | Mantear webhooks + polling fallback, seguir docs oficiales |
| Billing MP requiere plan preapproval aprobado | Medio | Media | Configurar plan en MP desde el inicio, no dejar para el final como v1 |
| Migración de 3 clientes Beta | Medio | Baja | v1 sigue en Lovable mientras v2 se estabiliza, migración gradual |
| Competidores agregan RAG/KB | Medio | Media | Velocidad de ejecución + foco en IA copiloto (no autopiloto) es diferenciador sostenible |
| Complejidad multi-tenant + realtime | Medio | Baja | Ya lo hicimos en v1, tenemos los specs y la experiencia |

## Verdict: 🟢 GO

### Conditions
- Ninguna. El concepto está probado (3 clientes Beta), el dominio es conocido (4 specs as-built), el stack es viable, y el mercado está activo con competidores que validan la demanda.

### Recommendation
Avanzar directamente a Phase 2 (Definition). El producto ya está validado — no necesitamos más evaluación. Definir el MVP con scope completo (todas las features de v1 + billing operativo), priorizar por dependencias técnicas, y arrancar el scaffold con create-stack-next en React+Vite.

**La prioridad #1 del ecosistema Kanam acaba de subir de nivel.**