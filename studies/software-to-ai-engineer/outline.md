# Clase: De Software Engineer a AI Engineer — El Roadmap Más Realista

Clase de estudio construida a partir del video de **Fazt**. Transcripción ASR en
`transcripcion.md`; informe de esta revisión en `AUDIT-2026-11-09.md`.

## Ficha

- Fuente: https://www.youtube.com/watch?v=qLobAfve9b0
- Canal: Fazt (@FaztTech)
- Título: «De Software Engineer a AI Engineer: El Roadmap Más Realista»
- Ponente: Fazt
- Publicado: 2026-07-30
- Duración: 32:47 (1967s, medida en el reproductor)
- Idioma: español
- Tipo: roadmap de carrera + mapa de conceptos. No es tutorial.
- Patrocinador: **seenode** (`seenode.link/fazt`), bloque 0:53–1:59. No es contenido.
- Re-evaluación: 2026-11-09 con `deepseek-v4.1-flash`.
- Recursos reales de la descripción: [System Design Primer](https://github.com/karanpratapsingh/system-design) y [video de RAG](https://youtu.be/_B4jGz0JEGE). Los videos de CLI y de modelos locales que el ponente anuncia no están en la descripción.

## Qué cambió respecto de la v1

1. Mapa temporal basado en los **capítulos oficiales** del video, no en una estimación.
2. Patrocinador corregido: seenode (el ASR decía "Cynote").
3. "Claude 4" → **Claude 5** (20:23).
4. Duración real: 32:47.
5. Agregados: graph engineering, el argumento de que la IA abarata el aprendizaje, el caveat de que RAG no es la única vía, y el detalle de los dos casos prácticos (correo y deploy).
6. Notas de cátedra donde el ponente simplifica de más (tokens, contexto, temperatura).
7. Glosario de errores del ASR.

## Mapa mental: las tres capas del video

El propio ponente resume su roadmap así (26:46–27:10):

| Capa | Qué es | Bloque |
|---|---|---|
| 1. Base de desarrollo | DB, API/backend, frontend, Git, redes, Docker | 2:37–11:17 |
| 2. Base de IA | Modelos: tokens, contexto, temperatura, roles; APIs y costo | 11:17–19:40 |
| 3. Implementaciones | Prompt/function calling, RAG, CLI, skills, MCP, LLM Ops | 19:40–32:47 |

La tesis del video: **AI Engineer = dev de toda la vida + modelos de IA**. No es carrera nueva ni investigación; es una actualización de la capa 1 con la capa 2, y la capa 3 es lo que se vende.

## Protocolo de estudio (cómo usar esta clase)

Regla: **no ver 32 minutos seguidos y después estudiar.** El video se olvida antes de llegar al módulo 8. Se ve por bloques y cada bloque se cierra con recuperación, no con relectura.

### Tres bloques, tres sesiones

| Bloque | Video | Cómo verlo | Tiempo |
|---|---|---|---|
| **A — Base y System Design** | 0:00–11:17 (saltear 0:53–1:59) | 1.25x. Es checklist, no contenido nuevo. | ~9 min |
| **B — Modelos, APIs, costos** | 11:17–19:40 | 1x. Pausar en 11:17–12:48 (bases) y 13:58–16:58 (costos). | ~8 min |
| **C — Implementaciones** | 19:40–32:47 | 1x. Pausar en 22:04 (RAG), 24:18 (MCP) y 28:21 (LLM Ops). | ~13 min |

### Loop por bloque (20–30 min con Kanam)

1. **Recuperar sin mirar.** Tres preguntas del bloque. Sin outline, sin video, sin buscar. Lo que no sale, no sale: eso es el dato.
2. **Corregir solo lo que falló.** Si está bien, no lo explico. La clase no es un resumen del video: es el reparcheo de tus gaps.
3. **Aplicar.** El ejercicio del bloque, con entregable concreto.
4. **Registrar.** Una línea con lo que no sabías y lo que queda pendiente. Sin registro no hay progreso visible.

### Modo examen

En la sesión de profundización **yo pregunto primero**. No empiezo explicando: empiezo midiendo. Si querés la explicación directa, la pido y la doy, pero el orden por defecto es recuperación → corrección → práctica.

### Qué NO hacer

- Volver a mirar el video antes de responder. La incomodidad de no acordarse es el mecanismo, no un obstáculo.
- Ver el bloque C antes que el B. Sin vocabulario de modelos y costos, MCP y RAG suenan a magia.
- Estudiar dos bloques el mismo día. Un bloque por sesión, con el ejercicio hecho.

### Orden recomendado

A → B → C si querés la estructura completa. Si tenés poco tiempo: **B y C primero**, y usá A como checklist en paralelo, porque las bases ya las tenés y el gap real está en la capa de IA.

## Resultado esperado

Al terminar la clase deberías poder:

1. Distinguir AI Engineer / ML Engineer / AI Researcher / MLOps por lo que hacen, no por el título.
2. Auditar tus propias bases (lenguaje, SQL, frontend, Git, redes, Docker) contra el checklist del video.
3. Explicar por qué System Design es el puente entre dev tradicional y dev con IA.
4. Definir tokens, ventana de contexto, temperatura y roles `system`/`user`/`assistant` sin repetir las imprecisiones del video.
5. Estimar el costo de una feature por 1.000 usos y decidir si el cliente puede pagarla.
6. Diferenciar suscripción (para desarrollar) de API (para el producto).
7. Diseñar una integración sin chat: evento → IA → validación → persistencia, con fallback.
8. Situar prompt engineering y function calling en su justa medida.
9. Diseñar un RAG mínimo y explicar qué rol cumple la base vectorial.
10. Nombrar las otras interfaces (CLI, skills, MCP) y el problema de seguridad de cada una.
11. Entender LLM Ops: rate limiting, routing, caché, escalado y costo por inferencia.
12. Elegir un primer proyecto y justificarlo.

## Mapa temporal (capítulos oficiales)

| Tiempo | Capítulo |
|---|---|
| 0:00 | Intro: de Software Engineer a AI Engineer |
| 0:53 | Patrocinado (seenode) — ignorar |
| 1:59 | Para quién es este roadmap |
| 2:37 | Las bases del desarrollo |
| 4:07 | AI Engineer vs MLE vs AI Researcher |
| 6:31 | ¿Qué hace realmente un AI Engineer? |
| 7:41 | Checklist previo: lenguaje, SQL, Git, redes, Docker |
| 9:07 | System Design |
| 11:17 | Bases de los modelos: tokens, contexto, temperatura, roles |
| 12:48 | APIs de IA: Anthropic y OpenAI |
| 13:58 | Costos: API vs suscripción (y modelos chinos) |
| 16:58 | Trabajar con la API y casos de uso reales |
| 19:40 | Prompt engineering y function calling |
| 22:04 | RAG y bases de datos vectoriales |
| 24:18 | CLI, Skills y MCP |
| 26:46 | Repaso del roadmap |
| 28:21 | LLMOps: desplegar modelos y optimizar costos |
| 30:23 | Resumen de roles y por dónde empezar |
| 32:20 | Cierre |

## Módulos

### Módulo 0 — Intro y para quién (0:00–2:37)

- **Objetivo:** entender la promesa y descartar el malentendido de base.
- **Idea fuerza (0:24–0:35):** «en realidad es como una continuación del desarrollo de software y que en realidad cualquiera puede aprender si ya sabe el desarrollo de software básico».
- **Para quién (1:59–2:37):** quien ya estudió algunos años o creó aplicaciones y quiere **actualizarse**. El propio autor anuncia un roadmap «desde cero» aparte: este no lo es.
- **Contra-malentendido:** AI Engineer no es quien crea modelos ni quien investiga modelos.
- **Pregunta:** ¿qué parte de tu stack ya cumple la base que el video asume?

### Módulo 1 — Las bases del desarrollo (2:37–4:07)

- **Objetivo:** confirmar que la capa 1 está cubierta.
- **Las tres partes de cualquier aplicación (2:37–3:25):** base de datos (SQL, NoSQL y nuevas), API/backend (Go, Python, JS/TS con Node, Java, .NET) y frontend que consume la API.
- **Lo que acompaña (3:31–4:04):** protocolos de seguridad y authorización, modelado de datos, herramientas de debugging y testing.
- **Lectura crítica:** es un checklist, no una ruta. El video no enseña ninguna de estas cosas.
- **Ejercicio:** marcar cada ítem como *lo defiendo en una entrevista* / *lo uso con ayuda* / *no lo tengo*.

#### El checklist, traducido a lo que importa en IA

El ponente lista siete ítems sin explicar qué los vuelve un prerrequisito. La traducción:

| Ítem | Para qué sirve realmente en un sistema de IA |
|---|---|
| Lenguaje | Leer y arreglar el código que conecta el modelo; sin esto no hay nada más |
| SQL / Postgres | Guardar conversaciones, resultados, costos; `pgvector` convierte la misma DB en base vectorial |
| APIs | La llamada al modelo es una API más: timeouts, reintentos, errores, auth |
| Frontend | El streaming en la UI es un problema de frontend, no de modelo |
| Git | Versionar prompts y datasets como versionás código: sin esto no hay rollback |
| Redes (HTTP) | Entender que una llamada de 8 s necesita timeout y que el SSE no es magia |
| Docker | Aislar el runtime de los agentes; reproducibilidad del entorno |

#### Lo que el checklist no incluye y un AI Engineer sí necesita

El video da la lista mínima de un dev web. Para IA faltan tres cosas de la capa 1:

- **Colas y trabajo asíncrono** (BullMQ, SQS, pg-boss): una llamada de IA de 8 s no cabe en un request HTTP síncrono.
- **Caché**: la misma pregunta no debería pagar dos veces.
- **Observabilidad mínima**: logs estructurados con `request_id`, duración y tokens. Sin esto no podés medir nada de los tres niveles de evaluación.

#### Autoevaluación del Módulo 1 (10 minutos)

Marcá cada ítem con una sola letra, sin autoengaño:

- **D** = lo defiendo en una entrevista sin ayuda.
- **H** = lo uso con ayuda (documentación, IA, colega).
- **N** = no lo tengo.

1. Lenguaje con tipos (TS): async/await, genéricos, módulos.
2. SQL: joins, índices, transacciones, `EXPLAIN`.
3. APIs: status codes, headers, auth, paginación, rate limits.
4. Frontend: React, estado, streaming, manejo de error de red.
5. Git: ramas, rebase, resolver conflictos.
6. Redes: qué pasa entre un click y la respuesta, CORS, timeouts, SSE.
7. Docker: imagen vs contenedor, variables de entorno, compose.
8. *(agregado)* Colas / asincronía: por qué una llamada larga no va en un request.
9. *(agregado)* Caché: claves, invalidación, qué se puede cachear en IA y qué no.
10. *(agregado)* Observabilidad: logs con `request_id`, latencia, costo por operación.

**Cómo se lee el resultado:** cualquier **N** en los ítems 1 a 7 es un bloqueo real antes de tocar modelos. Cualquier **N** en 8 a 10 no bloquea el aprendizaje de la capa 2, pero bloquea llevar algo a producción.

**Dato de carrera:** un AI Engineer junior hoy se contrata con 1–7 en D y 8–10 en H. Un senior necesita 8–10 en D, porque **son los tres ítems que permiten medir** — y medir es lo que separa el rol del vibe coding.

### Módulo 2 — Roles en IA (4:07–6:31)

- **Objetivo:** separar cuatro roles que suelen confundirse.

| Rol | Qué hace | Nivel |
|---|---|---|
| AI Engineer | Crea aplicaciones que **usan** modelos | Práctico |
| ML Engineer | Entrena, adapta y hace tuning de modelos; entiende papers | Avanzado |
| AI Researcher | Diseña modelos y crea investigación; matemática avanzada, PhD | Muy avanzado |
| MLOps / DevOps IA | Despliega y opera modelos en la nube | Transversal |

- **Citas:** ML Engineer «entrena modelos o los puede ir adaptando, es decir, hacer tuning» (4:40–4:47); AI Researcher «ya no leen investigaciones, sino que básicamente las crean» (6:03–6:06).
- **Etiqueta:** descripciones orientativas, no estándar de la industria. [opinión informada]
- **Ejercicio:** escribir en una frase qué le pedirías a cada rol en un equipo de 4 personas.

### Módulo 3 — Qué hace un AI Engineer + checklist (6:31–9:07)

- **Objetivo:** definir el rol y medir el gap real.
- **Definición (7:26–7:38):** «un AI engineer es básicamente una persona que crea aplicaciones de toda la vida, pero utiliza modelos de IA».
- **Checklist (7:41–8:58):**
  1. Un lenguaje de programación: sintaxis, para qué sirve, alternativas.
  2. Una base de datos SQL; recomienda PostgreSQL.
  3. APIs.
  4. Frontend.
  5. Git.
  6. Redes a nivel práctico: HTTP, UDP, FTP.
  7. Docker y nociones de nube.
- **Claim del ponente (7:54–8:00):** «ya tienes modelos inteligentes que pueden responderte cualquier tipo de duda», así que aprender esto es más fácil que antes. [opinión]
- **Ejercicio:** elegir el ítem más flojo y escribir qué evidencia te faltaría para considerarlo cubierto.

### Módulo 4 — System Design (9:07–11:17)

- **Objetivo:** entender por qué el diseño de sistemas es el puente.
- **Definición (9:13–9:36):** «no pensamos solamente en lenguajes o frameworks, sino básicamente en los servicios, en la forma en la que se despliegan las aplicaciones y cómo estas se conectan».
- **Contenidos que menciona:** proxies, diseño de base de datos, **ACID** y CAP, colas, publish/subscribe.
- **Recursos:** repo *System Design* y *System Design Primer* (link en la descripción).
- **La frase que importa (11:03–11:09):** en un sistema con IA «van a aparecer un nuevo recuadro o unos cuantos recuadros nuevos». El resto del diagrama es igual.
- **Ejercicio 1:** diagrama de un CRUD con auth + un componente de IA. Marcar servicios, datos de entrada/salida, dónde vive el estado y qué pasa si el componente de IA falla.

### Módulo 5 — Bases de los modelos (11:17–12:48)

- **Objetivo:** manejar el vocabulario mínimo antes de tocar una API.
- **Cuatro conceptos:** tokens, ventana de contexto, temperatura, roles.
- **Roles:** `system` es el prompt que configura el comportamiento; `user` es el mensaje; `assistant` es la respuesta del modelo.
- **Notas de cátedra (corrigen al video):**
  - **Tokens:** el video los llama «el streaming de datos» (11:21). Un token es una unidad subpalabra; el streaming es el modo de entrega. El costo y los límites se miden en tokens.
  - **Contexto:** el video dice que es «cuánto podemos conversar antes de que empiece a inventar» (11:47). Es el máximo de tokens que el modelo puede atender en una llamada; al excederlo se trunca o falla.
  - **Temperatura 0:** el video dice «no te inventes nada» (11:56). Baja la aleatoriedad; no garantiza veracidad. Para eso hacen falta contexto, instrucciones y verificación.
- **Ejercicio 2:** explicar los cuatro conceptos con un ejemplo de una app propia, sin usar las palabras del video.

### Módulo 6 — APIs de IA (12:48–13:58)

- **Objetivo:** saber qué se contrata cuando se usa un modelo.
- **Proveedores que menciona:** Anthropic (Claude Opus, Sonnet, Fable) y OpenAI (GPT 5.5, 5.6, GPT Image).
- **Claim (13:42–13:45):** Anthropic no genera imágenes. [verificado: correcto a octubre 2026]
- **Idea fuerza:** el modelo es la IA; la API es el canal; se paga por uso.
- **Ejercicio:** listar qué modelo usarías para (a) clasificar 10.000 correos, (b) generar una imagen de producto, (c) resumir un contrato de 80 páginas. Justificar.

### Módulo 7 — Costos: API vs suscripción (13:58–16:58)

- **Objetivo:** poder decir que no a un cliente con números.
- **Cobro:** por millón de tokens.
- **Error típico del cliente (14:18–14:24):** creer que pagando US$100 o US$200 tiene IA ilimitada dentro del producto.
- **Diferencia central (14:25–15:20):**
  - **Suscripción** (Claude Code, OpenCode, GPT Codex): para **desarrollar**. US$20 / US$100 / US$200.
  - **API:** para **el producto**. Se paga por uso.
  - No son intercambiables.
- **Por qué la suscripción es barata (15:00–15:18):** la empresa subsidia el consumo; una suscripción de US$200 no cubre el gasto real. [opinión informada]
- **Modelos chinos (15:42–16:38):** más baratos; sirven para tareas simples. Para imágenes con pocos detalles, archivos grandes o máxima precisión, OpenAI/Anthropic responden mejor. [opinión]
- **Dato que falta en el video:** no da precios por MTok ni una estimación concreta. Se completa en la lección de costos con las páginas oficiales.
- **Ejercicio 3:** estimar tokens y costo por 1.000 usos de «resumir un email de 300 palabras». Decidir si la feature es viable a US$5/mes por usuario.

### Módulo 8 — Trabajar con la API y casos de uso (16:58–19:40)

- **Objetivo:** diseñar integraciones que no sean un chat.
- **Lo básico (16:58–17:25):** llamada API, formatos de respuesta (`markdown`, `JSON`, `HTML`), concurrencia, manejo de errores.
- **Caso A — UI asistida (18:10–18:27):** un botón que rellena un campo de texto. La misma llamada, distinta interfaz.
- **Caso B — Email (18:27–18:57):** el backend recibe el correo y, **antes de guardarlo**, lo procesa: resume, valida, clasifica y decide si vale la pena persistirlo.
- **Caso C — Deploy auto-reparable (18:58–19:20):** falla el deploy → se pasa el error a la IA → corrige → push → redeploy. El propio ponente lo marca como complejo y caro.
- **Ejercicio 4:** elegir un proceso manual propio y escribir el flujo evento → IA → validación → persistencia, incluyendo qué pasa si la IA devuelve basura.

### Módulo 9 — Prompt engineering y function calling (19:40–22:04)

- **Objetivo:** dimensionar ambas prácticas sin sobrevalorarlas.
- **Prompt engineering (19:47–20:40):** «saber cómo pedirle algo». Tuvo mala reputación por sobreventa. Los modelos actuales interpretan mejor el contexto: el ponente cita un post del equipo de Claude Code que eliminó una gran cantidad de prompts internos porque **Claude 5** ya interpreta mejor. [anécdota]
- **Pero en producto propio sigue siendo necesario (20:37–21:00):** definir el comportamiento del sistema. Ejemplos del video: «Eres un sistema manejador de errores de despliegue», «Eres un clasificador de correos».
- **Function calling / tools (21:00–22:04):** la IA ejecuta código real (una función del backend) en vez de solo responder. Ejemplo: clasificar y eliminar un correo.
- **Lectura crítica:** el video le resta épica al prompt engineering y se la da al function calling. En un producto real, el prompt del sistema es lo que hace que el tool calling sea confiable.
- **Ejercicio 5:** escribir el system prompt de un clasificador de correos y la función que ejecutaría. Definir qué hace si la confianza es baja.

### Módulo 10 — RAG y bases vectoriales (22:04–24:18)

- **Objetivo:** entender cómo una IA lee datos propios.
- **RAG (22:08–22:18):** *retrieval augmented generation*. El caso: una empresa con ventas, RRHH, pagos e inventario quiere consultar sus datos en lenguaje natural.
- **Qué datos entran:** bases de datos, documentos, Excels, cualquier origen.
- **Base vectorial (23:05–24:00):** los datos se convierten a vectores; la IA consulta esa copia. Puede ser una DB aparte (Pinecone, Chroma) o la misma DB con soporte de vectores.
- **Caveat del ponente (24:12–24:18):** «no es la única forma de lograr que una IA pueda interpretar tus datos». [importante]
- **Agregado nuestro, no del video:** `pgvector` en PostgreSQL es la vía más corta si ya usás Postgres. El ponente no lo nombra.
- **Ejercicio 6:** RAG mínimo sobre 20 documentos: origen → chunking → embedding → storage → consulta → respuesta con cita de la fuente.

### Módulo 11 — CLI, Skills y MCP (24:18–26:46)

- **Objetivo:** conocer las otras superficies de entrega.
- **CLI (24:20–24:55):** un cliente de consola que consulta tu API. Permite que una IA use tu sistema desde la terminal. Requiere acotar qué puede hacer para que no reescriba código.
- **Skills (24:55–25:05):** «definir un prompt y poder reutilizarlo». Es lo más liviano del video: minutos.
- **MCP (25:06–26:27):** conector entre un chat existente (ChatGPT, Claude Desktop) y tu API. Funciona como traductor: el usuario pide «ventas de este año» y el MCP lo convierte en `GET /ventas?desde=2026`.
- **Ventaja económica:** el usuario paga su suscripción; vos solo desplegás el traductor.
- **Seguridad (27:20–27:35):** el MCP puede dar acceso a datos que el usuario no debería ver. «Es como diseñar una API al final del día».
- **Frameworks (27:56–28:17):** LangChain, LlamaIndex, Temporal, Inngest. Útiles; no obligatorios al principio.
- **Ejercicio 7:** diseñar un MCP de solo lectura sobre una API propia y listar qué endpoints **no** expondrías.

### Módulo 12 — Repaso del roadmap (26:46–28:21)

- **Objetivo:** consolidar la estructura de tres capas.
- El ponente repite el orden: modelos → teoría → práctico vendible.
- **Advertencia:** todo está «sobre simplificado»; cada implementación tiene su propia profundidad (vectorización de grandes volúmenes, documentación de tools del MCP, permisos del CLI).
- **Ejercicio:** dibujar el mapa de tres capas con tus propios proyectos en cada casillero.

### Módulo 13 — LLM Ops (28:21–30:23)

- **Objetivo:** entender el costo operativo de poner un modelo en producción.
- **Dos escenarios:** modelo en nube propia (AWS, GCP, Azure; pagás uso de nube) o self-hosted/local.
- **Por qué una empresa elige self-host:** no quiere que sus datos salgan. [opinión informada]
- **Problemas operativos que enumera:** rate limiting, optimización de costos, model routing, caching, escalado y concurrencia.
- **Definición:** LLM Ops es «mandar a producción modelos inteligentes o aplicaciones que utilicen modelos inteligentes».
- **Ejercicio:** para una app con 10.000 usuarios/día, elegir API externa o self-host y justificar con tres números (costo, latencia, privacidad).

### Módulo 14 — Resumen de roles y por dónde empezar (30:23–32:47)

- **Objetivo:** cerrar con una decisión.
- **Recomendación (31:38–31:45):** «empiecen con el RAG». Es la forma más básica de entender cómo una IA responde sobre datos.
- **Después:** MCP. Y a medida que aparezcan: más frameworks.
- **Término emergente (30:57–31:22):** *graph engineering* — generar grafos a partir de la información. El ponente lo menciona como tendencia, sin desarrollarlo.
- **Mapeo final:** AI Engineer genera aplicaciones; ML Engineer trabaja con modelos; AI Researcher diseña modelos.
- **Cierre:** es una actualización, no una carrera nueva (30:42–30:55).

## Ejercicios por bloque

- [ ] **E1 — Bases:** marcar los 7 ítems del checklist y elegir el gap principal.
- [ ] **E2 — Vocabulario:** explicar tokens, contexto, temperatura y roles con ejemplos propios.
- [ ] **E3 — System Design:** diagrama de una app propia + un recuadro de IA, con punto de falla.
- [ ] **E4 — Costo:** estimación por 1.000 usos de una feature real, con precio por MTok verificado.
- [ ] **E5 — Integración:** flujo evento → IA → validación → persistencia, con fallback.
- [ ] **E6 — Prompt + tools:** system prompt de clasificador + función ejecutable + umbral de confianza.
- [ ] **E7 — RAG:** prototipo sobre 20 documentos con cita de fuente.
- [ ] **E8 — MCP:** diseño de un conector de solo lectura y lista de endpoints prohibidos.

## Banco de preguntas para estudiar con el usuario

1. ¿A qué rol apuntás en 12 meses y qué te falta para decirlo con honestidad?
2. De los 7 ítems del checklist, ¿cuál defenderías en una entrevista y cuál no?
3. ¿Por qué System Design importa más que aprender otro framework?
4. Explicame tokens, contexto y temperatura sin repetir las definiciones del video.
5. ¿Cuándo conviene suscripción y cuándo API? Dame un caso de cada uno.
6. ¿Cómo le explicás a un cliente que su idea de "IA ilimitada por US$100" no existe?
7. ¿Qué proceso manual tuyo automatizarías primero con un flujo sin chat?
8. ¿Prompt engineering o function calling: cuál pesa más en un producto real y por qué?
9. ¿Qué corpus pequeño usarías para tu primer RAG y cómo evaluarías si responde bien?
10. ¿Qué endpoints no expondrías en un MCP y por qué?
11. ¿Self-host o API para tu primer proyecto? Defendé la decisión con costo, latencia y privacidad.
12. ¿Qué le falta a este roadmap para el AI Engineer de 2026? (ver "Lo que el video no cubre").

## Aplicación a tu perfil (Gonzo)

Contexto: React/TS, Supabase/Edge Functions, billing, tooling; 10 años de desarrollo; inglés B2.

- **Ya cubierto:** lenguaje (TS), DB (Postgres/Supabase), frontend (React), Git, APIs REST, Docker parcial.
- **Gaps reales:** System Design explícito, práctica con APIs de IA y costos, RAG end-to-end, evaluación de calidad.
- **Plan de 4 semanas (ajustado):**
  - **Semana 1:** bases de LLM + costo. Medir tokens y precio real de una llamada; comparar Anthropic vs OpenAI vs un modelo chino.
  - **Semana 2:** integración sin chat. Edge Function que clasifique o resuma, con validación de salida y fallback.
  - **Semana 3:** RAG mínimo con `pgvector` sobre 20 documentos, con cita de fuente y 10 preguntas de evaluación.
  - **Semana 4:** MCP de solo lectura o chat mínimo en React + mini System Design del conjunto.

## Evaluación en concreto

El video dice "empezar por RAG" pero no dice cómo saber si el RAG responde bien. Sin esto no hay producto: un RAG que responde con seguridad y se equivoca es peor que no tener RAG. La evaluación se hace en **tres niveles**, y cada uno responde una pregunta distinta.

### Nivel 1 — Origen del dato (¿de dónde sacó esto?)

- **Qué se mide:** de las afirmaciones de la respuesta, cuántas citan una fuente real que **existe** y **dice lo que se le atribuye**.
- **Cómo se mide:** por cada respuesta, listar las afirmaciones y verificar la cita contra el documento original. Dos defectos separados: *cita inexistente* (peor) y *cita real que no sostiene la afirmación*.
- **Umbral típico:** 0 citas inventadas. Una sola cita falsa en un producto de soporte al cliente destruye la confianza.

### Nivel 2 — Calidad de la respuesta (¿está bien?)

- **Qué se mide:** si la respuesta resuelve la consulta, sin inventar y sin omitir lo esencial.
- **Cómo se mide:** un **conjunto de casos con respuesta conocida** (golden set). Se escribe a mano una vez, 20 a 50 casos, cada uno con la respuesta esperada. Cada cambio de prompt, de modelo o de chunking se compara contra ese set.
- **Umbral típico:** una tasa de acierto que no baje entre versiones. El número importa menos que la **tendencia**.
- **Nota:** es la misma lógica que el gate de regresión de `scripts/test-handoff-merge.py` o `test-skill-router.py`: sin casos fijos, "funciona" es una opinión.

### Nivel 3 — Salud del sistema (¿está caro, lento o roto?)

- **Qué se mide:** latencia p50/p95, tasa de error, costo por consulta y cuántas veces el modelo se negó o devolvió una salida inválida (JSON roto, texto vacío).
- **Por qué el tercero importa:** los dos primeros se miden en el laboratorio; este se mide en producción. Un RAG con 95 % de acierto y 8 segundos de latencia no sirve para soporte en vivo.
- **Trampa:** el costo por consulta se dispara con respuestas largas o con reintentos silenciosos. Sin medirlo, el primer mes es barato y el segundo no.

### Mapeo contra el sistema Kanam (honesto)

| Nivel | Qué tenemos | Qué falta |
|---|---|---|
| Origen del dato | `check-unsourced-claims.py`, `check-refs.py`, `wiki_lint`; el curso de Vane midió la calidad de las fuentes | Verificación de que una cita **sostenga** la afirmación, no solo que exista |
| Calidad | `check-*.py` (22 gates binarios), regresión del skill router 10/10, pre-commit con tests | Un **golden set semántico**: nada mide si una respuesta es *mejor* que la anterior, solo si rompe un contrato |
| Salud | `stallCount` en el pipeline, límites de contexto, memoria de costos por plan | Costo por request medido, latencia observada, tasa de fallo de modelo |

**Conclusión del mapeo:** el sistema es fuerte en verificación binaria (pasa / no pasa) y débil en evaluación continua (¿mejor / peor?). Es exactamente el hueco que el video no cubre, y es la diferencia entre tener gates y tener evals.

## Lo que el video NO cubre (y un AI Engineer 2026 sí necesita)

- **Evals:** cómo medir si la respuesta es buena. Sin esto no hay producción.
- **Chunking y calidad de retrieval:** el video dice "varios pasos" y no entra.
- **Agents:** bucles multi-paso con tools; solo cubre function calling básico.
- **Guardrails:** validación de salida, límites de costo, permisos.
- **Observabilidad:** trazas, latencia, tasa de error, costo por request.
- **Structured outputs:** JSON schema como contrato de confiabilidad.
- **Fine-tuning:** cuándo conviene y cuándo no.
- **Privacidad y legal:** solo lo roza al hablar de self-host.

## Glosario de errores del ASR

| ASR | Correcto |
|---|---|
| Cynote / Cynode | seenode |
| Note 10 | .NET 10 |
| Postres / Postre SQL | PostgreSQL |
| Maya SQL | MySQL |
| ASIS | ACID |
| IPI | API |
| EA engineer | AI Engineer |
| CBS | CVs |
| pr the engineering / PR engineer | prompt engineering |
| RAC / RAS | RAG |
| Cloud / Sonate / output | Claude / Sonnet / Opus |
| LlM OS | LLM Ops |
| Lane Shain / Laraf / Injes | LangChain / LlamaIndex / Inngest |
| Pinecon | Pinecone |
| fast.de | fazt.dev |

## Notas editoriales

- Transcripción automática: los nombres propios y los números son lo más frágil. Las citas de este outline se contrastaron contra la descripción oficial y contra fuentes primarias cuando el claim era mutable.
- El bloque 0:53–1:59 es publicidad de seenode; se conserva en la transcripción por fidelidad, no es contenido.
- El video es un roadmap, no un tutorial. Cada módulo necesita una lección práctica aparte para convertirse en habilidad.
- Los claims marcados [opinión] o [anécdota] no se tomaron como hechos: subsidio de suscripciones, calidad de modelos chinos, self-host por privacidad.
- El ponente promete videos de CLI y de modelos locales "en la descripción" que no están. No buscarlos.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
