# HANDOFF — Sport Cars Jeep (actualización)

## Estado actual
**Fecha:** 2026-07-24 00:39 ART
**Fase completada:** Fase 5 — Leads, Test Drive y Cotizador (backend real)
**Próxima fase:** Fase 6 — QA e Integración (o lo que Gonzo decida)

## Resumen de lo hecho hoy

### Fase 0 — Discovery (completa)
### Fase 1 — Scaffold (completa)
### Fase 2 — Contenido estático (completa)
### Fase 3 — Inventario MeLi (completa)
### Fase 4 — Chatbot con RAG (completa)
### Fase 5 — Leads (completa)
- API `/api/leads` con validación Zod
- Formularios de contacto, test drive y cotizador conectados a Supabase local
- Panel `/admin/leads` con filtros, búsqueda y exportación CSV
- Env vars de Supabase configuradas en Vercel

## URLs
- **Preview:** https://sportcars-pi.vercel.app
- **Supabase Studio local:** http://127.0.0.1:54323
- **Panel admin:** https://sportcars-pi.vercel.app/admin/leads
- **Repo:** https://github.com/gonzoblasco/sportcars

## Pendiente
- Configurar LLM en Vercel para que el chatbot funcione en producción
- Obtener seller_id/nickname real de MeLi de Sport Cars
- Notificación automática de leads
- Migrar a Supabase cloud
- Autenticación en panel admin
