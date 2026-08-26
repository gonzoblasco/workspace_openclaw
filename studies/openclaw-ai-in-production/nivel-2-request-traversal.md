# Nivel 2 - Request Traversal (Cap 2)

Badge: 🔀 Request Pipeline | Recursos: libro Cap 2 + repo OpenClaw live + workspace real

## Subnivel 2.1 - El pipeline de 6 fases

### Topic: Pipeline de 6 fases

**Teoría (vocabulario con nombre):**
- **Six-phase message flow**: el patrón central de orquestación del request handling. Todo mensaje entrante (Telegram webhook, Discord event, WebSocket control UI, HTTP API) pasa por las mismas 6 fases en el mismo orden.
- **getReplyFromConfig()** (src/auto-reply/reply/get-reply.ts): el orquestador maestro. Acepta MsgContext, devuelve ReplyPayload que el Gateway entrega por el canal de origen.
- **Las 6 fases:**
  1. **Context assembly** - finalizeInboundContext() + applyMediaUnderstanding(): computa session history, memory flush, link understanding. La fase más token-heavy (lee hasta el history limit y puede correr memory compaction).
  2. **Pre-agent hooks** - emitPreAgentMessageHooks(): emite before_agent_start, plugins inspeccionan/mutan el contexto antes de cualquier lógica de agente. Debe ser rápida.
  3. **Command authorization gate** - resolveCommandAuthorization() + initSessionState(): enforce DM pairing, allowlist, per-session sandboxing ANTES de cualquier tool invocation. La más security-sensitive.
  4. **Directive resolution** - resolveReplyDirectives(): parsea directivas inline (/think, /verbose, /elevated, /reset) y las aplica al run config. Debe tolerar el rango más amplio de input malformado sin bloquear.
  5. **Inline action handling** - handleInlineActions(): procesa acciones embebidas (quick replies, location, confirm, buttons, media player). Debe evitar crashear con acciones user-provided.
  6. **Model run** - runPreparedReply(): invoca el model provider con el contexto ensamblado. La fase que más necesita retry (model/network fallan transitoriamente).
- **Cada fase tiene un primary operational concern**, no un "highest budget" separado. No todas las fases son iguales en costo/seguridad/retry.
- **Pipeline determinista**: cada fase pasa su resultado a la siguiente. Extensible insertando fases nuevas, pero no es drop-in (cambia type contracts downstream).

**Práctica:** nuestro flujo diario (mensaje -> contexto -> hooks -> auth -> directivas -> model run) es exactamente este pipeline. Los /fuera, /reasoning, /status que usamos son las directivas inline de la fase 4.

**Verificación (mock interview):** ¿Por qué el pipeline de 6 fases es determinista y reproducible?
**Esperada:** porque cada fase pasa su resultado a la siguiente en orden fijo, con boundaries discretos e instrumentables - lo que lo hace debuggable bajo carga. Correr el mismo mensaje varias veces da resultados comparables.

### Topic: Context assembly + dedupe cache

**Teoría:**
- **finalizeInboundContext()** (src/auto-reply/reply/inbound-context.ts): normaliza el mensaje y chat type en FinalizedMsgContext.
- **buildHistoryContext()**: arma el session history (últimos 50 mensajes por default, configurable via messages.groupChat.historyLimit).
- **resolveMemoryFlushContextWindowTokens()**: resuelve el budget de memory flush (el resumen que reduce tokens cuando la sesión excede la ventana del modelo).
- **applyLinkUnderstanding()**: resumen de links incluidos en el mensaje que el agente debe conocer.
- **Inbound dedupe cache** (src/auto-reply/reply/inbound-dedupe.ts): cache compartida que previene que el mismo provider message corra dos veces para el mismo agente, incluso si un routing bug lo presenta bajo main y direct keys. Global singleton (Symbol.for("openclaw.inboundDedupeCache")). TTL 20 min, max 5000 entries.
- **buildInboundDedupeKey()**: compone la key de idempotencia desde provenance fields: provider + accountId + sessionScope + peerId + threadId + messageId. Devuelve null si falta provider o messageId (esos mensajes saltan dedupe).
- **resolveInboundDedupeSessionScope()**: lee el session key y extrae el agent ID -> session scope `agent:<agentId>`. Crítico: agrupa por agente, así el mismo mensaje no corre dos veces para el mismo agente aunque se presente bajo keys distintas.
- **shouldSkipDuplicateInbound()**: consulta el cache con la key; si ya se procesó, skip.

**Verificación:** ¿Qué garantiza el session scope en el dedupe key y por qué importa?
- Agrupa mensajes por agente (agent:<id>), asegurando que el mismo mensaje físico no corra dos veces para el mismo agente aunque un routing bug lo presente bajo main y direct keys.

## Subnivel 2.2 - Latencia, streaming e idempotencia

### Topic: Tool execution + streaming + idempotency

**Teoría:**
- **Tool execution latency taxonomy**: tool execution NO es una fase numerada - es cross-cutting que el model-run usa. El worked example es el command-poll backoff.
- **recordCommandPoll()** (src/agents/command-poll-backoff.ts): trackea polls vacíos consecutivos por command y deriva el próximo delay. Schedule fijo: 5s -> 10s -> 30s -> 60s.
- **Adaptive polling** (src/agents/bash-tools.process.ts): mismo concepto dentro del bash process tool. Resetea el delay cuando llega output, avanza en el schedule cuando no. Un tool lento nunca starvea el event loop del Gateway.
- **Async streaming como anti-bottleneck primitive**: mantiene el output del modelo fluyendo por WebSocket, así un model call lento/interrumpido no bloquea el Gateway.
- **OpenAIWebSocketManager** (src/agents/openai-ws-connection.ts): dueño de la conexión + auto-reconnect. MAX_RETRIES=5, BACKOFF_DELAYS_MS=[1000,2000,4000,8000,16000]. Resetea retryCount en open, schedulea reconnect con backoff en error.
- **Idempotency key**: "digital fingerprint" de una acción. Si el server ve la misma key, sabe que ya procesó esa request exacta y devuelve el resultado original en vez de duplicar el side effect. Permite retry seguro.
- **buildInboundDedupeKey()** = la idempotency key del pipeline. Garantiza que el mismo provider message nunca se procese dos veces para el mismo agente, bajo retry o routing duplication.

**Verificación:** ¿Por qué el streaming async es el "anti-bottleneck primitive"?
- Porque mantiene el output del modelo fluyendo por WebSocket con auto-reconnect, de modo que un model call lento o interrumpido no bloquea el Gateway ni el event loop. El backoff bounded permite reconectar sin hammering.

### Topic: Access control gates + DM pairing

**Teoría:**
- **Access control es cross-cutting gate** que corre antes de tool invocation - es sobre authorization, no latencia.
- **resolveElevatedPermissions()** (src/auto-reply/reply/reply-elevated.ts): decide si un sender puede usar elevated mode. Síncrono, devuelve { enabled, allowed, failures }. failures es un array que nombra cada gate que rechazó (ej gate:"allowFrom", key:"tools.elevated.allowFrom.<provider>") - el caller puede reportar exactamente por qué se denegó.
- **Dos gates de acceso** deciden si un sender puede invocar tools: (1) channel-layer DM pairing, (2) elevated-mode allowlist en resolveElevatedPermissions.
- **DM pairing como human-in-the-loop access control**: manual safety switch que requiere que un humano apruebe la conexión entre un sistema automatizado y el canal privado de un usuario. Halt antes de enviar respuesta. Previene outreach automatizado no autorizado. Es la mitad channel-layer del control de acceso, enforceada separada del elevated gate.

**Verificación:** ¿Cuáles son los dos gates de acceso y en qué capa vive cada uno?
- DM pairing (channel layer, human-in-the-loop) y elevated-mode allowlist (resolveElevatedPermissions). El DM pairing se enforcea antes, en la capa de canal; el elevated gate decide si los tools elevated están permitidos.

### Topic: Retry con exponential backoff

**Teoría:**
- **computeBackoff()** (src/infra/backoff.ts): convierte un attempt number en delay jittered y capped. BackoffPolicy = { initialMs, maxMs, factor, jitter }. El jitter (base * jitter * random) evita que muchos clients retryen en lockstep tras un outage compartido.
- **retryAsync()** (src/infra/retry.ts): driver del retry loop, módulo separado de backoff.ts. Overload numérico: delay exponencial (initialDelayMs * 2**i). Overload de options: agrega jitter, Retry-After handling, shouldRetry.
- **Announce queue backoff** (src/agents/subagent-announce-queue.ts): el mismo backoff aplicado al drain loop de la announce queue. scheduleAnnounceDrain() drena colas y hace backoff en fallos consecutivos: 2s, 4s, 8s... capped 60s.
- **Distinción clave del cap (bridge a Cap 3):** NO todos los errores se manejan igual.
  - **Transient model/network failures** -> retry silencioso con exponential backoff (el user solo necesita la respuesta final).
  - **Authorization denials, malformed directives, unsafe inline actions** -> surface como mensajes user-facing explícitos (el user/operator debe corregir el request).
  - Esa distinción entre hidden recovery y visible failure es el puente al Cap 3 (aislar fallos para que no se propaguen).

**Verificación:** ¿Por qué el jitter en el backoff es importante en producción?
- Para evitar que muchos clientes retryen en lockstep tras un outage compartido (thundering herd). El jitter esparce los retries aleatoriamente dentro de la ventana computada.

## Cierre del nivel

- **Self-review (rúbrica):**
  - Qué salió bien: el pipeline de 6 fases se mapea 1:1 con nuestro flujo diario (contexto, hooks, auth, directivas /fuera//reasoning//status, model run). La distinción hidden recovery vs visible failure es un insight fuerte para la entrevista.
  - Qué faltó: hands-on de routing multi-binding (mismo pendiente del Cap 1 - no tenemos 2 canales). Verificar modeSource en startup.
- **Pendiente del nivel:** hands-on del cap (2 canales o simular con HTTP endpoint), verificar modeSource.
- **Badge:** 🔀 Request Pipeline (nivel 2 mapeado en primera pasada; XP pendiente de segunda pasada).
