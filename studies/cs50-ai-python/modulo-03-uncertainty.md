# Módulo 3 — Uncertainty: clase

> Clase del **Módulo 3** de *Harvard CS50's AI with Python* (Brian Yu).
> Fuentes: `transcripcion.md` (citas con t= verificadas), mis conocimientos, y el código en `uncertainty/practica/`.
> Sin numpy ni scipy: todo el módulo corre con la librería estándar.

---

## 3.1 Por qué incertidumbre y no otra cosa

> "rarely are our machines going to be able to know things for sure." (3:40:32)

El Módulo 2 asumía un mundo cierto: `P → Q`, `P`, por lo tanto `Q`. El mundo real no funciona así. "Harry visitó Hogwarts" es un hecho de un ejercicio; "está lloviendo" casi nunca se sabe con certeza — se mide.

**La probabilidad no es un parche sobre la lógica: es la lógica que se usa cuando no podés saberlo todo.**

---

## 3.2 Las tres reglas que sostienen todo

### Rango

> "must range between 0 and 1 inclusive." (3:43:16)

`0` es imposible, `1` es seguro. Nada en el medio se inventa: se calcula.

### Probabilidad condicional

> "conditional probability is the degree of belief in a proposition given some evidence that has already been revealed to us." (3:49:37)

`P(a | b)` = creencia en `a` dado que `b` ya pasó.

### Independencia

> "independence refers to the idea that the knowledge of one event" (4:01:27)

Dos eventos son independientes si conocer uno no cambia nada del otro. **Sin esa suposición, una red bayesiana es imposible**: 30 variables interconectadas tendrían una tabla de `2³⁰` filas.

### Y la que hace todo el trabajo

> "in probability theory, which is known as Bayes rule." (4:06:02)

```
P(a|b) = P(b|a) · P(a) / P(b)
```

**Bayes invierte una condicional.** Y el error más común de todo el campo es confundir `P(a|b)` con `P(b|a)`.

`p1_probabilidad.py` lo mide con 200.000 experimentos:

```
P(W|R) = 0.9014   (si llueve, casi seguro me mojo)
P(R|W) = 0.6596   (si me mojé, ¿llovió?)
```

**Muy distintos.** La lluvia es rara (30%), así que la mayoría de las veces que te mojaste no había llovido. Bayes corrige por cuán común es la causa. Es el **error de tasa base**, y no se ve en la fórmula: se ve corriendo.

---

## 3.3 Variables aleatorias y modelos

> "we call a variable in probability theory a random variable." (3:57:06)

Una variable que puede tomar varios valores, cada uno con una probabilidad.

Y la regla del producto, que es la base de todo:

> "the probability of A and B as the probability of A times the probability of B given A" (3:56:36)

```
P(a ∧ b) = P(a) · P(b|a)
```

---

## 3.4 Redes bayesianas: la estructura es el cálculo

> "the first of the models we're going to talk about are what are known as Bayesian networks. And a Bayesian network is just going to be some network of random variables" (4:29:22)

Un grafo dirigido acíclico donde las flechas dicen "esta variable depende de aquella". Cada nodo tiene una tabla de probabilidad condicionada a sus **padres**.

La factorización, que es todo el punto:

```
P(X1, ..., Xn) = Π P(Xi | padres(Xi))
```

### Por qué eso importa más de lo que parece

`p2_red_bayesiana.py` cuenta los números que hay que escribir:

| Variables | Conjunta `2ⁿ` | Cadena, cada una con 1 padre | Factor |
|---|---|---|---|
| 3 | 8 | 7 | 1× |
| 10 | 1.024 | 28 | 37× |
| 20 | 1.048.576 | 58 | 18.079× |
| 30 | 1.073.741.824 | 88 | **12.201.612×** |

**Mil millones de entradas contra 88 números.** La notación matemática del curso (`Π P(Xi | padres)`) no es una forma más corta de escribir lo mismo: es la diferencia entre calcular y no poder calcular.

**Y el límite del truco:** si un nodo tiene 20 padres, su tabla local ya tiene `2²⁰` filas. La factorización no elimina el exponencial — lo mueve de la cantidad de variables al ancho de la vecindad más grande.

---

## 3.5 Inferencia por enumeración: la respuesta exacta

> "you'll need to normalize them at the end" (4:48:57)

Dada la red y una evidencia, ¿cuál es la distribución de la consulta? Se suman las probabilidades de los mundos que cumplen la evidencia y se normaliza.

```
P(R=T | W=T) = 0.6585
```

Y **no es 0.90**, aunque `P(W=T | R=T) = 0.90`. Es Bayes.

**El costo:** con `n` variables, `2ⁿ` mundos por consulta. Exacto siempre, e impagable pasado cierto tamaño.

---

## 3.6 Sampling: exactitud por velocidad

> "one method is through a procedure known as sampling." (5:00:37)

Cuando enumerar no es posible, se estima mirando muestras.

| Método | Qué hace | Problema |
|---|---|---|
| Prior sampling | Genera mundos completos y filtra por evidencia | Desperdicia casi todas las muestras |
| Rejection sampling | Igual, con nombre propio | El mismo desperdicio |
| **Likelihood weighting** | Fija la evidencia y **pondera** por su probabilidad | Sesgo si las evidencias hijas son muchas |

> "One such sampling method is called likelihood weighting." (5:09:05)

`p4_sampling.py` lo mide con el mismo presupuesto:

```
Verdad exacta: P(R=T | W=T) = 0.6585

método                   estimación     muestras usadas    error
prior sampling           0.6573        8219 (41%)          0.0013
likelihood weighting     0.6591        20000 (100%)        0.0006
```

Con dos condiciones simultáneas el desperdicio se pone peor: prior sampling baja a ~23% de las muestras y su error sube 9×.

**Y la honestidad del método:** likelihood weighting **no es exacto**. El error baja como `1/√n`. Cuatro decimales de exactitud piden cien millones de muestras. Sampling es más rápido, no más verdadero.

---

## 3.7 HMM y filtrado: el estado está oculto

> "what's called a Markov chain, where a Markov chain is just some sequence of random variables" (5:14:36)

Con estado que cambia en el tiempo, el modelo es una cadena de Markov: **sólo importa el estado anterior**.

> "before, we're going to use what we call a hidden Markov model." (5:23:57)

En un HMM el estado real está oculto y sólo se observan emisiones.

Y la tarea central:

> "One task is called filtering, which is given observations from the start until now, calculate the distribution for the current state" (5:27:48)

```
predicción:    P(S_t) = Σ P(S_t | S_{t-1}) · P(S_{t-1} | evidencia)
actualización: P(S_t | e_t) ∝ P(e_t | S_t) · P(S_t)
```

### El orden importa, y la primera versión estaba mal

Escribí tres versiones del filtrado antes de que diera bien:

1. **Transición primero, emisión después** → no coincidía con la fuerza bruta (0.7174 contra 0.9529).
2. **Evidencia con emisión desplazada** → peor.
3. **Emisión primero, transición después** → coincidencia exacta en los tres pasos.

La recursión del filtrado es **emitir y después transicionar**. Al revés contesta otra pregunta y devuelve números plausibles que no son los buscados. La fuerza bruta lo agarró.

```
t    filtrado     fuerza bruta   coincide
1    0.6923       0.6923         sí
2    0.9054       0.9054         sí
3    0.9420       0.9420         sí
```

### El límite de la suposición de Markov

Si el clima tuviera memoria de tres días, el HMM de un paso daría probabilidades incorrectas y **la recursión no tendría cómo darse cuenta**: sigue sumando 1 y se ve perfectamente sana desde adentro.

Es el mismo problema de la heurística no admisible del Módulo 1: **una suposición falsa no rompe el cálculo, rompe la garantía.**

---

## 3.8 La parte que se aplica al workspace

`p6_gate_bayes.py` aplica Bayes a la decisión que se toma cien veces por sesión:

> Cuando un gate da verde, ¿qué se sigue?

```
P(bien | pasa) = P(pasa | bien) · P(bien) / P(pasa)
```

Con sensibilidad 0.90 y especificidad 0.95 —un gate bueno— variando sólo la **tasa base**:

| Tasa base de cambios bien | P(bien \| pasa) |
|---|---|
| 0.99 | 0.9994 |
| 0.90 | 0.9939 |
| 0.50 | 0.9474 |
| 0.20 | 0.8182 |
| 0.05 | 0.4865 |
| **0.01** | **0.1538** |

**El mismo gate en las siete filas.** Lo que cambia es cuánto significa que haya pasado.

### El gate nuevo, sin historial

Un check recién escrito, corrido sobre un repo donde nunca falló, tiene tasa base 1.0 y posterior **1.0 por construcción**. Ese 100% no es evidencia: es la definición de no haber corrido nunca el caso que lo rompe.

Es exactamente lo que el Módulo 1 encontró en la reapertura y que `AGENTS.md` ya documenta: **una verificación que da verde sin haber verificado**. La probabilidad condicional explica por qué: la tasa base del caso roto es 0, y entonces `P(bien | pasa)` no se movió.

Y algo que parece un error y no lo es: **un verde aporta siempre +2.89 de log-odds**, en todas las filas. La evidencia de un evento es independiente del prior. Lo que cambia es de dónde se parte: con prior 0.05, subir 2.89 te deja en 0.49 — seguís sin poder afirmar nada.

---

## Práctica del módulo

Seis scripts en `uncertainty/practica/`. Gate: `python3 run_all.py` → **6 de 6**.

| # | Práctica | Afirmación |
|---|---|---|
| 1 | `p1_probabilidad.py` | Tres identidades se sostienen en la simulación; `P(W\|R) ≠ P(R\|W)` |
| 2 | `p2_red_bayesiana.py` | La factorización coincide y ahorra 12 millones de veces |
| 3 | `p3_enumeracion.py` | `P(R\|W=T) = 0.6585`, exacta y no 0.90 |
| 4 | `p4_sampling.py` | Likelihood weighting usa el 100% de las muestras |
| 5 | `p5_hmm.py` | El filtrado recursivo coincide con la fuerza bruta |
| 6 | `p6_gate_bayes.py` | Un verde no vale nada sin tasa base |

Ver `practica-modulo-03.md` para la salida real.

---

## Preguntas para estudiar

1. `P(a|b) ≠ P(b|a)`. ¿Qué tiene que pasar para que sí sean iguales? ¿Por qué eso casi nunca ocurre en la práctica?
2. ¿Qué gana una red bayesiana exactamente al suponer independencia condicional? ¿Qué pierde si la suposición es falsa — y cómo se notaría?
3. Enumerar es exacto y sampling no. ¿Por qué la gente elige sampling en producción? ¿Qué evidencia te haría volver a enumerar?
4. Likelihood weighting pondera en vez de descartar. ¿Cuándo esa ponderación se vuelve tan mala como descartar?
5. El filtrado recursivo asume Markov. Si el proceso tiene memoria de `k` pasos, ¿qué se hace? ¿Se puede arreglar sin cambiar la estructura?
6. **El cálculo del gate:** si tu pre-commit pasa siempre, ¿cuánta información te da? ¿Qué haría falta para que un verde signifique algo?
7. Un gate con especificidad 0.95 tiene 5% de falsos positivos. En un repo con 1000 cambios correctos y 1 roto, ¿cuántas fallas ves? ¿Qué te dice eso sobre interpretar un rojo?
8. ¿En qué se parecen la suposición de Markov en `p5` y la heurística no admisible del Módulo 1? ¿En qué se diferencia el síntoma?

---

## Referencias

- Transcript: `studies/cs50-ai-python/transcripcion.md` (Módulo 3 ≈ cues 731–1150)
- Outline: `studies/cs50-ai-python/outline.md` (Módulo 3)
- Código: `studies/cs50-ai-python/uncertainty/practica/`
- Proyectos: https://cs50.harvard.edu/ai/2020/

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
