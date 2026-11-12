# Bloque 4 — Vector databases e índices (módulos 15-17, 30:54 - 39:21)

> Esta clase verifica Chroma contra la doc oficial el 2026-11-11 y mide la escala del workspace para decidir si la vector DB hace falta. El número de 192.000 operaciones del video lo recalculé.

## La idea en una frase

**Una vector database no es una base de datos que guarda vectores: es un índice que evita comparar contra todos.** Guardar vectores lo hace cualquier archivo; lo que comprás con Chroma, Pinecone o `pgvector` es la estructura que responde "los k más parecidos" sin recorrer el corpus.

Si esa estructura no te ahorra tiempo medible, la vector DB es un costo sin beneficio. Es la primera cosa que hay que medir y la que el curso no mide.

## El cálculo del ponente, verificado

Dice: 500 documentos × 384 dimensiones = 192.000 operaciones por query (31:36). **La cuenta cierra** (500 × 384 = 192.000) y el ejemplo de la guía telefónica es correcto en espíritu.

Pero hay dos matices que cambian la conclusión:

1. **192.000 multiplicaciones son nada.** Un CPU moderno hace del orden de miles de millones por segundo. En NumPy, esa query tarda **microsegundos**. El ponente habla de "you'd be there all day", que describe el caso de millones de entradas, no el de 500.
2. **Lo que sí duele no es el cómputo: es el I/O.** Leer 500 × 1,5 KB de disco por query es más caro que multiplicar. Igual: a esa escala, entra en el page cache del sistema operativo y desaparece.

**Traducción:** el ejemplo justifica el concepto de índice, no la adopción de una vector DB. Confundir las dos cosas es el error más común de los tutoriales de RAG.

## La escala real del workspace (medida hoy)

| Dato | Valor |
|---|---|
| Vectores en `section_vectors` | 2.352 |
| Vectores en `session_vectors` | 965 |
| **Total** | **3.317** |
| Dimensiones | 1.024 |
| **Operaciones por query exhaustiva** | **3.317 × 1.024 ≈ 3,4 millones** |

3,4 millones de multiplicaciones por query. **Medido con los vectores reales del workspace (965 vectores × 1.024 dims):**

| Implementación | Tiempo por query |
|---|---|
| Loop Python puro (`sum(x*y for ...)`) | ~24,6 ms |
| Matvec NumPy (`M @ q`) | **~0,014 ms** |

Diferencia: ~1.750×. Y aun así, 24,6 ms en Python puro **es usable** para un asistente que responde en segundos. Eso es lo que el video no dice: **`memory_search` hoy hace búsqueda exhaustiva y funciona.** No porque sea eficiente, sino porque 3.317 vectores es un corpus que entra en RAM sin pensar.

El detalle técnico que importa: NumPy es 1.750× más rápido justamente porque **hace las 3,4 millones de multiplicaciones**, que es el número del video. El número no estaba mal; lo que estaba mal era suponer que eso es lento.

**La regla práctica:** la búsqueda exhaustiva es viable hasta ~100.000 vectores con NumPy; los problemas empiezan en el millón. Chroma y Pinecone existen para el millón, no para el millar. El workspace está **un factor 30 por debajo** del punto donde el índice se vuelve necesario.

Eso no significa que SQLite sea la respuesta final: si la memoria crece 10× por año (verificado: hoy 3.317, hace un mes menos), en 2-3 años el cálculo cambia. Pero "en 2-3 años" es un disparador medible, no un motivo para migrar hoy.

## Chroma: qué es cierto y qué cambió — verificado en la doc oficial

### Lo que el video dice bien

**El default no persiste.** Verificado en `docs.trychroma.com`: `chromadb.Client()` es in-memory y pierde todo al cerrar el proceso. Para persistir hay que usar `PersistentClient(path=...)`. El ponente lo marca como gotcha (34:51) y tiene razón: es el error #1 de quien sigue un tutorial rápido.

### Lo que el video no refleja: la API se movió

La doc actual de Chroma expone tres clientes nombrados explícitamente, y el que menciona el video ya no es la forma de hacerlo:

| Cliente | Comportamiento | Cuándo |
|---|---|---|
| `EphemeralClient` | En memoria, explícito | Tests, demo |
| `PersistentClient(path)` | En disco | Uso local real |
| `HttpClient` | Servidor Chroma remoto | Producción / multi-proceso |

En el video se usa `chromadb.client` (minúscula) y `chromadb.Client()`. **`chromadb.client()` está deprecado**; la forma actual es `EphemeralClient`. Si copiás el código del video, funciona pero tira warning y el estilo es viejo.

### El default de embeddings sigue siendo `all-MiniLM-L6-v2`

Confirmado en la doc (`DefaultEmbeddingFunction`). Implicación que el video no dice: **si no pasás `embedding_function`, tu colección queda atada a 384 dimensiones**, y cambiarlo después exige reindexar todo. Elegir el modelo de embedding no es tuning; es una decisión de esquema, como la primary key.

Sí se puede pasar uno propio (verificado: `OpenAIEmbeddingFunction`, o una clase que implemente `EmbeddingFunction` con `name()`, `get_config()` y `build_from_config()`). El video lo menciona de pasada con OpenAI (35:34) y no aclara que la forma actual exige esos tres métodos para que la colección sea reconstruible.

## Los tres índices, con criterio para elegir

El ponente nombra HNSW, IVF y LSH y sólo desarrolla HNSW (33:07). Completo lo que falta porque **es la única parte de la Parte 1 que no envejeció**:

| Índice | Cómo funciona | Ventaja | Costo |
|---|---|---|---|
| **HNSW** | Grafo de vecinos por capas; busca descendiendo | Recall alto, rapidez; default de casi todo | RAM: guarda el grafo en memoria; lento de construir |
| **IVF** | Agrupa en clusters (k-means) y busca sólo en los cercanos | Menos RAM que HNSW | Requiere entrenar los centroides; pierde recall en los bordes de cluster |
| **LSH** | Hash que colisiona vectores parecidos | Muy rápido, streaming-friendly | Recall malo en alta dimensión; hoy casi nadie lo usa solo |

**El dato que importa:** HNSW es **aproximado**. No garantiza devolver el vecino exacto; devuelve uno muy probablemente correcto. Por eso existe el parámetro `ef_search`: subirlo mejora el recall y cuesta latencia. Si tu RAG "no encuentra" algo que sabés que está, antes de cambiar el modelo subí el recall del índice y compará contra la búsqueda exhaustiva.

**Cuándo IVF gana:** corpus de decenas de millones de vectores con RAM acotada. **Cuándo LSH gana:** casi nunca en 2026. Se enseña por historia.

## Chroma vs. Pinecone vs. lo que ya tenés

El ponente recomienda Chroma para aprender y Pinecone para producción (34:07). La matriz real:

| Opción | Costo | Operación | Cuándo |
|---|---|---|---|
| SQLite + NumPy | $0 | la tuya | hasta ~100k vectores — **el caso del workspace** |
| Chroma local | $0 | la tuya | prototipo con necesidad de metadata filtering y API cómoda |
| `pgvector` | el de tu Postgres | la tuya | ya tenés Postgres y querés una sola fuente de verdad |
| Pinecone | por uso | gestionada | >1M vectores, equipo sin ops |
| Qdrant / Weaviate | self-host | la tuya | necesitás filtros complejos, multi-tenant |

**Lo que el video no dice y es lo decisivo:** el vector store es la pieza más **reemplazable** de todo el RAG. La interfaz es siempre `add` / `query` / `delete`. La decisión que no se puede deshacer es la del **modelo de embedding** (fija las dimensiones) y la del **chunking** (fija la calidad). Migrar de SQLite a Chroma es un día de trabajo; cambiar el modelo es reindexarlo todo.

## Contraste con el workspace: qué haría yo

**No migraría a Chroma hoy.** Los 3.317 vectores no lo justifican, y la búsqueda exhaustiva con NumPy da el mismo resultado sin una dependencia más.

**Lo que sí cambiaría, en orden de impacto:**

1. **Agregar FTS5 al lado** (bloque 2) — resuelve identificadores exactos, gratis.
2. **Chunking** (bloque 5) — es donde está el problema real de calidad, no en el índice.
3. **El índice**, sólo cuando el conteo supere ~100k. Disparador medible, no intuición.

## Ejercicio del bloque

**Medí el punto de quiebre de tu propio sistema.**

1. Corré una query exhaustiva sobre tus vectores y cronometrala (10 repeticiones, tomá la mediana).
2. Multiplicá por 30, por 300 y por 3.000 (simulando corpus 30×, 300×, 3.000×).
3. Mirá en qué número deja de ser aceptable.
4. Entregable: `escala.md` con los tres tiempos y el número de vectores donde vas a migrar.

```python
import sqlite3, struct, time, statistics, math, os
db = os.path.expanduser("~/.openclaw/workspace/memory/vectors.db")
c = sqlite3.connect(db)
rows = [r[0] for r in c.execute("select query_vector from session_vectors")]
def vec(b):
    n = len(b)//4; return struct.unpack(f"{n}f", b[:n*4])
vecs = [vec(r) for r in rows]
q = vecs[0]
def scan(q, vs):
    best = []
    for v in vs:
        d = sum(x*y for x, y in zip(q, v))   # ya normalizados
        best.append(d)
    return best
ts = []
for _ in range(10):
    t0 = time.perf_counter(); scan(q, vecs); ts.append(time.perf_counter()-t0)
print("vectores", len(vecs), "mediana ms", round(statistics.median(ts)*1000, 2))
```

Y la versión que da el número real (la que hace `memory_search` si se vectoriza):

```python
import numpy as np
M = np.vstack([np.array(v, dtype=np.float32) for v in vecs])   # 965 x 1024
q = M[0]
t0 = time.perf_counter(); scores = M @ q; dt = time.perf_counter() - t0
print("numpy ms", round(dt*1000, 3), "top", scores.argmax())
```

Medido en la Mac mini el 2026-11-11: loop Python **24,62 ms**, NumPy **0,014 ms**. Si tu `memory_search` tarda segundos, el tiempo no está en la comparación de vectores. Está en leer la DB, en el modelo de embedding o en el LLM.

## Banco de preguntas

1. Si 192.000 multiplicaciones son microsegundos, ¿qué justifica realmente adoptar una vector DB?
2. ¿Por qué cambiar el modelo de embedding después de tener una colección es mucho más caro que cambiar la vector DB?
3. HNSW es aproximado. ¿Qué parámetro subís si tu RAG no encuentra algo que sabés que está, y qué costo pagás?
4. El workspace tiene 3.317 vectores. ¿En qué número concreto migrarías, y por qué ese y no otro?

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
