# Módulo 7 — Language: clase

> Clase del **Módulo 7**, el último, de *Harvard CS50's AI with Python* (Brian Yu).
> Fuentes: `transcripcion.md` (citas con t= verificadas), mis conocimientos, y el código en `language/practica/`.
> **Aviso que corresponde:** el curso es de 2020. Este módulo termina en la arquitectura del transformer y no cubre los modelos de escala de 2026. Se enseña como fundamento, y la clase lo marca donde el estado del arte va más lejos.

---

## 7.1 Lo que cambia: la tarea deja de ser clasificar

Los módulos anteriores tenían salidas fijas: una clase, un número, una asignación. En lenguaje, la salida es **una secuencia**, y su longitud no se conoce de antemano.

Eso rompe todo lo anterior. Una red que clasifica devuelve `[0.2, 0.8]`; una red que genera texto devuelve una palabra, que vuelve a entrar como entrada, que devuelve otra.

---

## 7.2 Tokenización: la primera decisión

> "we were able to do this essentially via a process known as tokenization. Tokenization is the process of splitting a sequence of" (11:02:27)

Partir el texto en unidades. Es una decisión de diseño, no un detalle: `"no es bueno"` tokenizado por palabra pierde la negación; tokenizado por sub-palabras la retiene.

---

## 7.3 n-gramas: el modelo de lenguaje más chico

> "An n-gram is just some contiguous sequence of n items from a sample of text." (10:59:45)

Con `n=2` es un **bigrama** (11:01:55), con `n=3` un **trigrama** (11:00:02). Contar secuencias da un modelo de lenguaje rudimentario.

Y una **cadena de Markov** para generar texto:

> "Recall that a Markov chain is some sequence of values where we can predict one value based on the values that came before it." (11:03:00)

### Medido

`p1_ngram.py` sobre un corpus chico:

```
=== Generar texto con Markov (bigramas) ===
  semilla "the cat":
    the cat ate the cat slept on the cat and then the fish a cat and
  semilla "a dog":
    a dog sat on the cat ate the bone and the house and the mat and

=== Trigramas ===
  semilla "the cat sat":
    the cat sat on a mat and the dog sat on a mat and then the
```

**Gramatical localmente, sin sentido global.** Cada palabra es plausible dada la anterior; la frase no va a ningún lado. Con trigramas se vuelve más repetitivo: menos continuaciones, más coherencia local.

### El problema que no desaparece

```
  frase inédita: "the cat danced on a purple mat"
  trigramas que el modelo ya vio: 0/5
```

La probabilidad del modelo es **cero**. No es "poco probable": es imposible. De ahí la suavización (additive smoothing) del curso: dar una probabilidad chica a lo que no se vio.

Y con corpus más grande **el problema no desaparece**: el vocabulario crece más rápido que el corpus.

---

## 7.4 Bag of words y Naive Bayes: clasificar sin entender

> "a model known as the bag of words model, which is a model that represents text as just an unordered collection of words." (11:07:00)

Y encima de eso, el clasificador:

> "we're going to use the bag of words model to build something known as a naive Bayes classifier." (11:07:32)

### Medido

`p2_naive_bayes.py` entrena sobre 4 opiniones positivas y 4 negativas, y clasifica:

```
  frase                    clase    log-pos      log-neg
  great acting             pos      -5.14        -6.53
  awful story              neg      -6.53        -5.43
  great story              pos      -5.14        -6.53
  boring film              neg      -7.22        -6.12
```

### La suposición ingenua, y por qué funciona igual

```
P(w₁, w₂ | clase) = P(w₁|clase) · P(w₂|clase)
```

Es **falsa**: `"great"` y `"wonderful"` correlacionan. Al multiplicar sus probabilidades, el modelo **cuenta dos veces la misma evidencia**.

```
"great wonderful excellent" -> pos (log-pos=-7.9, log-neg=-11.5)
```

Sigue clasificando bien, pero los **scores están calibrados de más**: tres sinónimos positivos lo hacen parecer mucho más seguro de lo que debería.

**Para ordenar clases alcanza. Para decir "probabilidad 0.999", no.** Ese es el costo de la suposición, y el detalle que el video no dice.

---

## 7.5 RNN y la secuencia

> "one tool that we can use is the recurrent neural network" (11:29:00)

Una RNN procesa token por token guardando un estado oculto. Y una arquitectura encoder-decoder para preguntas y respuestas:

> "an architecture known as an encoder-decoder architecture" (11:29:36)

### Por qué no se puede paralelizar

> "it's very difficult to parallelize this process" (11:39:19)

El paso `n` necesita el estado del `n-1`. No hay forma de computar dos a la vez.

---

## 7.6 Attention: mirar a todos a la vez

> "what we really want is some way to decide for ourselves which of the input values are worth paying attention to" (11:34:30)

> "this is the key idea behind a mechanism known as attention" (11:34:30)

La idea: en vez de pasar todo por un estado, cada token pregunta a todos los demás cuánto le importan.

Y en el transformer:

> "we're also going to add one additional component, which is going to be a self-attention step" (11:43:40)

> "this problem that recurrent neural networks are not easy to parallelize has become an increasing problem. And as a result of that, that was one of the main motivations for a different architec" (11:40:08)

> "The positional encoding is some vector that represents the position of the word in the sentence." (11:42:51)

### Medido: los dos costos tienen forma distinta

`p3_secuencia.py`, d=64:

```
  n (tokens)     RNN (n·d²)         attention (n²·d)       gana
  10             40,960             12,800                 attention
  100            409,600            1,280,000              RNN
  1000           4,096,000          128,000,000            RNN
  10000          40,960,000         12,800,000,000         RNN
  100000         409,600,000        1,280,000,000,000      RNN
```

**Punto de cruce: n=33.** Con menos tokens, attention hace menos operaciones; con más, el RNN.

**Y por eso el transformer ganó igual:** el RNN es secuencial, attention es una multiplicación de matrices. Una GPU con miles de núcleos no desperdicia el hardware.

### El problema de attention, que el video no menciona

`n²·64`. Con n=100.000 son **1.28 × 10¹² operaciones en una capa**. Con 32 capas, intratable.

**Todo modelo de contexto largo de 2026 usa una variante que rompe el `n²`**: sparse attention, sliding window, o aproximaciones. El transformer del video es el punto de partida, no el que corre en producción.

---

## 7.7 Positional encoding: sin él, el orden se pierde

`p4_posicional.py` lo verifica:

```
"el gato muerde al perro" vs "el perro muerde al gato"

  celdas que difieren con positional encoding: 32/80
  (2 palabras cambiadas × 16 dimensiones)
```

Sin positional encoding, self-attention computa la **misma matriz** para las dos frases: `quién muerde a quién` es indistinguible. Con el encoding, cada token lleva su posición.

### La geometría que el encoding impone

```
  par de posiciones     distancia euclidiana
  (0, 1)                1.172
  (0, 100)              3.651
  (5, 6)                1.172
  (5, 50)               3.758
```

**Posiciones vecinas tienen vectores cercanos; lejanas, vectores lejos.** El modelo no aprende "dónde está el token": aprende la geometría que el encoding le impone, y esa geometría ya trae la noción de cercanía.

---

## 7.8 Cierre: lo que el curso no dice, y lo que sí dejó

### Lo que no dice

- **Embeddings.** El curso no menciona word embeddings: los tokens son símbolos, no vectores aprendidos.
- **Perplejidad.** El curso no mide un modelo de lenguaje. Nunca dice si un bigrama es mejor que otro.
- **Escala.** No cubre instruction tuning, RLHF, ni nada de lo que hace que un LLM sirva.
- **Contexto largo.** El `n²` de attention no aparece.

### Lo que sí dejó, y se puede usar

| Idea del módulo | Dónde vive en el workspace |
|---|---|
| Tokenizar antes de comparar | Normalizar rutas y nombres antes de deduplicar en la memoria |
| n-gramas y Markov | El modelo mental de "predecir la próxima palabra" |
| Bag of words pierde el orden | "No es bueno" ≠ "bueno": los gates por substring tienen ese límite |
| Naive Bayes cuenta de más | Los scores de un clasificador naive sobrevenden su certeza |
| RNN secuencial vs attention paralela | La misma dicotomía del Módulo 1: búsqueda vs enumerar |
| Attention como filtro | Recortar contexto por relevancia es una decisión de diseño, no un preset |
| Positional encoding | Lo que no le digas al modelo, no lo sabe: el orden hay que darlo |

Y la lección que cierra el curso entero: **cada familia de técnicas existe porque la anterior tiene un techo.** Búsqueda → conocimiento → probabilidad → optimización → aprendizaje → redes → lenguaje. Ninguna reemplaza a la anterior; cada una resuelve el caso donde la previa falla.

---

## Práctica del módulo

Cuatro scripts en `language/practica/`. Gate: `python3 run_all.py` → **4 de 4**.

| # | Práctica | Afirmación |
|---|---|---|
| 1 | `p1_ngram.py` | Los n-gramas generan texto plausible y sin sentido |
| 2 | `p2_naive_bayes.py` | Bag of words + Bayes clasifica sin entender |
| 3 | `p3_secuencia.py` | RNN es lineal y secuencial; attention, cuadrática y paralela |
| 4 | `p4_posicional.py` | Sin posición, el orden de las palabras se pierde |

Ver `practica-modulo-07.md`.

---

## Preguntas para estudiar

1. `"no es bueno"` y `"es bueno"` tienen el mismo bag of words menos una palabra. ¿Por qué eso basta para confundir a un clasificador por frecuencia?
2. Un trigrama con una palabra nueva da probabilidad 0. ¿Qué hace la suavización exactamente, y qué precio paga?
3. RNN hace `n·d²`, attention `n²·d`. ¿Para qué `n` cruzan con `d=64`? ¿Y si `d=1024`?
4. El transformer ganó aunque haga más operaciones en secuencias cortas. ¿Cuándo dejaría de ganar?
5. Sin positional encoding, dos permutaciones producen la misma atención. ¿Por qué eso es un problema sólo para "quién hace qué a quién" y no para clasificar películas?
6. **El `n²` de attention:** un modelo con 1M de tokens de contexto. ¿Cuántas operaciones por capa? ¿Qué hace un modelo real para evitar eso?
7. Un clasificador Naive Bayes devuelve 0.999. ¿Por qué no creerle ese número? ¿Qué tipo de error cometió?
8. **El cierre del curso:** enumerá las siete familias y el techo de cada una. ¿Cuál usarías para decidir qué herramienta llamar en un agente?

---

## Referencias

- Transcript: `studies/cs50-ai-python/transcripcion.md` (Módulo 7 = desde el cue 2376)
- Outline: `studies/cs50-ai-python/outline.md` (Módulo 7)
- Código: `studies/cs50-ai-python/language/practica/`
- Proyectos: https://cs50.harvard.edu/ai/2020/

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
