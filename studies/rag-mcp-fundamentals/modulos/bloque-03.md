# Bloque 3 — Búsqueda semántica y embeddings (módulos 10-14, 16:10 - 30:54)

> Los números de similitud y las dimensiones reales se calcularon a mano el 2026-11-11 (`/tmp/vec_demo.py`) contra vectores reales del workspace, no se copiaron del video.

## La idea en una frase

**Un embedding es una función que convierte texto en un punto, y la distancia entre puntos es una apuesta sobre el significado.** No es magia: es una función entrenada para que textos que aparecen en contextos parecidos queden cerca. Si el contexto de entrenamiento no se parece a tu dominio, la cercanía es ruido con formato numérico.

## Lo que el ponente explica bien

- **La definición** (20:04): "takes text and converts it into numbers that represent meaning". Correcto.
- **El modelo de referencia:** `all-MiniLM-L6-v2`, 384 dimensiones, 22M parámetros (18:25-18:40). Es el default de Chroma todavía hoy —verificado en `docs.trychroma.com` el 2026-11-11— así que no está "muerto", pero es de **2021**.
- **La lectura del score** (23:26): "the pair with the value closest to one are similar and away from one are dissimilar". Correcto para coseno.
- **La honestidad del 384:** dice que no se puede graficar y que hace falta matemática (21:48). Es el punto donde muchos tutoriales mienten con dibujitos de 2D.

## Donde el ponente se queda corto (y esto importa para tu trabajo)

### 1. El ejemplo 2D no dice lo que parece

Da tres vectores: `(1,5)`, `(2,4)`, `(6,1)` (22:32). Calculé los dot products y los cosenos reales:

| Par | Dot product | Coseno | Lectura |
|---|---|---|---|
| d1 · d2 | 22 | **0.9648** | muy similares |
| d2 · d3 | 16 | 0.5882 | medio |
| d1 · d3 | 11 | **0.3547** | distintos |

Ojo: **el dot product y el coseno no ordenan igual**. d2·d3 = 16 supera a d1·d3 = 11, y el coseno respeta ese orden acá — pero por poco. Con vectores de distinta norma, el dot product premia el más largo aunque esté más lejos en ángulo. Por eso **todo sistema serio normaliza antes de comparar**, y por eso el workspace guarda los vectores ya normalizados (norma 1.0, verificado).

### 2. Los scores absolutos son inútiles como umbral

El ejemplo real del video (25:06-25:20): *dogs vs pets* 73.3%, *dogs vs remote* 36.2%, *pets vs remote* 33.8%.

**No hay un número que signifique "es relevante".** 73% parece alto; en otro corpus el mismo par de frases da 0.42. El score depende del modelo, del corpus y de la longitud de los textos. Lo único que se puede hacer:

1. Comparar **rankings**, no valores.
2. O calibrar un umbral por corpus con pares conocidos (positivos y negativos) y mirar la distribución.
3. O —lo que hacen los sistemas de producción— **no usar umbral**: devolver top-k y dejar que el LLM decida, con el riesgo de meter ruido.

Si alguien te dice "usá 0.7 como umbral de similitud", te está vendiendo un número que sólo funciona en su corpus.

### 3. La elección del modelo de embedding está desactualizada — verificado hoy

Tabla real, MTEB Multilingual v2, leída de la fuente que cita el leaderboard el 2026-11-11:

| Modelo | Score MTEB | Dims | Params | Licencia | Dónde |
|---|---|---|---|---|---|
| harrier-oss-v1-27b (Microsoft) | 74.27 | 5.376 | 27B | MIT | self-host |
| KaLM-Embedding-Gemma3-12B (Tencent) | 72.32 | 3.840 | 11.76B | **no usable en la UE** | self-host |
| Qwen3-Embedding-8B (Alibaba) | 70.58 | 4.096 | 8B | Apache-2.0 | self-host |
| Qwen3-Embedding-0.6B (Alibaba) | 64.34 | **1.024** | **0.6B** | Apache-2.0 | **local — el del workspace** |
| all-MiniLM-L6-v2 (el del curso) | — (no rankea en la tabla) | 384 | 22M | Apache-2.0 | local |

**Lectura honesta:** el del workspace es `Qwen3-Embedding-0.6B` — 0.6 mil millones de parámetros, 1.024 dimensiones, Apache-2.0, corre local. Está **seis puntos MTEB arriba** del modelo del curso y cabe en la Mac mini. El curso recomienda un modelo de 2021 porque el curso se grabó con la mentalidad de 2023.

No hace falta subir a los de 8B o 27B: con 0.6B y 1.024 dims para 3.300 vectores, el cuello de botella no es la calidad del embedding.

## Lo que nadie dice: el embedding tiene un techo de dominio

Un modelo genérico entrenado con texto web entiende "dogs vs pets". **No entiende la jerga de tu proyecto.** Si tus documentos dicen "cable", "fricción absorbida", "slice", "canon checker", el embedding los pone cerca porque están en el mismo tipo de texto, no porque signifiquen lo mismo.

Las tres salidas reales, en orden de costo:

1. **Nada** — si el corpus es chico y el usuario reformula, funciona igual.
2. **Híbrido con BM25** — resuelve los identificadores exactos y la jerga literal. Gratis (ver bloque 2).
3. **Fine-tuning del embedding** — carísimo, sólo si hay miles de pares query-documento etiquetados. Nadie en un workspace personal llega ahí.

El curso no menciona ninguna de las tres. El módulo 11 se queda en "elegí local o API".

## Contraste con el workspace: los números reales

Verifiqué lo siguiente abriendo `memory/vectors.db`:

| Dato | Valor real |
|---|---|
| Tablas vectoriales | `section_vectors` (2.352 filas), `session_vectors` (965) |
| Bytes por vector | 4.096 |
| Dimensiones | **1.024 floats de 32 bits** |
| Norma del vector | **1.0** → ya normalizado al guardar |
| Tamaño del chunk asociado | 1.009 caracteres |
| Modelo | `qwen3-embedding:0.6b` vía Ollama |

Dos consecuencias prácticas:

1. **La similitud es coseno, disfrazada de dot product.** Con norma 1.0, `a·b = cos(a,b)`. Está bien hecho.
2. **El chunk de 1.009 caracteres es un problema para el embedding de 1.024 dims.** El modelo tiene una ventana de contexto; meterle 1.000 caracteres de una sección densa diluye el vector: representa "el promedio del tema", no "el pedazo puntual". Es el puente al bloque 5 (chunking), y es la razón por la que la búsqueda a veces trae secciones enteras cuando debería traer una frase.

## El dato del curso que ya no aplica

- **"1.8 trillones de parámetros" para GPT-4** (19:22): era rumor en 2023, OpenAI nunca lo confirmó. No lo cites.
- **"350 GB y 3.6 TB"** para GPT-3.5 y GPT-4: pesos en FP32, sin cuantizar. Hoy esos modelos corren cuantizados a una fracción. La comparación de "tamaño" contra un embedding de 90 MB sigue siendo válida en el orden de magnitud, pero los números exactos no.
- **"all-MiniLM es un perfect fit"** (19:50): lo era para un demo de 2023. No es una recomendación de 2026.

## Ejercicio del bloque

**Medí tu propio umbral en vez de creerle a uno.**

1. Elegí 5 pares de textos que sabés **similares** y 5 que sabés **distintos** (de tu corpus real).
2. Calculá el coseno de cada par con el modelo que uses.
3. Mirá las dos distribuciones. Si se superponen, **no hay umbral que sirva** y la decisión es top-k.
4. Entregable: `umbral.md` con la tabla de 10 valores y la conclusión en una línea.

Bonus que vale más: repetí con la query real (`"¿cuál es la política de X?"`) contra el documento correcto y contra uno del mismo tema pero equivocado. Ahí se ve si el modelo distingue o sólo agrupa por tema.

```python
# con Ollama local (lo que usa el workspace)
import json, urllib.request, math
MODEL = "qwen3-embedding:0.6b"
def emb(text):
    body = json.dumps({"model": MODEL, "prompt": text}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/embeddings",
                                 data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())["embedding"]
def cos(a, b):
    d = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(x*x for x in b))
    return d / (na * nb)
print(cos(emb("dogs are allowed in the office"), emb("pets are welcome at work")))
```

## Banco de preguntas

1. Con vectores de norma 1, ¿dot product y coseno dan lo mismo? ¿Y si no están normalizados?
2. ¿Por qué 0.73 de similitud no significa "relevante", y qué tres estrategias existen en su lugar?
3. El workspace usa un modelo de 0.6B y 1.024 dims. ¿Qué caso justificaría subir a 8B? ¿Y qué caso no?
4. Si la búsqueda de memoria trae una sección entera cuando vos buscabas una frase, ¿es problema del embedding o del chunking? Justificá con el dato de los 1.009 caracteres.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
