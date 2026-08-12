# SoporteML v3 - HANDOFF

> **Sesión:** 2026-08-12 (Fase 2 + port de diseño v1)
> **Estado:** Fase 1 completa ✅ + Fase 2 (integración MeLi) avanzando + diseño de v1 portado

---

## Qué se hizo

### Fase 0 - Definición (completa)
- `PRODUCT.md`, `ROADMAP.md`, `BRIEF.md` (independencia de vendor, alpha 100% local).
- ADR-001 (independencia de vendor), ADR-002 (runtime Node + Hono), ADR-003 (design tokens de Lovable).
- Insumos de Lovable: `BACKEND-REFERENCE.md`, `DESIGN-TOKENS-LOVABLE.md`, `DESIGN-GUIDE-LOVABLE.md`.

### Fase 1 - Alpha local (completa)
- Monorepo Turborepo + pnpm (`apps/web` + `apps/api` + `packages/db`).
- `packages/db`: schema SQLite (20+ tablas), repositorios (tenancy, questions, products, **oauth**).
- `apps/api` (Hono): cliente MeLi, token service, sync service, auth mock, IA (Ollama), billing mock.
- `apps/web` (Vite): design system Lovable, login mock, dashboard.

### Fase 2 - Integración MeLi (2026-08-12) ✅
- **OAuth MeLi real end-to-end** (PKCE S256): `/meli/connect` + `/meli/callback` + tabla `oauth_states`.
- **Token real de producción verificado** (GONZOBLASCO / MLA). Refresh automático.
- **Modo mock** (`MELI_MOCK=1`): sync genera 5 preguntas de ejemplo, instantáneo. Fallback a mock si no hay token.
- **Fix multi-tenant**: `questions.meli_question_id` → `UNIQUE(company_id, meli_question_id)`.
- Publish mock (no toca API real). UX con toasts de sonner.
- **Túnel HTTPS (cloudflared)** como redirect URI (la app publicada no acepta localhost).

### Port del diseño de v1 (2026-08-12) ✅
- Stack de v1 instalado (Radix, CVA, framer-motion, next-themes, sonner, etc.).
- Capa shadcn/ui copiada de v1 + alias `@/`.
- `index.css` = tokens Lovable v3 + utilidades custom de v1 + Inter.
- `AppSidebar` rediseñado (colapsable, tema, mobile) sin acoplamiento v1.
- `App.tsx` al layout de v1 + logout + toasts.
- **Playground de componentes** (`src/pages/Playground.tsx`, solo dev) — alternativa a Storybook.

## Cómo correr

```bash
# Terminal 1 - backend (puerto 3001) — necesita .env con credenciales MeLi + MELI_MOCK
cd apps/api && pnpm dev

# Terminal 2 - frontend (puerto 5173)
cd apps/web && pnpm dev
```

Abrir http://localhost:5173 → "Entrar (modo demo)" → Sincronizar → ver preguntas mock → Responder.

**Para OAuth real:** levantar túnel cloudflared (`cloudflared tunnel --url http://localhost:3001`), actualizar `MELI_REDIRECT_URI` en `.env` + redirect en panel MeLi, conectar desde Ajustes. El token actual sigue en la DB mientras no expire.

## Dónde está cada cosa

- Código: repo `gonzoblasco/soporteml-v3` (independiente, NO submodule). Último commit: `5e237ab`.
- Memoria institucional: `.knowledge/` en el workspace.
- ADRs: `docs/adr/` en el repo (ADR-001..003).

## Pendientes (Fase 2 + próximos)

- [ ] **Actualizar ROADMAP.md** antes de ampliar alcance (decisión acordada).
- [ ] Explorar features extra por permisos MeLi (métricas, publicaciones, promociones).
  - Opciones A+B recomendadas: dashboard con métricas reales + enriquecer respuestas con datos de la publicación.
  - Definir modo mock para las features nuevas.
- [ ] Probar Mercado Pago real en sandbox.
- [ ] Email (Resend + Lovable Email).
- [ ] Afinar categorización del mock (algunas preguntas caen en categoría genérica).
- [ ] Validación visual del port de diseño (build OK, falta revisión visual fina de Gonzo).

## Notas de decisión

- "adelante" a secas = seguir con mi recomendación según el contexto de la tarea actual (regla acordada 2026-08-12).
- Storybook NO se usa (equipo de 1 dev): se usa Playground de componentes en su lugar.
- Modo mock por defecto en dev (`MELI_MOCK=1`) para no tocar la cuenta real de MeLi.
