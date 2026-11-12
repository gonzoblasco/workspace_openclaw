# Práctica del Módulo 5 — Learning

> Las preguntas del Módulo 5, **corridas**. Sin sklearn ni numpy.
> Gate: `python3 run_all.py` → 5 de 5.

```
PASA   p1_knn.py                la maldición crece con la dimensión
PASA   p2_regresion.py          α no cambia el óptimo; el grado sí cambia el test
PASA   p3_confusion.py          accuracy sola premia un clasificador que no detecta nada
PASA   p4_heldout.py            medir sobre train da 1.0 y no dice si generaliza
PASA   p5_qlearning.py          explorar y explotar se miden

RESULTADO: PASA (5 de 5)
```

---

## 1. Nearest neighbor: la frontera, y cuando el "cercano" deja de existir

### La frontera de decisión

```
k=1  (memoriza cada punto)
+++++++++++++++++++++++++++++++--++------
++++++++++++++++++++++++++++++-------+++
...
+++++++++---+++++----------------------
+++++++++++++-+++++++-------------------

k=15 (frontera más suave)
++++++++++++++++++++++++++++++++++++++++
...
+++++++++++++++++++++-------------------
+++++++++++++++++-----------------------
```

Con `k=1` la frontera se retuerce alrededor de cada punto: memoriza el ruido. Con `k=15` los errores sueltos se ahogan en la mayoría de sus vecinos.

### La maldición

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

**El ratio crece con la dimensión y tiende a 1.** En 500 dimensiones, el vecino más cercano y el más lejano están casi a la misma distancia: "el más cercano" deja de tener sentido.

Y no es un problema del algoritmo — es del espacio.

> Un detalle que descubrió el script: con 2000 muestras en 1D, el punto de consulta puede **coincidir** con una muestra y dar distancia 0. Con 400 muestras deja de pasar. La medición necesita que el muestreo no tenga ese accidental.

---

## 2. Regresión: la tasa, la normalización y el overfitting

### La tasa (con datos normalizados)

```
  α          iteraciones al mínimo   estado
  0.001      294                    convergió
  0.01       293                    convergió
  0.05       85                     convergió
  0.1        42                     convergió
  0.5        7                      convergió
  1.0        300                    convergió (oscilando)
```

**Y sin normalizar, el techo caía en α ≈ 0.02.** Eso es lo que apareció cuando la primera versión del script mostró que "el descenso de gradiente diverge para cualquier α razonable". Con `x` en `0..10`, `x²` llega a 100 y el gradiente explota.

**Normalizar no es cosmético: es parte del algoritmo.**

### La divergencia

```
  α=1.0: loss inicial 0.451 → final 8.549e-02 (convergió)
  α=2.0: loss inicial 0.451 → final 1.908e+24 (divergió)
  α=3.0: loss inicial 0.451 → final 9.585e+24 (divergió)
```

Con α grande el error **crece** con las iteraciones. El descenso de gradiente no tiene garantía de bajar: se mueve en la dirección del gradiente, y si el paso es demasiado largo, se pasa del mínimo y sube por el otro lado.

### Overfitting

```
  grado    error en train     error en test      veredicto
  1        0.11               0.23
  2        0.11               0.25
  3        0.02               0.29
  7        0.00               35.39              OVERFIT (peor que el modelo simple en test)
```

**El 7 ajusta 8 puntos perfecto y explota en test.** El 1 tiene más error en train y **menos en test**.

El veredicto de OVERFIT no puede ser "test > 10× train": esa es exactamente la métrica que el modelo sobreajustado manipula. El criterio tiene que ser relativo al modelo sano.

---

## 3. La matriz de confusión: el clasificador que no hace nada

```
Dataset: 2000 casos, 16 positivos (prevalencia 0.8%)

=== "todo negativo" ===
  TP=0     FP=0
  FN=16    TN=1984
  accuracy=0.9920  recall=0.0000  F1=0.0000

=== con señal (sensibilidad 0.90, especificidad 0.95) ===
  TP=14    FP=88
  FN=2     TN=1896
  accuracy=0.9550  recall=0.8750  precision=0.1373  F1=0.2373
```

**El trivial GANA en accuracy (99.2% contra 95.5%) y pierde en todo lo demás.**

Y el de "señal": de cada 102 veces que dice positivo, **sólo 14% lo son**. Eso es el mismo problema de tasa base del Módulo 3, aplicado a un clasificador.

### Qué métrica

| Métrica | Cuándo importa |
|---|---|
| Recall / sensibilidad | Falso negativo caro (diagnóstico) |
| Precision | Falso positivo caro (alarma que molesta) |
| F1 | Sólo si ambos cuestan parecido |
| Accuracy | Casi nunca con clases desbalanceadas |

**La métrica es la decisión de producto**, no un detalle del test.

---

## 4. Holdout: la única forma de saber si un modelo sirve

```
  1. Sobre los mismos datos (k=1):   accuracy = 1.0000
  2. Holdout 70/30:                  accuracy = 0.8333
  3. 5-fold:  particiones ['0.9000','0.7750','0.7500','0.9250','0.9000']
             media = 0.8500   desvío = 0.0725
```

**El 1.0000 no es mejor modelo: es peor pregunta.** Con k=1, cada punto es su propio vecino más cercano y el modelo se memoriza a sí mismo.

**Y k-fold no da un número mejor: da un número con error conocido.**

### El mismo cálculo, sobre el gate del workspace

`heldout.py` verifica que cada cita del outline exista literalmente en el transcript y que el timestamp sea el del bloque que la contiene.

**Ese es el caso correcto**: el transcript es un corpus que el outline **no** usó como señal. Es el test set. Y por eso rechazó **62 de 79** timestamps la primera vez.

Los casos de "accuracy sobre train":

- Un gate que revisa el archivo que escribió (lint de formato).
- Un test escrito copiando la salida actual del código.
- Un chequeo que nunca se corrió contra un caso que debería fallar.

**Los tres dan verde. Los tres miden si el artefacto es igual a sí mismo.**

---

## 5. Q-learning: explorar y explotar, medidos

```
Grilla 8x6: S=inicio, G=premio (+10), X=trampa (-10), #=pared
  S......G
  ..#.....
  ..#.....
  ..#.X...
  .....#..
  ........

=== 1. Con exploración (ε=0.2) ===
  recompensa media, primeros 100 episodios: 5.54
  recompensa media, últimos 100:              8.52
  política aprendida: llegó, 7 pasos

=== 2. Sin exploración (ε=0) ===
  recompensa media, últimos 100: 9.40
  política: llegó, 7 pasos

=== 3. Exploración pura (ε=1.0) ===
  recompensa media, últimos 100: -37.29
```

**Con ε=1 el agente nunca usa lo que aprendió: juega al azar y no llega.**

### Y el resultado que no era el que esperaba

Esperaba que ε=0 se trabara en el primer camino, y medí 40 semillas: **0/40 subóptimos, todos 7 pasos (el óptimo)**.

No contradice la teoría. La precisa:

> **El ε=0 no se traba porque haya una recompensa por el medio que tiente: se traba porque la experiencia que tuvo es la única que conoce.** En un mapa donde el premio está en el borde y el primer camino al azar ya es el único que importa, la experiencia basta.

Con recompensa intermedia, o con trampa, no alcanza. La lección depende del problema, no del parámetro.

Y el patrón se repite del Módulo 4: **el ε que decae —explorar temprano, explotar al final— es la misma forma de simulated annealing.**

---

## Qué queda después de correrlo

| La respuesta de manual | Lo que mostró el código |
|---|---|
| Nearest neighbor es un clasificador | En 500 dimensiones "el más cercano" pierde sentido |
| El descenso de gradiente converge | Con α grande el error **crece**. Normalizar decide si converge |
| α no importa, el óptimo es el mismo | Cierto para el óptimo; falso para si llegás |
| Un modelo con error 0.00 en train es excelente | En test da 35.39. Es overfitting |
| Accuracy mide qué tan bueno es un clasificador | Un modelo que nunca detecta nada saca 99.2% |
| El held-out es una técnica de ML | Es cómo se audita cualquier artefacto, incluido un gate |
| Con ε=0 el agente se traba | Depende del mapa. En 40/40 llegó al óptimo |
| Exploración y explotación es un tema de RL | Es el mismo dilema del annealing y de todo pipeline iterativo |

---

## Cómo volver a correrlo

```bash
cd studies/cs50-ai-python/learning/practica
python3 run_all.py            # las 5
python3 p3_confusion.py       # el clasificador trivial con 99%
python3 p4_heldout.py         # el 1.0000 que no significa nada
```

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
