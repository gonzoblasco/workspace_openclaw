# Nivel 1 - Arquitectura del Gateway (Cap 1)

Badge: 🏛️ Gateway Architecture | Recursos: libro Cap 1 + repo OpenClaw live + workspace real

> **Fecha:** 26/08 - reinicio del estudio, lectura completa del Cap 1.
> **Nota al margen (Preface):** el libro pide 16GB de RAM, pero corremos bien en la Air M2 con 8GB porque los modelos van a cloud (la inferencia pesada no toca la RAM local). El requisito del editor es para autohosting completo de modelos, no para el setup cloud-first de Gonzo.

## Subnivel 1.1 - El Gateway como control plane

**Idea central:** OpenClaw es **Gateway-centric hub-and-spoke**. El Gateway es el *control plane* - la única costura arquitectónica (seam) que decide qué pasa, a dónde van los requests y quién puede conectarse.

**Por qué centralizar en un solo proceso (3 propiedades):**
1. **Seguridad consistente** - un solo lugar donde se aplican las políticas; ningún channel adapter puede saltarse la auth mientras otro la cumple.
2. **Estado de routing en un lugar** - el mapeo origen → agente se computa una vez y es auditable.
3. **Un solo proceso para reiniciar/observar** a las 2am.

**Trade-off deliberado:** el Gateway puede ser cuello de botella. La respuesta de OpenClaw: **path de request lo más delgado posible**. El Gateway NO hace inferencia, NO maneja tool calls largos, NO es dueño del filesystem de sesión. Todo eso lo delega al **Agent Runtime** (Cap 2).

**Configuración de red (gateway.bind y gateway.port):**
- `gateway.bind`: loopback (solo misma máquina) | lan | tailnet | auto | custom
- `gateway.port`: default `18789` para operación local
- **Regla de seguridad clave:** cambiar `bind` a algo no-loopback SIN endurecer `auth.mode` es la forma más común de exponerse a la red local. El Gateway arranca sin warning porque "weak" es context-dependent - no conoce tu topología.

**gateway.mode (eje ortogonal a bind):**
- `local`: mismo proceso maneja auth + ciclo de vida de channel adapters + routing (deployment estándar)
- `remote`: solo auth y proxying corren localmente, el Agent Runtime vive en otro host (base del edge agent pattern del Cap 13)

### Verificación 1.1
- ¿Qué propiedad gana OpenClaw al centralizar auth/routing/session en un solo proceso?
- ¿Cuál es el trade-off de esa centralización y cómo lo mitiga OpenClaw?
- ¿Qué hace `bind: loopback` y qué riesgo hay al cambiarlo sin endurecer auth?

## Subnivel 1.2 - Startup sidecar sequence (Bulkhead)

**Idea:** el Gateway nunca queda "parcialmente abierto": o presenta una superficie completamente autenticada, o no escucha en absoluto.

**Secuencia (src/gateway/server-startup.ts):** los sidecars (hooks internos, browser control server, channel adapters, plugin services) arrancan DESPUÉS de que el listener HTTP/WebSocket está bound y autenticado.

**Bulkhead pattern al startup:** cada sidecar corre en su propio `try/catch`. Un adapter que falla (ej. Telegram caído) NO impide que Discord arranque, y ninguno de los dos impide que el Gateway sirva control UI o health endpoint. **"Partial availability > total unavailability"** - un Gateway con 2 de 3 canales es más útil que uno que se niega a arrancar.

**Housekeeping de largo plazo:** cleanup de session locks stale. `SESSION_LOCK_STALE_MS = 30 min`. Un lock es stale solo si su proceso dueño está muerto hace ≥30min (PID-alive checks via `getProcessStartTime`/`isPidAlive`). Evita que un Gateway nuevo robe sesiones de un sibling aún corriendo en rolling-restart.

**Pendiente de diseño:** los shutdown hooks del Cap 11 (`Platform-as-a-Service`) para zero-downtime restart - el viejo debe terminar sus agent sessions antes de que el nuevo tome los locks.

**Vocabulario:** sidecar, bulkhead pattern, partial availability, session lock stale, PID-alive check, rolling-restart.

## Subnivel 1.3 - Channel adapters como spokes desacoplados

**Idea:** cada canal es un **channel adapter** - un plugin autocontenido que sabe el protocolo de UN servicio de mensajería, traduce sus eventos al formato interno de OpenClaw y entrega respuestas de vuelta.

**Propiedades clave:**
- Los adapters NO dependen entre sí, NO dependen del agent runtime. Solo hablan con el Gateway.
- Si la API de Slack cae, Telegram sigue operando.
- Agregar una extensión nueva no afecta el routing ni el session state de otros canales.

**Channel registry (src/channels/registry.ts):** los 9 canales core (Telegram, WhatsApp, Discord, IRC, Google Chat, Slack, Signal, iMessage, LINE) en un tuple constante. Cada entrada lleva metadata (label, docs path, system image name) pero **sin implementación** - viven en `extensions/`.

**El punto crítico de diseño:** `normalizeAnyChannelId` consulta el **live plugin registry**, NO una lista hardcodeada. Un canal nuevo (ej. Zalo en `extensions/zalo/`) se resuelve sin tocar `src/channels/registry.ts`. El registry es la única seam entre core y spoke.

**ChannelPlugin interface (mínima a propósito):**
- `id` - identificador canónico (ej. `"telegram"`)
- `meta` - display name, aliases, docs path
- `config` + `setup` - resuelve/valida config
- `status` adapter - `probeAccount` prueba la cuenta antes de usarla
- `outbound` adapter - `ChannelOutboundAdapter` con delivery mode + chunking
- **NO tiene** métodos top-level start/stop. No necesita saber de sesión, routing ni hooks.

**El `id` es inmutable en producción:** si forkés un adapter y cambiás su id, tenés que actualizar TODOS los bindings de openclaw.json que lo referencian. Crucial para blue-green de adapters (Cap 10).

**Alias y discovery:** el mismo adapter alcanzable bajo varios nombres lógicos (iMessage = "imessage" + "imsg"; IRC = "irc" + "internet-relay-chat"). Los alias permiten que configs viejas sigan funcionando cuando un adapter cambia su id canónico. **Regla:** usar ids canónicos en config nueva, pero NO remover aliases sin auditar los bindings.

**Más allá de los 9 core:** extensions/msteams, matrix, zalo, feishu, twitch, nostr, nextcloud-talk, etc. La lista de canales runtime es propiedad de **qué plugins están cargados** (tu openclaw.json), no del core. Core binary chico, no carga credenciales/TLS/network de canales que no usás.

## Subnivel 1.4 - PluginRegistry (extensión sin tocar core)

**Idea:** el **PluginRegistry** es la estructura central que el Gateway usa para entender qué hay disponible en runtime. Lleva tools, hooks, HTTP routes, CLI commands, Gateway method handlers, services - cada punto de extensión.

**Objetivo de diseño:** agregar cualquier capacidad nueva (tool, route, hook, channel) **sin editar nada en `src/`**.

**PluginRegistry type (src/plugins/registry.ts):** un named list por extension point. Cada plugin append-a su lista sin tocar el estado de otros.

**gatewayHandlers (atención especial):** dict de method-name → handler-function. El registry **impone que no haya duplicados**: si dos plugins registran el mismo method, el registry registra un error en `diagnostics` y droppea el registro en silencio (fail-safe).

**diagnostics (crítico para producción):** acumula warnings/errors del proceso de carga. Hace visible el fallo de registro **al startup**, no cuando se invoca la capability faltante:
- Typed hook con nombre no reconocido → `level: "warn"` (no runtime exception)
- HTTP route que overlap con ruta existente a distinto auth level → `level: "error"`
- **Regla operativa:** cualquier `level: "error"` en diagnostics es un **blocking alert** para el pipeline de monitoreo.

**plugin API (createApi):** `registerTool`, `registerChannel`, `registerHook`, `registerHttpRoute`, `registerProvider`, `registerGatewayMethod`, `registerCli`, `registerService`, `registerCommand`, + shorthand `on`. Todo escribe en el registry compartido.

**hookPolicy (intersección con seguridad):** `allowPromptInjection` controla si un plugin puede registrar hooks `before_prompt_build`/`before_agent_start`. **Security policy se enforcea en registration time, no en invocation time** - un plugin malicioso no puede bypassear restricciones de prompt injection difiriendo su registro o con dynamic module loading. Cap 5 lo desarrolla.

**Singleton global (src/plugins/runtime.ts):** `Symbol.for("openclaw.pluginRegistryState")` asegura que TODAS las copias del paquete (aun si un plugin bundlea su propia copia del SDK) compartan el mismo state object - evita split-registry bugs. `version` counter permite detectar rebuild tras config reload.

**Vocabulario:** PluginRegistry, diagnostics, registration-time enforcement, split-registry bug, typed hooks.

## Subnivel 1.5 - Seven-tier routing waterfall

**Idea:** `resolveAgentRoute` (src/routing/resolve-route.ts) implementa un **waterfall de 7 tiers** - secuencia de match predicates cada vez menos específicos, primer match gana.

**Tiers (de más a menos específico):**
1. peer-exact match
2. thread-parent peer match
3. guild-with-roles match
4. guild match
5. team match
6. account match
7. channel-wide match
- fallback: default agent

**Determinismo + auditabilidad:** el campo `matchedBy` en `ResolvedAgentRoute` te dice exactamente qué tier hizo match. Loggear esto para cada inbound es valioso en producción (diagnóstico de routing surprises). Con `--verbose`: `[routing] match: matchedBy=<tier> agentId=<id>`.

**sessionKey y mainSessionKey:**
- `sessionKey` - identifica dónde se guarda el estado del agent conversation (agent ID + channel + account + peer en string lowercase estable).
- `mainSessionKey` - forma simplificada para "direct message collapse" (múltiples peers del mismo account comparten un thread).
- `lastRoutePolicy` ("main" | "session") - qué key recibe los updates de last-route.

**Riesgo operativo (dmScope):** cambiar `dmScope` de `"main"` a `"per-peer"` post-deployment cambia los session keys calculados → las conversations existentes parecen reiniciarse de cero. **Session key migration NO es automática** - dmScope es decisión de deployment-time, no runtime.

**Agent-to-agent dispatch via ACP:**
- Un orchestrator que spawnea sub-agent usa **ACP sessions** (AcpSessionManager en src/acp/control-plane/manager.ts).
- El sub-agent tiene su propia session identity, separada del channel session del orchestrator → no aparece en el historial del canal, y puede ser reemplazado/upgradeado sin romper la sesión del orchestrator.
- `reconcilePendingSessionIdentities` al startup: re-linkea ACP sessions cuyo identity se commiteó a disco antes de un restart, garantizando que workflows multi-agent sobrevivan restarts.

**Vocabulario:** routing waterfall, tier, matchedBy, sessionKey, mainSessionKey, lastRoutePolicy, dmScope, ACP, session reconciliation.

## Subnivel 1.6 - Horizontal scaling topology

**Mito a romper:** OpenClaw NO es inherentemente single-instance.

**Qué es stateless:** el proceso Gateway (auth token-based, routing lee del config object cargado de disco).

**Qué es stateful:** los agent session data (conversation history, in-progress tool calls, memory embeddings) bajo `OPENCLAW_STATE_DIR`. En single-host es un dir local; en multi-instance debe ser un **shared persistent volume**.

**Render config (render.yaml):** `disk: mountPath /data` + `OPENCLAW_STATE_DIR: /data/.openclaw` + `OPENCLAW_WORKSPACE_DIR: /data/workspace` + `generateValue: true` para el token (platform-managed, no se commitea).

**Two-instance consistency:**
- Ambos montan el mismo volume, ambos leen el mismo state dir, un load balancer distribuye.
- `session-write-lock.ts` (src/agents/session-write-lock.ts) previene que dos instancias procesen el mismo session simultáneamente (file-system lock).
- **El shared volume es el punto único de coordinación.** Para el workload conversacional (bajo request rate, alto processing time por request) el file-system locking en network volume es ADECUADO. No escala a high-frequency trading ni real-time game server, pero evita la complejidad de Redis/etcd para agentes conversacionales.

**Bind mode + reverse proxy:**
- En contenedor con LB que termina TLS: `bind: lan` (o 0.0.0.0 via PORT=8080) + `auth.mode: trusted-proxy`.
- Trusted-proxy extrae el user identity de un header del proxy upstream (`gateway.auth.trustedProxy.userHeader`), no de bearer token.
- **Dos safety checks:** (1) valida que el request venga de un proxy IP conocido (`gateway.trustedProxies`), (2) `requiredHeaders` exige headers extra (ej. HMAC). Falla → `trusted_proxy_untrusted_source` o `trusted_proxy_missing_header_<name>`.

**Lección:** saber qué es stateless vs qué debe compartirse separa el deployment que escala limpio del que corrompe sesiones bajo carga.

## Subnivel 1.6 - Token Exchange en el boundary

**Idea:** el patrón más importante de seguridad. Un device credential de largo plazo (`OPENCLAW_GATEWAY_TOKEN` o `gateway.auth.token`) se intercambia en el boundary por un session token de corta duración y scope-limitado. **OJO:** es credential-scoping, NO RFC 8693 OAuth token exchange (no se mintea downstream token).

**Por qué importa:** la superficie de ataque de un credential largo (si lo interceptan, acceso indefinido hasta rotación manual) vs un session token (solo durante la sesión actual, no crea sesiones nuevas). El Gateway **nunca deja pasar el credential largo** - el agent runtime recibe un context object con authority ya resuelta.

**authorizeGatewayConnect (src/gateway/auth.ts):** el punto central de enforcement. Token branch:
- Sin token → `{ ok: false, reason: "token_missing" }`
- Token mal → `safeEqualSecret` (constant-time) + rate limit failure → `{ ok: false, reason: "token_mismatch" }`
- Token OK → resetea el limiter → `{ ok: true, method: "token" }`

**safeEqualSecret (src/security/secret-equal.ts):** comparación en tiempo constante para prevenir timing attacks (inferir cuántos chars acertaste por el tiempo de respuesta). **Es la ÚNICA ruta de comparación aprobada** para credenciales en el Gateway. Un fallback a `===` rompe la garantía para esa branch.

**ResolvedGatewayAuth:** separa config del credential. `mode` (none|token|password|trusted-proxy) + `modeSource` (override|config|token|password|default). El modo y su origen se reportan al startup - **diagnóstico de config drift**: si `modeSource: "token"` (inferido de env var) en vez de `"config"`/`"override"`, significa que el modo no fue declarado explícitamente.

**Local vs remote credential resolution (credentials.ts):** separa credenciales locales (Gateway habla con su propia HTTP surface) de remotas (client conecta a Gateway en otro host), basado en `gateway.mode` + `OPENCLAW_SERVICE_KIND=gateway`. En split-topology (macOS app → VM cloud), el app lee `gateway.remote.url` + token local; la VM lee `OPENCLAW_GATEWAY_TOKEN` del env. Rotan de forma independiente.

**Rate limiting como control de confiabilidad + seguridad:** sobrepasar `maxAttempts` en `windowMs` → `rate_limited` + `retryAfterMs` (Retry with Exponential Backoff signal). El count sobrevive resets de conexión → efectivo contra reconnect-looping attackers. Sin rate limit, un cliente misconfigurado en loop tight puede saturar el auth path con miles de log lines.

**Tailscale como variante de Token Exchange:** `auth.allowTailscale: true` → `resolveVerifiedTailscaleUser` hace WhoIs lookup contra el Tailscale control plane. Verifica que la identidad del header `tailscale-user-login` coincide con la identidad del nodo IP. El machine key de Tailscale nunca toca el Gateway; solo un verified user claim (login, email, name) para audit + access decisions. **Mismatch guard:** proxy comprometido que inyecta otro login → `{ ok: false, reason: "tailscale_user_mismatch" }`, tratado como auth failure, no silent pass-through. (Cap 4 completa: zero-trust, mTLS, SOUL.md signing.)

**Net effect:** el credential largo NUNCA llega al agent runtime. El Gateway guarda el secret y reenvía solo un identity claim verificado de corta vida. El agent layer queda least-privileged aunque canales y deployments se multipliquen.

## Verificación en vivo contra nuestro workspace

> Nuestro `openclaw.json` (2026-08-26) confirma el capítulo directamente:

```json
{
  "gateway": {
    "auth": { "mode": "token", "token": "..." },
    "bind": "loopback",
    "mode": "local",
    "port": 18789,
    "tailscale": { "mode": "serve", "resetOnExit": false }
  }
}
```

- `bind: loopback` + `port: 18789` = el default seguro que el libro recomienda para single-host. ✔️
- `mode: token` = Token Exchange explícito (no inferido). ✔️
- `mode: local` = deployment estándar, el mismo proceso que maneja auth + canales. ✔️
- `tailscale: serve` = el patrón de remote webchat (PWA en iPhone) que el capítulo describe como variante Tailscale de Token Exchange. Nuestro webchat remoto ES el caso de uso que motiva la sección. ✔️

**Esto es la ventaja diferencial del estudio:** el libro describe teoría, nosotros la operamos en producción real todos los días.

## Notas de conexión

- **Bulkhead (startup)** → Cap 3 lo desarrolla en profundidad (containing cascading failures).
- **Hook policy / prompt injection** → Cap 5 (PBAC).
- **trusted-proxy pattern** → Cap 10 (rate limiting + versioning para public-facing).
- **Edge agent deployment (remote mode)** → Cap 13.
- **Zero-trust, mTLS, SOUL.md signing** → Cap 4.
- **Shutdown hooks / zero-downtime restart** → Cap 11.
