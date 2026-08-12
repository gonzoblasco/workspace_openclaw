# SoporteML v3 - HANDOFF

> **Sesión:** 2026-08-11 (arranque → Fase 1 completa)
> **Estado:** Fase 1 (alpha local) COMPLETA ✅

---

## Qué se hizo

### Fase 0 - Definición (completa)
- `PRODUCT.md` - definición completa del producto (visión, roles, features, límites, principios).
- `ROADMAP.md` - roadmap vivo (F0 definición → F1 alpha local → F2 validación → F3 despliegue → F4 beta).
- `BRIEF.md` - contexto de versiones + dirección (independencia de vendor).
- ADR-001 (independencia de vendor / alpha 100% local), ADR-002 (runtime Node + Hono), ADR-003 (design system tokens de Lovable).
- Insumos de Lovable: `BACKEND-REFERENCE.md` (schemas + edge functions), `DESIGN-TOKENS-LOVABLE.md` (tokens).

### Fase 1 - Alpha local (completa)
- **Monorepo:** Turborepo + pnpm (`apps/web` + `apps/api` + `packages/db`).
- **`packages/db`:** schema SQLite (20+ tablas mapeadas de Postgres), tipos, helpers, capa de repositorios (tenancy, questions, products). 4 tests + typecheck limpio.
- **`apps/api` (Hono):** cliente MeLi (OAuth PKCE, sync, publish), token service con refresh, sync service con ficha proactiva, auth mock, IA con Ollama (categoriza + sugiere), billing mock. Verificado en vivo.
- **`apps/web` (Vite):** design system con tokens de Lovable (ADR-003), login mock, dashboard con Inbox/Productos/Ajustes, cliente API con proxy. Build OK.
- **Repo del proyecto:** `gonzoblasco/soporteml-v3` (privado) creado + README.

## Cómo correr

```bash
# Terminal 1 - backend (puerto 3001)
cd apps/api && pnpm dev

# Terminal 2 - frontend (puerto 5173)
cd apps/web && pnpm dev
```

Abrir http://localhost:5173 → "Entrar (modo demo)".

## Dónde está cada cosa

- Código: repo del proyecto `gonzoblasco/soporteml-v3` (independiente, NO submodule).
- Memoria institucional: `.knowledge/` en el workspace (PRODUCT, ROADMAP, ADRs, referencias).
- ADRs: `docs/adr/` en el repo del proyecto (ADR-001..003).

## Cómo verificar

- `cd packages/db && pnpm test` → 4 tests pasan.
- `cd apps/api && pnpm check-types` → limpio.
- `cd apps/web && pnpm build` → build OK.
- Levantar backend + frontend → login demo → Inbox vacío → (con MeLi conectado) sync + responder.

## Issues conocidos

- **MeLi no conectado:** la app corre con auth mock y sin MeLi real (falta MELI_APP_ID/MELI_SECRET_KEY). El sync de preguntas real requiere conectar MeLi.
- **Billing es mock:** Mercado Pago nunca se probó (ADR-003, post-MVP). El flujo de suscripción es simulado.
- **IA usa Ollama local:** si Ollama no está corriendo, la IA usa un fallback mock determinístico.
- **`@soporteml/db` se resuelve por build:** hay que compilar el db (`pnpm build` en packages/db) antes de que el api lo importe. En dev, `tsx` lo maneja.

## Qué sigue (Fase 2 - validación de integraciones)

- [ ] Probar Mercado Pago real en sandbox (crear/chequear/cancelar suscripción).
- [ ] Conectar MeLi real (MELI_APP_ID/MELI_SECRET_KEY) y validar el sync end-to-end.
- [ ] Email (Resend + Lovable Email) si hace falta.
- [ ] Decidir si el billing entra en el MVP o queda post-MVP.

## Decisiones clave de la sesión

- **Independencia de vendor:** alpha 100% local (SQLite + backend local + Ollama). Supabase solo si hay razones válidas (ADR-001).
- **Runtime backend:** Node + Hono (ADR-002).
- **Design system:** tokens de Lovable como fuente de verdad (ADR-003).
- **Ficha proactiva:** el scraping del post MeLi se dispara solo al crear la ficha (no bajo demanda), IA llena baches.
- **Autopilot:** umbral de confianza + aprobación en categorías sensibles (garantía/técnico/reclamos).
- **Billing:** post-MVP, mockeado en alpha.
