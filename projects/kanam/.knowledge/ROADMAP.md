# Kanam — Roadmap

**Versión:** 0.1
**Fecha:** 2026-07-26

---

## MVP v0.1 — "El Diario"

### Fase 1: Fundación (issues #1, #2, #13, #14, #12) ✅ COMPLETA

- [x] **#1** Scaffold: Next.js + Tailwind + shadcn/ui + Biome + Vitest + PWA esqueleto
- [x] **#2** Supabase: proyecto + schema (entries, profiles) + auth (magic link) + RLS + Edge Function ping
- [x] **#14** Tipos de entrada: constantes y tipos TypeScript
- [x] **#13** Supabase client: setup en el frontend (cliente, middleware, hooks)
- [x] **#12** Auth UI: login page + magic link flow

### Fase 2: Core (issues #3, #4, #5)

- [ ] **#3** Timeline: página principal con lista cronológica inversa
- [ ] **#4** Crear entrada: modal con tipos (nota, check-in, foto)
- [ ] **#5** Editar/eliminar entrada

### Fase 3: IA (issue #7)

- [ ] **#7** IA: Edge Function para resumen diario (Ollama Cloud)

### Fase 4: UX (issues #8, #9, #10)

- [ ] **#8** Tags + filtros en entradas
- [ ] **#9** PWA: offline support + install prompt
- [ ] **#10** Testing en iOS + fixes

### Fase 5: Deploy (issues #6, #11)

- [ ] **#6** Despliegue en Vercel
- [ ] **#11** CI/CD: GitHub Actions con lint + build

## Post-MVP

Dependiendo del uso real, evaluar:
- Writing tracker
- Notificaciones push
- Multi-tenant (invitaciones)
- Dashboard de proyectos
