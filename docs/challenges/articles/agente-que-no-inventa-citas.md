# Cómo construí un agente que no puede inventar citas

*Borrador para publicar. Fuente: `localdoc-agent`, el proyecto de referencia. Números verificados contra el repo y la eval real.*

---

## El problema que no es de retrieval

Todo el mundo construye un RAG en una tarde. Subís PDFs, cortás en chunks, embeddés, buscás por similitud, pasás los fragmentos al modelo. Funciona, y en el demo se ve bien.

Y entonces el modelo escribe:

> “El contrato vence el 15 de diciembre, según la cláusula 4.2, página 3.”

El problema: la cláusula 4.2 dice otra cosa, y la página 3 no existe. El modelo no mintió a propósito. **Rellenó un hueco con lo que sonaba probable.** Y como el usuario no va a verificar, la respuesta incorrecta pasa.

Eso no es un problema de retrieval. Es un problema de **verificación**. Y no se arregla con un mejor modelo: se arregla con código.

## La única idea

Cada respuesta viene con citas estructuradas: `chunk_id` y una cita textual. La app no confía en el modelo; verifica.

```python
def verify_citations(citations, chunks_by_id):
    valid, invalid = [], []
    for cit in citations:
        chunk = chunks_by_id.get(cit["chunk_id"], "")
        if _normalize(cit["quote"]) in _normalize(chunk):
            valid.append(cit)
        else:
            invalid.append(cit)
    return valid, invalid
```

Una cita válida es aquella cuyo texto es **una subcadena** del chunk. Si falla, se le pide al modelo una vez más y, si vuelve a fallar, la respuesta se convierte en una negativa.

Esto no es otro LLM revisando al primero. Es contención de strings, y cualquiera puede reproducirla abriendo la base.

## Lo que casi salió mal, tres veces

Y acá va la parte que no suele contarse.

**1. Los embeddings eran falsos y los tests eran verdes.**

La primera versión llamaba `ollama embed`, un subcomando que **no existe** en el CLI. Cada llamada fallaba y caía silenciosamente a un mock de tres dimensiones. Los tests pasaban porque solo verificaban estructura, no valores.

El fix no fue “arreglar el mock”. Fue eliminar el fallback: si los embeddings fallan, la ingesta explota con un error claro. Un sistema que degrada en silencio es peor que uno que se rompe fuerte.

**2. La búsqueda vectorial no era vectorial.**

`sqlite-vec` nunca se cargaba. La tabla `chunks_vec` se creaba como una tabla normal, y el “KNN” era fuerza bruta. Funcionaba de casualidad con 13 chunks y habría colapsado con 1.300.

Lo encontré porque verifiqué el `sqlite_master`:

```
CREATE TABLE chunks_vec (chunk_id INTEGER PRIMARY KEY, embedding BLOB)   ← mal
CREATE VIRTUAL TABLE chunks_vec USING vec0(...)                          ← bien
```

**3. Tres veces un subagente reportó archivos que nunca escribió.**

No es un problema del modelo: es un problema de confiar en el auto-reporte. La lección fue procesual. Antes de aceptar cualquier entrega, correr el repo:

```bash
git status --short
uv run pytest -q
```

Si el archivo no está en el filesystem, no existe. Punto.

## El modelo no es el producto

La pregunta que todos hacen es “¿cuál modelo?”. La respuesta honesta es: **importa menos de lo que creés, y más de lo que mide.**

| Modelo | Accuracy (18 preguntas) | P50 |
|---|---:|---:|
| Gemma 4 12B | **18/18** | 49.5 s |
| Gemma 3 4B | 4/18 | 6.8 s |

El 4B es 7 veces más rápido y 4,5 veces menos preciso. Para un demo, alcanza. Para un contrato, no.

Y un detalle que nadie esperaría: **un 9B puede ser más lento que un 12B.** Qwen3.5:9B mantuvo un contexto de 262k residente y no completó una sola respuesta en 90 segundos. El 12B, con su configuración por defecto, respondió en 50.

La conclusión no es “usá el modelo más grande”. Es **medí en tu máquina, con tu corpus, con tus preguntas**. El benchmark ajeno es un prior, no una verdad.

## La parte que no hace el modelo

Una de las 18 preguntas pedía sumar dos montos de contrato. El 12B fallaba sistemáticamente: no suma.

La solución no fue un modelo mejor. Fue admitir que la aritmética **no es trabajo del LLM** y escribir ocho líneas de código determinístico. El agente recupera y redacta; la calculadora suma.

Es el mismo principio de las citas, aplicado a otra capa: **lo que se puede verificar con código, se verifica con código.**

## Qué es un proyecto local-first, en serio

Tres pruebas, no tres promesas:

1. **Cero sockets.** Durante la transcripción o la consulta, `lsof` no muestra ninguna conexión saliente. Medido, no declarado.
2. **Se puede borrar.** Un botón que elimina índice, embeddings y borradores; verificado por filesystem.
3. **No se alquila.** En diez años, el archivo se abre sin suscripción.

Y una consecuencia que casi nadie menciona: si los datos no salen, **tampoco entran**. El modelo tiene que ser local porque la privacidad no es una feature, es la arquitectura.

## Lo que este proyecto no hace

- No lee PDFs escaneados. Los rechaza con un mensaje claro.
- No es rápido. 50 segundos por respuesta con un 12B.
- No escala. Una persona, una máquina, un corpus.
- No tiene un benchmark independiente. Las 18 preguntas las escribió el mismo que escribió el sistema.

Decir esto no debilita el proyecto. Lo hace creíble. Un repo que admite sus límites es un repo que alguien puede usar sin sorpresas.

## El método, resumido

1. **Elegir la restricción.** No “un RAG”, sino “un agente cuyas citas no pueden ser inventadas”.
2. **Verificar lo verificable.** Substring, aritmética, `lsof`. Código, no opinión.
3. **Eliminar los fallbacks silenciosos.** Si algo falla, que grite.
4. **Medir antes de elegir.** Modelos, latencia, precisión. Los números van al repo.
5. **Publicar las fallas.** La sección más valiosa de un README es “qué salió mal”.

---

*Proyecto: [localdoc-agent](https://github.com/gonzoblasco/localdoc-agent). Proyecto hermano, sobre las personas en vez de los contratos: [Field Notes](https://github.com/gonzoblasco/field-notes).*
