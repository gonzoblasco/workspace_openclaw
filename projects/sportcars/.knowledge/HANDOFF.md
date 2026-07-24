# HANDOFF — Sport Cars Jeep

## Estado actual
**Fecha:** 2026-07-23 22:28 ART
**Fase completada:** Fase 4 — Chatbot con RAG
**Próxima fase:** Fase 5 — Leads, Test Drive y Cotizador (backend real)

## Resumen de lo hecho

### Fase 0 — Discovery (completa, modo detallado)
- BRIEF.md, DEFINITION.md, EVALUATION.md, ARCHITECTURE.md, DATA_MODEL.md, DESIGN.md, OPENSPEC.md, ROADMAP.md, TRACKER.md, STATUS.md
- 5 ADRs
- Presupuesto: 300 USD/mes, chatbot con Ollama/DeepSeek propio de Gonzo

### Fase 1 — Scaffold (completa)
- Repo: `github.com/gonzoblasco/sportcars`
- Next.js 15 + Tailwind + shadcn/ui (11 componentes)
- Biome configurado
- Vercel project linkeado + deploy
- Supabase local corriendo + schema SQL aplicado
- Types de base de datos generados

### Fase 2 — Contenido estático (completa)
- Layout con header (nav + CTAs) y footer
- Home con hero, modelos, usados, sucursales, CTA
- `/vehiculos` — grid de 6 modelos Jeep
- `/vehiculos/[slug]` — detalle con specs y CTAs
- `/sucursales` — 3 sucursales con info completa
- `/test-drive` — formulario de agendamiento
- `/contacto` — formulario + contacto directo
- `/cotiza-tu-usado` — formulario de evaluación
- SEO base con meta tags y sitemap

### Fase 3 — Inventario MeLi (completa)
- `lib/services/meli.ts` — searchByNickname, searchBySellerId, getItem, getItems
- `/api/meli/inventory` — API route con cache ISR 30 min
- `/usados` — grid con cards de usados reales, imágenes, precio
- Home con usados destacados sincronizados
- Fallback si MeLi falla

### Fase 4 — Chatbot con RAG (completa)
- Knowledge base con 20 chunks (modelos, sucursales, FAQs, políticas)
- Servicio RAG con keyword matching (preparado para pgvector)
- `/api/chat` con streaming (Vercel AI SDK + Ollama/DeepSeek)
- Widget flotante con sugerencias rápidas y streaming
- Configurable via env: LLM_BASE_URL, LLM_MODEL, LLM_API_KEY

## Decisiones clave
1. **Pilot CRM diferido al Post-MVP** — sin acceso admin, leads en Supabase
2. **Chatbot custom** — no Cliengo, con Ollama/DeepSeek propio de Gonzo
3. **Inventario via MeLi API pública** — sin credenciales del seller
4. **300 USD/mes** — modelo SaaS, LLM cubierto por Gonzo
5. **Proyecto finito** — se muestra en preview de Vercel, dominio real después

## URLs
- **Preview:** https://sportcars-pi.vercel.app
- **Supabase Studio local:** http://127.0.0.1:54323
- **Repo:** https://github.com/gonzoblasco/sportcars

## Pendiente para mañana

### Fase 5 — Leads, Test Drive y Cotizador (backend real)
- [ ] Conectar formularios a Supabase (tabla `leads`)
- [ ] API route `/api/leads` con validación Zod
- [ ] Notificación de leads por email/WhatsApp
- [ ] Panel simple `/admin/leads` protegido
- [ ] Exportación a CSV

### Post-MVP
- [ ] Captura de datos en chatbot (nombre/teléfono)
- [ ] Derivación a WhatsApp desde chatbot
- [ ] Persistencia de conversaciones en Supabase
- [ ] Migrar RAG a pgvector embeddings
- [ ] Integración Pilot CRM automática

## Cosas a confirmar
- **Seller ID/nickname de MeLi** — el que pasaste (`BM20260326092151`) parece ID de publicación, no de seller. Verificar.
- **Configurar LLM en Vercel** — setear `LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY` en environment variables de Vercel para que el chatbot funcione en producción.

## Archivos clave
- `src/lib/constants/site.ts` — datos del concesionario
- `src/lib/constants/knowledge-base.ts` — knowledge base del chatbot
- `src/lib/services/meli.ts` — integración MeLi
- `src/lib/services/rag.ts` — RAG del chatbot
- `src/components/shared/chat-widget.tsx` — widget de chat
- `src/app/api/chat/route.ts` — API de chat
- `src/app/api/meli/inventory/route.ts` — API de inventario
- `supabase/migrations/00001_initial_schema.sql` — schema de base de datos
- `projects/sportcars/.knowledge/` — documentación completa del proyecto
