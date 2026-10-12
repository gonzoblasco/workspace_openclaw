# Módulo 1 · Lección 1 de 30: Respuestas Autónomas en Canales de Chat Activos

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 1
**Lección:** 1 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo (2026-10-12). Registro fiel del contenido del curso; las observaciones de verificación van marcadas aparte al final.

---

## Idea central

Un bot conversacional ingenuo responde de inmediato a cada paquete entrante: interrumpe discusiones humanas, satura canales compartidos y quema cuota de cómputo en mensajes irrelevantes.

En OpenClaw, una respuesta autónoma **eficaz** requiere un ciclo de evaluación previa:

> escucha pasiva -> evalúa el contexto acumulado en la ventana temporal -> decide si intervenir -> calcula un retardo de cortesía antes de emitir cualquier salida.

El fundamento es **desacoplar la ingesta del mensaje de la decisión de emisión**. Al ingresar un payload por Slack, Telegram o Discord, el motor de eventos no invoca ciegamente al LLM: lo somete a una **compuerta contextual** que evalúa tres factores:

1. **Relevancia temática** directa respecto a las responsabilidades asignadas al agente.
2. **Grado de resolución** que la conversación ya alcanzó entre participantes humanos.
3. **Riesgo de redundancia** (generar ruido sobre algo ya dicho).

---

## Anatomía del pipeline de escucha pasiva

Cuando un canal tiene actividad constante, varios participantes escriben rápido, corrigen erratas en líneas separadas o mantienen hilos paralelos. Si el agente reacciona al primer mensaje incompleto, interviene a destiempo con premisas falsas.

Por eso la arquitectura usa un **buffer de agregación con ventana deslizante** antes de invocar la inferencia:

- El receptor de **Webhooks o WebSockets** deposita los mensajes en una cola temporal en memoria.
- Mientras la ventana siga activa, los eventos del mismo usuario o hilo **extienden un temporizador de debouncing**.
- Solo cuando cesa la ráfaga de escritura inmediata, el pipeline **consolida el bloque** y pasa a la fase de arbitraje.

**Detalle clave:** la bifurcación de descarte **no desecha** la información. El mensaje ignorado pasa al **contexto pasivo**: se indexa en la memoria del hilo, para que si más adelante alguien menciona al asistente o hace una pregunta que depende de lo discutido antes, el agente tenga el hilo completo sin haber interrumpido el intercambio.

---

## Configuración del despachador y debounce

Ejemplo del curso: un canal de soporte interno `#infra-helpdesk` donde ingenieros humanos discuten caídas de servidores junto con el agente.

```yaml
version: "2.1"
agent:
  id: "ops-context-bot"
  mode: "autonomous_listener"
channels:
  - id: "slack-infra-helpdesk"
    platform: "slack"
    settings:
      aggregation:
        debounce_seconds: 4
        max_wait_seconds: 12
      arbitration:
        confidence_threshold: 0.78
        require_direct_mention: false
        cooldown_period_seconds: 45
        suppress_if_human_answered: true
      generation:
        simulate_typing: true
        typing_wpm: 90
        base_delay_ms: 1200
```

| Parámetro | Significado |
|---|---|
| `debounce_seconds: 4` | Tras una línea, el bot espera 4 s antes de evaluar. Si llega otra línea, el reloj se reinicia. |
| `max_wait_seconds: 12` | Techo absoluto desde el primer mensaje: quien escribe párrafos largos no bloquea el pipeline para siempre. |
| `confidence_threshold: 0.78` | Puntaje mínimo del clasificador de intenciones para tomar la palabra. |
| `cooldown_period_seconds: 45` | Evita monopolizar el canal: tras emitir, el agente se silencia 45 s salvo mención explícita. |
| `simulate_typing` / `typing_wpm` | En vez de responder al instante (invasivo, rompe la cadencia), activa "está escribiendo..." y gradúa la entrega. |

> **REMEMBER del curso:** en canales de alta concurrencia, **nunca** pongas `debounce_seconds` por debajo de 2 s. Un valor muy bajo fragmenta oraciones de usuarios que aprietan Enter repetido y dispara inferencias innecesarias contra el proveedor.

---

## Lógica del evaluador de intervención

Para decidir si interviene sin mención explícita, OpenClaw usa una función de **arbitraje ligero**: un modelo rápido y barato calcula un vector de probabilidad o una clasificación estructurada **antes** de mandar el historial completo a un modelo generativo más pesado.

```python
import time
from typing import Dict, Any, Tuple
class ArbitrationService:
    def __init__(self, confidence_threshold: float = 0.78, cooldown: int = 45):
        self.threshold = confidence_threshold
        self.cooldown = cooldown
        self.last_reply_timestamps: Dict[str, float] = {}
    def should_intervene(
        self,
        channel_id: str,
        thread_messages: list[Dict[str, str]],
        agent_capabilities: list[str]
    ) -> Tuple[bool, float, str]:
        current_time = time.time()

        # 1. Comprobación de Cooldown
        last_reply = self.last_reply_timestamps.get(channel_id, 0.0)
        if (current_time - last_reply) < self.cooldown:
            return False, 0.0, "Canal en periodo de enfriamiento activo"
        # 2. Comprobación de resolución humana
        last_message = thread_messages[-1]["content"].lower()
        if any(marker in last_message for marker in ["resuelto", "solucionado", "ya quedó", "listo gracias"]):
            return False, 0.1, "Problema resuelto por interacción humana"
        # 3. Cálculo de puntuación de relevancia temática
        score = self._compute_relevance_score(thread_messages, agent_capabilities)
        if score >= self.threshold:
            self.last_reply_timestamps[channel_id] = current_time
            return True, score, "Umbral superado: intervención requerida"
        return False, score, "Puntuación de relevancia insuficiente"
    def _compute_relevance_score(
        self,
        messages: list[Dict[str, str]],
        capabilities: list[str]
    ) -> float:
        text = " ".join([m["content"].lower() for m in messages[-3:]])

        # Ponderación basada en coincidencia de dominios (simplificada para ejecución local)
        matches = sum(1 for cap in capabilities if cap.lower() in text)
        has_interrogative = any(q in text for q in ["cómo", "error", "falla", "dónde", "ayuda", "504", "crash"])

        base_score = 0.35 if has_interrogative else 0.1
        score = base_score + (matches * 0.25)
        return min(round(score, 2), 1.0)
```

Ejemplo de uso con un hilo de incidente:

```python
service = ArbitrationService(confidence_threshold=0.75, cooldown=45)
capabilities = ["redis", "postgres", "timeout", "cluster"]
# Simulación de un hilo donde dos ingenieros reportan un incidente
thread = [
    {"role": "user", "author": "carlos", "content": "Alguien está viendo caídas en staging?"},
    {"role": "user", "author": "marina", "content": "Sí, tenemos un error crítico de timeout en el cluster de redis"}
]
intervene, score, reason = service.should_intervene("slack-infra-helpdesk", thread, capabilities)
print(f"Intervenir: {intervene} | Puntuación: {score} | Motivo: {reason}")
```

Salida:

```text
Intervenir: True | Puntuación: 0.85 | Motivo: Umbral superado: intervención requerida
```

El clasificador detecta el término problema (`error`) más dos capacidades del asistente (`timeout`, `redis`): 0.85, por encima de la barrera de 0.75.

---

## Calibración de umbrales

El balance entre precisión y falsos positivos depende de la naturaleza del equipo:

- **Canal de operaciones críticas:** umbral moderado (**0.70 a 0.75**): se tolera una respuesta no solicitada si previene un incidente largo.
- **Canal de debate general:** umbral alto (**0.85**) o **doble mención** obligatoria, para evitar fricción entre participantes.

---

## Integración del despachador con la API de mensajería

Aprobada la intervención, se ensambla la carga útil **respetando la latencia de cortesía**. Responder en menos de 300 ms desconcierta: es antinatural frente a bloques de texto complejos.

```python
import asyncio
import time
from typing import Dict, Any
class AutonomousDispatcher:
    def __init__(self, platform_client: Any, typing_wpm: int = 90, base_delay_ms: int = 1200):
        self.client = platform_client
        self.typing_wpm = typing_wpm
        self.base_delay = base_delay_ms / 1000.0
    async def dispatch_reply(self, channel_id: str, thread_ts: str, text_payload: str) -> Dict[str, Any]:
        # 1. Calcular duración simulada de tecleo según longitud del texto
        words = len(text_payload.split())
        typing_duration = min((words / self.typing_wpm) * 60.0, 8.0)

        # 2. Retardo base de lectura previa
        await asyncio.sleep(self.base_delay)
        # 3. Disparar indicador de typing en la plataforma
        await self.client.send_typing_indicator(channel_id=channel_id, thread_ts=thread_ts)
        await asyncio.sleep(typing_duration)
        # 4. Entrega formal del mensaje en el hilo correspondiente
        response = await self.client.post_message(
            channel_id=channel_id,
            thread_ts=thread_ts,
            text=text_payload,
            metadata={"source": "openclaw_autonomous_dispatcher"}
        )
        return response
```

El `thread_ts` confina la respuesta autónoma al hilo donde nació el problema, sin colapsar la vista principal.

> **PITFALL del curso:** despachar respuestas autónomas a la **raíz** de canales públicos de alta actividad (en vez de abrir/continuar un hilo) causa confusión contextual inmediata y multiplica las quejas sobre el bot.

---

## Check your understanding

**En un canal activo, ¿cuál es el objetivo principal de configurar un buffer con debouncing antes de invocar al modelo?**

- [ ] Esperar a que nadie escriba en el canal durante al menos 10 minutos.
- [x] **Agrupar las líneas consecutivas de un usuario que escribe en ráfagas antes de invocar la evaluación del agente.**
- [ ] Persistir el historial en una base relacional para auditorías de cumplimiento.
- [ ] Bloquear temporalmente a usuarios que envíen más de cinco mensajes por minuto.

---

## Ejercicio práctico: simulación de una cola de agregación

Comprobar el ciclo sin levantar un cliente de Slack/Discord. Dos productores simulando `dev_ops` y `backend_lead`, y un consumidor que procesa la cola con la lógica de agregación.

```python
import asyncio
import time
from dataclasses import dataclass
@dataclass
class ChatEvent:
    user: str
    text: str
    timestamp: float
class ChannelEventBuffer:
    def __init__(self, debounce_window: float = 2.0):
        self.debounce_window = debounce_window
        self.pending_messages: list[ChatEvent] = []
        self.last_arrival: float = 0.0
    async def push_event(self, event: ChatEvent):
        self.pending_messages.append(event)
        self.last_arrival = time.time()
    async def await_flush(self) -> list[ChatEvent]:
        while True:
            await asyncio.sleep(0.5)
            if self.pending_messages:
                elapsed = time.time() - self.last_arrival
                if elapsed >= self.debounce_window:
                    batch = list(self.pending_messages)
                    self.pending_messages.clear()
                    return batch
async def simulate_traffic(buffer: ChannelEventBuffer):
    # Ráfaga 1: Usuario escribe en varias partes
    print("[12:00:00] Usuario marcos escribe parte 1...")
    await buffer.push_event(ChatEvent("marcos", "hola equipo", time.time()))
    await asyncio.sleep(0.8)

    print("[12:00:01] Usuario marcos escribe parte 2...")
    await buffer.push_event(ChatEvent("marcos", "se cayó la base de staging con error 500", time.time()))
    await asyncio.sleep(0.8)
    print("[12:00:02] Usuario marcos escribe parte 3...")
    await buffer.push_event(ChatEvent("marcos", "alguien sabe qué pasó con postgres?", time.time()))
async def main():
    buf = ChannelEventBuffer(debounce_window=2.0)
    producer_task = asyncio.create_task(simulate_traffic(buf))

    print("Iniciando monitor de escucha pasiva en OpenClaw...")
    batch = await buf.await_flush()
    await producer_task

    consolidated = " ".join([m.text for m in batch])
    print("\n--- Bloque consolidado post-debounce ---")
    print(f"Total mensajes absorbidos: {len(batch)}")
    print(f"Texto listo para arbitraje: \"{consolidated}\"")
if __name__ == "__main__":
    asyncio.run(main())
```

Salida esperada (el evaluador **no** dispara tras el primer "hola equipo"; espera los 2 s de silencio tras el tercer mensaje):

```text
Iniciando monitor de escucha pasiva en OpenClaw...
[12:00:00] Usuario marcos escribe parte 1...
[12:00:01] Usuario marcos escribe parte 2...
[12:00:02] Usuario marcos escribe parte 3...
--- Bloque consolidado post-debounce ---
Total mensajes absorbidos: 3
Texto listo para arbitraje: "hola equipo se cayó la base de staging con error 500 alguien sabe qué pasó con postgres?"
```

---

## Resumen

Las respuestas autónomas en canales activos transforman a OpenClaw de un bot de comandos en un **miembro colaborativo** del equipo. La clave: **nunca responder en caliente a cada evento**.

1. **Agregación con debouncing:** unifica ráfagas de escritura rápida en un bloque coherente y evita inferencias fragmentadas.
2. **Filtro de arbitraje:** evalúa pertinencia técnica, descarta hilos ya resueltos por humanos y respeta periodos de enfriamiento.
3. **Emisión graduada:** protege la experiencia simulando cadencias humanas de lectura/tecleo y canalizando siempre dentro del hilo.

---

## Notas de verificación (Kanam)

- **El config del curso es ilustrativo.** El bloque `agent.config.yaml` (con `mode: "autonomous_listener"`, `arbitration`, etc.) es un ejemplo pedagógico; en una instalación real de OpenClaw la configuración vive en `~/.openclaw/openclaw.json`, y no existe un `agent.config.yaml` en este workspace. Antes de aplicar cualquier parámetro, mapearlo al esquema real (ver docs de configuración del gateway).
- **El código es ejecutable en local** (Python estándar, sin dependencias externas): sirve como sandbox para entender el debounce y el arbitraje sin tocar Slack/Discord.
- **Ejercicio de debounce: verificado, salida exacta.** Corrido en local (Python 3.9.6), reproduce el bloque consolidado de 3 mensajes tal como promete el material.
- **Ejemplo de arbitraje: el material promete `0.85`, el código da `1.00`.** Corrido localmente, la salida real es `Intervenir: True | Puntuación: 1.0`. Causa: el comentario del ejemplo dice "dos capacidades (timeout y redis)", pero `_compute_relevance_score` cuenta coincidencias por **substring** de `capabilities = ["redis", "postgres", "timeout", "cluster"]` sobre el texto del hilo, y el texto contiene **tres** ("redis", "timeout" y "cluster"), no dos. Con `base_score 0.35 + 3 * 0.25 = 1.10`, truncado a `1.0`. Para que diera 0.85 harían falta exactamente 2 coincidencias. **El output impreso en el curso no sale del código que el propio curso muestra** - dato a tener en cuenta si se copia el ejemplo como base: el scoring es un juguete didáctico, no un clasificador real (coincidencia literal, sensible a falsos positivos como "cluster").
- **Próxima lección (teaser del propio curso):** *"filtrado selectivo de notificaciones y menciones directas"*. Coincide con la L02 del plan previo (filtrado de notificaciones) - es la numeración del curso la que manda.
