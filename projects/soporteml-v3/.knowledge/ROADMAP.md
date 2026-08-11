# SoporteML v3 - ROADMAP.md

> **Qué es:** roadmap vivo del proyecto. Se adapta a medida que definimos el producto y aprendemos.
> **Estado:** INICIAL (2026-08-11).
> **Regla:** este documento es dinámico — cada fase se revisa y ajusta cuando la alcanzamos. No es un plan estático.

---

## Fase 0 - Definición (EN CURSO)

**Objetivo:** tener el producto y la arquitectura definidos antes de tocar código.

- [x] Recibir referencia técnica del backend (Lovable) → `BACKEND-REFERENCE.md`
- [x] Recibir design tokens (Lovable) → `DESIGN-TOKENS-LOVABLE.md`
- [x] Crear `PRODUCT.md` (definición de producto)
- [x] Crear `ROADMAP.md` (este documento)
- [ ] Resolver preguntas abiertas de `PRODUCT.md` (sección 7)
- [ ] Decidir runtime del backend (Deno vs Node+Hono) → ADR
- [ ] Cruzar tokens de Lovable contra v1 → ADR de design system
- [ ] Definir estructura del monorepo

**Criterio de salida:** producto definido, arquitectura decidida, ADRs escritos.

---

## Fase 1 - Alpha local (100% local, sin nube)

**Objetivo:** sistema completo corriendo en local: SQLite + backend local + frontend. Cero servicios cloud.

**Entregables:**
- [ ] Scaffold monorepo (web + api + db)
- [ ] Capa de datos SQLite (schema mapeado desde `BACKEND-REFERENCE.md`, repositorios)
- [ ] Backend local: núcleo MeLi (sync, publish, oauth, webhook, item-proxy)
- [ ] Auth mock local (login de prueba con roles)
- [ ] **Onboarding:** registro → conexión MeLi (OAuth) → primera sincronización → bandeja poblada
- [ ] Frontend sobre design system cerrado (tokens reconciliados)
- [ ] IA mockeada o real según API keys disponibles
- [ ] Billing (Mercado Pago) **mockeado** — post-MVP, no bloquea la alpha

**Criterio de salida:** un vendedor puede registrarse, conectar su MeLi, ver sus consultas, responder y publicar, con IA asistida — todo local.

---

## Fase 2 - Validación de integraciones

**Objetivo:** probar de verdad las integraciones que nunca se validaron.

- [ ] Mercado Pago: probar flujo real en sandbox (crear/chequear/cancelar suscripción) — **post-MVP, no bloquea**
- [ ] IA: conectar API keys reales (Lovable AI Gateway + OpenAI)
- [ ] Email: Resend + Lovable Email
- [ ] Decidir si el billing entra en el MVP o queda para después

**Criterio de salida:** todas las integraciones probadas y funcionando, o descartadas con razón.

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
- [ ] Métricas de uso
- [ ] Iterar sobre feedback real

---

## Notas de evolución

- Este roadmap es **vivo**: cada fase se revisa al alcanzarla. Si aprendemos algo que cambia el plan, se actualiza acá.
- La **Fase 1 (alpha local)** es la prioridad: es donde se valida que la arquitectura de independencia de vendor funciona.
- El **billing (Mercado Pago)** es el mayor riesgo técnico (nunca probado) — se aísla en la Fase 2 para no bloquear la alpha.
