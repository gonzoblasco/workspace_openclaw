# Adopción — LangGraph Complete Course for Beginners

**Fecha:** 2026-11-11
**Pregunta que responde este archivo:** *¿qué estamos haciendo mal hoy en el workspace que este curso arregla?* No *qué enseña el curso*.

## Artefacto: `scripts/check-state-schema.py`

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| El estado es un `TypedDict` y **LangGraph no valida en runtime**; una clave no declarada queda fuera del esquema y el checkpointer la guarda igual (Módulo 4, «Langraph automatically sets that as like a a none value in this case if you don't pass an input», 0:42:23; Módulo 10, `Annotated` como contrato del estado, 2:05:41) | `projects/oss-post-graph` escribe **8 claves** en el estado que no están en `GraphState`: los nodos mutan el dict en sitio y cuelgan datos transitorios del estado, sin que ningún tipo ni test lo note. | `scripts/check-state-schema.py <repo>` — falla (exit 1) si un nodo escribe `state["k"]` con `k` fuera del `TypedDict`. |

### Por qué era un problema real y no un tema del curso

`projects/oss-post-graph` es un grafo LangGraph en producción-personal que redacta posts desde PRs mergeados. Su estado se declara en `src/state.py` con 13 claves. Los nodos escriben 18. La diferencia no es cosmética:

- `draft_path_temp`, `facts_pr`, `facts_issue`, `facts_comments`, `facts_files`, `gate_stdout`, `gate_stderr`, `already_published` son claves que **se persisten en el checkpoint** y no aparecen en el esquema. Quien lea `GraphState` para entender qué viaja entre nodos se pierde ocho de los datos, y ninguno de los dos nodos que las escriben documenta que las necesitan.
- Es exactamente el escenario que el curso describe como fuente de errores silenciosos: el grafo no se rompe al agregar una clave, así que el defecto se acumula.

### La salida real, corrida contra el repo (no una proyección)

```
$ python3 scripts/check-state-schema.py projects/oss-post-graph
FALLA: 8 clave(s) escrita(s) sin declarar en state.py:

  src/draft.py
    - 'draft_path_temp'  <- `state['draft_path_temp'] = ...` sin estar en el TypedDict

  src/facts.py
    - 'facts_comments'  <- `state['facts_comments'] = ...` sin estar en el TypedDict
    - 'facts_files'  <- `state['facts_files'] = ...` sin estar en el TypedDict
    - 'facts_issue'  <- `state['facts_issue'] = ...` sin estar en el TypedDict
    - 'facts_pr'  <- `state['facts_pr'] = ...` sin estar en el TypedDict

  src/gates.py
    - 'already_published'  <- `state['already_published'] = ...` sin estar en el TypedDict
    - 'gate_stderr'  <- `state['gate_stderr'] = ...` sin estar en el TypedDict
    - 'gate_stdout'  <- `state['gate_stdout'] = ...` sin estar en el TypedDict

Arreglo: agregar la clave al TypedDict de estado, o declararla en
ALLOWED_UNDECLARED si es transitoria y documentada.
EXIT=1
```

### El gate no es un siempre-verde

Se probó en las dos direcciones, porque un script que solo falla no es un gate:

```
$ python3 check-state-schema.py .   # repo limpio: 2 claves declaradas, 2 escritas
OK: 2 claves declaradas, ninguna clave sin declarar.
EXIT_CLEAN=0

$ python3 check-state-schema.py .   # se agrega un nodo que escribe 'nueva'
FALLA: 1 clave(s) escrita(s) sin declarar en state.py:
    - 'nueva'  <- `state['nueva'] = ...` sin estar en el TypedDict
EXIT_DIRTY=1
```

## Qué NO se adoptó, y por qué

| Idea del curso | Motivo de descarte |
|---|---|
| `interrupt()` / `Command(resume=...)` como colaboración humano-IA | **Ya lo hacemos bien.** `projects/oss-post-graph/src/approval.py` usa `langgraph.types.interrupt` y `Command(resume=...)`, e incluso documenta la idempotencia al reanudar. El curso *no* lo cubre (usa una variable global y declara el atajo); no hay nada que traer. |
| `MemorySaver` / checkpointers | Ya usamos `SqliteSaver`, más robusto que el `MemorySaver` del curso. |
| Recorte de historial a N mensajes (Módulo 9) | Nuestros grafos son de un solo run sin conversación multi-turno; el problema no existe hoy. Candidato si aparece un agente conversacional. |
| `lambda state: state` como passthrough de router | Nuestro grafo es lineal (`START → facts → … → approval → END`), sin routers. No hay router que envolver. Candidato si se agrega un branch condicional. |
| `add_messages` como reducer | Nuestro estado no transporta lista de mensajes: es un pipeline de datos a disco. Adoptarlo hoy sería copiar patrón sin problema. |
| Pricing de gpt-4o («tens of pennies…», 1:37:24) | Claim de época; el curso no lo respalda con fuente y no aplica a nuestro stack (Ollama local). |

## Deuda que deja este artefacto

- Las 8 claves siguen sin declarar en `projects/oss-post-graph`. **El gate las detecta, no las arregla**: declarar es una edición en otro proyecto y el curso no es autorización para tocar su código en esta sesión.
- El gate no corre en ningún CI todavía. Candidato: agregarlo al gate del proyecto (`projects/oss-post-graph`) o al pre-commit del workspace, y recién entonces exigir exit 0.
- No se creó skill nueva: la regla del curso es que la skill se escribe cuando el artefacto sobrevivió un uso real. Este es el primer uso.

## Lectura del material

El curso es bueno en lo que se propone: **fundamentos**. La secuencia Módulos 3–7 (grafo mínimo → estado múltiple → secuencial → router → loop) es la que hace entendible el ReAct agent del Módulo 11, y saltearla es la razón por la que tanta gente copia un agente sin saber por qué el router devuelve un string.

Lo que **no** cubre y hoy pesa más que lo que enseña: checkpointer y persistencia real, `interrupt()` (lo esquiva con una global), subgrafos, `Send`, streaming token a token, y observabilidad. Para nuestro uso, el valor concreto son dos cosas: el vocabulario para leer nuestros propios grafos (router, reducer, tool node) y el hábito de que **el estado es un contrato tipado**.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
