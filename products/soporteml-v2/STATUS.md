# Product Status: SoporteML v2

**Última actualización:** 2026-07-15

---

## Current phase: Phase 2 — MeLi Integration + Auto-learn (en progreso)

### Phases
- [x] Phase 1: Foundation — ✅ COMPLETA
- [~] Phase 2: MeLi Integration + Auto-learn — en progreso
- [~] Phase 3: Inbox UI — en progreso
- [ ] Phase 4: KB UI + RAG — pendiente
- [ ] Phase 5: AI Copilot — pendiente
- [ ] Phase 6: Auto-respuesta inteligente — pendiente
- [ ] Phase 7: Resumen IA de hilos — pendiente
- [ ] Phase 8: Billing MP — pendiente
- [ ] Phase 9: Settings consolidado — pendiente
- [ ] Phase 10: Analytics básico — pendiente
- [ ] Phase 11: Hardening + Polish — pendiente

### Phase 2 detail
- [x] Edge Function: meli-oauth-callback (exchange code → tokens, store in companies)
- [x] Edge Function: sync-meli-questions (fetch from MeLi API, upsert products/buyers/questions)
- [x] Edge Function: meli-webhook (receive events, trigger sync)
- [x] Edge Function: meli-initial-fetch (fetch listings + historical questions, trigger auto-learn)
- [x] Edge Function: auto-generate-product-ficha (AI generates CRM fields per product)
- [x] Edge Function: auto-generate-kb (AI generates KB articles from historical Q&A)
- [x] OpenSpec spec: meli-integration (4 requirements, 6 scenarios)
- [x] OAuth UI (Settings → MeLi connect button + callback handler)
- [x] Onboarding flow with progress (welcome → connect-meli → learning → done)
- [x] Deploy Edge Functions to Supabase local (6 functions serving)
- [ ] Cron job for periodic polling (fallback)
- [ ] Token refresh logic

### Decisions log
- 2026-07-15: Producto aprobado — reemplazo total de v1, stack React+Vite+Supabase
- 2026-07-15: MVP scope cerrado en 10 features (incluye auto-respuesta inteligente opt-in)
- 2026-07-15: Auto-learn de MeLi agregado al onboarding
- 2026-07-15: ADR-001 — React+Vite (no Next.js) para compatibilidad con Lovable
- 2026-07-15: Biome 2.5.4 (schema actualizado, tailwindDirectives habilitado)
- 2026-07-15: web-app-builder skill actualizada con lecciones del scaffold
- 2026-07-15: Cambio de modelo qwen3.5:cloud → deepseek-v4-flash

### Blockers
- Se necesita APP_ID y CLIENT_SECRET de MeLi Developer para probar OAuth real
- Se necesita OPENAI_API_KEY para auto-generate functions
- Docker debe estar corriendo para deploy local de Edge Functions

### Next action
1. OAuth UI (Settings → MeLi connect)
2. Onboarding flow with progress indicators
3. Deploy Edge Functions to Supabase local
4. Test OAuth flow end-to-end