# Spec: la cadena OSS -> LinkedIn, con LangGraph 🌿

**Creado:** 2026-10-22
**Origen:** sesion del 2026-10-22 sobre el research externo de OpenClaw + LangChain (verificado en
`docs/research/2026-10-22-verificacion-claims.md`). Gonzo pidio: *documentemos el 1, agreguemoslo a su
roadmap pero no lo hagamos ahora, y luego avancemos con el 2*.
**Rol dueno:** kanam-mind (la skill que gobierna los posts ya es de MIND)
**Estado:** PROPUESTO - pendiente de delegacion
**Complejidad:** T=17 (HIGH-CRITICAL) - **requiere confirmacion de Gonzo antes de implementar**
**Relacionado:** ADR-099 (LangChain es capa de ejecucion, no orquestador), ADR-083 (frontera de roles),
ADR-100 (fuente unica), ROADMAP 2.2 (cadena OSS -> LinkedIn)

---

## 1. Lo que ya existe (y por que NO hay que construirlo)

**La skill `linkedin-merge-post` ya hace este workflow entero.** Vive en el workshop de MIND
(`~/.openclaw/agents/kanam-mind/agent/workshop-skills/linkedin-merge-post/SKILL.md`), son 8 pasos
completos, y fue verificada el 2026-09-14 sobre `carbon-design-system/ibm-products #9878`:

| paso | que hace |
|---|---|
| 1 | Identificar el merge (`gh search prs --author=@me --merged`) |
| 2 | **Decidir elegibilidad**: solo PR propio mergeado; el credito de un maintainer es material de entrevista, no de branding |
| 3 | **Sacar los hechos de GitHub, nunca de memoria**: issue, PR body, reviews, diff real |
| 4 | Clasificar el nicho (a11y / Agentic / Fullstack) y elegir el angulo |
| 5 | Escribir el draft a `docs/linkedin/<repo>-<topic>.md` |
| 6 | **Pasar los dos gates de publicacion** |
| 7 | Entregar, registrar los cambios de criterio, commit y push |
| 8 | **Despues de publicar**, voltear el `Status:` a publicado y tratar los comentarios entrantes como informacion |

**Consecuencia directa: esto NO es un workflow para construir. Es un workflow para cerrar.** La
pregunta correcta no es "como hago el grafo", sino "que le falta a esta skill para que la cadena
funcione sola".

---

## 2. Lo que se midio (el diagnostico)

| # | Hecho medido | Fuente |
|---|---|---|
| 1 | **4 drafts esperando OK desde el 2026-10-01** (el 2026-10-07 el ultimo). Ninguno se publico | `stat` de `docs/linkedin/*.md` |
| 2 | **2 merges sin post**: `adobe/react-spectrum #10503` y `carbon-design-system/carbon #22887`. Los dos son **a11y**, o sea material valido por la regla | `gh api` + DB `contributions` |
| 3 | **2 de 10 posts publicados.** El ROADMAP 2.2 pide 3+ publicados y "1 post por merge dentro de la semana" | `docs/linkedin/` |
| 3b | **11 PRs mergeados distintos** en la DB (12 filas, con un duplicado): 10 de a11y + 1 de CI. **Ninguno del nicho agentic ni del fullstack** | `memory.db` tabla `contributions` + titulos via `gh api` |
| 4 | **El gate obligatorio del paso 6 esta muerto.** La skill exige el "anti-ai pass" de `skills/anti-ai`. **Ese directorio no existe**: se elimino en la reestructuracion del 2026-09-22 (16 stubs vacios eliminados, entre ellos `anti-ai`). El paso 6 es inejecutable tal como esta escrito | `ls skills/anti-ai` + `memory/2026-09-22.md` |
| 5 | **La regla de branding apunta a un lugar equivocado.** La skill dice que la politica de los 3 nichos vive en `MEMORY.md`. **`MEMORY.md` tiene 0 menciones de "nicho"**; la regla real esta en `memory/user-profile.md:47` | `grep -c` |
| 6 | **No hay corpus de ediciones de posts.** `docs/voz-gonzo.md` tiene 3 casos de **ediciones de Gonzo** sobre mensajes a personas, pero de posts publicos no hay ninguno. El loop de aprendizaje no existe para esta cadena | `docs/linkedin/` |
| 7 | **El post canonico se autodescribe.** `astryx-5419.md` tiene una seccion "anatomia del estilo" de 6 puntos + "notas para futuros posts". **Esa es la spec del formato** - no hace falta inventarla | `docs/linkedin/astryx-5419.md` |
| 8 | **`content-serializer` tambien se referencia y no existe** (linea 41 de la skill). Referencia muerta secundaria | `find` en todos los workshops |
| 9 | La skill tiene `disable-model-invocation: true` | su frontmatter |

### El hallazgo de fondo

> **La cadena no falla por falta de capacidad. Falla por falta de cierre.**

El paso 7 dice "commit and push" y el paso 8 dice "flipear el status a publicado". Pero un post
publicado **en LinkedIn** no es un commit: es una accion externa. Y el primer dia que un post quedo
publicado y su archivo seguia diciendo `draft para revision de Gonzo` (verificado por la propia skill
el 2026-09-14), el archivo se quedo mintiendo. **Cuatro drafts llevan tres semanas esperando un OK
que el flujo no pide de forma explicita.** Ese es el cuello de botella, y no lo arregla un grafo
mas inteligente: lo arregla un gate que exija la publicacion y su registro.

**Y hay una ironia util:** los dos merges sin post (#10503, #22887) son **los dos unicos casos
documentados de post publicado con exito**. O sea, el material mas valioso ya se identifico, se
redacto y se publico. Lo que no se cierro fue el **registro**: el post de #5419 sigue diciendo
`PUBLICADO 25/08/2026` mientras el de #10503 no existe como archivo.

---

## 3. Que es un grafo LangGraph y que NO es

### Lo que un grafo daria (real)

- **Estado tipado** entre los 8 pasos: hoy el estado vive en el contexto de la conversacion y en el
  archivo markdown, sin tipar. Con un `TypedDict` (`MergeFacts`, `NicheDecision`, `DraftPost`,
  `PublishState`) cada paso declara que consume y que produce, y un paso mal formado falla en el borde.
- **Reanudacion**: el paso 3 (leer la historia del PR) y el paso 5 (redactar) son los caros. Con
  `langgraph-checkpoint` (ya instalado y **sin usar** en `langchain-starter`, ADR-099) el grafo
  retoma del ultimo super-step correcto en vez de re-leer todo.
- **`interrupt()` para la aprobacion**: el paso 6/7 es exactamente el caso de uso - el grafo se
  detiene, espera el OK de Gonzo, y **reanuda con el mismo `thread_id`**. La idempotencia que exige
  la doc oficial ("the node restarts from the beginning of the node where the `interrupt` was called")
  aplica: el nodo de "escribir el post" tiene que ser idempotente.
- **Un gate de publicacion verificable** en vez de un recordatorio en prosa: el grafo no puede avanzar
  a "publicado" sin que exista el archivo con `Status: PUBLICADO <fecha>` y la URL real.

### Lo que un grafo NO arregla

- **La publicación en LinkedIn es una acción externa.**Sigue requiriendo OK explicito de Gonzo
  (AGENTS.md: "Nada sale sin un si explicito"). El grafo puede *preparar* y *recordar*; no puede
  publicar solo.
- **La calidad editorial.** La skill `linkedin-merge-post` tiene las reglas de fondo que un grafo no
  puede verificar: el angulo, el tono, el criterio de a11y que hace que un post conecte.
- **La cadencia.** Es una decision humana ("1 post por merge dentro de la semana" es un compromiso).

### El veredicto honesto

**El caso de LangGraph aqui es mas debil que en el chat RAG de OnWheels.** Allá el grafo reemplaza
codigo que no existe. Acá el grafo **reemplaza una skill de 8 pasos que ya funciona** y le agrega dos
capacidades reales (estado tipado y aprobacion reanudable) y una capacidad que de verdad falta
(**el gate de cierre**).

Por eso la propuesta es **incremental y en este orden**, y por eso la **Fase 0 de esto no es
LangGraph en absoluto**: es arreglar los tres gates rotos, que son gratis.

---

## 4. Alcance

### Fase 0 - Cerrar los gates rotos (SIN LangGraph, sin proyecto nuevo)

Esto es lo que desbloquea la cadena hoy, y son tres fixes:

| # | Fix | Que estaba roto | Como se verifica |
|---|---|---|---|
| 0.1 | **Decidir que se hace con el gate "anti-ai"** | El paso 6 de la skill exige un gate que no existe | La skill dice que gate se corre. Si no hay equivalente, se dice explicitamente y se sustituye por uno real |
| 0.2 | **Corregir el puntero de la politica** | La skill dice `MEMORY.md`; la regla esta en `memory/user-profile.md:47` | La skill apunta al lugar real |
| 0.3 | **Escribir los 2 posts que faltan** (#10503, #22887) | 2 merges a11y sin material | Los 2 archivos existen con el shape de `astryx-5419.md` y pasan el gate de guiones |

Y un cuarto, que es el que mas valor tiene y el que menos trabajo da:

| # | Fix | Por que |
|---|---|---|
| 0.4 | **Un gate de "publicado" verificable**: un script que recorra `docs/linkedin/*.md` y falle si hay un `Status: draft` con mas de N dias, o si un merge elegible no tiene post | El cuello de botella medido son 4 drafts de 3 semanas. Un recordatorio en prosa no lo evita; un gate sí |

**Nota de alcance:** 0.1 a 0.4 **no son trabajo de LangChain**. Son trabajo de MIND (su propia skill) y
de un script del workspace. Se documentan aca porque son el **prerrequisito** de que la cadena valga
algo, pero no dependen de esta spec.

### Fase 1 - El grafo (recien ahi, y con la justificacion medida)

**Precondicion para empezar:** la Fase 0 esta hecha y hay al menos **un post nuevo** que haya pasado
por el grafo de punta a punta. Sin eso, el grafo es un modelo de un proceso que nunca corrio.

| pieza | decision | estado |
|---|---|---|
| Donde vive | `projects/oss-post-graph/` (repo propio, venv propio). **ADR-099 §4**: proceso separado, venv y `requirements.txt` pineados, sin acople por dependencias | Abierta |
| Como se invoca | **MCP stdio** (`mcp<2`, FastMCP 1.30.0) - medido: resuelve con los pines de `langchain-starter` intactos, 0 conflictos, sin Postgres, sin `LANGGRAPH_CLOUD_LICENSE_KEY`, sin LangSmith. El mismo patron que ya usa `browser-use` | **Medido** |
| Checkpointer | `langgraph-checkpoint-sqlite` - medido: resuelve con `langgraph 0.6.11` + `langgraph-checkpoint 2.1.2`, 0 conflictos. `langgraph-checkpoint 2.1.2` ya esta instalado y sin usar en `langchain-starter` | **Medido** |
| Modelo de los pasos | Ollama local via `langchain-ollama`, como el starter | Abierta |
| Estado tipado | `TypedDict` por paso. Los **hechos del PR se escriben a disco** (markdown o JSON), no al modelo: el grafo Orquesta, la verdad vive en el archivo | Abierta |
| Aprobacion | `interrupt()` antes de "publicar". Idempotente: el nodo de escritura se puede re-ejecutar | Abierta |
| Que NO hace | No publica en LinkedIn. No decide el nicho (lo decide MIND). No inventa hechos (los lee de `gh`) | **Firme** |

### Lo que NO entra (y por que)

| Fuera | Motivo |
|---|---|
| Publicar solo, sin OK | Regla dura de AGENTS.md. El grafo prepara; Gonzo publica |
| El grafo decide el nicho o el angulo | Es criterio editorial de MIND (paso 4 de la skill). Un grafo que elige el angulo es un generador de contenido sin criterio |
| Memoria propia del grafo (preferencias, historial) | ADR-099 §3: seria una segunda base de memoria. El learning loop vive en `docs/linkedin/` (ver 0.4 / F2) |
| Un cron que genere posts solo | ADR-099 §3: seria un segundo scheduler. `automations` es el scheduler |
| Reemplazar la skill | El grafo la **invoca por pasos**, no la borra. La skill es el procedimiento; el grafo es el carrier de estado |
| Un proyecto en `skills/` | ADR-083: una skill de rol vive en `agents/<rol>/skills/`, no en `skills/` |

---

## 5. Lo que el research aporto y lo que no (esta spec es el resultado)

El research externo (§4.3 del research) proponia un revisor de codigo como grafo con
WRITE -> SELECT -> COMPRESS -> ISOLATE. **La forma es buena y ya esta hecha a mano**: la revision
adversarial que se usa en `docs/entrevistas/` tiene exactamente esa forma (severidad, evidencia,
veredicto accionable), y `pr-review-response` cubre el caso de PR.

Lo que el research **no vio**, y es lo que esta spec propone: **el cuello de botella de la cadena
OSS->LinkedIn no es la redaccion, es el cierre.** 4 drafts de tres semanas y 2 merges a11y sin
material no son un problema de capacidad de escritura.

Y el aporte tecnico real del research que **si** se sostiene: el `checkpointer` por super-step con
pending writes (verificado en la doc oficial: *"LangGraph stores pending checkpoint writes from any
other nodes that completed successfully at that super-step. When you resume... you don't re-run the
successful nodes"*), y la regla de idempotencia antes de un `interrupt()`. Ambas cosas hacen falta
exactamente en el paso 3 (leer la historia) y el paso 5 (escribir).

---

## 6. Preguntas abiertas (para Gonzo)

1. **El gate "anti-ai":** ¿se reconstruye, se sustituye por otro, o se saca del paso 6 y se deja solo el de guiones? (hoy la skill exige un gate inexistente: eso hace el paso inejecutable)
2. **El umbral del gate de cierre:** ¿cuantos dias sin publicar cuentan como "abandonado"? (medido: hay drafts de 21 dias)
3. **¿El grafo escribe el archivo, o arma el material y lo escribe MIND?** (el grafo escribiendo el post completo es mas automatico; el grafo armando el material y MIND redactando conserva el criterio)
4. **¿Nicho Agentic/AI-Native:** hay merges mergeados de ese nicho? **Medido: no hay ni uno.** La DB registra **11 PRs mergeados distintos** (12 filas, con un duplicado) y **10 son de a11y** (aria, screen reader, foco, anuncio) y **1 es de CI** (`facebook/astryx #4914`, fallback de diff de dos puntos). **Ninguno es del nicho agentic/AI-Native ni del fullstack.** O sea: de los 3 nichos de branding, **solo el a11y tiene material propio**. Los otros dos son hoy declaracion, no backlog. Eso no es un bug: es que la regla de 3 nichos se escribio el 2026-08-25 y el material propio todavia no llego. La pregunta es si se ajusta la regla o se produce el material
5. **¿Se unifica el corpus de ediciones?** (hoy `docs/voz-gonzo.md` excluye explicitamente los posts de branding, y los posts no tienen corpus propio. O se amplia el alcance de `voz-gonzo` a posts, o se crea un corpus aparte)

---

## 7. Criterio de exito

- [ ] Los 2 merges a11y sin post tienen archivo, con el shape de `astryx-5419.md` y el gate de guiones en OK
- [ ] El gate de cierre existe y corre, y detecta el caso de los 4 drafts actuales
- [ ] La skill de MIND no apunta a un gate inexistente ni a un archivo equivocado
- [ ] **Un post nuevo recorre el grafo de punta a punta**, y se puede mostrar el estado reanudable
- [ ] El grafo **nunca** publica: el paso de publicacion queda esperando OK de Gonzo

---

## Trazabilidad

- La skill que gobierna la cadena: `~/.openclaw/agents/kanam-mind/agent/workshop-skills/linkedin-merge-post/SKILL.md`
- El post canonico (la spec del formato): `docs/linkedin/astryx-5419.md`
- La regla de branding (3 nichos): `memory/user-profile.md:47` - **no** `MEMORY.md`
- La cadena en el roadmap: `docs/ROADMAP.md` §2.2
- La frontera de capa: `docs/adr/ADR-099-langchain-capa-de-ejecucion.md` (secciones 1, 2, 3 y 4)
- La frontera de rol: `docs/adr/ADR-083-frontera-de-roles-core-no-escribe-codigo.md`
- El research verificado: `docs/research/2026-10-22-verificacion-claims.md`
- El otro workflow documentado (sin implementar): `projects/onwheels/.knowledge/ROADMAP.md` §F2.R

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
