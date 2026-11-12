# Clase: AI Agents For Beginners – OpenClaw Case Study

- Fuente: https://www.youtube.com/watch?v=AZDSpS5v57w
- Canal: freeCodeCamp.org (curso creado por @KodeKloud)
- Expositor: Mumshad Mannambeth (fundador de KodeKloud)
- Duración: 3:05:58 (11.158 s)
- Publicado: 2026-07-07
- Idioma: inglés (subtítulos automáticos, glosario de ASR en `transcripcion.md`)
- Capítulos: los 22 oficiales de la descripción del video, alineados 1:1 con los módulos

## Resultado esperado

Al terminar la clase deberías poder:

1. Explicar qué es un LLM y de dónde sale la alucinación, en términos de predicción del próximo token.
2. Estimar el costo y el presupuesto de contexto de una llamada, y elegir temperatura según la tarea.
3. Diseñar un schema de tools e implementar el loop de function calling (el modelo pide, tu código ejecuta).
4. Decidir workflow vs. agente con el checklist de cuatro preguntas, sin sobre-ingeniería.
5. Implementar el ciclo percibir-razonar-actuar con memoria, guardrails y manejo de errores.
6. Probar, monitorear y asegurar un agente: unit + mock + eval, logs y métricas, sandbox y mínimo privilegio.
7. Leer la arquitectura de OpenClaw: canal → gateway → agent loop → tools/memoria → respuesta.

## Mapa temporal

| Tiempo | Bloque |
|---|---|
| 00:00 - 07:54 | Bienvenida: qué es Chat GPT, transformer, pre-trained, generativo y límites del LLM |
| 07:54 - 15:23 | Evolución de GPT, competidores, qué hace "large" a un LLM y bling spots |
| 15:23 - 17:54 | Cómo usa un developer un LLM: la API como request/response |
| 17:54 - 31:13 | Tokens, tokenización, costo, ventana de contexto y qué pasa cuando se llena |
| 31:13 - 38:29 | Roles del mensaje, prompting por patrones, few-shot, persona y chain of thought |
| 38:29 - 45:01 | Primer programa de 7 líneas, SDK vs. HTTP crudo y lab de la primera llamada |
| 45:01 - 51:08 | Tareas determinísticas vs. no determinísticas y el costo de usar un LLM de más |
| 51:08 - 58:20 | Tools: nombre, descripción, parámetros; tool loop y function calling |
| 58:20 - 01:08:16 | Workflows con caminos predefinidos vs. agentes autónomos; cuándo usar cada uno |
| 01:08:16 - 01:13:15 | Definición de agente y el ciclo percibir-razonar-actuar (Zippy) |
| 01:13:15 - 01:21:13 | Lab del while loop y los cinco componentes de todo agente |
| 01:21:13 - 01:26:19 | Planeamiento, ReAct y los cuatro modos de falla con sus guardrails |
| 01:26:19 - 01:33:56 | Memoria: sliding window, truncation, summarization y memoria persistente |
| 01:33:56 - 01:43:08 | Multi-agente: orquestador + especialistas, pipeline, debate y handoffs |
| 01:43:08 - 01:52:20 | Cody, los seis modos de falla y los cinco principios de error handling |
| 01:52:20 - 02:00:25 | Vocabulario de Google (grounding) y frameworks: LangChain, Mastra y por qué OpenClaw no usa ninguno |
| 02:00:25 - 02:09:25 | Labs: safe agent, SDK desde cero y el asistente personal completo |
| 02:09:25 - 02:14:39 | Tour del codebase de OpenClaw: las seis áreas de `src/` |
| 02:14:39 - 02:30:44 | Arquitectura OpenClaw: cuatro paquetes PI, cinco fases del loop, locks y memoria persistente |
| 02:30:44 - 02:39:30 | Testing de agentes no determinísticos: unit, mocks, evals y e2e |
| 02:39:30 - 02:51:55 | Observabilidad, seis métricas y las cinco palancas de optimización |
| 02:51:55 - 03:05:58 | Seguridad de agentes y las técnicas de prompt engineering que usa OpenClaw |

## Módulos

### Módulo 1 - Course Welcome & Architecture Fundamentals (00:00 - 07:54)

**Objetivo:** entender qué es un LLM por dentro (transformer, pre-trained, generativo) y por qué eso explica sus límites.

- El curso se presenta como remedio a la sensación de que "AI is overwhelming" (00:00:38). Promete cuatro agentes construidos desde cero: Zippy, Savvy, Meshy y Cody (00:01:17).
- El arco del curso: "Zippy's journey from being a solo generic agent to becoming an orchestrator" (00:01:36).
- Chat GPT son dos cosas: la interfaz de chat y el modelo GPT. "GPT is the brain and chat is the interface" (00:03:49).
- El transformer nace en 2017 con el paper *Attention Is All You Need*: "A transformer is a specific design for how an AI system processes language." (00:04:36). La superpotencia es la atención: mirar todas las palabras a la vez y relacionarlas (00:05:35).
- Pre-trained significa que el modelo aprendió patrones de miles de millones de textos antes de hablar con un usuario. No aprende hechos: aprende regularidades de secuencia (00:06:31).
- La alucinación es consecuencia directa del mecanismo: "GPT isn't looking up facts. It's generating text that sounds like it should be correct based on patterns" (00:07:50).
- El bloque cierra con la alucinación como propiedad del mecanismo, no como un bug que se arregla con un prompt: si el modelo solo predice la continuación más plausible, la verificación de hechos tiene que venir de afuera (00:07:50).

**Ejercicio:** escribir en 10 líneas qué es un LLM para alguien que nunca usó uno, explicando por qué puede inventar datos con seguridad. Entregable: `m1-llm-en-10-lineas.md`.

### Módulo 2 - Hallucinations, Model Evolution, & Competitors (07:54 - 15:23)

**Objetivo:** ubicar la evolución de los modelos y distinguir capacidad de escala de capacidad real.

- Línea de tiempo: "GPT1 came out in 2018 and proved that the concept works." (00:08:27), y sigue GPT-2 (2019), GPT-3 (2020), GPT-3.5 (2022), GPT-4 (2023), GPT-4o (2024).
- No hay un solo proveedor: "Claude from Anthropic, Gemini from Google, and Llama from Meta, which is open source" (00:09:07). Comparten la misma arquitectura transformer y el mismo mecanismo de generación.
- "Large" mide dos cosas: datos y parámetros. Para dimensionar: "all of English Wikipedia, every article ever written is about 4 billion words" (00:10:27). El video dice que GPT-3 se entrenó con ~125 veces eso; el paper de GPT-3 reporta ~300B tokens, que contra ~4B palabras de Wikipedia da un orden de 50-75x, no 125x. **El número del video es ilustrativo, no exacto** (arXiv:2005.14165).
- Los parámetros son los diales internos que el entrenamiento ajusta: "Parameters are internal settings the model tunes during training" (00:10:46). La analogía del básquet: nadie calcula el ángulo; se ajusta errando.
- Más grande no siempre es mejor: "bigger isn't always better" (00:13:22): más parámetros implica más cómputo, más costo y más latencia.
- Fortalezas: texto fluido, resumen, traducción, código, instrucciones en lenguaje natural. Puntos ciegos: matemática, conocimiento posterior al corte, y confabulación.
- Límite central del curso: "On their own, LLMs can only produce text." (00:14:40). Un agente es un LLM con tools y un loop.

**Ejercicio:** armar una tabla de tres modelos actuales (proveedor, contexto, precio de input/output, fecha de corte) con fuente oficial y fecha de consulta. Entregable: `m2-modelos.md`.

**Nota de práctica (2026-11-12):** el primer barrido de Vane quedó en `m2-informe-modelos-2026-11-12.md`, con la auditoría incluida. La auditoría encontró que la mayoría de los modelos elegidos están deprecados (GPT-5.1, Claude Sonnet 4.5, Gemini 2.5 Pro, Mistral Large 2407) y que el "tool calling no publicado" de GPT-5.1 es un falso negativo: la ficha oficial lista `function_calling`. Falta la segunda pasada con modelos vigentes y URLs oficiales.

### Módulo 3 - Developer Fundamentals & Working with APIs (15:23 - 17:54)

**Objetivo:** pasar del chat a la API: el LLM como servicio request/response.

- En el chat escribís en una caja; como developer, tu programa habla con el proveedor a través de una API. El chat es una interfaz; la API es un contrato entre programas.
- El patrón es siempre el mismo: tu aplicación manda un pedido, el proveedor procesa y devuelve una respuesta. "It's a simple back and forth request in request out." (00:15:38).
- Sobre ese contrato se construye el agente: manda mensajes, recibe respuestas y decide el siguiente paso (00:15:58).
- El resto del bloque repite la explicación de parámetros del módulo anterior (duplicado de edición, ver notas).

**Ejercicio:** dibujar el diagrama app → API → modelo → respuesta y marcar dónde vive cada decisión del agente. Entregable: `m3-api-diagrama.md`.

### Módulo 4 - Token Economics & Managing Context Windows (17:54 - 31:13)

**Objetivo:** manejar tokens como presupuesto: costo, latencia y ventana de contexto.

- "A token is a chunk of text." (00:17:54): puede ser una palabra, un pedazo o un carácter. La tokenización explica por qué "tokenization" se parte en `token` + `isization` (00:18:34).
- Regla práctica: "one token is roughly four characters of English text" (00:20:31); una redacción de 1.000 palabras son ~1.300-1.500 tokens.
- Costo: los proveedores cobran por token de entrada y de salida. Ejemplo del video: "GBD40 charges around $2.50 per million input tokens, and $10 per million output tokens" (00:21:11). **Precio mutable: verificar antes de usarlo en una estimación.**
- La salida es más cara porque se genera secuencialmente: "input tokens are processed all at once in parallel, while output tokens are generated one at a time" (00:21:31).
- La ventana de contexto es memoria de trabajo, no memoria larga: "The context window is the LLM's working memory." (00:26:13). "Long-term memory, by contrast, is like a notebook you can refer back to anytime." (00:29:04).
- Cuando se llena: truncation (se tira lo viejo), summarization (se resume lo viejo) o sliding window (ventana fija que avanza). El curso las presenta como las tres salidas comunes (00:27:48).
- Un turno de agente consume mucho más que un chat: system prompt + definiciones de tools + historial + resultados + razonamiento. El ejemplo del video llega a "around 23,000 tokens for just one turn" (00:30:01).
- La tensión de fondo: "More context means better results, but higher cost." (00:31:01). Gestionarla es una skill de producción.

**Ejercicio:** calcular el costo de un agente de 5 iteraciones con 20k tokens de contexto por llamada usando el precio oficial vigente de un proveedor. Entregable: `m4-costo.md` con la cuenta y la fuente del precio.

### Módulo 5 - API Message Roles & Prompt Engineering Nuances (31:13 - 38:29)

**Objetivo:** entender el prompt como activación de patrones, no como una orden a un humano.

- Tesis del bloque: "Prompting isn't just writing instructions. It's shaping which patterns in the model get activated." (00:32:10). "Don't use bullet points" activa el patrón que intenta suprimir; "Write in paragraphs only" funciona mejor.
- Los mensajes de la API tienen rol: system (reglas del developer), user (pedido), assistant (respuesta del modelo). "Every message has a role attached to it." (00:32:10). "The system role is for the developer." (00:32:29).
- Más contexto y más restricciones producen mejor salida: de "help me with my schedule" a un resumen con conflictos y sugerencia de qué reunión mover (00:33:27).
- Few-shot: "You can show the model exactly what you want by including an example in the prompt." (00:34:06). El ejemplo enseña formato y tipo de entrada a la vez.
- Persona: "When you assign a role, you're activating a cluster of patterns from training" (00:35:42). No es solo tono; cambia vocabulario y prioridades.
- Chain of thought: pedir los pasos hace que cada salida condicione la siguiente: "This is called chain of thought prompting" (00:36:40).
- Cierre: el system prompt de un agente de producción no es un párrafo, es un programa: OpenClaw lo arma en "a 19 section programmatically built file" (00:38:17).

**Ejercicio:** reescribir cinco instrucciones negativas como positivas y medir la diferencia con 10 corridas a temperatura 0. Entregable: `m5-prompts.md` con antes/después y resultado.

### Módulo 6 - Hands-On Lab: Practice Labs & First API Call (38:29 - 45:01)

**Objetivo:** hacer la primera llamada real desde Python y ver la teoría en el código.

- El programa mínimo son siete líneas: importar el SDK, crear el cliente, llamar a completions, imprimir `choices[0].message.content` (00:38:29).
- SDK vs. HTTP crudo: el SDK evita el boilerplate de headers, JSON y errores. "The SDK handles the HTTP the headers the JSON encoding and error handling for you." (00:40:04).
- Cada concepto tiene una línea: tokens = todo lo que va en `messages`; temperatura = parámetro; contexto = límite de `messages`; prompt = `content`.
- "Add temperature equals zero to the API call and you get the same answer every time you run it." (00:41:02).
- Labs: "The lab environment already has the required API keys baked in" (00:42:01), con créditos y claves de varios proveedores.
- En el lab se corre `hello_llm.py`; con temperatura 0 la historia del robot sale idéntica, con temperatura 1 cambia en cada corrida: "Same prompt. Completely different output." (00:44:15).

**Ejercicio:** correr el programa dos veces con temperatura 0 y dos con temperatura 1, y anotar qué cambió y qué no. Entregable: `m6-temperatura.md`.

### Módulo 7 - Multi-Turn History, API Costs, & Trade-offs (45:01 - 51:08)

**Objetivo:** decidir cuándo NO usar un LLM y cómo mantener una conversación sin memoria real.

- Regla de oro: "If the answer is always the same for the same input, use code." (00:46:08). Si requiere juicio o comprensión de lenguaje, usá el LLM.
- "An API call takes hundreds of milliseconds." (00:47:04): es más lento (milisegundos vs. microsegundos), cuesta tokens y puede equivocarse en cuentas.
- El patrón de la calculadora de recibos: la matemática es código; la frase de agradecimiento creativa es LLM. "Let the LLM think. Let code execute." (00:48:01).
- La API es stateless: "The only memory it has is what you put in the messages list." (00:50:14). La memoria de la conversación es el array de mensajes que reenviás: "The only memory it has is what you put in the messages list." (00:50:14).
- Los tres roles en acción: system fija comportamiento, user aporta input, assistant conserva el historial. Sin el turno del assistant, "that city" no tiene referente.

**Ejercicio:** implementar un traductor de fechas y un resumen de reseñas en el mismo script, usando código para lo determinístico y LLM solo para el juicio. Entregable: `m7-cuando-usar-llm.py`.

### Módulo 8 - Architecture Overview: Tool Schemas & Execution Loops (51:08 - 58:20)

**Objetivo:** entender las tools como el puente entre el texto y el mundo, y el loop que las ejecuta.

- "A tool is a function that the LLM can call to interact with the outside world." (00:52:08). Sin tools, el modelo solo responde con lo que aprendió en entrenamiento.
- "A tool has three parts. Name, what the tool is called, description, what the tool does" (00:53:05) y parameters (qué inputs necesita).
- Tipos comunes: búsqueda, cálculo, llamadas a API, operaciones de archivos y ejecución de código (00:53:44).
- Frontera de seguridad: el modelo no ejecuta nada. "The LLM never runs the tools itself." (00:54:23). "This is an important safety boundary." (00:54:23).
- El loop de tool use: el modelo emite un tool call; tu código lo ejecuta; el resultado vuelve como mensaje de tool; el modelo decide el siguiente paso. "This pattern is often called function calling." (00:55:07).
- Lab `tool_app.py`: el modelo pide `check_cal`, el código ejecuta el mock y el modelo convierte los datos en respuesta. "The model chose the right tool. Your code executed it." (00:58:02).

**Ejercicio:** definir el schema de una tool `search_flights(origin, destination, date, max_price)` y escribir el handler + dispatcher. Entregable: `m8-tool-schema.py`.

### Módulo 9 - Predefined AI Workflows vs. Autonomous Agents (58:20 - 01:08:16)

**Objetivo:** distinguir workflow de agente por quién controla el flujo, y elegir lo más simple que funcione.

- Workflow: "Systems where LLMs and tools are orchestrated through predefined code paths." (00:58:20). La palabra clave es *predefined*.
- Patrones: secuencial (encadenar llamadas), routing (clasificar y derivar), paralelización/sectioning, voting (consenso), orchestrator-worker y evaluator-optimizer (01:00:15).
- "In a workflow, you the developer decide the steps in advance." (01:02:12). "In an agent, the LLM decides what to do next." (01:02:32).
- El test práctico: "Can I draw a flowchart of every possible path before running it?" (01:03:49). Sí → workflow; no → agente.
- Principio de diseño: "Find the simplest solution possible and only increase complexity when needed." (01:04:36).
- Cuatro preguntas de decisión: ¿puedo definir todos los caminos?, ¿el LLM debe decidir el siguiente paso?, ¿es una tarea repetible y bien definida?, ¿el costo debe estar estrictamente controlado? (01:06:50).
- "You don't have to choose just one." (01:07:10): los mejores sistemas mezclan workflow para lo predecible y agente para lo abierto.

**Ejercicio:** tomar tres tareas propias y clasificarlas con el checklist de cuatro preguntas, justificando cada respuesta. Entregable: `m9-workflow-o-agente.md`.

### Módulo 10 - The Core Loop: Perceive, Reason, Act (01:08:16 - 01:13:15)

**Objetivo:** definir agente sin misticismo: un LLM en un loop con tools y un objetivo.

- Definición del curso: "An AI agent is an LLM that runs in a loop using tools to accomplish a goal, deciding its own next steps based on what it observes." (01:09:22).
- La definición de Anthropic que cita: "agents are LLMs using tools based on environmental feedback in a loop" (01:09:41).
- El ciclo: percibir (input, resultados de tools, historial), razonar (decidir el próximo paso), actuar (llamar una tool o responder). "This loop is often called the perceive, reason, act cycle." (01:10:01).
- Ejemplo Zippy: busca restaurantes italianos, descubre que Trattoria Roma está llena, prueba la siguiente opción, chequea el calendario y reserva. "No developer wrote this sequence." (01:11:16).
- Límites actuales de Zippy: investigación superficial, sin ejecución de código, sin memoria entre sesiones. "These aren't bugs, they are design boundaries." (01:11:55).
- OpenClaw es el caso de producción del mismo loop: recibe mensajes de WhatsApp/Telegram/Slack, razona, ejecuta tools y responde (01:12:14).

**Ejercicio:** escribir el pseudocódigo del loop para un agente de reservas y marcar dónde exactamente decide el LLM y dónde decide tu código. Entregable: `m10-loop.md`.

### Módulo 11 - Hands-On Lab: Engineering the Standard While Loop (01:13:15 - 01:21:13)

**Objetivo:** implementar el loop mínimo y reconocer los cinco componentes de cualquier agente.

- Lab `agent_loop.py`: un `while true` que llama al modelo, lee `finish_reason` y corta en `stop`; la rama `else` es donde después entran las tools (01:13:53).
- Multi-turn: se reemplaza la pregunta única por una lista de preguntas y se van apendiendo preguntas y respuestas. "checking finish reason equals stop to decide when to exit is the core of every agent in this course." (01:15:10).
- Los cinco componentes: modelo (cerebro), tools (manos), memoria (contexto), loop de orquestación y system prompt (instrucciones y personalidad). "Every agent, no matter how simple or complex, is built from five components." (01:15:46).
- "His model is his brain." (01:15:46). Las tools definen qué puede hacer; la memoria es lo que sabe ahora; el loop es código sorprendentemente simple: "This is surprisingly simple." (01:17:38).
- El system prompt es el componente que más cambia el comportamiento: "A weak system prompt produces a chaotic agent." (01:18:18).
- "Openclaw uses all five." (01:18:18): modelo multi-proveedor con fallback, tools de bash/web/mensajería, memoria con compresión, core loop y system prompt configurable.

**Ejercicio:** escribir `agent_components.py` con los cinco componentes en un solo archivo y una tool mock de calendario. Entregable: el script corriendo.

### Módulo 12 - Planning Limits, Brittle Logic, & Mitigation Guardrails (01:21:13 - 01:26:19)

**Objetivo:** darle planeamiento al agente sin volverlo frágil: ReAct y límites duros.

- Savvy es la especialista en investigación. "Agents don't just react, they plan." (01:25:06). El plan ocurre dentro de la generación del LLM: "This planning happens inside the LLM's text generation." (01:21:52).
- Chain of thought aplicado a agentes: pedir en el system prompt que piense el plan paso a paso antes de actuar (01:22:12).
- ReAct: "The most common pattern for agent reasoning is called react, which stands for reasoning and acting." (01:22:32). El ciclo es pensamiento → acción → observación → nuevo pensamiento.
- Cuatro modos de falla: "Common failures going in circles, overplanning, wrong assumptions, not adapting." (01:25:24), sobre-planeación, supuestos equivocados y no adaptarse cuando la evidencia contradice el plan.
- Guardrails: "Maximum iterations. Cap the number of loop cycles to prevent infinite loops." (01:24:07); token budgets; instrucciones explícitas para fallas; "Structured output. require the agent to output its plan in a specific format" (01:24:26).
- OpenClaw aplica estos límites en la capa de orquestación: máximo de iteraciones, compresión de contexto y fallback de modelo (01:24:46).

**Ejercicio:** agregar a un agente ReAct un máximo de 8 iteraciones, un budget de tokens y una instrucción de fallback cuando la búsqueda no devuelve resultados. Entregable: `m12-guardrails.py`.

### Módulo 13 - Memory Managers: Sliding Windows & Vector DBs (01:26:19 - 01:33:56)

**Objetivo:** administrar la memoria de corto plazo y entender qué hace falta para la de largo plazo.

- Lab de memoria: `trim_history(messages, max_messages=6)` conserva el system prompt y corta lo más viejo. "A sliding window." (01:27:36). El contador de mensajes se estabiliza en seis: "the message count levels off at six" (01:27:56).
- El problema: cada iteración del agente suma razonamiento, tool calls y resultados; una tarea con 10 tool calls puede consumir decenas de miles de tokens (01:28:44).
- Tres estrategias: "Truncation simply drops the oldest messages." (01:29:04); summarization (resume lo viejo, cuesta una llamada extra); context compression (quita lo menos importante, no mensajes enteros).
- "The context window resets with each new conversation." (01:29:42). No viene con el LLM: es una capa de ingeniería.
- Implementaciones: key-value store inyectado en el system prompt, "A vector database stores past conversations as embeddings" (01:30:02), o archivos que el agente lee después.
- El impacto es de producto: "It's the difference between an agent that feels smart for one conversation and one that feels smart over time." (01:30:59).
- El lab de ReAct cae dentro de este capítulo en el mapa oficial: se pide escribir "Before every tool call, write thought colon your reasoning." (01:32:44).

**Ejercicio:** implementar `load_memory`/`save_memory` sobre JSON e inyectar las preferencias en el system prompt al arrancar. Entregable: `m13-memoria-persistente.py`.

### Módulo 14 - Multi-Agent Frameworks & Inter-Agent Communication (01:33:56 - 01:43:08)

**Objetivo:** saber cuándo partir un agente en varios y cómo se pasan información.

- Meshy (memoria) y Cody (código) se suman al equipo. "Zippy becomes something new. Not just an assistant, but an orchestrator." (01:34:35).
- El problema que resuelve: "A single agent with 50 tools and a massive system prompt can get confused." (01:34:55).
- Patrón principal: "One common pattern, orchestrator plus specialists." (01:35:15). Zippy descompone, Savvy investiga, Meshy guarda preferencias, Cody escribe el script y Zippy ensambla.
- Paralelismo: "In a multi- aent system, they happen in parallel." (01:35:53). También hay pipeline (planner → executor → reviewer) y debate/adversarial con sintetizador (01:36:29).
- Comunicación: historial compartido, handoff messages o memoria compartida; cada uno con trade-offs de complejidad, latencia y consistencia (01:36:50).
- Regla de uso: "Multi-agent systems add complexity. Only use them when you really need them." (01:37:08). Un agente bien diseñado suele alcanzar.
- Lab `patterns_agent.py`: structured output (bloque JSON final), input guardrails y human-in-the-loop para acciones de alto riesgo. "A deterministic Python function can't be jailbroken or persuaded." (01:39:38). "Every other tool runs without interruption." (01:39:56).

**Ejercicio:** diseñar un sistema de tres agentes para un caso propio, definiendo handoffs y qué información viaja en cada uno. Entregable: `m14-multiagente.md`.

### Módulo 15 - Deconstructing Production Failures & Error Handling (01:43:08 - 01:52:20)

**Objetivo:** diseñar para la falla: los seis modos y las cinco reglas.

- Cody ejecuta código y por eso es el que más falla: scripts, bases de datos y comandos tienen efectos laterales. "Cody is a code and automation specialist." (01:43:08).
- "There are six common failure modes." (01:43:46): tool failure, mala selección de tool, tool call alucinada, loop infinito, overflow de contexto y errores del modelo.
- Tool failures: "When a tool call fails, don't hide the error. Send it back to the agent as context." (01:44:24). El agente ve el error y cambia de estrategia.
- "Infinite loops are the biggest threat." (01:45:02): contador de iteraciones y, al llegar al límite, forzar la mejor respuesta disponible.
- "Use model fallback." (01:45:59): si el proveedor primario falla, se prueba otro. Claude → GPT → Gemini en el ejemplo.
- "Five core principles for error handling." (01:46:18): esperar fallas, mostrar el error al agente, límites duros, loggear todo y fallar con gracia ante el usuario.
- "Robust error handling is what separates demo agents from production systems." (01:47:34).

**Ejercicio:** envolver un tool en try/except que devuelva el error al agente y agregar un tope de iteraciones con salida graceful. Entregable: `m15-errores.py`.

### Módulo 16 - Grounding Data & Prepackaged Frameworks (LangChain, Mastra) (01:52:20 - 02:00:25)

**Objetivo:** traducir vocabulario entre proveedores y decidir framework vs. código propio.

- El problema: Google llama "extensions", "grounding" y "orchestration layer" a lo que Anthropic llama agents, tools y el loop. "mostly the same thing with different names" (01:52:42).
- Extensions vs. function calling: en extensions el agente llama la API directamente; en function calling tu aplicación ejecuta. Function calling da más control (01:53:20).
- "One of Google's key contributions is the concept of grounding" (01:53:40): conectar respuestas a fuentes verificables (búsqueda o data stores).
- "A grounded agent is less likely to make things up because it's citing real sources." (01:54:20).
- Frameworks: LangChain/LangGraph (Python, grafo), Anthropic SDK (liviano), OpenAI Agents SDK (handoffs), Google ADK (Gemini/Google Cloud) y Mastra (TypeScript-first) (01:56:19).
- "The trade-off is control versus speed." (01:56:00). Los frameworks deciden estructura por vos; si no coincide, peleás con el framework.
- OpenClaw no usa ninguno: "Open Claw doesn't use Langchain, Langraph, the OpenAI agents SDK" (01:58:34); se apoya en "a purpose-built package by Mario Zechner, the same developer behind OpenClaw." (01:58:53). Razones: caso de uso específico, abstracciones que gotean, lock-in y tamaño.

**Ejercicio:** comparar LangGraph y Mastra para un caso concreto (lenguaje, lock-in, ecosistema) y escribir una recomendación de 5 líneas. Entregable: `m16-frameworks.md`.

### Módulo 17 - Hands-On Lab: Building a Production Personal Assistant (02:00:25 - 02:09:25)

**Objetivo:** convertir el agente de juguete en uno que no se cae ni se cuelga.

- Dos fallas del agente feliz: un tool que lanza excepción mata el script, y un `while true` puede no terminar nunca. "This lab fixes both." (02:00:25).
- "The fix wrap tool execution in try except inside execute tool." (02:01:02): el error vuelve como string al agente, no como traceback al usuario.
- "After the loop, add a four else block." (02:02:00): el `for` con `max_iterations` y el `else` que pide la mejor respuesta posible cuando se agota el presupuesto.
- Lab de SDK desde cero: instalar, crear cliente con base URL y API key, mandar un mensaje y leer `choices[0].message.content`. "Six lines of real code." (02:05:02).
- Historial: se apende la respuesta del assistant y la pregunta siguiente para que el modelo vea el intercambio completo (02:05:40).
- Lab final: `tools_starter.py` + `agent_starter.py`, tres tools (`check_cal`, `search_web`, `get_user_preferences`), `run_agent` con loop y tope de iteraciones. "One agent, three tools, conversation memory, error handling." (02:09:02).

**Ejercicio:** completar el asistente con una cuarta tool propia y probar una tarea de dos pasos que la requiera. Entregable: `m17-asistente.py` + transcripción de la corrida.

### Módulo 18 - OpenClaw Codebase Tour & File Architecture (02:09:25 - 02:14:39)

**Objetivo:** tener un mapa para leer un codebase de agente grande sin perderse.

- "Most are support structure, clients, platform, code, tooling." (02:10:54). El agente vive en `src/`; el resto es soporte, clientes, plataforma y tooling.
- Seis áreas dentro de `src/`: agent loop, memoria, tools, canales, providers y seguridad (02:11:14).
- "The key file is pi embedded runner.ts." (02:11:14). "The key file is pi embedded runner.ts." (02:11:14), donde corre el ciclo percibir-razonar-actuar.
- Memoria: `manager.ts` lee/escribe/busca; `search-manager.ts` hace búsqueda vectorial; SQLite como storage (02:11:53).
- Tools: `openclaw-tools.ts` registra más de 50 tools, cada una con descripción y schema; `bash-tools.ts` es la ejecución de shell (02:12:32).
- Canales y providers: cada plataforma normaliza mensajes; `hybrid.ts` prueba proveedores en secuencia y hace fallback (02:13:32).
- Seguridad: `src/agent-sandbox` controla binarios, paths y operaciones. "The agent cannot talk its way past them." (02:14:11). Las reglas están en código, no en el prompt.

**Ejercicio:** recorrer el repo real de OpenClaw y ubicar los seis directorios de `src/`, anotando qué archivo haría qué en un caso propio. Entregable: `m18-mapa-repo.md`.

### Módulo 19 - Custom Layouts, Terminal Interfaces, & Concurrency Locks (02:14:39 - 02:30:44)

**Objetivo:** entender cómo OpenClaw convierte el loop de tutorial en sistema concurrente y persistente.

- El camino de un mensaje: canal → normalización → routing → gateway WebSocket → agent loop → auto-reply → canal. "OpenClaw is a single user self-hosted AI assistant." (02:14:41).
- "Open Claw has eight main systems." (02:15:36): ejecución, gateway, canales, tools, routing, plugins, config y memoria.
- Cuatro paquetes de Mario Zechner: `pi-ai` (llamadas HTTP/streaming), `pi-agent-core` (tipos y `AgentTool`), `pi-coding-agent` (sesión y loop) y `pi-tui` (terminal). "OpenClaw owns the edges. The PI packages own the middle." (02:20:58).
- Lab de ACI: dos tools vagas (`search`, `get_info`) hacen que el modelo elija mal; con descripciones precisas, enums y normalización de parámetros, la misma pregunta acierta siempre. "Three changes all to the interface. Now not the logic." (02:23:07).
- "The loop runs in five phases." (02:23:28): setup, validación de contexto, attempt loop, error handling y persistencia.
- Persistencia: JSONL por sesión, write lock, compaction cuando el contexto se acerca al límite y OAuth profile tracking (02:26:04).
- "The core loop. Send to model. Check for tool calls. Execute tools. Repeat. That's 10 lines of code." (02:27:40). Lo que lo hace producción es lo que lo rodea: locks, fallback, compaction, error recovery.
- Lab de memoria persistente: guardar preferencias en JSON, cargarlas al inicio e inyectarlas en el system prompt. "The model doesn't remember anything. Your code does." (02:28:00).

**Ejercicio:** implementar un `save_preference`/`forget_preference` sobre JSON y demostrar que una corrida nueva recuerda la preferencia sin repetirla en el prompt. Entregable: `m19-memoria-json.py`.

### Módulo 20 - Testing Non-Deterministic Agents & LLM-as-a-Judge Evals (02:30:44 - 02:39:30)

**Objetivo:** probar algo que no devuelve siempre lo mismo, sin resignar rigor.

- "Testing an agent is not like testing a regular function." (02:30:44): el mismo input puede tomar caminos distintos y producir respuestas distintas.
- Cuatro razones: output no determinístico, múltiples respuestas válidas, dependencias externas y caminos de ejecución complejos (02:31:22).
- Qué testear: selección de tool, argumentos válidos, recuperación de errores, formato de salida, cumplimiento de guardrails y finalización de la tarea. "You test behaviors and properties." (02:32:02).
- Cuatro estrategias: unit tests de tools (sin LLM), mocks de respuestas, evals con LLM como juez y end-to-end en schedule (02:33:18).
- "Strategy three, evaluation based testing or eval." (02:34:14). "You can use another language model as a judge." (02:34:35): input + respuesta + rúbrica 1-5; falla debajo de 3.
- En OpenClaw el framework es Vitest: unit de tools, schema tests, integración de routing y persistencia; el comportamiento del LLM se cubre con evals y revisión manual (02:35:36).
- Lab `test_agent.py`: tres capas en un archivo. "Three layers, one file." (02:38:56): unit, mock y eval con una llamada real.

**Ejercicio:** escribir tres tests para un agente propio: uno de tool, uno de dispatcher con mock y uno de formato de salida. Entregable: `m20-tests.py` con la salida de la suite.

### Módulo 21 - Observability, Tracking Performance Metrics, & Optimization Levers (02:39:30 - 02:51:55)

**Objetivo:** poder explicar qué hizo un agente en producción y bajar costo/latencia con evidencia.

- "Log everything. Measure what matters." (02:39:48): loggear cada paso del loop (mensaje, tool call con argumentos, resultado con tokens, respuesta final, tiempo total).
- "There are six numbers worth tracking on every request." (02:40:45): tokens por request, tool calls, latencia, tasa de error, iteraciones y uso de contexto.
- Debug por síntoma: respuesta mala → mirar los datos de la tool ("Fix the tool, not the model.", 02:42:20); tool equivocada → descripciones; loop sin progreso → formato del resultado; lento → separar tiempo de LLM y de tool.
- "diagnosed by reading 3 minutes of logs." (02:44:38). OpenClaw streamea eventos en tiempo real (texto, tool calls, errores, retries, compaction).
- Lab `monitored_agent.py`: `run_log` por tool con duración y resultado truncado, contadores de tokens prompt/completion, conteo de iteraciones con warning y resumen final.
- Performance: "The biggest cost driver is almost always context size." (02:47:43). El caso del video pasa de 250.000 a 75.000 tokens, "a 70% reduction in token cost with no change to what the agent can do" (02:48:23).
- Palancas: reducir llamadas, reducir contexto, rutear a modelos baratos, paralelizar tools y cachear. Orden: "Don't optimize prematurely." (02:51:33). "Open claw handles concurrent users with execution lanes." (02:50:16).

**Ejercicio:** instrumentar un agente con log por tool y contadores de tokens, correr una tarea y proponer una reducción de contexto basada en los números. Entregable: `m21-metricas.md` + script.

### Módulo 22 - Agent Security, Advanced Prompt Assemblies, & Wrap-up (02:51:55 - 03:05:58)

**Objetivo:** cerrar con el modelo de amenazas de un agente y las técnicas de prompt que usa OpenClaw en producción.

- "An AI agent is different." (02:51:55): llama tools, lee archivos, ejecuta código y manda mensajes; esa capacidad es el riesgo.
- Cuatro riesgos: "First, prompt injection." (02:52:15); tool abuse; data exfiltration; excessive permissions. "Every capability you don't need is an attack surface you don't have to defend." (02:53:32).
- Mitigaciones: sandbox, mínimo privilegio, validación de argumentos en el borde de la tool, filtrado de salida, rate limiting y aprobación humana para acciones destructivas.
- "Think of it as defense in depth." (02:55:49): ninguna capa alcanza sola. Principio final: "Never trust input" (02:56:08), ni del usuario ni de las tools ni de datos externos.
- Seis técnicas de prompting: persona, positivo sobre negativo, orden/estructura (patrón U: 75% de acierto al inicio/final vs. 45% en el medio, 03:00:55), chain of thought por estructura (tags `think`/`final`), "before replying" (memoria y skills antes de responder) y few-shot en el system prompt (02:57:25).
- Dos extra: emotional framing (mejora ~8% promedio, hasta 115% en generación compleja, 03:04:09) y re-reading/RE2 (repetir la pregunta al final, 03:04:49). **Claims de papers sin link en el video: tratar como afirmaciones, no como evidencia verificada.**
- Cierre: el system prompt de OpenClaw lo arma una función de 646 líneas con secciones condicionales y orden deliberado. "The key insight at scale prompt engineering becomes software engineering." (03:05:28).

**Ejercicio:** hacer el threat model de un agente propio en una página: activos, entradas no confiables, tools peligrosas y capa de defensa para cada riesgo. Entregable: `m22-threat-model.md`.

## Ejercicios por bloque

- [ ] M1: explicar un LLM en 10 líneas sin jerga.
- [ ] M2: tabla de tres modelos actuales con fuente y fecha.
- [ ] M3: diagrama app → API → modelo.
- [ ] M4: costo de un agente de 5 iteraciones.
- [ ] M5: cinco instrucciones negativas reescritas.
- [ ] M6: temperatura 0 vs. 1, dos corridas cada una.
- [ ] M7: script que combine código determinístico y LLM.
- [ ] M8: schema + handler de una tool.
- [ ] M9: tres tareas clasificadas con el checklist.
- [ ] M10: pseudocódigo del loop de reservas.
- [ ] M11: `agent_components.py` con los cinco componentes.
- [ ] M12: guardrails de iteraciones, tokens y fallback.
- [ ] M13: memoria persistente en JSON.
- [ ] M14: diseño de un sistema de tres agentes.
- [ ] M15: tool con try/except y tope de iteraciones.
- [ ] M16: comparación LangGraph vs. Mastra.
- [ ] M17: asistente con una cuarta tool.
- [ ] M18: mapa de `src/` del repo real.
- [ ] M19: `save_preference`/`forget_preference`.
- [ ] M20: suite de tres tests.
- [ ] M21: instrumentación y propuesta de reducción.
- [ ] M22: threat model de una página.

## Banco de preguntas para estudiar con el usuario

1. ¿Por qué un LLM puede sonar seguro y estar equivocado? Explicá el mecanismo, no la etiqueta "alucinación".
2. Si tu agente hace 8 iteraciones con 30k tokens de contexto cada una, ¿dónde está el costo y qué recortarías primero?
3. ¿Qué diferencia hay entre una tool que devuelve datos y una que tiene efectos laterales? ¿Cómo cambia el diseño?
4. ¿Cuándo un workflow es mejor que un agente? Dame un caso propio y justificalo con las cuatro preguntas.
5. ¿Qué tres guardrails le pondrías a un agente que puede mandar emails? ¿Por qué esos y no otros?
6. ¿Cómo probarías que un agente elige la tool correcta sin gastar tokens en cada test?
7. ¿Qué loggearías para poder reconstruir una corrida que salió mal? ¿Qué métrica te dice que el contexto está por explotar?
8. ¿Cuál es la diferencia entre sandbox, mínimo privilegio y validación de argumentos? ¿Por qué se necesitan las tres?
9. ¿Qué técnica de prompting te parece más riesgosa de adoptar sin medir? ¿Cómo la validarías?

## Notas editoriales

- **Nombre del expositor:** el ASR dice "Mumshed" y "Bumshad Manhatt"; la ficha del curso y la plataforma del expositor apuntan a **Mumshad Mannambeth**, fundador de KodeKloud. "CodeCloud" en el ASR es **KodeKloud**. El glosario de `transcripcion.md` lo deja asentado.
- **Mapa oficial vs. contenido real:** los 22 capítulos son los de la descripción del video, pero los límites no siempre coinciden con el contenido. Casos claros: el lab de ReAct cae dentro del capítulo de memoria (13), el capítulo 19 se titula "Custom Layouts, Terminal Interfaces, & Concurrency Locks" pero contiene el tour de paquetes PI, el lab de ACI y el lab de memoria persistente, y el capítulo 22 incluye toda la sección de prompt engineering. Se respetó el mapa oficial 1:1 y se anotó el contenido real de cada bloque.
- **Duplicados de edición:** la intro se repite casi literal entre 00:00:38 y 00:04:17, y el segmento de parámetros se repite entre 00:10:46 y 00:16:07. Parece un empalme de grabación; el transcript los conserva.
- **Precios y modelos:** el video da precios de GPT-4o y una lista de modelos de 2026 ("Cloud Opus 4.6", "GBD 5.5", "Gemini 2.5") que son datos mutables. No se usan como referencia vigente sin verificar contra la página oficial del proveedor.
- **Papers citados sin link:** activation patching (2025),Turpin et al. (2023), el benchmark de negación (ACL 2023), el estudio de atención en forma de U (Stanford 2024), emotional framing (Microsoft Research 2023) y RE2 (EMNLP 2024). El video no da DOIs ni URLs; quedan como afirmaciones del expositor, no como bibliografía verificada.
- **OpenClaw como caso:** el curso describe un agente open source llamado OpenClaw, pero no necesariamente la versión que corre en este workspace. Cualquier afirmación sobre archivos, tools o comportamiento actual se verifica contra el repo/instalación local antes de usarse.
- **Acciones externas:** la clase usa labs con API keys provistas por KodeKloud; nada de lo que se haga en los labs debe ejecutarse contra las credenciales reales del workspace sin OK.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
