# Práctica del Módulo 1 — Search

> Las preguntas del Módulo 1, **corridas**, no respondidas de memoria.
> Cada práctica es un script autocontenido que afirma una propiedad y falla si la propiedad no se cumple.
> Gate del módulo: `python3 run_all.py` → 7 de 7.

---

## Por qué cada pregunta es un script

Una respuesta leída se olvida; una respuesta que **falla cuando se equivoca** es una respuesta aprendida. Cada archivo de acá se escribió con la misma forma: plantea una afirmación, la ejecuta sobre datos reales y devuelve `0` sólo si el resultado la sostiene.

| # | Práctica | Afirmación que se verifica | Cómo se rompe |
|---|---|---|---|
| 1 | `p1_frontier.py` | La estructura de la frontier **es** el algoritmo | Pila en A\* → DFS; fila → BFS |
| 2 | `p2_consistencia.py` | Admisible ≠ consistente | Heurística con desnivel local |
| 3 | `p3_adversarial.py` | Un mapa adversarial se **genera por propiedad** | Dibujado a mano no rompe nada |
| 4 | `p4_costos.py` | BFS deja de ser óptimo con costos distintos | Terreno con peajes |
| 5 | `p5_agente.py` | La heurística no admisible cambia el **plan**, no la velocidad | Confundir `respuesta_rapida` con `respuesta` |
| 6 | `p6_minimax.py` | Alpha-beta poda sin cambiar el valor de la raíz | Orden adverso de hijos |
| 7 | `p7_reapertura.py` | Admisible sin consistente **obliga** a reabrir | Búsqueda por fuerza bruta del caso |

---

## 1. La frontier es el algoritmo

```
variante         ordena por                 es en realidad         costo  expandidos
A* con PILA      LIFO (costo y h nulas)     DFS                    41     42   <-- NO óptimo
A* con FILA      FIFO (costo y h nulas)     BFS                    41     143
A* solo con h    h decreciente              greedy best-first      47     48   <-- NO óptimo
A* real          g+h decreciente            A*                     41     81
```

**Respuesta a la pregunta 1:** pila → DFS, fila → BFS. No "A\* con otra estructura": la estructura *define* el orden de salida, y el orden de salida *es* el algoritmo. La heurística queda decorativa.

**Detalle que no se ve leyendo:** A\* con pila sacó 42 nodos y encontró costo 41 en este mapa. Esa coincidencia es veneno: si el mapa hubiera tenido un desvío, el mismo código daría un costo peor. La optimalidad de A\* no viene del código, viene del orden.

---

## 2. Admisibilidad ≠ consistencia

```
heurística                 admisible?   consistente?   costo   expandidos  reaperturas
manhattan                  sí           sí             41      81          0
cero (sin info)            sí           sí             41      143         0
manhattan*1.5              NO (97)      NO (286)       41      87          0
manhattan al cuadrado/20   NO (51)      NO (192)       47      48          0

heurística admisible con desnivel en (1, 1):
  admisible:   sí
  consistente: NO (2 violaciones)
```

Las dos cosas se miden distinto:

- **Admisible:** `h(n) ≤ costo real(n → t)`. Se verifica contra el mapa entero.
- **Consistente:** `h(n) ≤ costo(n, n') + h(n')`. Se verifica **arista por arista**.

La consistencia **implica** admisibilidad. Al revés no.

**Lo que falla la intuición:** la heurística con desnivel es admisible y **A\* sin reapertura igual encuentra el óptimo en `maze-b`**. No hay reapertura. Eso no la salva: significa que este mapa no expone el problema. Ver práctica 7.

---

## 3. El mapa adversarial se genera, no se dibuja

Dibujé tres mapas a mano intentando romper la heurística inflada. Los tres fallaron: salieron con el mismo costo para todos los algoritmos, porque "donde yo creía que había un desvío" no estaba en el camino óptimo.

La solución fue invertir la carga: en lugar de dibujar y verificar, **declarar la propiedad y buscar**.

```
adversarial(mapa) := existe w ≥ 1.5 tal que A*_w devuelve costo > BFS

#####################
#A  #   #    #  #   #
...
inicio=(1, 1)  objetivo=(19, 13)  óptimo BFS=30

BFS (óptimo)           30      -
greedy                 32      51
A* w=1.0               30      105
A* w=1.5               32      51
A* w=2.0               32      50
```

Encontrado en la **semilla 0** de 500. Lo importante no es el mapa: es que el criterio es la propiedad, y se puede correr de nuevo.

---

## 4. Costos distintos rompen BFS (y debilitan Manhattan)

```
Mapa con barro (~, costo 3)

algoritmo                      optimiza       costo real   expandidos
BFS (pasos, ignora costo)      pasos          57           -
UCS (costo uniforme, g)        costo          49           175
A* con Manhattan               costo          49           169
```

BFS devolvió **57 cuando el óptimo es 49**: 8 de más. BFS minimiza *pasos*, no *pesos*. Su optimalidad depende de que todos los pasos cuesten lo mismo.

**Y Manhattan:** sigue siendo admisible, porque cada paso cuesta **≥ 1** y Manhattan cuenta pasos: subestima o acierta, nunca sobreestima. Pero es débil — trata el barro como si costara 1. Ahorra casi nada frente a UCS (**×1.04**).

**La corrección real (para la 6):** con costos variables, lo que se cambia no es la cola sino la heurística: `h = costo mínimo del terreno × distancia Manhattan`. Eso sí es una cota útil, y sigue siendo admisible.

---

## 5. A\* fuera del laberinto: un agente eligiendo herramientas

```
h del agente                         costo   expandidos   plan
h=0 (no sabe nada)                   5       5     read -> grep(verificar) -> razonar
h real mínima (admisible)            5       5     read -> grep(verificar) -> razonar
h inflada: confunde rápido con listo 8       5     read -> razonar sin verificar -> verificar tarde
```

El grafo tiene una **trampa**: `razonar sin verificar` lleva a `respuesta_rapida`, que *parece* la meta pero no lo es.

La heurística inflada da `h(respuesta_rapida) = h(respuesta) = 0`, así que declara victoria ahí. Termina pagando 3 más y el total sale **8 contra 5**.

**La traducción al workspace:** `g` es lo ya gastado en el turno; `h` es la estimación de lo que falta. Un agente que "confía en su intuición" está usando una `h` inflada: llega antes a una respuesta, pero se saltea la verificación. Eso no es velocidad — es un plan distinto con menos control. Y es exactamente lo que `AGENTS.md` llama *"el auto-reporte de un subagente no es un hecho"*.

---

## 6. Alpha-beta: el orden cambia el trabajo, nunca el resultado

```
Árbol: profundidad 4, factor ~3, 81 hojas

variante                           valor raíz   nodos    hojas    podadas
minimax sin poda                   6            121      81       0
alpha-beta orden original          6            69       40       19
alpha-beta mejor primero           6            37       17       24
alpha-beta peor primero            6            108      68       13
```

**Las cuatro ramas dan 6.** Eso es la garantía: podar no cambia la respuesta.

El trabajo sí cambia: entre **17 y 68 hojas** para el mismo árbol, según el orden.

**Respuesta a la 5:** con orden adverso (peores movimientos primero) alpha-beta se degrada hacia el minimax completo: 68 de 81 hojas, casi nada podado. Con orden perfecto explora aproximadamente `b^(d/2)`, que en un árbol de profundidad 4 y factor 3 es `3^2 = 9` en lugar de 81.

**La traducción al pipeline A/B:** evaluar primero el caso más probable de fallar permite descartar el resto con pocas evaluaciones. Evaluar primero los casos triviales es el orden adverso: gasta todo y no descarta nada.

---

## 7. La reapertura: el caso donde la inconsistencia muerde

En `maze-b` con heurística inconsistente no hubo reapertura. Eso no prueba que no importe: prueba que la grilla con costo 1 esconde el problema. Para verlo hubo que **buscar el grafo por fuerza bruta** (misma técnica que p3).

```
Encontrado en la semilla 29
  s --1.5--> a    a --0.4--> b    b --2--> t
  s --2.5--> b    a --2--> t      c --2.5--> t
  s --2.5--> c    a --1.0--> c    b --1.5--> c

h: {s: 0, a: 1.5, b: 0, c: 1.5, t: 0}
distancia real a t: {s: 3.5, a: 2.0, b: 2.0, c: 2.5, t: 0.0}

  admisible:    sí
  consistente:  NO

variante                           costo    expandidos   reaperturas
A* con reapertura                  3.5      5            1
A* sin reapertura                  3.5      4            0
```

**Lo incómodo y lo honesto:** sin reapertura el costo sale **igual** en este grafo. El nodo reabierto no estaba en el camino ganador. Se reabre para corregir su `g`, pero el camino final pasa por otra rama.

Ese es el motivo por el que el bug es difícil de ver a ojo: el resultado sale bien y la única señal es el contador de reaperturas. Por eso A\* guarda `best_g` y compara — no porque siempre cambie el resultado, sino porque sin esa comparación el algoritmo deja de ser correcto *en general* y el caso que lo rompe no avisa.

Es la misma forma del error que `AGENTS.md` documenta: **una verificación que da verde sin haber verificado**.

---

## Resumen: qué queda después de correrlo

| La respuesta de manual | Lo que mostró el código |
|---|---|
| A\* con otra estructura sigue siendo A\* | Pila → DFS, fila → BFS. La estructura *es* el algoritmo |
| La admisibilidad sostiene la optimalidad | Tiene que ser **más fuerte** para evitar reapertura: consistencia |
| Un mapa sirve para testear el algoritmo | Sólo si es adversarial, y lo adversarial se verifica por propiedad |
| BFS siempre encuentra el camino óptimo | Sólo con costo uniforme. Con peajes pierde por 8 |
| Greedy es "A\* sin g" | Es un plan distinto, y el plan es lo que cambia, no la velocidad |
| La poda depende del tamaño del árbol | Depende del **orden**. Mismo árbol: 17 o 68 hojas |
| Un resultado correcto implica un algoritmo correcto | El caso de reapertura da el costo bien y el algoritmo está mal |

---

## Cómo volver a correrlo

```bash
cd studies/cs50-ai-python/search/practica
python3 run_all.py              # las 7, con el veredicto
python3 p3_adversarial.py       # el mapa adversarial, generado de nuevo
python3 p7_reapertura.py        # el caso de reapertura, buscado de nuevo
```

Cada script imprime su propio resultado. `run_all.py` sale con código 0 solo si las 7 pasan.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
