# ROADMAP — SoporteML v2

> Fecha: 2026-08-03
> Estado: Fase 1 en curso

---

## Fase 1 — Frontend propio, backend existente

**Objetivo:** Frontend v2 corriendo local contra el backend real (Supabase en Lovable Cloud). Salir de Lovable como editor/host de la UI.

### M1 — Fundación
- [ ] Scaffold Vite + React + TS + Tailwind + shadcn/ui
- [ ] Biome + simple-git-hooks (pre-commit: lint → test → build)
- [ ] Cliente Supabase + tipos de DB
- [ ] Auth (email/password) + multi-company + guards de ruta
- [ ] Layout app (sidebar, header, company switcher, dark/light)

### M2 — Inbox (núcleo del producto)
- [ ] Tabs (Pendientes, Publicadas, Auto IA, Archivadas)
- [ ] Lista de preguntas + agrupación por hilo (buyer+producto)
- [ ] Detalle de pregunta + respuesta sugerida por IA
- [ ] Búsqueda + navegación por teclado

### M3 — Copiloto IA + Autopilot
- [ ] Copiloto con RAG (KB + contexto producto + source chips)
- [ ] Tonos configurables
- [ ] Autopilot: auto-respuesta con umbral de confianza

### M4 — Knowledge Base
- [ ] Lista de artículos + creación/edición
- [ ] Chunking + embeddings + búsqueda semántica
- [ ] Realtime sobre estado de procesamiento

### M5 — Integración MeLi + Analytics + Settings + Templates + Customers
- [ ] Estado de conexión MeLi (RPC, 4 niveles de salud)
- [ ] Analytics (KPIs, deltas, volumen, distribución, export CSV)
- [ ] Settings (2 paneles)
- [ ] Templates, Customers

### M6 — Pulido + verificación
- [ ] Tests en componentes críticos (Inbox, QuestionCard, AICopilotPanel)
- [ ] Validación visual (screenshots + evaluación crítica)
- [ ] Deploy frontend v2 a producción apuntando al backend real

---

## Fase 2 — Backend propio progresivo

**Objetivo:** Migrar feature por feature a un backend bajo control de Gonzo, hasta apagar Lovable.

### B1 — Fundación backend
- [ ] Cuenta Supabase Cloud propia (plan free) — crear
- [ ] Migrar schema (54 migraciones) en limpio (datos pueden limpiarse)
- [ ] Configurar secrets propios (OpenAI, MP, MeLi, Google OAuth)
- [ ] Decidir por feature: Supabase Edge Function vs Node (Fastify/Express)

### B2+ — Migración incremental
- [ ] Auth → Supabase propio
- [ ] Inbox/questions → propio
- [ ] Copiloto/RAG → propio
- [ ] Autopilot → propio
- [ ] KB → propio
- [ ] MeLi (OAuth + webhook + sync) → propio
- [ ] Billing MP → propio (si aplica)
- [ ] Reconfigurar apps OAuth/webhooks MeLi y MP al nuevo dominio

### Bf — Apagado de Lovable
- [ ] Verificar cero dependencia
- [ ] Cerrar/deprecar proyecto Lovable

---

## Decisiones técnicas pendientes (para Fase 2)
- Supabase Cloud propio vs self-hosted → decidido: Cloud (plan free)
- Edge Functions vs Node por feature → evaluar en cada migración (B1)
- Auth: Supabase Auth vs JWT propio → decidir en B1 (default: Supabase Auth)
