# Roadmap: SoporteML v2

**Fecha:** 2026-07-15
**Fase:** 3 — Roadmap & Plan

---

## Stack técnico confirmado

- **Frontend:** React 19 + Vite + TypeScript + Tailwind v4 + shadcn/ui
- **Backend:** Supabase (Postgres + Auth + Realtime + Edge Functions/Deno + Storage)
- **IA:** OpenAI (text-embedding-3-small + GPT para copiloto + clasificación)
- **Vectores:** pgvector en Supabase
- **Billing:** Mercado Pago Preapproval API
- **Integración:** Mercado Libre API (OAuth, preguntas, mensajes, webhooks)
- **Metodología:** create-stack-next (OpenSpec, ADRs, HANDOFF, CHANGELOG, AGENTS.md)
- **Deploy:** local primero (Supabase CLI + Vite dev server), producción después

---

## Phase 1: Foundation — 2-3 días

**Goal:** proyecto scaffolded con estructura metodológica, auth multi-tenant funcionando, Supabase configurado local.

**Deliverable:** app corre local, registro/login funciona, empresas aisladas con RLS.

**Tasks:**
1. Scaffold React+Vite+TS con create-stack-next (adaptado a Vite, no Next.js)
2. Configurar Tailwind v4 + shadcn/ui
3. Configurar Supabase CLI local (migraciones, Edge Functions, tipos)
4. Diseñar esquema DB multi-tenant (companies, users, memberships, roles) — basado en v1 pero simplificado
5. Implementar auth Supabase directo (registro, login, reset password)
6. RLS policies multi-tenant (todo aislado por company_id)
7. Setup AGENTS.md, HANDOFF.md, CHANGELOG.md, ADRs en el repo
8. OpenSpec init + primer spec: auth-multi-tenant

**Demo:** usuario se registra, crea empresa, hace login, ve dashboard vacío.

**Skill:** web-app-builder (scaffold + domain structure)

---

## Phase 2: MeLi Integration — 3-4 días

**Goal:** cuenta MeLi conectada, preguntas sincronizándose, webhooks operativos.

**Deliverable:** inbox vacío pero con preguntas reales de MeLi appearing via webhook + realtime.

**Depends on:** Phase 1

**Tasks:**
1. OAuth flow con Mercado Libre (redirect, callback, token storage)
2. Edge Function: sync-meli-questions (poll + webhook handler)
3. Edge Function: meli-webhook (receiver de eventos de MeLi)
4. Tablas: questions, products, buyers (migraciones)
5. Supabase Realtime en questions (postgres_changes)
6. Polling fallback (por si webhooks fallan)
7. OpenSpec spec: meli-integration

**Demo:** conectar cuenta MeLi, ver preguntas reales appearing en realtime.

**Skill:** sdd-brownfield (spec) + agent-dispatcher (implement)

---

## Phase 3: Inbox UI — 3-4 días

**Goal:** inbox completo con todas las vistas, filtros, agrupación, SLA, navegación.

**Deliverable:** inbox funcional — preguntas agrupadas por hilo, filtros por estado, búsqueda, SLA tracking, navegación teclado.

**Depends on:** Phase 2

**Tasks:**
1. Layout dos columnas (lista + detalle)
2. GroupedQuestionCard — agrupación por buyer_id + product_id
3. Tabs: Pendientes, Por vencer, Publicadas, Auto IA, Archivadas
4. Búsqueda client-side en tiempo real
5. SLA tracking (campos received_at, answered_at, sla_deadline)
6. Navegación por teclado (j/k, enter, esc)
7. Priority Inbox — hilos que requieren atención humana (requires_human = true)
8. Absorción cross-bandeja (fetchPriorityThreadKeys)
9. Badge "N (M urg.)" en grouped cards
10. OpenSpec spec: inbox

**Demo:** inbox con datos reales, navegable con teclado, filtros funcionando.

**Skill:** agent-dispatcher (implement) + agent-review (gate)

---

## Phase 4: Knowledge Base UI + RAG — 2 días

**Goal:** KB ya auto-poblada en Phase 2, ahora damos UI de gestión + el RAG funciona para el copiloto.

**Deliverable:** admin ve y edita KB auto-generada, crea artículos nuevos, el copiloto los usa al generar borradores.

**Depends on:** Phase 2 (KB auto-poblada)

**Tasks:**
1. Tablas: kb_articles, kb_chunks (con pgvector) — kb_articles ya tiene datos auto-generados
2. Edge Function: embed-kb-chunk (text-embedding-3-small → pgvector) — corre también en batch para los auto-generados
3. RPC: match_kb_chunks (cosine distance, umbral 0.45, top 5)
4. UI: Settings → Knowledge Base (listado con badge "Auto" vs "Manual", CRUD de artículos, editar auto-generados)
5. Split de texto en chunks automático
6. RLS: KB aislada por company_id
7. Re-embed automático cuando se edita un artículo
8. OpenSpec spec: knowledge-base

**Demo:** ver KB auto-generada, editar un artículo, crear uno nuevo, ver que el copiloto lo usa.

**Skill:** agent-dispatcher (implement)

---

## Phase 5: AI Copilot — 3-4 días

**Goal:** copiloto genera borradores con RAG + contexto CRM, tono configurable, instrucciones custom.

**Deliverable:** vendedor abre pregunta, copiloto sugiere respuesta con KB + contexto, edita, envía.

**Depends on:** Phase 3 (inbox UI) + Phase 4 (KB)

**Tasks:**
1. Edge Function: ai-copilot (JWT auth, company_id server-side)
2. System prompt con contexto CRM (support_summary, key_points, shipping_notes, faq_bullets, do_not_say)
3. RAG: embed pregunta → match_kb_chunks → incluir en prompt
4. Response JSON estructurado: summary, draft, missing_data, kb_sources, crm_suggestions
5. UI: panel del copiloto al lado del detalle de pregunta
6. Tono configurable (formal, casual, directo — por empresa)
7. Instrucciones custom del vendedor (textarea en Settings)
8. Manejo de errores: sin API key → respuesta manual; sin KB → solo CRM
9. Envío de respuesta a MeLi via API
10. OpenSpec spec: ai-copilot

**Demo:** pregunta real, copiloto sugiere respuesta con KB, vendedor edita y envía.

**Skill:** agent-dispatcher (implement) + agent-review (gate)

---

## Phase 6: Auto-respuesta inteligente — 2-3 días

**Goal:** IA clasifica preguntas rutinarias vs complejas, auto-responde las rutinarias, eleva las complejas.

**Deliverable:** feature opt-in funcionando, preguntas rutinarias se responden solas, badge "Auto IA" visible.

**Depends on:** Phase 5 (AI copilot)

**Tasks:**
1. Edge Function: classify-question (rutinaria vs compleja, con score de confianza)
2. Edge Function: auto-answer (si rutinaria + score > umbral → genera respuesta + envía a MeLi)
3. Config en Settings: activar/desactivar, umbral de confianza, criterios de clasificación
4. Campo en questions: auto_answered (bool), auto_answer_score (float)
5. Badge "Auto IA" en inbox para preguntas auto-respondidas
6. Auditoría: vendedor puede ver auto-respuestas, revertir (re-abrir como pendiente)
7. Notificación al vendedor: "X preguntas auto-respondidas" (toast/counter)
8. Fallback: si IA no confidente → queda pendiente normal
9. OpenSpec spec: auto-answer

**Demo:** activar feature, preguntas rutinarias se responden solas, ver badge en inbox, revertir una.

**Skill:** agent-dispatcher (implement)

---

## Phase 7: Resumen IA de hilos — 1-2 días

**Goal:** hilos con 2+ preguntas muestran resumen auto-generado, cacheado por hash.

**Deliverable:** abrir hilo con 2+ preguntas → resumen IA aparece arriba del detalle.

**Depends on:** Phase 3 (inbox UI)

**Tasks:**
1. Tabla: thread_summaries (company_id, buyer_id, product_id, questions_hash, summary, created_at)
2. Edge Function: summarize-thread (resolve preguntas, calcular hash, cache check, LLM call)
3. Componente ThreadSummary (skeleton + render + refresh)
4. Hash: sha256 de IDs + final_answer ordenados
5. Regeneración automática cuando cambia el hash (nueva pregunta)
6. No mostrar para hilos de 1 pregunta
7. OpenSpec spec: thread-summary

**Demo:** hilo con 5 preguntas muestra resumen, llega pregunta nueva → se regenera.

**Skill:** agent-dispatcher (implement)

---

## Phase 8: Billing Mercado Pago — 2-3 días

**Goal:** suscripción mensual operativa real. Plan creado en MP, secrets configurados, webhooks funcionando.

**Deliverable:** vendedor se suscribe, MP cobra, webhook confirma, billing_status activo.

**Depends on:** Phase 1 (auth + DB)

**Tasks:**
1. **Crear plan de preapproval en Mercado Pago** (esto es lo que v1 NUNCA hizo)
2. Configurar secrets en Supabase Vault: MP_ACCESS_TOKEN, MP_PREAPPROVAL_PLAN_ID
3. Edge Function: mp-create-subscription (crear preapproval, devolver checkout_url)
4. Edge Function: mp-check-subscription (verificar estado)
5. Edge Function: mp-cancel-subscription (pausar)
6. Edge Function: mp-webhook (IPN receiver + validación HMAC)
7. UI: Settings → Plan (ver plan, suscribirse, cancelar, danger zone)
8. Polling de verificación como fallback si webhook no llega
9. Gates: billing_status=active requerido para acceder al inbox (o trial period)
10. OpenSpec spec: billing-mp

**Demo:** suscribirse real, ver cobro en MP, webhook actualiza estado, cancelar.

**Skill:** agent-dispatcher (implement) + agent-review (gate) — billing es crítico

---

## Phase 9: Settings consolidado — 1-2 días

**Goal:** todos los settings en un solo lugar, UX limpia.

**Deliverable:** Settings con secciones: Empresa, Operadores, MeLi, Copiloto (tono + instrucciones), Auto-respuesta, KB, Plan/Billing, Danger zone.

**Depends on:** Phases 1-8 (consolida todo)

**Tasks:**
1. Layout de Settings con secciones
2. Empresa: nombre, logo, info
3. Operadores: invitar, roles (admin/operador), revocar
4. MeLi: estado de conexión, reconectar, desconectar
5. Copiloto: tono, instrucciones custom, preview
6. Auto-respuesta: toggle, umbral, criterios
7. KB: link a gestión de artículos
8. Plan/Billing: plan actual, estado, upgrade/downgrade, cancelar
9. Danger zone: eliminar empresa, eliminar operador

**Demo:** navegar todas las secciones, cambiar configuración, ver que persiste.

**Skill:** agent-dispatcher (implement)

---

## Phase 10: Analytics básico — 1-2 días

**Goal:** visibilidad de métricas clave sin ser un dashboard complejo.

**Deliverable:** página de Analytics con métricas de volumen, tiempos, tasas.

**Depends on:** Phase 3 (inbox data)

**Tasks:**
1. Queries/aggregations: preguntas/día, tiempo de respuesta promedio, tasa auto-respuesta, tasa resolución
2. Charts simples (recharts o similar): línea temporal, barras por estado, donut auto vs manual
3. Filtros: rango de fechas, por operador
4. RLS: solo ve datos de su empresa
5. OpenSpec spec: analytics

**Demo:** ver gráficos con datos reales de las preguntas gestionadas.

**Skill:** agent-dispatcher (implement)

---

## Phase 11: Hardening + Polish — 2-3 días

**Goal:** producción-ready. Error handling, loading states, empty states, responsive, tests.

**Deliverable:** app lista para que los 3 clientes Beta migren.

**Depends on:** Phases 1-10

**Tasks:**
1. Error boundaries en rutas críticas
2. Loading skeletons en todos los async views
3. Empty states (sin preguntas, sin KB, sin operadores)
4. Responsive (mobile/tablet — los vendedores usan mucho el celular)
5. Tests unitarios (vitest) en lógica crítica
6. Tests E2E (Playwright) en flujos principales
7. Rate limiting en Edge Functions
8. Logging estructurado en Edge Functions
9. Migración de 3 clientes Beta (datos + onboarding)
10. CHANGELOG final del MVP

**Demo:** app completa, responsive, sin crashes, lista para producción.

**Skill:** agent-review (gate completo) + agent-dispatcher (fixes)

---

## Timeline estimado

| Fase | Duración | Acumulado |
|---|---|---|
| 1. Foundation | 2-3 días | 3 días |
| 2. MeLi Integration + Auto-learn | 4-5 días | 7-8 días |
| 3. Inbox UI | 3-4 días | 10 días |
| 4. KB UI + RAG | 2 días | 12 días |
| 5. AI Copilot | 3-4 días | 16 días |
| 6. Auto-respuesta | 2-3 días | 18 días |
| 7. Resumen IA | 1-2 días | 20 días |
| 8. Billing MP | 2-3 días | 23 días |
| 9. Settings | 1-2 días | 25 días |
| 10. Analytics | 1-2 días | 27 días |
| 11. Hardening | 2-3 días | 30 días |

**Total estimado: ~30 días (6 semanas a ritmo sostenido, 3 semanas a ritmo intensivo)**

---

## Paralelismo posible

Algunas fases se pueden paralelizar con subagentes en la Air:

- **Phase 4 (KB UI + RAG)** depende de Phase 2 (auto-learn) en vez de Phase 1 → puede correr en paralelo con Phase 3
- **Phase 7 (Resumen IA)** solo depende de Phase 3 → puede correr en paralelo con 4, 5, 6
- **Phase 8 (Billing)** solo depende de Phase 1 → puede correr en paralelo con 2, 3, 4
- **Phase 10 (Analytics)** solo depende de Phase 3 → puede correr en paralelo con 5, 6, 7, 8, 9

Con paralelismo (Mini planifica + Air codea): **~3 semanas intensivas**.

---

## Skill mapping

| Fase | Skill primaria | Skill secundaria |
|---|---|---|
| 1. Foundation | web-app-builder | — |
| 2. MeLi Integration | sdd-brownfield (spec) + agent-dispatcher (impl) | — |
| 3. Inbox UI | agent-dispatcher | agent-review (gate) |
| 4. KB + RAG | agent-dispatcher | — |
| 5. AI Copilot | agent-dispatcher | agent-review (gate) |
| 6. Auto-respuesta | agent-dispatcher | — |
| 7. Resumen IA | agent-dispatcher | — |
| 8. Billing MP | agent-dispatcher | agent-review (gate crítico) |
| 9. Settings | agent-dispatcher | — |
| 10. Analytics | agent-dispatcher | — |
| 11. Hardening | agent-review (gate completo) | agent-dispatcher (fixes) |

---

## Risk register

| Riesgo | Impacto | Prob | Mitigación | Trigger |
|---|---|---|---|---|
| Plan preapproval MP no se aprueba rápido | Alto | Media | Crearlo día 1 de Phase 8 (o antes), tener plan B con checkout simple | Pasan 3 días sin aprobación |
| API MeLi rate limits | Medio | Media | Backoff exponencial + cache + polling espaciado | 429s frecuentes |
| Supabase free tier no suficiente | Medio | Baja | Plan pago desde el inicio (ya tenemos cuenta) | DB size > 500MB |
| OAuh MeLi cambia | Alto | Baja | Seguir docs oficiales, mantener adapter aislado | Docs cambian |
| Migración de 3 clientes más compleja de lo esperado | Medio | Media | v1 sigue en Lovable, migración gradual uno por uno | Primer cliente tiene issues |
| Scope creep | Alto | Alta | Las 10 features están cerradas. Todo lo nuevo → post-MVP | "Solo una cosa más..." |

---

## Post-MVP (rough when)

| Feature | Cuando |
|---|---|
| Multi-marketplace (Amazon, MercadoPago envíos) | Después de validar v2 con 3+ clientes |
| WhatsApp post-venta | Después de 3 meses de uso estable |
| Templates con variables dinámicas | Cuando los clientes lo pidan |
| Integración KanamAI (enrutamiento de modelos) | Cuando KanamAI etapa 2 esté lista |
| App móvil | Si los clientes lo piden fuerte |
| Import de datos históricos de v1 | Migración manual por cliente, on-demand |
| Deploy a producción | Después de Phase 11, cuando hardening pase |