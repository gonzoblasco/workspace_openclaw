# Clase: AI Engineer Full Course in 3 Hours [FREE]

- Fuente: https://www.youtube.com/watch?v=XFNggsFFZJw
- Canal: Cloud X Berry
- Expositor: no nombrado en el video ni en la descripción
- Duración: 2:53:54
- Publicado: 2026-10-11
- Idioma: inglés (subtítulos automáticos, glosario de ASR en `transcripcion.md`)
- Capítulos: los 33 oficiales de la descripción, más los 7 intros/recaps de módulo, alineados 1:1 con los módulos

## Tesis de la clase

**Poner un modelo a responder es la parte fácil; el trabajo está en lo que se construye alrededor.** El curso no enseña un framework ni un lenguaje: enseña la arquitectura de un sistema de IA en producción, y lo hace con un solo caso que evoluciona. Un agente de reembolsos de una tienda ficticia, **Cloud X Berry**, que arranca como un chatbot que solo contesta y termina siendo un sistema en producción con tools, MCP, RAG, un knowledge graph, un add-on fine-tuneado, un gateway, evals, red teaming y un platform interno. Cada módulo es la respuesta a un límite concreto del anterior.

Los módulos 1 a 3 son el núcleo conceptual (agente → sistema → conocimiento). Los módulos 4 y 5 son lo que casi ningún curso de producto cubre: **por qué el modelo se comporta como se comporta** y **qué corre debajo, físicamente, con qué costo**. El módulo 6 cierra con lo que decide si el proyecto vive o muere: operación, evaluación, seguridad de plataforma.

## Resultado esperado

Al terminar la clase deberías poder:

1. Distinguir un chatbot de un agente por lo que **hace**, no por cómo se ve, y enumerar los cinco subsistemas alrededor del modelo (percepción, razonamiento, acción, aprendizaje, comunicación).
2. Decidir cuándo un agente alcanza y cuándo corresponde un **sistema multi-agente**, con sus costos reales (llamadas, contexto perdido en handoffs, dificultad para atribuir el error).
3. Explicar por qué un agente olvida, y tratar la **ventana de contexto como un presupuesto**, incluido el efecto "lost in the middle".
4. Escribir tool calling correcto: schema explícito, descripción tan cuidada como el prompt, errores devueltos como información, y aprobación humana para acciones irreversibles.
5. Diferenciar **MCP** de **agent skills**: protocolo de conexión a herramientas vs. empaquetado de know-how, y cuándo hace falta cada uno (o ninguno).
6. Justificar un **AI gateway** frente a un API gateway, y qué agrega para tráfico de modelo (costo por token, routing, fallback, chequeos, caché).
7. Diagnosticar un RAG por la **cadena de recuperación** antes de culpar al modelo, y elegir entre las variantes (híbrido, re-ranking, rewrite, corrective RAG, Self-RAG) por el fallo concreto que cada una arregla.
8. Separar **knowledge graph**, **GraphRAG** y **graph engineering**, y diseñar una knowledge base viva (versionado, borrado real, proveniencia, revisión) en vez de un cementerio de notas.
9. Explicar de dónde viene el comportamiento de un modelo y elegir entre cambio de **conocimiento (RAG)**, de **comportamiento (fine-tuning/LoRA)** o de **tamaño/costo (distilación, compresión, routing)**, empezando por el peldaño más barato.
10. Describir qué hacen CPU, GPU, TPU y NPU, por qué CUDA es un foso competitivo, y por qué **prefill** y **decode** estresan el hardware de forma distinta.
11. Elegir entre cloud generalista, NeoCloud y capacidad cruda, y qué palancas de costo funcionan (prompt caching, recorte de tokens, routing) — y cuáles se olvidan.
12. Explicar por qué el ciclo de desarrollo cambia (**SDLC → AIDLC**), qué agregan MLOps y LLMOps sobre DevOps, y cómo se diseña una eval con golden dataset.
13. Nombrar las **siete razones por las que un proyecto de IA muere después del piloto** y atacarlas antes de escribir código.
14. Correr **red teaming** sobre un agente que mueve dinero, y entender que la defensa vive en el sistema, no en el prompt.
15. Dibujar la anatomía completa de un sistema de IA listo para producción y trazar una request fallida por todas sus capas.

## Mapa temporal

| Tiempo | Bloque |
|---|---|
| 0:00:00 - 0:02:38 | Course Intro: qué se construye y qué no hace falta saber |
| 0:02:38 - 0:03:26 | Módulo 1 Intro: de responder a hacer |
| 0:03:26 - 0:06:08 | 1. Qué hace que algo sea un agente |
| 0:06:08 - 0:09:40 | 2. Los cinco subsistemas alrededor de un agente |
| 0:09:40 - 0:13:09 | 3. Un agente vs. multi-agente |
| 0:13:09 - 0:16:53 | 4. Memoria del agente: por qué olvidan |
| 0:16:53 - 0:21:05 | 5. Ventana de contexto como presupuesto y "lost in the middle" |
| 0:21:05 - 0:22:01 | Módulo 1 Recap |
| 0:22:01 - 0:22:47 | Módulo 2 Intro: de un agente a un sistema |
| 0:22:47 - 0:28:20 | 6. Tool calling |
| 0:28:20 - 0:33:13 | 7. MCP |
| 0:33:13 - 0:37:54 | 8. MCP vs. agent skills |
| 0:37:54 - 0:43:01 | 9. Roles y límites: propiedad clara en multi-agente |
| 0:43:01 - 0:47:46 | 10. El AI gateway |
| 0:47:46 - 0:49:07 | Módulo 2 Recap: dónde se chequea cada request |
| 0:49:07 - 0:50:00 | Módulo 3 Intro: darle algo en qué apoyarse |
| 0:50:00 - 0:54:53 | 11. Más allá del RAG básico |
| 0:54:53 - 1:00:03 | 12. Guía de variantes de RAG |
| 1:00:03 - 1:05:34 | 13. Knowledge graph vs. GraphRAG vs. graph engineering |
| 1:05:34 - 1:10:14 | 14. Agentic RAG: cuando la recuperación es una decisión |
| 1:10:14 - 1:15:44 | 15. Una knowledge base viva, no un cementerio de notas |
| 1:15:44 - 1:17:07 | Módulo 3 Recap: cuando la respuesta vive en un documento |
| 1:17:07 - 1:17:56 | Módulo 4 Intro: de dónde viene el comportamiento |
| 1:17:56 - 1:23:31 | 16. Arquitectura de datos para IA: pipelines, versionado, lineage |
| 1:23:31 - 1:29:19 | 17. De las primeras redes neuronales a los transformers |
| 1:29:19 - 1:34:18 | 18. Cambiar un modelo: conocimiento, comportamiento o tamaño |
| 1:34:18 - 1:38:59 | 19. LoRA |
| 1:38:59 - 1:43:37 | 20. Distilación |
| 1:43:37 - 1:49:08 | 21. El rol del reinforcement learning |
| 1:49:08 - 1:50:29 | Módulo 4 Recap |
| 1:50:29 - 1:51:19 | Módulo 5 Intro: qué hace falta para correr esto |
| 1:51:19 - 1:55:54 | 22. El alfabeto de chips: CPU, GPU, TPU, NPU |
| 1:55:54 - 2:00:42 | 23. Qué hace CUDA |
| 2:00:42 - 2:05:47 | 24. Dentro de una GPU: entrenamiento vs. inferencia |
| 2:05:47 - 2:10:59 | 25. Clouds hechos para IA |
| 2:10:59 - 2:16:19 | 26. Prompt caching y otras palancas de costo |
| 2:16:19 - 2:17:42 | Módulo 5 Recap: qué corre debajo y cuánto cuesta |
| 2:17:42 - 2:18:38 | Módulo 6 Intro: cómo sabés que funciona y sigue funcionando |
| 2:18:38 - 2:23:16 | 27. SDLC vs. AIDLC |
| 2:23:16 - 2:27:42 | 28. DevOps vs. MLOps vs. LLMOps y el trace |
| 2:27:42 - 2:32:59 | 29. AI evals |
| 2:32:59 - 2:37:21 | 30. Por qué los proyectos de IA fallan en producción |
| 2:37:21 - 2:42:17 | 31. AI red teaming |
| 2:42:17 - 2:47:06 | 32. Platform engineering para IA |
| 2:47:06 - 2:52:35 | 33. Anatomía de un sistema de IA listo para producción |
| 2:52:35 - 2:53:54 | Módulo 6 Recap: el sistema entero, punta a punta |

## Módulos

### Módulo 1 — De responder a hacer (0:02:38 - 0:22:01)

**Objetivo:** entender qué distingue a un agente de un chatbot y qué piezas lo rodean.

- **La definición operativa es por acción, no por apariencia.** El mismo mensaje («mi pedido llegó roto, quiero un reembolso») en un chatbot termina en una respuesta; en un agente sigue: "A person still has to find the order, check the policy, and send the money back. Now, picture the same message going to an agent. It looks up the order" (03:52).
- **Cinco subsistemas como checklist, no como cajas obligatorias.** "One way to break an agent down is into five core subsystems: perception," (06:48) — y la advertencia de que "These are useful capabilities to look for, not five boxes that every agent must have" (07:03).
- **Percepción ≠ grounding.** "Perception is about reading what comes in. Grounding is about tying the agent's answer to real data it looked up" (07:32).
- **Razonamiento incluye routing.** "while a harder task goes to a larger one. That choice is called routing" (08:02).
- **Acción tiene aduana.** El layer valida el formato, ejecuta y devuelve errores como información; y "some actions can't be undone, like a refund or a change to a live system. For those this layer pauses and asks a person to approve it" (08:32). El modelo propone; el sistema dispone.
- **"Learning" acá no es entrenar.** "Here learning doesn't mean retraining the model. It means the system around the model uses what happened before to do better" (08:45).
- **El número de modelos no es el número de agentes.** Un agente es un loop de decisión: "It might call more than one model along the way, but one loop is in charge" (10:14).
- **Regla de multi-agente:** empezar con uno. "Start with one agent and stay there when one agent can" (12:28); escalar cuando el trabajo se parte de verdad, no cabe en un contexto, o hace falta un chequeo independiente. Y el recordatorio incómodo: "Splitting the work doesn't automatically improve the thinking" (12:58).
- **Memoria es almacenamiento + búsqueda, no una caja mágica.** "A vector database is one way to find those facts by meaning. It's a storage and search tool, not the memory itself" (15:26).
- **Ventana de contexto como presupuesto.** La analogía de los 40 CVs: los primeros se leen, el medio se escanea, los últimos quedan frescos. Eso es *lost in the middle*, y empeora en agentes porque cada step agrega output y errores.

**Preguntas de estudio:**
- ¿Un sistema con tres modelos y un loop es uno o tres agentes? ¿Por qué?
- ¿Qué diferencia hay entre que el agente "aprenda" y que se reentrene el modelo?
- Si un pipeline multi-agente da una respuesta mala, ¿qué te cuesta más: encontrarlo o arreglarlo?

**Ejercicio:** tomá un flujo que hoy resuelve un humano (aprobación, reclamo, búsqueda de datos) y escribí en una tabla las cinco columnas de subsistemas: qué haría cada una en tu caso, y cuál de las cinco NO tiene hoy. Entregable: `agente-checklist.md`.

### Módulo 2 — De un agente a un sistema (0:22:01 - 0:49:07)

**Objetivo:** conectar el agente con el mundo: tools, protocolo, know-how, propiedad y puerta de entrada.

- **Una tool es una descripción, no código.** "It only sees this description. So, a vague description leads to wrong choices. Good teams write tool descriptions as carefully as they write prompts" (24:00).
- **El modelo escribe una request estructurada.** No "decide" por dentro: emite un objeto con nombre de tool y schema de inputs (0:24:00).
- **Cada paso se registra: el trace.** "That record is called a trace. Each line shows which tool was asked for, with what inputs, what came back, how long it took, and what it cost" (27:13). El trace vuelve en el Módulo 6 como columna vertebral de operaciones — es el mismo concepto, no otro.
- **MCP resuelve el problema N×M.** "10 apps and 10 tools can mean a 100 separate pieces of glue code" (29:05). La diferencia con tool calling manual: "the server provides it instead of a developer pasting it into each app" (30:59).
- **Agent skill = carpeta con instrucciones que se cargan bajo demanda.** "A skill is a folder. Inside is a main instruction file with a short header and a longer body" (34:40); la idea es "load instructions when they are needed, not all at once" (37:49). Skill ≠ MCP: MCP conecta herramientas, skill empaqueta know-how. Y "if the agent is small with one clear job, you may need neither" (37:34).
- **Multi-agente sin dueño es un problema de organización.** Propiedad clara por parte del trabajo, y el checking agent que devuelve el trabajo es tan valioso como la velocidad.
- **AI gateway vs. API gateway.** Un gateway común ya hace login, rate limit, routing y logs; el de IA agrega control de **costo por token**, elección de modelo, fallback entre proveedores, chequeos de contenido y caché. La analogía del ponente: "An AI gateway works more like a company expense system for model calls" (45:13).

**Preguntas de estudio:**
- ¿Por qué una descripción de tool vaga produce errores que no aparecen en el código?
- ¿En qué caso escribís una skill y en qué caso un servidor MCP? ¿Y cuándo ninguno?
- ¿Qué se puede hacer con un AI gateway que sea imposible con un API gateway?

**Ejercicio:** listá las 5 acciones externas de tu producto y para cada una escribí la descripción de 1 línea que vería el modelo, el schema de inputs y si pide aprobación humana. Entregable: `tools.md`.

### Módulo 3 — Darle al agente algo en qué apoyarse (0:49:07 - 1:17:07)

**Objetivo:** entender por qué el RAG básico se rompe y cómo elegir la variante correcta por el fallo que arregla.

- **Qué hace el RAG básico.** Buscar los documentos, meter los mejores pasajes en el contexto y responder sobre esa evidencia en vez de la memoria del modelo (0:50:15-0:50:31).
- **Diagnóstico antes que parche.** "Instead of blaming the model, you walk the retrieval path one step at a time" (53:48): ¿el documento está en el índice?, ¿es la versión actual?, ¿el chunk conservó la regla y su excepción juntas?, ¿el buscador trajo lo correcto?
- **Las variantes se justifican por el fallo que arreglan, y cada una cuesta.** Hybrid retrieval (términos exactos que los embeddings pierden), re-ranking, rewrite de query y answer check. "Every piece you add costs time, money, and one more thing that can fail" (59:40); la regla: "Add anything else only when you can name the failure it fixes" (55:28).
- **Tres preguntas antes de aprobar un diseño RAG complejo:** qué fallo arregla, cuánto cuesta, cómo se sabe que funciona (0:59:40).
- **Knowledge graph ≠ GraphRAG ≠ graph engineering.** La analogía de la red de trenes: el mapa (el grafo), el planificador de rutas (GraphRAG, que trae información relacionada a la respuesta) y el equipo de topografía (graph engineering: decidir qué nodos y links mantener y extraerlos). El nombre GraphRAG "is used loosely right now so it's fair to ask a team what they mean by it" (1:03:17).
- **El diagnóstico de una respuesta mala va por capas:** primero ¿el hecho estaba en la base?, después ¿la recuperación siguió el link correcto y fue lo bastante lejos?, recién ahí la decisión del agente (1:04:25).
- **Agentic RAG cambia quién decide.** "Agentic rag changes who's in charge of that path" (1:06:01). La recuperación pasa a ser una tool que el agente elige; el camino no lo escribió nadie de antemano.
- **Knowledge base viva.** Ingestion continua, versionado con fecha de vigencia, borrado real (si no, "a retired policy can keep answering questions for months", 1:12:13), proveniencia y revisión. "A living knowledge base is the opposite. It's treated like software" (1:11:14).
- **El retrieval también respeta permisos.** "Retrieval should respect who's asking the same way the rest of the system does" (1:13:24): sin eso, el agente cita una nota interna a un cliente.

**Preguntas de estudio:**
- El agente responde con una política vencida. ¿Cuál de las cuatro preguntas del retrieval path falla primero?
- ¿Cuándo un knowledge graph te da algo que ningún chunk puede dar?
- ¿Por qué agentic RAG es más caro y más difícil de evaluar que un pipeline fijo?

**Ejercicio:** tomá tres respuestas malas reales de un asistente de documentos y diagnosticá cada una en una capa distinta (ingesta, versión, chunking, ranking, decisión). Entregable: `diagnostico-rag.md`.

### Módulo 4 — De dónde viene el comportamiento (1:17:07 - 1:50:29)

**Objetivo:** saber qué cambia realmente cuando alguien pide fine-tune, y elegir el peldaño más barato.

- **Datos primero, con versión y lineage.** Cada modelo entrenado apunta al dataset, al código y a los settings que lo produjeron: "That trail is called lineage" (1:21:06). Sin eso no hay rollback ni explicación.
- **Por qué transformers.** Backpropagation, y *Attention Is All You Need* (2017): atención que pesa tokens entre sí en paralelo, con múltiples heads. Eso es lo que permite entrenar sobre volúmenes enormes.
- **Tres cosas distintas a cambiar:** qué sabe (conocimiento → retrieval), cómo se comporta (comportamiento → fine-tuning), y cuánto cuesta (tamaño → distilación/compresión/routing). "So when a team says we need to fine-tune, ask what exactly they want to change" (1:34:04).
- **LoRA = congelar el original y entrenar un add-on chico.** "Laura takes a lighter path. The name stands for low rank adaptation. The idea is to freeze the" (1:35:03). Evita copiar el modelo entero por tarea y el olvido catastrófico del fine-tuning completo.
- **Tres preguntas sobre un LoRA propuesto:** qué queda congelado, qué debe cambiar el add-on, y cómo se comprueba que ayudó sin romper lo demás (1:38:34). Y no subir el rank "automatically better": "Raise it when your evaluation show a real gap, not before" (1:38:34).
- **Distilación = student imita al teacher por ejemplos, no por pesos.** "The teacher generates highquality examples and the student learns to reproduce the behavior those examples show" (1:40:16). El truco de 2015: el teacher da una distribución sobre todas las opciones y esa información fina ayuda más que la etiqueta dura.
- **RL aprende por consecuencia, no por ejemplo.** Rewards sobre respuestas generadas (1:44:06). Y la advertencia clave: "Optimizing for a feedback signal can push behavior the wrong way if the evaluation doesn't measure what you care about" (1:48:10). Si el único reward es satisfacción del cliente, el atajo es prometer reembolsos a todos.
- **La respuesta completa suele ser una mezcla:** políticas por retrieval, tono por add-on chico, costo por modelo destilado y routing (1:33:09-1:33:23).

**Preguntas de estudio:**
- ¿Qué se congela en un LoRA y por qué eso reduce el riesgo de olvido?
- ¿Distilación copia pesos? ¿Qué copia exactamente?
- Un reward mal elegido, ¿con qué se parece más: a un bug o a un incentivo perverso?

**Ejercicio:** tomá un pedido de "necesitamos fine-tuning" y escribí las tres preguntas de diagnóstico con la respuesta esperada de cada una. Entregable: `fine-tuning-o-no.md`.

### Módulo 5 — Qué corre debajo y cuánto cuesta (1:50:29 - 2:17:42)

**Objetivo:** entender el hardware y el costo como decisiones de producto.

- **El alfabeto de chips.** GPU: muchos cores para matemática en paralelo. TPU (Google): acelerador construido alrededor del grid math, con unidades que pasan resultados en cadena y poca lógica de decisión (1:53:38). NPU: no es una GPU chica; corre tareas de IA chicas con muy poca energía, con menor precisión (1:54:20). DPU: networking, storage y seguridad.
- **CUDA es un foso competitivo, no una librería.** La jerarquía threads → blocks → grid permite que el mismo código corra en una GPU de laptop o en una de datacenter: "So the same code can spread across a small GPU in a laptop or a huge one in a data center. It doesn't need to" (1:57:45).
- **Entrenamiento vs. inferencia.** Entrenamiento: forward, backward y update, batches enormes, mucha memoria, y varias GPUs que tienen que hablar constantemente (1:02:00). Inferencia: **prefill** (lee todo el prompt en paralelo, pesado de cómputo) y **decode** (escribe un token por vez, limitado por **memory bandwidth** más que por cómputo) (2:02:18-2:03:04).
- **El KV cache** guarda resultados intermedios para no recalcular y crece con el largo del prompt y de la respuesta (2:03:20) — de ahí sale el prompt caching.
- **Un montón de GPUs no es un cloud.** Los proveedores se diferencian por el software y las operaciones alrededor del chip: provisioning sin manos, aislamiento entre clientes, no dejar GPU ociosa (slices, compartir en el tiempo), medición para facturar, y recuperación automática (2:08:03-2:09:16). Tres tipos: cloud generalista, NeoCloud y capacidad cruda.
- **Prompt caching: por qué funciona.** Prefill arma el KV cache; para el mismo texto inicial el resultado es idéntico, así que se guarda y se reusa (2:11:39). Requiere orden: instrucciones y tool descriptions estables primero, mensaje del cliente al final.
- **Las otras palancas:** cortar tokens (instrucciones muertas, tool results viejos, menos pasajes), routing a modelos más chicos, y cuidar que menos tokens no baje la calidad — lost in the middle otra vez.

**Preguntas de estudio:**
- ¿Por qué decode está limitado por memoria y no por cómputo?
- ¿Qué tiene que ser verdad para que el prompt caching ahorre de verdad?
- ¿Qué diferencia operativa hay entre un NeoCloud y comprar capacidad cruda?

**Ejercicio:** dado tu sistema, listá qué parte del prompt es estable (cacheable) y qué parte cambia por request. Reordená el prompt en consecuencia. Entregable: `presupuesto-tokens.md`.

### Módulo 6 — Cómo sabés que funciona, y sigue funcionando (2:17:42 - 2:53:54)

**Objetivo:** llevar el sistema a producción con evaluación, seguridad y plataforma.

- **SDLC → AIDLC, por cuatro diferencias concretas.** (1) Se versiona y revisa más que código: prompts, retrieval settings, datasets, versiones de modelo y adapters (2:19:46). (2) Los datos son parte del sistema, no preparación previa: "Data work isn't prep before the real work. For AI systems, it's a large share of the real work" (2:20:42). (3) El testing deja de ser binario: una respuesta puede ser plausible y estar mal. (4) La calidad se mide estadísticamente y el sistema cambia sin que nadie toque código.
- **MLOps y LLMOps.** MLOps versiona código, datos y modelo juntos, y agrega detección de drift. LLMOps es la versión cuando no entrenás el modelo: elegís uno, le das forma, y lo que más revisás son prompts y retrieval (2:24:15).
- **El trace como columna vertebral de operaciones.** Responde siete preguntas sobre una sola request: qué vio el modelo, qué decidió, qué herramientas llamó, qué volvió, cuánto tardó, cuánto costó y qué se hizo con la respuesta.
- **Evals con golden dataset.** "The heart of an eval system is a golden data set" (2:28:58): tickets reales, con los casos difíciles incluidos a propósito, etiquetados por gente que conoce la política, y con acuerdo entre etiquetadores en los casos importantes. "A data set of easy tickets will give you a high score and false confidence" (2:29:12).
- **Las siete razones del fracaso post-piloto** (2:32:55-2:36:25), y ninguna es el modelo:
  1. **Los datos no significan lo mismo** entre sistemas (un return cuenta al volver el ítem o al pagar el reembolso). "It gives confident wrong answers and a better model would give the same wrong answers" (2:34:05).
  2. **Nadie sabe describir el trabajo:** el conocimiento vive en la cabeza de la support lead.
  3. **Se automatiza un proceso roto**, y va más rápido.
  4. **El hueco entre demo y producto** (permisos, testing, monitoreo, concurrencia, plan de fallos).
  5. **Costo oculto:** el precio por call no es el costo por ticket resuelto.
  6. **Sin medida de éxito** acordada antes de empezar.
  7. **Personas y roles:** hace falta quien traduzca negocio ↔ IA.
- **Red teaming ≠ testing.** "A test checks that the system does what it should. Red teaming acts like an attacker and tries to make the system do what it shouldn't" (2:38:02). Dos riesgos: seguridad (robo de datos, acciones no autorizadas) y seguridad de contenido. Y el criterio de calidad: "Then ask whether the defense lives in the prompt or in the system" (2:42:28). Cada fix se convierte en test permanente.
- **Platform engineering:** si tres equipos construyen lo mismo (gateway, loop, tools, KB, evals, traces) la empresa lo paga tres veces y junta tres sets de errores; la plataforma da caminos asfaltados.
- **La anatomía end-to-end** (2:47:06): aplicación → control loop → AI gateway → modelo en aceleradores → tools/MCP, retrieval, knowledge graph, memoria → capa de seguridad (guardrails, permisos, aprobación humana) → capa de observación (traces, evals, dashboards) → plataforma (pipelines, prompts versionados, eval gate). El trace de una request cuenta la historia completa: presupuesto, cache, lookup de orden, retrieval de política, disputa entre documento viejo y nuevo, decisión y aprobación.

**Preguntas de estudio:**
- ¿Por qué "el modelo es raramente la razón" es la conclusión de todo el módulo, y no una excusa?
- ¿Qué diferencia un eval de un test unitario, en una frase?
- ¿Cuándo una defensa que vive en el prompt es suficiente y cuándo es teatro?

**Ejercicio de cierre:** dibujá la anatomía de tu propio sistema con las siete capas del módulo. Marcá qué capa no existe todavía. Entregable: `anatomia-mi-sistema.md`.

## Banco de preguntas

1. Un agente y un chatbot reciben el mismo mensaje. ¿Qué evidencia observable distingue al agente?
2. ¿Por qué el número de modelos que llama un agente no determina cuántos agentes hay?
3. Nombrá dos costos reales de pasar de un agente a varios, además del dinero.
4. ¿Qué hace el control loop cuando una acción es irreversible?
5. ¿Por qué una descripción de herramienta vaga es un bug de producto?
6. ¿Qué problema resuelve MCP que tool calling a mano no resuelve?
7. Una skill y un servidor MCP: ¿cuándo uno, cuándo el otro, cuándo ninguno?
8. ¿Qué agrega un AI gateway a un API gateway? Nombrá tres controles.
9. El agente responde con una política que ya no rige. Nombrá las tres primeras cosas que revisás, en orden.
10. ¿Qué fallo arregla exactamente el hybrid retrieval y qué fallo no arregla?
11. Diferenciá knowledge graph, GraphRAG y graph engineering en una línea cada uno.
12. ¿Por qué el borrado de un documento es un paso de ingeniería y no una operación de archivo?
13. Un equipo pide fine-tuning para que el agente conozca la política nueva de reembolsos. ¿Qué les respondés?
14. LoRA: ¿qué se congela y por qué eso importa para la evaluación?
15. ¿Qué copia un modelo destilado de su teacher?
16. Un reward único de "satisfacción del cliente" sobre un agente de reembolsos. ¿Cuál es el atajo que aprende?
17. Prefill y decode: ¿cuál de los dos está limitado por memoria y por qué?
18. ¿Por qué el prompt caching exige un orden estable del prompt?
19. Nombrá las siete razones de fracaso post-piloto que da el ponente, sin mirar.
20. Red teaming: ¿por qué cada fix tiene que convertirse en test permanente?
21. ¿Qué significa que la defensa viva "en el sistema, no en el prompt"?

## Notas editoriales

- **El curso no nombra al expositor**, ni en el video ni en la descripción. No se le atribuye una identidad que la fuente no da.
- **Duración:** 2:53:54 según el reproductor (10.434 s); el último bloque del ASR cierra en 2:53:41 porque YouTube no subtitula el final.
- **Cloud X Berry** es la tienda ficticia del caso, no un cliente real; el canal es Cloud X Berry.
- **«AILC» en el ASR es AIDLC.** El propio cue aclara el nombre: "Some teams call this an AI development life cycle" (2:19:33).
- **«Laura» es LoRA** en todos los cues; el único lugar donde el ASR lo dice bien es al expandir el acrónimo: "The name stands for low rank adaptation" (1:35:03).
- **El Módulo 3 usa «GraphRAG» de forma laxa**, y el ponente lo dice: conviene preguntarle a cada equipo qué entiende por el término. El outline respeta esa ambigüedad en vez de resolverla por su cuenta.
- **Citas verificadas:** cada cita textual del outline se corrió contra `transcripcion.md` con el chequeo de timestamps; las frases partidas entre cues se recortaron a un fragmento contenido en uno solo.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
