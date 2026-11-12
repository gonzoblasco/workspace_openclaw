# Módulo 1 — Search: clase

> Clase del **Módulo 1** de *Harvard CS50's AI with Python* (Brian Yu), armada sobre `studies/cs50-ai-python/`.
> Fuentes: el transcript del curso (`transcripcion.md`, citas con t= verificados), mis conocimientos, y el código que corre en `search/astar.py`.
> Sigo el formato del curso: primero la idea, después el código, al final las preguntas. **Los ejercicios no son opcionales** — son donde la teoría se verifica.

---

## 1.1 Qué es un problema de búsqueda (0:06:04)

Un agente que debe llegar de un estado inicial a un objetivo por una secuencia de acciones. Ejemplo del curso: el perro robótico que tiene que salir de un laberinto.

> "This is an example of what you might call a search problem." (0:06:04)

Todo problema de búsqueda tiene **cinco piezas**. Si falta una, no hay problema que resolver:

| Pieza | Qué es | En el laberinto |
|---|---|---|
| **Estado inicial** | La configuración que tenés ahora | `A` en la esquina |
| **Acciones** | Lo que podés hacer | Moverte arriba/abajo/izquierda/derecha |
| **Modelo de transición** | Qué estado resulta de aplicar una acción | `(x,y) + (dx,dy)`, si no es pared |
| **Test de objetivo** | La condición que dice si llegaste | `estado == B` |
| **Costo de camino** | Cuánto cuesta cada paso | 1 por movimiento |

> "A state is just some configuration of the agent in its environment." (0:07:49)
> "And in order to do that, we'll introduce to our AI a transition model, which" (0:09:56)
> "is a goal test, some way to determine whether a given state is a goal state." (0:13:30)
> "we'd really like to find one that minimizes this path cost." (0:14:51)

**La clave:** el algoritmo es *cómo ordenás lo que te queda por explorar*. Nada más. Cambiá la estructura de datos y tenés otro algoritmo.

> "to be stored inside of a single data structure that we'll call the frontier." (0:19:12)

---

## 1.2 La frontier: una sola idea, cuatro algoritmos

La **frontier** guarda los nodos que sabés que existen pero todavía no exploraste. La pregunta que decide todo es: **¿cuál saco primero?**

| Estructura | Orden de salida | Algoritmo |
|---|---|---|
| Pila (LIFO) | El último que entró | **DFS** |
| Fila (FIFO) | El primero que entró | **BFS** |
| Cola de prioridad por `h(n)` | El que parece más cerca | **Greedy best-first** |
| Cola de prioridad por `g(n) + h(n)` | El que combina lo pagado + lo estimado | **A\*** |

### DFS — profundidad (0:30:36)

> "this way the algorithm ends up working when we use a stack that we call this version of the algorithm depth first search." (0:30:36)

Explora lo más profundo posible. Ahorra memoria (guarda solo un camino), pero **no garantiza optimalidad** y puede caer en un pozo. En un laberinto finito siempre encuentra solución: explora todo si hace falta (0:34:37).

### BFS — anchura (0:30:52)

> "It turns out that there's another algorithm called breadth first search," (0:30:52)

Explora por niveles. Garantiza el **camino más corto** cuando todos los pasos cuestan lo mismo, al precio de guardar muchísimos nodos. En la demo del curso, `maze2` le costó **77 estados** contra **casi 400** de DFS (0:50:08) — DFS llegó por suerte por un camino largo.

---

## 1.3 Greedy best-first: el que elige por olfato (0:57:05)

> "Greedy best-first search, often abbreviated G-BFS, is a search algorithm that instead of expanding the deepest node like DFS or the shallowest node like BFS, this algorithm is always going to expand the node that it thinks is closest to the goal." (0:57:05)

La heurística del curso es la **distancia Manhattan**: `|x1-x2| + |y1-y2|`, ignorando las paredes.

> "And it's something called the Manhattan distance," (0:58:57)

**Por qué falla:** ignora cuánto costó llegar. Si el camino directo está bloqueado, se mete en un desvío largo igual, porque el desvío "parecía cerca".

Esto se ve en `maze-b` del ejercicio:

```
greedy best-first    costo=47  expandidos=48
A*                   costo=41  expandidos=81
```

Greedy expandió **casi la mitad** de nodos que A\*, y aun así devolvió un camino **6 pasos más caro**. Ese es el trato: velocidad por optimalidad.

---

## 1.4 A\*: lo pagado más lo que falta (1:07:45)

> "into a more formal algorithm known as A star search. A star search is going to solve this problem by instead of just considering the heuristic, also considering how long it took us to get to any particular state." (1:07:45)

A\* ordena por **`f(n) = g(n) + h(n)`**:

- `g(n)`: costo real para llegar a `n` (lo que ya pagaste)
- `h(n)`: estimación de lo que falta hasta el objetivo
- `f(n)`: estimación del costo **total** del camino que pasa por `n`

La intuición: no elijas el que parece más cerca del final, elegí el que **en total** promete ser más barato.

### Admisibilidad: el contrato que hace a A\* óptimo (1:11:55)

> "So the conditions are H of n, my heuristic, needs to be admissible. What does it mean for a heuristic to be admissible? Well, a heuristic is admissible if it never overestimates the true cost." (1:11:55)

**`h(n) ≤ costo real de n al objetivo`, siempre.**

Manhattan cumple en una grilla con movimientos de 4 direcciones: cada paso cambia la distancia en exactamente 1, así que nunca podés llegar en menos pasos que la distancia Manhattan. No puede sobreestimar.

**Qué pasa si la rompés:** el ejercicio lo mide. Con `h' = 2·h` en `maze-b`:

```
A*                   costo=41  expandidos=81   ← admisible, óptimo
A* w=2.0  costo=47  expandidos=48  SUBÓPTIMO (+6)
```

A\* con heurística inflada explora **40% menos** y devuelve un camino **6 pasos peor**. Más rápido, pero ya no es A\*: es una búsqueda voraz disfrazada. Si necesitás optimalidad, la admisibilidad no es opcional.

---

## 1.5 Minimax y alpha-beta: cuando el otro también decide (1:16:36)

Hasta acá, un solo agente optimizando. En un juego, el oponente **maximiza su propio beneficio**, que es tu pérdida.

> "And the algorithm we're going to take a look at is an algorithm called Minimax, which works very well for these deterministic games where there are two players." (1:16:36)

Minimax recorre el árbol asumiendo que el rival juega perfecto: en tus turnos elegís el máximo, en los suyos el mínimo.

**Alpha-beta pruning** (1:45:51) poda las ramas que ya no pueden cambiar la decisión:

> "And it's for that reason this approach, this optimization to minimax, is called alpha, beta pruning." (1:45:51)

Alpha = lo mejor que ya tenés garantizado. Beta = lo peor que el rival te puede forzar. Si `beta ≤ alpha`, esa rama está muerta: no importa lo que pase adentro, no te va a cambiar la jugada.

**Depth-limited + evaluación** (1:48:51): cuando el árbol no entra en ninguna computadora (ajedrez), cortás a cierta profundidad y estimás con una función de evaluación.

> "So in order to do that, we need to add one additional feature to depth-limited Minimax called an evaluation function, which is just some function that is going to estimate the expected utility of a game from a given state." (1:48:51)

---

## 1.6 El ejercicio, y qué mide

El outline pide: A\* sobre un laberinto con Manhattan, correrlo sobre dos mapas, comparar contra BFS. La prueba es que **A\* expanda menos en ambos y devuelva el mismo costo**.

`search/astar.py` hace exactamente eso, más dos cosas que el outline no pedía y que son las que enseñan:

1. Suma **greedy** a la comparación, para ver el fallo de optimalidad sin que nadie te lo cuente.
2. Corre A\* con **heurística inflada (`w=1.5`, `w=2.0`)**, para romper la admisibilidad a propósito y ver qué se pierde.

```
$ python3 search/astar.py

== maze-a (29x31) ==
  BFS                  costo=53  expandidos=362
  greedy best-first    costo=53  expandidos=54
  A*                   costo=53  expandidos=117
  A* w=1.5  costo=53  expandidos=54   (0.46× los de A* admisible) óptimo
  A* w=2.0  costo=53  expandidos=54   (0.46× los de A* admisible) óptimo
  OK maze-a: A* costó 53 (= BFS) y expandió 117 vs 362 (×3.1 menos)

== maze-b (29x21) ==
  BFS                  costo=41  expandidos=143
  greedy best-first    costo=47  expandidos=48
  A*                   costo=41  expandidos=81
  nota maze-b: greedy costó 47 vs óptimo 41 (subóptimo, como predice la clase)
  nota maze-b: A* con w=2.0 devolvió 47 en vez del óptimo 41 - la heurística inadmisible rompe la garantía
  A* w=1.5  costo=41  expandidos=87   (1.07× los de A* admisible) óptimo
  A* w=2.0  costo=47  expandidos=48   (0.59× los de A* admisible) SUBÓPTIMO (+6)
  OK maze-b: A* costó 41 (= BFS) y expandió 81 vs 143 (×1.8 menos)

RESULTADO: PASA
```

**Lo que muestran los números, y que no se ve leyendo el método:**

- A\* expande **3.1× menos** que BFS en `maze-a` y **1.8× menos** en `maze-b`, con el mismo costo. La optimidad sobrevive al ahorro.
- En `maze-a` el camino es tan directo que el inflado no rompe nada: la heurística ya era exacta en toda la ruta recta. La lección: **la admisibilidad sólo importa donde hay un desvío obligatorio**. Un mapa malo para el ejercicio te deja creyendo que A\* admisible y A\* inflado son lo mismo.
- En `maze-b`, `w=1.5` todavía es óptimo y **cuesta 7% más nodos** que el admisible. Inflar un poco no ahorra nada: el punto de inflexión está más arriba.
- Greedy en `maze-a` gana igual que A\*, y en `maze-b` pierde. La misma heurística, dos mapas, dos resultados. Un test en un solo mapa no prueba nada.

---

## 1.7 Qué de esto sirve fuera del curso

Tres cosas que trasladan al trabajo de todos los días, sin metáfora:

1. **La frontier es la memoria de trabajo del agente.** Cuando un agente elige qué herramienta usar, "costo ya pagado + estimación del resto" es A\*, y "lo que parece más cerca" es greedy. El segundo es más rápido y a veces está mal.
2. **Contar los estados expandidos.** El outline lo deja como candidato: un bucle de agente que no sabe cuántos pasos gastó no puede decir si mejoró. Es la diferencia entre optimizar y sentir que se optimizó.
3. **La admisibilidad como contrato explícito.** Un gate que promete "falla cuando hay un error" tiene el mismo problema que una heurística: si el chequeo sobreestima el alcance de lo que ve (sostiene que es seguro sin haber mirado), la garantía se cae sin que nadie lo note.

---

## Preguntas para estudiar juntos

1. **La estructura de la frontier.** Si cambiás la cola de prioridad de A\* por una pila, ¿qué algoritmo tenés? ¿Y si la cambiás por una fila? Justificá sin mirar la tabla.
2. **Admisibilidad vs consistencia.** El curso habla de heurísticas admisibles. Una heurística **consistente** cumple `h(n) ≤ costo(n,a,n') + h(n')`. ¿Qué garantía extra da, y por qué A\* con una heurística consistente nunca necesita reabrir un nodo?
3. **¿Por qué BFS es óptimo y DFS no?** En el fondo, ¿qué propiedad del orden de exploración sostiene la optimalidad de BFS?
4. **El mapa de prueba.** `maze-a` hizo que A\* inflado fuera óptimo. ¿Qué propiedad tiene `maze-a` que lo hace inútil como test de admisibilidad? ¿Cómo construirías un mapa adversarial?
5. **Greedy y A\* en el mismo mapa.** Greedy hizo 48 expansiones y costo 47; A\* hizo 81 y costo 41. ¿Cuándo elegirías greedy a sabiendas de que no es óptimo?
6. **Alpha-beta.** Alpha y beta son cotas. ¿Qué pasa con la poda si el árbol está mal ordenado (peores movimientos primero)? ¿En el mejor caso, cuántas ramas de un árbol de profundidad `d` y factor `b` se exploran?
7. **Costo uniforme.** Si los pasos tienen costos distintos (barro cuesta 3, camino cuesta 1), ¿qué cambia en BFS? ¿Y en la heurística Manhattan?
8. **Del curso a tu workspace.** Un agente que decide qué herramienta usar: ¿dónde está su `g` y dónde su `h`? ¿Qué sería una heurística admisible en ese problema?

---

## Referencias

- Transcript: `studies/cs50-ai-python/transcripcion.md` (Módulo 1 = cues 42–438)
- Outline: `studies/cs50-ai-python/outline.md` (Módulo 1)
- Código: `studies/cs50-ai-python/search/astar.py` + `search/maps/`
- Proyectos del curso: https://cs50.harvard.edu/ai/2020/

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
