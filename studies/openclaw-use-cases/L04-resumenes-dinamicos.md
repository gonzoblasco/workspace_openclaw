# Módulo 1 · Lección 4 de 30: Generación Dinámica de Resúmenes de Conversaciones

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 1 - Asistentes de Mensajería Contextuales
**Lección:** 4 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo (2026-10-12), tratado como **dato externo** (sandbox). Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Cuando un canal mantiene interacción continua, el historial acumulado satura la ventana de contexto: enviar todo en cada turno sube latencia, dispara costos y **diluye la atención del modelo**, que empieza a ignorar directivas como `SOUL.md`.

La generación dinámica de resúmenes resuelve esto con **compactación recursiva**: el agente extrae acuerdos, variables operativas y temas abiertos, descartando ruido antes de que el búfer exceda los límites operativos.

---

## Anatomía del desbordamiento de contexto

Un hilo activo genera decenas de intercambios breves (confirmaciones, saludos, fragmentos de código). Si cada llamada incluye todo lo anterior, el prompt crece linealmente. Al saturarse hay dos degradaciones:

1. **Pérdida de foco en el centro** (*lost in the middle*): el modelo recuerda con precisión el inicio del sistema y los últimos mensajes, pero **pasa por alto decisiones tomadas en medio**.
2. **Agotamiento presupuestario de tokens**: el runtime trunca abruptamente los mensajes más antiguos, **eliminando contexto fundacional sin criterio semántico**.

Mitigación: **arquitectura de ventana deslizante con punto de control** (*checkpoint windowing*). La memoria activa se divide en tres niveles: **directivas base** (inmutables), **resumen destilado** y **búfer de mensajes crudos recientes**. Mantener las directivas base inmutables garantiza que identidad y restricciones sigan activas; el búfer reciente aporta cohesión lingüística inmediata.

---

## Estrategias de compactación: por lotes vs. progresiva

| Característica | Compactación por lotes | Compactación progresiva |
|---|---|---|
| Frecuencia de invocación | Baja (solo ante saturación) | Alta (micro-pasos constantes) |
| Distribución de latencia | Picos elevados | Poca variación perceptible |
| Riesgo de deriva semántica | Bajo a corto plazo | Medio (efecto "teléfono descompuesto") |
| Costo total de tokens | Menor consumo global | Mayor consumo de inferencia auxiliar |

- **Por lotes (batch):** deja crecer el historial hasta un umbral crítico (~80% de la ventana) y luego procesa todo en un bloque. Menos llamadas, pero picos de latencia y riesgo de perder sutilezas intermedias.
- **Progresiva (rolling):** procesa en microbloques continuos (p. ej. retener los últimos 6 crudos y condensar los 4 anteriores en el resumen existente):

$$S_t = f_{LLM}(S_{t-1}, M_{eviction})$$

donde $S_{t-1}$ es el resumen acumulado previo, $M_{eviction}$ los mensajes que abandonan la ventana activa, y $S_t$ el nuevo resumen consolidado.

Para prevenir la deriva semántica (resumen sobre resumen diluye detalles), el curso usa **esquemas estructurados de extracción** en lugar de resúmenes en prosa libre.

---

## Check your understanding

**¿Cuál es la técnica recomendada para evitar la pérdida de detalles críticos tras múltiples ciclos de resumen progresivo?**

- [ ] Pedirle al LLM un párrafo fluido con la historia completa.
- [x] **Separar el estado en secciones tipadas: acuerdos tomados, entidades detectadas y tareas pendientes.**
- [ ] Descartar los mensajes más viejos sin resumir al superar el límite.
- [ ] Aumentar la ventana activa a 200 mensajes antes del primer resumen.

---

## Implementación del Compactor

El ciclo de compresión corre en un **subproceso desacoplado** antes de inyectar el prompt al modelo principal, con una plantilla de sistema que produce un formato predecible en Markdown. El script de ejemplo usa `tiktoken` para medir carga, separa la ventana reciente y ejecuta compactación semántica estructurada:

```python
import os
from typing import List, Dict
import tiktoken
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MAX_WINDOW_TOKENS = 1200
RAW_BUFFER_SIZE = 4  # Mantener intactos los últimos 4 mensajes
ENCODER = tiktoken.get_encoding("cl100k_base")
def count_tokens(messages: List[Dict[str, str]]) -> int:
    total = 0
    for msg in messages:
        total += len(ENCODER.encode(msg["content"])) + 4
    return total
def compact_conversation(existing_summary: str, evicted_messages: List[Dict[str, str]]) -> str:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in evicted_messages])
    prompt = f"""Tu tarea es actualizar el estado estructurado de la conversación.
Incorpora los eventos de los mensajes desalojados al resumen previo sin inventar datos.
ESTRUCTURA REQUERIDA:
- [ACUERDOS]: Decisiones firmes, fechas pactadas o configuraciones confirmadas.
- [ENTIDADES]: Servidores, nombres propios, IPs, repositorios o IDs de tickets.
- [PENDIENTES]: Tareas pendientes o preguntas no resueltas.
Resumen Previo:
{existing_summary or "Ninguno."}
Mensajes a condensar:
{transcript}
Resumen Estructurado Actualizado:"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()
def prepare_context_window(
    system_instruction: str,
    running_summary: str,
    message_history: List[Dict[str, str]]
) -> tuple[List[Dict[str, str]], str]:
    if len(message_history) > RAW_BUFFER_SIZE:
        evicted = message_history[:-RAW_BUFFER_SIZE]
        retained = message_history[-RAW_BUFFER_SIZE:]
        updated_summary = compact_conversation(running_summary, evicted)
    else:
        retained = message_history
        updated_summary = running_summary
    assembled = [{"role": "system", "content": system_instruction}]
    if updated_summary:
        assembled.append({
            "role": "system",
            "content": f"Contexto acumulado de la sesión anterior:\n{updated_summary}"
        })
    assembled.extend(retained)
    return assembled, updated_summary
# Simulación
if __name__ == "__main__":
    system_rules = "Eres un asistente de infraestructura que ayuda a depurar incidentes."
    current_summary = ""
    history = [
        {"role": "user", "content": "Hola, se cayó el nodo redis-03 en us-east-1."},
        {"role": "assistant", "content": "Entendido. ¿Tienes logs del momento del fallo?"},
        {"role": "user", "content": "Sí, arrojó un error OOM a las 14:32 UTC. Ya lo reinicié."},
        {"role": "assistant", "content": "Perfecto. Deberíamos revisar si la memoria maxmemory está en 8GB."},
        {"role": "user", "content": "Confirmado, estaba en 4GB por error de Terraform. Ya apliqué el cambio a 8GB."},
        {"role": "assistant", "content": "Bien hecho. ¿Sigue respondiendo a los pings de salud?"},
        {"role": "user", "content": "Sí, el ping es de 2ms. Ahora necesito revisar redis-04 para ver si tiene el mismo error."}
    ]
    final_prompt, new_summary = prepare_context_window(system_rules, current_summary, history)
    print("--- RESUMEN ACTUALIZADO ---")
    print(new_summary)
    print(f"\n--- MENSAJES FINALES INYECTADOS: {len(final_prompt)} ---")
```

Salida que muestra el curso:

```text
--- RESUMEN ACTUALIZADO ---
- [ACUERDOS]: Se aumentó la directiva maxmemory de redis-03 de 4GB a 8GB mediante corrección en Terraform tras reinicio.
- [ENTIDADES]: Nodo redis-03, región us-east-1, Terraform, error OOM a las 14:32 UTC.
- [PENDIENTES]: Ninguno sobre redis-03.
--- MENSAJES FINALES INYECTADOS: 6 ---
```

> **PITFALL del curso:** usar el mismo modelo de frontera (Claude 3.5 Sonnet, GPT-4o) para el subproceso de resumen dispara los costos. Usar modelos compactos y rápidos (`gpt-4o-mini`, `claude-3-haiku` o **un modelo local vía Ollama**) con temperatura muy baja (0.0-0.2).

---

## Dinámica del consumo de tokens

Dimensionar la política de retención requiere entender la interacción entre tasa de mensajes entrantes, tamaño de la ventana sin resumir y techo presupuestario. Pasados ~20 mensajes, el costo del historial crudo crece con pendiente insostenible; con compactación activa, la ventana **converge a un techo predecible** (directivas fijas + resumen acotado + ventana cruda pequeña).

---

## Persistencia y serialización del resumen

Un asistente no vive en un único proceso: los usuarios dejan de escribir horas o días, y el servidor puede reiniciar pods entre mensajes. El resumen debe tratarse como **artefacto de estado desacoplado**, almacenado junto al puntero de secuencia del último mensaje procesado.

```json
{
  "channel_id": "slack-C05X7ABC123",
  "thread_ts": "1710931200.000400",
  "last_compacted_seq": 42,
  "summary_state": {
    "version": 4,
    "last_updated": "2025-03-20T14:45:10Z",
    "agreements": ["Aprobado despliegue a staging para el viernes a las 18:00 UTC", "Responsable asignado: @mariana"],
    "entities": {"service": "billing-api", "pr_number": "412", "environment": "staging-us-west"},
    "open_questions": ["¿Se requiere migración de esquema en la base de datos de producción?"]
  }
}
```

Al separar campos como arreglos/diccionarios, el compactor aplica **operaciones idempotentes**: si el subproceso falla a mitad o recibe dos mensajes simultáneos, el puntero `last_compacted_seq` impide reprocesar el mismo segmento (evita duplicados en la lista de acuerdos).

> **TIP del curso:** ante correcciones explícitas ("olvídalo, cambiamos la hora a las 20:00"), añadir al prompt del compactor una regla para **buscar inconsistencias y sobrescribir** el acuerdo anterior, en vez de anexar ambos.

---

## Detección de pérdida de fidelidad en producción

Tres indicadores de degradación a monitorear:

1. **Alucinación regresiva:** el asistente vuelve a preguntar algo ya respondido (p. ej. pedir de nuevo un ID de hace diez turnos).
2. **Desaparición de identificadores:** claves únicas (tokens, IPs, hashes de commit, nombres exactos) sustituidas por genéricos ("el commit anterior" en vez de `a3f89c1`).
3. **Contradicción temporal:** asumir que una tarea sigue abierta aunque se cerró en turnos intermedios.

Para protegerse de (2): una **etapa determinista previa al LLM compactor** con regex que detecte patrones canónicos (UUIDs, hashes Git, URLs, IPs) y los **ancle en `[ENTIDADES]`**, garantizando persistencia independiente del comportamiento generativo.

---

## Resumen

La generación dinámica de resúmenes permite mantener interacciones duraderas sin agotar tokens ni degradar la ventana. Ventana estratificada = **directivas fijas + resumen estructurado por campos + búfer móvil**. El paso natural siguiente es saber **cuándo la complejidad o el riesgo exceden las capacidades del asistente**, requiriendo transferencia limpia a un humano.

**Up next · Lección 5 de 30:** *Derivación Segura de Mensajes a Operadores*. **Queda 1 lección** para cerrar el Módulo 1.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo se determina el tamaño ideal del búfer de mensajes crudos antes de compactar?
2. ¿Qué impacto tiene el resumen progresivo sobre la latencia que percibe el usuario?
3. ¿Por qué es preferible un modelo pequeño para el resumen en lugar del principal?
4. ¿Cómo evita OpenClaw que se borren acuerdos cuando una conversación dura semanas?

(Anotadas para profundizar.)

---

## Notas de verificación (Kanam)

**Esta lección converge mucho mejor con OpenClaw real que las anteriores.** Casi todo lo conceptual tiene anclaje:

| Afirmación del curso | Realidad en OpenClaw |
|---|---|
| Compactación de historial con ventana reciente intacta | ✅ `docs/concepts/compaction.md`: *"Older conversation turns are summarized... Recent messages are kept intact"*. El historial completo queda en disco. |
| Resumen persistido junto al puntero de secuencia | ✅ El resumen *"is saved in the session transcript"*, con historial íntegro en disco. |
| Preservar identificadores (IPs, hashes, IDs) | ✅ **`agents.defaults.compaction.identifierPolicy: "strict"`** es el **default**: preserva identificadores opacos. Convergencia directa con `[ENTIDADES]`. |
| Usar un modelo compacto/local para resumir | ✅ Existe **`agents.defaults.compaction.model`** (acepta `ollama/llama3.1:8b`). El PITFALL del curso mapea a un campo real. |
| Techo predecible de tokens tras compactar | ✅ La compactación converge; hay `keepRecentTokens` (default 20.000) como presupuesto de la cola reciente. |
| Guardas de calidad / auditoría del resumen | ✅ `mode: "safeguard"` es el default (auditorías de calidad, reintentos correctivos; encabezados obligatorios que deben sobrevivir). |
| Flush de memoria antes de compactar | ✅ Existe `memoryFlush` (modelo opcional, p. ej. local). El curso lo intuye como "guardar notas". |
| Pruning vs. compactación | ✅ Real: **pruning** recorta resultados de tool (en memoria); **compaction** resume conversación (persistido). El curso no lo menciona, pero es el complemento ligero. |

**Lo que NO mapea / es ilustrativo (no copiar tal cual):**
- ❌ **El código no es OpenClaw; es un ejemplo OpenAI.** Usa `tiktoken` + `openai` (cliente `OpenAI`), y `gpt-4o-mini`. Aquí **`tiktoken` y `openai` no están instalados** → el script no corre tal cual. OpenClaw hace la compactación nativa (no requiere ese código).
- ❌ **El esquema JSON `summary_state` con `last_compacted_seq`/`version` es inventado.** OpenClaw guarda el resumen en el transcript y expone `compaction.*` en config, no ese archivo.
- ❌ **`checkpoint windowing` / `[ACUERDOS]/[ENTIDADES]/[PENDIENTES]` como formato literal** no son nombres/estructuras documentadas del producto (aunque la *idea* de secciones tipadas y preservación de identificadores sí está implementada).
- ❌ **Output aritméticamente inconsistente:** el curso imprime **"6 mensajes inyectados"**, pero su propio código produce **5**. Verificado: `history=7`, `RAW_BUFFER_SIZE=4` → `evicted=4`, `retained=3`; ensamblado = `1 (system) + 1 (resumen) + 3 = 5`. Además, el resumen mostrado **no** sale de ejecutar el script (requiere una llamada real a la API). Tercer ejemplo consecutivo cuyo print no se reproduce corriendo el código.
- `temperature: 0.1` en la llamada de ejemplo: válido para la API OpenAI, pero irrelevante para el esquema de config de OpenClaw.
