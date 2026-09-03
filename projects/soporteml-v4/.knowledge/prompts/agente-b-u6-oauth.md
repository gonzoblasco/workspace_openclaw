# Prompt - Agente B, U6 (OAuth MeLi real) + revisión de U5

> Copiar y pegar en el Agente B (VS Code). El workspace que tiene cargado es el mismo que el de Kanam, así que el proyecto está en `projects/soporteml-v4/`.

---

Estás trabajando en SoporteML V4, Fase 1 (pulido + integraciones). Sos el Agente B (VS Code). Tu rol en el pipeline de revisión cruzada: primero REVISAR la U5 del Agente A (Mercado Pago billing), y luego DESARROLLAR la U6 (OAuth MeLi real). **U6 es la última unidad de la Fase 1.**

## Contexto del pipeline
SoporteML V4 usa el pipeline A/B de revisión cruzada (skill agent-orchestration-pipeline): el Agente A desarrolla unidades impares, el B pares, y cada uno revisa la del otro antes de avanzar. El Agente A desarrolló U5 (MP billing). Tu trabajo tiene dos partes: (1) revisar U5 con ojos frescos, y (2) desarrollar U6.

## El proyecto
Todo vive en `projects/soporteml-v4/` (el workspace que tenés cargado es el mismo que el mío). El código está en la raíz de `projects/soporteml-v4/` (monorepo pnpm: apps/api, apps/web, packages/db). El `.knowledge/` (BRIEF, PLAN, STATUS, HANDOFF, PIPELINE-AB, ADR-001) está en `projects/soporteml-v4/.knowledge/`. Leé el HANDOFF, el PIPELINE-AB y el BACKEND-REFERENCE (si lo copiaste de v3) para contexto completo.

## Estado actual del repo
- Repo git: `gonzoblasco/soporteml-v4` (independiente).
- U1-U5 completadas. 45 tests verdes. Build sin warning de chunk.
- **Servidores dev corriendo desde v4:** API en `localhost:3001`, web en `localhost:5173`.
- **Nota operativa:** el pre-commit hook usa `turbo`, que en el sandbox de VS Code falla con un I/O error al leer `~/Library/Application Support/com.vercel.cli/auth.json`. Corré `git commit` fuera del sandbox (o con `SKIP_SIMPLE_GIT_HOOKS=1` SOLO si ya verificaste lint + test manualmente).

## PARTE 1 - REVISAR la U5 del Agente A (cross-review)

El Agente A implementó el billing de Mercado Pago. Verificá con ojos frescos:

### Cambios de U5 (commits `9b743d5` + `3b59857`)
1. **`9b743d5`** - fix de U4: `SlaService.alertsFor` ahora filtra por `company_id` (multi-tenant) y `sla_alert_sent_at === null` (idempotencia).
2. **`3b59857`** - U5: `apps/api/src/mp/client.ts` (nuevo) conecta la API de preapproval de MP, `BillingService` degrada a mock sin credenciales, webhook IPN `POST /billing/webhook`.

### Puntos de revisión
1. **Que la degradación a mock sea correcta** - sin `MP_ACCESS_TOKEN`, el servicio sigue funcionando en modo mock (patrón `MELI_MOCK`).
2. **Que el webhook no rompa nada en mock** - `POST /billing/webhook` sin credenciales no debe fallar ni hacer nada raro.
3. **Que `MpClient` sea inyectable** - para testear sin credenciales reales.
4. **Que el fix de U4 (alertsFor) sea correcto** - multi-tenant + idempotencia.

### Reglas de la revisión
- Si encontrás bugs, corregilos (commit aparte, con mensaje claro).
- Documentá el resultado de tu revisión en el HANDOFF.

## PARTE 2 - DESARROLLAR la U6: OAuth MeLi real

### Contexto
El flujo OAuth de MeLi ya está implementado en el código (PKCE S256, state + code_verifier, exchange de code por tokens, refresh automático en `token-service.ts`). El problema es de **validación real**: el `MELI_REDIRECT_URI` en `.env` apunta a un dominio de túnel cloudflared **temporal** (`bread-folks-proven-chocolate.trycloudflare.com`) que probablemente ya no existe, y `MELI_MOCK=1` está activo (no toca la API real de MeLi). La U6 es validar el flujo OAuth real de punta a punta.

### Requisitos
1. **Levantar un túnel persistente** con `cloudflared` (está instalado en `/opt/homebrew/bin/cloudflared`) que apunte al API (`localhost:3001`). El túnel debe ser **persistente** (no temporal) para que el callback de MeLi funcione de forma estable.
2. **Actualizar `MELI_REDIRECT_URI`** en `.env` al dominio del túnel persistente + `/meli/callback`.
3. **Desactivar el mock** (`MELI_MOCK=0` o quitar la variable) para que el flujo use la API real de MeLi.
4. **Validar el flujo OAuth real de punta a punta:** `/meli/connect` genera la URL de autorización, MeLi redirige al callback, el code se intercambia por tokens, y el token se guarda en la DB.
5. **Verificar que el sync real funciona** - con el token real, `POST /meli/sync` trae preguntas reales de MeLi.

### Criterios de aceptación
1. Túnel persistente levantado y apuntando al API.
2. `MELI_REDIRECT_URI` actualizado al dominio del túnel.
3. Flujo OAuth real validado de punta a punta (connect → autorización MeLi → callback → token guardado).
4. Sync real trae preguntas reales (o al menos no falla).
5. Si el flujo real no se puede completar (falta credencial, MeLi rechaza, etc.), documentar el bloqueo con detalle y dejar el código listo para cuando se pueda.

### Archivos relevantes
- `apps/api/src/app.ts` - endpoints `/meli/connect` y `/meli/callback` (líneas ~78-123)
- `apps/api/src/meli/client.ts` - `buildAuthUrl`, `exchangeCode`
- `apps/api/src/meli/token-service.ts` - guarda/refresca tokens
- `apps/api/src/meli/sync-service.ts` - sync de preguntas
- `apps/api/.env` - `MELI_APP_ID`, `MELI_SECRET_KEY`, `MELI_REDIRECT_URI`, `MELI_MOCK`
- `apps/api/src/index.ts` - `FORCE_MOCK` (lee `MELI_MOCK`)

### Nota sobre credenciales
Las credenciales de MeLi (`MELI_APP_ID`, `MELI_SECRET_KEY`) ya están en `.env`. El `MELI_REDIRECT_URI` debe coincidir con el dominio registrado en la app de MeLi (si el dominio del túnel cambia, hay que actualizarlo también en el panel de MeLi). Si no podés validar el flujo real por un bloqueo externo (dominio no registrado, credencial inválida), documentalo claramente.

## Reglas
- Commit atómico + push. Idealmente 1-2 commits para U6 (cambios de código + docs).
- Commits en inglés, UI/prompts en español.
- No romper invariantes: multi-tenant, ADRs, identidad V4, a11y.
- Verificación obligatoria: build + tests + lint verdes antes de commitear.
- Actualizar docs: al cerrar U6, marcar U6 como hecha en `PLAN.md` y `STATUS.md` (en `.knowledge/`), y commitear los docs al repo v4.
- Dejar nota en el HANDOFF con el estado final de la Fase 1.

## Nota de cierre de Fase 1
U6 es la última unidad de la Fase 1. Al cerrarla, actualizá el `STATUS.md` para reflejar que la Fase 1 está completa (o qué bloqueos quedaron), y dejá una nota clara de qué integraciones reales quedaron validadas y cuáles pendientes de credenciales/configuración de Gonzo.
