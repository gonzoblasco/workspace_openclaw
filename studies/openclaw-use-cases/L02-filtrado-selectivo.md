# Módulo 1 · Lección 2 de 30: Filtrado Selectivo de Notificaciones y Menciones

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 1 - Asistentes de Mensajería Contextuales
**Lección:** 2 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo (2026-10-12). Registro fiel del contenido del curso; las observaciones de verificación van marcadas aparte al final.

---

## Idea central

Conectar un agente autónomo directamente a canales activos (Slack, Discord, Telegram) **sin una capa de discriminación** genera fatiga de notificaciones, saturación de llamadas al LLM y respuestas erráticas a mensajes que nunca requerían atención. Un bot ingenuo despierta ante cualquier evento donde aparezca su nombre o `@mention`, procesando saludos casuales, hilos secundarios o discusiones entre humanos con el mismo costo y latencia que una solicitud crítica.

El filtrado selectivo transforma el flujo entrante en un **embudo jerárquico**. En lugar de delegar cada evento al modelo principal, el sistema evalúa **metadatos del canal, jerarquías de mención y reglas sintácticas** antes de decidir si el agente debe intervenir, actualizar su contexto silenciosamente o ignorar el mensaje por completo.

---

## Anatomía del tráfico entrante y niveles de activación

El webhook entrega un **payload enriquecido** que describe no solo el texto plano, sino el entorno: `channel_id`, tipo de interacción (`direct_message`, `thread_reply`, `channel_mention`), rol del emisor y presencia de menciones masivas (`@channel` / `@here`).

Tres niveles de activación:

| Nivel | Acción | Costo |
|---|---|---|
| **Ignorado estricto (Drop)** | Descartado en milisegundos por código determinista, sin invocar embeddings ni modelos. | ~0 |
| **Observación pasiva (Context Ingest)** | No exige respuesta, pero se guarda en el búfer local para no perder el hilo temporal. | bajo |
| **Respuesta activa (Dispatch)** | Cumple relevancia semántica, permisos y urgencia: dispara el agente. | alto |

Las **menciones masivas** (`@everyone`, `@here`) son el error más común: se descartan de inmediato salvo que el agente esté configurado explícitamente para moderación de anuncios. Procesar un `@here` como solicitud directa hace que el bot interrumpa transmisiones generales con respuestas fuera de lugar.

```text
Evento entrante
   │
   ├─ ¿bot / subtype de sistema? ──────────────► DROP
   ├─ ¿canal no registrado? ────────────────────► DROP
   ├─ ¿mención de difusión (@here/@channel)? ───► DROP
   ├─ ¿canal pasivo? ───────────────────────────► INGEST
   ├─ ¿mención directa o hilo del bot? ─────────► DISPATCH
   └─ resto (canal activo sin mención) ─────────► INGEST
```

---

## Reglas estáticas: listas blancas, canales y roles

El filtrado más eficiente ocurre en la **frontera del sistema**: en vez de procesar el significado del texto, OpenClaw evalúa si las **coordenadas** del mensaje están autorizadas mediante una política declarativa. ACLs para tres entidades:

- `allowed_channels`: canales donde el bot puede responder activamente.
- `passive_channels`: canales donde lee y almacena historial, pero **no** puede emitir respuestas públicas.
- `allowed_roles` / `allowed_users`: quiénes tienen autoridad para invocar herramientas del agente.

```yaml
message_filter:
  channels:
    deny_all_by_default: true
    active:
      - "C048A1B2C3D"   # #soporte-tecnico
      - "C099F8E7D6C"   # #infraestructura-devops
    passive:
      - "C012X3Y4Z5W"   # #incidencias-general
  users:
    restricted_mode: false
    blacklist:
      - "USLACKBOT"
      - "B0123456789"   # Bot de CI/CD
  ignore_broadcast_mentions: true
  ignore_bot_messages: true
  min_message_length: 3
```

> **PITFALL del curso:** no ignorar explícitamente los mensajes de otros bots (`ignore_bot_messages: true`) puede crear **bucles infinitos de retroalimentación** donde dos agentes se responden mutuamente hasta agotar el límite de tasa de la API.

---

## Heurísticas de relevancia y expresiones regulares

Una mención explícita no siempre demanda respuesta compleja: los usuarios mencionan asistentes para confirmar presencia ("estás ahí?"), etiquetarlos en conversaciones ajenas ("esto lo puede revisar más tarde") o **dentro de bloques de código y citas**. OpenClaw intercala un **evaluador sintáctico** antes del despacho: descarta patrones vacíos y preclasifica la intención.

```python
import re
from typing import Dict, Any, Optional

class NotificationFilter:
    def __init__(self, bot_id: str, active_channels: set, passive_channels: set):
        self.bot_id = bot_id
        self.active_channels = active_channels
        self.passive_channels = passive_channels
        # Excluir menciones dentro de bloques de código markdown
        self.code_block_pattern = re.compile(r"```[\s\S]*?```|`[^`]+`")
        # Identificar menciones de difusión
        self.broadcast_pattern = re.compile(r"<!(?:here|channel|everyone)>|@(everyone|here)")

    def evaluate(self, event: Dict[str, Any]) -> str:
        """Devuelve el estado de procesamiento: 'DROP', 'INGEST' o 'DISPATCH'"""
        # 1. Descartar eventos de otros bots o subtipos de sistema
        if event.get("bot_id") or event.get("subtype") in ["channel_join", "channel_leave"]:
            return "DROP"
        channel = event.get("channel")
        raw_text = event.get("text", "")
        # 2. Descartar si el canal no está registrado
        if channel not in self.active_channels and channel not in self.passive_channels:
            return "DROP"
        # 3. Limpiar bloques de código antes de comprobar menciones
        text_without_code = self.code_block_pattern.sub("", raw_text)
        # 4. Descartar menciones de difusión
        if self.broadcast_pattern.search(text_without_code):
            return "DROP"
        # 5. Comprobar si el bot fue mencionado directamente
        bot_mention = f"<@{self.bot_id}>"
        has_direct_mention = bot_mention in text_without_code
        # Si el canal es solo pasivo, nunca se despacha respuesta activa
        if channel in self.passive_channels:
            return "INGEST"
        # En canal activo, despachar solo si hay mención directa o es hilo abierto por el bot
        is_thread_reply_to_bot = event.get("thread_ts") and event.get("parent_user_id") == self.bot_id
        if has_direct_mention or is_thread_reply_to_bot:
            # Descartar si el mensaje no tiene contenido útil tras remover la mención
            cleaned_text = text_without_code.replace(bot_mention, "").strip()
            if len(cleaned_text) < 2:
                return "DROP"
            return "DISPATCH"
        return "INGEST"
```

El pipeline evita el costo de transferir cadenas extensas cuando la mención fue accidental o parte de un snippet técnico compartido entre desarrolladores.

---

## Gestión del contexto en hilos de conversación

Una mención directa suele ser solo el primer mensaje de una cadena. Una vez que el bot responde y genera un hilo, procesar **solo** las menciones directas rompe la fluidez: los humanos esperan responder en el hilo sin volver a tipear `@openclaw` cada vez.

OpenClaw implementa un **rastreador de estado por hilo** que evalúa la propiedad `thread_ts` (Slack) o el id del mensaje padre (Discord/Telegram):

```text
Canal público (sin mención) ─────────────► DROP
Canal público (@openclaw)   ─────────────► Inicia hilo + DISPATCH
                                             │
                             Hilo creado por el bot
                                             ├─ Usuario responde sin mención ─────► DISPATCH (si ventana < TTL)
                                             └─ Usuario responde tras inactividad ─► DROP / INGEST
```

Regla de resolución para mensajes dentro de un hilo activo:

```text
Activar en Hilo = (ParentMessage.author == BotID)
                  ∧ (Δt < ThreadTTL)
                  ∧ (User ∉ Blacklist)
```

Si el hilo lo inició el bot y `Δt` desde el último mensaje no supera el TTL (típicamente 10-30 min), el mensaje se despacha **sin exigir mención**. Superado el lapso, el hilo expira y requiere mención explícita, para que el bot no participe en conversaciones paralelas cuando el tema ya concluyó.

> **TIP del curso:** configurá un umbral de silencio (`thread_idle_timeout: 900s`). Permite que el equipo siga debatiendo dentro del hilo sin que el agente intervenga ante cada mensaje nuevo.

---

## Rate limiting y contención de ráfagas

Aun superando listas blancas y reglas sintácticas, una oleada de menciones puede saturar las cuotas del proveedor de modelo. OpenClaw usa **Token Bucket** a nivel de canal y de usuario: cada interacción descuenta créditos; si el depósito se vacía, los mensajes sobrantes se encolan en baja prioridad o se rechazan con una notificación silenciosa.

```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, capacity: int = 5, refill_rate_per_sec: float = 0.2):
        # Capacidad máxima de tokens (mensajes permitidos en ráfaga)
        self.capacity = capacity
        # Tasa de recarga: 0.2 tokens/seg = 1 mensaje cada 5 segundos
        self.refill_rate = refill_rate_per_sec
        self.buckets = defaultdict(lambda: {"tokens": float(capacity), "last_update": time.time()})

    def allow_request(self, user_id: str) -> bool:
        now = time.time()
        bucket = self.buckets[user_id]
        # Calcular tokens acumulados desde la última interacción
        elapsed = now - bucket["last_update"]
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + elapsed * self.refill_rate)
        bucket["last_update"] = now
        # Consumir un token si está disponible
        if bucket["tokens"] >= 1.0:
            bucket["tokens"] -= 1.0
            return True
        return False
```

Integrarlo al pipeline garantiza que ningún usuario agote los recursos del agente, incluso si manda comandos en bucle o etiqueta al bot repetidamente.

---

## Configuración completa de filtrado en OpenClaw

En producción, todas las capas convergen en el archivo principal del conector (`config/messaging.json` o equivalente):

```json
{
  "messaging": {
    "engine": "slack",
    "filter_pipeline": {
      "enabled": true,
      "rules": {
        "drop_broadcast_mentions": true,
        "strip_code_blocks_before_eval": true,
        "min_character_length": 3,
        "ignore_bots": true
      },
      "channels": {
        "whitelist_active": ["C048A1B2C3D", "C099F8E7D6C"],
        "whitelist_passive": ["C012X3Y4Z5W"],
        "fallback_action": "DROP"
      },
      "threads": {
        "auto_track_replies": true,
        "ttl_seconds": 900
      },
      "rate_limits": {
        "user_capacity": 5,
        "refill_rate_per_sec": 0.2
      }
    }
  }
}
```

Esto **desacopla el costo de infraestructura del volumen bruto de tráfico**: el modelo solo se activa cuando hay intención real, contextual y autorizada.

---

## Check your understanding

**Si un usuario escribe en un canal activo `#soporte`: "Ejecuta `@openclaw status` para comprobar los servicios", ¿qué acción toma el pipeline?**

- [ ] DISPATCH, porque `#soporte` es activo y el mensaje contiene la mención literal `@openclaw`.
- [x] **DROP, porque la mención está contenida dentro de un bloque de código inline y se elimina en el preprocesamiento sintáctico.**
- [ ] INGEST, porque el mensaje contiene información diagnóstica que debe guardarse en la memoria pasiva.

> ⚠️ **Ver nota en la sección final:** la respuesta que el curso marca como correcta (DROP) **no coincide** con lo que devuelve el código que el propio curso muestra.

---

## Ejercicio práctico: filtro con descarte de citas

Filtrar un payload entrante considerando que las **citas** (líneas que empiezan con `>`) no deben activar al bot si la mención está dentro del bloque citado.

Requisitos: descartar si viene de un bot (`is_bot: true`); remover líneas que empiezan con `>`; si tras limpiar queda la mención directa (`<@BOT123>`) → `DISPATCH`; si no → `DROP`.

```python
import re

def process_message_event(event: dict, bot_id: str) -> str:
    # Paso 1: Comprobar emisor
    if event.get("is_bot", False):
        return "DROP"
    raw_text = event.get("text", "")
    # Paso 2: Remover líneas de citas (Markdown blockquotes)
    cleaned_lines = [
        line for line in raw_text.splitlines()
        if not line.strip().startswith(">")
    ]
    cleaned_text = "\n".join(cleaned_lines)
    # Paso 3: Evaluar presencia de mención en el texto restante
    target_mention = f"<@{bot_id}>"
    if target_mention in cleaned_text:
        return "DISPATCH"
    return "DROP"

# Prueba 1: Mención en una cita que debe ignorarse
payload_quote = {
    "is_bot": False,
    "text": "> El usuario preguntó a <@BOT123> sobre los logs\nEstoy de acuerdo con esa observación."
}
print(process_message_event(payload_quote, "BOT123"))
# Salida esperada: DROP

# Prueba 2: Mención fuera de la cita que debe atenderse
payload_direct = {
    "is_bot": False,
    "text": "> El servidor falló\n<@BOT123> puedes revisar qué pasó?"
}
print(process_message_event(payload_direct, "BOT123"))
# Salida esperada: DISPATCH
```

---

## Resumen

El filtrado selectivo protege la disponibilidad y el presupuesto del agente. El pipeline combina: **validaciones estáticas** de canal/usuario, **limpiadores sintácticos** (menciones masivas, código, citas), **seguimiento temporal de hilos** y **rate limiting**. Con el tráfico entrante limpio y discriminado, el siguiente paso es **moldear la personalidad y el estilo** de las respuestas mediante archivos de directivas de comportamiento.

**Up next · Lección 3 de 30:** *Configuración del Tono Asistido con SOUL.md*.

---

## Notas de verificación (Kanam)

- **Verificado local (Python 3.9.6):**
  - Ejercicio de citas: Prueba 1 → `DROP` ✅ y Prueba 2 → `DISPATCH` ✅. Salida **exacta** a lo prometido.
  - `RateLimiter` (capacidad 5, refill 0.2/s): 6 requests seguidas → `[True, True, True, True, True, False]`. Coherente con la capacidad declarada.
- **⚠️ Hallazgo: el "check your understanding" contradice al código del propio curso.** El curso marca **DROP** como correcto, pero el `NotificationFilter` que muestra devuelve en ese escenario **`INGEST`**: al eliminar el bloque de código inline la mención desaparece, y en un canal **activo** sin mención directa el código cae en su rama final `return "INGEST"` (observación pasiva), no en `DROP`. Para obtener `DROP` ese escenario tendría que fallar una validación previa (bot, canal no registrado, difusión o texto útil < 2), y ninguna aplica. **La clave del quiz no sale del código que el curso muestra** - mismo patrón que el `0.85` vs `1.0` de la Lección 1: el output/marcado pedagógico no se reproduce ejecutando el ejemplo.
- **Config ilustrativa, no real.** `message_filter` (YAML) y `config/messaging.json` son ejemplos pedagógicos. En esta instalación la configuración vive en `~/.openclaw/openclaw.json`; no hay `config/messaging.json` ni `agent.config.yaml` en el workspace. Mapear parámetros al esquema real antes de aplicar.
- **Preguntas abiertas del propio curso** (sección "Can you answer these?"): canal privado/DM vs público; impacto del almacenamiento pasivo en la ventana de contexto; distinción mención intencional vs cita en plataformas sin markdown; reconexión de hilos antiguos días después. Quedan como material para profundizar (no resueltas acá).
