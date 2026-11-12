# Bloque 5 — Chunking: el precision problem (módulos 18-20, 39:21 - 48:49)

> Los números de chunking del workspace salen de `scripts/memory-catalog-v2.py` y de medir `session_vectors` el 2026-11-11. La comparación con lo que recomienda el curso es directa.

## La idea en una frase

**El chunking no es dividir texto: es decidir qué unidad de significado le entregás al embedding.** Cortás de más y perdés contexto; cortás de menos y perdés precisión. Todo lo demás —tamaño, overlap, separadores— son parámetros de esa decisión.

Si el embedding es el motor, el chunking es la caja de cambios. Un motor bueno con una caja mala da un auto malo.

## El precision problem, bien explicado por el ponente

El caso (39:43): un handbook de 50 páginas metido **como una sola entrada**. Ante "what's the remote work policy", el sistema devuelve el handbook entero. El ponente lo llama *precision problem* (40:12) y el nombre es exacto.

**El mecanismo, que el video no desarma:** el embedding de un documento de 50 páginas es el **promedio de todos sus temas**. Un vector promedio de un handbook no está cerca de "política de home office"; está moderadamente cerca de **todo**. La similitud se aplana: todos los queries tienen scores parecidos y el ranking se vuelve casi aleatorio. Y peor, devuelve el documento entero porque **eso** es lo que está guardado.

Con chunking, cada vector representa un pedazo de un tema y la distancia vuelve a significar algo.

## Los parámetros del ponente, con su razón

| Regla del video | Valor | Por qué |
|---|---|---|
| Tamaño | 200-500 caracteres | Balance contexto/precisión (43:30) |
| Overlap | 50-100 caracteres | Preservar contexto de frontera (41:20) |
| Cortar en oraciones | sí | Integridad gramatical |
| No cortar palabras | sí | El token partido no existe para el modelo |
| Preservar párrafos | sí | Estructura lógica |
| **Probar con queries reales** | siempre | Es la única validación que importa |

La última es la que más se ignora y la que más define la calidad.

### Lo que el video deja afuera y hoy importa

Dice que semantic chunking y agentic chunking quedan fuera de alcance (42:32). Es honesto, pero esa es **la evolución del chunking**:

- **Semantic chunking:** corta donde el embedding de dos oraciones consecutivas cambia bruscamente de dirección. Detecta los cambios de tema que el corte fijo no ve.
- **Agentic / LLM chunking:** un modelo decide dónde cortar según la estructura del documento. Caro, lento, y hoy ya viable para corpus chicos y estables.

Para un corpus de 3.000 fragmentos, el corte fijo con buenos separadores es **suficiente**. Para 100.000 documentos heterogéneos, el corte fijo es la causa raíz de los malos resultados. No es una cuestión de gusto: es de escala.

### Una advertencia sobre el overlap

El overlap no es gratis: **cada chunk solapado se embebe y se indexa dos veces**. Con 50 de overlap sobre chunks de 500, inflás el corpus un 10% y duplicás resultados en el ranking. El RAG devuelve el mismo texto dos veces y el LLM se confunde sobre cuántas fuentes distintas tiene.

Por eso hay que **deduplicar por similitud después del retrieval**, no sólo antes. El curso no lo dice.

## El chunking real del workspace: los números

Verifiqué `scripts/memory-catalog-v2.py`:

```python
CHUNK_SIZE = 1500
MAX_CHUNKS_PER_SESSION = 3
...
raw_chunks = [content[j : j + CHUNK_SIZE] for j in range(0, len(content), CHUNK_SIZE)]
```

Y medí la distribución de `chunk_text` en `session_vectors` (965 registros):

| Estadística | Caracteres |
|---|---|
| mínimo | 63 |
| p25 | 903 |
| **mediana** | **1.385** |
| p75 | 1.628 |
| máximo | 3.062 |
| promedio | 1.248 |
| chunks exactamente 1.500 | 80 |

### Qué dicen esos números

1. **El tamaño real es ~2,8× el máximo que recomienda el curso.** 1.385 vs 500. No es "un poco más grande": está en otra categoría.
2. **Hay 80 chunks cortados exactamente a 1.500.** Eso confirma el corte ciego por índice de carácter: cortó a mitad de una palabra o de una oración. Es exactamente el defecto que el video señala en 40:53.
3. **Cero overlap.** El corte es `content[j:j+1500]` sin solape. Una frase cortada entre dos chunks se pierde en la frontera.
4. **Hay chunks de 63 caracteres.** Esos son casi inútiles: el vector de un fragmento de dos líneas es ruido.
5. **Máximo 3.062:** el límite de 3 chunks por sesión hace que las sesiones largas **pierdan el resto del contenido**. Una sesión de 8.000 caracteres indexa 4.500 y tira 3.500. Ese contenido no se puede encontrar nunca.

### La consecuencia concreta

Un vector de 1.385 caracteres para un modelo de 1.024 dimensiones **representa el promedio del tema**, no el pedazo puntual. Si en una nota de 8 párrafos hablás de cinco cosas, el vector es una mezcla. Buscás "el bug del `.uid` en Godot" y el vector de la sesión entera está cerca porque menciona Godot, no porque contenga ese bug.

Eso explica el síntoma típico: **`memory_search` trae la sesión entera cuando buscabas una frase.** No es el embedding; es la granularidad.

Y no es un bug: es un trade-off deliberado por costo de reindexado. 3.317 vectores × 1.024 dims se tuvieron que generar con Ollama local; chunkear a 500 caracteres habría multiplicado por 3 el trabajo. **Es una decisión defendible para el volumen de hoy,** y un techo claro para el de mañana.

## Contraste: qué cambiaría, en orden

| Cambio | Impacto | Costo |
|---|---|---|
| **Cortar en fronteras** (párrafo > oración > palabra) | Alto: elimina los chunks cortados a mitad | Bajo, una función de split |
| **Overlap de ~100** | Medio: recupera frases de frontera | Reindexar |
| **Bajar a 800-1000 caracteres** | Alto: más precisión sin explotar el corpus | Reindexar 3× |
| **Deduplicar post-retrieval** | Medio: menos ruido al LLM | Código, no reindexado |
| **Semantic chunking** | Bajo a esta escala | Alto (necesita embeddings dobles) |

**Lo que no haría:** bajar a 500 como dice el curso. Con un corpus de sesiones técnicas, 500 caracteres es media idea. El número del video está calibrado para FAQs y políticas cortas, no para notas de trabajo.

## El error conceptual que hay que desactivar

> "Chunk más chico = mejor precisión, siempre."

No. **Chunk más chico = mejor precisión hasta que el chunk deja de contener una idea completa.** Pasado ese punto, el embedding de "para el home office" sin el contexto de qué política es, apunta a cualquier lado. El óptimo está en el tamaño de una unidad de significado de **tu** dominio: un artículo de FAQ (~200), una sección de política (~500), un turno de sesión técnica (~800-1500).

El video da el rango y deja afuera la regla: **el tamaño correcto es el de la unidad que un humano citaría como respuesta.** Si la respuesta buena a tu pregunta es un párrafo de 1.200 caracteres, tu chunk es 1.200.

## Ejercicio del bloque

**Medí tu propio precision problem con dos configuraciones.**

1. Tomá 5 sesiones reales de `memory/` y chunk-ealas a 1.500 ciego (lo que hace hoy) y a 500 con corte en oración y overlap 100.
2. Hacé las mismas 5 preguntas contra las dos colecciones con el mismo embedding.
3. Anotá en cada caso: ¿trajo el fragmento correcto? ¿trajo ruido alrededor? ¿cuántos caracteres de contexto le llegaron al LLM?
4. Entregable: `chunking.md` con la tabla de 5 filas × 2 columnas y una conclusión sobre si vale reindexar.

```python
import re
def chunk_bien(text, size=800, overlap=100):
    """Corta en párrafo > oración > palabra, nunca a mitad de palabra."""
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", text)
    chunks, cur = [], ""
    for p in parts:
        if len(cur) + len(p) + 1 <= size:
            cur = (cur + " " + p).strip()
        else:
            if cur: chunks.append(cur)
            cur = p
    if cur: chunks.append(cur)
    # overlap: arrastra la cola del anterior
    out = [chunks[0]] if chunks else []
    for prev, nxt in zip(chunks, chunks[1:]):
        out.append((prev[-overlap:] + " " + nxt).strip())
    return out
```

## Banco de preguntas

1. ¿Por qué el embedding de un documento entero está "moderadamente cerca de todo"?
2. El workspace tiene 80 chunks exactamente a 1.500 caracteres. ¿Qué te dice eso sobre el método de corte?
3. Con `MAX_CHUNKS_PER_SESSION = 3`, ¿qué pasa con una sesión de 8.000 caracteres?
4. ¿Por qué bajar a 500 caracteres puede empeorar la calidad en tu corpus, y cuál es la regla para saber cuál es el tamaño correcto?

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
