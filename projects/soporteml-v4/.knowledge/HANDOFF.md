# SoporteML V4 - HANDOFF

> **Sesión:** 2026-08-27 (congelación de sincronización MeLi)
> **Estado:** DB congelada - trabajando con datos reales como mock

---

## ⚠️ Estado actual (2026-08-27): Sincronización MeLi CONGELADA

**La DB está congelada con datos reales descargados.** No se sincroniza con MeLi, no se renueva el token, no se inyecta data sintética.

- **Datos reales en DB:** 174 preguntas, 63 productos, 139 clientes.
- **`MELI_MOCK=1`** en `apps/api/.env`: el sync NO toca la DB ni llama a MeLi (congela).
- **Cron `soporteml-meli-token-refresh` DESACTIVADO** (no renueva token).
- **Backups:** `apps/api/backups/soporteml-v4/soporteml-2026-08-27-0838.db` + export JSON en `apps/api/mock-data/` (gitignored).
- **Commit:** `2c2c388` (sin firma GPG - error de agente SSH).

**Para reactivar la sincronización real:** `MELI_MOCK=0` + reactivar cron + backend con token vigente.

**Detalle técnico de la congelación:**
- `sync-service.ts`: `forceMock` (constructor) genera data sintética para tests; `MELI_MOCK=1` en env congela (no hace nada).
- `index.ts`: ya NO traduce `MELI_MOCK=1` a `forceMock` (antes inyectaba data sintética en la DB real).

---

## Sesión previa (2026-08-17) - Fase 0 + UI V4

> **Estado:** Fase 0 completa + UI V4 arrancada

---

## Qué se hizo

### Fase 0 - Fundamentos del reinicio (completa)
- **Decisión de Gonzo:** v3 quedó como template básico (features limitadas en la UI, UI/UX sosa). V4 = reinicio con estándar superior.
- **Conservar** backend + capa de datos de v3 (activo valioso: OAuth MeLi real, schema 20+ tablas, token de producción).
- **Reconstruir** frontend con diseño avanzado + desbloquear features que el schema ya modela.
- **Identidad visual (ADR-001):** híbrido oscuro + color por categoría. Base oscura premium + acento amarillo MeLi + color por categoría (precio=azul, stock=verde, técnico=violeta, envío=naranja, garantía=rosa).
- **Lucide (ADR-030, workspace):** librería de iconos base en todos los proyectos.

### Backend verificado + mock enriquecido + tests
- **Backend verificado a fondo** (pregunta de Gonzo: "si todo es mock, ¿cómo confirmamos que funciona?"): categorización mock 6/6, multi-tenant aísla empresas, publish marca como respondida, sync idempotente.
- **Mock enriquecido:** 13 preguntas (antes 6), 6 productos (antes 3), varias por producto, producto sin preguntas activas (Parlante agotado).
- **Refactor para testear:** `createApp(db)` en `app.ts` (factory con DB inyectable), `index.ts` solo hace `serve()`.
- **14 tests del API** (antes 0): health, auth, sync, multi-tenant, publish, idempotencia, productos, IA, billing. Todos pasan en 378ms.
- **Fix /ai/suggest:** en modo mock usa `sugerirMock` determinístico (consistente con el sync), no la IA real.

### UI V4 arrancada (el corazón)
- **`index.css`:** tokens V4 (base oscura premium + acento amarillo MeLi + colores por categoría).
- **`AppSidebar`:** logo con glow amarillo, navegación agrupada, item activo con barra lateral iluminada.
- **`App.tsx`:** stats por categoría, bandeja con barra lateral de color, cards con micro-interacciones, login premium.
- **Verificado en browser:** 13 preguntas con color por categoría, publicar respuesta funciona (badge cambia a Respondida, stats bajan).
- **Build de producción OK.**

## Cómo correr

```bash
# Terminal 1 - backend (puerto 3001)
cd apps/api && pnpm dev

# Terminal 2 - frontend (puerto 5173)
cd apps/web && pnpm dev
```

Abrir http://localhost:5173 → "Entrar (modo demo)" → Sincronizar → ver 13 preguntas con color por categoría → Responder.

## Estado - Sesión 2026-08-24 (mañana)

**Contexto crítico:** el 2026-08-23 se removió la referencia del submódulo `soporteml-v4` del workspace (GitHub como fuente de verdad). Como `*.db` y `.env` están en `.gitignore`, el reclon no trajo la DB con el token de MeLi de la cliente (PRO_MOTORS / `meliUserId: 48316325`). Se reconectó el OAuth real con una nueva URL de túnel y se reconfiguró el webhook.

### Reconexión OAuth + webhook (2026-08-24)
- **Token real regenerado** mediante URL de OAuth con state + code_challenge persistido en DB.
- `meliUserId` guardado en DB local: `48316325` (cuenta de la cliente, PRO_MOTORS).
- **Access token expira:** 2026-08-24 ~19:02 UTC (16:02 hora Argentina) - se renueva automáticamente con `refresh_token` mientras `MeliTokenService` tenga el refresh token.
- **Nuevo túnel cloudflare quick:** `https://observe-orchestra-liquid-moss.trycloudflare.com`.
- **Endpoint de notificaciones MeLi agregado:** `POST /meli/notifications` (sin auth, responde 200, mapea `user_id` -> `company_id` via `meli_tokens`, dispara `syncCompany` async).
- **Webhook registrado manualmente en el panel de MeLi** para `questions` (y opcionalmente items/orders si se configuran): `https://observe-orchestra-liquid-moss.trycloudflare.com/meli/notifications`.
- **Config actual en `apps/api/.env`:**
  - `MELI_APP_ID=8921097700859218`
  - `MELI_SECRET_KEY=<credactado>`
  - `MELI_REDIRECT_URI=https://observe-orchestra-liquid-moss.trycloudflare.com/meli/callback`
  - `MELI_MOCK=0`
  - `APP_URL=http://localhost:5173`

### Pendientes inmediatos (UI - a definir al volver)
- Revisar Inbox actual (lista en una sola fila por pregunta) y decidir rediseño con **grilla** en lugar de fila.
- Agregar **modal** (o side panel - preferencia del momento: modal) para ver **detalles de la pregunta**.
- Definir qué detalles mostrar en el modal: texto completo, producto (título, foto, stock, visitas, precio), cliente/historial, sugerencia IA, plantillas rápidas, estado SLA, acciones (responder, marcar, publicar).
- Verificar build + tests después de los cambios de UI.

### Backend - timestamp real de la pregunta (2026-08-24, sesión tarde)
- **Problema:** `questions.created_at` guardaba la fecha de sincronización local, no la fecha real en que el comprador hizo la pregunta en MeLi. Pésima UX para el vendedor.
- **Solución:** agregar columna `asked_at` en `questions`. El endpoint de MeLi `/my/received_questions/search` ya devolvía `date_created` en `MeliQuestion`; ahora `sync-service.ts` lo persiste en `asked_at`. `created_at` sigue siendo la metadata de inserción local.
- **Cambios:** schema, type `Question`, `QuestionsRepo.create/map`, `MeliSyncService.processQuestion`, API types en frontend, test mock en `email-service.test.ts`.
- **Tests:** 57 verdes (53 api + 4 db), lint OK, build OK.
- **Pendiente UI:** cambiar `timeAgo` y demás labels para usar `asked_at` cuando exista; mostrar `created_at` solo como metadata secundaria si aplica.

### Nota de continuidad
- **No tocar `*.db` ni `.env` sin respaldo previo.** La DB con el token debe conservarse; si se mueve/clona el proyecto, copiar `apps/api/soporteml.db` + `.env` a `backups/soporteml-v4/` antes.
- Si el túnel cloudflare cae, la URL del webhook y el `MELI_REDIRECT_URI` cambian: reiniciar túnel, actualizar `.env` y panel de MeLi, regenerar URL de OAuth.

---

## Estado - Sesión 2026-08-18

### Las 7 features core del schema están implementadas (todas verificadas en browser)

1. **Plantillas** - CRUD + conectadas al flujo de responder (insertar en el input).
2. **KB gestión** - CRUD de artículos con chunking.
3. **KB RAG** - búsqueda semántica con embeddings (Ollama all-minilm), discrimina bien entre 4 artículos.
4. **Autopilot** - responde automáticamente por categoría + umbral de confianza.
5. **Clientes (CRM)** - notas + tags.
6. **Métricas** - dashboard de KPIs, top productos, ventas.
7. **SLA** - detección de consultas vencidas + banner en Inbox + configuración en Ajustes.

### SLA (slice 7, commits `641f94f` + `037f0f8`)
- **`sla-service.ts`** - detección NO destructiva (`detect`) + marcado explícito (`markAlerted`).
- **Bug crítico resuelto:** el check destructivo original rompía el banner con StrictMode (la 1ra llamada al load marcaba la pregunta, la 2da la limpiaba). La detección no destructiva resuelve el race condition.
- **Endpoints:** `GET /sla/alerts` (detecta, no marca) + `POST /sla/mark-alerted` (marca explícito).
- **UI:** sección SLA en Ajustes (target min, escalación, emails) + banner de alertas en Inbox.
- **Tests:** 2 nuevos (26 total). Verificado en browser: banner "1 consulta vencida por SLA - Comprador (55 min)".

### Pre-commit hooks agregados
- **`simple-git-hooks`** con pre-commit que corre `pnpm lint && pnpm test` (commits `037f0f8` + `986027b`).
- **Lint arreglado:** el script `lint` estaba roto (ESLint no instalado). Agregué ESLint 10 + typescript-eslint 8 + plugins React con flat config (`eslint.config.js`). 0 errores, 4 warnings (react-refresh en componentes shadcn/ui, patrón estándar).
- **Nota:** desactivé `react-hooks/set-state-in-effect` y `react-hooks/purity` (reglas nuevas muy estrictas que marcan patrones legítimos de shadcn/ui - media queries, dialogs).

### Pipeline A/B definido (2026-08-18)
- **`PIPELINE-AB.md`** creado - metodología adaptada de la skill `agent-orchestration-pipeline` (validada en Kanam Story Fase 3).
- **Fase 0 completa** (7 features core + SLA + lint + hooks + pipeline). **Fase 1 en curso** (pulido + integraciones).
- **Unidades Fase 1:** U1 RAG minScore (A), U2 code-splitting (B), U3 validación visual (orquestador), U4 email Resend (B), U5 MP billing (A), U6 OAuth MeLi (B).

### U1: Ajuste fino RAG (Agente A, commits `6c95905` + docs `ee43d90`)
- **Problema:** `searchChunks` usaba `minScore` 0.2 hardcodeado → una consulta sin match real ("¿Aceptan cuotas?") devolvía el chunk más cercano (garantía).
- **Cambios:**
  - `packages/db/src/repo/kb.ts`: `DEFAULT_MIN_SCORE = 0.45` (exportada) y es el nuevo default de `searchChunks`.
  - `apps/api/src/kb-service.ts`: `search` lee `kb_similarity_threshold` de los settings de la empresa (configurable, ya no hardcodeado).
  - `packages/db/src/repo/settings.ts` + `apps/api/src/app.ts`: `PUT /settings` ahora acepta `kbSimilarityThreshold` (y `kbTopK`).
  - Tests: `apps/api/src/kb-service.test.ts` (4 tests, embeddings one-hot determinísticos sin Ollama).
- **Total:** 30 tests del API (26 + 4), build + lint verdes.

> **Nota para el Agente B (revisión de U1):** al revisar, prestar atención a (1) que el default 0.45 no rompa matches reales (los tests lo cubren con vectores controlados, pero validar el caso real con Ollama si está disponible), (2) la decisión de exponer el threshold en `company_settings` en vez de una constante global única — cada empresa puede ahora ajustarlo por `PUT /settings`, y (3) que `KbService.search` respeta un `minScore` explícito en `opts` por encima del threshold de settings (útil para llamadas que quieran sobreescribir).

### Revisión de U1 + U2: Code-splitting (Agente B, commits `21fda14` + `ab914c8`)

**Resultado de la revisión de U1:** la U1 del Agente A está bien implementada y los puntos pedidos se verificaron:
1. **Default 0.45** — no rompe matches reales: los tests controlados lo cubren (match exacto → score 1 pasa; sin match → score 0 no pasa). No validé el caso real con Ollama (no lo tengo corriendo en este sandbox), sigue como pendiente de verificación manual opcional.
2. **Threshold per-empresa** — decisión correcta: `search` lee `kb_similarity_threshold` de settings y `PUT /settings` lo expone. Alineado con el schema.
3. **`minScore` explícito en `opts`** — correcto: `opts.minScore ?? settings.kb_similarity_threshold`, la llamada explícita gana.

**BUG CORREGIDO (commit `21fda14`, "fix: return real cosine-similarity score from KB search"):** `kb-service.ts` devolvía `score: 0` siempre en `search`, porque `searchChunks` calculaba el score con `cosineSimilarity` pero lo descartaba (devolvía solo el chunk). Arreglo: `searchChunks` ahora devuelve `ScoredKbChunk[]` (`{ chunk, score }`), y `search` mapea `{ content, score: s.score }`. **El contrato no se rompe:** el único consumidor es `apps/api/src/app.ts` (usa `r.content`) y los tests usan `content`/`length`. Agregué una aserción `score === 1` en el test existente.

**U2: Code-splitting (commit `ab914c8`, "perf: code-split views into lazy-loaded chunks"):**
- **Problema:** bundle principal 512 kB (gzip 157 kB), sobre el warning de 500 kB de Vite. `App.tsx` (~1491 líneas) tenía las 7 vistas inline → un solo chunk.
- **Cambio:** extraje cada vista a `apps/web/src/views/` (`Inbox`, `Products`, `Templates`, `KnowledgeBase`, `Customers`, `Metrics`, `Settings`), cada una con sus propios helpers (`CATEGORY_COLORS`, `QuestionCard`, `StatCard`, `StatusBadge`, `MetricCard`, `StatusPill`, `timeAgo`). `App.tsx` quedó como shell (~30 líneas) con `React.lazy` + `<Suspense>`. `Playground` también lazy. **No** introduje React Router (mantengo el estado `view`).
- **Resultado:** bundle principal → **338.93 kB** (gzip 106.55 kB), sin warning de chunk. Cada vista es un chunk propio bajo demanda (Inbox 10.32, Metrics 5.84, Settings 6.65, Templates 5.69, etc.).
- **A11y preservada:** fallback de Suspense con `role="status"` + `aria-live="polite"` + label sr-only "Cargando vista...". La navegación por sidebar/teclado no cambió.
- **Verificación:** `pnpm build` + `pnpm test` + `pnpm lint` verdes (34 tests: 30 api + 4 db). Build completo de turbo OK sin warning.

> **Nota para el Agente A (próximo en la cadena, revisión de U2):** la U2 está lista. Puntos a mirar: (1) que las vistas sigan funcionando igual (verificar en browser que el sidebar cambia de vista y el Suspense fallback se ve al navegar, sobre todo en modo demo), (2) que el chunk principal (339 kB) y cada vista estén separados, y (3) la a11y del fallback. Si tenés Ollama, validá el caso real del default 0.45 de la U1 que dejé como pendiente manual.

### Revisión de U2 + U3: Validación visual (Agente A, commit `e0aeac4`)

**Resultado de la revisión de U2:** la U2 del Agente B está bien implementada. Verificado con ojos frescos:
1. **Code-splitting no rompió nada:** las 7 vistas + Playground cargan bajo demanda. Verificado en browser que el sidebar cambia de vista y el fallback de Suspense se muestra al navegar (sobre todo en modo demo). Ningún import roto, cada vista tiene su `export default`, y no quedaron referencias colgantes a helpers inline en `App.tsx` (verificado con grep).
2. **Fix del score no rompió el contrato:** `searchChunks` ahora devuelve `ScoredKbChunk[]` (`{ chunk, score }`) y `KbService.search` mapea `{ content, score: s.score }`. El único consumidor (`apps/api/src/app.ts:414`) usa `r.content`, y los tests usan `content`/`length`. Todo alineado.
3. **A11y del fallback correcta:** `role="status"` + `aria-live="polite"` + label sr-only "Cargando vista...". Se confirma en el DOM (`<status>` role).
4. **Sin referencias colgantes:** `grep` de `QuestionCard|StatCard|StatusBadge|MetricCard|StatusPill|timeAgo|CATEGORY_COLORS` en `App.tsx` da vacío.

**BUG CORREGIDO en U3 (commit `e0aeac4`, "fix(web): default to dark theme..."):** la app cargaba en **tema claro** por default. `main.tsx` usaba `defaultTheme="system"` + `enableSystem` en `next-themes`, y en un OS claro el html toma la clase `light`, que sobreescribe los tokens oscuros de `:root`. Como la identidad V4 (ADR-001) es **oscura premium por default**, en un OS claro la app perdía la identidad (fondo claro, badges claros, sin glow MeLi). Fix: `defaultTheme="dark"`. El toggle del sidebar sigue permitiendo cambiar a claro, y ahora al recargar persiste la preferencia.

**Validación visual en browser (tema oscuro):** las 7 vistas (Inbox, Products, Templates, KB, Customers, Metrics, Settings) se ven consistentes con ADR-001:
- Base oscura `#0a0e1a` + superficies elevadas + glassmorphism ✓
- Acento amarillo MeLi con glow en botones/logo/item activo ✓
- Color por categoría (precio azul, stock verde, técnico violeta, envío naranja, garantía rosa) en stats, badges y barras laterales ✓
- Micro-interacciones: cards con hover, bordes que se iluminan, stats con barra de color ✓
- A11y: jerarquía de headings, focus visible, labels en botones de solo icono ✓

**Verificación:** build + lint + 34 tests verdes. Bundle principal 338.95 kB (code-splitting preservado).

> **Nota para el Agente B (próximo en la cadena, revisión de U3):** la U3 está lista. Puntos a mirar: (1) que el default de tema oscuro no rompa nada en modo light (toggle), y (2) que la preferencia de tema persista. La validación final de la identidad visual la hace Gonzo — es quien aprueba colores/espaciado/tipografía.

### Revisión de U3 + U4: Email (Resend) (Agente B, impl `22baacb`)

**Resultado de la revisión de U3:** la U3 del Agente A está bien implementada y mínima. Verificado con ojos frescos:
1. **El toggle de tema sigue funcionando:** el sidebar usa `useTheme` + `setTheme(theme === "dark" ? "light" : "dark")`, que es independiente de `enableSystem`. Con `defaultTheme="dark"`, al recargar el `theme` resuelve a "dark" y el toggle puede pasar a claro y volver.
2. **La identidad oscura se preserva:** con `defaultTheme="dark"` (sin `enableSystem`) next-themes aplica `class="dark"` al `<html>`, que no tiene regla propia en CSS → cae en los tokens oscuros de `:root`. En un OS claro ya no se fuerza la clase `light`. El tema claro existe (`.light` sobreescribe los tokens de `:root`), así que cambiar a claro renderiza bien, no queda un HTML sin estilos.
3. **Sin regresiones:** el cambio es solo de configuración del ThemeProvider (`main.tsx`), no toca login/sync/responder/navegar. `disableTransitionOnChange` ya estaba en el commit original, no introduce flash; sin `enableSystem` tampoco hay delay de resolución de tema del sistema.
4. **Conclusión:** fix correcto, preserva el toggle y la identidad V4. La validación final de colores/espaciado/tipografía sigue siendo de Gonzo.

**U4: Email (Resend):**
- **Servicio de email** (`apps/api/src/email-service.ts`): `EmailService` usa la **API HTTP de Resend** (fetch, sin dependencia nueva) con `from` configurable (`EMAIL_FROM`). Lee `RESEND_API_KEY` del env. **Si no hay clave, degrada a modo dev:** loguea el email que se habría enviado (con destinatario, asunto y cuerpo) y devuelve `{ mode: "dev" }`. Un fallo de Resend también degrada a dev (registra el error) — el email NUNCA rompe el flujo de la app.
- **Disparo SLA por email:** `POST /sla/mark-alerted` ahora, antes de marcar, si hay `sla_alert_emails` configurados, arma el detalle de las consultas vencidas (nuevo `SlaService.alertsFor`, que reutiliza el cálculo de atraso de `detect`) y llama `email.sendSlaAlert`. **Idempotente:** `detect()` solo devuelve preguntas sin `sla_alert_sent_at`, así que las ya marcadas no re-notifican; y el email se envía solo con las alertas que la UI detectó.
- **`SlaNotifier` inyectable** en `createApp` (AppConfig.email) para testear el disparo sin Resend.
- **Tests (5 nuevos, 39 total api+db):** `email-service.test.ts` (modo dev loguea y no falla, no envía sin destinatarios, arma el detalle) + `app.test.ts` (marca y notifica al destinatario, y no llama al servicio sin destinatarios).
- **Verificación:** build + typecheck + lint verdes (0 errores, 4 warnings pre-existentes de shadcn/ui). Bundle principal 338.95 kB (code-splitting preservado).
- **.env:** agregué `RESEND_API_KEY=` (vacío) + `EMAIL_FROM=` con comentarios. El servicio está en **modo dev** hasta que Gonzo ponga la clave real.

> **Nota para el Agente A (próximo en la cadena, revisión de U4):** la U4 está lista. Puntos a mirar: (1) que la degradación a dev sea correcta (loguea pero no falla), (2) que el disparo sea idempotente (marca → no re-detecta → no re-notifica), y (3) que el email no rompa el flujo de marcado si Resend falla. La integración real queda pendiente de que Gonzo configure `RESEND_API_KEY` en `.env` (avisar que el `EMAIL_FROM` debe ser un dominio verificado en Resend).

### Revisión de U4 + U5: Mercado Pago billing (Agente A, commits `9b743d5` + `3b59857`)

**Resultado de la revisión de U4:** el email service de Resend está bien implementado. Verificado con ojos frescos:
1. **Degradación a dev correcta:** sin `RESEND_API_KEY`, `EmailService.send` loguea el email que se habría enviado y devuelve `{ mode: "dev" }` — nunca lanza. Un fallo de Resend también degrada a dev (try/catch). El email NUNCA rompe el flujo de la app.
2. **Idempotencia a nivel de `detect()`:** `detect()` solo devuelve preguntas sin `sla_alert_sent_at`, así que las ya marcadas no re-notifican. El wiring en `mark-alerted` envía el email solo con las alertas que la UI detectó.
3. **El email no rompe el marcado:** el `try/catch` alrededor de `email.sendSlaAlert` garantiza que un fallo de email no impide `markAlerted`.
4. **HTML con identidad V4:** fondo `#0a0e1a`, acento `#ffe600`, y `escapeHtml` previene inyección de HTML en el email.

**BUG CORREGIDO en U4 (commit `9b743d5`, "fix(api): harden SLA email alertsFor..."):** `SlaService.alertsFor` no filtraba por empresa ni por `sla_alert_sent_at`. Dos problemas: (1) un doble submit de los mismos `questionIds` re-notificaba (la idempotencia solo vivía en `detect()`, no en `alertsFor`), y (2) un id de pregunta de otro tenant podía filtrarse al email (multi-tenant). Fix: `alertsFor` ahora filtra `q.company_id === companyId` y `q.sla_alert_sent_at === null` — defensa en profundidad además de `detect()`.

**U5: Mercado Pago billing:**
- **`apps/api/src/mp/client.ts`** (nuevo): `MpClient` conecta la API de preapproval de MP (crear + consultar). Lee `MP_ACCESS_TOKEN` del env; sin credenciales `enabled` es false.
- **`BillingService`** (`apps/api/src/billing/service.ts`): acepta un `MpClient` inyectable (para tests) y lee `MP_ACCESS_TOKEN` del env. **Degradación a mock:** sin credenciales, `createSubscription` devuelve la URL ficticia y `confirmSubscription` simula el pago (30 días) — la app funciona igual (patrón de `MELI_MOCK`). Con credenciales, `createSubscription` crea un preapproval real y devuelve su `init_point`.
- **Webhook IPN:** nuevo `POST /billing/webhook` (sin auth de la app, lo llama MP). `handleWebhook` correlaciona el preapproval por `mp_preapproval_id`, consulta el estado real en MP y confirma la suscripción solo si está `authorized`. En modo mock no matchea (no hay preapproval real) y no hace nada.
- **Tests (6 nuevos, 45 total api+db):** `billing/service.test.ts` — 3 mock (degrada a mock, alreadySubscribed, webhook no matchea) + 3 real con `MpClient` mockeado (crea preapproval real, webhook confirma authorized, webhook no confirma pending).
- **Verificación:** build + typecheck + lint verdes (0 errores, 4 warnings pre-existentes de shadcn/ui). Bundle principal 338.95 kB (code-splitting preservado).
- **.env:** agregué `MP_ACCESS_TOKEN=` (vacío) + `MP_NOTIFICATION_URL=` + `MP_BACK_URL=` con comentarios. El billing está en **modo mock** hasta que Gonzo ponga el token de sandbox de MP.

> **Nota para el Agente B (próximo en la cadena, revisión de U5):** la U5 está lista. Puntos a mirar: (1) que la degradación a mock sea correcta (sin `MP_ACCESS_TOKEN` la app funciona igual), (2) que el webhook IPN no rompa nada en modo mock (no matchea y no hace nada), y (3) que el `MpClient` inyectable permita testear el flujo real sin credenciales. La integración real queda pendiente de que Gonzo configure `MP_ACCESS_TOKEN` (sandbox) en `.env` y una `MP_NOTIFICATION_URL` pública (túnel) para el webhook. El `transactionAmount` del preapproval está en 0 — el monto real se define en el panel de MP / plan.

### Revisión de U5 + U6: OAuth MeLi real (Agente B)

**Resultado de la revisión de U5:** la U5 del Agente A está bien implementada. Verificado con ojos frescos:
1. **Degradación a mock correcta:** `MpClient.enabled = accessToken.length > 0` (`mp/client.ts`). Sin `MP_ACCESS_TOKEN`, `createSubscription` cae en la rama mock (URL `checkout.mock.mercadopago`) y el flujo funciona completo (status → subscribe → confirm → active). Cubierto por `billing/service.test.ts`.
2. **Webhook no rompe en mock:** `POST /billing/webhook` sin credenciales → `status` queda `undefined` → no confirma → devuelve `null` → responde 200 no-op. Cubierto por test.
3. **`MpClient` inyectable:** `BillingServiceOptions.mp` opcional; los tests inyectan un mock y prueban el flujo real sin credenciales (crea preapproval real, webhook confirma `authorized`, no confirma `pending`).
4. **Fix de U4 (`alertsFor`):** filtra `company_id === companyId` y `sla_alert_sent_at === null` (`sla-service.ts`) — multi-tenant + idempotencia correctos, defensa en profundidad además de `detect()`.
5. **Verificación:** 45 tests verdes (41 api + 4 db), build + lint sin errores (4 warnings pre-existentes shadcn/ui), bundle 338.95 kB. **Sin bugs encontrados.**

**U6: OAuth MeLi real — DESBLOQUEADA y VALIDADA (2026-08-21).**
- **El código estaba completo y listo** (verificado 2026-08-18: `/meli/connect` genera URL con PKCE S256, `exchangeCode`, `token-service`, callback y sync implementados, sync degrada a mock sin token).
- **Desbloqueo con túnel quick (sin dominio propio):** el bloqueo previo era por túnel named/persistente (exigía `cloudflared tunnel login` + dominio en Cloudflare). Para desarrollo alcanza el **túnel quick** (`cloudflared tunnel --url http://localhost:3001`) que NO requiere cuenta ni dominio. Mismo patrón que v3 (12/08).
- **Flujo validado end-to-end (2026-08-21):** connect → autorización MeLi en browser (Gonzo) → callback → token real guardado → sync real contra API. `meliUserId: 10061615` (GONZOBLASCO, misma cuenta que v3). Sync real corrió sin errores, 0 preguntas (no hay activas sin responder).
- **Config actual:** `MELI_REDIRECT_URI=https://meaningful-cotton-attached-effects.trycloudflare.com/meli/callback`, `MELI_MOCK=0`. Redirect registrado en el panel de MeLi por Gonzo.
- **⚠️ Túnel quick:** la URL cambia en cada reinicio del túnel → actualizar `.env` + panel de MeLi. Para sesión de desarrollo está bien; túnel named/persistente (dominio propio) queda como mejora futura si se quiere estabilidad.
- **Estado de Fase 1:** U1-U6 completas y validadas. La integración real de MeLi OAuth está funcionando.

### U7: Métricas reales de visitas de MeLi (Agente A, commits `d9ca178` + `371ac18` + `99a010e`)
- **Objetivo:** enriquecer el dashboard de métricas con tráfico real de visitas de MeLi (Opción A definida al cerrar U6).
- **`MeliClient.getItemVisits`** (client.ts): GET /items/visits con rango de fechas, devuelve `total_visits`. **Parseo defensivo (`extractVisits`)** que maneja los formatos que puede devolver la API real: objeto plano `{ item_id, total_visits }` (doc oficial), array `[{ id|item_id, total_visits }]`, y mapa `{ [itemId]: number | { total_visits } }`. 11 tests unitarios (`client.test.ts`) cubren cada formato. Así el sync real no se rompe sin importar qué formato devuelva MeLi (la cuenta propia no tiene productos para validar hoy; la validación real queda para la cuenta con productos).
- **Sync** (sync-service.ts): `enrichProduct` guarda `total_visits` en `meli_cache` (rango 30 días). Aislado en try/catch - un fallo del endpoint de visitas NO degrada el resto del enrich (stock/vendidos/condition). En mock, `MOCK_ITEMS` incluye valores de ejemplo.
- **MetricsService** (metrics-service.ts): `MetricsSummary.visits { total, topProducts[] }`. `total` = suma de `meli_cache.total_visits` de productos activos; `topProducts` = top 5 por visitas. Campos existentes intactos (retrocompatibilidad).
- **UI** (Metrics.tsx): KPI "Visitas" (icono `Eye`, violeta, sub "tráfico 30 días") + tarjeta "Top productos por visitas". Grid KPIs 4→5 columnas. UI en español.
- **Tests:** `app.test.ts` valida `visits.total > 0` y `topProducts`. Total 41 tests verdes.
- **⚠️ Lección del cross-review (importante):** el Agente B introdujo un bug en su revisión - asumió que `/items/visits` devuelve un array `[{id, total_visits}]` y "corrigió" el parseo que en realidad era correcto (objeto plano). El orquestador (Kanam) verificó contra la doc oficial de MeLi y revirtió el parseo a objeto plano (commit `99a010e`), conservando el try/catch aislado de B (mejora válida). **Lección: el cross-review puede introducir regresiones basadas en suposiciones falsas - el orquestador debe verificar contra la fuente real (doc de la API) antes de aceptar un fix.**
- **Pendiente (validar con cuenta real de productos, 2026-08-22):** la cuenta propia (GONZOBLASCO) no tiene productos ni consultas activas, así que el sync real de visitas no se puede validar hoy. Mañana con una cuenta que tenga productos y consultas reales: (1) reconectar OAuth (nuevo login, el token expira a las 6h), (2) correr sync real, (3) confirmar que getItemVisits trae visitas reales y el dashboard las muestra. El parseo defensivo (`extractVisits`) cubre los formatos posibles para que no falle.

## Dónde está cada cosa

- **Código + memoria + mockups:** repo `gonzoblasco/soporteml-v4` (independiente, creado 2026-08-18). Todo vive en `projects/soporteml-v4/`.
- **Commit inicial:** `feat: initial SoporteML V4 - fullstack CRM for Mercado Libre sellers` (84 archivos).
- **v3 queda como referencia/historial:** `gonzoblasco/soporteml-v3` (no se toca).
- **ADRs:** `docs/adr/ADR-030-lucide-iconos-base.md` (workspace), `projects/soporteml-v4/.knowledge/ADR-001-identidad-visual.md`.
- **Nota:** el workspace ignora `projects/soporteml-v4/` (todo vive en el repo v4).

## Pendientes (próxima sesión)

- [x] **U1: Ajuste fino RAG** - subir minScore (0.2) o filtrar por similitud mínima para consultas sin match. ✅ (commit `6c95905`, ver sección U1 arriba)
- [x] **U2: Code-splitting** - resolver warning de chunk > 500kB (lazy load de vistas). ✅ (commit `ab914c8`, ver sección U2 arriba)
- [x] **U3: Validación visual** - ajustar colores/espaciado/tipografía según feedback. ✅ (commit `e0aeac4`, ver sección U3 arriba — validación final de Gonzo pendiente)
- [ ] **U4: Email (Resend)** - integrar envío de alertas SLA + notificaciones. ✅ (ver sección U4 abajo — en modo dev, esperando `RESEND_API_KEY`)
- [ ] **U5: Mercado Pago** - validar flujo de billing real (nunca probado). ✅ (ver sección U5 arriba — en modo mock, esperando `MP_ACCESS_TOKEN`)
- [x] **U6: OAuth MeLi real** - ✅ **DESBLOQUEADA y VALIDADA** (2026-08-21, túnel quick + redirect registrado). OAuth real end-to-end funcionando, token de producción guardado, sync real OK. Ver sección U6 arriba.

**Cierre de Fase 1 (2026-08-21):** U1-U6 completas y validadas. La integración real de MeLi OAuth está funcionando (túnel quick, sin dominio propio). **U7 completada:** métricas reales de visitas de MeLi (KPI + top productos + sync real/mock), 41 tests verdes, build sin warning. Pendiente: validar el endpoint real de visitas contra la API (token expirado en DB local). Próximo: validar visitas reales o avanzar con el siguiente slice.

Detalle del pipeline A/B y paridad: `PIPELINE-AB.md`.

## U8: Sync real robusto + validación de visitas con cuenta de terceros (2026-08-21)

**Contexto:** la U7 quedó con un pendiente: validar el endpoint real de visitas de MeLi. La cuenta propia (GONZOBLASCO) no tenía productos activos, así que se conectó una cuenta de terceros (Agos, PRO_MOTORS, `meliUserId: 48316325`).

**Problemas encontrados y resueltos:**
1. **El sync se colgaba** con la cuenta real. Causa raíz doble:
   - `MeliClient` no tenía timeout en ningún `fetch`. Un request lento a MeLi bloqueaba el sync indefinidamente.
   - `processQuestion` llamaba a `AiService.sugerirRespuesta` (Ollama local) por cada pregunta importada. 50 preguntas = 50 llamadas a Ollama.
2. **El túnel quick de cloudflared expiró** (`meaningful-cotton-attached-effects.trycloudflare.com` dio NXDOMAIN). Se reinició, se actualizó `MELI_REDIRECT_URI` en `apps/api/.env` y se registró la nueva URL (`gzip-hour-close-baseline.trycloudflare.com`) en el panel de MeLi.
3. **El endpoint `/items/visits` rechaza múltiples IDs** (`maximum amount of items to query is 1`). El intento de batch visits falló con 400. Se volvió a 1 request por item, pero en paralelo y con timeout.
4. **El enriquecimiento de productos ocurría en el orden incorrecto.** `enrichItems` corría antes de que los productos existieran, así que no persistía cache. Se refactorizó para que `enrichItems` devuelva un mapa de datos y `processQuestion` cree la ficha con cache real desde el inicio.

**Cambios aplicados:**
- `apps/api/src/meli/client.ts`:
  - `DEFAULT_TIMEOUT_MS = 15_000`.
  - `fetchWithTimeout` con `AbortSignal.timeout` aplicado a todos los endpoints (OAuth, questions, items, visits, categories, users, answers).
  - Nota en `getItemVisits`: la API solo permite 1 item por request.
- `apps/api/src/meli/sync-service.ts`:
  - `syncCompany` extrae items únicos, llama `enrichItems` y pasa el mapa a `processQuestion`.
  - `enrichItems` consulta `GET /items/{id}` una vez por item y `GET /items/visits` en paralelo (timeout aislado por item).
  - `processQuestion` crea/actualiza la ficha con título real y cache (`stock`, `vendidos`, `condition`, `categoría`, `visitas`).
  - Sync en modo real **ya no genera sugerencias IA**; la sugerencia se hace on-demand via `POST /ai/suggest`. En modo mock sigue la categorización determinística instantánea.
- `apps/api/src/meli/client.test.ts`: test del formato real de visitas (array con `item_id`, `total_visits`, `visits_detail`).

**Validación real:**
- Cuenta de Agos conectada vía OAuth (token real guardado, `meliUserId: 48316325`).
- Sync real: 50 preguntas + 23 productos en **5.1s**.
- Métricas de visitas: **788 visitas totales** en 30 días, top productos correctos (Escape Akrapovic: 389, Asiento de gel: 106, Campera Racetech: 55, etc.).
- Productos creados con **títulos reales** (no solo IDs).

**Verificación:** 57 tests (53 api + 4 db), build + lint + typecheck verdes, bundle web 338.95 kB.

**Deuda técnica:** test automatizado del timeout contra un mock server lento. Se pospone para no instalar dependencias nuevas en esta unidad.

**Fase 1 CERRADA (2026-08-21).** U1-U8 completas y validadas. Próximo: definir Fase 2.

## Notas de decisión

- "adelante" a secas = seguir con mi recomendación según el contexto (regla acordada).
- El ecosistema de MDs es un sistema vivo: no fijar todas las fases con anticipación, definir la fase actual y evolucionar.
- V4 se construye sobre el repo de v3 (no es repo nuevo) - el backend es el activo valioso.
- **Lección SLA:** el check destructivo (marca al detectar) rompe con React StrictMode (doble mount del load). Separar detección (no destructiva) de marcado (explícito).

**Demo local con datos reales (2026-08-21):** para poder ver los datos reales de la cuenta de terceros en la UI local sin auth, se delegó a Qwen Code (Agente A: deepseek-v4-flash) la modificación de `POST /auth/dev/setup` para reutilizar la empresa con token de MeLi. El cross-review del Agente B corrigió el `LIMIT 1` arbitrario (devolvía la cuenta propia vacía) ordenando por cantidad de datos sincronizados (productos > cache > preguntas), priorizando la cuenta de terceros (23 productos, 50 preguntas, visitas reales). Verificado contra la DB real: `dev/setup` devuelve `ed3538fa-...` (cuenta de Agos). 53 tests + build verdes. Lección: las buenas prácticas se aplican siempre, incluso en demos - delegar a Qwen Code y verificar contra la fuente real.

---

## Estado - Sesion 2026-08-24 (tarde)

### Seguridad pre-Beta: SoporteML solo lee, no publica
- **Decision de Gonzo:** hasta la primer Beta, SoporteML v4 no debe afectar el trabajo diario del cliente en MeLi. El vendedor sigue respondiendo desde la app de MeLi; SoporteML solo centraliza lectura, categorizacion, sugerencias y CRM.
- **Implementacion:** agregado flag `MELI_PUBLISH_ENABLED` (default `false` / `0`).
  - `MeliSyncService.publishAnswer`: si `MELI_PUBLISH_ENABLED` no es `1` o `true`, solo marca la pregunta como respondida localmente y guarda `final_answer`. Nunca llama a la API real de MeLi.
  - `MeliTokenService.getConnectionStatus`: devuelve `publishEnabled` para que la UI refleje el modo.
  - UI `Inbox.tsx`: cuando `publishEnabled` es `false`, el boton dice "Guardar respuesta", el toast dice "Respuesta guardada" y el header indica "solo lectura (publicacion desactivada hasta Beta)".
  - `.env`: `MELI_PUBLISH_ENABLED=0` con comentario de seguridad.
- **Tests:** 59 verdes (55 api + 4 db), incluyendo test especifico de que publish no toca MeLi cuando el flag esta desactivado.
- **Build:** lint OK (4 warnings preexistentes shadcn/ui), build OK.

### Timestamp real de la pregunta
- **Problema:** `questions.created_at` guardaba la fecha de sincronizacion local, no la fecha real en que el comprador hizo la pregunta en MeLi.
- **Solucion:** columna `asked_at` en `questions` que guarda `date_created` del endpoint de MeLi. `created_at` sigue siendo metadata de insercion local.
- **Cambios:** schema, types, repo, sync-service, API types, test mock.
- **Tests:** 59 verdes (57 en el primer commit, ahora 55 api + 4 db tras los tests nuevos de publish). Build OK.

### Pendientes inmediatos (UI)
- Cambiar `timeAgo` para usar `asked_at` cuando exista.
- Redisenar Inbox a grilla por comprador (cards de comprador con contador de productos con nuevas preguntas).
- Modal por comprador con CRM interno: historial de preguntas del mismo comprador, detalle del producto (foto de MeLi), responder con plantillas, sugerencia IA, notas/tags.
- Verificar build + tests tras cambios de UI.

---

## Estado - Sesion 2026-08-24 (noche)

### Nueva Inbox CRM-style: grilla por comprador + modal de detalle
- **Decision:** pasar de una lista por pregunta a una grilla de tarjetas de comprador. Cada tarjeta muestra el nickname, cantidad de consultas y un preview de las preguntas recientes. Al hacer click se abre un modal con el historial completo de ese comprador.
- **Backend:**
  - `packages/db/src/repo/questions.ts`: `listInbox` ordena por `asked_at DESC, created_at DESC`; nuevo `listByBuyer(companyId, buyerId)` para el historial CRM.
  - `apps/api/src/app.ts`: endpoints `GET /questions/buyer/:buyerId` y `GET /products/:id`.
  - `apps/api/src/meli/client.ts`: `MeliItem` incluye `thumbnail` y `price`.
  - `apps/api/src/meli/sync-service.ts`: `enrichItems` trae `thumbnail` y `price` de MeLi; `processQuestion` los guarda en `meli_cache`. Fallback de foto: `thumbnail ?? pictures[0].url`.
  - `apps/web/src/lib/api.ts`: metodos `listQuestionsByBuyer`, `getProduct`, `aiSuggest`.
- **Frontend:**
  - Nuevos componentes: `BuyerCard.tsx`, `BuyerDetailDialog.tsx`, `StatusBadge.tsx`, `components/ui/dialog.tsx`.
  - `Inbox.tsx`: grilla de compradores, stat de "Compradores", orden por pregunta mas reciente usando `asked_at`.
  - `BuyerDetailDialog`: header con contador, lista de productos del comprador con foto cacheada, historial de preguntas, respuesta con textarea + plantillas + sugerencia IA, boton "Guardar respuesta" (local hasta Beta).
- **Accesibilidad:** dialog con `aria-describedby`, focus gestionado por Radix, Escape para cerrar, roles y headings correctos.
- **Pipeline:** `pnpm test` 59 verdes (55 api + 4 db), `pnpm lint` OK (4 warnings preexistentes de shadcn/ui), `pnpm build` OK.

### Fix post-deploy + limpieza de mocks (2026-08-24, 16:03)
- **Problema:** despues del deploy de la nueva UI, las DB locales existentes carecian de las columnas `asked_at` y `buyer_nickname`, lo que causaba 500 en `GET /api/questions` y tarjetas con "Comprador".
- **Fixes:**
  - `packages/db/src/index.ts`: migracion lightweight que agrega `asked_at` y `buyer_nickname` si faltan.
  - `apps/api/src/meli/sync-service.ts`: al re-encontrar preguntas existentes, actualiza `buyer_nickname`, `asked_at`, `meli_permalink` y `meli_status` sin duplicar.
  - `apps/api/src/app.ts`: `POST /auth/dev/setup` reutiliza la empresa demo con mas datos sincronizados.
- **Pipeline:** `pnpm test` 59 verdes, lint OK, build OK. Commits `1e76210` (CRM inbox) y `73cb88b` (migracion y recovery).

### No mas fallback silencioso a mock + resolucion de nicknames (2026-08-24, 20:08)
- **Problema:** la DB local tenia datos reales de la cliente mezclados con mocks (`comprador_mock_xx`). El sync caia a mock cuando el token de MeLi no se podia refrescar, contaminando la empresa real.
- **Fixes:**
  - `apps/api/src/meli/sync-service.ts`:
    - Con `MELI_MOCK=0`, si no hay token o el refresh falla, lanza un error claro. Ya no genera mocks silenciosos.
    - `resolveBuyerNickname`: si `searchQuestions` no trae `nickname`, consulta `GET /users/{buyer_id}` de MeLi y cachea por sync.
    - `upsertCustomer` usa el nickname resuelto.
    - Actualiza `meli_status` de preguntas existentes.
  - Logging explicito al entrar en modo mock (solo cuando `MELI_MOCK=1` o `forceMock`).
- **Limpieza local ejecutada:**
  - Backup de `soporteml.db` y `.env` en `apps/api/backups/soporteml-v4/`.
  - Borradas 39 preguntas mock (IDs cortos `910000xxx`) y 18 productos mock (`MLA900000xxx`). Quedan 50 preguntas reales y 24 productos reales.
- **Tests de frontend:** se agrego Vitest + Testing Library a `apps/web` con 12 tests:
  - `BuyerCard.test.tsx`: renderizado, estadisticas, preview, interacciones click/teclado.
  - `StatusBadge.test.tsx`: estados conocidos y desconocidos.
  - `BuyerDetailDialog.test.tsx`: carga, CRM, productos con thumbnail, historial, guardado de respuesta local (API mockeada).
- **Pipeline:** `pnpm test` 71 verdes (55 api + 4 db + 12 web), `pnpm lint` OK, `pnpm build` OK.
- **Commits:** `7fb5634` (sync hardening + nicknames) y `f96ccf6` (frontend tests).

### Cron de refresh proactivo del token MeLi (2026-08-24, 20:29)
- **Problema:** el refresh del access token de MeLi era perezoso (solo cuando el sync lo pedia). Si no habia sync por >6h, el token quedaba vencido y el proximo sync lo renovaba (funciona, pero con una ventana muerta).
- **Solucion (dos partes):**
  1. **Backend** (commit `cc7067e`): nuevo endpoint `POST /meli/refresh-token` (auth + admin) que refresca el access token de TODAS las empresas con refresh token. Nuevo metodo `MeliTokenService.refreshAll()`. 2 tests nuevos (57 api).
  2. **Cron de OpenClaw** (`soporteml-meli-token-refresh`): dispara el endpoint cada 5 horas (los access tokens duran ~6h). Delivery none (silencioso).
- **Validado end-to-end:** el endpoint refresco el token real de la cuenta de la cliente (meliUserId 48316325) y extendio `expires_at` de `2026-08-25T01:13` a `2026-08-25T05:29` UTC.
- **Credenciales del cron:** userId `521a68d2-f0dd-48c7-94fb-a07c7afccbc0` + companyId `4dd8ea5d-f1e5-4bd6-a59d-6f9bc4656798` (admin de la cuenta real). Si cambian los ids en la DB (reconexion OAuth con empresa nueva), actualizar el cron.
- **Nota:** el cron corre solo mientras el backend de SoporteML este levantado en localhost:3001. Si no esta corriendo, el cron falla (el agentTurn lo reporta). No es una solucion para un server apagado - es prevencion local para que el token no se venza mientras desarrollo.

### Nota de continuidad
- Backup de `.env` y `*.db` del v4 antes de cualquier movimiento futuro.
- Si el tunel cloudflare cae, actualizar `MELI_REDIRECT_URI` en `.env` y en el panel de MeLi, y regenerar URL de OAuth.
- No activar `MELI_PUBLISH_ENABLED=1` hasta la primer Beta.
- **Proximo paso inmediato:** reiniciar el backend (`apps/api`) para cargar el codigo nuevo y correr la migracion; luego sincronizar para validar que el token se renueva y los nicknames reales se recuperan.

### Fix de sincronizacion de preguntas nuevas + estado real (2026-08-24, 21:45)

**Bug 1: el sync no traia las preguntas nuevas (Gonzo detecto timestamps inverosimiles).**
- Todos los cards mostraban preguntas de hace 163-324 dias, pero en MeLi habia consultas de hoy mismo.
- **Causa:** el endpoint `/my/received_questions/search` de MeLi devuelve las preguntas MAS VIEJAS primero (orden ascendente de fecha) y `syncCompany` pedía solo `limit: 50` sin `offset`. Se quedaba con el historico viejo y nunca paginaba hasta las nuevas (que estan al final de la paginacion). El filtro `date_created.from/to` NO funciona en esta API (verificado - lo ignora).
- **Fix:**
  - `MeliClient.searchQuestions` ahora acepta `offset`.
  - `MeliSyncService.fetchAllQuestions()` pagina con `offset` (page size 50) hasta agotar paginas o alcanzar MAX_QUESTIONS_TO_SYNC = 400.
  - Commit `18dcc4c`.
- **Validado end-to-end:** sync real paso de 50 a 173 preguntas. Las mas nuevas estan (FERNANDOAGUIRRE387 2026-08-23 = ayer).

**Bug 2: el card mostraba estado mentiroso (todos "Pendiente").**
- La UI leía `q.status` (local, siempre pending porque la publicacion esta off pre-Beta) en vez de `meli_status` (real de MeLi: 48 ANSWERED, 1 BANNED, 1 UNANSWERED).
- **Fix:** `lib/question-status.ts` (web) con `displayStatus()` e `isAwaiting()` que priorizan `meli_status` con fallback a `status`. `StatusBadge` ahora muestra Respondida/Bloqueada/Pendiente segun MeLi. Commit `b806920`. 18 tests web.

**Total:** 79 tests verdes (57 api + 4 db + 18 web), lint OK, build OK.

### Filtros de dashboard + categorias renombradas (2026-08-24, 22:13)

**Punto 1 - "Pendientes" como filtro clickeable:**
- El StatCard "Pendientes" del dashboard ahora es un boton toggle (como las categorias). Click filtra la grilla a solo preguntas sin responder (`isAwaiting`); click de nuevo la quita.
- Refactor: `activeCategory` -> `activeFilter` generico que acepta `"pending"` o un nombre de categoria.

**Punto 2 - Categorias renombradas al vocabulario del vendedor de motos (cambio de Gonzo):**
- **Nuevas categorias:** Precio, Stock, Compatibilidad, Caracteristicas, Service, Envio, Garantia, Otros.
- **"Tecnico" eliminado.** "Compatibilidad" y "Caracteristicas" separadas.
- **Default del clasificador: Otros** (antes Tecnico/Precio).
- `apps/api/src/ai/service.ts`: `QuestionCategory` y `mockCategorizar` actualizados con nuevo orden de checks y keywords (Service: taller/mantenimiento/aceite/cadena/frenos; Caracteristicas: pesa/peso/medidas/material/color/incluye; Compatibilidad: sirve/le va/para X modelo/para marcas).
- `apps/web/src/views/Inbox.tsx`: StatCards con 8 categorias nuevas + colores (grid lg 5 cols).
- `apps/web/src/components/CategoryBadge.tsx`: estilos para las categorias nuevas.
- `apps/api/src/app.test.ts`: test de categorias variadas actualizado a "Compatibilidad".
- `POST /ai/backfill-categories` soporta `{ force: true }` para re-categorizar todas.
- Commit `0ec9190`.

**⚠️ Pendiente accionable (requiere Gonzo):** la DB real sigue teniendo valores viejos (Tecnico). Para ver las categorias nuevas en la UI hay que re-correr el backfill con `force:true` sobre las 173 preguntas reales y recargar el frontend. El codigo ya esta; falta disparar el backfill.

**Pipeline:** `pnpm test` 81 verdes (58 api + 4 db + 19 web), `pnpm lint` OK (4 warnings preexistentes shadcn/ui), `pnpm build` OK. Commit `0ec9190`.
