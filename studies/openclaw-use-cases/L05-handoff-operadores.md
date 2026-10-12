# Módulo 1 · Lección 5 de 30: Derivación Segura de Mensajes a Operadores (Human-in-the-Loop)

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 1 - Asistentes de Mensajería Contextuales
**Lección:** 5 de 30 · **cierra el Módulo 1**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo (2026-10-12), tratado como **dato externo** (sandbox). Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

La derivación segura (human-in-the-loop o *handoff*) es el mecanismo por el cual un agente de OpenClaw **suspende temporalmente su autonomía** para transferir el control de la conversación a una persona. De nada sirve delegar respuestas o resumir interacciones si el sistema intenta responder peticiones que comprometen la seguridad, tocan transacciones irreversibles o superan su umbral de certeza.

Cuando ocurre una derivación, no basta con silenciar al bot. Exige **tres garantías simultáneas:**

1. El agente **detiene de inmediato** la emisión de respuestas automáticas en ese hilo.
2. Se **inyecta el contexto consolidado** en la interfaz del operador sin saturar el canal público.
3. Se mantiene un **canal de supervisión** para reanudar el control **solo cuando el humano libere la sesión explícitamente**.

---

## Anatomía del protocolo de desvío y estados de sesión

Una sesión no es un flujo binario abierto/cerrado, sino una **máquina de estados finitos** gestionada a nivel de canal. Mientras el hilo está en `autonomous`, cada mensaje dispara el ciclo habitual. Cuando se detecta una condición de traspaso, la sesión transita a `escalated` / `human_pending`, lo que **inhibe cualquier webhook de respuesta saliente** hacia el usuario.

El control vive en la **persistencia del estado** (almacenamiento local o clave-valor del workspace). El runtime evalúa ese valor **antes** de consultar al modelo, evitando colisiones donde operador y agente contesten a la vez.

```text
                 condición de traspaso
   autonomous ─────────────────────────► human_pending
       ▲                                   │
       │                                   │ operador acepta
       │ /release                          ▼
       └──────────────────────────── handoff_active
```

- En `human_pending`, OpenClaw invoca un **webhook de notificación interna** (Slack/Discord del equipo) y **encola el ticket**. Desde ese instante, el procesador descarta cualquier intento del modelo de generar texto para el usuario final.
- Si un operador acepta, la sesión pasa a `handoff_active`: los mensajes del usuario se enrutan **solo** a la pantalla del operador, y las respuestas del operador se envían al canal del cliente con la identidad visual correspondiente.
- Cuando el operador culmina, ejecuta `/release`: la sesión vuelve a `autonomous` y reanuda el bucle.

---

## Criterios de derivación: heurísticas vs. clasificación semántica

Un sistema robusto **no confía la derivación a un único método**. Palabras clave solas omiten sarcasmo o giros indirectos; delegar todo a un LLM agrega latencia y costo a mensajes obvios. La arquitectura combina **tres capas jerárquicas:**

1. **Determinista** (regex y comandos explícitos): en memoria local, antes de llamar a cualquier API. Captura "quiero hablar con una persona", "agente humano", `/ayuda`.
2. **Sentimiento y repetición:** monitorea la entropía. Si el usuario repite la misma pregunta 3 veces en una ventana de 4 mensajes, o la polaridad cae por debajo de un umbral negativo crítico, deriva de forma preventiva.
3. **Semántica** (intenciones críticas): el modelo evalúa si la consulta cae en categorías restringidas de las directivas del agente (disputa de cobros, cancelación por fraude, amenazas legales).

```json
{
  "routing_rules": {
    "deterministic_keywords": ["^humano$", "^operador$", "^representante$", "^asesor$"],
    "max_unresolved_turns": 3,
    "restricted_intents": ["disputa_reembolso", "incidente_seguridad", "cancelacion_urgente"],
    "sentiment_threshold": -0.65
  }
}
```

Un mensaje con la palabra exacta "operador" detiene la inferencia en ~0 ms y deriva. Un cliente describiendo un cobro duplicado pasa por el analizador semántico, reconoce `disputa_reembolso` y activa la transferencia **antes** de que el agente prometa un reintegro financiero no autorizado.

---

## El paquete de transferencia (Handoff Payload)

La falla más común del handoff es transferir un **hilo en blanco**, obligando al operador a preguntar "¿en qué le puedo ayudar hoy?" (destruye la experiencia y desperdicia minutos). OpenClaw lo resuelve empaquetando un payload estructurado en el momento de la transición: **resumen dinámico** de la conversación (la rutina de síntesis de la lección anterior), **entidades extraídas** (IDs de cliente, referencias de producto, direcciones) y el **motivo exacto** de la escalación. Se transmite al bus de mensajería del equipo; los operadores reciben una tarjeta interactiva para reclamar la conversación, y en el canal del usuario se emite un mensaje de espera.

---

## Implementación del controlador de derivación

Un **middleware/interceptor** en el pipeline de mensajería intercepta cada mensaje entrante antes de invocar el motor de razonamiento. Ejemplo del curso en TypeScript:

```typescript
import { MessageContext, AgentResponse, SessionState } from '@openclaw/core';
import { QueueManager } from './queueManager';

const config = {
  keywords: [/^\/?(humano|operador|asesor|ayuda)$/i],
  restrictedIntents: ['disputa_reembolso', 'incidente_seguridad']
};

export async function handleIncomingMessage(ctx: MessageContext, queue: QueueManager): Promise<AgentResponse | null> {
  const currentStatus = await ctx.store.get<SessionState>(`session:${ctx.sessionId}:status`) || SessionState.Autonomous;

  // Si un operador ya atiende la sesión, silenciar al agente
  if (currentStatus === SessionState.HandoffActive) {
    await queue.forwardMessageToOperator(ctx.sessionId, ctx.message.text);
    return null; // El agente no emite texto
  }
  // 1. Detección determinista (regex)
  if (config.keywords.some(r => r.test(ctx.message.text.trim()))) {
    return await triggerHandoff(ctx, queue, 'deterministic_keyword', 'Solicitud directa del usuario');
  }
  // 2. Detección semántica (intención crítica)
  const intentCheck = await ctx.classifier.detectIntent(ctx.message.text);
  if (config.restrictedIntents.includes(intentCheck.name)) {
    return await triggerHandoff(ctx, queue, 'restricted_intent', `Intención crítica: ${intentCheck.name}`);
  }
  // 3. Flujo autónomo normal
  return ctx.agent.executeTurn(ctx);
}

async function triggerHandoff(ctx: MessageContext, queue: QueueManager, triggerType: string, reason: string): Promise<AgentResponse> {
  await ctx.store.set(`session:${ctx.sessionId}:status`, SessionState.HumanPending); // transición atómica
  const summary = await ctx.memory.generateDynamicSummary(ctx.sessionId);
  const entities = await ctx.memory.getExtractedEntities(ctx.sessionId);
  const payload = { sessionId: ctx.sessionId, channel: ctx.channelId, triggerType, reason, summary, entities, timestamp: new Date().toISOString() };
  await queue.enqueueTicket(payload);
  return { text: 'He transferido tu caso a un especialista de nuestro equipo. En un momento continuará la atención por este mismo chat.', status: 'transferred' };
}
```

El controlador **sella la sesión antes** de emitir la confirmación al cliente: al cambiar a `HumanPending`, los mensajes subsiguientes se encolan sin despertar al modelo.

> **PITFALL del curso:** **nunca** uses una variable en memoria local (`let isEscalated = true`) para rastrear el handoff. Si la instancia se reinicia o corre en múltiples réplicas detrás de un balanceador, el bot volverá a responder **encima** del operador humano. El estado debe vivir siempre en el **almacenamiento compartido**.

---

## Retorno seguro del control al agente (`/release`)

Si un caso termina y la sesión queda en `handoff_active`, los mensajes futuros se pierden. La reanudación debe ser **explícita y sanitizada:**

1. **Invocación:** el operador envía `/release` o pulsa "Finalizar atención".
2. **Inyección del resumen de resolución:** el operador puede dejar una nota breve ("Se emitió reembolso manual por $15"); OpenClaw la inyecta en la memoria del workspace.
3. **Restablecimiento:** `session:<id>:status` vuelve a `autonomous`.
4. **Confirmación al usuario:** notifica el cierre o espera la próxima interacción.

```typescript
export async function handleOperatorRelease(sessionId: string, operatorId: string, resolutionNote: string, ctx: MessageContext): Promise<void> {
  await ctx.memory.appendNote(sessionId, { author: `operator:${operatorId}`, note: resolutionNote, timestamp: new Date().toISOString() });
  await ctx.store.set(`session:${sessionId}:status`, SessionState.Autonomous);
  await ctx.messaging.send(sessionId, 'La atención con el especialista ha finalizado. Si tienes otra consulta, aquí sigo para ayudarte.');
}
```

Al documentar la nota en memoria persistente, si el usuario vuelve 5 minutos después con una duda relacionada, el agente accede a lo que el operador resolvió y evita respuestas contradictorias.

> **REMEMBER del curso:** todo evento de derivación debe registrarse en las métricas con su **motivo exacto** (`deterministic_keyword`, `restricted_intent`, `timeout`). Derivaciones frecuentes por intenciones no contempladas son la **principal señal** de que las directivas del agente requieren actualización.

---

## Check your understanding

**Si un operador humano entra a un canal activo y responde al usuario SIN modificar el estado de la sesión, ¿qué ocurre técnicamente?**

- [ ] El sistema funciona sin problemas porque el operador tiene prioridad natural en el socket.
- [x] **El bot continuará respondiendo automáticamente en el hilo a menos que el estado de la sesión se actualice a un modo silenciado.**
- [ ] El LLM detectará automáticamente la presencia del operador por el remitente y dejará de inferir.

---

## Ejercicio guiado: directivas de derivación

**Paso 1** - `routing.config.json` con palabras reservadas e intenciones:

```json
{
  "handoff": {
    "enabled": true,
    "target_channel": "slack://hooks.slack.com/services/T00/B00/XXXXXX",
    "triggers": {
      "keywords": ["operador", "representante", "cancelar servicio", "hablar con alguien"],
      "restricted_categories": ["facturacion_disputa", "fuga_datos", "queja_grave"],
      "sentiment_threshold": -0.7
    },
    "timeout_seconds": 900
  }
}
```

**Paso 2** - ante dos entradas, verificar en logs que la consulta regular ("¿Dónde veo mis facturas?") invoca `ctx.agent.executeTurn()`, y la de escalación ("Quiero cancelar el servicio y hablar con un representante ya mismo") activa `triggerHandoff()`, detiene el modelo, genera el JSON para el webhook y emite el mensaje de transición.

---

## Resumen

La derivación segura es la **salvaguarda indispensable** para operar agentes en canales sin incurrir en riesgos operativos o legales. Modelar la conversación como máquina de estados explícita (`autonomous → human_pending → handoff_active → autonomous`), silenciar al bot a nivel de middleware **antes** de la inferencia, y proveer al operador un payload con contexto consolidado, hace que OpenClaw opere como un colaborador confiable que **sabe cuándo responder y cuándo ceder la palabra**.

**UP NEXT · Lección 6 de 30:** *Configuración de Tareas Periódicas con Cron* - **inicia el Módulo 2: Tareas Programadas y Rutinas Autónomas.**

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo evita OpenClaw que un usuario quede atrapado indefinidamente si ningún operador acepta el ticket en `human_pending`?
2. ¿Qué pasa con el historial que el operador intercambió con el cliente una vez ejecutado `/release`?
3. ¿Se puede activar el handoff solo en horario laboral y usar una directiva especial fuera de horario?
4. ¿Cómo afecta la derivación segura al cálculo de costos de tokens?

(Anotadas para profundizar.)

---

## Notas de verificación (Kanam)

**Base conceptual: sólida y coherente.** El patrón human-in-the-loop (máquina de estados explícita, silenciar antes de inferir, handoff payload, `/release` con nota de resolución, estado en almacenamiento compartido y no en memoria local, métricas por motivo) es **buena ingeniería** y coincide con el marco que el workspace ya adoptó (ADR-086: *"la escalación como entrega de mando y no como alerta"*, la L4 del embudo). El PITFALL del estado en memoria local es **correcto y crítico**: un proceso efímero que se reinicia reanuda respuestas sobre el operador. Este es el mismo principio que el propio `AGENTS.md`/ADR-086 documenta.

**Lo que NO existe en la instalación real (el curso lo presenta como producto):**
- ❌ **`/release` no es un slash command de OpenClaw.** Verificado contra la lista real (`tools/slash-commands.md`): existen `/compact`, `/new`, `/status`, `/reset`, `/model`, `/queue`, `/session`, `/steer`, `/loop`, `/reasoning`… **no `/release`**. La derivación a operador y su liberación **no son una feature nativa con ese comando**; la máquina de estados `autonomous/human_pending/handoff_active` es un **modelo pedagógico** que uno construiría **encima** de OpenClaw, no un estado interno del producto.
- ❌ **`@openclaw/core` no existe como paquete.** El import `from '@openclaw/core'` (con `MessageContext`, `AgentResponse`, `SessionState`, `ctx.classifier`, `ctx.memory.generateDynamicSummary`, `queueManager`) es **inventado**. Los paquetes reales bajo `@openclaw/` instalados son `ai`, `fs-safe`, `proxyline` - no un `core` con esa API. El middleware **no es código que corra** contra OpenClaw tal cual.
- ❌ **`SessionState.HumanPending` / `HandoffActive` no aparecen en el runtime ni en la doc.** Es una abstracción del curso.
- ❌ **`ctx.classifier` / `ctx.memory` / `ctx.store` / `queueManager` / `enqueueTicket` / `forwardMessageToOperator`**: API inventada, sin correlato en el SDK real.

**Patrón (quinto caso):** el curso enseña **conceptos correctos y valiosos** (por qué y cómo derivar) envueltos en **detalles de implementación fabricados** (un paquete `@openclaw/core`, un comando `/release`, enums de estado). Sirve como **guía de diseño**; **no es código ejecutable** ni una feature nativa. El valor real: define el *qué* (máquina de estados, tres capas de detección, payload, liberación explícita, estado compartido); el *cómo* hay que construirlo con las piezas reales de OpenClaw (hooks de canal, almacenamiento, `message`/`automations`), no con las clases del ejemplo.

**Cierre del Módulo 1.** Con esta lección se completan las 5 lecciones prometidas del módulo *"Asistentes de Mensajería Contextuales"*. La Lección 6 abre el **Módulo 2: Tareas Programadas y Rutinas Autónomas** (arranca con *Configuración de Tareas Periódicas con Cron*).
