# Product Status: SoporteML v2

**Última actualización:** 2026-07-15

---

## Current phase: Phase 1 — Foundation (en progreso)

### Phases
- [~] Phase 1: Foundation — scaffold done, auth UI + Supabase local pendiente
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
- [ ] Supabase local corriendo
- [ ] Auth UI (login, register, reset password)
- [ ] shadcn/ui components instalados
- [ ] OpenSpec init
- [ ] Auth hook (useAuth)

### Decisions log
- 2026-07-15: Producto aprobado — reemplazo total de v1, stack React+Vite+Supabase
- 2026-07-15: MVP scope cerrado en 10 features (incluye auto-respuesta inteligente opt-in)
- 2026-07-15: Auto-learn de MeLi agregado al onboarding
- 2026-07-15: ADR-001 — React+Vite (no Next.js) para compatibilidad con Lovable
- 2026-07-15: Biome 2.5.4 (schema actualizado, tailwindDirectives habilitado)

### Blockers
- Ninguno

### Next action
1. `supabase init` + `supabase start` para DB local
2. Instalar shadcn/ui components base
3. Implementar auth UI + useAuth hook
4. OpenSpec init + spec auth-multi-tenant