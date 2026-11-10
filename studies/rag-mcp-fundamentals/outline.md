# Clase: RAG & MCP Fundamentals – A Hands-On Crash Course

- Fuente: https://www.youtube.com/watch?v=I7_WXKhyGms
- Canal: freeCodeCamp.org
- Expositor: no nombrado en el video ni en la descripción
- Duración: 1:39:53
- Publicado: 2026-01-22
- Idioma: inglés (subtítulos automáticos, glosario de ASR en `transcripcion.md`)
- Capítulos: los 27 + 12 oficiales de la descripción, alineados 1:1 con los módulos

## Resultado esperado

Al terminar la clase deberías poder:

1. Explicar RAG sin jerga y decidir cuándo corresponde **prompt engineering, fine-tuning o RAG**, y por qué.
2. Implementar búsqueda por keywords (TF-IDF y BM25) y explicar en qué falla.
3. Implementar búsqueda semántica con embeddings: qué es un vector, qué mide el **dot product** y cómo se interpretan los scores.
4. Elegir entre modelo de embedding local y de API, y dimensionar el costo de comparar contra un corpus completo.
5. Usar una **vector DB** (Chroma, Pinecone) y entender qué hacen HNSW, IVF y LSH por debajo.
6. Diagnosticar el **precision problem** y diseñar una estrategia de chunking con tamaño, overlap y reglas de corte.
7. Armar el pipeline RAG completo (ingesta → chunk → embed → store → retrieve → augment → generate) y nombrar qué es offline y qué es online.
8. Poner un RAG en producción: qué cachear en cada capa, qué métricas mirar, qué umbral alerta y cómo degradar sin romper.
9. Explicar por qué existe **MCP**, qué es un agente y por qué la estandarización de tools resuelve el problema N×M de integraciones.
10. Describir la arquitectura MCP (cliente/servidor, local vs remoto), y los tres componentes del servidor (**resources, tools, prompts**) y los tres del cliente (**roots, sampling, elicitation**).
11. Construir un servidor MCP con FastMCP, probarlo con el **MCP Inspector** y escribir un cliente que lo consuma.

## Mapa temporal

| Tiempo | Bloque |
|---|---|
| 00:00 - 00:52 | Overview: qué cubre el curso y cómo funcionan los labs |
| 00:52 - 01:50 | Explicación mínima de RAG (el ejemplo del policy document) |
| 01:50 - 02:41 | Caso real: el policy copilot |
| 02:41 - 04:12 | Retrieval, augmenting y generation; qué sistema se espera |
| 04:12 - 06:40 | Cuándo usar prompt engineering, fine-tuning o RAG |
| 06:40 - 08:15 | Voz y estilo con fine-tuning, y sus límites |
| 08:15 - 09:36 | Por qué RAG gana en información factual dinámica |
| 09:36 - 13:12 | Keyword search: TF-IDF y BM25 |
| 13:12 - 16:10 | Lab 1: búsqueda por keywords y sus límites |
| 16:10 - 18:01 | Búsqueda semántica: buscar por significado |
| 18:01 - 20:04 | Modelos de embedding: tamaño y local vs API |
| 20:04 - 22:00 | Cómo un texto se convierte en vector |
| 22:00 - 27:08 | Similitud vectorial y dot product |
| 27:08 - 30:54 | Lab 2: búsqueda semántica con embeddings |
| 30:54 - 32:15 | Vector DBs: Chroma y Pinecone |
| 32:15 - 35:53 | Índices: HNSW, IVF y LSH |
| 35:53 - 39:21 | Lab 3: inicializar y consultar una vector DB |
| 39:21 - 41:40 | El precision problem: por qué chunkear |
| 41:40 - 44:28 | Estrategias de chunking: tamaño, overlap, fronteras |
| 44:28 - 48:49 | Lab 4: chunking y retrieval optimizado |
| 48:49 - 50:40 | El pipeline RAG completo |
| 50:40 - 52:54 | Lab 5: pipeline RAG end-to-end |
| 52:54 - 54:00 | Producción: caché, monitoreo, errores |
| 54:00 - 56:51 | Estrategias de caché: query, embedding, búsqueda, LLM |
| 56:51 - 57:39 | Métricas propias de un RAG |
| 57:39 - 59:40 | Arquitectura de producción en Kubernetes y cierre de la Parte 1 |
| 59:40 - 1:00:59 | Introducción a MCP |
| 1:00:59 - 1:06:15 | El rol de los agentes en sistemas orientados a la acción |
| 1:06:15 - 1:08:00 | Por qué hacen falta tools estandarizadas |
| 1:08:00 - 1:10:12 | Arquitectura MCP: clientes, servidores, local vs remoto |
| 1:10:12 - 1:12:40 | Lab 6: preparar el entorno del asistente |
| 1:12:40 - 1:14:13 | Resources, tools y prompts |
| 1:14:13 - 1:22:55 | Especificación MCP y JSON-RPC |
| 1:22:55 - 1:26:22 | Lab 7: usar un servidor MCP existente |
| 1:26:22 - 1:29:12 | Construir un servidor propio con el SDK de Python |
| 1:29:12 - 1:29:45 | Probar con el MCP Inspector |
| 1:29:45 - 1:35:29 | Lab 8: desarrollar resources, tools y prompts |
| 1:35:29 - 1:39:40 | Construir un cliente MCP: roots, sampling, elicitation |

## Módulos

### Parte 1: Retrieval Augmented Generation (RAG)

### Módulo 1 - Course Overview: Building Integrated AI Systems (00:00 - 00:52)

**Objetivo:** saber qué se va a construir y qué no requiere saber de antemano.

- Tesis del curso: construir **sistemas integrados**, no herramientas sueltas. RAG para el conocimiento, MCP para la coordinación a nivel sistema.
- Claim de audiencia: "No background knowledge in AI or AI models or coding or programming required" (00:42).
- Los laboratorios abren en el navegador y no requieren entorno propio (01:26). Son el mecanismo de práctica: cinco labs para RAG, tres para MCP.

**Ejercicio:** escribir en tres líneas el sistema propio que justificaría RAG (qué documento privado, qué pregunta) y el que justificaría MCP (qué acción externa). Entregable: `mi-sistema.md`.

### Módulo 2 - The Simplest Explanation of RAG (00:52 - 01:50)

**Objetivo:** entender RAG con el ejemplo manual antes de automatizarlo.

- El problema: un LLM no tiene acceso al documento privado y "would hallucinate and provide an incorrect or generic answer" (01:56, cue anterior al capítulo).
- La solución manual: buscar la sección, pegarla en el prompt, pedirle que la use.
- **Definición operativa:** retrieval = buscar la información; augmenting = mejorar el prompt con ella; generation = el LLM responde sobre ese prompt aumentado (02:50-03:05).

**Ejercicio:** repetir el ejemplo a mano con un documento propio de dos páginas y registrar qué parte del trabajo hizo cada etapa. Entregable: tabla de tres filas (retrieval / augment / generate).

### Módulo 3 - Real-world Use Case: Internal Policy Chatbot (01:50 - 02:41)

**Objetivo:** fijar el caso que recorre todo el curso.

- El sistema se llama **policy copilot** y debe responder preguntas sobre políticas internas recuperando de los documentos y generando la respuesta.
- El usuario no busca: pregunta. El sistema hace el lookup (03:18-03:48).

**Ejercicio:** listar tres preguntas de tu dominio donde el usuario hoy "pega el documento en el chat" a mano. Entregable: `casos.md`.

### Módulo 4 - Understanding Retrieval, Augmenting, and Generation (02:41 - 04:12)

**Objetivo:** separar las tres etapas como piezas independientes y verificables.

- El pipeline esperado se enuncia como una cadena: el sistema recupera, aumenta y genera (03:48).
- Marca el error de framing del curso: RAG no reemplaza todo, es una técnica entre varias (se desarrolla en el módulo 5).

**Ejercicio:** dado un error del sistema (respuesta vaga o respuesta equivocada), clasificar en qué etapa falla: retrieval, augment o generate. Entregable: tres diagnósticos escritos.

### Módulo 5 - When to use Prompt Engineering, Fine-Tuning, or RAG (04:12 - 06:40)

**Objetivo:** elegir la herramienta por tipo de problema, no por moda.

- Regla dura: "Rack is not the solution to all problems" (04:03).
- El caso del *policy copilot* se descompone en tres problemas con tres soluciones:
  - **Restricciones y seguridad** (qué debe y no debe revelar, redirigir a HR): "best practices are a good solution to this" (06:23).
  - **Voz y estilo** del CEO escocés: fine-tuning sobre sus discursos, emails, blog posts y videos (07:08).
  - **Información factual dinámica**: RAG.

**Ejercicio:** para tu propio caso, escribir qué parte se resuelve con instrucciones, qué parte con estilo y qué parte con datos. Entregable: `decision.md` con tres columnas.

### Módulo 6 - Solving Voice and Style with Fine-Tuning (06:40 - 08:15)

**Objetivo:** entender qué hace bien el fine-tuning y por qué no resuelve el conocimiento.

- Fine-tuning: "Fine-tuning is the process where you provide a model hundreds of sample" (07:08).
- Límites enumerados por el ponente (07:39-07:55): las políticas cambian y hay que reentrenar; el entrenamiento es caro y lento; no hay citas posibles; más data de entrenamiento no significa más precisión; **knowledge cutoff**.
- Conclusión: "Fine-tuning is great for stable unchanging patterns like communication style, but terrible for dynamic factual information" (07:55).

**Ejercicio:** escribir una lista de cinco rasgos de estilo que no cambiarían en años (candidatos a fine-tuning) y cinco hechos que cambian todos los meses (candidatos a RAG). Entregable: `estilo-vs-hechos.md`.

### Módulo 7 - Why RAG is Best for Dynamic Factual Information (08:15 - 09:36)

**Objetivo:** justificar RAG por tiempo de recuperación, no por moda.

- Argumento central: RAG recupera "at query time, not at training time" (08:10).
- El retrieval empieza por identificar keywords en la pregunta: en el ejemplo, *reimbursement* y *home office* (08:55).
- Se anticipa el motor de todo lo que sigue: búsqueda por coincidencia exacta.

**Ejercicio:** escribir por qué, para tu caso, actualizar el índice es más barato que reentrenar. Entregable: tres líneas, con la operación concreta que cambia.

### Módulo 8 - Keyword Search Techniques: TF-IDF and BM25 (09:36 - 13:12)

**Objetivo:** implementar el baseline de recuperación y conocer su punto de falla.

- Mecánica de keyword search: contar ocurrencias y rankear por frecuencia entre documentos (09:53-10:07).
- La versión ingenua (grep o query SQL) sólo devuelve coincidencias exactas: "the chances of getting accurate information every time is low" (09:24).
- **TF-IDF:** `TfidfVectorizer` de scikit-learn; `fit_transform` da una matriz término×documento; "The word office appears in all sentences, so they get a score of 0.4" (11:06). La consulta se resuelve con `transform` y devuelve score por documento.
- **BM25:** `rank_bm25`; indexa y puntúa con `get_scores`. Diferencia observada: "The word office gets a score of zero because the BM25 algorithm is a bit more strict in assigning scores" (12:17) — penaliza términos presentes en todos los documentos.
- Detalle técnico: el lab usa además **cosine similarity** sobre los vectores TF-IDF (14:45) y menciona un enfoque híbrido TF/BM25 con pesos (15:58), que deja como exploración.

**Ejercicio:** correr TF-IDF y BM25 sobre tres documentos propios y comparar el ranking del mismo query. Entregable: tabla con los scores de ambos motores y una frase explicando la diferencia.

### Módulo 9 - Hands-on Lab 1: Basic Search and Keyword Limitations (13:12 - 16:10)

**Objetivo:** ver con scores reales dónde se rompe el keyword search.

- Setup: portal de preguntas a la izquierda, VS Code + terminal a la derecha; es un Linux real (13:31).
- Tareas: contar documentos del *employee handbook* (tres), correr `grep` sobre "holiday" y guardar en `extracted content` (14:00), explorar el script TF y el de BM25.
- Resultado que importa: la consulta *pet policy* devuelve `pet policy.md` con "a score of 0.4676 whereas the other files have a score less than 0.1" (15:15). Es el número que se pide como verificación.

**Ejercicio:** reproducir el lab con tus documentos: mismo query, dos motores, un resultado donde el ranking falle. Entregable: `lab1.md` con la evidencia.

### Módulo 10 - Introduction to Semantic Search and Meaning (16:10 - 18:01)

**Objetivo:** entender qué problema nuevo resuelve buscar por significado.

- Punto de falla del keyword search: una variante en la pregunta mata el resultado; sin el término exacto el documento no aparece (16:13). El ejemplo: *allowance* en lugar de *reimbursement*, *work from home* en lugar de *home office*.
- Semantic search convierte query y documentos a vectores y busca cercanía: "Documents with similar meanings end up close together in this space" (17:28).
- La intuición: *reimbursement* y *allowance* quedan cerca aunque sean palabras distintas (17:43).

**Ejercicio:** escribir cinco pares de términos que significan lo mismo en tu dominio y que un buscador de keywords perdería. Entregable: `sinonimos.md`.

### Módulo 11 - Embedding Models: Parameter Size and Local vs. API Models (18:01 - 20:04)

**Objetivo:** elegir un modelo de embedding con criterio de tamaño y despliegue.

- Modelo de referencia: `all-MiniLM-L6-v2`, "maps sentences and paragraphs to a 384dimensional dense vector space" y es de 22 millones de parámetros (18:25-18:40).
- Qué significa un parámetro: un valor aprendido durante el entrenamiento (18:53).
- Comparación de escala: 22M contra 175B de GPT-3.5 y 1.8T de GPT-4 (19:22); tamaño en disco: ~90 MB contra 350 GB y 3.6 TB (19:38). La implicación práctica es local vs remoto, no calidad.
- Modelos locales: corren en tu máquina, gratis, sin internet (26:19). Modelos de API: `text-embedding-3-small` de OpenAI, se paga por uso y requiere red (26:32-26:47).
- Referencia de comparación: el leaderboard de embeddings de Hugging Face (26:47).

**Ejercicio:** elegir el modelo de embedding para tu caso y justificar con tres criterios (tamaño, privacidad, costo por volumen). Entregable: `modelo-embedding.md`.

### Módulo 12 - How Embeddings Convert Text into Mathematical Vectors (20:04 - 22:00)

**Objetivo:** desarmar la caja negra del embedding.

- Definición: "An embedding model takes text and converts it into numbers that represent meaning" (20:04).
- El modelo no mira palabras, mira aspectos de significado: animal, workplace, permisos (20:18-20:34).
- La visualización en dos dimensiones explica la idea pero no el caso real: el modelo usa 384 dimensiones y "we don't even know how to imagine this or plot that on a graph" (21:48).

**Ejercicio:** escribir con tus palabras por qué "dibujar los vectores" no es una explicación válida para 384 dimensiones. Entregable: un párrafo.

### Módulo 13 - Vector Similarity and the Dot Product (22:00 - 27:08)

**Objetivo:** medir similitud sin poder verla.

- Herramienta: el **dot product** como regla que funciona en cualquier cantidad de dimensiones (22:02).
- El procedimiento paso a paso con vectores 2D: multiplicar componente a componente, sumar, normalizar a 0-1 (22:46-23:26).
- Lectura del score: "the pair with the value closest to one are similar and away from one are dissimilar" (23:26).
- Implementación: `sentence-transformers` + `numpy`, con `np.dot` sobre los embeddings (24:24-24:52).
- Resultados del ejemplo: *dogs* vs *pets* 73.3%, *dogs* vs *remote* 36.2%, *pets* vs *remote* 33.8% (25:06-25:20). La conclusión: el modelo distingue temas, no palabras (25:35).

**Ejercicio:** correr el mismo experimento con tres frases propias y predecir el ranking antes de ejecutar; comparar. Entregable: `dot-product.md` con predicción y resultado.

### Módulo 14 - Hands-on Lab 2: Implementing Semantic Search with Embedding Models (27:08 - 30:54)

**Objetivo:** ver el mismo corpus fallar y funcionar según el motor.

- Query del lab: *distributed workforce policies*. Con keyword search "most of the scores are zero" (28:32); con embeddings el script identifica el documento correcto (29:52).
- Score que se pide reportar: 0.3982 entre *remote work policy* y *distributed work policies* (30:09-30:22).
- Pregunta conceptual del lab: qué enfoque entiende mejor el significado del query. Respuesta: semantic search (30:39).

**Ejercicio:** replicar el contraste keyword vs semántico sobre un corpus propio y registrar el score del resultado correcto. Entregable: `lab2.md`.

### Módulo 15 - Scaling with Vector Databases: Chroma and Pinecone (30:54 - 32:15)

**Objetivo:** entender por qué no alcanza con comparar contra todo.

- El costo: 500 documentos × 384 dimensiones = 192.000 operaciones por query, "like searching through a phone book page by page" (31:36).
- La vector DB aporta recuperación inmediata, uso eficiente de recursos y escalabilidad mediante índices (32:06).
- **Chroma:** open source, Python-friendly, free, ideal para aprender y experimentar (33:21).
- **Pinecone:** servicio gestionado, se paga por uso, usado en producción (33:37).
- Recomendación del ponente: empezar con Chroma y migrar a Pinecone para producción (34:07).

**Ejercicio:** calcular el costo de comparación exhaustiva para tu corpus (documentos × dimensiones) y decidir si necesitás índice. Entregable: la cuenta y la decisión.

### Módulo 16 - Indexing Algorithms: HNSW, IVF, and LSH (32:15 - 35:53)

**Objetivo:** saber qué hace un índice vectorial por dentro.

- Idea: pre-organizar vectores en vecindarios, así "we don't search the entire space" (32:36).
- **HNSW** (hierarchical navigable small world): grafo donde cada vector se conecta a sus vecinos más similares; la búsqueda arranca en un punto y sigue conexiones; "It's fast and accurate, which is why most vector databases use it by default" (33:07).
- **IVF** (inverted file) y **LSH** (locality-sensitive hashing) se mencionan como variantes, sin desarrollo (33:21).

**Ejercicio:** explicar en tres frases por qué HNSW no garantiza el vecino exacto y por qué igual sirve. Entregable: `indices.md`.

### Módulo 17 - Hands-on Lab 3: Initializing and Querying a Vector Database (35:53 - 39:21)

**Objetivo:** usar Chroma de verdad, incluido su default peligroso.

- Flujo del script: importar Chroma, crear cliente, crear colección `policies`/`techp docs`, cargar el modelo `all-MiniLM`, agregar documentos, consultar con `collection.query` (34:07-34:37).
- **Gotcha crítico:** "the default behavior of Chromadb is that it's not persistent. When you create a client with just chromadb.client, client, it stores everything in memory" (34:51). Para persistir hay que usar `PersistentClient` con un path (35:05).
- Se puede reemplazar el embedding por defecto, incluso por el de OpenAI, pasando `embedding_function` y la API key (35:34).

**Ejercicio:** montar Chroma con `PersistentClient`, reiniciar el proceso y verificar que los documentos siguen. Entregable: `lab3.md` con el conteo antes y después del reinicio.

### Módulo 18 - The Precision Problem: Why Document Chunking is Essential (39:21 - 41:40)

**Objetivo:** ver el problema que introduce un documento grande.

- Escenario: un handbook de 50 páginas como **una sola entrada** en la vector DB (39:43).
- Resultado: técnicamente funciona, pero ante "what's the remote work policy" devuelve el handbook entero (39:56).
- Nombre del problema: "This is what I call the precision problem" (40:12). Con chunking, la respuesta trae sólo las secciones relevantes (40:24).

**Ejercicio:** meter un documento largo sin chunking, hacer un query puntual y medir qué porcentaje de la respuesta es irrelevante. Entregable: `precision-problem.md`.

### Módulo 19 - Chunking Strategies: Fixed-size, Overlap, and Boundary Rules (41:40 - 44:28)

**Objetivo:** elegir una estrategia de chunking con parámetros justificados.

- **Fixed size:** 500 caracteres por chunk, simple y confiable (40:38-40:53).
- El defecto: corta en mitad de una oración; "dogs are allowed" en un chunk y "on Fridays" en otro (41:07).
- **Overlap:** 50 caracteres de solape para preservar el contexto de la frontera (41:20).
- Otras estrategias: por oración, por párrafo; el video deja afuera semantic chunking y agentic chunking (42:32).
- **Principios que da el ponente** (43:30-44:12): 200-500 caracteres por chunk; 50-100 de overlap; cortar en oraciones; no cortar palabras; preservar párrafos; y sobre todo **probar con queries reales** y ajustar.
- Advertencia del trade-off: chunks chicos pierden contexto, chunks grandes pierden precisión (42:03-42:16).

**Ejercicio:** correr la misma query con dos tamaños de chunk y dos overlaps; quedarse con el que responde mejor la pregunta real. Entregable: matriz 2×2 con resultados.

### Módulo 20 - Hands-on Lab 4: Document Chunking and Optimized Retrieval (44:28 - 48:49)

**Objetivo:** usar las herramientas estándar en lugar de escribir tu propio splitter.

- El script `chunking problem demo` muestra el caso sin chunking: devuelve el documento entero truncado (45:39).
- Herramientas: **LangChain** con `RecursiveCharacterTextSplitter` (chunk size 200, overlap 50, separadores definidos) (47:09-47:24) y **spaCy** para chunking por oración (46:39).
- Cierre del lab: `chunked search` compara una colección con chunking contra una sin chunking (48:11).

**Ejercicio:** reproducir la comparación con y sin chunking y anotar diferencias en longitud de la respuesta y pertinencia. Entregable: `lab4.md`.

### Módulo 21 - Bringing it All Together: The RAG Pipeline (48:49 - 50:40)

**Objetivo:** dibujar el pipeline completo con la frontera offline/online en el lugar correcto.

- Todo el trabajo pesado —cargar documentos, chunkear, embeber, guardar en la DB, indexar— ocurre **antes** de que el usuario pregunte: eso es el `rag pipeline` (49:38).
- Parámetros concretos del ejemplo: chunk de 500 con overlap de 50, embeddings de OpenAI, carga a vector DB (50:06).
- En consulta: recuperar chunks, aumentar el prompt con ellos, generar (50:19).

**Ejercicio:** dibujar tu pipeline marcando qué corre offline y qué corre por query. Entregable: diagrama + lista de componentes.

### Módulo 22 - Hands-on Lab 5: Building a Complete End-to-End RAG Pipeline (50:40 - 52:54)

**Objetivo:** ver el pipeline entero en un solo script legible por secciones.

- Secciones del script: carga y chunking; setup de Chroma y almacenamiento de chunks; procesamiento del query; búsqueda; context augmentation; generate response; función `rag pipeline` que compone todo (51:32-52:30).

**Ejercicio:** escribir tu propio pipeline mínimo en un archivo, con las funciones separadas igual que el demo. Entregable: `rag_pipeline.py` + salida de una consulta.

### Módulo 23 - Production Concerns: Caching, Monitoring, and Error Handling (52:54 - 54:00)

**Objetivo:** reconocer los tres problemas de producción antes de tenerlos.

- RAG es lento por diseño: cada query genera embeddings, busca en la DB y llama al LLM; "a single query can take nearly a second" (53:14).
- La palanca: "Most queries are repeated or are very similar" (53:14).
- La cifra del ponente: de 950 milisegundos a 5 milisegundos, "190 times faster" (53:29-53:42). *(El ASR pierde la palabra "milliseconds" en la segunda cifra; 950/5 = 190.)*
- Tres frentes: caching para velocidad, monitoring para visibilidad, error handling para que no se caiga (52:44-53:00).

**Ejercicio:** medir el tiempo de una query propia en frío y en caliente (misma pregunta dos veces). Entregable: dos tiempos y la diferencia.

### Módulo 24 - Implementation Strategies for Query, Embedding, and LLM Caching (54:00 - 56:51)

**Objetivo:** cachear en la capa correcta.

- Cuatro caches, cada uno contra un cuello de botella distinto (53:56):
  - **Query cache:** pares pregunta-respuesta completos; ideal para FAQs (54:03).
  - **Embedding cache:** vectores ya calculados, útil cuando el mismo texto aparece en varias búsquedas (54:15).
  - **Vector search cache:** resultados de la DB; "Remote work and working from home might return identical chunks" (54:26).
  - **LLM response cache:** la operación más cara y la más valiosa (54:42).
- Implementación: Redis; la clave es un **hash del query más el contexto** (55:11).
- **TTL:** lo justo para ganar performance sin servir datos viejos; documentos estables toleran TTL largo, contenido dinámico exige TTL corto (55:24-55:40).

**Ejercicio:** elegir dos de los cuatro caches para tu caso y definir su clave y su TTL. Entregable: `caches.md`.

### Módulo 25 - Essential Metrics for Tracking RAG Performance (56:51 - 57:39)

**Objetivo:** medir lo que importa en un RAG, no sólo lo que importa en cualquier API.

- Métricas genéricas: response time, throughput, error rate (55:55).
- Métricas propias del RAG: **retrieval quality** (relevancia de los chunks devueltos), **embedding performance** (tiempo de generar vectores) y **chunking efficiency** (56:10).
- Umbrales citados: respuesta mayor a 2 segundos es problema de performance; error rate por encima de 5% es problema de sistema (56:25).
- Regla sana: "the key is to set realistic thresholds based on" datos reales, no targets teóricos (56:25), para evitar alert fatigue (56:40).

**Ejercicio:** definir un umbral de latencia y otro de error rate para tu caso, justificados con una medición propia. Entregable: `slo.md`.

### Módulo 26 - Production Architecture: Microservices on Kubernetes (57:39 - 59:40)

**Objetivo:** entender qué se separa cuando el sistema crece.

- La caída no se evita, se absorbe: bases de datos caídas, servicios de LLM no disponibles, timeouts de red (56:40). El objetivo es **graceful degradation**: que el usuario reciba alguna respuesta (56:56).
- **Fallback en cascada** (57:10): pipeline completo → búsqueda por keywords → devolver chunks crudos → matching de texto simple → mensaje de error útil.
- El patrón del circuito: probar periódicamente si el servicio volvió —el estado **half-open**— y cerrar el circuito si responde (57:24).
- Arquitectura en capas (57:54-58:38): **data** (Chroma, Redis, PostgreSQL), **rag pipeline** como microservicios (query processing, chunking, embedding, generation, retrieval, augmentation) que escalan por separado, **application** (web, mobile, admin) y **monitoring** (Prometheus, Grafana, Jaeger, ELK).
- Cierre honesto: quedan afuera multimodal RAG, graph RAG, hybrid search, federated RAG, reranking, query expansion y context compression (59:06).

**Ejercicio:** escribir el fallback de tres pasos para tu sistema, de mejor a peor respuesta aceptable. Entregable: `fallback.md`.

### Parte 2: Model Context Protocol (MCP)

### Módulo 27 - Introduction to Model Context Protocol (MCP) (59:40 - 60:59)

**Objetivo:** entrar a MCP con una pregunta concreta, no con una definición.

- Promesa del segmento: "This is a crisp, nononsense, no BS hands-on" (59:35).
- Recorrido: por qué hace falta, qué es, la arquitectura, usar un server existente, construir server y client (60:05).

**Ejercicio:** anotar tres integraciones que hoy hacés a mano con APIs y que te gustaría exponer como tools. Entregable: `integraciones.md`.

### Módulo 28 - The Role of AI Agents in Action-Oriented Systems (60:59 - 66:15)

**Objetivo:** entender qué agrega un agente sobre un LLM suelto.

- Límite del LLM: "it can't perform any action on its own" (1:00:47).
- El caso vuelo: buscar en terceros, comparar contra preferencias (barato/caro, asiento, comida), decidir, reservar y avisar (61:01-61:16).
- Definición operativa de agente: interactúa con tools de terceros, tiene memoria, conversa con el LLM y **itera** hasta completar la tarea (62:01).
- Analogía del ponente: un agente es "except now it can think" (1:03:43). Lo que antes era lógica escrita a mano en Zapier o en scripts de Python ahora lo decide el LLM: qué ruta tomar, cuántas veces iterar, qué tool usar, cuándo el objetivo está cumplido (63:13-63:43).
- Workflow típico: el agente pide al LLM interpretar el input, elegir las tools, buscar datos, leer preferencias, decidir y actuar (63:43-64:43).
- Aclaración honesta: el código mostrado es **pseudo código** (65:54).

**Ejercicio:** escribir el loop de tu propio agente en seis pasos, marcando dónde decide el LLM y dónde no. Entregable: `agente-loop.md`.

### Módulo 29 - Why We Need Standardized Tools for Third-Party Interactions (66:15 - 68:00)

**Objetivo:** ver el problema N×M que MCP viene a resolver.

- Un agente accede a terceros **a través de tools** (66:09).
- El problema real no es tener tools: es que cada tercero es distinto. Los ejemplos del ponente (66:51): `API/flights`, `flights list`, `list flights`, con respuestas también distintas.
- Con millones de sitios, escribir todos esos conectores a mano no escala (67:06).
- MCP como respuesta: "Think of MCPS as a guide for the AIS to choose the right" (1:07:21).

**Ejercicio:** estimar cuántos conectores implicaría tu caso con N fuentes y M consumidores, y cuántos con un protocolo común. Entregable: la cuenta.

### Módulo 30 - MCP Architecture: Clients, Servers, and Local vs. Remote Hosting (68:00 - 70:12)

**Objetivo:** ubicar cada pieza antes de tocar código.

- Arquitectura cliente-servidor: el agente usa el MCP **client** para hablar con el **server** (67:51).
- Los clientes ya vienen embebidos en herramientas conocidas: Cursor, Windsurf, Claude Code, Claude Desktop (67:51-68:04).
- Casos de uso citados: acceso a un MongoDB local; logs de consola y HTML del navegador para depurar front-end (68:34); acceso **read-only** a Stripe, BigQuery y Data Studio para investigar datos faltantes o transacciones (68:48).
- Quién construye servidores: cualquiera que conozca la API; los vendors publican los oficiales y la comunidad los propios, "at your own risk" sin garantía de que estén testeados o al día (69:01-69:32).

**Ejercicio:** mapear qué servidores MCP usarías (oficiales vs comunitarios) y qué riesgo implica cada comunitario. Entregable: tabla fuente → tipo → riesgo.

### Módulo 31 - Hands-on Lab 6: Setting up the AI Assistant Environment (70:12 - 72:40)

**Objetivo:** tener un cliente MCP funcionando antes de escribir un servidor.

- Lab: siete tareas; cliente **Roo Code**, extensión de VS Code descrita como alternativa a Cursor o Windsurf (71:00).
- Configuración: provider *OpenAI compatible*, base URL y API key del entorno, modelo gratuito provisto por el lab (71:28-71:58).

**Ejercicio:** conectar un cliente MCP de tu preferencia a un modelo propio y verificar una respuesta. Entregable: captura de la configuración sin secretos.

### Módulo 32 - Core MCP Components: Resources, Tools, and Prompts (72:40 - 74:13)

**Objetivo:** distinguir los tres componentes del servidor por su función.

- **Tools:** "The server must list all of its capabilities as a list of tools defined in a specific format" (1:14:47); cada tool lleva descripción y esquema de entrada/salida. Es lo que hoy sería la API del servidor.
- **Resources:** datos que el AI necesita para decidir, como políticas de reembolso o guías de ciudades (75:01). Llevan URI (https, archivo, repo git), nombre, título y descripción (75:32).
- **Prompts:** instrucciones que el autor del servidor sabe que funcionan mejor que las que inventaría el agente. Ejemplo del ponente (76:14-76:30): en vez de "find me a flight to London", un prompt que ordena llamar `search flights` con origen, destino y fecha en un formato específico. Se definen con nombre, título, descripción y argumentos (77:00).

**Ejercicio:** para tu integración, listar tres tools, dos resources y un prompt. Entregable: `componentes-mcp.md`.

### Módulo 33 - Understanding the MCP Specification and JSON-RPC Protocol (74:13 - 82:55)

**Objetivo:** entender el contrato que hace que cualquier cliente sirva con cualquier servidor.

- Qué significa MCP: *Model* = el LLM; *context* = darle contexto de terceros; *protocol* = un conjunto de estándares (72:55).
- Reglas de la especificación (73:22-73:36): comunicación en formato **JSON-RPC**, conexión **stateful**, el servidor ofrece resources/prompts/tools y el cliente ofrece sampling/roots/elicitation. Si el servidor cumple, cualquier cliente lo usa (73:50).
- **JSON-RPC:** Remote Procedure Call sobre JSON: llamar un método remoto con parámetros y recibir respuesta (77:44).
- Formato de request (78:13): `jsonrpc` versión **2.0**, `method`, `params`, `id`. El response lleva versión, resultado, id y un campo opcional de error (78:27).
- Punto fino: JSON-RPC **no define el transporte**; puede ser HTTP, websockets, TCP, UDP, Unix sockets, message queue o stdio (78:42). MCP soporta **HTTP y stdio** (78:54).

**Ejercicio:** escribir a mano el request y el response JSON-RPC de una tool propia, con y sin error. Entregable: `jsonrpc.md`.

### Módulo 34 - Hands-on Lab 7: Connecting to and Using an Existing MCP Server (82:55 - 86:22)

**Objetivo:** consumir un servidor MCP ya hecho desde un cliente.

- Pregunta de control: los transportes soportados son **HTTP y stdio** (83:14).
- El servidor del lab es *flight booking server*, con `server.py` y `pyproject.toml` (83:39).
- Conexión: en Roo Code, *MCP servers* → *edit project MCP* → pegar el JSON con `command: uv`, `args: run python server.py` (84:54-85:08). El refresh muestra el servidor en verde con sus tools y resources (85:23).
- Prueba: pedir un vuelo LAX→JFK; el cliente **pide aprobación** antes de ejecutar el tool (85:50) y devuelve el resultado.

**Ejercicio:** conectar un servidor MCP existente a tu cliente y ejecutar una tool, registrando el pedido de aprobación. Entregable: log del flujo.

### Módulo 35 - Building a Custom MCP Server with the Python SDK (86:22 - 89:12)

**Objetivo:** escribir un servidor propio con el SDK.

- Diseño primero (86:32): resources (aeropuertos, estado de vuelos, clima, políticas, programas de fidelidad), tools (buscar vuelos, detalles, crear y editar reservas, check-in, asientos, equipaje) y prompts (mejor vuelo, optimizar presupuesto, manejar disrupciones).
- Estructura con **FastMCP**: importar `fastmcp`, inicializar el servidor, definir cada pieza, y correrlo indicando transporte (stdio o HTTP) (87:19-87:47).
- El decorador es lo que convierte una función en componente: `mcp.resource`, `mcp.tool`, `mcp.prompt` (88:01-88:29).
- Variantes de servidor: stateful por defecto, stateless con el flag de HTTP stateless; transporte **streamable HTTP** disponible para streaming (88:44).

**Ejercicio:** escribir un servidor FastMCP mínimo con una tool, un resource y un prompt. Entregable: `server.py` propio.

### Módulo 36 - Testing with the MCP Inspector (89:12 - 89:45)

**Objetivo:** probar el servidor sin escribir un cliente todavía.

- Arranque: `npx` con el paquete `@modelcontextprotocol/inspector` levanta una web que permite listar prompts, tools y resources desde la barra de navegación (89:25-89:39).

**Ejercicio:** levantar el Inspector contra tu servidor y ejecutar cada componente una vez. Entregable: captura de cada pestaña.

### Módulo 37 - Hands-on Lab 8: Developing Resources, Tools, and Prompts for MCP (89:45 - 95:29)

**Objetivo:** completar un servidor y conectarlo a un cliente real.

- Pregunta de control: las tres features del servidor son **resources, tools y prompts** (90:07).
- Setup del proyecto: `uv init flight-booking-server` y `uv add mcp` (90:55-91:10).
- Tareas de código: agregar `@mcp.resource` a `get_airports` con tipo y nombre de archivo (92:05), `@mcp.tool` a `search_flights` y `create_booking` (92:31-92:45), y los decoradores de prompts (92:59).
- Conexión al cliente: editar el `mcp.json` de proyecto con nombre `flight-booking`, comando `uv run python server.py` y el directorio del proyecto (93:40-93:55); el refresh muestra el servidor en verde con tools y resources (94:24).
- Prueba: el cliente pide aprobación antes del tool call y devuelve dos vuelos LAX→JFK (95:08).

**Ejercicio:** terminar tus tres decoradores y consumir el servidor desde el cliente. Entregable: `lab8.md` con la prueba.

### Módulo 38 - Building an MCP Client: Roots, Sampling, and Elicitation (95:29 - 99:40)

**Objetivo:** entender qué ofrece el cliente y por qué el servidor depende de él.

- Si no querés depender de un cliente existente, el SDK permite escribir el propio: conectar al servidor HTTP, `list tools`, llamar `search flights` con origen y destino, `read resource`, `get prompts` (96:06-96:22).
- **Context:** el servidor puede reportar al cliente con `info`, `report progress` y `debug` — útil para tareas largas como una reserva (96:52-97:07).
- **Roots:** carpetas del cliente que el servidor **puede ver**, como carpetas compartidas; para que tools como linters o file readers accedan a lo justo y no a toda la máquina. El cliente define los roots permitidos y el servidor los lee con `session.list_roots` (97:22-98:06).
- **Sampling:** el servidor **no** llama al LLM directamente; pide al cliente una generación (por ejemplo, resumir un resource), y el cliente decide modelo y límites. El servidor define el handler de sampling y usa `create_message` (98:06-98:50).
- **Elicitation:** el servidor pide datos al usuario final, por ejemplo una confirmación antes de confirmar un vuelo; requiere un callback handler en el cliente (99:06-99:36).
- Razón de diseño que da el ponente: el servidor debe quedar liviano y desacoplado de la infraestructura de IA (98:21).

**Ejercicio:** escribir un cliente mínimo y decidir qué features necesita tu servidor (roots, sampling o elicitación) y por qué. Entregable: `cliente.md` + `client.py`.

## Banco de preguntas

1. ¿Qué diferencia hay entre keyword search, semantic search y RAG, y cuál resuelve qué?
2. ¿Por qué BM25 le da cero a un término que aparece en todos los documentos y TF-IDF no?
3. ¿Qué mide exactamente el dot product y por qué se normaliza?
4. ¿Por qué 500 documentos de 384 dimensiones implican 192.000 operaciones por query, y qué hace un índice para evitarlo?
5. ¿Cuál es el default peligroso de ChromaDB y cómo se cambia?
6. ¿Qué es el *precision problem* y qué parámetro lo resuelve parcialmente?
7. ¿Qué corre offline y qué corre online en un pipeline RAG?
8. ¿En qué capa cachearías si el cuello es el LLM, y en cuál si el cuello es el embedding? ¿Por qué la clave es un hash de query + contexto?
9. ¿Qué significa *graceful degradation* y cuál es la cascada del ponente?
10. ¿Por qué existe MCP si ya existen APIs? Explicá el problema N×M.
11. ¿Cuál es la diferencia entre un tool, un resource y un prompt en un servidor MCP?
12. ¿Por qué el servidor no llama al LLM directamente, qué es sampling y quién controla el modelo?
13. ¿Qué garantiza la especificación MCP sobre el transporte y qué deja a elección?
14. ¿Qué pasa si un cliente no implementa roots o elicitation y tu servidor depende de ellos?

## Notas editoriales

- **Cifra de caché.** El ASR dice "950 milliseconds" contra "5 seconds" y "190 times faster". 950/5 = 190, así que la segunda cifra son 5 **milisegundos**. Se cita la cifra corregida y se marca la del cue original.
- **Frase del curso mezclada.** El cierre de la Parte 1 (59:11-59:35) es del mismo expositor y habla de RAG; el corte oficial al siguiente capítulo está en 59:40. Se deja dentro del módulo 26.
- **Repeticiones del ASR.** El ponente repite una frase completa en 06:38-06:52 ("Next, we look at how to solve the problem of voice, style, and language..."); no es un error de transcripción, es el video. Se citó una sola vez.
- **Pseudo código.** El ponente aclara en 65:54 que el código del agente es pseudo código. Nada de lo mostrado en ese módulo debe correrse.
- **Expositor.** Ni el video ni la descripción nombran al expositor. No se infiere a partir del canal ni de los labs.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
