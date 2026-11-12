# Práctica del Módulo 6 — Neural Networks

> Las preguntas del Módulo 6, **corridas**. Todo a mano: sin tensorflow, sin numpy.
> Gate: `python3 run_all.py` → 4 de 4.

```
PASA   p1_perceptron.py             el perceptrón no puede con XOR y no converge
PASA   p2_activaciones.py           sin no-linealidad, N capas = 1 capa
PASA   p3_backprop.py               el gradiente analítico coincide con el numérico
PASA   p4_gradient_descent.py       batch y SGD gastan el mismo cómputo distinto

RESULTADO: PASA (4 de 4)
```

---

## 1. El perceptrón: no puede con XOR

```
  función  errores finales    convergió?
  AND      0                  sí             w=[0.17, 0.29] b=-0.37
  OR       0                  sí             w=[0.17, 0.69] b=-0.07
  XOR      4                  NO             w=[-0.13, -0.01] b=0.03
```

**La firma del fracaso:**

```
  AND: [2, 3, 3, 3, 3, 2] ... [2, 1, 2, 2, 1, 0]
  XOR: [3, 3, 3, 2, 3, 2] ... [4, 4, 4, 4, 4, 4]
```

AND converge en pocas épocas y se queda. XOR **nunca llega a cero**: oscila entre dos soluciones que siempre se equivocan en otros dos puntos.

No es falta de entrenamiento. **No hay recta** que separe `{(0,1),(1,0)}` de `{(0,0),(1,1)}`.

### La salida es lineal, y se ve en la fórmula

```
w1·x1 + w2·x2 + b = 0
    ⟹  x2 = -(w1/w2)·x1 - b/w2
```

Es una recta. Nunca una curva. XOR necesita dos rectas:

```
h1 = OR(x1, x2)     h2 = NAND(x1, x2)     y = AND(h1, h2)
```

Lo que Minsky y Papert señalaron en 1969, en 20 líneas.

---

## 2. Sin no-linealidad, N capas = 1 capa

### Las tres activaciones

```
  z        sigmoid      relu       d(sigmoid)     d(relu)
  -3       0.0474       0.00       0.0452         0.00
   0       0.5000       0.00       0.2500         0.00
   3       0.9526       3.00       0.0452         1.00
```

Sigmoid satura en los extremos (derivada 0.045 en `z=3`); ReLU tiene derivada **1**.

### Softmax

```
  z=[1, 1, 1]      -> p=[0.3333, 0.3333, 0.3333]  suma=1.0000
  z=[0, 0, 10]     -> p=[0.0, 0.0, 0.9999]        suma=1.0000
```

Con `[1,1,1]` la red no se decide. Con `[0,0,10]` está segura.

### La verificación numérica

```
  x                  2 capas lineales          1 capa equivalente
  [0.1, 0.5, -0.3]   [-0.016524, -0.69836]     [-0.016524, -0.69836]
  [1.0, -1.0, 0.0]   [-1.583451, -1.950546]    [-1.583451, -1.950546]
  [0.3, 0.3, 0.3]    [-0.674676, -0.71307]     [-0.674676, -0.71307]

  Idénticas en las tres entradas. La segunda capa no agregó nada.
```

`W₂(W₁x + b₁) + b₂ = (W₂W₁)x + (W₂b₁ + b₂)`. **Es álgebra, no opinión.**

### Y el gradiente que desaparece

```
 2 capas con derivada 0.25 -> 6.25e-02
 4 capas                   -> 3.91e-03
 6 capas                   -> 2.44e-04
10 capas                   -> 9.54e-07
```

Con 10 capas, el gradiente que llega a la primera es `10⁻⁶` del que salió. **La red deja de aprender abajo.** ReLU lo evita porque su derivada es 1, no 0.25.

---

## 3. Backpropagation: la verificación que lo prueba

```
  parámetro      analítico          numérico           Δ
  W1[0,0]        -0.0461542428      -0.0461542428      8.22e-12
  W1[0,1]        -0.0230771214      -0.0230771214      1.34e-12
  W1[1,0]        0.0643564294       0.0643564295       1.34e-11
  W1[1,1]        0.0321782147       0.0321782147       1.16e-12
  b1[0]          -0.0769237381      -0.0769237381      1.10e-12
  b1[1]          0.1072607157       0.1072607157       1.70e-12
  W2[0]          -0.1284681920      -0.1284681920      3.04e-13
  W2[1]          -0.2318267096      -0.2318267096      6.75e-12
  b2             -0.5173265831      -0.5173265831      8.26e-12

  diferencia máxima: 1.34e-11
  OK  Coinciden en los 9 parámetros. El backprop está bien derivado.
```

**El gradiente numérico es el oráculo; el analítico es la implementación.** Si difieren, la derivación está mal. Es la única verificación que convierte "creo que está bien" en "está bien".

### La simplificación que hace esto tratable

```
δ_salida = ŷ - y
```

Con sigmoid + cross-entropy, la derivada de la activación **se cancela** contra la del loss. No queda `σ'(z)`.

Con MSE, `δ = (ŷ-y)·σ'(z)`, y con `σ' ≤ 0.25` el gradiente se achica 4× **por capa** desde el principio. Es la razón por la que cross-entropy reemplazó a error cuadrático en clasificación.

### Y aprende XOR

```
  loss por época: 0.3771 -> 0.000302 en 4000 épocas

  x          y      ŷ          predicción
  [0, 0]     0      0.0003     0
  [0, 1]     1      0.9997     1
  [1, 0]     1      0.9997     1
  [1, 1]     0      0.0004     0
```

**XOR resuelto con dos neuronas ocultas.** Las dos rectas que el perceptrón no podía dibujar las construye la capa oculta.

### El bug que costó 6 intentos

`forward()` tenía un `zip` anidado donde la variable del generador interior shadoweaba a la de afuera:

```python
z1 = [sum(w * xi for w, xi in zip(row, x)) + b for row, b in zip(W1, b1)]
```

El error salía como `'int' object is not iterable` y señalaba la línea equivocada. Lo resolví renombrando **todos** los identificadores de la comprensión (`wi`, `xi`, `bias`) para que no colisionen con los del `zip` de afuera.

**Lección:** los nombres de variable en comprensiones anidadas en Python 3 no escapan, pero los errores que producen sí son confusos. Renombrar explícito es más barato que depurar.

---

## 4. Batch vs SGD: mismo cómputo, distinto

```
=== Mismo presupuesto: 20.000 puntos evaluados ===
  modo           pasos    loss final
  batch          100      10.0829
  stochastic     20000    9.6927
  mini-batch 8   2500     9.1987
  mini-batch 32  625      9.1708
```

```
=== 40 semillas ===
  modo           loss media     loss mejor     atascado
  batch          10.0829        10.0829        0/40
  stochastic     9.6789         9.1957         0/40
  mini-batch 8   9.2169         9.1652         0/40
```

**Batch es determinista:** las 40 semillas dan la misma loss, porque no usa el azar.

### Lo que el experimento NO mostró

Batch no se atascó, y mini-batch **ni llegó al valle bueno**. La pérdida con dos valles no alcanzó para separarlos: el modelo lineal no tiene capacidad para representar la curva, y los cuatro quedaron lejos del óptimo por igual.

**Lo que sí separa es el costo del paso:** batch hizo 100 pasos; stochastic, 20.000, con el mismo cómputo.

Y lo que se busca en SGD es eso: con dataset grande, promediar todo por paso es carísimo; con un punto por paso hacés 100× más updates. **El ruido es exploración**, como la temperatura del annealing (M4) y el ε del Q-learning (M5).

---

## Qué queda después de correrlo

| La respuesta de manual | Lo que mostró el código |
|---|---|
| El perceptrón es un clasificador | No converge en XOR, nunca, y no hay recta que lo salve |
| Agregar capas agrega capacidad | Sólo con no-linealidad. Sin ella, N capas = 1 capa, medido |
| Sigmoid es la activación clásica | Su derivada máxima 0.25 mata 10 capas |
| Backprop es "propagar el error" | Es un gradiente que hay que verificar contra el numérico |
| Cross-entropy es una elección de loss | Es la que cancela `σ'` y hace tratable el gradiente |
| SGD es una versión barata de batch | Usa 200× más pasos con el mismo cómputo |
| El ruido del SGD es un defecto | Es exploración, como la temperatura del annealing |
| Los nombres de variable son cosmética | Un shadowing en un `zip` me costó 6 intentos |

---

## Cómo volver a correrlo

```bash
cd studies/cs50-ai-python/neural/practica
python3 run_all.py              # las 4
python3 p3_backprop.py          # el gradiente analítico vs el numérico
python3 p2_activaciones.py      # N capas lineales = 1 capa
```

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
