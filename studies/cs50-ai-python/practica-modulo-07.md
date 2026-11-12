# Práctica del Módulo 7 — Language

> Las preguntas del Módulo 7, **corridas**. Sin librerías.
> Gate: `python3 run_all.py` → 4 de 4.

```
PASA   p1_ngram.py                los n-gramas generan texto plausible y sin sentido
PASA   p2_naive_bayes.py          bag of words + Bayes clasifica sin entender
PASA   p3_secuencia.py            RNN es lineal y secuencial; attention, cuadrática y paralela
PASA   p4_posicional.py           sin posición, el orden de las palabras se pierde

RESULTADO: PASA (4 de 4)
```

---

## 1. n-gramas: el modelo de lenguaje más chico

```
  palabras: 86   vocabulario: 20 tokens distintos

  2-gramas: 44 distintos
     6x  and the
     5x  the cat
     5x  sat on
  3-gramas: 64 distintos
     4x  on the mat
     3x  sat on the
```

### Generar con Markov

```
  semilla "the cat":
    the cat ate the cat slept on the cat and then the fish a cat and
  semilla "a dog":
    a dog sat on the cat ate the bone and the house and the mat and
```

Gramatical localmente, sin sentido global. Y con trigramas más repetitivo:

```
  semilla "the cat sat":
    the cat sat on a mat and the dog sat on a mat and then the
```

### El vocabulario cero

```
  frase inédita: "the cat danced on a purple mat"
  trigramas que el modelo ya vio: 0/5
  la probabilidad del modelo es CERO.
```

No es "poco probable": es imposible. De ahí la suavización. Y con corpus más grande **el problema no desaparece**: el vocabulario crece más rápido que el corpus.

---

## 2. Bag of words y Naive Bayes

```
"great movie loved it" -> {'great': 1, 'movie': 1, 'loved': 1, 'it': 1}
"it loved movie great" -> {'it': 1, 'loved': 1, 'movie': 1, 'great': 1}
¿el mismo bag? sí
```

**Dos frases con el mismo conjunto de palabras son el MISMO dato.** Para sentimiento alcanza; para `"no es bueno"` no.

### Clasificando

```
  frase                    clase    log-pos      log-neg
  great acting             pos      -5.14        -6.53
  awful story              neg      -6.53        -5.43
  great story              pos      -5.14        -6.53
  boring film              neg      -7.22        -6.12
```

### La suposición ingenua, y su precio

```
"great wonderful excellent" -> pos (log-pos=-7.9, log-neg=-11.5)
```

Tres sinónimos positivos **cuentan la misma evidencia tres veces**. El modelo clasifica bien y su score **está calibrado de más**: parece mucho más seguro de lo que debería.

**Para ordenar clases alcanza. Para decir "probabilidad 0.999", no.**

---

## 3. RNN vs self-attention: dos formas de costo

```
  n (tokens)     RNN (n·d²)         attention (n²·d)       gana
  10             40,960             12,800                 attention
  100            409,600            1,280,000              RNN
  1000           4,096,000          128,000,000            RNN
  10000          40,960,000         12,800,000,000         RNN
  100000         409,600,000        1,280,000,000,000      RNN

  Punto de cruce: n=33
```

**El transformer ganó igual**, porque el RNN es secuencial y attention es una multiplicación de matrices. Una GPU con miles de núcleos no desperdicia el hardware.

### El problema que el video no menciona

`n²·64`. Con n=100.000: **1.28 × 10¹² operaciones en una capa**. Con 32 capas, intratable.

Todo modelo de contexto largo de 2026 rompe el `n²` con sparse attention, sliding window o aproximaciones. El transformer del video es el punto de partida.

### Y lo que el RNN hacía mejor

El RNN tiene un estado que acumula **toda** la historia. Attention tiene un límite fijo: **no puede mirar más allá de su ventana.**

Por eso "olvidar" una instrucción de la mitad de la conversación es un problema de atención, no de memoria: el modelo no la está mirando.

---

## 4. Positional encoding: sin él, el orden se pierde

```
"el gato muerde al perro" vs "el perro muerde al gato"

  celdas que difieren con positional encoding: 32/80
  (2 palabras cambiadas × 16 dimensiones)
```

Sin él, self-attention computa la **misma matriz** para las dos frases: `quién muerde a quién` es indistinguible.

### El encoding, con sus números

```
  pos=0    [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
  pos=1    [0.841, 0.54, 0.1, 0.995, 0.01, 1.0, 0.001, 1.0]
  pos=10   [-0.544, -0.839, 0.841, 0.54, 0.1, 0.995, 0.01, 1.0]
  pos=100  [-0.506, 0.862, -0.544, -0.839, 0.841, 0.54, 0.1, 0.995]
```

No hay dos posiciones con el mismo vector. Y `pos=100` sigue siendo distinguible de `pos=0`, porque las frecuencias bajas giran lentísimo.

### La geometría que el encoding impone

```
  par de posiciones     distancia euclidiana
  (0, 1)                1.172
  (0, 2)                2.131
  (0, 10)               3.447
  (0, 100)              3.651
  (5, 6)                1.172
  (5, 50)               3.758
```

**Posiciones vecinas, vectores cercanos; lejanas, vectores lejos.** El modelo no aprende "dónde está el token": aprende la geometría que el encoding le impone, y esa geometría ya trae la noción de cercanía.

---

## Qué queda después de correrlo

| La respuesta de manual | Lo que mostró el código |
|---|---|
| Los n-gramas modelan lenguaje | Generan texto gramatical y sin sentido |
| Con más corpus mejora | El vocabulario crece más rápido: siguen los ceros |
| Bag of words es una simplificación | `"great movie loved it"` y `"it loved movie great"` son el mismo dato |
| Naive Bayes asume independencia | Cuenta la evidencia varias veces: los scores no son probabilidades |
| Attention es más eficiente que RNN | Hace MÁS operaciones: gana por paralelismo, no por matemática |
| El transformer resuelve el contexto largo | `n²` es intratable pasado ~100k. Todo 2026 usa variantes |
| Attention entiende la secuencia | Sin positional encoding, dos permutaciones son indistinguibles |
| Un modelo olvidó una instrucción | No la olvidó: no la está mirando. Es atención, no memoria |

---

## Cómo volver a correrlo

```bash
cd studies/cs50-ai-python/language/practica
python3 run_all.py            # las 4
python3 p1_ngram.py           # el Markov generando texto
python3 p3_secuencia.py       # el cruce en n=33
```

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
