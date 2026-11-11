# Clase: LangGraph Complete Course for Beginners — Complex AI Agents with Python

- Fuente: https://www.youtube.com/watch?v=jGg_1h0qzaM
- Canal: freeCodeCamp.org
- Expositor: Vaibhav Mehra (estudiante de robótica e IA)
- Duración: 3:09:51 (11.391 s)
- Idioma: inglés
- Transcripción: [transcripcion.md](transcripcion.md)
- Código del curso: <https://github.com/iamvaibhavmehra/LangGraph-Course-freeCodeCamp>

## Resultado esperado

Al terminar el curso:

1. **Modelar un grafo de estado** en LangGraph: `TypedDict` como esquema de estado, nodos como funciones, `START`/`END`, `add_edge` y `add_conditional_edges`.
2. **Escribir un router como función pura** que devuelva el nombre de la arista (no el estado), y saber por qué LangGraph exige `lambda state: state` como passthrough cuando se agrega un router con `add_node`.
3. **Construir un ReAct agent**: `@tool` con docstring obligatorio, `bind_tools`, `ToolNode`, y el ciclo `agent → tools → agent` cerrado con una arista dirigida de vuelta.
4. **Entender `add_messages` como reducer** y usar `Annotated[Sequence[BaseMessage], add_messages]` para que el estado se *agregue* en vez de sobrescribirse.
5. **Mantener memoria de conversación** con una lista de mensajes externa al grafo y saber sus dos límites (se pierde al cerrar el proceso; crece sin techo y encarece el prompt).
6. **Construir un RAG agent**: cargar PDF, chunking con overlap, embeddings, Chroma como vector store, retriever como tool, y un segundo nodo que ejecuta la tool call a mano.

## Mapa temporal

Capítulos oficiales de la descripción del video; el intervalo de cada módulo sale de ellos.

| Tiempo | Bloque | Qué pasa |
|---|---|---|
| 0:00:00 | Introduction | Presentación, qué se construye, nivel del curso |
| 0:01:24 | Type Annotations | `Dict`, `TypedDict`, `Union`, `Optional`, `Any`, `Callable`, `Lambda` |
| 0:08:35 | Elements | Grafo, nodos, edges, conditional edges, START/END, tools, tool node, `StateGraph`, Runnable, tipos de mensaje |
| 0:18:39 | Agent 1 | Grafo mínimo: un nodo |
| 0:32:22 | Agent 1 Exercise | Primer ejercicio |
| 0:33:07 | Agent 2 | Estado con múltiples claves |
| 0:43:27 | Agent 2 Exercise | Ejercicio con `if` dentro del nodo |
| 0:44:29 | Agent 3 | Grafo secuencial: dos nodos y una edge; el error lógico del `state.final` |
| 0:54:04 | Agent 3 Exercise | Ejercicio de dos nodos |
| 0:55:36 | Agent 4 | Router + `add_conditional_edges` + `path_map` |
| 1:13:09 | Agent 4 Exercise | Cuatro números, dos operaciones |
| 1:14:14 | Agent 5 | Loops: contador en el estado y arista condicional que vuelve |
| 1:29:19 | Agent 5 Exercise | Higher-or-lower automático, 7 intentos |
| 1:31:01 | AI Agent 1 | Primer LLM en el grafo: stateless |
| 1:42:54 | AI Agent 2 | Memoria: `Union[HumanMessage, AIMessage]`, historial, log a archivo |
| 2:03:20 | AI Agent 3 P1 | Prerrequisitos: `Annotated`, `Sequence`, `BaseMessage`, `ToolMessage`, reducer |
| 2:12:28 | AI Agent 3 P2 | ReAct agent completo |
| 2:28:46 | AI Agent 4 | Proyecto «Drafter»: colaboración humano-IA con save tool |
| 2:52:09 | RAG Agent | PDF → chunks → Chroma → retriever tool → grafo de dos agentes |
| 3:06:15 | RAG Agent Testing | Verificación contra el PDF y caso de no-hallazgo |
| 3:09:04 | Course Outro | Cierre |

## Módulos

### Módulo 1 — Anotaciones de tipo (0:01:24 – 0:08:35)

- **Objetivo:** leer el código de LangGraph sin que sorprendan `TypedDict`, `Annotated` ni `Optional`.
- **Contenidos:**
  - `Dict` describe la forma de un diccionario; `TypedDict` la fija como tipo, y así es como LangGraph declara el estado.
  - `Union` permite varias alternativas en una clave (lo usa después para `HumanMessage | AIMessage`).
  - `Optional[X]` es equivalente a `Union[X, None]`; el aviso del ponente es que una clave no pasada en el `invoke` queda en `None` y usarla para *calcular* otra clave revienta.
  - Cita: «it can provide hints to uh help catch incorrect usage» (0:05:30) — las anotaciones son hints para el editor y la librería, **no validación en runtime**: Python no frena un dato mal tipado.
- **Ejercicio:** reescribir un `TypedDict` de 4 claves con `Optional` explícito y comprobar qué pasa al invocar un grafo sin esa clave.

### Módulo 2 — Elementos de LangGraph (0:08:35 – 0:18:39)

- **Objetivo:** distinguir nodo, edge, tool, tool node y Runnable, que es donde se confunde todo.
- **Contenidos:**
  - Grafo = «the overarching structure and it maps out how different tasks aka nodes are connected and executed».
  - Nodo vs tool: el nodo es parte de la estructura del grafo; la tool es una funcionalidad *dentro* de un nodo («a hammer for the nails, a screwdriver for the screws»).
  - Tool node: nodo especial cuyo único trabajo es correr una tool y devolver el resultado al estado.
  - Edge vs conditional edge: la primera es dirección fija; la segunda elige el próximo nodo «based on the specific condition or logic applied to the current state» — es un `if/else`.
  - **START/END no ejecutan nada**: START marca dónde arranca, END que el proceso terminó.
  - `StateGraph` administra nodos, edges y estado; el Runnable es el bloque Lego que se puede combinar.
  - Cinco tipos de mensaje: `HumanMessage`, `AIMessage`, `SystemMessage`, `ToolMessage`, `FunctionMessage`.
- **Ejercicio:** dibujar (papel o diagrama) el grafo de un bot de soporte y marcar cuál flecha es condicional; entregar el diagrama con la lista de nodos y el estado.

### Módulo 3 — Grafo mínimo (0:18:39 – 0:32:22)

- **Objetivo:** el ciclo completo: esquema → nodo → grafo → compile → invoke.
- **Contenidos:**
  - Estado como `class AgentState(TypedDict)` con una clave (`message: str`).
  - Un nodo es una función normal que recibe el estado y devuelve el estado actualizado; **sin `return state` el grafo no avanza**.
  - `StateGraph(AgentState)` → `add_node("greeter", greeting_node)` → `set_entry_point` / `set_finish_point` → `graph.compile()`.
  - **`invoke` es sobre el grafo compilado**, no sobre `StateGraph`: el error que muestra el ponente es «state graph object has no attribute», por invocar el grafo sin compilar.
  - Docstring como hábito: en este módulo no lo usa la IA, pero en el ReAct agent es lo que le explica la tool al modelo. Cita: «dock strings is what will tell your AI agents when we actually build the AI agents your LLMs what that function actually does» (0:24:41).
- **Ejercicio:** el grafo «hello world» con un nodo que salude por nombre; entregar el código y la salida de `invoke`.

### Módulo 4 — Estado con múltiples claves (0:33:07 – 0:44:29)

- **Objetivo:** estado heterogéneo y claves que no se pasan.
- **Contenidos:**
  - Claves de distinto tipo conviven: `list[int]` de valores, `str` de nombre, `str` de resultado.
  - Cita: «Langraph automatically sets that as like a a none value in this case if you don't pass an input» — **una clave no pasada en el `invoke` queda en `None`**.
  - El corolario del ponente es el bug clásico: si esa clave `None` se usa para *calcular* otra, falla; si solo se le asigna, funciona.
  - Acceso al resultado: `answers` (todo el estado) vs `answers["result"]` (una clave).
- **Ejercicio (oficial):** un solo nodo que reciba lista de enteros, nombre y operación (`+` / `*`), y devuelva «Hi jack sparrow your answer is 24». Pista del ponente: hace falta un `if` dentro del nodo, sin agregar otro nodo.

### Módulo 5 — Grafo secuencial y el error lógico del `state.final` (0:44:29 – 0:55:36)

- **Objetivo:** varios nodos encadenados y cómo se pisa (o no) el estado.
- **Contenidos:**
  - `add_edge("first_node", "second_node")` es lo único nuevo frente al grafo de un nodo.
  - El ponente introduce **un error lógico a propósito**: el segundo nodo asigna `state["final"] = ...` y borra lo que escribió el primero. Cita: «we've completely replaced all of the content we had before».
  - La corrección es concatenar (`state["final"] = state["final"] + ...`), no asignar.
  - **Regla que sale del módulo:** un nodo puede leer/escribir cualquier clave del estado, cuantas veces quiera; el orden lo fija el grafo, no la función.
- **Ejercicio:** construir el grafo de dos nodos, reproducir el bug, y arreglarlo sin cambiar la estructura del grafo (solo el nodo).

### Módulo 6 — Router y aristas condicionales (0:55:36 – 1:14:14)

- **Objetivo:** el concepto más difícil del curso: cómo el router elige el próximo nodo.
- **Contenidos:**
  - Importar `START` y `END` de `langgraph.graph` en vez de `set_entry_point`/`set_finish_point`; ambas formas son válidas.
  - **El router devuelve el nombre de la arista, no el estado.** Cita: «we are returning this updated state in this one and this one. But in this node, we're not. We're just returning the edge».
  - Como `add_node` exige una función que devuelva estado, se envuelve con `lambda state: state` — un passthrough, porque el router no modifica nada, solo compara.
  - `add_conditional_edges(source, path, path_map)`: `source` = nodo de salida, `path` = la función router, `path_map` = diccionario `{nombre_de_arista: nodo_destino}`.
  - START se conecta **al router**, nunca directo a los nodos de operación, porque entonces el router no decide nada.
  - Los nodos de operación vuelven a `END` con dos edges dirigidas.
- **Ejercicio (oficial):** cuatro números y dos operaciones → dos resultados. El ponente lo describe como replicar el mismo código una vez más, y lo señala como el ejercicio más difícil hasta ese punto.

### Módulo 7 — Loops (1:14:14 – 1:31:01)

- **Objetivo:** iterar dentro del grafo sin un nodo router extra.
- **Contenidos:**
  - La arista condicional sale del propio nodo que itera (`random_node`) y tiene dos destinos: el mismo nodo (loop) o `END` (exit).
  - El estado necesita un contador (`counter: int`) y una lista acumuladora.
  - **Robustez:** el nodo de saludo fuerza `state["counter"] = 0`, así el valor que mande el humano no cambia la cantidad de iteraciones. Cita del caso: pasar `-2` generaría siete números en vez de cinco.
  - Consejo de práctica: `print` o breakpoints en cada nodo; el ponente los usa para mostrar el recorrido.
  - Criterio de diseño: el ponente recomienda **dibujar el grafo antes de codearlo**, igual que un diseñador de UI entrega el diseño al desarrollador.
- **Ejercicio (oficial):** higher-or-lower automático, número entre 1 y 20, máximo 7 intentos, sin intervención humana. El nodo de pista dice «higher»/«lower» y el grafo ajusta los límites inferior/superior. Inputs: nombre, lista vacía de intentos, `attempts=0`, `lower=1`, `upper=20`.

### Módulo 8 — Primer LLM en el grafo (stateless) (1:31:01 – 1:42:54)

- **Objetivo:** meter un modelo en un nodo y entender qué *no* hace.
- **Contenidos:**
  - Estado con `messages: list[HumanMessage]` — el tipo importa porque le dice al modelo quién habla.
  - `ChatOpenAI(model="gpt-4o")` con API key en `.env`; LangGraph se apoya en langchain para esto: «langraph is built on top of lang chain».
  - El nodo llama `llm.invoke(state["messages"])` y **no** guarda la respuesta en el estado.
  - **No hay memoria:** cita el fallo demostrado en vivo — el usuario dice «Hi, I am Bob», después pregunta «what is my name?» y el modelo responde «I don't have the ability to know your name». El ponente lo dice sin rodeos: «Nowhere in the code have we actually created some sort of memory».
  - Costo: el ponente afirma que gpt-4o es «extremely cheap» (1:37:11) y de precio «tens of pennies for like a,000 tokens» (1:37:24) — **es un claim sin fuente y del momento en que se grabó**; ver notas editoriales.
- **Ejercicio:** correr el bot, preguntarle el nombre después de decirlo, y explicar en una línea por qué no lo sabe.

### Módulo 9 — Memoria de conversación (1:42:54 – 2:03:20)

- **Objetivo:** historial de mensajes como memoria, y sus dos límites.
- **Contenidos:**
  - `messages: Annotated[list, add_messages]`… en este módulo todavía no: usa `Union[HumanMessage, AIMessage]` y **appendea a mano** (`state["messages"].append(AIMessage(content=response.content))`).
  - El historial vive **fuera** del grafo (`conversation_history`), y se le pasa entero en cada `invoke`: cita «the entire conversation history is sent, not just the current human message».
  - `response.content` extrae solo el texto, sin tokens ni metadata.
  - Se demuestra que el mensaje del humano se guarda **sin alterar**: escribe a propósito «good morning» mal escrito y el log lo conserva igual.
  - **Límite 1 — se pierde al cerrar el proceso.** El ponente lo muestra: reinicia y el bot ya no sabe quién es el usuario. Solución de prototipo: volcar a `logging.txt` (o `login.txt` según el ASR). Para producción: base de datos.
  - **Límite 2 — el historial crece sin techo.** Cada mensaje se reenvía, y los tokens de entrada son el costo. Cita: «if the number of human messages exceeds five or something like that, then you remove the first human message». El `5` es arbitrario, y se descarta la más vieja porque la última es la más relevante.
- **Ejercicio:** agregar el recorte a 5 mensajes y comprobar con `print(len(state["messages"]))` que la longitud se estabiliza.

### Módulo 10 — Prerrequisitos del ReAct agent (2:03:20 – 2:12:28)

- **Objetivo:** `Annotated`, `Sequence`, `BaseMessage` y el reducer antes de escribir el agente.
- **Contenidos:**
  - `Annotated[tipo, "texto"]` agrega metadata sin cambiar el tipo: el ejemplo es `email: Annotated[str, "must be a valid email format"]`, y el texto aparece al imprimir `email.__metadata__`. Cita: «annotated is a type annotation which provides additional context to your uh variable or your key without actually affecting the type itself» (2:05:41).
  - `Sequence[BaseMessage]` es el tipo de la lista de mensajes.
  - `BaseMessage` es la clase padre (`HumanMessage`, `AIMessage`, `ToolMessage`, `SystemMessage` heredan).
  - **`add_messages` es un reducer:** sin reducer, cada update *reemplaza* el valor; con `add_messages`, se agrega. Cita: «a reducer function is essentially just a rule that controls how updates from nodes are combined with the existing state».
  - `ToolMessage` lleva el resultado de la tool de vuelta al modelo, con `tool_call_id`.
- **Ejercicio:** explicar en un párrafo, con el ejemplo del email, por qué `Annotated` no valida nada por sí solo.

### Módulo 11 — ReAct agent (2:12:28 – 2:28:46)

- **Objetivo:** el patrón que aparece en casi todo agente real.
- **Contenidos:**
  - `@tool` sobre una función normal; **el docstring es obligatorio**: si falta, el error es «the function must have a dock string if description is not provided». El docstring es lo que le dice al modelo para qué sirve la tool.
  - `llm.bind_tools(tools)` le da acceso al modelo; los parámetros de la tool los rellena el LLM, no el humano.
  - Nodo agente: `SystemMessage` + `state["messages"]` (incluida la `HumanMessage` del usuario, que el ponente señala que había olvidado) → `llm.invoke(...)` → `return {"messages": response}`; el reducer se encarga del append.
  - `should_continue(state)` mira el **último mensaje**: si tiene `tool_calls`, devuelve `"continue"`; si no, `"end"`.
  - `ToolNode(tools)` es el nodo que ejecuta.
  - `add_conditional_edges("agent", should_continue, {"continue": "tools", "end": END})` + `add_edge("tools", "agent")` → **el ciclo**.
  - Demostraciones: `add 3+4` usa la tool; `add 34 + 21` y `add 3 + 4` en la misma consulta llama dos veces; «add 40 + 12 and then multiply the result by 6» encadena dos tools; «also tell me a joke» responde sin tool. Ese último caso es la prueba de robustez del patrón.
- **Ejercicio:** agregar `subtract` y `multiply`, y verificar con una consulta que encadene dos tools y otra que no necesite ninguna.

### Módulo 12 — Proyecto «Drafter»: colaboración humano-IA (2:28:46 – 2:52:09)

- **Objetivo:** salir del ReAct puro cuando el ciclo no sirve: la save tool debe terminar el grafo.
- **Contenidos:**
  - Planteo: una empresa pierde tiempo redactando documentos; el sistema debe aceptar feedback continuo y guardar el borrador.
  - **Por qué no es un ReAct agent:** en ReAct la tool siempre vuelve al agente; acá, cuando se usa `save`, se termina. El conditional edge sale de `tools`, no del agente.
  - Estado global (`document_content`) para pasar datos a las tools: cita «the correct way to do it in langraph is through something called injected state now injected state is beyond the scope of this uh course so the workound on that is to use a global variable». **Es un workaround, y el ponente lo declara.**
  - Dos tools: `update` (contenido) y `save` (nombre de archivo que decide el modelo; si no termina en `.txt`, se lo agrega).
  - `should_continue` mira la última `ToolMessage`: si usó `save`, `END`; si usó `update`, vuelve al agente.
  - Robustez: si `state["messages"]` está vacío, el agente saluda y pide el documento — no asume que ya hay uno.
  - Demo: email a Tom, feedback iterativo, guardado en un archivo `unable to attend meeting email.txt`; el nombre lo generó el agente sin que el humano se lo dictara.
- **Ejercicio:** extender el Drafter con una tool que *liste* los borradores guardados; entregar el grafo actualizado y una corrida.

> **Nota de correctitud:** el ponente llama human-AI collaboration a esto, pero el humano no decide cuándo el agente para: lo hace el modelo al elegir `save`. La colaboración real (interrumpir, aprobar, editar) es `interrupt()` de LangGraph, que el curso no cubre. Ver notas editoriales.

### Módulo 13 — RAG agent (2:52:09 – 3:09:04)

- **Objetivo:** recuperación sobre un documento propio, con el retriever como tool.
- **Contenidos:**
  - `temperature=0` para respuestas deterministas; cita: «temperature equal to zero makes the model output more deterministic».
  - **Embedding model y LLM tienen que ser compatibles** — el argumento del ponente es la dimensión del vector. Es correcto en el fondo, pero la regla real es otra: el embedding se elige por la dimensión y por el dominio, y no tiene por qué ser del mismo proveedor que el LLM. Ver notas editoriales.
  - `PyPDFLoader` → 9 páginas; `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)`.
  - `chunk_overlap` existe para que una frase cortada entre chunks no desaparezca del contexto de ambos.
  - Chroma como vector store persistido en disco, colección `stock_market`; `retriever` con `search_type="similarity"` y `k=5` (el default es 4).
  - Tool retriever: si encuentra, devuelve los chunks; si no, «I found no relevance information in the document». Ese fallback es lo que evita que el modelo invente.
  - System prompt pide **citar** las partes del documento: cita «Please always site the specific parts of the document you use in your answers. This is really just to make sure it's not hallucinating».
  - El grafo es de dos agentes: nodo LLM y nodo retriever, unidos por el conditional edge `should_continue` (si hay tool calls, al retriever; si no, END).
  - Prueba: pregunta por el S&P 500 en 2024 y verifica el 25%/23% contra el PDF; pregunta por OpenAI (que no cotiza) y el sistema dice que no está en el documento.
- **Ejercicio:** cambiar el PDF por uno propio de 3–5 páginas, y hacer dos preguntas: una respondible, una que no esté. Entregar ambas respuestas y comprobar que la segunda no inventa.

### Módulo 14 — Cierre (3:09:04 – 3:09:51)

- El ponente declara el curso como punto de partida, no de llegada: «although this course is finishing here, your journey in Langraph is just beginning».

## Ejercicios por bloque

- [ ] Módulo 1 — `TypedDict` con `Optional` explícito + caso de clave faltante.
- [ ] Módulo 2 — diagrama de un bot de soporte con la flecha condicional marcada.
- [ ] Módulo 3 — grafo «hello world» con salida de `invoke`.
- [ ] Módulo 4 — ejercicio oficial: lista + nombre + operación, salida «Hi jack sparrow your answer is 24».
- [ ] Módulo 5 — reproducir el bug de `state.final` y corregirlo dentro del nodo.
- [ ] Módulo 6 — ejercicio oficial: cuatro números, dos operaciones, dos resultados.
- [ ] Módulo 7 — higher-or-lower automático con 7 intentos y sin humano.
- [ ] Módulo 8 — demostrar con una corrida que el bot stateless no recuerda el nombre.
- [ ] Módulo 9 — recorte de historial a 5 y `len(state["messages"])` estable.
- [ ] Módulo 10 — párrafo explicando por qué `Annotated` no valida.
- [ ] Módulo 11 — `subtract` + `multiply`, una consulta encadenada y una sin tools.
- [ ] Módulo 12 — tool que liste borradores guardados.
- [ ] Módulo 13 — PDF propio, pregunta respondible y pregunta fuera del documento.

## Banco de preguntas para estudiar con el usuario

1. ¿Por qué un router devuelve una **arista** y no un estado? ¿Qué tiene que hacer un nodo router entonces, y por qué el ponente usa `lambda state: state`?
2. ¿En qué se diferencia `add_messages` de un `append` manual? ¿Qué bug desaparece al usarlo, y qué bug *nuevo* aparece?
3. El módulo 5 muestra un nodo que sobrescribe `state["final"]`. En un grafo sin reducer, ¿qué habría pasado con `message` en el primer grafo, y por qué ahí no molestaba?
4. ¿Por qué el Módulo 8 (bot stateless) y el Módulo 9 (chatbot con memoria) tienen el **mismo grafo** y distinto comportamiento?
5. El historial de conversación crece y se reenvía entero. ¿Cuáles son los dos problemas del Módulo 9, y el curso resuelve alguno de forma definitiva?
6. ¿Por qué el Drafter no es un ReAct agent? ¿Qué cambia en el grafo, y qué pierde al no usar `interrupt()`?
7. En el RAG agent, ¿qué dos cosas evitan que el modelo invente: una mecánica de recuperación y una instrucción de prompt?
8. ¿Qué es lo que realmente hace que `k=5` importe, y por qué el curso no discute el trade-off (chunks de más = más contexto, más costo y más ruido)?

## Notas editoriales

- **El curso está grabado con modelos de 2025 y el precio que cita ya no aplica.** El ponente dice que gpt-4o es «extremely cheap» y que el precio es «tens of pennies for like a,000 tokens» (1:37:24). En la fecha del curso (mayo 2025) era una afirmación razonable; hoy el modelo ya no es el barato por defecto. La cifra se toma como dato de época, no como presupuesto.
- **La regla del ponente de que el embedding tiene que ser compatible con el LLM es una simplificación.** El ponente lo justifica por dimensión del vector. La restricción real es que el embedding sea compatible con **la dimensionalidad del índice** que se creó, no con el LLM: se puede recuperar con un embedding y generar con otro, y de hecho es lo normal. La frase correcta sería que el embedding tiene que ser el mismo con el que se construyó el índice.
- **La human-AI collaboration del Drafter es colaboración por turnos, no control humano.** El grafo no se interrumpe esperando aprobación: el modelo decide llamar a `save`. `interrupt()` y `Command(resume=...)` de LangGraph existen justamente para eso y quedan fuera del alcance declarado.
- **Workaround declarado:** el uso de una variable global en vez de `InjectedState` está explícitamente presentado como atajo de curso principiante. No copiarlo en código real: `InjectedState` es la vía correcta.
- **No cubre:** checkpointer/persistencia (`MemorySaver`), `interrupt()`, streaming token a token, subgrafos, `Send`/map-reduce, observabilidad (LangSmith), ni deploy. El curso es de fundamentos y lo dice.
- **El patrón de los Módulos 3–7 es la base de todo lo demás.** Quien saltee los grafos sin LLM para ir directo al ReAct agent va a copiar código sin entender por qué el router devuelve un string y no el estado.
- Código de referencia del curso: <https://github.com/iamvaibhavmehra/LangGraph-Course-freeCodeCamp>. No se verificó el contenido del repo en esta sesión; el outline se armó contra el transcript.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
