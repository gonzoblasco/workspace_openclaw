# Práctica B1 — ¿Qué corpus y qué pregunta? (bloque 1)

> El ejercicio del bloque 1 pide escribir `mi-sistema.md`. Lo hice con datos **reales** de este workspace, no con un caso inventado. Los números salen de `memory/memory.db` y `memory/vectors.db`, medidos el 2026-11-12.

## 1. El documento privado

El corpus de este workspace, medido:

| Dato | Valor |
|---|---|
| Secciones indexadas (`sections` en `memory.db`) | 1.987 |
| Notas diarias/sesiones en `daily_notes` | 157 |
| Sesiones relacionales (`sessions_relacional`) | 112 |
| Fragmentos con vector en `vectors.db` | 2.352 filas sobre 1.824 secciones |
| Sesiones con vector en `session_vectors` | 968 filas sobre 112 sesiones |
| Documentos fuente | `memory/*.md`, daily notes, sesiones, learnings, ADRs |

Un LLM general **no vio ninguno** de estos documentos: son notas de trabajo privadas de los últimos meses.

## 2. La pregunta real

Tomé una pregunta que se hizo este mes y cuya respuesta correcta está escrita:

> **"¿Cuál es la política de modelo por agente y niveles de pensamiento?"**
>
> Respuesta correcta: la declara **ADR-090**, y el resumen operativo vive en el bloque managed de `AGENTS.md`. Los modelos por rol son deepseek-v4.1-flash para CORE, gpt-oss:120b-cloud para dev/ops/critic/planner, y así por rol.

El archivo fuente es identificable: `docs/adr/ADR-090*.md` y el bloque `<!-- BEGIN MANAGED:model-operativo -->` de `AGENTS.md`.

## 3. La herramienta: ¿forma o hechos?

**Hechos.** La respuesta es un dato concreto (qué modelo usa cada rol), no un estilo ni un formato. La pregunta exige recuperar un documento y citarlo.

Consecuencia directa de la tabla del bloque 1:

| Qué querés cambiar | Herramienta | Veredicto para este caso |
|---|---|---|
| Comportamiento, límites, seguridad | Prompt | No aplica |
| Voz, estilo, tono | Fine-tuning | **No aplica**: nada que ver con estilo |
| Hechos, políticas, precios, docs | **RAG** | ✅ **Este es el caso** |

Y el motivo para no usar fine-tuning acá es exactamente el que el video enumera: ADR-090 puede superarse con otro ADR, y el 2026-11-06 ya hubo que corregir un hecho de modelo. Reentrenar cada vez que cambia una decisión es imposible; reindexar es un comando.

## 4. El costo de equivocarse

Si `memory_search` responde "el modelo de CORE es gpt-oss:120b" y el real es deepseek-v4.1-flash:

- **Quién lo nota:** nadie hasta que un agente arranca con el modelo equivocado y un resultado sale distinto al esperado.
- **Cuándo:** días después, sin correlación con la búsqueda que lo causó.
- **Gravedad:** alta. Un hecho de configuración mal recuperado se propaga a decisiones.

Eso lo convierte en un caso **crítico** de RAG: falla silenciosa con consecuencia durable. Es peor que un RAG de FAQ que responde mal y el usuario reformula.

---

## La contradicción: el corpus tiene huecos que el índice no cubre

Verifiqué `memory/vectors.db` contra `memory/memory.db` y aparecieron tres cosas que **no encajan** con la promesa del bloque 1 ("RAG automatiza el humano"):

### a) ~~1.667 secciones huérfanas~~ → RESUELTO: el `section_id` apunta a `sections`, no a `daily_notes`

Primera lectura mía: 1.824 `section_id` contra 157 filas en `daily_notes` = 1.667 huérfanos. **Era un error de lectura.** `memory.db` tiene 19 tablas y la que corresponde es `sections` (1.987 filas):

```
section_vectors section_id distintos:  1.824
sections en memory.db:                 1.987
section_id sin fila en sections:           0
```

**Cero huérfanos.** El mapeo es `section_vectors.section_id → sections.id`, y cada sección referencia su documento por `doc_id`/`doc_type`. La lectura de "hueco" venía de comparar contra la tabla equivocada.

Lección de método: antes de declarar datos huérfanos, verificar **contra qué tabla apunta la FK**. Es el mismo error de generalizar una lectura que el curso comete con BM25.

### b) Tres vectores con 32 dimensiones en vez de 1.024 — **CONFIRMADO**

```
965 filas con 1.024 dims
  3 filas con   32 dims  ← todas de la sección 103
```

32 dimensiones es exactamente la firma del **fallback SHA-256** de `get_embedding()`. Esos tres vectores son basura: cualquier similitud contra ellos es ruido. `memory-reembed.py` existe para repararlos, pero **nadie corrió**.

### c) ~~Siete secciones fantasma~~ → RESUELTO: mismo error de tabla

Comparé `session_vectors.session_id` contra `daily_notes.id` y salieron 7 sin fila. La tabla correcta es **`sessions_relacional`** (112 filas):

```
session_vectors session_id distintos:  112
sessions_relacional:                   112
sin fila:                                0
```

**Cero fantasmas.** El `session_id` apunta a `sessions_relacional.id`, cuya columna de texto es `content_bare`, no `content`.

### d) El chunking desborda la sección que dice representar

El registro 92 tiene 1.336 caracteres en `daily_notes`, pero sus chunks miden **1.590, 1.848 y 696**. El chunk 0 es 254 caracteres *más largo* que la sección a la que pertenece. Con `CHUNK_SIZE = 1500` eso no debería pasar salvo que el chunk incluya texto que no está en `content` (encabezado armado, o un contenido anterior que después se editó).

Y el caso más grave: hay **una sesión con 78 chunks** (sesión 80), otra con 75 y otra con 57. `MAX_CHUNKS_PER_SESSION = 3` en el script actual dice que deberían ser 3.

Verificado el detalle: esas tres sesiones tienen **todos sus chunks en 1.024 dims y todos con `chunk_text`**, índices correlativos `0..77`, `0..74`, `0..56`. No son vectores de una versión vieja con otro esquema: son chunks generados por un proceso que **no usó el tope de 3**. O se corrió una versión anterior del script, o hay otro escritor de `session_vectors` (el reembed no crea chunks: sólo recalcula vectores).

Esto sí viola la regla que el propio script declara, y es lo único de los cuatro hallazgos que sigue en pie.

## Lo que esto confirma del bloque 1 — y lo que me comí

El bloque 1 dice: **"la que falla más seguido es augmenting, no retrieval"**, y que nadie mide si el LLM usó el contexto.

Mi primera inspección del índice creyó ver 1.667 huérfanos, 7 fantasmas y un tope de chunks roto. **Dos de esos cuatro eran lectura mía contra la tabla equivocada.** El índice no tiene huecos: tiene una FK correcta hacia `sections` y `sessions_relacional`.

Quedan **dos hallazgos reales**:

1. **3 vectores de 32 dims** (sección 103) = firma del fallback SHA-256. Basura que devuelve scores ruidosos.
2. **Sesiones con 78, 75 y 57 chunks** donde el script declara un tope de 3. Alguien escribió sin ese tope.

Los dos son verificables con un `SELECT` y ninguno necesita un embedding mejor. Eso es el argumento del bloque 1 aplicado al revés de como yo lo usé: **el problema casi nunca está donde la primera lectura dice que está.**

Y sigue valiendo la conclusión del bloque 6: sin un set de 20 preguntas con fuente correcta, ni los 3 vectores de 32 dims ni los 78 chunks se habrían detectado.

## Entregable

`mi-sistema.md` = este archivo. Los cuatro bloques están completos, con la pregunta real y el costo de equivocarse.

**Verificado:** `section_id → sections.id` y `session_id → sessions_relacional.id`, ambos con 0 huérfanos.

**Pendiente (deuda real, no del ejercicio):** averiguar qué proceso escribió las sesiones con 78/75/57 chunks, y correr un reembed de la sección 103 para matar los 3 vectores de 32 dims.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
