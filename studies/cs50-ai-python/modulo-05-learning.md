# Módulo 5 — Learning: clase

> Clase del **Módulo 5** de *Harvard CS50's AI with Python* (Brian Yu).
> Fuentes: `transcripcion.md` (citas con t= verificadas), mis conocimientos, y el código en `learning/practica/`.
> Este es el módulo donde el curso toca algo que el workspace **ya tiene adoptado**: `ADOPCION.md` y `heldout.py`.

---

## 5.1 Lo que cambia

> "one of the most popular is the idea of supervised machine learning, or just supervised learning." (7:20:00)

Hasta acá: escribías la regla. En aprendizaje le das al sistema **entradas y salidas** y el sistema descubre la regla.

```
Datos: (x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)
Objetivo: f tal que f(x) ≈ y
```

Y la consecuencia que hay que tener presente todo el módulo: **no escribís `f`, la elegís de una familia y la ajustás**. La calidad del resultado depende tanto de los datos como de la elección.

---

## 5.2 Dos tareas: clasificación y regresión

> "we hope that our computer will be able to figure out some function that, given those inputs, is able to get those outputs" (7:20:49)

- **Clasificación:** `y` es una categoría. ¿Spam o no? ¿Gato o perro?
- **Regresión:** `y` es un número. ¿A qué precio? ¿Cuánta lluvia?

Y un primer algoritmo, el más simple de todos:

> "a very popular and common machine learning algorithm known as nearest neighbor classification" (7:27:04)

**Nearest neighbor no aprende nada**: guarda los datos y elige al momento de clasificar.

> "K nearest neighbor classification algorithm, where K is some parameter" (7:29:18)

### La maldición de la dimensionalidad — medido

`p1_knn.py` mide qué tan lejos está el vecino más cercano en `d` dimensiones:

```
  dims     vecino más cercano     vecino más lejano    ratio
  1        0.0002                 0.9048               0.000
  2        0.0234                 0.9835               0.024
  5        0.1756                 1.4408               0.122
  10       0.6588                 1.9719               0.334
  50       2.2032                 3.5773               0.616
  100      3.4886                 4.9398               0.706
  500      8.5783                 9.7640               0.879
```

**El ratio crece con la dimensión y tiende a 1.** Con 500 dimensiones, casi no hay diferencia entre el vecino más cercano y el más lejano: todos están a la misma distancia.

Eso mata al nearest neighbor en alta dimensión. **Y no es un problema del algoritmo: es del espacio.** Ningún algoritmo basado en distancia escapa de eso.

---

## 5.3 Regresión lineal y descenso de gradiente

> "a technique known as linear regression to find some sort of line that will separate the two halves from each other" (7:32:31)

Y para el ajuste, el mismo descenso de gradiente del Módulo 4:

> "in an optimization problem, as you recall from before, we were either trying to maximize some objective function" (8:01:11)

### Lo que medí, y el hallazgo que no estaba en el plan

```
Datos normalizados a [-1, 1]

  α          iteraciones al mínimo   estado
  0.001      294                    convergió
  0.01       293                    convergió
  0.05       85                     convergió
  0.1        42                     convergió
  0.5        7                      convergió
  1.0        300                    convergió (oscilando)
```

**Sin normalizar, el techo caía en α ≈ 0.02.** Con `x` en `0..10`, `x²` llega a 100 y el gradiente explota para cualquier paso razonable. La primera versión del script parecía demostrar que "el descenso de gradiente no funciona" — y lo que estaba mal eran los datos.

**Normalizar no es cosmético: es parte del algoritmo.** Y esa es la primera lección que un curso de ML real tiene que enseñar.

---

## 5.4 Overfitting: el modelo que gana en train y pierde en test

> "a problem known as overfitting. And overfitting is a big problem that you can encounter in machine learning, which happens anytime a model fits too closely with a data" (8:08:29)

```
8 puntos de entrenamiento, polinomio de grado d

  grado    error en train     error en test      veredicto
  1        0.11               0.23
  2        0.11               0.25
  3        0.02               0.29
  7        0.00               35.39              OVERFIT
```

**El grado 7 ajusta los 8 puntos casi perfecto (error 0.00) y explota en test (35.39).** El grado 1 tiene más error en train y menos en test.

**Un modelo mejor en los datos que vio puede ser peor en los que no vio.** Esa es la definición, y la razón por la que existe el held-out.

### La regularización

> "you'll see us add some regularizing term to what we're trying to minimize in order to avoid this problem of overfitting" (8:15:04)

Penalizar la complejidad del modelo dentro de la función de costo. Un modelo complejo tiene que ganar por mucho al simple para que valga la pena.

---

## 5.5 Holdout: la única forma de saber si un modelo sirve

> "the key idea is separating the training data from the testing data" (8:18:07)

> "you could employ a method known as holdout cross-validation, where in holdout cross-validation, we split up our d" (8:15:36)

### Medido

`p4_heldout.py`, sobre el mismo clasificador:

```
  1. Sobre los mismos datos (k=1):   accuracy = 1.0000
  2. Holdout 70/30:                  accuracy = 0.8333
  3. 5-fold:                         media 0.8500, desvío 0.0725
```

**El 1.0000 no es mejor modelo: es peor pregunta.** Con k=1 cada punto es su propio vecino más cercano y el modelo se memoriza a sí mismo.

Y k-fold no da un número mejor: **da un número con error conocido**.

### El gate del workspace es este mismo cálculo

`studies/cs50-ai-python/heldout.py` verifica que cada cita del outline exista **literalmente** en el transcript, y que el timestamp sea el del bloque que la contiene.

**Ese es el caso correcto:** el transcript es un corpus que el outline **no** usó como señal. Es el test set, no el train set. Y por eso rechazó 62 de 79 timestamps la primera vez.

Lo que sería "accuracy sobre train":

- Un gate que revisa el mismo archivo que escribió (lint de formato).
- Un test escrito copiando la salida actual del código.
- Un chequeo que nunca se corrió contra un caso que debería fallar.

**Los tres dan verde. Los tres miden si el artefacto es igual a sí mismo.**

---

## 5.6 La matriz de confusión: por qué la exactitud sola miente

El curso evalúa los modelos por matriz de confusión, y la práctica lleva eso a su forma más incómoda.

Dataset con prevalencia del 0.8% (16 positivos sobre 2000):

```
=== Clasificador trivial: "todo negativo" ===
  TP=0     FP=0
  FN=16    TN=1984
  accuracy=0.9920  recall=0.0000  F1=0.0000

=== Clasificador con señal (sensibilidad 0.90, especificidad 0.95) ===
  TP=14    FP=88
  FN=2     TN=1896
  accuracy=0.9550  recall=0.8750  precision=0.1373  F1=0.2373
```

**El trivial GANA en accuracy (99.2% contra 95.5%) y pierde en todo lo demás.**

Si elegís el modelo por accuracy, descartás el único que detecta algo.

### Qué métrica, y por qué

| Métrica | Cuándo importa |
|---|---|
| **Recall** / sensibilidad | Cuando un falso negativo cuesta caro (diagnóstico) |
| **Precision** | Cuando un falso positivo cuesta caro (alarma que molesta) |
| **F1** | Sólo si ambos errores cuestan parecido |
| **Accuracy** | Casi nunca, con clases desbalanceadas |

Y el costo de cada error **no es un número objetivo: se elige.** Un filtro de spam prefiere perder un spam antes que bloquear un email del jefe. Un detector de fraude prefiere lo contrario.

**La métrica es la decisión de producto, no un detalle del test.**

---

## 5.7 Aprendizaje por refuerzo

> "the idea of reinforcement learning is rather t" (8:28:50)

Sin dataset: el agente actúa, recibe recompensa y aprende de la experiencia.

### El modelo

> "we need to do is formalize this notion of what we mean about states and actions and rewards" (8:31:56)

Un **MDP** (proceso de decisión de Markov): estados, acciones, recompensas.

### Q-learning

> "we would like to be able to learn in this state taking this action, is that a good thing or a bad thing?" (8:38:43)

```
Q(s,a) ← Q(s,a) + α · [ r + γ · max Q(s',a') - Q(s,a) ]
```

Aprende el valor de tomar cada acción en cada estado, sin conocer el modelo del mundo.

### El dilema

> "it's never going to explore and go along that route instead. So in reinforcement learning, there is this tension between exploration and exploitation." (8:48:25)

- **Exploración:** probar cosas nuevas.
- **Explotación:** usar lo que ya sabés que funciona.

### Medido

```
  ε        recompensa final     política
  0.0      9.40                 llegó (7 pasos)
  0.2      8.52                 llegó (7 pasos)
  1.0      -37.29               (no llega al premio)
```

**Con ε=1 (exploración pura) nunca usa lo que aprendió: juega al azar.**

**Y con ε=0** —medido en 40 semillas sobre un mapa con recompensa al final— **también llegó, 0/40 subóptimos.** Eso no contradice la teoría: la precisa. En un mapa donde el premio está en el borde y el primer camino al azar es el único que importa, la experiencia basta.

**El ε=0 no se traba porque haya una recompensa por el medio que tiente: se traba porque la experiencia que tuvo es la única que conoce.** Con recompensa intermedia, o con trampa, no alcanza.

Y el patrón se repite del Módulo 4: **el ε que decae —explorar temprano, explotar al final— es la misma forma de simulated annealing.**

---

## 5.8 Lo que este módulo le hace al workspace

Es el primer módulo donde el curso **confirma algo que ya está corriendo**, en vez de agregar algo nuevo.

| Idea del curso | Ya existe en el workspace |
|---|---|
| Train/test split | `heldout.py` sobre las clases |
| Overfitting | El gate que da verde sobre su propio archivo |
| Matriz de confusión | El conteo de verdades de un gate |
| Métrica = decisión | `verification-gates` (exit 0 / 1 / 3) |
| Exploración vs explotación | Pipeline A/B (más vuelta del mismo modelo = explotación) |

Y `ADOPCION.md` ya lo documentó: el curso se adoptó por esta sola idea, y el artefacto es `heldout.py`. El resto del módulo es comprensión, no adopción nueva.

---

## Práctica del módulo

Cinco scripts en `learning/practica/`. Gate: `python3 run_all.py` → **5 de 5**.

| # | Práctica | Afirmación |
|---|---|---|
| 1 | `p1_knn.py` | La maldición crece con la dimensión y tiende a 1 |
| 2 | `p2_regresion.py` | α no cambia el óptimo; el grado sí cambia el test |
| 3 | `p3_confusion.py` | Accuracy sola premia un clasificador que no detecta nada |
| 4 | `p4_heldout.py` | Medir sobre train da 1.0 y no dice si generaliza |
| 5 | `p5_qlearning.py` | Explorar y explotar se miden; ε que decae |

Ver `practica-modulo-05.md`.

---

## Preguntas para estudiar

1. Un clasificador con 99% de accuracy no detecta ningún caso positivo. ¿Qué métrica te lo habría dicho, y por qué la accuracy no?
2. Nearest neighbor no aprende. ¿Qué guarda en vez de aprender, y por qué eso lo hace inútil en alta dimensión?
3. El descenso de gradiente converge con α=0.5 y oscila con α=1.0. ¿Qué propiedad de la función de costo decide ese límite?
4. Un polinomio de grado 7 ajusta 8 puntos con error 0.00 y explota en test. ¿Qué haría la regularización para evitarlo? ¿Qué paga?
5. Holdout da 0.833; 5-fold da 0.850 ± 0.07. ¿Por qué el segundo número es **más** informativo aunque sea distinto?
6. **El gate del workspace:** si un check nunca falló, ¿qué mide su verde? Formulalo con la tasa base del Módulo 3.
7. Q-learning con ε=0 llegó al óptimo en 40/40 corridas. ¿Contradice la teoría de exploración/explotación, o el mapa es el que no la necesita? ¿Qué mapa haría falta para ver el fallo?
8. El ε que decae y la temperatura del annealing son la misma forma. ¿Qué comparten los dos problemas que hace que la solución sea idéntica?

---

## Referencias

- Transcript: `studies/cs50-ai-python/transcripcion.md` (Módulo 5 = cues 1617–2002)
- Outline: `studies/cs50-ai-python/outline.md` (Módulo 5)
- Código: `studies/cs50-ai-python/learning/practica/`
- Adopción: `studies/cs50-ai-python/ADOPCION.md`
- Proyectos: https://cs50.harvard.edu/ai/2020/

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
