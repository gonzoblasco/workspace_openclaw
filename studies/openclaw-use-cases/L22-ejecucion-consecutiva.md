# Módulo 5 · Lección 22 de 30: Ejecución Consecutiva de Herramientas y Habilidades

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 5 - Encadenamiento en Bucle Agéntico
**Lección:** 22 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

En un bucle agéntico, una tarea rara vez se resuelve con una única llamada a herramienta. El verdadero trabajo empieza al **encadenar la salida de una función como entrada de la siguiente** sin intervención humana. No es un script determinista de tuberías rígidas: es un **ciclo iterativo** donde el LLM actúa como motor de decisión, evaluando el resultado de una acción antes de seleccionar y parametrizar la siguiente habilidad.

Esto exige preservar la coherencia del estado a través del **contexto de conversación**: cada herramienta devuelve una respuesta estructurada que se reinyecta en el historial; el agente la parsea, **actualiza su modelo mental** y emite una nueva `tool_call` adaptada a los hallazgos inmediatos.

---

## Anatomía del ciclo de paso de argumentos

Patrón estricto de **solicitud → ejecución → retroalimentación contextual**. Ante "auditar un repositorio y reportar vulnerabilidades", el agente no corre un comando monolítico: emite una intención hacia el runtime para invocar una herramienta, **suspende su generación de texto libre** y espera el payload de respuesta.

El núcleo es la **transformación de datos entre llamadas**. Una herramienta de bajo nivel (`fs.read_file`) entrega texto/buffers; el agente lo analiza semánticamente, extrae identificadores clave (hashes de commit, nombres de funciones) y **construye dinámicamente** los argumentos de la siguiente (`security.scan_ast`). La salida de una función **rara vez encaja limpia** en el esquema de la siguiente sin esa capa intermedia de razonamiento.

---

## Registro y preservación del contexto entre llamadas

Para que dos herramientas cooperen, el resultado de la primera debe persistir en la ventana de contexto sin degradar rendimiento ni desbordar tokens. El runtime integra la respuesta como un mensaje con **rol `tool`** asociado al **`tool_call_id`** de la llamada previa.

Si el modelo pierde el identificador o los datos intermedios se truncan agresivamente, la siguiente llamada sufre **alucinación de argumentos**. Si un log de 400 líneas solo tiene 2 relevantes, volcarlo entero satura el búfer y diluye la atención: la estrategia es dotar al agente de **herramientas intermedias de extracción** o canalizar salidas como **JSON compacto**.

Esquema de mensajería del curso (TypeScript):

```typescript
const contextHistory = [
  { role: "user", content: "Localiza la última factura rechazada y notifica al cliente por Telegram." },
  { role: "assistant", content: null,
    tool_calls: [{ id: "call_billing_981", type: "function",
      function: { name: "billing_query_invoices", arguments: JSON.stringify({ status: "failed", limit: 1 }) } }] },
  { role: "tool", tool_call_id: "call_billing_981", name: "billing_query_invoices",
    content: JSON.stringify({ invoice_id: "inv_2024_0891", customer_id: "cust_4412", amount: 149.00, reason: "insufficient_funds" }) }
];
```

En la iteración siguiente el modelo ve que tiene `invoice_id` y `customer_id` pero aún no el contacto de Telegram → emite una **segunda llamada consecutiva** (`crm_get_contact`) encadenando los identificadores obtenidos.

Traza del curso (billing → crm → telegram):

```python
def resolve_failed_invoice(query):
    step1 = billing_tool({"status": query, "limit": 1})
    cust_id = step1.get("customer_id"); inv_id = step1.get("invoice_id")
    step2 = crm_tool({"customer_id": cust_id})
    chat_id = step2.get("telegram_id")
    msg = f"Factura {inv_id} fallida para {chat_id}"
    step3 = telegram_tool({"chat_id": chat_id, "text": msg})
    return step3.get("delivered")
```

---

## Manejo de dependencias de datos y esquemas dinámicos

A diferencia de un script estático, el modelo encuentra esquemas imprevistos: si `billing_query_invoices` devuelve un array vacío (sin transacciones fallidas), invocar `crm_get_contact` con un ID inexistente **rompe el flujo o produce errores en cascada**.

Cada habilidad debe definir **contratos con JSON Schema estricto** para evitar argumentos con tipos incompatibles o propiedades faltantes:

```json
{
  "name": "crm_get_contact",
  "description": "Recupera la informacion de contacto del cliente dado su customer_id",
  "parameters": {
    "type": "object",
    "properties": { "customer_id": { "type": "string", "description": "Identificador unico del cliente con prefijo cust_" } },
    "required": ["customer_id"],
    "additionalProperties": false
  }
}
```

Cuando el resultado es vacío o inesperado, el bucle debe **permitir una ramificación**: buscar con criterios más amplios, **o** emitir un mensaje final informando ausencia de datos en vez de forzar la siguiente llamada.

### PITFALL del curso (correcto)
Inyectar respuestas gigantescas de herramientas anteriores (dumps SQL, archivos completos) satura la ventana y provoca que el modelo **omita parámetros obligatorios** en las llamadas siguientes. Diseñar herramientas intermedias que **filtren o resuman** antes de devolver al bucle.

### Check your understanding
**¿Cómo transfiere un agente los datos de una herramienta a la siguiente?**
- [ ] Emitir llamadas paralelas a todas las herramientas prediciendo argumentos futuros.
- [x] **Procesar el resultado devuelto en el rol `tool` e inyectar sus campos como argumentos en la siguiente `tool_call`.** ✅ (acierta)

---

## Patrones de control: límite de profundidad y cortafuegos de ejecución

Un riesgo del encadenamiento es el **bucle infinito**: el agente invoca una herramienta, obtiene un error menor, intenta corregirlo, y entra en una espiral que consume tokens y cuota.

Según el curso, OpenClaw implementa un **`max_consecutive_calls`** (típicamente 5-10 pasos): al superarlo, el runtime **suspende el bucle** y fuerza una respuesta conversacional con el estado parcial. Y **`abort_on_duplicate_calls`** detecta si el agente emite la misma llamada con argumentos idénticos dos veces seguidas (señal de ciclo ciego).

```python
agent_runner = OpenClawRunner(
    agent_id="ops_assistant",
    max_consecutive_calls=6,
    timeout_per_step=15.0,
    abort_on_duplicate_calls=True
)
```

### REMEMBER del curso (correcto)
Nunca permitas ejecuciones consecutivas **sin un límite rígido de iteraciones**. El razonamiento autónomo debe estar siempre acotado por un monitor de pasos.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo evita el runtime que dos herramientas consecutivas colisionen en el sistema de archivos?
2. ¿Qué ocurre si una herramienta en la mitad de una cadena devuelve un timeout?
3. ¿Es posible ejecutar varias herramientas en paralelo dentro de un mismo paso?
4. ¿Cómo afecta el aumento de herramientas disponibles a la precisión de las llamadas consecutivas?

(Anotadas. La #1 conecta con la concurrencia de L17; la #3 con function-calling parallel tool calls; la #4 con "tool overload".)

---

## Resumen

La ejecución consecutiva transforma a OpenClaw de asistente conversacional en un sistema capaz de resolver tareas multi-etapa: cada paso consume la salida del anterior. Controlar el **tamaño del payload** y limitar la **profundidad de recursión** garantiza estabilidad en producción.

**UP NEXT · Lección 23 de 30:** *Validación de Estados Intermedios en Bucles*. Faltan **3 lecciones** para cerrar el Módulo 5.

---

## Notas de verificación (Kanam)

**El núcleo conceptual es correcto - es el estándar de function-calling y coincide con cómo opera OpenClaw de verdad:**

| El curso dice | Realidad |
|---|---|
| El agente emite `tool_call`, suspende texto, espera el payload, y el resultado vuelve como rol `tool` con `tool_call_id` | ✅ **Es el esquema estándar de tool-calling** (OpenAI-style). OpenClaw lo usa (docs mencionan payloads tool-call `<tool_call>`/`<function_call>` y su manejo). El patrón solicitud→ejecución→feedback es real. |
| Encadenar salida→entrada con razonamiento intermedio (no tuberías rígidas) | ✅ Correcto: es la esencia del bucle agéntico. |
| **PITFALL**: volcar payloads gigantes satura la ventana y hace omitir parámetros | ✅ **Correcto y crítico.** Mapea directamente a `contextPruning` (L20) y a la compactación nativa. |
| Contratos **JSON Schema** estrictos por herramienta (`required`, `additionalProperties: false`) | ✅ **Real**: las tools de OpenClaw se definen con schemas JSON (los `tool_describe`/`tool_search` de este mismo entorno usan schemas). |
| **REMEMBER**: límite rígido de iteraciones obligatorio | ✅ **Correcto en espíritu** (ver abajo el mecanismo real). |
| Check-your-understanding: procesar el resultado en rol `tool` | ✅ Acierta. |

**Lo que NO coincide con la instalación real:**
- ❌ **`OpenClawRunner(...)`, `max_consecutive_calls` y `abort_on_duplicate_calls` no existen** como API del producto (verificado: no aparecen en docs). Son **inventados**.
- ⚠️ **El límite real es distinto:** OpenClaw acota la ejecución por **presupuesto de tiempo** (`agents.defaults.timeoutSeconds`, default 48h, `0`=ilimitado) y por **budgets de payload** (p. ej. `--script-tool-budget`, default 50, cap 200). **No** hay un `max_consecutive_calls` de pasos conversacionales con ese nombre. El "monitor de pasos" existe conceptualmente (bounding), pero no con esa superficie.
- ❌ **`tool_calls`/`tool_call_id`/rol `tool`**: válidos como **esquema estándar de function-calling**, pero el material los presenta como API de OpenClaw con `JSON.stringify`-style objects; es el formato del proveedor, no una clase `OpenClawRunner`.
- ⚠️ **La traza `resolve_failed_invoice`** es **pseudocódigo ilustrativo**: `billing_tool`, `crm_tool`, `telegram_tool` no existen. El código **no corre**.
- ⚠️ **Parallel tool calls (su pregunta #3):** es real en function-calling, pero OpenClaw docs no lo confirman como capacidad expuesta; el único "parallel" documentado es `parallel-search` (proveedor de búsqueda web), no paralelización de tools.

**Verificación ejecutable:**
- ❌ El único código mostrado depende de herramientas/runner inexistentes → **no ejecutable**.
- ✅ El **concepto** (encadenamiento por rol `tool`) es correcto y verificable contra el estándar de function-calling que OpenClaw usa.

**Patrón (vigésimo segundo caso, consistente):** **concepto correcto y estándar** (encadenamiento tool→tool con rol `tool`/`tool_call_id`, contratos JSON Schema, no volcar payloads) montado sobre una **API de runner inventada** (`OpenClawRunner`, `max_consecutive_calls`, `abort_on_duplicate_calls`). El *qué* es correcto; el *cómo* real es el presupuesto de tiempo de `agents.defaults.timeoutSeconds` + budgets de payload + el pruning/compactación, no esa clase.

**Nota de contexto (Módulo 5):** tras esta L22 el propio curso indica *"3 lessons left in Encadenamiento en Bucle Agéntico"* → Módulo 5 = 5 lecciones (L21-L25). Lección 23: *Validación de Estados Intermedios en Bucles*.
