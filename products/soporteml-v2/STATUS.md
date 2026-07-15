# Product Status: SoporteML v2

**Última actualización:** 2026-07-15

---

## Current phase: Phase 1 — Foundation (✅ COMPLETA)

### Phases
- [x] Phase 1: Foundation — ✅ COMPLETA
- [ ] Phase 2: MeLi Integration + Auto-learn — pendiente
- [ ] Phase 3: Inbox UI — pendiente
- [ ] Phase 4: KB UI + RAG — pendiente
- [ ] Phase 5: AI Copilot — pendiente
- [ ] Phase 6: Auto-respuesta inteligente — pendiente
- [ ] Phase 7: Resumen IA de hilos — pendiente
- [ ] Phase 8: Billing MP — pendiente
- [ ] Phase 9: Settings consolidado — pendiente
- [ ] Phase 10: Analytics básico — pendiente
- [ ] Phase 11: Hardening + Polish — pendiente

### Phase 1 detail
- [x] Scaffold React+Vite+TS
- [x] Dependencias instaladas
- [x] Config TS, Biome, Vitest, Tailwind v4
- [x] Estructura de carpetas
- [x] Entity types (9 entidades)
- [x] Migración inicial SQL (schema + RLS + pgvector + match_kb_chunks)
- [x] AGENTS.md, HANDOFF.md, CHANGELOG.md, ROADMAP.md, ADR-001
- [x] CI GitHub Actions
- [x] Verification gate: lint ✅ typecheck ✅ test ✅ build ✅
- [x] Git init + primer commit
- [x] Supabase local corriendo (Docker + supabase start)
- [x] .env.local con keys reales
- [x] shadcn/ui init + components (button, input, card, label, dialog, dropdown-menu, avatar)
- [x] Auth UI (LoginPage, RegisterPage)
- [ ] useAuth hook
- [ ] OpenSpec init

### Decisions log
- 2026-07-15: Producto aprobado — reemplazo total de v1, stack React+Vite+Supabase
- 2026-07-15: MVP scope cerrado en 10 features (incluye auto-respuesta inteligente opt-in)
- 2026-07-15: Auto-learn de MeLi agregado al onboarding
- 2026-07-15: ADR-001 — React+Vite (no Next.js) para compatibilidad con Lovable
- 2026-07-15: Biome 2.5.4 (schema actualizado, tailwindDirectives habilitado)
- 2026-07-15: web-app-builder skill actualizada con lecciones del scaffold

### Blockers
- Ninguno

### Next action
1. useAuth hook + ProtectedRoute wrapper
2. Onboarding flow (crear empresa post-registro)
3. OpenSpec init + spec auth-multi-tenant
4. Commit final de Phase 1