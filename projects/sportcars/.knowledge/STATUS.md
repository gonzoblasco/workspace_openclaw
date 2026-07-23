# STATUS — Sport Cars Jeep

## Estado actual
Fase 0.2 de Product Discovery completada. Modo detallado activado. Esperando decisión de Gonzo para iniciar Fase 1 (Scaffold).

## Documentos listos
- BRIEF.md ✅
- DEFINITION.md ✅
- EVALUATION.md ✅
- ARCHITECTURE.md ✅
- DATA_MODEL.md ✅
- DESIGN.md ✅
- OPENSPEC.md ✅
- ROADMAP.md ✅
- TRACKER.md ✅
- ADRs ✅ (5 iniciales)

## Decisiones tomadas
1. SaaS a **300 USD/mes** todo incluido
2. Chatbot custom con LLM + RAG, corriendo en infraestructura propia de Gonzo (Ollama/DeepSeek)
3. Reemplazo del sitio actual (sportcarsjeep.com.ar), pero se muestra primero como **proyecto finito**
4. Integración Pilot CRM se difiere al Post-MVP por falta de acceso admin
5. Inventario via API pública de Mercado Libre
6. Stack: Next.js 15 + Tailwind + shadcn + Supabase + Vercel

## Bloqueos actuales
Ninguno técnico. Tareas pendientes de Gonzo:
- Obtener nickname/seller_id de Mercado Libre de Sport Cars
- Confirmar acceso al DNS de sportcarsjeep.com.ar (para reemplazo final)
- Confirmar guidelines de Stellantis

## Próximo hito
Fase 1 — Scaffold & Setup del proyecto.

## Última actualización
2026-07-23