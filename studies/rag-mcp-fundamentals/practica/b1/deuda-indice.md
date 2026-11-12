# Deuda abierta — 2 hallazgos reales de la auditoría B1 (2026-11-12)

> Esto no es parte del curso. Son dos defectos reales que salieron del ejercicio del bloque 1 y que quedan registrados con su evidencia para que nadie los redescubra.

## 1. Tres vectores de 32 dimensiones (firma del fallback SHA-256)

### Evidencia

```
session_vectors, distribución de dimensiones:
  965 filas con 1.024 dims
    3 filas con    32 dims   ← todas de la sesión 103
```

Las tres filas son de `idx.session_vectors` (no de `section_vectors`), `session_id = 103`. 32 dims es exactamente lo que devuelve el fallback de `get_embedding()` en `memory-catalog-v2.py` cuando Ollama no responde:

```python
h = hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()
return [float(i) for i in h]      # 32 bytes → 32 dims
```

### Por qué importa

Un vector de 32 dims de un SHA-256 no tiene relación semántica con nada. Cualquier similitud contra esas filas es ruido, y la búsqueda puede devolver la sesión 103 con un score plausible (los vectores normalizados pueden dar cosenos altos por casualidad).

### Estado

`scripts/memory-reembed.py` existe para esto y **sí cubre `idx.session_vectors`** (verificado: línea 119). Pero al correrlo hoy:

```
$ python3 scripts/memory-reembed.py --dry-run
Model qwen3-embedding:0.6b not usable: timed out
Nothing written. Fix Ollama/model first.
```

**El timeout es de 60 s y el modelo no está cargado.** El runner activo en ese momento era `gemma4:12b-mlx` (proceso 41501). Un `POST /api/embeddings` a `qwen3-embedding:0.6b` con el runner de gemma cargado tarda más de 60 s o se cuelga en el swap de modelo. Con `/api/tags` respondiendo 200 y el modelo presente en la lista, el problema es de **carga en frío**, no de modelo ausente.

### Qué haría falta para cerrarlo

1. Correr `memory-reembed.py` con el modelo ya caliente (un `curl` previo al endpoint hasta que responda, después el script).
2. O subir el timeout de `embed()` de 60 s a ~180 s para el primer request.
3. Verificar después: `SELECT count(*) FROM session_vectors WHERE length(query_vector)=128` (32 floats × 4 bytes) debe dar **0**.

**No se tocó nada:** el script aborta antes de escribir y lo confirma ("Nothing written"). Esto es deuda abierta, no un cambio en curso.

## 2. Sesiones con más chunks que el tope declarado

### Evidencia

```
memoria-catalog-v2.py:  MAX_CHUNKS_PER_SESSION = 3

session_vectors, top:
  sesión 80: 78 chunks  (idx 0..77, todos 1.024 dims, todos con chunk_text)
  sesión 96: 75 chunks  (idx 0..74)
  sesión 93: 57 chunks  (idx 0..56)
```

Los tres casos tienen **todo su contenido en 1.024 dims y `chunk_text` completo**, índice correlativo sin huecos. No son residuos de un esquema viejo: son chunks generados por un proceso que **no respetó el tope**.

### Por qué importa

El tope de 3 existe para acotar el costo de reindexado. Si algún proceso escribe 78 chunks por sesión, una reindexación completa pasa de 3 a 78 vectores por sesión y el corpus explota. Además, 78 chunks de la misma sesión compiten entre sí en el ranking: el retrieval devuelve cinco pedazos de la misma nota.

### Qué haría falta para cerrarlo

1. Identificar el escritor: buscar en `scripts/` y en los hooks de cierre cualquier otro `INSERT INTO session_vectors` que no pase por `memory-catalog-v2.py`.
2. Decidir el invariante: ¿el tope es 3 o se levantó a propósito y el script quedó desactualizado?
3. Si el tope rige: consolidar las sesiones 80, 96 y 93 y reindexar.

**Hipótesis a verificar (no confirmada):** la versión actual del script arma como máximo 1 representante + 2 chunks crudos = 3. Un proceso que haga chunking por sección en vez de por sesión produciría exactamente lo que se ve.

## Cómo encaja con las prácticas del curso

Los dos hallazgos son ejemplos del mismo punto del bloque 1, aplicado al revés de como lo usé primero: **el índice no estaba roto donde yo dije que estaba** (esas dos lecturas eran mías contra la tabla equivocada), **pero sí tenía dos defectos chicos y reales** que se ven con un `SELECT` y no necesitan un embedding mejor.

Y es el argumento del bloque 6: ninguno de los dos se habría detectado sin medir. Un set de evaluación no los encuentra; una auditoría de esquema sí. Son diagnósticos distintos y el RAG necesita los dos.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
