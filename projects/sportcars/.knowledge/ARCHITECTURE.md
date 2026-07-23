# ARCHITECTURE — Sport Cars Jeep

## Resumen ejecutivo

Reemplazo del sitio brochure `sportcarsjeep.com.ar` por una plataforma de generación de leads para concesionario oficial Jeep/Ram. El sitio consume inventario de Mercado Libre vía API pública, sincroniza leads con Pilot CRM vía webhook, e incorpora un chatbot custom con base de conocimiento.

## Restricciones confirmadas (por Gonzo)

| Restricción | Implicancia |
|---|---|
| SaaS a 400 USD/mes (todo incluido) | El presupuesto debe cubrir hosting, dominio, base de datos, LLM del chatbot, y eventualmente servicios auxiliares |
| Chatbot custom | No usar Cliengo; construir uno propio con LLM + RAG |
| Reemplazo del sitio actual | sportcarsjeep.com.ar apunta al nuevo sitio; migración DNS al final |
| Hermana no tiene acceso admin de Pilot | No podemos depender de credenciales Pilot para el MVP; leads se capturan en Supabase y se sincronizan con Pilot más adelante o vía contacto humano |
| Sport Cars publica en MeLi directamente | El inventario de usados (y probablemente 0km) ya existe en MeLi; lo consumimos por API pública sin necesitar credenciales del seller |

## Stack tecnológico definitivo

| Capa | Tecnología | Justificación |
|---|---|---|
| **Frontend** | Next.js 15 + React 19 + TypeScript 5 | Stack de Gonzo, SSR/SSG para SEO de concesionario, App Router |
| **Estilos** | Tailwind CSS 4 + shadcn/ui | Velocidad, consistencia, dark mode opcional |
| **Backend serverless** | Next.js Route Handlers + Supabase Edge Functions | Para webhooks, proxy a APIs externas, chatbot streaming |
| **Base de datos / BaaS** | Supabase (PostgreSQL + PostgREST) | Auth opcional, almacenar leads, contenido del sitio, knowledge base del chatbot |
| **CMS** | Payload CMS 3 o Sanity | Contenido editorial (promociones, landing pages, blog) — a definir si vale la pena para MVP |
| **Chatbot** | Vercel AI SDK + OpenAI/DeepSeek/Claude API + RAG en Supabase | Bot custom con embeddings de la base de conocimiento |
| **Inventario** | Mercado Libre Search API pública | `/sites/MLA/search?nickname=sportcarsjeep` (sin auth) |
| **Lead pipeline** | Supabase (tabla `leads`) + webhook posterior a Pilot | Pilot no disponible en MVP por falta de credenciales admin |
| **Contacto humano** | WhatsApp API/click-to-chat + email | Derivación cuando el bot no resuelve o el usuario pide vendedor |
| **Hosting** | Vercel | Optimizado para Next.js, preview branches, edge functions |
| **Analytics** | Vercel Analytics + Plausible o PostHog | Métricas de conversión y engagement |

## Arquitectura de alto nivel (C4 — Contexto)

```
+-------------+     +---------------------+     +----------------------+
|   Comprador |---->|  Sport Cars Web     |---->|  Mercado Libre API   |
|  (visitante)|     |  (Next.js + Vercel) |     |  (inventario usados) |
+-------------+     +----------+----------+     +----------------------+
                               |
                               v
                    +----------+----------+
                    |  Supabase           |
                    |  - leads            |
                    |  - knowledge base   |
                    |  - analytics/events |
                    +----------+----------+
                               |
                               v
                    +----------+----------+
                    |  Chatbot (AI SDK)   |
                    |  + RAG embeddings   |
                    +----------+----------+
                               |
                               v
                    +----------+----------+
                    |  WhatsApp / Email   |
                    |  (derivación humana)|
                    +---------------------+

[Post-MVP]
Sport Cars Web ----> Pilot CRM API (lead creation webhook)
                      - app token + sub origen + company_code
```

## Arquitectura de contenedores

```
┌─────────────────────────────────────────┐
│         Vercel Edge / Node              │
│  ┌─────────────────────────────────┐    │
│  │ Next.js App Router              │    │
│  │  ├─ Pages (RSC + Client comps)  │    │
│  │  ├─ /api/leads (POST)           │    │
│  │  ├─ /api/chat (streaming)       │    │
│  │  ├─ /api/meli/inventory (GET)   │    │
│  │  └─ /api/webhooks/*             │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │ Supabase Edge Functions       │    │
│  │  (respaldo/proxy si hace falta)│   │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│           Supabase Cloud                │
│  ┌───────────────┐  ┌──────────────┐   │
│  │ PostgreSQL    │  │ Auth (opc.) │   │
│  │  - leads      │  │ Row Level     │   │
│  │  - kb_chunks  │  │ Security      │   │
│  │  - events     │  └──────────────┘   │
│  │  - vehicles   │                     │
│  └───────────────┘                     │
└─────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────┐      ┌──────────────┐
│ Mercado Libre │      │ OpenAI/      │
│ Search API    │      │ DeepSeek/    │
│ (pública)     │      │ Claude API   │
└──────────────┘      └──────────────┘
```

## Decisiones arquitectónicas clave

### 1. Pilot CRM: defer, no bloquear
- **Situación:** No tenemos credenciales admin. La hermana es vendedora.
- **Decisión:** El MVP guarda leads en Supabase. Tan pronto como alguien con acceso admin (dueño, gerente, o contacto de Pilot) nos dé el app token + sub origen, agregamos webhook a Pilot en horas.
- **Beneficio:** El sitio empieza a funcionar y generar valor sin depender de acceso interno privilegiado.
- **Riesgo:** Duplicación temporal de trabajo (lead en Supabase + manual en Pilot). Mitigación: panel simple para exportar leads a CSV o enviar a WhatsApp del vendedor.

### 2. Inventario desde Mercado Libre (API pública)
- **Situación:** Sport Cars publica directamente en MeLi y eso viaja a Pilot.
- **Decisión:** Consumimos inventario desde `/sites/MLA/search?nickname=sportcarsjeep` o `seller_id` sin autenticación.
- **Beneficio:** Stock real, sin integración privada, sin depender de credenciales.
- **Riesgo:** MeLi puede rate-limitar. Mitigación: cache en Supabase con revalidación cada 15-30 minutos.

### 3. Chatbot custom con RAG
- **Situación:** Gonzo quiere chatbot propio; no quiere Cliengo.
- **Decisión:** Vercel AI SDK + LLM API + embeddings en Supabase (pgvector). Base de conocimiento cargada manualmente al inicio con specs, precios referenciales, preguntas frecuentes, políticas del concesionario.
- **Beneficio:** Control total, no costo de SaaS de terceros, se adapta a Sport Cars.
- **Riesgo:** Costo de LLM y curva de mantenimiento. Mitigación: prompt caching, modelos baratos (DeepSeek/gpt-4o-mini), limitar conversación.

### 4. No CMS para MVP (a menos que sea necesario)
- **Situación:** Contenido inicial es pequeño (modelos, sucursales, FAQs).
- **Decisión:** Hardcodear/JSON inicial. Si el contenido crece o Sport Cars quiere editar promociones, se agrega Payload CMS o Sanity en Fase 2.
- **Beneficio:** Menor complejidad, menos costo, más rápido.

### 5. Next.js como full-stack
- **Decisión:** Todas las APIs (leads, chat, MeLi proxy) viven en Route Handlers de Next.js, no backend separado.
- **Beneficio:** Menos infraestructura, deploy simple en Vercel, edge caching.
- **Riesgo:** Acoplamiento. Mitigación: mantener lógica de negocio desacoplada en `lib/services/`.

### 6. WhatsApp como derivación humana
- **Decisión:** El chatbot deriva a WhatsApp del vendedor cuando el usuario lo pide o la confianza del bot es baja.
- **Beneficio:** No necesitamos WhatsApp Business API para empezar; click-to-chat es gratis e instantáneo.

## Patrones de diseño

- **Hexagonal / Ports & Adapters:** `lib/services/` para adapters externos (MeLi, Pilot, LLM, WhatsApp). El dominio no depende de implementaciones.
- **Repository pattern:** Acceso a Supabase encapsulado en `lib/repositories/`.
- **Server Components por defecto; Client Components para interacción:** Chatbot, formularios, filtros de inventario.
- **Streaming para chat:** Vercel AI SDK `useChat`.

## Esquema de datos (resumen)

Ver `DATA_MODEL.md` para el detalle completo.

Entidades principales:
- `leads` — contactos capturados del sitio
- `knowledge_chunks` — chunks de la base de conocimiento para RAG
- `events` — eventos de analytics (vista de página, clic, conversación)
- `vehicles` — cache local de inventario MeLi
- `conversations` — historial de chatbot

## Integraciones

### Mercado Libre
- Endpoint: `GET https://api.mercadolibre.com/sites/MLA/search?nickname=sportcarsjeep`
- Respuesta: listings activos con título, precio, imágenes, permalink, atributos
- Rate limit: típico de MeLi; cachear en Supabase
- Categoría probable: `MLA1744` (Autos y Camionetas) o similar

### Pilot CRM (post-MVP)
- Endpoint: `POST https://<dominio_pilot>/pilot/leadcreation/webhook`
- Body: `{ id, otros_datos }` según API encontrada
- Auth: app token + sub origen + company_code
- Se agrega en cuanto se consigan credenciales

### LLM (chatbot)
- Proveedor: **Ollama local / DeepSeek API** (infraestructura propia de Gonzo)
- Vía Vercel AI SDK
- Costo target: ~0-30 USD/mes (casi cero si Ollama local, bajo si DeepSeek API)
- **Nota:** como Gonzo cubre el LLM con su propia infraestructura, el presupuesto de 300 USD/mes al cliente se aliviana significativamente

## Seguridad

- Supabase Row Level Security (RLS) activado en todas las tablas
- API routes validan inputs con Zod
- Secrets en Vercel Environment Variables (no en repo)
- No exponer keys de LLM ni Supabase service role al cliente
- Rate limiting en endpoints de leads y chat (Vercel KV o Upstash)

## Performance / SEO

- Next.js App Router con SSR para páginas de modelos y listings
- Sitemap.xml generado automáticamente
- Open Graph por vehículo/modelo
- Imágenes con Next.js Image + CDN de MeLi
- Core Web Vitals target: LCP < 2.5s, CLS < 0.1

## Presupuesto estimado mensual (300 USD)

| Ítem | Costo estimado USD/mes |
|---|---|
| Vercel Pro + Analytics | ~20 |
| Supabase Pro (si escala) | ~25 |
| Dominio + DNS | ~2 |
| Ollama local / DeepSeek API | ~0-30 |
| Email/notificaciones (Resend/Postmark) | ~0-10 |
| Buffer / reserva | ~200-240 |
| **Total** | **~250-300** |

Si usás Ollama local en tu propia infraestructura, el costo de LLM es casi cero y el margen mejora mucho. El presupuesto de 300 USD es ajustado pero viable si el tráfico es moderado.

## Riesgos técnicos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| MeLi cambia/bloquea API pública | Media | Alto | Cache agresiva + fallback a contenido estático |
| Costo de LLM se dispara | Media | Medio | Limitar conversaciones, usar modelos baratos, caching |
| No se consiguen credenciales Pilot | Media | Medio | MVP funciona sin Pilot; leads en Supabase + exportación manual |
| Guidelines de Stellantis limitan diseño | Baja | Medio | Mantener logos/colores oficiales, usar fotos de marca |
| Tráfico bajo → pocos leads | Alta | Bajo | El sitio también sirve como carta de presentación digital |

## Próximos pasos (0.2 → Go/No-Go)

1. Gonzo valida stack y presupuesto
2. Confirmar si se puede usar el mismo dominio (acceso a DNS de sportcarsjeep.com.ar)
3. Obtener `nickname`/seller_id de MeLi de Sport Cars
4. Confirmar proveedor de LLM
5. Escribir OpenSpec formal y ADRs
6. Definir epics y tasks en ROADMAP.md
7. Decisión Go/No-Go