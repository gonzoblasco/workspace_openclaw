# Bloque 6 — Pipeline completo, caché, métricas y producción (módulos 21-26, 48:49 - 59:40)

> Los números de este bloque son del video y están marcados como tales. La traducción al workspace se hizo contra `scripts/memory-catalog-v2.py` y `scripts/memory-reembed.py` el 2026-11-11.

## La idea en una frase

**Un RAG en producción no es el pipeline: es la frontera entre lo que se hace una vez (offline) y lo que se hace por query (online), y todo lo que se rompe en esa frontera.**

El ponente la marca bien en 49:38: cargar, chunkear, embeber e indexar ocurre **antes** de que el usuario pregunte. El usuario sólo paga retrieve → augment → generate.

## El mapa, con tiempos medidos en orden de magnitud

| Fase | Cuándo | Costo dominante | Falla típica |
|---|---|---|---|
| **Ingesta** (cargar, parsear) | offline | I/O de disco | encoding, PDFs rotos |
| **Chunking** | offline | CPU, barato | el problema del bloque 5 |
| **Embedding** | offline **y online** | el modelo, caro | modelo cambiado → reindexar todo |
| **Indexado** | offline | RAM/CPU | índice desactualizado |
| **Retrieval** | online | el índice | recall bajo |
| **Augment** | online | tokens de contexto | prompt que ignora el contexto |
| **Generate** | online | llamada al LLM | alucinación, latencia |

**El punto que casi nadie internaliza:** embedding aparece en **dos** fases. Offline embeber el corpus; online embeber la query. Si esos dos embeddings usan modelos distintos, el sistema no funciona y **no falla con error**: devuelve basura con scores plausibles. En el workspace eso está controlado porque los dos lados usan `qwen3-embedding:0.6b` desde la misma variable; si un día se cambia el default de un script y no el del otro, `memory_search` queda roto en silencio. `scripts/memory-reembed.py` existe justo para eso.

## Caché: los cuatro niveles, traducidos

El ponente lista cuatro (53:56):

| Cache | Qué guarda | Ahorra | Riesgo |
|---|---|---|---|
| **Query cache** | pregunta → respuesta final | todo el pipeline | datos viejos si la política cambió |
| **Embedding cache** | texto → vector | el modelo de embedding | poco, el embedding es barato en local |
| **Vector search cache** | query → chunks | la búsqueda | chunks viejos si se reindexó |
| **LLM response cache** | prompt → respuesta | la llamada más cara | el más peligroso: contexto cambiado, respuesta vieja |

### La cifra del video, corregida

El ponente dice: *"Instead of taking 950 milliseconds, a cache response might then just take just 5 seconds. That's 190 times faster"* (53:29-53:42).

**950 ms / 5 s no da 190; 950 / 5 sí.** Son **5 milisegundos**, no segundos: el ASR se comió la palabra *milliseconds* en la segunda cifra. El "190×" del propio ponente lo confirma. Se corrige acá y no en el transcript.

### La regla de la clave

Verificado como correcto lo que dice en 55:11: la clave es **hash(query + contexto)**, no hash(query). Si la misma pregunta sobre el mismo documento da respuestas distintas según el contexto recuperado, cachear sólo la query devuelve la respuesta equivocada con confianza alta.

### Lo que el video no dice: el caché de un RAG personal no paga

El workspace tarda ~25 ms en el loop de similitud y unos segundos en el embedding + LLM. Un caché de query cachearía **preguntas que ya no se repiten**: en un asistente personal, casi nadie pregunta dos veces exactamente lo mismo. El beneficio está en el caché del **LLM** (el más caro) y sólo si hay un patrón de repetición medido.

**Regla:** no cachear sin medir primero cuántas queries son repetidas. Si la tasa de repetición es menor al 10%, el caché es infraestructura muerta que hay que mantener.

## Métricas: las tres propias de un RAG

El ponente separa genéricas (response time, throughput, error rate) de propias (56:10):

| Métrica | Cómo se mide | Umbral que da |
|---|---|---|
| **Retrieval quality** | ¿el chunk correcto apareció en el top-k? | el más importante y el más ignorado |
| **Embedding performance** | ms para embeber | señal de que el modelo se cayó a un fallback |
| **Chunking efficiency** | ¿cuántos chunks hacen falta para cubrir la respuesta? | demasiados = chunks malos |

**Los umbrales del video** (56:25): respuesta > 2 s es problema de performance; error rate > 5% es problema de sistema. Son razonables para un chat de empresa, **lentos para un asistente personal**: si `memory_search` tarda 2 segundos, se siente roto. Para uso propio, el techo honesto son 500 ms.

### El hueco más grande de la Parte 1

**El curso no menciona evaluación en ningún momento.** No hay una sola línea sobre cómo medir si el sistema acierta. Sin eso, un RAG se "siente" bien o mal y no se puede mejorar.

Lo mínimo viable, que no necesita herramientas:

1. **Un set de 20 preguntas** con la respuesta correcta y el fragmento fuente escrito a mano.
2. Correrlas después de cada cambio y contar aciertos de retrieval (¿está el fragmento en el top-5?).
3. Contar aciertos de generación (¿la respuesta dice eso?).

Sin ese set, cada cambio de chunking o de modelo es una apuesta a ciegas. Con 20 preguntas, es una medición.

## Producción: la cascada, y qué significa cada paso

El ponente describe el graceful degradation (56:56) y la cascada (57:10):

```
pipeline completo → búsqueda por keywords → chunks crudos → texto simple → mensaje útil
```

Esto es correcto y **es la parte más reusable del curso.** Traducida a cualquier sistema:

| Nivel | Degrada a | Nunca pierde |
|---|---|---|
| 1. RAG completo | — | — |
| 2. Keyword | pierde semántica | encuentra lo exacto |
| 3. Chunks sin generar | pierde la respuesta redactada | entrega la fuente |
| 4. Matching de texto | pierde relevancia | da algo |
| 5. Mensaje de error | nada | dice qué falló |

**El half-open state** (57:24): probar periódicamente si el servicio volvió, con pocas requests, antes de cerrar el circuito. Es el patrón Circuit Breaker estándar, y el ponente lo nombra bien.

### La arquitectura de capas (57:54)

| Capa | Componentes | Regla |
|---|---|---|
| **Data** | Chroma, Redis, PostgreSQL | estado durable |
| **RAG pipeline** | microservicios: query, chunk, embed, retrieve, augment, generate | escalan por separado |
| **Application** | web, mobile, admin | lo que ve el usuario |
| **Monitoring** | Prometheus, Grafana, Jaeger, ELK | visibilidad |

Para un workspace personal, esto es **infraestructura de más**: un solo proceso hace todas las capas. La arquitectura vale cuando el volumen obliga; copiarla antes la vuelve un impuesto.

## Contraste con el workspace: qué hay y qué falta

| Pieza | Estado | Comentario |
|---|---|---|
| Ingesta | ✅ `memory-catalog-v2.py` | idempotente, upsert por fecha |
| Chunking | ⚠️ ciego a 1.500, 3 chunks | ver bloque 5 |
| Embedding | ✅ `qwen3-embedding:0.6b` + fallback SHA-256 con warning | el fallback está bien pensado: avisa si se rompe |
| Índice | ⚠️ exhaustivo sobre SQLite | válido a esta escala |
| Retrieval | ✅ coseno con vectores normalizados | bien hecho |
| Augment | ⚠️ no medido | nunca se verifica si el LLM usó el contexto |
| Generate | ✅ | |
| **Caché** | ❌ no hay | correcto: no paga a esta tasa de repetición |
| **Métricas** | ❌ no hay | el hueco real |
| **Evaluación** | ❌ no hay | el hueco más grande |
| **Degradación** | ⚠️ el fallback SHA-256 existe, pero no hay cascada a keyword | ver bloque 2: FTS5 lo resolvería |

**El veredicto:** el sistema está mejor construido de lo que un tutorial de este curso produciría — normaliza, avisa del fallback, es idempotente. Le faltan exactamente las tres cosas que el curso tampoco enseña a fondo: **evaluación, métricas y cascada**.

## Cierre de la Parte 1: qué se queda y qué se tira

**Se queda:**
1. La distinción prompt / fine-tuning / RAG y el motivo (forma vs. hechos).
2. La cascada de degradación y el half-open state.
3. Los cuatro niveles de caché y la regla de la clave con contexto.
4. La idea de retrieval quality como métrica propia.

**Se tira:**
1. La elección de `all-MiniLM-L6-v2` (2021).
2. La API de Chroma tal como se muestra (`chromadb.Client` vs. `EphemeralClient`).
3. Los números de GPT-4 (1.8T parámetros, nunca confirmado).
4. La idea de que 500 documentos justifican una vector DB.
5. "Chunk más chico es mejor, siempre."

**Y lo que agrego yo, que el curso no tiene:** la parte 1 enseña a *construir* RAG. No enseña a *saber si funciona*. Esa es la diferencia entre un tutorial y un sistema.

## Ejercicio final de la Parte 1

**Construí el set de evaluación mínimo. Es el único ejercicio que cambia algo.**

1. Elegí 10 preguntas reales sobre tu propio workspace (cosas que buscaste el último mes).
2. Para cada una, escribí: la respuesta correcta, el archivo fuente y una frase que debe aparecer.
3. Corré `memory_search` con cada una y anotá: ¿el archivo fuente está en los resultados? ¿el top-1 es el correcto? ¿la frase aparece en el contexto?
4. Entregable: `eval.md` con la tabla 10 × 4.

Ese archivo te permite, después de cualquier cambio, saber si mejoraste o empeoraste. Sin él, todo lo demás es fe.

## Banco de preguntas

1. ¿Por qué el embedding aparece en dos fases y qué pasa si los modelos no coinciden?
2. La cifra de caché del video: 950 ms → 5 ms, 190×. ¿Qué se rompió en la transcripción?
3. ¿Por qué cachear sólo la query y no query + contexto puede devolver una respuesta equivocada con confianza?
4. ¿Cuáles son las tres métricas propias de RAG y cuál es la que el curso nunca mide?
5. De la arquitectura en capas de Kubernetes, ¿qué copiarías a un sistema personal y qué sería un impuesto?

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
