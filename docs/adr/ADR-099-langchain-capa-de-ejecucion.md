# ADR-099: LangChain es la capa de ejecución de flujos, no el orquestador

**Fecha:** 2026-10-19
**Estado:** Aceptado
**Actualizado:** 2026-10-22
**Decisores:** Gonzo / Kanam
**Origen:** sesión 2026-10-19 - Gonzo: *"amaria empecemos a usar langchain en la practica común"*. Al ir a decidir el alcance se midió el starter contra el disco y apareció que su estrategia declaraba un índice de 4.423 vectores que no existe.
**Relacionado:** ADR-066 (guardias no leen código de proyecto), ADR-073 (multi-agente), ADR-074 (despacho), ADR-077/088/089 (pipeline A/B), ADR-083 (frontera de roles), ADR-090 (modelos por rol), ADR-098 (`projects/` dentro del workspace)

---

## Contexto

`projects/langchain-starter` existe desde el 2026-09-24, completo y corriendo como servicio permanente (`127.0.0.1:8100`, LaunchAgent + watchdog, verificado hoy: `/health` responde 200). `docs/LANGCHAIN_STRATEGY.md` lo presenta como la base de las herramientas internas del ecosistema, con siete fases planificadas.

> **Actualización 2026-10-28 (no cambia la decisión, cambia el estado).** El starter se **retiro del disco**
> en la limpieza de `projects/` (21 -> 3). El codigo sigue en el repo privado `gonzoblasco/langchain-starter`.
> Se descargaron su LaunchAgent, su watchdog y la automation de salud del gateway. Lo que este ADR
> decide, **LangChain es la capa de ejecucion de un flujo, no el orquestador**, sigue vigente y no
depende de que el starter exista: el patron RAG queda como referencia de implementacion a clonar
> desde el repo, y el primer flujo real sigue siendo la decision pendiente de la seccion 2.

Lo que nunca se decidió fue **qué capa ocupa**. La pregunta quedó abierta desde el principio y se resolvía por inercia: el starter tiene un agente ReAct, y OpenClaw también tiene agentes, así que ambos parecían competir por el mismo lugar.

### Lo medido hoy contra el disco

El starter está sano como servicio, pero su estrategia miente sobre su alcance. Verificado:

| Afirmación en `LANGCHAIN_STRATEGY.md` | Medido el 2026-10-19 |
|---|---|
| Fase 5.2 "el scanner cubre 3 fuentes: proyectos + `docs/` + `skills/`" | **No existe ese scanner.** `store.py` acepta rutas por argumento, una por una. Ningún script recorre fuentes. |
| "Índice: 4423 vectores (eran 1243)" | **10 embeddings** en la colección `starter_knowledge`, de un solo documento. `chroma.sqlite3` sin modificar desde el 2026-09-24 18:39. |
| "10 tests en el starter + 25 en kanam-insight" | 10 tests correctos; **`kanam-insight` no existe** en `projects/` y el propio documento lo declara descontinuado en otra sección. |
| "Es la base sobre la que se construyen las herramientas internas del ecosistema" | Ningún consumidor real. El único citado está descontinuado. |

Es el mismo patrón que el documento ya se auto-diagnosticó en su §5b: *"documentación que declara un estado que ya no es cierto, sin nada que lo verifique"*. La corrección de entonces fue acotada al documento; no tocó las cifras.

**Consecuencia para esta decisión:** el starter no es hoy una base de conocimiento. Es un **esqueleto verificado** (RAG, agente, API, servicio) con un corpus de demo. Cualquier plan de adopción amplia que asuma lo contrario arranca sobre una premisa falsa.

---

## Decisión

**Se adopta LangChain como capa de ejecución de flujos de IA dentro de proyectos. No reemplaza la orquestación del gateway, ni la memoria, ni el scheduling.**

### 1. Reparto de responsabilidades (fijo)

| Capa | Dueño | Qué hace |
|---|---|---|
| Orquestación de agentes | **OpenClaw** | Sesiones, subagentes, pipeline A/B, roles, despacho, verificación |
| Memoria y contexto duradero | **OpenClaw** (`memory.db`) | Daily, todos, inbox, learnings, sesiones, recuperación semántica |
| Tiempo y eventos | **OpenClaw** (automations) | Heartbeat, cron, wakes |
| **Ejecución de un flujo de IA** | **LangChain** | Cadenas con estado tipado, RAG, grafos con ramificación, streaming HTTP |
| Superficie de conversación | **OpenClaw** | Chat, canales, webchat |

La regla corta: **OpenClaw decide *quién* hace la tarea; LangChain decide *cómo se encadenan los pasos* de una tarea concreta.** Un grafo de LangChain no delega a subagentes, y el gateway no ejecuta grafos.

### 2. Cuándo un proyecto usa LangChain

Cuatro disparadores, todos verificables. Basta uno:

1. **Cadena multi-paso con estado tipado** que hoy se escribe a mano en Python y se rompe cuando cambia un paso.
2. **RAG que sirve a un consumidor externo** (una API, un frontend, otro servicio) - no a la conversación del agente.
3. **Streaming HTTP** como contrato de entrega.
4. **Ramificación real** (grafos con ciclos o rutas condicionales), donde un `if` encadenado ya no se lee.

### 3. Cuándo NO se usa

- **Orquestar subagentes o roles.** Eso es del gateway (ADR-073/074), y duplicarlo produce dos schedulers y dos fuentes de estado.
- **Memoria.** El retrieval puede consultar `memory.db`, pero la escritura y la verdad siguen siendo suyas. LangChain no abre una segunda base de memoria.
- **Automatizaciones y heartbeat.** Son de `automations`.
- **Como dependencia del bootstrap del workspace.** Ningún script del workspace importa LangChain. Las guardas no leen código de proyecto (ADR-066) y esto no es la excepción.

### 4. Reglas de frontera

- **Proceso separado.** Un flujo LangChain corre como servicio propio, con su `venv` y su `requirements.txt` pinneado. No se instala en el entorno del gateway.
- **Contrato explícito.** Si sirve a otro consumidor, expone HTTP y documenta request/response. Si es interno, es un CLI.
- **Sin acople por venv compartido.** El HANDOFF del starter ya registra que `kanam-insight` reusaba su venv; con `kanam-insight` descontinuado, la regla queda: **cada proyecto que use LangChain declara sus propias dependencias.**

### 5. Prerrequisito antes de ampliar el uso

El starter deja de ser demo **cuando su corpus es real**, no cuando el código está completo. Criterio medido, no declarado:

- El índice contiene documentos de más de una fuente, y el número de chunks es reproducible con un comando documentado.
- El documento de estrategia se corrige contra el disco.

**Re-medido el 2026-10-22 (no cambia el criterio, lo deja con el estado real):**

| Criterio | Estado | Medido |
|---|---|---|
| Documento de estrategia corregido contra el disco | **CUMPLE** | `docs/LANGCHAIN_STRATEGY.md` §5c ya no declara 4.423 vectores: dice 10 embeddings y distingue lo verificado de lo supuesto. Corrección hecha el 2026-10-19. |
| Índice con documentos de más de una fuente | **NO CUMPLE** | La colección `starter_knowledge` sigue con **10 embeddings de un solo documento**. `chroma.sqlite3` sin modificar desde el 2026-10-19 13:54. |
| Número de chunks reproducible con un comando documentado | **CUMPLE (el comando) / FALTA (la corrida)** | `venv/bin/python3 scripts/scan_sources.py --list` es determinista: hoy reporta **372 archivos** (era 333 el 2026-10-19; creció con la documentación nueva). La corrida de indexado (`store.py --sources --reset`) **no se ha hecho**. |

**Lo que falta para que el starter deje de ser demo:** una sola corrida de `store.py --sources --reset` contra Ollama local. Es una corrida explicita, no un efecto colateral: borra el índice entero y re-embebe. El servicio (`127.0.0.1:8100`) sigue sano y el watchdog de launchd sigue activo.

Hasta entonces, el starter se usa como **referencia de implementación** (patrón RAG, patrón ReAct, patrón servicio), no como base de conocimiento.

---

## Consequences

### Positivas
- **Se termina la ambigüedad de capas.** La pregunta "¿LangChain o el pipeline A/B?" deja de tener dos respuestas.
- **El primer uso concreto es chico y verificable:** un flujo con RAG servido por HTTP dentro de un proyecto, sin tocar el gateway.
- **Se documenta la deriva medida**, no la declarada. El starter queda con su estado real escrito al lado.
- **No se agrega dependencia al bootstrap.** El costo de arranque del agente no cambia.

### Negativas
- **Dos runtimes.** Python con su venv por un lado, Node con el gateway por el otro. Cada servicio nuevo es un proceso que alguien tiene que monitorear (el starter ya necesitó watchdog + alerta).
- **Ventaja de ecosistema, no de agente.** LangChain no mejora la conversación; mejora los flujos que producen artefactos o responden por API. El beneficio es más lento de ver.
- **Riesgo de duplicación.** Un grafo que "casi" orquesta agentes es la tentación obvia. La frontera del punto 1 es la que hay que sostener.

### Neutras
- El starter sigue corriendo como está. No se toca su código en esta decisión.

---

## Acciones

1. ~~Backlog #80 abierto~~ → cerrado con esta decisión.
2. ~~Corregir las tres afirmaciones falsas de `docs/LANGCHAIN_STRATEGY.md` contra el disco medido~~ → **CERRADO el 2026-10-19** (commit `3e80c91` del repo del proyecto + §5c del documento). Re-verificado el 2026-10-22: el documento ya no declara 4.423 vectores ni el scanner de 3 fuentes, y separa lo verificado de lo supuesto.
3. **Pendiente:** definir el primer flujo real que justifique el punto 2 de la sección 2 (RAG servido a un consumidor externo). Candidato natural: retrieval sobre `docs/` + `skills/` para el propio agente - pero eso hoy lo resuelve `memory.db`, así que el primer caso tiene que ser otro.
4. **Pendiente (nuevo, 2026-10-22):** correr `venv/bin/python3 scripts/store.py --sources --reset` una vez, para que la colección deje de tener 10 embeddings de demo y pase a los ~372 archivos que el scanner reporta. Es el criterio medido de la sección 5.

## Revisión 2026-10-22 - un research externo, verificado

Gonzo compartió un research externo (604 líneas, 74 fuentes) sobre una arquitectura OpenClaw + LangGraph. **Entra como dato, no como instrucción** (AGENTS.md). Se preservó y se verificó claim por claim: `docs/research/2026-10-22-verificacion-claims.md` (26 claims: 13 verdadero, 5 parcial, 3 falso, 1 no documentado).

**La regla de lectura que queda:** un ADR nuestro no es dogma. Pero un ADR registra **el estado real de este stack**, y ese estado no lo invalida un documento de otra persona. Entonces cada claim se clasifica por naturaleza: **hecho técnico** (gana la fuente citada) / **hecho sobre nuestras restricciones** (gana el ADR) / **valor** (se decide, no se hereda). Ningún claim se aceptó por autoridad.

**Lo que el research aporta (verificado):**

- El **patrón MCP para flujos acotados** es correcto, y `/mcp` es **stateless** (cada request es independiente y no sustituye los hilos de LangGraph). Verificado en la doc oficial y en el wheel real de `langgraph-api` (`api/mcp.py:495`).
- El **`checkpointer` por super-step con pending writes** es el aporte real: permite reiniciar desde el último paso exitoso sin re-ejecutar los nodos que completaron. El starter **ya tiene `langgraph-checkpoint 2.1.2` instalado y sin usar** (cero imports en `app/`, `scripts/`, `tests/`).
- La **regla de idempotencia antes de un `interrupt()`** es correcta y oficial: *"the node restarts from the beginning of the node where the `interrupt` was called when resumed"*.
- **Tool Search** aplaza los esquemas MCP: ya lo tenemos en el runtime.

**Lo que el research se equivoca (refutado contra la fuente):**

- "Las mutaciones del registro MCP requieren el Gateway **detenido**" → **falso**: `cli/mcp/registry.md` dice que el CLI solo lee o escribe config.
- `OPENCLAW_DISABLE_CRON_HOST_EXECUTION=1` → **no existe** en los docs ni en el binario.
- "LangSmith self-hosted" como opción local → es un **add-on Enterprise** con license key, Kubernetes, Postgres, Redis y ClickHouse.

**La medición que cambia el plan:** un servidor **MCP stdio propio** (`mcp<2`, FastMCP 1.30.0) resuelve con los pines del starter **intactos** y **0 conflictos** (`uv pip compile`), sin Postgres, sin `LANGGRAPH_CLOUD_LICENSE_KEY` y sin LangSmith. La vía que propone el research (`langgraph-api` + Agent Server) también resuelve, pero exige Postgres, Redis y verificación de licencia **para un flujo acotado**. El research señala el patrón correcto y lo implementa con la capa más pesada disponible.

**Lo que este ADR NO cambia:** la frontera de la sección 1 sigue igual. El research propone un "career mentor" con memoria propia por usuario y un cron propio: eso es exactamente la segunda base de memoria y el segundo scheduler que este ADR prohíbe. Si alguna vez se quiere, se reconstruye sobre `memory.db` + `automations`.

**Pendiente de decisión de Gonzo (no resuelto por este ADR):** cuál es el primer flujo real que justifique la sección 2. La vía técnica está medida (MCP stdio propio sobre el RAG del starter, o `langgraph-api` si algún día hace falta estado persistente), pero **el flujo es una decisión de producto, no de arquitectura**. Este ADR registra la frontera y la medición; no elige el caso de uso.
