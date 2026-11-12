# Módulo 4 — Optimization: clase

> Clase del **Módulo 4** de *Harvard CS50's AI with Python* (Brian Yu).
> Fuentes: `transcripcion.md` (citas con t= verificadas), mis conocimientos, y el código en `optimization/practica/`.
> scipy no está instalado: la programación lineal se resuelve recorriendo vértices, que es lo que hace el solver.

---

## 4.1 Un cambio de pregunta

Hasta acá: "¿existe un camino?" y "¿cuál es el más corto?". Esos son problemas de **búsqueda**: importa el camino.

> "what we'll take a look at today is a category of types of problems and algorithms to solve them" (5:35:17)

Y los problemas de hoy son otros:

> "in order to try to find a global maximum or a global minimum somehow." (5:41:24)

**No importa el camino. Importa qué tan buena es la configuración final.** Esa es toda la diferencia, y de ahí sale todo el módulo:

| Pregunta | Familia | Devuelve |
|---|---|---|
| ¿Cómo llego de A a B? | Búsqueda (Módulo 1) | El camino |
| ¿Cuál es la mejor configuración? | Búsqueda local | Un punto y un valor |
| ¿Cuánto maximo puedo producir con estas restricciones? | Programación lineal | Un óptimo con variables continuas |
| ¿Existe una asignación que cumpla todo? | CSP | Una asignación válida |

---

## 4.2 Hill climbing: subir hasta trabarse

La idea mínima. Una **función objetivo** mide qué tan buena es cada configuración:

> "some function that measures for any given state how good is that state" (5:39:27)

Y el algoritmo es exactamente lo que suena: mirar los vecinos, moverse al que mejora, parar cuando ninguno mejora.

### El paisaje, y sus trampas

> "these various different types of plateaus" (5:50:57)

Un espacio de estados no es una loma. Tiene:

- **Máximos locales:** un pico que no es el más alto.
- **Mesetas:** una zona plana donde ningún vecino mejora — y no hay dirección.
- **Crestas:** una subida donde el vecino inmediato empeora pero el camino sigue subiendo.

Hill climbing no distingue ninguno del máximo global. **Desde adentro son iguales.**

### Medido

`p1_hill_climbing.py` corre hill climbing sobre un paisaje con tres picos desde 200 puntos de partida:

```
Máximos locales encontrados:
  x=   4.70  valor=1.4042  GLOBAL
  x=  -0.95  valor=0.8162  local
  x=  -8.00  valor=0.5501  local

termina en el global: 35/200 (18%)
ATASCADO en un máximo local: 165/200 (82%)
```

**82% de las corridas se traba.** Y no puede saberlo: desde adentro, un máximo local es indistinguible del global — no hay vecino que mejore en ninguno de los dos, y el criterio de parada es el mismo.

### Random restart

> "we can reduce that risk by repeating the process multiple times. So one variant of hill climbing is random restart" (5:53:43)

```
 1 reinicios: 28%
 3 reinicios: 61%
 5 reinicios: 79%
10 reinicios: 94%
20 reinicios: 100%
```

No necesitás entender el paisaje: repetir desde puntos al azar sube la probabilidad. **Pero tampoco garantiza llegar al global** — reiniciar desde un punto al azar puede caer siempre en el mismo pozo. Sólo cambia la probabilidad.

---

## 4.3 Simulated annealing: aceptar lo peor a propósito

> "the most popular technique for trying to approach the problem from that angle is a technique known as simulated annealing" (6:03:50)

> "we're going to simulate that process of some high temperature system where things are moving around randomly quite frequently, but over time decreasing that temperature" (6:04:23)

La regla:

```
P(aceptar un empeoramiento de Δ) = exp(-Δ / T)
```

| Δ | T=1.0 | T=0.5 | T=0.1 | T=0.01 |
|---|---|---|---|---|
| 0.01 | 0.990 | 0.980 | 0.905 | 0.368 |
| 0.10 | 0.905 | 0.819 | 0.368 | ~0 |
| 0.50 | 0.607 | 0.368 | 0.007 | ~0 |
| 2.00 | 0.135 | 0.018 | ~0 | ~0 |

**Con T alta acepta casi todo; con T baja, casi nada.** El "casi nada" del final es lo que garantiza que termine en un pico en vez de vagar.

### Medido, contra hill climbing

```
método                                 llega al global    valor medio
simulated annealing (1 corrida)        44%                0.9940
hill climbing (1 corrida)              26%                0.9777
```

Y el trazado de una corrida que sí llega:

```
iteración    T            valor actual
0            1.000000     0.8158
229          0.317311     0.6286     ← BAJÓ: aceptó empeorar
459          0.100183     1.1489
919          0.009986     1.3994
1839         0.000100     1.4042     ← global
```

**El valor baja al principio.** Ese es el trabajo que hill climbing no hace: salir del pozo antes de que se vuelva trampa.

### La honestidad del método

Simulated annealing **no garantiza** el global. Con `T₀` baja se comporta como hill climbing; con `T₀` alta y enfriamiento lento tarda más. La garantía teórica (enfriamiento logarítmico) **asume tiempo infinito**. En la práctica se elige el presupuesto y se reza.

---

## 4.4 Programación lineal: el óptimo está en un vértice

> "known as these categories of linear programming types of problems" (6:14:55)

El curso resuelve una fábrica con `scipy.optimize.linprog` (6:21:47). Acá no hay scipy, así que se hace lo que hace el solver: **recorrer los vértices**.

```
Maximizar  40·X + 30·Y
sujeto a    X +  Y <= 12
            2X + Y <= 16
            X, Y  >= 0

Vértices factibles:
  ( 0,  0)  Z=  0
  ( 0, 12)  Z=360
  ( 4,  8)  Z=400   ← óptimo
  ( 8,  0)  Z=320
```

Y verificado con un barrido de 10.000 puntos interiores: el mejor es el mismo (4, 8).

### Por qué es un teorema, no una coincidencia

El objetivo es **lineal** y el dominio es un **polígono convexo**. Una función lineal sobre un polígono no tiene máximo interior. Por eso `linprog` puede recorrer vértices y terminar: **no le falta buscar, no hay nada que buscar adentro.**

### Dónde se rompe

- **Restricción no lineal** (`X·Y <= 12`): el óptimo puede estar en el interior, y recorrer vértices devuelve una respuesta falsa con la misma seguridad.
- **Programación entera** (`X`, `Y` enteros): el óptimo puede no ser un vértice del poliedro relajado.

La formulación lineal es una **elección**, no una propiedad del problema.

---

## 4.5 CSP: variables, dominios y restricciones

> "a constraint satisfaction problem is just some set of variables, x1 all the way through xn, some set of domains for each of" (6:28:30)

Un CSP tiene tres cosas:

1. **Variables** — las casillas vacías de un Sudoku (6:29:19).
2. **Dominios** — los valores que cada una puede tomar.
3. **Restricciones** — qué combinaciones son válidas.

### Tipos de restricción

> "unary constraint is a constraint that just involves a single variable" (6:32:16)
> "in contrast to something like a binary constraint, which is a constraint that involves two variables" (6:32:47)

Y por dureza:

- **Duras:** hay que cumplirlas o no hay solución. Un Sudoku con dos 5 en la misma fila no es un Sudoku.
- **Suaves:** preferencias. Se satisfacen lo más posible; un horario puede cumplir todas las duras y sólo algunas suaves.

### Consistencia: podar antes de equivocarse

> "we'll just go ahead and remove Monday from a's domain" (6:35:07)

**Node consistency:** sacar del dominio los valores que violan una restricción unaria.

> "arc consistency refers to when all of the values in a variable's domain satisfy the variable's binary constraints" (6:37:17)

**Arc consistency:** para cada valor de `A`, tiene que existir al menos un valor compatible en `B`.

> "we need to add back some arcs to the queue in order to continue to enforce arc consistency" (6:47:02)

**AC-3** propaga esto hasta que no cambia nada.

### Backtracking, y su mejora

> "something known as backtracking search. And the big idea of backtracking search is we'll go ahead and make assignments" (6:51:04)

Y la mejora:

> "by maintaining arc consistency in the backtracking search process" (7:07:26)

### Medido — y el resultado no es el que el outline esperaba

`p4_csp.py` corre los dos sobre dos problemas:

```
=== Horarios de examen (4 estudiantes, 3 días) ===
  backtracking puro              5 nodos
  backtracking + forward         5 nodos    3 podas

=== Coloreado de grafo (9 nodos, 3 colores) ===
  backtracking puro              79 nodos
  backtracking + forward         21 nodos   48 podas   3.76x
```

**En el horario chico el forward checking no gana nada.** La primera rama que prueba ya es solución: no hay ramas muertas que podar.

**En el coloreado gana 3.76×**, porque ahí sí hay que retroceder.

La lección no es "forward checking es mejor". Es más precisa:

> **Una poda no mejora un árbol que no tiene ramas muertas.**

Y la consecuencia operativa: agregar inferencia a un solver que no se equivoca es trabajo desperdiciado. Agregarla donde sí hay retroceso es la diferencia entre 79 y 21 nodos.

---

## 4.6 Lo que este módulo le hace al workspace

`p5_camino_vs_resultado.py` corre A\* y hill climbing sobre el mismo mapa y mide **qué se puede preguntar** con cada uno:

| Pregunta | A\* | Hill climbing |
|---|---|---|
| ¿Cuál es el camino más corto? | sí | no |
| ¿Los pasos son adyacentes y válidos? | por construcción | por el objetivo |
| ¿Mejorar una ruta existente? | no | sí |
| Garantía de óptimo | con `h` admisible | ninguna |

Y el hallazgo incómodo de la corrida: **la ruta de hill climbing no es válida** (atraviesa paredes), y el puntaje la dio por buena. El optimizador no sabe qué es una pared: **sólo maximiza lo que le pongas en el objetivo.**

### Las dos traducciones al trabajo con agentes

1. **"Escribí el plan" es búsqueda. "Mejorá este plan" es búsqueda local.** Elegir uno y esperar del otro lo que no puede dar es el error más común al montar un pipeline.
2. **Un agente que mejora un draft con la última sugerencia es hill climbing.** No escapa del óptimo local, y por eso necesita un criterio externo —no más vueltas del mismo modelo—. Es exactamente lo que el pipeline A/B aporta.

---

## Práctica del módulo

Cinco scripts en `optimization/practica/`. Gate: `python3 run_all.py` → **5 de 5**.

| # | Práctica | Afirmación |
|---|---|---|
| 1 | `p1_hill_climbing.py` | Hill climbing queda atrapado 82% de las veces |
| 2 | `p2_annealing.py` | Aceptar lo peor a propósito llega más al global |
| 3 | `p3_lineal.py` | El óptimo de un programa lineal está en un vértice |
| 4 | `p4_csp.py` | Forward checking gana **solo** cuando hay ramas muertas |
| 5 | `p5_camino_vs_resultado.py` | Camino y resultado no son la misma pregunta |

Ver `practica-modulo-04.md`.

---

## Preguntas para estudiar

1. Hill climbing no sabe que está atrapado. ¿Qué información necesitaría para saberlo, y por qué el algoritmo no la tiene?
2. Simulated annealing acepta empeorar. ¿Por qué `exp(-Δ/T)` y no, por ejemplo, `1/(1+Δ)`? ¿Qué tiene esa forma que la otra no?
3. Si el enfriamiento es demasiado rápido, annealing es hill climbing. Si es demasiado lento, no termina. ¿Cómo se elige en la práctica, sin saber el paisaje?
4. Un programa lineal con objetivo lineal y dominio convexo tiene el óptimo en un vértice. ¿Qué dos suposiciones rompen eso, y cómo se nota en la respuesta?
5. Arc consistency mira pares. ¿Por qué eso **no** garantiza que el CSP tenga solución? ¿Qué hace falta además?
6. En `p4`, el horario chico no ganó nada con forward checking. ¿Cómo sabrías, **antes** de programarlo, si un CSP va a tener ramas muertas?
7. **El `p5` con la ruta inválida:** el optimizador devolvió puntaje 737 atravesando paredes. ¿Qué le faltaba al objetivo? ¿Qué tiene eso que ver con medir un agente con métricas fáciles en vez de las correctas?
8. Si un pipeline "mejora" un texto con el mismo modelo en N iteraciones, ¿qué familia de algoritmo es? ¿Qué necesitaría para no quedarse en el óptimo local?

---

## Referencias

- Transcript: `studies/cs50-ai-python/transcripcion.md` (Módulo 4 = cues 1234–1616)
- Outline: `studies/cs50-ai-python/outline.md` (Módulo 4)
- Código: `studies/cs50-ai-python/optimization/practica/`
- Proyectos: https://cs50.harvard.edu/ai/2020/

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
