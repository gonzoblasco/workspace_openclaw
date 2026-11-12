# Clase: n8n Full Course – Architect Scalable AI Automations from Scratch

- Fuente: https://www.youtube.com/watch?v=YY-egxTQirA
- Canal: freeCodeCamp.org
- Expositor: Rahul Joshi (co-fundador y CEO de TechDome, creador de @automationsbyrahul)
- Duración: 43:05
- Publicado: 2026-10-09
- Idioma: inglés (subtítulos automáticos, glosario de ASR en `transcripcion.md`)
- Capítulos: los 14 oficiales de la descripción del video, alineados 1:1 con los módulos

## Resultado esperado

Al terminar la clase deberías poder:

1. Distinguir qué problema resuelve n8n frente a Zapier/Make y cuándo conviene self-hostear.
2. Leer y escribir el patrón canónico de cualquier pipeline: **trigger → transformación → lógica → IA → acción**.
3. Usar el nodo HTTP Request contra una API real con paginación, credenciales y transformación de datos.
4. Decidir entre una LLM suelta y un **agente** con tools, y diseñar el tool mínimo necesario.
5. Elegir el mecanismo de memoria (Simple Memory vs. base persistente) según el caso; usar una Sheet como knowledge base sin vector DB.
6. Diseñar un **multi-agente por roles** y una arquitectura **event-driven** con filtro antes de molestar a un humano.
7. Implementar **human-in-the-loop**, manejo de errores con retry/fallback/alerta, y monitoreo de ejecuciones y costo de tokens.

## Mapa temporal

| Tiempo | Bloque |
|---|---|
| 00:00 - 01:45 | Intro: qué es n8n y qué cubre el curso |
| 01:45 - 04:44 | Canvas, hosting y self-hosting |
| 04:44 - 07:44 | Workflow 1: webhook → Set → IF → OpenAI → Gmail |
| 07:44 - 10:21 | Workflow 2: chatbot de CRM con Google Sheets como tools |
| 10:21 - 13:06 | HTTP Request node + SerpAPI + limpieza a Sheets |
| 13:06 - 15:46 | Documento de embarque: prompt con schema, decisión, acción |
| 15:46 - 18:38 | Agente vs. LLM: web search + email |
| 18:38 - 22:01 | Google Sheets como knowledge base |
| 22:01 - 24:37 | Memoria corto vs. largo plazo |
| 24:37 - 27:28 | Multi-agente de contenido (4 roles) |
| 27:28 - 32:25 | Event-driven: calificación de leads + alerta filtrada |
| 32:25 - 34:40 | Human-in-the-loop con Slack |
| 34:40 - 38:12 | Error handling, retries y fallbacks |
| 38:12 - 43:05 | Monitoreo, observabilidad y costo de tokens |

## Módulos

### Módulo 1 - Qué es n8n (00:00 - 01:45)

**Objetivo:** ubicar n8n como infraestructura de orquestación, no como juguete de zapier.

- Self-host y orquestación: el expositor describe el recorrido, de qué se trata n8n y cómo construir automatizaciones reales desde cero. La cita literal del bloque (00:48) es "complete journey what NAT actually is, how it works, and how you can build real world automation systems" — el ASR transcribe "n8n" como "NAT". La frase "automation infrastructure and orchestration engine" no aparece en el transcript: era una paráfrasis con comillas.
- El claim de alcance: "Zapier is just a small subset of what NAT can actually do" (01:06). **Lectura crítica:** es una afirmación de marketing del ponente, no una comparación medida; Zapier también integra miles de apps. Lo defendible es que n8n es *self-hostable, código abierto y programable* (nodes en JS, Code node), y eso es lo que Zapier no da.
- Autopresentación: co-fundador/CEO de TechDome, "the number one creator on NAN", "I've helped transform over 1200 plus b" (00:33). **Evidencia: anécdota del ponente, sin fuente verificable.**
- Promesa de contenido: workflow design, API orchestration, agentes, vector DBs, event-driven, deployment, self-hosting (01:23).

**Ejercicio:** escribir en 5 líneas el caso de uso propio que justificaría n8n sobre Zapier (self-host, datos propios, lógica de código, agentes con tools). Entregable: `mi-caso.md`.

### Módulo 2 - Canvas, hosting y self-hosting (01:45 - 04:44)

**Objetivo:** entender qué te da la instancia propia y cómo se ve la anatomía de un workflow.

- Vías de instalación: descarga desde GitHub para correr local (01:45), plan pago tipo starter para ~2.000–2.500 ejecuciones de workflow, y self-host como "the real power" (01:58). **El ASR reporta el número de ejecuciones de forma ambigua; no se toma como especificación de precio.**
- Self-host sobre infraestructura propia: AWS, Azure o cualquier cloud; el demo usa un VPS (el ASR deforma el proveedor y no es un dato firme de la clase).
- Vista del entorno: workspace personal, multi-usuario y control de accesos, integración con GitHub, visibilidad de workflows (02:30).
- **Todo workflow empieza con un trigger** y hay cinco familias: manual, evento de app, schedule, webhook, y chat (03:06).
- Capacidades del canvas: conectar APIs, transformar datos, loops, ejecución en paralelo, **sistemas de aprobación** (03:22) — esto es la semilla del módulo 12.

**Ejercicio:** listar los triggers disponibles en la propia instancia y clasificarlos en las 5 familias. Entregable: tabla trigger → familia.

### Módulo 3 - Workflow 1: form-to-AI email (04:44 - 07:44)

**Objetivo:** ejecutar el patrón canónico de punta a punta. Es el esqueleto de todo lo que sigue.

- Secuencia: **webhook → Set → IF → OpenAI → Gmail**; "Data comes in via a web hook, gets cleaned, goes through a logic check, gets sent to AI, and finally delivers a personalized email" (04:49).
- Webhook en POST sobre un path fijo (`architecture-demo`), con datos pinned para testear sin llamada externa (05:06).
- Set node: mapea name / email / company y agrega un campo hard-coded, con input y output lado a lado (05:22–05:58).
- IF node: una sola condición, `company` no vacía; la rama false no hace nada y en producción iría a otro template, Slack o CRM (05:58–06:31).
- OpenAI node con prompt dinámico que inyecta `$json.name` vía expresión; la salida llega como `message.content` (06:31–07:02).
- Cierre: leer el **execution log** para ver el JSON completo desde el webhook hasta lo que Gmail envió (07:19).

**Ejercicio:** reconstruir el workflow con la propia cuenta, pero con la rama false conectada a algo (registro en Sheet o Slack). Entregable: captura del execution log de un run true y uno false.

### Módulo 4 - Workflow 2: chatbot de CRM (07:44 - 10:21)

**Objetivo:** ver cómo el agente decide a qué tool ir, y cómo se valida su salida.

- Stack: GPT-4o mini + Google Sheets + memoria, sobre el **chat trigger** del editor (07:51).
- El agente ("brain") decide si consultar la Sheet de *outreach* o la de *opportunities* — "It never guesses and always looks up data first" (08:42).
- Dos Sheets como tools separadas por dominio: una por prospecto/outreach, otra por oportunidad/deal (08:42–08:58).
- Memory buffer window para multi-turno dentro de la sesión (09:16).
- **IF de validación de salida**: si hay respuesta sigue, si no, se loguea el fallo en otra Sheet para debug sin romper el bot (09:16–09:49).
- Cada turno se persiste (timestamp, session id, mensaje, respuesta) y se responde con el Chat Response node (09:49–10:06).

**Ejercicio:** agregar un tercer tool de solo lectura (ej. FAQ) y verificar que el agente no lo invoca cuando la pregunta es sobre deals. Entregable: dos runs, con y sin invocación del tool, y la justificación.

### Módulo 5 - HTTP Request node y API scraping (10:21 - 13:06)

**Objetivo:** dominar el nodo que conecta n8n con *cualquier* API REST.

- Métodos GET/POST/PUT/DELETE y tipos de auth: API key en header o query, Bearer, **OAuth2** (Google, Salesforce), Basic Auth (10:39–10:55).
- **Nunca hardcodear keys en el canvas**: se usan credenciales n8n (11:13). Regla de higiene que vale para cualquier proyecto.
- Ejemplo SerpAPI: `serpapi.com/search`, `engine=google`, `q`, `num=10`, API key desde credencial (11:13).
- **Paginación**: SerpAPI devuelve `next_page_token`; el patrón es "Check if it exists. Loop back. Fire another request." (11:29).
- Transformación con Code node: tomar `organic_results`, mapear a campos planos (name, website, description, source URL) y estampar `scraped_at` (11:46).
- Sheets en **append mode**, con mapeo columna por columna, y el nodo como pieza intercambiable (Airtable, Notion, CRM, webhook, email) (12:03–12:19).

**Ejercicio:** correr la misma API con paginación acotada a 2 páginas y escribir el JSON plano a una Sheet. Entregable: Sheet con ≥20 filas y el Code node comentado línea por línea.

### Módulo 6 - Documento de embarque: prompt con schema (13:06 - 15:46)

**Objetivo:** aprender el patrón de cuatro pasos de todo sistema de IA y por qué el prompt estructurado es la diferencia.

- **El patrón universal: input → AI analysis → decision → action** (13:25). Es el corazón conceptual del curso.
- Prompt engineering: "If you just say, \"Read this document,\" you'll get back a paragraph. And paragraphs don't automate" (13:59). Se pide una lista explícita de campos (B/L number, shipper, consignee, vessel, ports) y se fuerza JSON.
- Salida estructurada → Code node que la convierte en campos predecibles para el resto del workflow (14:17).
- **Decisión de compliance:** si falta B/L number, shipper o consignee, el documento requiere humano; si están todos, se loguea y sigue (14:35).
- **Acción:** email inmediato "flagging exactly which document and which field needs attention", en vez de fallar en silencio (14:52).
- Aplicabilidad declarada por el ponente: facturas, tickets de soporte, contratos — cualquier dato estructurado enterrado en texto libre (15:10).

**Ejercicio:** escribir el prompt con schema para un tipo de documento propio (factura o CV) y definir los campos "obligatorios" que disparan el humano. Entregable: prompt + tabla campo → requerido sí/no → acción si falta.

### Módulo 7 - Agente vs. LLM (15:46 - 18:38)

**Objetivo:** distinguir generación de texto de decisión con tools, y saber dónde termina el agente.

- Distinción base: "An LLM is just" (15:59).
- **La jerarquía importa**: "the agent is this node here and the LLM is plugged into it, not the other way around" (16:16). En n8n el LLM es *sub-nodo* del agente.
- Forma invariante: user request → agent → select tool → execute → return result (16:16).
- Tool único (Google Search vía SerpAPI) y la justificación: "One tool, one clear job. That's often better than giving an agent five tools it barely uses" (17:24).
- **Distinción fina que casi todos confunden:** el nodo Send Email *no es un tool del agente*; es el paso siguiente del workflow. "The agent doesn't decide to send an email. The workflow does that automatically every time" (17:41).

**Ejercicio:** convertir a nodo determinista algo que se le pediría al agente como tool, y justificar la elección. Entregable: un párrafo con el criterio "¿el modelo debe decidir esto o siempre pasa?".

### Módulo 8 - Google Sheets como knowledge base (18:38 - 22:01)

**Objetivo:** tener una alternativa honesta a la vector DB para bases chicas y medianas.

- Caso: Telegram trigger → AI agent → OpenAI Chat Model → Sheet como tool → Telegram Send Answer (19:07–20:14).
- El agente está instruido a usar el tool *solo* para políticas, refunds, envíos, cancelaciones, warranty e info de empresa (19:42).
- La Sheet devuelve la fila relevante (question / answer / category) y el modelo redacta la respuesta (20:31).
- Cuándo alcanza: "This is a simpl" (21:21). "Sometimes a clean Google sheet is enough" (21:38).
- **Matiz:** el ponente dice "you don't need Pinecone, Supabase, a vector DB, or embeddings for *every* use case", no que no hagan falta nunca. La clase no cubre cuándo sí hacen falta (búsqueda semántica sobre corpus grande) — es un hueco, y por eso el propio video dice luego "vector databases" en la promesa del minuto 01:23 sin desarrollarlo.

**Ejercicio:** clasificar 5 casos propios en "Sheet alcanza" / "necesita embeddings" y justificar por volumen y tipo de matching (literal vs. semántico). Entregable: tabla con criterio explícito.

### Módulo 9 - Memoria corto vs. largo plazo (22:01 - 24:37)

**Objetivo:** hacer que el asistente recuerde después del restart.

- **Corto plazo:** Simple Memory (buffer window), contexto solo de la sesión; se pierde al cerrar (22:29).
- **Largo plazo:** persistente, en base de datos, recuperable días o meses después y entre sesiones (22:29).
- Esquema mínimo de la Sheet de memoria: `user_id`, `message`, `response`, `timestamp` (22:45).
- Orden del workflow, que es lo que hace la magia: Telegram trigger → *get conversation history* (filtrado por user id) → Code node que lo formatea → **inyección en el system message del agente** → respuesta → *log conversation turn* → Telegram (23:01–23:35).
- Loop conceptual: **retrieve history → respond → save history** (23:35).
- Ventaja de tenerlo en Sheet: se puede inspeccionar, editar y **corregir a mano** la memoria del AI (24:25).

**Ejercicio:** implementar memoria persistente con clave de usuario y probar en sesión nueva que recuerda un dato de la sesión anterior. Entregable: dos capturas, sesión 1 guardando, sesión 2 recordando, más el schema del sheet.

### Módulo 10 - Multi-agente de contenido (24:37 - 27:28)

**Objetivo:** romper un agente monolítico en roles con contrato de salida.

- Problema del agente único: "the prompt gets bloated, the model gets confused about what it's supposed to be doing right now, and quality drops" (24:59).
- Pipeline de 4 roles en serie: research → analysis → writing → publishing; "The output of one becomes the input of the next" (25:15–25:33).
- **Contratos de rol:** el research "only researches... not allowed to write anything"; analysis devuelve un outline en **JSON** (title, hook, section headings); writing produce markdown; publishing "packages everything. SEO title, meta description, tags, and marks the status as published" (25:33–26:23).
- Detalle de robustez: un Code node "parse publish package" que **limpia el JSON aunque el modelo lo envuelva en fences de markdown** (26:41).
- Trigger: webhook con un topic como input (25:50).

**Ejercicio:** diseñar un pipeline de 3 roles para un dominio propio (ej. soporte: clasificar → redactar → validar) con el schema JSON de *cada* handoff. Entregable: `pipeline.md` con los schemas y el prompt de cada rol.

### Módulo 11 - Event-driven: calificación de leads (27:28 - 32:25)

**Objetivo:** dejar de pollear y filtrar antes de interrumpir a alguien.

- Crítica al polling: "Every 15 minutes, check if something changed." (27:32). "react. Something happens" (27:49).
- Tres fuentes de evento, **intercambiables en la cabeza del pipeline**: webhooks (universal, cualquier cosa que haga HTTP), app triggers (version pre-built del webhook: Typeform, Calendly, Stripe) y database updates (Airtable, Postgres, Sheets) (28:06–28:58).
- Regla de diseño: "All three of these are interchangeable at the front of your pipe" (28:58).
- Pipeline: form → webhook → AI analyze lead → parse → **CRM entry (todos)** → IF `lead_score >= 7` → Slack hot-lead alert (29:15–31:29).
- Juicio estructurado del AI: lead score sobre 10, intent, urgency y un summary de una línea pensado para leerse en 2 segundos (30:21).
- **Filtro como disciplina:** "Not every event deserves a notification. Every lead gets logged. Only the hot ones interrupt a human" (29:48).
- **Patrón de acceso a nodos previos:** el nodo de Slack puede leer campos directo desde `parse lead analysis` en vez del nodo inmediatamente anterior (31:45) — útil cuando un nodo no arrastra todos los campos.

**Ejercicio:** rediseñar un pipeline propio de polling a evento, con una regla explícita de "qué se loguea siempre vs. qué notifica". Entregable: diagrama + tabla de umbrales.

### Módulo 12 - Human-in-the-loop (32:25 - 34:40)

**Objetivo:** poner aprobación humana donde un error cuesta.

- Fórmula en una línea: "AI does the work. A human gives the okay, then the action happens" (32:35).
- Justificación: "AI can write something that's slightly wrong, off-brand, or just weird" (32:35). Si eso va directo a un cliente, es un problema.
- Implementación: webhook → AI writer → **Slack "send and wait for response"** con botones approve/reject → IF approved → Gmail, o NoOp en reject (33:09–33:57).
- El punto técnico clave: el workflow **literalmente se detiene** esperando la respuesta humana (33:41).
- Criterio de aplicación declarado: "Anytime AI is doing something that a mistake would actually cost you" (34:32).

**Ejercicio:** identificar en un flujo propio el único punto donde falta "que un humano diga sí" y agregarlo con Slack. Entregable: el nodo con `send and wait` configurado y el run pausado.

### Módulo 13 - Error handling, retries y fallbacks (34:40 - 38:12)

**Objetivo:** hacer la diferencia entre demo y producción.

- El fallo del workflow anterior: Google Sheets, el agente o el log fallan y **el workflow falla en silencio**: "The user sends a message and gets nothing back" (34:48–35:06).
- Inventario honesto de puntos frágiles: "Three parts of this workflow depend on outside services" — Sheets, el agente, Sheets de nuevo (35:41).
- Recorrido nodo por nodo: Telegram trigger → get history → format history (interno, **no se toca**) → AI agent → OpenAI Chat Model (**no se toca**) → simple memory (**no se toca**) → log conversation turn → Telegram Send Answer → **notify error to user** (35:58–37:21).
- **Solo se tocan los nodos que llaman servicios externos**; los internos quedan. Criterio de eficiencia, no de completitud.
- Las tres capas: **retry** si falla el servicio externo, **fallback** al usuario si sigue fallando, **alerta al owner** por Telegram si se rompe el workflow (37:38).

**Ejercicio:** auditar un workflow propio y clasificar cada nodo en externo/interno, luego definir retry, fallback y alerta para cada externo. Entregable: tabla nodo → tipo → política.

### Módulo 14 - Monitoreo, observabilidad y costo de tokens (38:12 - 43:05)

**Objetivo:** saber que algo falló *antes* de que lo pregunte un cliente.

- El diagnóstico del ponente: "If one of your automations started failing right now, would you know?... for most people building with n8n, the honest answer is no" (38:12–38:29).
- **Tres métricas:** execution time (un pico = algo lento o trabado), failure rate (una falla es normal, una tendencia creciente no), y AI token usage (directo a la factura) (39:38).
- **Tres herramientas:** logs (qué pasó y cuándo), alerts (aviso cuando cruza un umbral) y metrics dashboard (tendencias, no un número aislado) (39:53).
- Pieza 1: Schedule trigger horario → *get recent executions* contra la **API propia de n8n** → Code node *calculate metrics* (total, fallidos, failure rate %, promedio de segundos) → append a Sheet → **IF failure rate >= 10 % → Telegram**; si no, silencio (40:11–41:03).
- Pieza 2: el objeto `token usage` (prompt / completion / total tokens) que **toda respuesta de AI agent ya trae** y casi nadie mira; un Code node lo extrae a su propia tab (41:03–41:37).
- La idea reutilizable: no es un workflow a correr aparte, es un patrón para **copiar dentro de cualquier agente** y tener costo por llamada (41:37).
- Cierre: "no fancy tools, no expensive software" — un schedule check, una Sheet como log y dashboard, y Telegram como early warning (42:10). Estimación del ponente: ~20 minutos de setup (42:10). *Es una estimación, no una medición.*

**Ejercicio:** implementar el logger de métricas contra la API de la propia instancia y el extractor de tokens en el workflow más usado. Entregable: Sheet con ≥3 filas horarias y una tab de tokens; alerta probada con umbral bajo.

## Ejercicios por bloque

- [ ] Módulo 1 — `mi-caso.md` con la justificación de n8n vs. Zapier.
- [ ] Módulo 2 — tabla de triggers por familia (5 familias).
- [ ] Módulo 3 — workflow form-to-AI con rama false cableada + execution logs.
- [ ] Módulo 4 — tercer tool read-only y dos runs contrastados.
- [ ] Módulo 5 — API paginada de 2 páginas a Sheet, Code node comentado.
- [ ] Módulo 6 — prompt con schema + campos obligatorios que disparan humano.
- [ ] Módulo 7 — criterio "¿decisión del modelo o paso fijo?" aplicado a un caso propio.
- [ ] Módulo 8 — tabla Sheet vs. embeddings para 5 casos.
- [ ] Módulo 9 — memoria persistente probada en sesión nueva.
- [ ] Módulo 10 — pipeline de 3 roles con schema de cada handoff.
- [ ] Módulo 11 — conversión de polling a evento + umbrales de notificación.
- [ ] Módulo 12 — nodo de aprobación con run pausado real.
- [ ] Módulo 13 — auditoría nodo → externo/interno → retry/fallback/alerta.
- [ ] Módulo 14 — logger de métricas + extractor de tokens funcionando.

## Banco de preguntas para estudiar

1. ¿Por qué el módulo 3 se llama "el esqueleto de todo lo que sigue"? Nombrá los cuatro pasos del patrón y mostrá cómo reaparecen en el módulo 11.
2. Si el agente ya sabe mandar emails por un tool, ¿por qué el ponente insiste en que el Send Email *no* sea un tool? Qué se pierde en cada diseño.
3. El módulo 8 dice que una Sheet alcanza como knowledge base. ¿En qué condiciones deja de alcanzar, y qué evidencia pedirías antes de saltar a embeddings?
4. En el multi-agente, ¿qué función cumple que cada rol devuelva un schema fijo y no texto libre? Relacionarlo con el Code node que limpia fences de markdown.
5. ¿Qué tres nodos del workflow de memoria **no** se tocan al agregar error handling, y por qué ese recorte es la decisión correcta?
6. "Production systems don't poll, they react." ¿Qué casos legítimos quedan para un schedule trigger y cómo se verían en el monitor del módulo 14?
7. El umbral de failure rate es 10 % y el lead score 7. ¿Son números arbitrarios? ¿Cómo los calibrarías sin datos históricos?
8. ¿Por qué el flujo de human-in-the-loop necesita que el workflow *se pause*, en lugar de solo notificar y seguir?
9. De todo el curso, ¿qué claim del ponente es verificable y cuál es solo anécdota? Mencioná al menos tres y separalos.

## Notas editoriales

- **Evidencia vs. anécdota.** Los claims "the number one creator on NAN" (00:33), "transform over 1200 plus b" (00:33) y "Zapier is just a small subset" (01:06) son afirmaciones del ponente sin fuente; la clase los registra como auto-presentación, no como dato medido. Lo verificable dentro del video es el comportamiento de los workflows, que sí se muestra corriendo.
- **Números deformados por el ASR / imprecisos en el audio.** El plan "starter" con "around 2,00 to 2500 workflow executions" (01:58) está mal transcripto; no se toma como precio ni como límite real. Igual criterio para "just a schedule check" (42:10): es estimación del ponente.
- **Proveedor de VPS.** El ASR devuelve "CBO cloud"/"CBT cloud", que no corresponde a ningún proveedor real; la clase no afirma cuál. El flujo de self-hosting es independiente del proveedor.
- **La promesa del minuto 01:23 incluye "vector databases", y el módulo 8 solo ofrece la alternativa sin vector DB.** No hay desarrollo de cuándo usar embeddings. Queda registrado como hueco del curso, no como contenido enseñado.
- **Los nombres de nodos y del producto fueron normalizados** (n8n, Rahul Joshi, SerpAPI, bill of lading, consignee, OpenAI) contra el glosario de `transcripcion.md`; los cues del transcript quedaron intactos.
- **Contenido promocional recurrente.** Cada módulo cierra empujando la "school community" y JSONs por comentario ("comment agents", "comment approve", "comment errors", "comment monitor"). Es el modelo de negocio del canal y no forma parte del contenido técnico; se omite deliberadamente.
- **Acciones externas:** nada de esta clase requiere publicar ni enviar nada hacia afuera. Los workflows descritos usan credenciales propias (SerpAPI, Telegram, Slack, Gmail, OpenAI) y se montan en la instancia local.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
