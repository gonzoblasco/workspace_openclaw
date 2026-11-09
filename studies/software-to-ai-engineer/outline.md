# Clase: De Software Engineer a AI Engineer — El Roadmap Más Realista

Clase de estudio construida a partir del video de **Fazt**. Transcripción ASR en
`transcripcion.md`.

## Ficha

- Fuente: https://www.youtube.com/watch?v=qLobAfve9b0
- Canal: Fazt (@FaztTech)
- Título: «De Software Engineer a AI Engineer: El Roadmap Más Realista»
- Ponente: Fazt
- Duración: ~32:36 (transcript hasta 1955s + cierre)
- Idioma: español (subtítulos automáticos)
- Tipo: roadmap de carrera + mapa de conceptos (no tutorial)
- Bloque NO contenido: 0:40–1:40 es publicidad (Cynode).

## Resultado esperado

1. Distinguir AI Engineer / ML Engineer / AI Researcher / MLOps.
2. Verificar si ya tienes las bases para saltar (lenguaje, DB, frontend, Git, redes, Docker).
3. Explicar por qué System Design es el puente entre dev tradicional y dev con IA.
4. Nombrar bases de LLM: tokens, ventana de contexto, temperatura, roles.
5. Usar una API de IA y estimar costo por token.
6. Diferenciar suscripción (desarrollar) vs API (producto).
7. Diseñar integraciones prácticas: chat, clasificación asíncrona, manejo de errores.
8. Situar prompt engineering y function calling (tools) en su justa medida.
9. Entender RAG y bases de datos vectoriales.
10. Nombrar otras interfaces: skills, CLI, MCP.
11. Entender Deploy / LLM Ops.
12. Elegir un primer proyecto (RAG) y hoja de ruta personal.

## Mapa temporal (aprox.)

| Tiempo | Bloque |
|---|---|
| 0:00–0:40 | Intro y promesa |
| 0:40–1:40 | Publicidad (Cynode) — ignorar |
| 1:40–4:00 | Bases web: DB / API / frontend |
| 4:00–6:40 | Roles en IA |
| 6:40–10:40 | AI Engineer = dev + IA; bases; System Design |
| 10:40–13:00 | Bases LLM |
| 13:00–17:00 | APIs, proveedores, costo, suscripción vs API |
| 17:00–21:00 | Prompt engineering y function calling |
| 21:00–24:00 | RAG y vector DB |
| 24:00–28:00 | Skills, CLI, MCP, frameworks |
| 28:00–30:00 | Deploy / LLM Ops |
| 30:00–32:00 | Resumen y recomendación (RAG) |
| 32:00–32:36 | Cierre |

## Módulo 0 — Marco y premisa

**Idea fuerza (0.12s–26.8s):** «Un roadmap sencillo… es como una continuación del desarrollo de software y cualquiera puede aprender si ya sabe el desarrollo de software básico.»

**Concepto:** dirigido a quien ya sabe desarrollar. No es carrera nueva ni investigación de modelos; es **capa de IA sobre dev tradicional**.

**Preguntas:**
- ¿Qué parte de tu stack ya cumple la base que el video asume?
- ¿Qué te falta hoy para llamarte AI Engineer con honestidad?

## Módulo 1 — Bases del desarrollo web (prerrequisito)

**Bases implícitas (160s–260s):** DB (SQL/NoSQL), API/backend (Go, Python, JS/TS, Java, .NET), frontend, auth/seguridad/debug/testing.

**Herramientas del dev (470s–540s):** lenguaje con sintaxis, DB SQL (Postgres recomendado), frontend, Git, redes (HTTP, UDP, FTP), Docker y nociones de nube.

**Nota:** checklist sin rutas de aprendizaje (el ponente promete video "desde cero").

## Módulo 2 — Roles en IA

| Rol | Qué hace | Nivel |
|---|---|---|
| AI Engineer | Crea apps que **usan** modelos IA | Práctico |
| ML Engineer | Entrena/adapta/tunea modelos | Avanzado |
| AI Researcher | Diseña modelos, escribe papers | Muy avanzado (PhD) |
| MLOps/DevOps IA | Despliega y opera modelos en cloud | Transversal |

**Claim cuidadoso:** las descripciones del ponente son orientativas, no estándar universal.

## Módulo 3 — Qué es un AI Engineer en la práctica

**Definición:** quien crea aplicaciones (DB, API, frontend) **usando modelos de IA**. No entrena ni diseña modelos.

**System Design (540s–660s):** pensar en servicios, conexiones y despliegues; mapeo de la app. Recursos: repos "System Design" y "System Design Primer". Aporte clave: un sistema con IA es igual al web, salvo "nuevos recuadros" (IA).

**Ejercicio 1:** diagrama de un CRUD con auth + un componente de IA (ej. generar resumen). Identificar servicios, datos de salida, almacenamiento.

## Módulo 4 — Bases de LLM

Conceptos mínimos:
1. **Tokens** — fragmentación y cobro/límite.
2. **Ventana de contexto** — cuánto se puede conversar antes de divagar.
3. **Temperatura** — 0 = fidelidad; alto = creatividad.
4. **Roles:** `system`, `user`, `assistant`.

## Módulo 5 — APIs de IA, proveedores y costo

**Proveedores:** OpenAI (GPT 5.5/5.6, GPT Image) y Anthropic (Claude Opus/Sonnet/Haiku/Fable).

**Costo:** por millón de tokens. Clientes suelen asumir que $100–200 da IA "ilimitada" dentro del producto: falso.

**Suscripción vs API (880s–920s):**
- Suscripción ($20/$100/$200) = para **desarrollar** (subsidio de las empresas).
- API (por token) = para **el producto** del cliente.
- No son intercambiables.

**Alternativas (940s–980s):** modelos chinos más baratos para features simples; para tareas complejas (imágenes con pocos detalles, archivos grandes, máxima precisión) OpenAI/Anthropic responden mejor. Self-hosting prometido en otro video.

**Ejercicio 2:** estimar tokens y costo por 1.000 usos de una feature (ej. resumir email). Decidir si vale.

## Módulo 6 — Integraciones prácticas

Patrones:
1. Chat en app.
2. Automatización por evento (email → IA resume/valida/clasifica → persiste).
3. Asistencia en despliegue (error → IA corrige código → re-push → redeploy; complejo y costoso).

**Manejo de errores (1020s–1060s):** fallos, formatos (`text`, `json`, `html`), concurrencia. Terreno conocido para un dev.

**Ejercicio 3:** elegir un proceso manual y diseñar flujo evento → IA → persistencia, con fallback.

## Módulo 7 — Prompt engineering y function calling

**Prompt engineering (1180s–1260s):** "cómo pedirle algo a la IA". Los modelos actuales (Claude 4) ya interpretan bien el contexto; no hace falta over-engineering. Pero en apps propias sigue siendo clave definir comportamiento del sistema ("Eres un clasificador de correos").

**Function calling / tools (1260s–1320s):** la IA ejecuta código (funciones del sistema) en vez de solo responder. Ej.: clasificar/eliminar un correo → la IA llama a la función.

**Nota editorial:** el video le resta épica al prompt engineering y la da al function calling. Ambos importan, pero function calling habilita automatización real.

## Módulo 8 — RAG y vector DB

**RAG (1320s–1360s):** permite a la IA leer/responder sobre **tus datos** (DB, docs, Excels, inventarios). Se vectorizan y el modelo consulta ese formato.

**Vector DB (1380s–1440s):** DB paralela a la de negocio en formato vector. Puede vivir en Postgres (`pgvector`) o en especializada (Pinecone, Chroma).

**Ejercicio 4:** RAG mínimo sobre 20 docs: origen → chunking → embedding → storage → consulta → respuesta con cita.

**Recomendación del ponente (1880s–1920s):** "Empiecen con el RAG… y luego MCP".

## Módulo 9 — Otras interfaces

1. **Skills (1480s–1500s):** definir prompt y reutilizar (ligero, minutos).
2. **CLI (1460s–1480s):** cliente de consola que consulta tu API.
3. **MCP (1500s–1580s):** "traductor" entre chat existente (ChatGPT/Claude Desktop) y tu API. Ventaja: el usuario paga su suscripción; tú solo despliegas el traductor. **Seguridad:** diseñarlo como API (no exponer datos indebidos).
4. **Frameworks (1660s–1680s):** LangChain, LlamaIndex, Temporal, Inngest (útiles, no obligatorios al principio).

## Módulo 10 — Deploy / LLM Ops

**Escenarios:** (1) modelo en nube propia (AWS/GCP/Azure), pagas por uso de nube; (2) self-hosted/local.

**Problemas operativos (1760s–1800s):** rate limiting, model routing, caché, escalado, costos.

**Concepto LLM Ops:** "mandar a producción modelos inteligentes"; igual que apps web pero con costo por inferencia.

## Módulo 11 — Cierre y hoja de ruta

- Empieza por **RAG**.
- Luego prueba **MCP**.
- Subir de nivel: entrenamiento/tuning o funcionamiento interno (ya es ML).

**Mapeo de roles (1860s–1880s):**
- AI Engineer → genera aplicaciones (más cercano a dev software).
- ML Engineer → trabaja con modelos (deploy, tuning, config).
- AI Researcher → diseña modelos (fundamento de todo).

## Aplicación a tu perfil (Gonzo)

Contexto: React/TS, Supabase/Edge Functions, billing, tooling; 10 años dev; inglés B2.

**Ya cumple:** lenguaje (TS), DB (Supabase/Postgres), frontend (React), Git, Docker (parcial), APIs REST.

**Gaps:** System Design explícito, bases LLM (práctica), API de IA integrada con costo, RAG end-to-end.

**Plan 4 semanas:**
- Semana 1: bases LLM + costo (experimentos con Anthropic/OpenAI, medir tokens).
- Semana 2: integración sin chat (Edge Function que clasifique/resuma, fallback).
- Semana 3: RAG mínimo (pgvector + embeddings + cita de fuente).
- Semana 4: chat mínimo en React o MCP mínimo + mini System Design.

**Notas vinculadas:** `memory/user-profile.md`, `memory/career-facts.md`, `studies/entrevistas-tecnicas/`.

## Preguntas para estudiar contigo

1. Roles: ¿a cuál apuntas en 12 meses y por qué?
2. Bases: ¿cuál es tu gap más grande hoy?
3. System Design: dibujemos juntos una app tuya con IA agregada.
4. LLM bases: explícame tokens/contexto/temperatura con ejemplo tuyo.
5. API + costo: calcula costo de una feature por 1.000 usos (Anthropic vs OpenAI).
6. Suscripción vs API: ¿cómo se lo explicas a un cliente?
7. Integración sin chat: ¿qué proceso manual automatizarías primero?
8. Prompt engineering vs function calling: ¿cuál pesa más en un producto real?
9. RAG: ¿qué corpus pequeño usarías de primer experimento?
10. Deploy: ¿self-hosted o API externa para un primer proyecto?
11. Crítica: ¿qué afirmaciones son evidencia y cuáles opinión del ponente?

## Mención y citas clave

- 0.12s–26.8s: roadmap sencillo, continuación del desarrollo de software.
- 240s–260s: ML Engineer entrena/adapta modelos.
- 340s–360s: AI Researcher diseña modelos.
- 400s–420s: suma de desarrollo típico + herramientas de IA.
- 540s–560s: System Design.
- 680s–700s: tokens.
- 700s–720s: temperatura.
- 760s–780s: API de IA.
- 880s–900s: suscripción subsidia, no cubre costo.
- 1180s–1220s: prompt engineering mala reputación; Claude 4 interpreta mejor.
- 1260s–1320s: function calling ejecuta código.
- 1320s–1360s: RAG.
- 1500s–1540s: MCP como traductor.
- 1700s–1740s: LLM Ops.
- 1880s–1920s: empezar por RAG.

## Notas editoriales

- Transcripción auto-generada: puede tener errores (nombres, números, términos). Verificar citas contra audio.
- Afirmaciones sin fuente (subsidio de suscripciones, modelos chinos, self-hosting): tratar como opiniones informadas.
- El video es roadmap perspectivo, no tutorial. Buscar docs oficiales antes de implementar (Anthropic, OpenAI, Supabase/pgvector).
- La publicidad (0:40–1:40) no es contenido; se conserva solo por fidelidad.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
