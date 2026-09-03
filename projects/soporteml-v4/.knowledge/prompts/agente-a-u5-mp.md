# Prompt - Agente A, U5 (Mercado Pago billing) + revisión de U4

> Copiar y pegar en el Agente A (VS Code). El workspace que tiene cargado es el mismo que el de Kanam, así que el proyecto está en `projects/soporteml-v4/`.

---

Estás trabajando en SoporteML V4, Fase 1 (pulido + integraciones). Sos el Agente A (VS Code). Tu rol en el pipeline de revisión cruzada: primero REVISAR la U4 del Agente B (email/Resend), y luego DESARROLLAR la U5 (Mercado Pago billing).

## Contexto del pipeline
SoporteML V4 usa el pipeline A/B de revisión cruzada (skill agent-orchestration-pipeline): el Agente A desarrolla unidades impares, el B pares, y cada uno revisa la del otro antes de avanzar. El Agente B desarrolló U4 (email/Resend). Tu trabajo tiene dos partes: (1) revisar U4 con ojos frescos, y (2) desarrollar U5.

## El proyecto
Todo vive en `projects/soporteml-v4/` (el workspace que tenés cargado es el mismo que el mío). El código está en la raíz de `projects/soporteml-v4/` (monorepo pnpm: apps/api, apps/web, packages/db). El `.knowledge/` (BRIEF, PLAN, STATUS, HANDOFF, PIPELINE-AB, ADR-001) está en `projects/soporteml-v4/.knowledge/`. Leé el HANDOFF, el PIPELINE-AB y el ADR-003 (billing post-MVP) si existe para contexto completo.

## Estado actual del repo
- Repo git: `gonzoblasco/soporteml-v4` (independiente).
- U1 (RAG), U2 (code-splitting), U3 (validación visual) y U4 (email/Resend) completadas. 39 tests verdes. Build sin warning de chunk.
- **Servidores dev corriendo desde v4:** API en `localhost:3001`, web en `localhost:5173`.
- **Nota operativa:** el pre-commit hook usa `turbo`, que en el sandbox de VS Code falla con un I/O error al leer `~/Library/Application Support/com.vercel.cli/auth.json`. Corré `git commit` fuera del sandbox (o con `SKIP_SIMPLE_GIT_HOOKS=1` SOLO si ya verificaste lint + test manualmente).

## PARTE 1 - REVISAR la U4 del Agente B (cross-review)

El Agente B implementó el email service con Resend. Verificá con ojos frescos:

### Cambios de U4 (commit `22baacb`)
1. **`apps/api/src/email-service.ts`** (nuevo) - `EmailService` usa la API HTTP de Resend (fetch, sin dependencia nueva), lee `RESEND_API_KEY` del env. Sin clave → degrada a modo dev (loguea el email, no falla). Un fallo de Resend también degrada a dev.
2. **`apps/api/src/sla-service.ts`** - nuevo `alertsFor(companyId, questionIds)` que reutiliza el cálculo de atraso.
3. **`apps/api/src/app.ts`** - `POST /sla/mark-alerted` notifica a `sla_alert_emails` con el detalle de las vencidas. Inyectable (`SlaNotifier` en `AppConfig.email`) para tests.
4. **Tests** - 5 nuevos (3 unit + 2 integración). Total 39 verdes.

### Puntos de revisión
1. **Que el email service sea robusto** - no lanza nunca, degrada a dev sin clave, escapa HTML (previene inyección).
2. **Que el disparo sea idempotente** - las alertas ya marcadas (`sla_alert_sent_at IS NULL`) no re-notifican.
3. **Que el wiring en `mark-alerted` no rompa el flujo** - el email nunca debe romper el marcado de la alerta.
4. **Que el HTML del email use la identidad V4** (fondo `#0a0e1a`, acento `#ffe600`).

### Reglas de la revisión
- Si encontrás bugs, corregilos (commit aparte, con mensaje claro).
- Documentá el resultado de tu revisión en el HANDOFF.

## PARTE 2 - DESARROLLAR la U5: Mercado Pago billing

### Contexto
El billing actual es un **mock** (`apps/api/src/billing/service.ts`): `createSubscription` devuelve una URL de checkout ficticia, `confirmSubscription` simula el pago exitoso (30 días), `cancelSubscription` pausa. ADR-003 dice que MP es post-MVP y **nunca fue probado**. La U5 es conectar el billing real de Mercado Pago (preapproval / suscripciones).

### Requisitos
1. **Integración real de MP** para suscripciones (preapproval): `createSubscription` debe crear un preapproval real en MP y devolver la URL de checkout real.
2. **Webhook IPN** de MP para confirmar pagos (reemplaza el `confirmSubscription` manual).
3. **Configurable por env:** las credenciales de MP se leen de env (`MP_ACCESS_TOKEN`, `MP_WEBHOOK_SECRET` o similar). NO hardcodear.
4. **Degradación a mock:** si no hay credenciales de MP configuradas, el servicio sigue funcionando en modo mock (patrón de `MELI_MOCK`). La app no debe romperse sin credenciales.
5. **No romper el flujo actual:** los endpoints `/billing/status`, `/billing/subscribe`, `/billing/confirm`, `/billing/cancel` siguen funcionando (en modo mock o real según credenciales).

### Criterios de aceptación
1. `createSubscription` crea un preapproval real en MP (si hay credenciales) o devuelve la URL mock (si no).
2. Webhook IPN de MP confirma el pago y activa la suscripción (si hay credenciales).
3. Degradación a mock sin credenciales - la app funciona igual.
4. Tests: al menos 1 test que verifique que sin credenciales el servicio degrada a mock, y que el flujo de suscripción funciona en modo mock.
5. Build + tests + lint verdes.

### Archivos relevantes
- `apps/api/src/billing/service.ts` - el servicio mock actual
- `apps/api/src/app.ts` - endpoints `/billing/*` (líneas ~471-489)
- `apps/api/src/meli/client.ts` - patrón de cómo se lee env y se degrada a mock
- `apps/api/src/index.ts` - dónde se configura el puerto/env
- `apps/api/src/app.test.ts` - tests del API
- `packages/db/src/schema.ts` - tabla `companies` (billing_status, plan, mp_preapproval_id)

### Nota sobre credenciales de MP
No hay credenciales de MP configuradas. Implementá la lectura de env con degradación a mock. Si necesitás probar el flujo real, avisá (necesita un access token de sandbox de MP que Gonzo debe configurar en `.env`).

## Reglas
- Commit atómico + push. Idealmente 1-2 commits para U5 (servicio + wiring + tests).
- Commits en inglés, UI/prompts en español.
- No romper invariantes: multi-tenant, ADRs, identidad V4, a11y.
- Verificación obligatoria: build + tests + lint verdes antes de commitear.
- Actualizar docs: al cerrar U5, marcar U5 como hecha en `PLAN.md` y `STATUS.md` (en `.knowledge/`), y commitear los docs al repo v4.
- Dejar nota para el Agente B (próximo en la cadena) en el HANDOFF.

## Nota para el próximo agente (Agente B)
Dejá un mensaje claro de qué revisaste de U4, qué implementaste en U5, y qué necesita revisión del Agente B. Mencioná si dejaste la integración de MP en modo mock (sin credenciales) esperando que Gonzo configure las credenciales reales.
