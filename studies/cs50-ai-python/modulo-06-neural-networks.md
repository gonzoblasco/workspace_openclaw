# Módulo 6 — Neural Networks: clase

> Clase del **Módulo 6** de *Harvard CS50's AI with Python* (Brian Yu).
> Fuentes: `transcripcion.md` (citas con t= verificadas), mis conocimientos, y el código en `neural/practica/`.
> Todo implementado a mano: sin tensorflow, sin numpy.

---

## 6.1 De la neurona al modelo

> "in effect designing an artificial neural network, or an ANN" (9:06:25)

Una neurona es una suma ponderada y una decisión:

```
z = w₁x₁ + w₂x₂ + ... + b
ŷ = [z > 0]
```

Con eso ya hay algo: una recta de decisión. Y ya se había visto que una recta no alcanza para todo.

---

## 6.2 La activación: qué convierte la recta en algo más

> "so this was one way we could define what will come to call an activation function, a function that determines when it is that this output becomes active" (9:10:46)

> "we could use a different function. And there are a number of choices, but the one that we looked at was the logistic sigmoid function" (9:11:04)

| Activación | Fórmula | Derivada máx. |
|---|---|---|
| sigmoid | `1/(1+e⁻ᶻ)` | 0.25 |
| ReLU | `max(0, z)` | 1 |
| softmax | `eᶻⁱ/Σeᶻʲ` | — |

> "Another popular one is the rectified linear unit, otherwise known as ReLU" (9:11:37)

Y softmax en la última capa de un clasificador:

> "the activation function I'm going to use here is called the softmax activation function" (10:23:42)

### El resultado medido, y el que importa

`p2_activaciones.py` verifica numéricamente:

```
  x                  2 capas lineales          1 capa equivalente
  [0.1, 0.5, -0.3]   [-0.016524, -0.69836]     [-0.016524, -0.69836]
  [1.0, -1.0, 0.0]   [-1.583451, -1.950546]    [-1.583451, -1.950546]
```

**Idénticas.** Dos capas lineales son una capa lineal:

```
W₂(W₁x + b₁) + b₂  =  (W₂W₁)x + (W₂b₁ + b₂)
```

**Sin no-linealidad, agregar capas no agrega capacidad.** Es álgebra, no opinión.

### La razón de ReLU: el gradiente que desaparece

```
 2 capas con derivada 0.25 -> gradiente 6.25e-02
 4 capas                  -> 3.91e-03
10 capas                  -> 9.54e-07
```

Con sigmoid, la derivada máxima es 0.25 y fuera de `[-4, 4]` es casi cero. En backpropagation los gradientes se **multiplican** capa por capa: con 10 capas, el que llega a la primera es `10⁻⁶` del que salió. La red deja de aprender abajo.

ReLU lo evita porque su derivada es **1** donde la neurona está activa.

---

## 6.3 El perceptrón y XOR: por qué hizo falta una capa oculta

> "known as a perceptron, can't deal with a situation like this, where we've seen this type of situation before, where there is no straight line that just goes straight through the data" (9:33:39)

`p1_perceptron.py` entrena el mismo perceptrón sobre AND, OR y XOR:

```
  función  errores finales    convergió?
  AND      0                  sí
  OR       0                  sí
  XOR      4                  NO
```

```
  AND: [2, 3, 3, 3, 3, 2] ... [2, 1, 2, 2, 1, 0]
  XOR: [3, 3, 3, 2, 3, 2] ... [4, 4, 4, 4, 4, 4]
```

**XOR nunca llega a cero.** El perceptrón oscila entre dos soluciones que siempre se equivocan en otros dos puntos.

No es falta de entrenamiento: **no hay recta** que separe `{(0,1),(1,0)}` de `{(0,0),(1,1)}`. Y el perceptrón sólo puede trazar una.

> "what was proposed was the idea of a multilayer neural network" (9:34:43)

---

## 6.4 Capas ocultas y backpropagation

> "It has an output layer, but also has one or more hidden layers in between" (9:35:00)

Con una capa oculta, la red compone rectas: dos neuronas ocultas pueden construir las dos que XOR necesita.

> "the idea of this algorithm is known as back propagation" (9:38:10)

### El descenso de gradiente

> "a technique called gradient descent. And what gradient descent is, it is an algorithm for minimizing loss when you're training a neural network" (9:20:45)

> "a method like stochastic gradient descent, which will randomly just choose one data point at a time" (9:24:15)

> "a technique called mini-batch gradient descent" (9:25:21)

### Lo que medí

`p4_gradient_descent.py`, mismo cómputo (20.000 puntos evaluados):

```
  modo           pasos    loss final
  batch          100      10.08
  stochastic     20000    9.69
  mini-batch 8   2500     9.20
```

Y **lo que el experimento no mostró**, que hay que decir: batch no se atascó, y mini-batch no llegó al valle bueno. La pérdida con dos valles no alcanzó para separarlos — el modelo lineal no tiene capacidad para representar la curva, y los cuatro quedaron lejos del óptimo por igual.

**Lo que sí separa es el costo del paso:** batch hizo 100 pasos; stochastic, 20.000, con el mismo cómputo.

Y el patrón que se repite del Módulo 4 y 5: **el ruido del SGD es una forma de exploración**, como la temperatura del annealing y el ε del Q-learning.

---

## 6.5 Backpropagation a mano: la verificación que lo prueba todo

`p3_backprop.py` implementa una red 2-2-1 con sigmoid y cross-entropy, deriva el gradiente a mano, y lo compara con la diferencia central:

```
  parámetro      analítico          numérico           Δ
  W1[0,0]        -0.0461542428      -0.0461542428      8.22e-12
  W1[0,1]        -0.0230771214      -0.0230771214      1.34e-12
  ...
  b2             -0.5173265831      -0.5173265831      8.26e-12

  diferencia máxima: 1.34e-11
  OK  Coinciden en los 9 parámetros.
```

**Esa es la única verificación que convierte "creo que está bien" en "está bien".** El gradiente numérico es el oráculo; el analítico es la implementación. Si difieren, la derivación está mal.

### La simplificación que hace esto tratable

```
δ_salida = ŷ - y
```

Con **sigmoid + cross-entropy**, la derivada de la activación **se cancela** contra la del loss. No queda `σ'(z)` para calcular.

Eso no es magia: es la razón por la que cross-entropy reemplazó al error cuadrático en clasificación. Con MSE, `δ = (ŷ-y)·σ'(z)`, y con `σ' ≤ 0.25` el gradiente se achica 4× por capa desde el principio.

### Y la red aprende XOR

```
  x          y      ŷ          predicción
  [0, 0]     0      0.0003     0
  [0, 1]     1      0.9997     1
  [1, 0]     1      0.9997     1
  [1, 1]     0      0.0004     0
```

**XOR resuelto con dos neuronas ocultas.** Las dos rectas que el perceptrón no podía dibujar las construye la capa oculta; la salida las combina.

### El bug que me costó 6 intentos

`forward()` tenía:

```python
z1 = [sum(w * xi for w, xi in zip(row, x)) + b for row, b in zip(W1, b1)]
```

En Python 3, la variable `w` del **generador** sobrevive a su scope y pisaba la `w` del `zip` exterior... no: el problema real era que el `for w, xi in` interior shadoweaba el nombre, y el error salía como `'int' object is not iterable`. Lo resolví renombrando **todos** los identificadores de comprehension (`wi`, `xi`, `bias`) para que no colisionen con los del `zip` de afuera.

**Lección:** los nombres de variable en comprensiones anidadas en Python 3 no escapan, pero los errores que producen sí son confusos. Renombrar explícito es más barato que depurar.

---

## 6.6 Lo que este módulo le deja al workspace

El curso dice algo que ya está en `AGENTS.md` de otra forma:

> "some more calculus here that we won't get into the details of" (9:38:10)

**Backpropagation es la cadena de responsabilidad del error.** El error de la salida se propaga hacia atrás, capa por capa, hasta el peso que lo causó.

Y eso es exactamente lo que hace un pipeline A/B bien armado: el revisor B dice "esto está mal", y la corrección tiene que llegar al paso que lo produjo, no sólo al último. Si el reporte queda en la superficie, es un forward sin backward: la red no aprende.

**La segunda lección:** el gradiente numérico es el oráculo. Dos implementaciones independientes del mismo cálculo son la única forma de saber que una está bien. Ya apareció en el Módulo 3 (el HMM) y acá vuelve a morder.

---

## Práctica del módulo

Cuatro scripts en `neural/practica/`. Gate: `python3 run_all.py` → **4 de 4**.

| # | Práctica | Afirmación |
|---|---|---|
| 1 | `p1_perceptron.py` | El perceptrón no puede con XOR y no converge |
| 2 | `p2_activaciones.py` | Sin no-linealidad, N capas = 1 capa |
| 3 | `p3_backprop.py` | El gradiente analítico coincide con el numérico |
| 4 | `p4_gradient_descent.py` | Batch y SGD gastan el mismo cómputo distinto |

Ver `practica-modulo-06.md`.

---

## Preguntas para estudiar

1. El perceptrón es una recta. ¿Qué exactamente agrega una capa oculta con activación no lineal?
2. `W₂(W₁x + b₁) + b₂` colapsa a una sola matriz. ¿Qué operación rompe esa igualdad, y por qué?
3. La derivada de la sigmoid tiene máximo 0.25. ¿Por qué eso importa más en una red profunda que en una de dos capas?
4. `δ = ŷ - y` no tiene `σ'`. ¿Dónde se fue la derivada de la activación? ¿Qué se perdió al elegir cross-entropy?
5. El gradiente numérico es lento (2 evaluaciones por parámetro). ¿Por qué se usa igual para verificar?
6. SGD hace 20.000 pasos donde batch hace 100. ¿Qué gana y qué pierde?
7. **La cadena de responsabilidad:** si el revisor B del pipeline A/B dice "esto está mal" pero la corrección sólo se aplica al mensaje final, ¿qué capa no está recibiendo el gradiente?
8. El nombre `w` en una comprensión anidada me costó 6 intentos. ¿Qué reglas de estilo evitan esa clase de bug?

---

## Referencias

- Transcript: `studies/cs50-ai-python/transcripcion.md` (Módulo 6 = cues 2003–2375)
- Outline: `studies/cs50-ai-python/outline.md` (Módulo 6)
- Código: `studies/cs50-ai-python/neural/practica/`
- Proyectos: https://cs50.harvard.edu/ai/2020/

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
