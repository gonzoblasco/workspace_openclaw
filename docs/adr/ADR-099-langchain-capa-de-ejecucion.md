# ADR-099: LangChain es la capa de ejecución de flujos, no el orquestador

**Fecha:** 2026-10-19
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** sesión 2026-10-19 - Gonzo: *"amaria empecemos a usar langchain en la practica común"*. Al ir a decidir el alcance se midió el starter contra el disco y apareció que su estrategia declaraba un índice de 4.423 vectores que no existe.
**Relacionado:** ADR-066 (guardias no leen código de proyecto), ADR-073 (multi-agente), ADR-074 (despacho), ADR-077/088/089 (pipeline A/B), ADR-083 (frontera de roles), ADR-090 (modelos por rol), ADR-098 (`projects/` dentro del workspace)

---

## Contexto

`projects/langchain-starter` existe desde el 2026-09-24, completo y corriendo como servicio permanente (`127.0.0.1:8100`, LaunchAgent + watchdog, verificado hoy: `/health` responde 200). `docs/LANGCHAIN_STRATEGY.md` lo presenta como la base de las herramientas internas del ecosistema, con siete fases planificadas.

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
- El documento de estrategia se corrige contra el disco (hoy declara 4.423 vectores y 445 archivos; tiene 10 y 1).

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
2. **Pendiente:** corregir las tres afirmaciones falsas de `docs/LANGCHAIN_STRATEGY.md` contra el disco medido (4.423 vectores, scanner de 3 fuentes, `kanam-insight`). Va como tarea propia, no como efecto colateral de este ADR.
3. **Pendiente:** definir el primer flujo real que justifique el punto 2 de la sección 2 (RAG servido a un consumidor externo). Candidato natural: retrieval sobre `docs/` + `skills/` para el propio agente - pero eso hoy lo resuelve `memory.db`, así que el primer caso tiene que ser otro.
