# SoporteML v3 - ROADMAP.md

> **Qué es:** roadmap vivo del proyecto. Se adapta a medida que definimos el producto y aprendemos.
> **Estado:** ACTUALIZADO (2026-08-12) — Fase 1 completa, Fase 2 MeLi lista, nuevas fases de producto.
> **Regla:** este documento es dinámico — cada fase se revisa y ajusta cuando la alcanzamos. No es un plan estático.

---

## Fase 0 - Definición ✅ COMPLETA

**Objetivo:** tener el producto y la arquitectura definidos antes de tocar código.

- [x] Recibir referencia técnica del backend (Lovable) → `BACKEND-REFERENCE.md`
- [x] Recibir design tokens (Lovable) → `DESIGN-TOKENS-LOVABLE.md`
- [x] Crear `PRODUCT.md` (definición de producto)
- [x] Crear `ROADMAP.md` (este documento)
- [x] Decidir runtime del backend → ADR-002 (Node + Hono)
- [x] Cruzar tokens de Lovable contra v1 → ADR-003 (design system tokens)
- [x] Definir estructura del monorepo → Turborepo + pnpm

**Criterio de salida:** producto definido, arquitectura decidida, ADRs escritos. ✅

---

## Fase 1 - Alpha local ✅ COMPLETA (2026-08-11)

**Objetivo:** sistema completo corriendo en local: SQLite + backend local + frontend. Cero servicios cloud.

**Entregables completados:**
- [x] Scaffold monorepo (web + api + db)
- [x] Capa de datos SQLite (schema mapeado de `BACKEND-REFERENCE.md`, repositorios incl. oauth)
- [x] Backend local: núcleo MeLi (oauth, sync, publish, token service)
- [x] Auth mock local (login de prueba con roles)
- [x] Frontend sobre design system (tokens Lovable reconciliados)
- [x] IA (Ollama local, deepseek-v4-flash:cloud) — categoriza + sugiere, fallback a mock
- [x] Billing mock (post-MVP, verificado)

**Criterio de salida:** un vendedor puede registrarse, conectar su MeLi, ver sus consultas, responder y publicar, con IA asistida — todo local. ✅

---

## Fase 2 - Validación de integraciones (EN CURSO)

**Objetivo:** probar de verdad las integraciones que nunca se validaron.

### Mercado Libre — ✅ FUNCIONAL (2026-08-12)
- [x] OAuth 2.0 + PKCE S256 end-to-end (connect + callback + persistencia de estados)
- [x] Token real de producción verificado (GONZOBLASCO / MLA) + refresh automático
- [x] Sync de preguntas real
- [x] Publicar respuestas
- [x] **Modo mock** (`MELI_MOCK=1`) — sync/publish de ejemplo, no toca la cuenta real
- [x] Fix multi-tenant (UNIQUE por empresa en preguntas)
- [x] Redirect URI con túnel HTTPS (cloudflared) para app publicada

### Pendiente en Fase 2
- [ ] Mercado Pago: probar flujo real en sandbox (crear/chequear/cancelar suscripción) — post-MVP, no bloquea
- [ ] IA: conectar API keys reales (Lovable AI Gateway + OpenAI) si hace falta
- [ ] Email: Resend + Lovable Email
- [ ] Decidir si el billing entra en el MVP o queda para después

**Criterio de salida:** todas las integraciones probadas y funcionando, o descartadas con razón.

---

## Fase 2.5 - Enriquecimiento del core con datos de MeLi (NUEVA - prioridad)

**Objetivo:** que la IA responda **mejor** usando datos reales de la publicación del vendedor. Respeta el core (bandeja + IA) y los límites del PRODUCT.md (no ampliar a e-commerce/ERP/analytics completo).

**Fundamento:** los permisos de la app de MeLi (publicaciones, métricas, promociones) abren datos valiosos. El camino de menor riesgo y mayor valor es **enriquecer las respuestas**, no ampliar el alcance.

**Entregables:**
- [x] **Respuestas enriquecidas con datos de la publicación (2026-08-12):**
  - [x] La IA usa stock real y vendidos en la sugerencia (ej: "quedan 5 unidades", "se vendieron 340")
  - [x] En modo real: sync trae GET /items/{id} y guarda stock/vendidos/condición en `meli_cache`
  - [x] Modo mock con datos de stock/ventas realistas por producto
  - [x] Categorización mock mejorada (stock vs ventas, keywords técnicos)
- [ ] Extender a variantes, envío y garantía reales de la publicación (usar `getItemDescription`)
- [ ] Decidir si sumar KPIs ligeros del vendedor (ventas, conversión) al dashboard — **post-MVP**, evaluar en Fase 4

**Criterio de salida:** la IA responde consultas con datos reales y actualizados de la publicación, verificable en mock y real.

**Nota de alcance:** el dashboard de métricas completo (ventas, conversión, reputación) NO es core — se pospone a post-MVP (Fase 4) para no romper el foco en la bandeja de consultas. El PRODUCT.md (sección 5) lo mantiene como límite.

---

## Fase 3 - Decisión de despliegue

**Objetivo:** decidir dónde corre el sistema en producción.

- [ ] Evaluar: ¿Supabase (con razones válidas) o backend propio deployado (Deno Deploy / Node / contenedor)?
- [ ] Migrar capa de datos SQLite → Postgres si corresponde
- [ ] Configurar auth real (OAuth MeLi + auth de usuarios)
- [ ] CI/CD

**Criterio de salida:** decisión de despliegue tomada con criterio, no por default.

---

## Fase 4 - Beta / Prod

**Objetivo:** sistema en producción con usuarios reales.

- [ ] Onboarding de primeros vendedores
- [ ] **Evaluar dashboard de métricas** (ventas, conversión, reputación) — decisión con datos reales de uso
- [ ] Iterar sobre feedback real

---

## Notas de evolución

- Este roadmap es **vivo**: cada fase se revisa al alcanzarla.
- **Fase 1 y Fase 2 (MeLi) completas** — la alpha local funciona con integración MeLi real + modo mock.
- **Fase 2.5 (enriquecimiento del core)** es la nueva prioridad: respuestas mejores con datos reales, sin ampliar alcance.
- El **billing (Mercado Pago)** sigue siendo el mayor riesgo técnico (nunca probado) — aislado en Fase 2, no bloquea.
- **Dashboard de métricas completo** = post-MVP (Fase 4). No es core.
- Decisiones de alcance 2026-08-12: modo mock por defecto en dev; Storybook descartado (playground de componentes en su lugar).
