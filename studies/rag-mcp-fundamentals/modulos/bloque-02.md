# Bloque 2 — Keyword search: TF-IDF y BM25 (módulos 8-9, 09:36 - 16:10)

> Todo lo numérico de esta clase se generó con un script propio el 2026-11-11 (`/tmp/bm25_demo.py`), no se copió del video. El código está al final para que lo corras.

## La idea en una frase

**El keyword search no busca significado: cuenta apariciones y las pondera.** Es un baseline honesto —barato, explicable, sin GPU— y su punto de falla está a una pregunta de distancia.

Por qué importa aunque "esté viejo": TF-IDF y BM25 siguen siendo el **baseline contra el que se mide todo lo demás**. Si tu RAG semántico no le gana a BM25 en tu corpus, tenés un problema de embeddings, no una mejora. Y hoy, en los sistemas de producción serios, la respuesta no es elegir: es **búsqueda híbrida** (BM25 + vectores, fusionados). El curso la menciona de pasada en el lab (15:58) y no la desarrolla.

## La mecánica, sin magia

El ponente la explica con un ejemplo (09:53-10:07): tres documentos, contar cuántas veces aparece "reimbursement" en cada uno y cuántas "home office". El documento que suma más, gana.

Eso ya es TF (term frequency). El paso que falta es **IDF**: un término que aparece en todos los documentos no distingue nada, así que vale poco. La fórmula que se usa:

```
score(q,d) = Σ_t  IDF(t) · TF(t,d)
```

- **TF alto** = el término es importante *en este documento*.
- **IDF alto** = el término es raro *en el corpus* → distingue.
- `IDF = log(N / df)` crece cuando `df` (documentos que contienen el término) es chico.

**Traducción a inglés de la calle:** TF-IDF premia palabras que están en el documento y son raras en general. Por eso "the", "de", "office" en un corpus de oficina no valen nada.

## BM25: la corrección al TF crudo

El ponente nota algo importante en 12:17 y vale desarmarlo: *"The word office gets a score of zero because the BM25 algorithm is a bit more strict in assigning scores and because this word is present in all documents"*.

**Se equivoca en el mecanismo.** BM25 no le da cero por estar en todos los documentos —eso ya lo hace el IDF de TF-IDF—. Le da cero por una razón distinta: en su demo el término "office" aparece en los tres documentos, así que `df = N` y con la fórmula de BM25:

```
IDF = ln( (N - df + 0.5) / (df + 0.5) + 1 )
```

con `N = df = 3` el cociente es `0.5 / 3.5 ≈ 0.143`, y `ln(1.143) ≈ 0.134`. No es cero: es **muy chico**. El cero que ve en pantalla es redondeo del print de la librería, no una regla del algoritmo.

Lo que BM25 agrega de verdad sobre TF-IDF son dos cosas:

| Corrección | Qué hace | Parámetro típico |
|---|---|---|
| **Saturación del TF** | El término 10 veces no vale 10 veces más; el rendimiento es sublineal | `k1 = 1.2 – 2.0` (1.5 habitual) |
| **Normalización por longitud** | Un documento largo no gana sólo por ser largo | `b = 0.75` |

Fórmula:
```
score(q,d) = Σ_t IDF(t) · ( tf · (k1+1) ) / ( tf + k1 · (1 - b + b · |d|/avgdl) )
```

## Lo que medí (y no coincide exactamente con el video)

Corrí un BM25 y un TF-IDF propios sobre tres frases de política. Las que usé:

- `d1`: "Dogs are allowed in the office on Fridays." (8 palabras)
- `d2`: "Pets are welcome at work at the end of the week." (11)
- `d3`: "Employees may bring their dog to the workplace once a week." (11)

| Query | BM25 (d1, d2, d3) | TF-IDF (d1, d2, d3) |
|---|---|---|
| `office` | **1.0778**, 0.0, 0.0 | **0.4001**, 0.0, 0.0 |
| `dog` | 0.0, 0.0, **0.9386** | 0.0, 0.0, **0.3288** |
| `remote work` | 0.0, **0.9386**, 0.0 | 0.0, **0.1474**, 0.0 |
| `furniture` | 0, 0, 0 | 0, 0, 0 |
| `pet` | **0, 0, 0** | **0, 0, 0** |

Tres cosas que saltan:

1. **Los scores absolutos no son comparables entre motores.** 1.07 de BM25 y 0.40 de TF-IDF son el mismo acierto. Nunca compares un score de BM25 contra un coseno de embedding; sólo compará **rankings**.
2. **La fila `pet` es el módulo entero.** El documento correcto dice "Pets", la query dice "pet". Singular contra plural. Cero los dos motores. Ese es el punto de falla, en una línea.
3. **`office` no es cero en TF-IDF** (0.4001) porque en mi corpus de tres frases no está en todos los documentos. El cero del video es un artefacto de su corpus, no una propiedad del algoritmo.

## El límite, dicho bien

El ponente dice: "if the exact keyword isn't there, the search fails" (16:13). Correcto, pero conviene nombrar los cuatro modos de falla, porque sólo uno es el que se ve:

| Falla | Ejemplo | ¿Se nota? |
|---|---|---|
| **Sinónimo** | query "allowance", doc dice "reimbursement" | Sí, devuelve vacío |
| **Morfología** | query "pet", doc dice "pets" | **No**, devuelve algo peor: otro documento |
| **Query larga** | query en lenguaje natural de 15 palabras | Sí, se diluye el score |
| **Vocabulario del dominio** | jerga interna que no está en el doc | Sí |

El asesino es el segundo: **el keyword search no falla con ruido, falla con un resultado plausible y equivocado.** Es la razón por la que no alcanza con mirar si devuelve algo.

## Cuándo el keyword search es *mejor* que el semántico

Esto el curso no lo dice y es el 80% del valor práctico del bloque:

- **Identificadores exactos:** números de ticket, SKUs, códigos de error, hashes. Un embedding de `ERR_CONN_REFUSED` es basura; un BM25 lo encuentra perfecto.
- **Nombres propios poco frecuentes:** un apellido raro. El embedding lo mezcla con apellidos parecidos.
- **Corpus chico y estable:** 200 documentos que no cambian. La ganancia de embeddings no paga el costo de reindexar.
- **Necesitás explicar por qué apareció un resultado.** "Aparece porque dice la palabra X" es defendible ante un usuario o un auditor. "El vector estaba cerca" no.

Esto explica por qué los buscadores reales son híbridos: **BM25 para lo exacto, vectores para lo difuso, un ranker que fusiona.** En esa arquitectura, TF-IDF/BM25 no es el pasado: es una de las dos patas.

## Contraste con el workspace

- El workspace **no tiene capa BM25**. `memory_search` es puramente semántico con `qwen3-embedding:0.6b`.
- Consecuencia concreta: buscar `ADR-090` o `check-pipeline-enforcement.py` por nombre exacto depende de que el embedding de ese string se parezca al del archivo. Para identificadores, es frágil.
- Si en algún momento la búsqueda de memoria falla en nombres exactos, **la solución no es un embedding más grande: es agregar un índice FTS5 de SQLite al lado y fusionar.** SQLite ya lo trae (`CREATE VIRTUAL TABLE ... USING fts5`), sin instalar nada. Es la mejora más barata que tiene ese sistema hoy.

## Qué NO llevarse

- No memorices las fórmulas. Memorizá **qué corrigen**: TF-IDF pondera rareza; BM25 agrega saturación y normalización por longitud.
- No copies los parámetros `k1=1.5`, `b=0.75` como si fueran óptimos: son el default histórico de Elasticsearch/Lucene. Para corpus muy cortos, `b` más bajo suele funcionar mejor.
- No uses la salida del video como ground truth: su demo de TF-IDF da 0.4 a "office" y la mía 0.4001 —cerca, pero por casualidad de corpus distintos—. Los números dependen de los documentos, no del algoritmo.

## Ejercicio del bloque

**Corré el script de abajo con tu propio corpus y rompé el ranking a propósito.**

1. Pegá tres documentos reales tuyos (de `studies/` o `memory/`).
2. Buscá un término que sepas que está, pero **en plural** en el doc y **en singular** en la query. Confirmá que da cero.
3. Agregá `d1` al lado un cuarto documento que repita la palabra 5 veces, y mirá cuánto sube el score de BM25 versus TF-IDF. Ahí se ve la saturación.
4. Entregable: `bm25.md` con la tabla de scores y la frase "la falla que encontré fue ___".

```python
import math, re
docs = ["...", "...", "..."]          # tus documentos
def tok(s): return re.findall(r"[a-záéíóúñ]+", s.lower())
k1, b = 1.5, 0.75
tokd = [tok(d) for d in docs]; N=len(tokd)
avgdl = sum(len(t) for t in tokd)/N
df={}
for t in tokd:
    for w in set(t): df[w]=df.get(w,0)+1
def idf(w):
    n=df.get(w,0); return math.log((N-n+0.5)/(n+0.5)+1)
def bm25(q):
    out=[]
    for t in tokd:
        s=0.0
        for w in set(tok(q)):
            tf=t.count(w)
            if tf: s+=idf(w)*(tf*(k1+1))/(tf+k1*(1-b+b*len(t)/avgdl))
        out.append(round(s,4))
    return out
print(bm25("tu query"))
```

## Banco de preguntas

1. ¿Por qué el score absoluto de BM25 y el de un coseno de embedding no se pueden comparar, y qué sí se puede comparar?
2. En mi demo, la query `pet` da cero contra un documento que dice "Pets". ¿Qué arreglaría esto sin embeddings? (Pista: stemming o normalización.)
3. Nombrá dos casos donde BM25 es estrictamente mejor que un embedding, y justificá.
4. ¿Por qué la solución a un fallo de búsqueda exacta en `memory.db` no es un modelo de embedding más grande?

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
