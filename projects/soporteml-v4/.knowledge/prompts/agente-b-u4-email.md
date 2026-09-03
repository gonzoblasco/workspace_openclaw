# Prompt - Agente B, U4 (Email/Resend) + revisión de U3

> Copiar y pegar en el Agente B (VS Code). El workspace que tiene cargado es el mismo que el de Kanam, así que el proyecto está en `projects/soporteml-v4/`.

---

Estás trabajando en SoporteML V4, Fase 1 (pulido + integraciones). Sos el Agente B (VS Code). Tu rol en el pipeline de revisión cruzada: primero REVISAR la U3 del Agente A (validación visual), y luego DESARROLLAR la U4 (email/Resend).

## Contexto del pipeline
SoporteML V4 usa el pipeline A/B de revisión cruzada (skill agent-orchestration-pipeline): el Agente A desarrolla unidades impares, el B pares, y cada uno revisa la del otro antes de avanzar. El Agente A desarrolló U3 (validación visual). Tu trabajo tiene dos partes: (1) revisar U3 con ojos frescos, y (2) desarrollar U4.

## El proyecto
Todo vive en `projects/soporteml-v4/` (el workspace que tenés cargado es el mismo que el mío). El código está en la raíz de `projects/soporteml-v4/` (monorepo pnpm: apps/api, apps/web, packages/db). El `.knowledge/` (BRIEF, PLAN, STATUS, HANDOFF, PIPELINE-AB, ADR-001) está en `projects/soporteml-v4/.knowledge/`. Leé el HANDOFF, el PIPELINE-AB y el PRODUCT.md (si lo copiaste de v3) para contexto completo.

## Estado actual del repo
- Repo git: `gonzoblasco/soporteml-v4` (independiente).
- U1 (RAG), U2 (code-splitting) y U3 (validación visual) completadas. 34 tests verdes. Build sin warning de chunk.
- **Servidores dev corriendo desde v4:** API en `localhost:3001`, web en `localhost:5173`.
- **Nota operativa:** el pre-commit hook usa `turbo`, que en el sandbox de VS Code falla con un I/O error al leer `~/Library/Application Support/com.vercel.cli/auth.json`. Corré `git commit` fuera del sandbox (o con `SKIP_SIMPLE_GIT_HOOKS=1` SOLO si ya verificaste lint + test manualmente).

## PARTE 1 - REVISAR la U3 del Agente A (cross-review)

El Agente A encontró y corrigió un bug de identidad visual. Verificá con ojos frescos:

### Cambios de U3 (commit `e0aeac4`)
- **Bug:** la app cargaba en tema claro por default. `main.tsx` usaba `defaultTheme="system"` en `next-themes`, y en un OS claro el `<html>` tomaba la clase `light`, sobreescribiendo los tokens oscuros de `:root`. Como ADR-001 define la oscura premium como identidad principal, la app perdía toda la identidad V4 en OS claros.
- **Fix:** `defaultTheme="dark"` en `main.tsx` (se quitó `enableSystem`). El toggle de tema del sidebar sigue permitiendo cambiar a claro.

### Puntos de revisión
1. **Que el fix no rompió el toggle de tema** - el usuario todavía puede cambiar a claro y volver a oscuro.
2. **Que la identidad oscura se mantenga en todas las vistas** - navegá por las 7 vistas (Inbox, Productos, Plantillas, KB, Clientes, Métricas, Ajustes) en el browser (`localhost:5173`) y verificá que todas se ven consistentes con ADR-001 (base `#0a0e1a`, acento MeLi con glow, color por categoría).
3. **Que no haya regresiones** - login, sync, responder, navegar funcionan.
4. **Que el `disableTransitionOnChange` no cause problemas** de flash al cargar.

### Reglas de la revisión
- Si encontrás bugs, corregilos (commit aparte, con mensaje claro).
- Documentá el resultado de tu revisión en el HANDOFF.

## PARTE 2 - DESARROLLAR la U4: Email (Resend)

### Contexto
El schema ya modela `sla_alert_emails` en `company_settings` (array de emails para alertas SLA), y la UI de Ajustes ya expone ese campo. Pero **no hay integración de email real** - las alertas SLA solo se muestran como banner en la bandeja. La U4 es implementar el envío real de emails (Resend) para las alertas SLA.

### Requisitos
1. **Servicio de email** (`apps/api/src/email-service.ts` o similar) que use **Resend** para enviar emails.
2. **Alerta SLA por email:** cuando `SlaService.detect()` encuentra consultas vencidas, enviar un email a los `sla_alert_emails` configurados con el detalle de las consultas vencidas.
3. **Configurable por env:** la clave de Resend se lee de `RESEND_API_KEY` en `.env` (NO hardcodear). Si no hay clave, **degradar a modo dev**: loguear el email que se habría enviado (patrón del mock de MeLi con `MELI_MOCK`).
4. **No romper el flujo actual:** si Resend falla o no hay clave, la app sigue funcionando (las alertas SLA siguen apareciendo en el banner).

### Criterios de aceptación
1. Servicio de email con Resend, configurable por env (`RESEND_API_KEY`), con degradación a modo dev si no hay clave.
2. Las alertas SLA disparan un email a los `sla_alert_emails` configurados (con detalle de consultas vencidas).
3. El email NO se envía repetidamente por la misma alerta (idempotencia - las alertas ya marcadas no re-notifican).
4. Tests: al menos 1 test que verifique que en modo dev (sin clave) el servicio loguea pero no falla, y que el disparo de alertas llama al servicio.
5. Build + tests + lint verdes.

### Archivos relevantes
- `apps/api/src/sla-service.ts` - `detect()` encuentra las consultas vencidas
- `apps/api/src/app.ts` - endpoint `GET /sla/alerts` (ahí se detecta)
- `packages/db/src/repo/settings.ts` - `sla_alert_emails` (destinatarios)
- `apps/api/src/meli/client.ts` - patrón de cómo se lee env y se degrada a mock
- `apps/api/src/index.ts` - dónde se configura el puerto/env
- `apps/api/src/app.test.ts` - tests del API

### Nota sobre la clave de Resend
No hay `RESEND_API_KEY` configurada todavía. Implementá la lectura de env con degradación a modo dev. Si necesitás probar el envío real, avisá (necesita una clave de Resend que Gonzo debe configurar en `.env`).

## Reglas
- Commit atómico + push. Idealmente 1-2 commits para U4 (servicio + wiring + tests).
- Commits en inglés, UI/prompts en español.
- No romper invariantes: multi-tenant, ADRs, identidad V4, a11y.
- Verificación obligatoria: build + tests + lint verdes antes de commitear.
- Actualizar docs: al cerrar U4, marcar U4 como hecha en `PLAN.md` y `STATUS.md` (en `.knowledge/`), y commitear los docs al repo v4.
- Dejar nota para el Agente A (próximo en la cadena) en el HANDOFF.

## Nota para el próximo agente (Agente A)
Dejá un mensaje claro de qué revisaste de U3, qué implementaste en U4, y qué necesita revisión del Agente A. Mencioná si dejaste la integración de Resend en modo dev (sin clave) esperando que Gonzo configure la clave real.
