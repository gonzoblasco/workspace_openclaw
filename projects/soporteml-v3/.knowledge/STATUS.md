# SoporteML v3 - STATUS

## 2026-08-12 (tarde) - Port del diseño v1 + playground de componentes

### Completado
- **Port del esqueleto visual de v1 al frontend v3** (extraído del código real de v1 en `projects/soporteml`):
  - Instalado stack de diseño de v1: Radix UI primitives, class-variance-authority, tailwind-merge, clsx, framer-motion, next-themes, sonner, tailwindcss-animate, lucide-react.
  - Copiada capa shadcn/ui de v1 (button, card, badge, input, sidebar, sheet, skeleton, tooltip, separator, sonner).
  - Configurado alias `@/` en Vite + TypeScript.
  - Fusionado `index.css`: tokens Lovable v3 (ya existían) + utilidades custom de v1 (glass-panel, glow-primary, text-gradient, animaciones) + fuente Inter.
  - Portado `AppSidebar` rediseñado (colapsable, tema claro/oscuro con next-themes, mobile drawer, footer con avatar/logout) sin acoplamiento a Supabase/router/auth de v1.
  - Portado `EmptyState`, `SkeletonCards`, `CategoryBadge` (adaptado a tokens muted/strong).
  - Creado `theme-provider` (next-themes).
  - `App.tsx` adaptado al layout de v1 (flex h-screen + sidebar + main scrollable) manteniendo features (mock sync, publish, IA) + logout.
- **Playground de componentes** (alternativa ligera a Storybook para equipo de 1 dev):
  - `src/pages/Playground.tsx` - catálogo visual de componentes (buttons, badges, inputs, cards, skeletons, empty states, status badges, iconos).
  - Solo visible en desarrollo (`import.meta.env.DEV`), no se incluye en build de producción.
  - Decisión: Storybook NO aporta suficiente para equipo de 1 dev (costo de mantenimiento > beneficio); el playground cubre el 80% del valor.

### Pendiente (Fase 2)
- [ ] Probar responder una pregunta mock desde la app (`/meli/publish` en modo mock).
- [ ] Probar Mercado Pago real en sandbox.
- [ ] Email (Resend + Lovable Email).
- [ ] Afinar keywords del mock de categorización.
- [ ] La URL del túnel cloudflared es temporal - cada reinicio cambia.

## 2026-08-12 - Integración MeLi funcionando + modo mock

### Completado
- **OAuth MeLi real end-to-end funcionando** (PKCE S256):
  - `GET /meli/connect` genera URL de autorización + persiste `state`/`code_verifier` en DB (tabla `oauth_states`).
  - `GET /meli/callback` (antes POST) verifica `state` (anti-CSRF), intercambia `code` → tokens, guarda en `meli_tokens`, redirige a página de éxito.
  - PKCE mejorado de `plain` → `S256`.
  - **Token real de producción obtenido y verificado** contra `api.mercadolibre.com` (`GONZOBLASCO`, id 10061615, site MLA). Refresh token guardado (refresh automático por `MeliTokenService`).
- **Modo mock para desarrollo** (`MELI_MOCK=1` en `.env`):
  - `MeliSyncService` genera 5 preguntas de ejemplo realistas (garantía, envío, talle, cuotas, accesorios) con productos y compradores mock.
  - Sin token conectado → fallback automático a mock (la app es usable en dev sin cuenta real).
  - **Fix de rendimiento:** en modo mock usa categorización determinística instantánea (no la IA real que tardaba ~40s en serie). Sync ahora responde en ~6ms.
- **Fix bug multi-tenant:** `questions.meli_question_id` era `UNIQUE` global → ahora `UNIQUE(company_id, meli_question_id)`. Cada empresa tiene su propio set aislado (dos empresas podían colisionar con el mismo ID de pregunta mock).
- **Frontend:** botón "Conectar Mercado Libre" en Ajustes ahora dispara el flujo OAuth real (`/meli/connect` + redirect). Link "Volver" post-OAuth apunta a la app local (`APP_URL`).
- **Scripts del API** cargan `.env` (`--env-file` en dev/start).
- **Túnel HTTPS (cloudflared)** como redirect URI válido para la app publicada de MeLi (la app de v1 es de producción, no acepta localhost).

### Pendiente (Fase 2)
- [ ] Probar responder una pregunta mock desde la app (`/meli/publish` en modo mock).
- [ ] Probar Mercado Pago real en sandbox.
- [ ] Email (Resend + Lovable Email).
- [ ] Afinar keywords del mock de categorización (algunas preguntas caen en categoría genérica).
- [ ] La URL del túnel cloudflared es temporal - cada reinicio cambia; hay que actualizar redirect en panel + `.env`.

## 2026-08-11 - Definición de producto

### Completado
- **Creado `PRODUCT.md`** - definición completa del producto: visión, usuarios/roles, features core, integraciones (MeLi funcional, MP nunca probado), límites explícitos, principios de arquitectura (independencia de vendor, alpha 100% local), preguntas abiertas.
- **Creado `ROADMAP.md`** - roadmap vivo: Fase 0 definición → Fase 1 alpha local → Fase 2 validación de integraciones → Fase 3 decisión de despliegue → Fase 4 beta.
- **Actualizado `BRIEF.md`** - refleja la nueva dirección: independencia de vendor, alpha local, stack propuesto.
- **Decisión de dirección (Gonzo):** primera alpha 100% local (SQLite + backend local). Supabase solo si hay razones válidas después. Recrear edge functions en runtime local (Deno/Node+Hono a decidir). Mercado Pago nunca probado → mockear en alpha.

### Pendiente (Fase 0)
- [ ] Resolver preguntas abiertas de PRODUCT.md (sección 7)
- [x] ~~Decidir runtime del backend~~ → **ADR-002: Node + Hono** (2026-08-11)
- [x] ~~Cruzar tokens de Lovable contra v1~~ → **ADR-003: design system tokens** (2026-08-11)
- [x] ~~Definir estructura del monorepo~~ → **Turborepo + pnpm** (estándar de Gonzo, ADR-029 react-18-design-patterns): `apps/web` (Vite) + `apps/api` (Hono) + `packages/db` (SQLite).

## Fase 1 - Alpha local (2026-08-11)

### Completado
- Estructura del monorepo definida: Turborepo + pnpm.
- **Scaffold monorepo creado** (apps/web + apps/api + packages/db).
- **packages/db implementado:** schema SQLite (20+ tablas), tipos, helpers, capa de repositorios (tenancy, questions, products). 4 tests + typecheck limpio.
- **apps/api implementado** (Hono): cliente MeLi (OAuth PKCE, sync, publish), token service con refresh, sync service con ficha proactiva, auth mock, rutas (health, auth/dev, meli/*, questions, products). Verificado en vivo.
- **apps/web implementado** (Vite + React + Tailwind): design system con tokens de Lovable (ADR-003), login mock, dashboard con Inbox/Productos/Ajustes, cliente API con proxy. Verificado end-to-end + build OK.
- **IA integrada** (Ollama local, deepseek-v4-flash:cloud): categoriza preguntas + sugiere respuestas con contexto del producto. Fallback a mock si Ollama no está. Verificado en vivo.
- **Billing mock** (post-MVP): flujo de suscripción simulado (crear/chequear/cancelar). Verificado en vivo.

### FASE 1 COMPLETA ✅

La alpha local corre completa: DB (SQLite) + backend (Hono) + frontend (Vite) + IA (Ollama) + billing (mock).

**Cómo correrla:**
- Backend: `cd apps/api && pnpm dev` (puerto 3001)
- Frontend: `cd apps/web && pnpm dev` (puerto 5173)

### Pendiente (Fase 2 - validación de integraciones)
- [ ] Probar Mercado Pago real en sandbox
- [ ] Conectar API keys reales de IA si hace falta
- [ ] Email (Resend + Lovable Email)

## 2026-08-07 - Arranque (sesión nocturna)

### Completado
- Creado repo v3 con estructura `.knowledge/`.
- Copiado `UI-DESIGN-SKILL.md` (estándar de implementación, basado en v1).
- Creado `DESIGN-GUIDE.md` (identidad visual documentada desde el código real de v1).
- Creado `BRIEF.md` con contexto de versiones (v1 = referencia, v2 = experimento descartado).
- **Recibida la guía de diseño oficial de Lovable** → guardada en `DESIGN-GUIDE-LOVABLE.md` (fuente de verdad de identidad visual para v3).
- Guardados prompts de referencia en `prompts/`:
  - `PROMPT-GUIA-DISENO.md` (ya ejecutado)
  - `PROMPT-SCHEMAS-BD.md` (pendiente de ejecutar)

## 2026-08-11 - Backend + design tokens aclarados

### Completado
- **Recibida la referencia técnica del backend de Lovable** → guardada en `BACKEND-REFERENCE.md` (327 líneas).
  - Schemas completos de Supabase/PostgreSQL: 20+ tablas, enums, RLS por tabla, funciones SQL, triggers, jobs pg_cron.
  - 25 Edge Functions con auth, input/output e integraciones.
  - Integraciones: MeLi (OAuth PKCE + webhook + cron), Lovable AI Gateway (Gemini), OpenAI embeddings, Mercado Pago (preapproval), Resend, Lovable Email.
  - Roles: agent / admin / super admin. Multi-tenant vía `memberships` + `user_belongs_to_company`.
  - Variables de entorno completas (solo nombres).
- El prompt `prompts/PROMPT-SCHEMAS-BD.md` quedó **ejecutado**.
- **Recibida la especificación de design tokens de Lovable** → guardada en `DESIGN-TOKENS-LOVABLE.md` (423 líneas).
  - Tokens nuevos: `--primary-muted`, `--primary-strong`, `--informative` (+foreground/muted/strong), `--surface-active`, `--surface-raised`, `--surface-sunken`, `--overlay`, `--glass`, `--focus-ring`, `--border-strong`, `--chart-1..5`, `--success/warning/destructive/informative-*-muted/strong`, badges de categoría con muted/strong.
  - Regla de estado global: fondo 12-15% + texto 100% con `*-strong` (no color base). Preferir tokens `*-muted` sobre `bg-<estado>/15`.
  - Escala tipográfica fina (Display→Micro/Overline/Metric/Mono) con Inter, tabular-nums para métricas.
  - Paleta completa v3 (base, marca, estados, badges, bordes, sidebar, gráficos, radio/sombras) + mapa token→componente + reglas WCAG AA + snippet CSS/Tailwind.
- El prompt `prompts/PROMPT-RECONCILIACION-TOKENS.md` quedó **ejecutado**.

### Pendiente
- [ ] Cruzar `DESIGN-TOKENS-LOVABLE.md` contra `DESIGN-GUIDE.md` y el skill (verificar que no haya conflictos con v1).
- [ ] Scaffold del repo v3.
- [ ] Implementación.

## Objetivo
Arrancar la versión definitiva de SoporteML a más tardar el lunes, con el design system y el backend aclarados desde el día uno.
