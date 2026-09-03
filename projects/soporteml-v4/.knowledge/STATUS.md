# SoporteML v4 - STATUS

**Actualizado:** 2026-08-21

## Estado: 🟢 FASE 1 COMPLETA - U8 (sync real robusto + visitas validadas) completada. Próximo: definir Fase 2.

## Fase 0 - Fundamentos del reinicio (COMPLETA)

- [x] Crear `.knowledge/` de V4 (BRIEF, PLAN, STATUS)
- [x] **Decidir la identidad visual de V4** - dirección híbrido oscuro + color por categoría (ADR-001)
- [x] Mockup de identidad validado por Gonzo (`mockups/identidad-v4.html`)
- [x] Iconografía Lucide incorporada al mockup (ADR-030, workspace)
- [x] **Verificar que el backend de v3 funciona** - verificado de punta a punta (`BACKEND-VERIFICADO.md`)
- [x] **Enriquecer el mock** - 13 preguntas (antes 6), 6 productos (antes 3), varias por producto, producto sin preguntas activas
- [x] **Agregar tests del API** - 26 tests que cubren health, auth, sync, multi-tenant, publish, idempotencia, productos, IA, billing, plantillas, KB, autopilot, clientes, métricas, SLA
- [x] **Arrancar la UI** (el corazón que le da vida al cuerpo) - layout + bandeja reconstruidos con identidad V4
- [x] **Slice 1 funcional: Plantillas de respuesta** - CRUD completo (repo, API, UI) + tests
- [x] **Plantillas conectadas al flujo de responder** - insertar plantilla en la respuesta desde la bandeja
- [x] **KB (RAG) - gestión de artículos** - CRUD de artículos con chunking (repo, API, UI) + tests
- [x] **KB (RAG) - búsqueda semántica** - embeddings + similitud coseno + contexto para la IA
- [x] **Autopilot** - responde consultas automáticamente por categoría + umbral de confianza
- [x] **Clientes (CRM)** - compradores con notas + tags + historial
- [x] **Métricas** - dashboard de ventas/consultas (la última feature core del schema)
- [x] **Validar el RAG con más artículos** - discrimina correctamente entre 4 categorías
- [x] **SLA** - detección de consultas vencidas + banner en Inbox + configuración en Ajustes
- [x] **Lint arreglado** - ESLint flat config (TS + React), 0 errores
- [x] **Pre-commit hooks** - simple-git-hooks con `pnpm lint && pnpm test`
- [x] **Definir el pipeline A/B** (`PIPELINE-AB.md`)

## Fase 1 - Pulido + integraciones (EN CURSO)

- [x] **U1 - Ajuste fino RAG (minScore)** - Agente A (commit `6c95905`)
  - **Problema resuelto:** con `minScore` 0.2, una consulta sin match real ("¿Aceptan cuotas?") devolvía el chunk más cercano (garantía). 
  - **Cambio:** `searchChunks` sube el default a `0.45` (alineado con `company_settings.kb_similarity_threshold`), con la constante `DEFAULT_MIN_SCORE` en `packages/db/src/repo/kb.ts`.
  - **Configurable por empresa:** `KbService.search` ahora lee `kb_similarity_threshold` de los settings, y `PUT /settings` acepta `kbSimilarityThreshold` (+ `kbTopK`). Deja de estar hardcodeado.
  - **Tests:** 4 nuevos en `apps/api/src/kb-service.test.ts` con embeddings one-hot determinísticos (sin Ollama): sin match → vacío, con match → chunk correcto, umbral configurable, umbral alto filtra matches débiles.
  - **Total:** 30 tests del API (26 + 4), todos verdes. Build + lint OK.
- [x] U2 - Code-splitting (chunk > 500kB) - Agente B (commit `ab914c8`)
  - **Problema resuelto:** el bundle principal era 512 kB (gzip 157 kB), justo sobre el warning de 500 kB de Vite. `App.tsx` (~1491 líneas) tenía todas las vistas inline → un solo chunk.
  - **Cambio:** se extrajo cada vista (`Inbox`, `Products`, `Templates`, `KnowledgeBase`, `Customers`, `Metrics`, `Settings`, `Playground`) a `apps/web/src/views/` con sus propios helpers, y se cargan con `React.lazy` + `<Suspense>` como chunks separados bajo demanda (sin introducir React Router).
  - **Resultado:** bundle principal 512 kB → **338.93 kB** (gzip 106.55 kB), sin warning de chunk. Cada vista es su propio chunk chico (Inbox 10.32, Metrics 5.84, Settings 6.65, etc.).
  - **A11y preservada:** el fallback de Suspense usa `role="status"` + `aria-live="polite"` + label sr-only; la navegación por sidebar y teclado intacta.
  - **Verificación:** build + typecheck + lint + 34 tests verdes (30 api + 4 db).
- [x] U3 - Validación visual (revisión de U2 + ajustes de identidad) - Agente A (commit `e0aeac4`)
  - **Revisión de U2 (cross-review):** el code-splitting está bien implementado. Las 7 vistas + Playground cargan bajo demanda con `React.lazy` + `<Suspense>` (verificado en browser: el fallback se muestra al navegar), el fallback es a11y-compliant (`role="status"` + `aria-live="polite"` + sr-only), no hay imports rotos ni referencias colgantes en `App.tsx`, y cada vista tiene su `export default`. El fix del score (`21fda14`) es correcto y no rompe el contrato: `searchChunks` devuelve `ScoredKbChunk[]` y el único consumidor (`app.ts`) usa `r.content`; tests alineados.
  - **Ajuste visual (bug encontrado):** la app cargaba en **tema claro** por default (`defaultTheme="system"` en `next-themes`), perdiendo la identidad oscura premium de ADR-001 en sistemas operativos claros. Fix: `defaultTheme="dark"` en `main.tsx`. El toggle del sidebar sigue permitiendo cambiar a claro.
  - **Verificación en browser:** las 7 vistas se ven consistentes con ADR-001 en tema oscuro (bg `#0a0e1a`, acento MeLi con glow, color por categoría, glassmorphism, micro-interacciones). Build + lint + 34 tests verdes. Bundle principal 338.95 kB (code-splitting preservado).
- [x] U4 - Email (Resend) - Agente B (commit `22baacb`)
  - **Revisión de U3 (cross-review):** el fix de tema oscuro (`e0aeac4`) es correcto y mínimo. `defaultTheme="dark"` (sin `enableSystem`) garantiza la identidad oscura de ADR-001 en cualquier OS. El toggle del sidebar sigue funcionando: usa `useTheme` + `setTheme` (independiente de `enableSystem`), y el tema claro existe en CSS (`.light` sobreescribe los tokens de `:root`), así que cambiar a claro renderiza bien. `disableTransitionOnChange` ya estaba antes, no introduce flash. Sin regresiones (cambio solo de tema). La validación visual final la hace Gonzo.
  - **Servicio de email (Resend):** nuevo `apps/api/src/email-service.ts` con `EmailService` (interface `SlaNotifier` inyectable para tests). Lee `RESEND_API_KEY` del env; si no hay clave **degrada a modo dev** (loguea el email que se habría enviado, patrón del mock de MeLi) y nunca falla.
  - **Disparo SLA por email:** `POST /sla/mark-alerted` ahora notifica a `sla_alert_emails` con el detalle de las consultas vencidas (nuevo `SlaService.alertsFor` reutiliza el cálculo de atraso). **Idempotente:** `detect()` solo devuelve preguntas sin `sla_alert_sent_at`, así que las ya marcadas no re-notifican.
  - **Tests:** 5 nuevos (3 unit email-service + 2 integración en app.test). Total 35 api + 4 db = 39. Build + lint verdes.
  - **Nota:** sin clave de Resend configurada aún; el servicio corre en modo dev esperando que Gonzo ponga `RESEND_API_KEY` en `.env`.
- [x] U5 - Mercado Pago (billing real) - Agente A (commits `9b743d5` + `3b59857`)
  - **Revisión de U4 (cross-review):** el email service de Resend está bien implementado. La degradación a dev (sin `RESEND_API_KEY`) loguea y no falla, el disparo es idempotente a nivel de `detect()`, y el wiring en `mark-alerted` nunca rompe el marcado (try/catch + degradación). **Bug corregido (commit `9b743d5`):** `SlaService.alertsFor` no filtraba por empresa ni por `sla_alert_sent_at`, así que un doble submit de los mismos ids re-notificaba y un id de otro tenant podía filtrarse al email. Ahora filtra `company_id === companyId` y `sla_alert_sent_at === null` (defensa en profundidad además de `detect()`).
  - **Integración MP (commit `3b59857`):** nuevo `apps/api/src/mp/client.ts` (`MpClient`) que conecta la API de preapproval de Mercado Pago (crear + consultar). `BillingService` ahora acepta un `MpClient` inyectable (para tests) y lee `MP_ACCESS_TOKEN` del env. **Degradación a mock:** sin credenciales, `createSubscription` devuelve la URL ficticia y `confirmSubscription` simula el pago (30 días) — la app funciona igual (patrón de `MELI_MOCK`).
  - **Webhook IPN:** nuevo `POST /billing/webhook` (sin auth de la app, lo llama MP). `handleWebhook` correlaciona el preapproval por `mp_preapproval_id`, consulta el estado real en MP y confirma la suscripción solo si está `authorized`. En modo mock no matchea (no hay preapproval real) y no hace nada.
  - **Tests:** 6 nuevos en `apps/api/src/billing/service.test.ts` (3 mock + 3 real con `MpClient` mockeado). Total 41 api + 4 db = 45. Build + lint + typecheck verdes.
  - **Nota:** sin `MP_ACCESS_TOKEN` configurado aún; el billing corre en modo mock esperando que Gonzo ponga el token de sandbox de MP en `.env` (y `MP_NOTIFICATION_URL` pública para el webhook).
- [x] U6 - OAuth MeLi real - Agente B ✅ **DESBLOQUEADA y VALIDADA (2026-08-21)**
  - **Revisión de U5 (cross-review, Agente B):** la U5 del Agente A está bien implementada. La degradación a mock es correcta (`MpClient.enabled = accessToken.length > 0`; sin credenciales el flujo funciona igual), el webhook IPN no rompe nada en mock (no matchea → no-op 200), el `MpClient` es inyectable (los tests prueban el flujo real con un mock sin credenciales), y el fix de U4 (`alertsFor`) filtra por empresa + `sla_alert_sent_at === null` correctamente. Sin bugs encontrados.
  - **Desbloqueo con túnel quick (2026-08-21):** `cloudflared tunnel --url http://localhost:3001` (NO requiere cuenta ni dominio). Flujo OAuth end-to-end validado: connect → autorización MeLi → callback → token real → sync real. `meliUserId: 10061615`, `MELI_MOCK=0`, redirect registrado en el panel. Nota: la URL del túnel quick cambia en cada reinicio.
- [x] U7 - Métricas reales de visitas de MeLi - Agente A ✅ (commits `d9ca178` + `371ac18` + `99a010e`)
  - **Objetivo:** tráfico real de visitas de MeLi (Opción A).
  - **MeliClient.getItemVisits** (GET /items/visits, formato objeto plano `{ item_id, total_visits }` confirmado por doc oficial MeLi). **Sync** guarda `total_visits` en `meli_cache` (rango 30 días, try/catch aislado - un fallo no degrada el enrich). **MetricsService.visits { total, topProducts }**. **UI**: KPI Visitas (icono `Eye`, violeta) + top productos por visitas, grid 5 columnas.
  - **Tests:** `app.test.ts` valida `visits.total > 0`. Total 41 tests verdes. Build + lint OK.
  - **⚠️ Lección:** el Agente B introdujo un bug en su cross-review (asumió array en vez de objeto plano para `/items/visits`). Kanam lo verificó contra la doc oficial y lo revirtió (commit `99a010e`), conservando el try/catch de B. El orquestador debe verificar contra la fuente real antes de aceptar un fix.
  - **Pendiente:** validar el endpoint real de visitas contra la API (token de DB local expirado/vacío).

- [x] **U8 - Sync real robusto + validación de visitas con cuenta de terceros** - Kanam / pipeline A/B manual ✅
  - **Problema resuelto:** el sync real se colgaba con cuentas que tenían muchas preguntas/productos. Causa raíz: doble problema. (1) `MeliClient` no tenía timeout en ningún `fetch`, así que un request lento a la API de MeLi bloqueaba el sync indefinidamente. (2) `processQuestion` llamaba a la IA real (`sugerirRespuesta` via Ollama) por cada pregunta importada, lo que convertía un sync de 50 preguntas en 50 llamadas a Ollama local.
  - **Cambios:**
    - `MeliClient`: agregado `DEFAULT_TIMEOUT_MS = 15_000` y `fetchWithTimeout` usando `AbortSignal.timeout`. Todos los endpoints de MeLi ahora tienen timeout (OAuth, questions, items, visits, categories, users, answers).
    - `MeliSyncService`: refactorizado para enriquecer items **antes** de crear productos. Extrae items únicos de las preguntas, consulta `GET /items/{id}` una vez por item, y luego `GET /items/visits` en paralelo con timeout (1 request por item; la API de MeLi rechaza múltiples IDs en batch). Los datos enriquecidos se pasan a `processQuestion` para crear la ficha con cache real desde el inicio.
    - Sync ya no genera sugerencias IA en modo real. La sugerencia se genera on-demand via `POST /ai/suggest` cuando el vendedor abre la pregunta. En modo mock sigue la categorización determinística instantánea.
    - Test de `extractVisits` para el formato real devuelto por MeLi (array con `item_id`, `total_visits`, `visits_detail`).
  - **Validación real:** cuenta de Agos (PRO_MOTORS, `meliUserId: 48316325`) conectada via OAuth. Sync real: 50 preguntas + 23 productos en **5.1s**. Métricas de visitas: **788 visitas totales** en 30 días, con top productos correctos (Escape Akrapovic: 389, Asiento de gel: 106, Campera Racetech: 55, etc.). Los productos se crean con títulos reales en lugar de IDs.
  - **Tests:** 53 tests del API (41 + 12 client), 4 db = 57 total. Build + lint + typecheck verdes. Bundle web 338.95 kB.
  - **Pendiente deuda técnica:** test automatizado del timeout (`AbortSignal.timeout`) contra un mock server lento. Se deja para cuando se agregue un mock server liviano (no se instaló dependencia nueva para no expandir scope).

**Cierre de Fase 1 (2026-08-21):** U1-U8 completas y validadas. Integraciones reales funcionando: OAuth MeLi (cuenta propia + cuenta de terceros), métricas de visitas reales, email en modo dev, MP en modo mock. 57 tests verdes, build sin warning. Próximo: definir Fase 2.

## Validación del RAG con más artículos (2026-08-17)

Se crearon 4 artículos (envío, garantía, compatibilidad, stock) y se verificó que la búsqueda semántica discrimina correctamente:
- ✅ "¿Cuánto tarda el envío a CABA?" → Política de envíos
- ✅ "¿Qué cubre la garantía?" → Política de garantía
- ✅ "¿El auricular es compatible con iPhone?" → Compatibilidad de dispositivos
- ✅ "¿Tienen stock?" → Disponibilidad de stock
- ⚠️ "¿Aceptan cuotas?" → devolvía garantía (no hay artículo de precios; minScore bajo 0.2 devolvía lo más cercano). **Resuelto en U1:** ahora con minScore 0.45 + threshold configurable, una consulta sin match devuelve vacío.

## Slice 6: Métricas (2026-08-17)

Dashboard del negocio - el vendedor ve la foto completa:
- ✅ `apps/api/src/metrics-service.ts` - calcula métricas cruzando questions + products + customers
- ✅ Endpoint API: GET /metrics
- ✅ UI: vista de Métricas en el sidebar (KPIs, consultas por categoría, top productos, estado, clientes)
- ✅ 1 test nuevo (24 total)
- ✅ Verificado en browser: 13 consultas, ventas estimadas $369M/861 unidades, top productos, 13 clientes
- **Nota:** ventas estimadas = vendidos x precio de los productos en meli_cache (mock)
- Commit `be4eb3b` en soporteml-v3

## Slice 5: Clientes (CRM) (2026-08-17)

CRM de compradores - el vendedor conoce a sus clientes:
- ✅ `packages/db/src/repo/customers.ts` - CRUD de clientes + tags
- ✅ Endpoints API: GET /customers, GET/PUT /customers/:id, GET/POST /customers/tags, DELETE /customers/tags/:id (con multi-tenant)
- ✅ UI: vista de Clientes en el sidebar (listar, editar notas/tags, crear tags)
- ✅ 3 tests nuevos (23 total): sync crea clientes, actualiza notas/tags, crea/lista tags
- ✅ Verificado en browser: 13 clientes del mock, creé tag "vip", asigné tag + nota a un cliente
- **Fix:** las rutas /customers/tags deben ir antes de /customers/:id (Hono matchea :id con "tags")
- Commit `2f11bea` en soporteml-v3

## UI V4 arrancada (2026-08-17)

El frontend de v3 se reconstruyó con la identidad V4 (híbrido oscuro + color por categoría):
- ✅ `index.css` - tokens V4 (base oscura premium + acento amarillo MeLi + colores por categoría)
- ✅ `AppSidebar` - logo con glow amarillo, navegación agrupada, item activo con barra lateral iluminada
- ✅ `App.tsx` - stats por categoría, bandeja con barra lateral de color, cards con micro-interacciones, login premium
- ✅ Verificado en browser: 13 preguntas con color por categoría, publicar respuesta funciona (badge cambia a Respondida, stats bajan)
- ✅ Build de producción OK
- Commit `a930cb9` en soporteml-v3

## Backend verificado (2026-08-17)

El backend de v3 (que se conserva) está sano y funciona de punta a punta:
- ✅ Typecheck pasa (api + web)
- ✅ Servidor arranca en `localhost:3001`
- ✅ Endpoints probados: health, dev setup, sync (13 preguntas mock), questions, products, meli/status, ai/suggest
- ✅ **Mocks verificados a fondo** (pregunta de Gonzo): categorización mock 6/6 correcta, multi-tenant aísla empresas, publish marca como respondida, sync idempotente (no duplica)
- ✅ **14 tests del API** (antes 0) - automatizan las verificaciones manuales
- ✅ **Mock enriquecido** - 13 preguntas, 6 productos, varias por producto, producto sin preguntas activas

Detalle completo: `BACKEND-VERIFICADO.md`

## Identidad visual decidida (2026-08-17)

**Dirección:** híbrido oscuro + color por categoría (ADR-001).

- Base oscura premium (`#0a0e1a`) + acento amarillo MeLi (`#ffe600`) con glow
- Color por categoría de consulta (precio=azul, stock=verde, técnico=violeta, envío=naranja, garantía=rosa)
- Iconografía Lucide (ADR-030)
- Micro-interacciones + a11y WCAG 2.1 AA integrada
- Mockup validado: `mockups/identidad-v4.html`

## Contexto del reinicio

**Motivo (decisión de Gonzo, 2026-08-17):** v3 quedó como template básico - features limitadas en la UI (solo 3 vistas genéricas) y UI/UX sosa (cards shadcn estándar, cero diseño avanzado). V4 reconstruye el frontend con diseño impactante y desbloquea las features que el schema ya modela.

**Activo conservado de v3:** backend (OAuth MeLi real, sync, IA, billing mock) + capa de datos (schema 20+ tablas, repositorios) + token real de producción MeLi.

**Metodología:** pipeline en cadena A/B, slices finos con release usable, `.knowledge/` vivo, a11y WCAG 2.1 AA integrada, diseño avanzado con CSS custom. Adaptada de Kanam Story/Forge, no fuente única de verdad.

## Próximo paso

Decidir la identidad visual de V4 con Gonzo (moodboard, dirección de diseño, tokens) antes de tocar código.
