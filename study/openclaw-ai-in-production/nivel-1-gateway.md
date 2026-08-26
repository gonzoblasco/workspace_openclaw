# Nivel 1 - Arquitectura del Gateway (Cap 1)

Badge: 🏛️ Gateway Architecture | Recursos: libro Cap 1 + repo OpenClaw live + workspace real

## Subnivel 1.1 - El Gateway como control plane

### Topic: Gateway como control plane (hub-and-spoke)

**Teoría (vocabulario con nombre):**
- **Control plane**: el componente que decide qué puede pasar, a dónde van las requests y quién puede conectarse. En OpenClaw es el proceso Gateway.
- **Hub-and-spoke**: el Gateway es el hub central; canales, plugins y agentes son los spokes que se conectan a él.
- **Single control plane**: auth + routing + session management en un solo proceso. 3 propiedades: (1) seguridad consistente (ningún canal se saltea el check), (2) routing auditable en un lugar, (3) un solo proceso para restart/upgrade/observar.
- **Trade-off del bottleneck**: todo pasa por el Gateway -> potencial bottleneck. Solución: request path fino (auth = comparación constante, routing = lookups en memoria con cache). El Gateway NO hace inference, NO maneja tool calls largos, NO posee el session state filesystem - eso es del **Agent Runtime**.
- **gateway.bind**: loopback | lan | tailnet | auto | custom - define la superficie de red.
- **gateway.port**: default 18789.
- **gateway.auth**: mode (none/token/password/tailscale/device-token/trusted-proxy) + token + rateLimit.
- **gateway.mode**: local (gestiona canales + agent runtime) vs remote (thin transport relay a otro Gateway) - base del edge deployment (Cap 13).
- **Startup sidecar sequence** (src/gateway/server-startup.ts): cada sidecar (hooks, browser server, canales, plugin services, ACP session manager) arranca en su propio try/catch -> **Bulkhead pattern al arranque**. Parcial > total: si cae Telegram, Discord arranca igual.
- **Stale session lock cleanup**: locks de sesión muertos > 30 min se limpian con PID-alive checks (isPidAlive) - evita robar sesiones a un sibling en rolling restart.
- **Insight del cap**: la simplicidad operativa del Gateway se compra con un modelo de plugins más sofisticado. El diagnostics del registry es tu primera señal de monitoreo.

**Práctica:** identificamos en nuestro workspace: gateway.bind loopback + Tailscale Serve (modo tailnet), auth por token.

**Verificación (mock interview):** ¿Por qué el Gateway es un bottleneck potencial y cómo lo evita OpenClaw?
**Respuesta esperada:** Porque todo el tráfico lo atraviesa; lo evita manteniendo el request path fino (auth de comparación constante, routing por lookups cacheados) y delegando inference/tool calls/state al Agent Runtime. Cap 2 detalla la asignación de trabajo.

### Topic: Channel adapters como spokes desacoplados

**Teoría:**
- **Channel adapter / ChannelPlugin**: plugin autónomo que habla el protocolo de UN servicio de mensajería, traduce eventos a formato interno, y entrega respuestas. Sin dependencia entre canales ni con el runtime - solo hablan con el Gateway.
- **Decoupling**: un fallo en Slack no afecta a Telegram; agregar un canal no toca routing/session de otros.
- **Channel registry** (src/channels/registry.ts): lista canónica de 9 canales core (telegram, whatsapp, discord, irc, googlechat, slack, signal, imessage, line) con metadata pero SIN implementación. Las implementaciones viven en extensions/.
- **normalizeAnyChannelId**: resuelve cualquier string raw a un ID canónico consultando el plugin registry live, no una lista hardcodeada. Nuevo canal (extensions/zalo/) se agrega sin tocar core.
- **Alias**: mismo adapter bajo múltiples nombres lógicos (imessage/imsg, irc/internet-relay-chat). Usar siempre IDs canónicos en config nueva; no remover aliases sin auditar bindings.
- **ChannelPlugin interface**: id (canónico, efectivamente inmutable post-deploy) + meta (nombre, aliases, docs) + config/setup + status (probeAccount) + outbound (delivery mode + chunking). SIN métodos start/stop top-level. Interface minimal.
- **Blue-green deploy de canales**: cambiar el id de un adapter forzado exige actualizar todos los bindings (Cap 10).

**Práctica:** nuestro workspace usa webchat como único canal. La lista de canales disponibles es propiedad de qué plugins se cargan (openclaw.json), no del core - core chico, sin credenciales de canales que no usamos.

**Verificación:** ¿Por qué cambiar el id de un channel adapter roto es una decisión de deployment no trivial?
**Esperada:** porque el id es el identificador que routing/config/allowlist usan; cambiarlo rompe todos los bindings existentes - por eso los aliases existen y por eso se trata como migración.

### Topic: PluginRegistry (extensión sin tocar core)

**Teoría:**
- **PluginRegistry** (src/plugins/registry.ts): estructura central de lo que el Gateway entiende en runtime. Registra: tools, hooks, typedHooks, channels, providers, gatewayHandlers, httpRoutes, cliRegistrars, services, commands, diagnostics.
- **gatewayHandlers**: diccionario method->handler; registry ENFORCE que no haya 2 plugins con el mismo method name (el segundo se dropea + diagnostic). Evita dispatch impredecible.
- **diagnostics**: acumula warnings/errors del load. error = blocking alert en producción (registro fallido = capability ausente sin excepción).
- **createApi()**: superficie que cada plugin usa (registerTool, registerHook, registerHttpRoute, registerChannel, registerProvider, registerGatewayMethod, registerCli, registerService, registerCommand, on).
- **hookPolicy / allowPromptInjection**: seguridad por plugin. Si plugins.entries.<id>.hooks.allowPromptInjection es false, bloquea o limpia los hooks before_prompt_build/before_agent_start. **Enforcement en registration time, no invocation** - un plugin malicioso no puede saltarse el filtro con loading dinámico.
- **Global registry singleton** (src/plugins/runtime.ts): Symbol.for("openclaw.pluginRegistryState") - evita split-registry cuando hay múltiples copias del SDK (Jest/Vitest, plugin bundling). El version counter detecta rebuilds (config reload).

**Verificación:** ¿Por qué la política de prompt injection se aplica en registration time y no en invocation?
- Esperada: para que un plugin malicioso no pueda bypassear la restricción retrasando su registro o con module loading dinámico. La capacidad de injectar contenido en el prompt se decide por config del plugin, no por su código.

### Topic: Routing de 7 tiers (agent-to-agent)

**Teoría:**
- **Routing waterfall** (src/routing/resolve-route.ts): 7 tiers de menos específico a menos específico, primer match gana:
  1. peer-exact
  2. thread-parent peer
  3. guild-with-roles
  4. guild
  5. team
  6. account
  7. channel-wide
  + default (si nada matchea)
- **matchedBy**: el tier que produjo el match. Logarlo (`[routing] match: matchedBy=<tier> agentId=<id>` con --verbose) es clave para diagnosticar routing sorpresas.
- **Determinismo**: el waterfall fijo hace el routing predecible y auditable, no emergente.
- **Session key + mainSessionKey**: session key codifica agent+channel+account+peer; mainSessionKey es la versión colapsada para DM collapse.
- **lastRoutePolicy** ("main"|"session"): qué key recibe las last-route updates.
- **dmScope** ("main"|"per-peer"): cambiarlo post-deploy = session keys distintas = conversaciones reinician. Es deployment-time decision, no runtime.
- **ACP (Agent Client Protocol)**: cuando un orchestrator spawna un sub-agent, AcpSessionManager asigna identidad de sesión separada - no aparece en history del canal usuario, puede ser reemplazado sin disrupar el orchestrator. **reconcilePendingSessionIdentities** al arranque re-linkea ACP sessions commiteadas antes de un restart - multi-agent sobrevive restarts.

**Verificación:** Si cambias dmScope de "main" a "per-peer" post-deploy, ¿qué pasa?
- Las session keys cambian -> las conversaciones existentes aparecen como nuevas (reinician). Por eso dmScope es deployment-time decision con migración explícita de session keys.

### Topic: Horizontal scaling topology

**Teoría:**
- El Gateway en gran parte es **stateless** (auth token-based, routing lee config, conexiones de canal por-instancia). Lo **stateful** es la session data (history, tool calls, memory embeddings) en OPENCLAW_STATE_DIR.
- **Shared persistent volume**: en multi-instancia, OPENCLAW_STATE_DIR debe ser un volumen compartido montado en todas las réplicas.
- **Write-lock** (src/agents/session-write-lock.ts): previene que 2 instancias procesen la misma sesión simultáneamente; la otra espera o devuelve backpressure.
- **Por qué funciona**: agentes conversacionales = bajo rate/sesión (seg-min entre mensajes) + alto tiempo por request (seg a decenas de seg). Bajo este patrón, filesystem lock en volume de red alcanza. NO escala a high-frequency trading, pero evita la complejidad de Redis/etcd.
- **bind + reverse proxy**: bind lan + auth trusted-proxy (userHeader). 2 safety checks: (1) validate request from known proxy IP (trustedProxies), (2) requiredHeaders (ej HMAC). Falla con trusted_proxy_untrusted_source o trusted_proxy_missing_header_<name>.

**Práctica:** nuestra depl es single-host (loopback), el shared volume no aplica aún. Concepto claro para cuando OpenClaw escale a multi-instancia.

**Verificación:** ¿Qué es lo stateful en OpenClaw y dónde vive? ¿Por qué el lock de archivo alcanza?
- La session data en OPENCLAW_STATE_DIR. Alcanza porque el patrón de agentes conversacionales tiene bajo rate y alto tiempo por request; no requiere coordinación distribuida como Redis.

### Topic: Token Exchange en el boundary

**Teoría:**
- **Token Exchange**: el long-lived device credential (OPENCLAW_GATEWAY_TOKEN / gateway.auth.token) se cambia en el boundary por un session token corto y scope-limited. No es RFC 8693 (no minta downstream token). El long-lived NUNCA viaja más allá del Gateway; el runtime recibe un context con authority ya resuelta.
- **Razón**: el ataque surface de un long-lived vs short-lived difiere. Interceptado: long-lived = acceso indefinido hasta rotación; short-lived = solo la sesión actual, no crea sesiones nuevas.
- **authorizeGatewayConnect** (src/gateway/auth.ts): punto central de enforcement. GatewayAuthResult = { ok, method, user, reason, rateLimited, retryAfterMs }. method: none|token|password|tailscale|device-token|trusted-proxy.
- **safeEqualSecret** (src/security/secret-equal.ts): comparación de tiempo constante anti timing-attack. Es la ÚNICA vía aprobada para comparar credenciales en el Gateway - un === rompe la garantía.
- **Rate limiting**: limiter.recordFailure en mismatch, reset en success. maxAttempts/windowMs. rate_limited + retryAfterMs (señal de retry con backoff). El contador sobrevive connection resets (efectivo contra reconnect-looping). Sin rate limit, un client mal config en loop puede saturar la auth path.
- **ResolvedGatewayAuth**: separa mode (auth scheme) de modeSource (de dónde derivó: override/config/token/password/default). Diagnostic: modeSource="token" vs declarado - señal de config drift.
- **Local vs remote credentials** (src/gateway/credentials.ts): separa credenciales locales (Gateway habla con su HTTP surface) de remotas (cliente -> Gateway en otro host). Rotan independientes.
- **Tailscale identity**: variante de Token Exchange. resolveVerifiedTailscaleUser hace WhoIs contra el control plane de Tailscale para verificar que el header tailscale-user-login matchea la identidad del IP del nodo. No confía en el header solo. Mismatch -> tailscale_user_mismatch = auth failure.

**Práctica:** usamos Tailscale Serve para webchat remoto (la variante tailscale de auth). Nuestra regla de "no exfiltrar datos privados" es coherente con el least-privilege del agent layer.

**Verificación:** ¿Qué gana el sistema al mantener el long-lived credential en el boundary y pasar solo una identity claim al runtime?
- El agent layer queda least-privileged: un secreto de larga duración interceptado da acceso indefinido, pero un session token interceptado da acceso solo a la sesión actual. Los secretos durables nunca alcanzan el agent runtime.

## Cierre del nivel

- **Self-review (rúbrica):**
  - Qué salió bien: conexión directa de cada concepto con nuestro workspace real (loopback+Tailscale, ACP/subagentes, memory persistente, crash recovery). Vocabulario con nombre dominado.
  - Qué faltó: hands-on de routing multi-binding (no tenemos 2 canales). Verificar auth mode en startup (pendiente).
- **Pendiente del nivel:** hacer el hands-on del cap (2 canales o simular con HTTP endpoint), verificar modeSource en startup del Gateway.
- **Badge:** 🏛️ Gateway Architecture (nivel 1 mapeado en primera pasada; XP pendiente de segunda pasada).
