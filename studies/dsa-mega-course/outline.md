# Clase: Data Structures and Algorithms Mega Course — Master Technical Interviews in 49 Hours

- **Fuente:** https://www.youtube.com/watch?v=xwI5OBEnsZU
- **Canal:** freeCodeCamp.org
- **Expositor:** Parth (Destination FAANG) — hoy cloud solutions architect en Microsoft, ex Microsoft/RBC/Nokia
- **Publicado:** 2025-10-21
- **Duración:** 48:48:19 (175.819 s)
- **Idioma:** inglés (subtítulos automáticos `en` ASR)
- **Lenguaje del curso:** Java
- **Transcripción:** `transcripcion.md` (9.850 bloques, 561.512 palabras)
- **Recursos del video:** [hoja de preguntas más pedidas](https://docs.google.com/spreadsheets/d/1hzP8j7matoUiJ15N-RhsL5Dmig8_E3aP/edit#gid=1377915986) · [repo con las soluciones en Java](https://github.com/DestinationFAANG/Destination-FAANG-Java-Solution)

> **Nota de escala.** Son 49 horas: la clase no se consume de una sentada, se estudia por módulo. Este outline es un mapa para navegar el video, no un resumen que lo reemplace. Cada módulo indica dónde está en el video, qué problemas resuelve y qué tenés que entregar al cerrarlo.

## Resultado esperado

Al terminar el recorrido, verificable por capacidades:

1. **Justificar la eficiencia de un algoritmo** con notación Big O sobre bloques de código concretos (tiempo y espacio), y elegir qué estructura usar según la operación dominante.
2. **Implementar en Java** las estructuras base — array, linked list, stack, queue, priority queue, árbol — sabiendo el costo de cada operación.
3. **Reconocer los ~14 patrones de entrevista** (sliding window, two pointers, binary search sobre espacio de respuesta, DFS/BFS, DP top-down/bottom-up, greedy, backtracking, intervals, bit manipulation) y decir cuál aplica a un problema nuevo.
4. **Resolver ~150-200 problemas de LeetCode** con la lógica explicada antes de escribir código, no por memorización.
5. **Defender la complejidad de tu solución** en una entrevista: qué es O(n), qué es O(n log n), cuándo n² es aceptable y cuándo es el techo.

## Mapa temporal

Oficial (29 capítulos de la descripción). Duración = hasta el capítulo siguiente.

| # | Tiempo | Bloque | Dur. |
|---|---|---|---|
| 1 | 0:00:00 | Introducción (qué cubre el curso, quién es el expositor) | 3 min |
| 2 | 0:03:14 | Entrevistas técnicas 101 (qué es DSA, por qué importa) | 4 min |
| 3 | 0:07:02 | Cómo juzgar un algoritmo (exactitud, tiempo, espacio) | 1 min |
| 4 | 0:08:02 | Qué es la complejidad temporal | 11 min |
| 5 | 0:18:42 | Qué es Big O (la O de "order") | 2 min |
| 6 | 0:20:20 | Big O para bloques de código | 13 min |
| 7 | 0:33:08 | Ejemplo de complejidad espacial | 2 min |
| 8 | 0:35:04 | Cómo volverse bueno resolviendo problemas de DSA | 2 min |
| 9 | 0:37:34 | Tipos de estructuras de datos | 11 min |
| 10 | 0:48:48 | Repaso rápido y plan de las 20 temas | 2 min |
| 11 | 0:50:21 | **Arrays** | 159 min |
| 12 | 3:29:02 | **Sliding Window** | 101 min |
| 13 | 5:09:48 | **Two Pointers** | 111 min |
| 14 | 7:00:25 | **Strings** | 89 min |
| 15 | 8:29:27 | **Sorting & Searching** | 179 min |
| 16 | 11:28:48 | **Linked List** | 160 min |
| 17 | 14:08:48 | **Stack** (arranca a las 14:08:47) | 155 min |
| 18 | 16:43:55 | **Queue** (teoría desde 16:49) | 74 min |
| 19 | 17:58:08 | **Priority Queue** (heap) | 178 min |
| 20 | 20:55:54 | **Trees** (teoría desde 20:57) | 264 min |
| 21 | 25:20:01 | **Graph** | 414 min |
| 22 | 32:14:13 | **Dynamic Programming** | 299 min |
| 23 | 37:13:04 | **Greedy** | 114 min |
| 24 | 39:06:36 | **Interval** | 86 min |
| 25 | 40:32:39 | **Backtracking** | 133 min |
| 26 | 42:45:51 | **Math & Geometry** | 57 min |
| 27 | 43:42:30 | **Matrix** | 133 min |
| 28 | 45:55:06 | **Design** | 87 min |
| 29 | 47:22:33 | **Bit Manipulation** | 86 min |
| 30 | 48:48:17 | Mensaje final | 2 min |

**Orden de estudio propuesto** (no es el orden del video; el video ya está ordenado de menor a mayor dificultad y así conviene seguirlo):

| Tramo | Módulos | Horas | Qué pasa |
|---|---|---|---|
| A — Fundamentos | 1-10 + Arrays | ~2,8 h | Big O y la estructura más usada |
| B — Patrones de ventana | Sliding Window + Two Pointers + Strings | ~5 h | Todo lo que se resuelve con dos índices |
| C — Buscar y ordenar | Sorting & Searching + Linked List | ~5,7 h | Binary search como patrón, no como algoritmo |
| D — Lineales LIFO/FIFO | Stack + Queue + Priority Queue | ~6,8 h | Monotonic stack y heap son el 80% de las preguntas medianas |
| E — Jerarquía y red | Trees + Graphs | ~11,3 h | El tramo más largo: es donde se juega la entrevista grande |
| F — Optimización | Dynamic Programming + Greedy | ~6,9 h | DP es el filtro de seniority |
| G — Cierre | Interval + Backtracking + Math + Matrix + Design + Bit | ~10,5 h | Menor prioridad por pregunta, pero aparecen seguido |

## Módulos

### Módulo 1 — Big O y cómo juzgar un algoritmo (0:00:00 – 0:50:21)

> **Trabajado en:** [`modulo-01-big-o.md`](modulo-01-big-o.md) (2026-11-12) — lección completa con ejercicios y respuestas.

**Objetivo:** poder mirar un bloque de código y decir su complejidad de tiempo y espacio sin correrlo.

**Contenidos:**

- Las tres preguntas del expositor para juzgar un algoritmo: «there are three things that we are looking for» `(0:07:03)` — exactitud, complejidad temporal, complejidad espacial.
- **Complejidad temporal como crecimiento, no como segundos:** «Time complexity is nothing but how much» `(0:07:21)`. La pregunta real es *cómo escala*, no *cuánto tarda*.
- Cinco complejidades con un ejemplo físico cada una:
  - **O(log n)** — buscar una carta en un mazo ordenado partiendo por el medio: «we are essentially eliminating 50% of all the inputs in one go» `(0:10:33)`.
  - **O(1)** — la bandeja de garbanzos numerada: la posición 5 siempre tiene 5 garbanzos, sin importar el tamaño `(0:11:16)`.
  - **O(n)** — buscar un valor en un array sin ordenar: «we might have to iterate over the entire array before we find the appropriate value» `(0:22:16)`.
  - **O(n²), O(n³)** — emparejar dos o tres mazos: «it's loop within a loop in order to find the established goal» `(0:13:28)`.
  - **O(2ⁿ)** — tirar monedas: cada moneda duplica las combinaciones `(0:14:18)`.
  - **O(n!)** — sentarse tres personas en tres asientos: 3×2×1 `(0:16:04)`.
- **Por qué se llama Big O:** «we are trying to calculate the upper bound of growth rate for the given algorithm» `(0:18:57)`. La O es de *order*.
- Big O de bloques reales `(0:20:20 – 0:33:08)`: acceso a primer elemento → O(1) «we can call this as big O of one or constant time complexity for this code block» `(0:20:44)`; búsqueda binaria → O(log n); búsqueda lineal → O(n); merge sort → «this code block is an example of go of n log n work» `(0:24:25)`; pares anidados → O(n²); Fibonacci recursivo → O(2ⁿ) `(0:26:05)`; permutaciones → O(n!).
- **Tabla de perspectiva** `(0:30:03)`: la misma entrada (10 / 100 / 1.000) en cada complejidad, con los números que el expositor proyecta. Es la tabla que hay que saberse: 2ⁿ para n=10 ya son 1.024 pasos, y para n=1.000 es un número de 301 dígitos.
- **Complejidad espacial con el ejemplo de los garbanzos** `(0:32:50)`: mover garbanzos negros y blancos entre dos frascos. Con un tercer frasco (espacio extra O(n)) se hace en una pasada; sin él, en O(n²).
- **Método para encarar un problema nuevo** `(0:35:04)`: entenderlo en los términos más simples, buscar patrones que se repiten, y «try to solve it using the most simplest terms or even the brute force approach even if it is not optimized for speed or anything else» `(0:35:42)`.
- **Clasificación de estructuras** `(0:37:34)`: lineales (array, linked list, stack, queue), no lineales / jerárquicas (tree, graph) y hash-based (hashmap, hashset). «A linear data structure is a data structure where basically all the elements are typically sequential» `(0:37:43)`.
- Plan de las 20 temas `(0:48:48)`: para cada tema, qué es, operaciones y patrones comunes, y los problemas más pedidos. «we are going to go with the 20 topics that I discussed earlier» `(0:49:03)`.

**Ejercicio:**
1. Elegí cinco problemas que ya hayas resuelto y escribí, sin mirar solución, su complejidad de tiempo y espacio con una línea de justificación cada uno.
2. Agarrá la tabla de perspectiva `(0:30:03)` y verificá a mano tres de sus celdas (por ejemplo O(n log n) para n=1.000 y 2ⁿ para n=10).
3. Describí en tres frases qué operación domina en un hashmap y por qué eso lo vuelve O(1) promedio.

---

### Módulo 2 — Arrays (0:50:21 – 3:29:02, 159 min)

**Objetivo:** dominar la estructura base y sus 9 problemas canónicos; entender por qué el acceso es O(1) y por qué insertar en el medio es O(n).

**Contenidos:**

- **Qué es un array:** «Array is nothing but a continuous block of memory that is currently stored inside your computer» `(0:50:36)`. Bloque contiguo + tamaño fijo + índice ⇒ acceso O(1), y el cálculo de dirección `(0:51:50)`.
- **Complejidad por operación** `(0:52:12)`: acceso O(1); inserción/búsqueda en el peor caso O(n) por el desplazamiento `(0:52:51)`; recorrido O(n); búsqueda lineal O(n) y binaria O(log n) si está ordenado `(0:54:06)`.
- **Ventajas y límites:** acceso aleatorio, *cache friendly*, base de otras estructuras; límites: tamaño fijo, inserción/borrado costosos `(0:55:05)`.
- **Cuándo pensar en array** `(0:57:08)`: implementar otras estructuras, memoización/tabulación, marcar visitados en grafos, y los patrones clásicos «popular coding patterns» `(0:57:47)`.
- Arrays multidimensionales `(0:58:18)` — para entrevistas alcanza con 2D.
- **Los problemas (en orden del video):**

| Tiempo | Problema | Patrón | Complejidad que se busca |
|---|---|---|---|
| 1:00:17 | Two Sum | hashmap complemento | O(n) tiempo, O(n) espacio |
| 1:10:07 | Contains Duplicate | hashset | O(n) |
| 1:17:27 | Contains Duplicate II | sliding window + set | O(n) |
| 1:30:19 | Valid Anagram | conteo de caracteres | O(n) |
| 1:39:23 | Group Anagrams | hashmap con clave canónica | O(n·k log k) |
| 1:52:20 | Product of Array Except Self ⭐ | prefix × suffix | O(n) sin división |
| 2:09:02 | Top K Frequent Elements | hashmap + heap / bucket sort | O(n log k) o O(n) |
| 2:19:53 | Roman to Integer | tabla de valores | O(n) |
| 2:30:30 | Verifying Alien Dictionary (premium) | comparación adyacente | O(n·k) |
| 3:12:44 | First Missing Positive | marcar por índice | O(n) O(1) espacio |

- **Idea fuerza:** Product of Array Except Self es el ejemplo de cómo un prefijo y un sufijo reemplazan a la división — el patrón reaparece en DP, matrices y monotonic stack.

**Ejercicio:** resolvé en Java, con LeetCode abierto, Two Sum, Contains Duplicate, Valid Anagram y Product of Array Except Self. Entregá: código que pase el juez + una línea de complejidad justificada por cada uno + qué patrón de la tabla aplicaste.

---

### Módulo 3 — Sliding Window (3:29:02 – 5:09:48, 101 min)

**Objetivo:** reconocer cuándo una ventana que se mueve reemplaza a un doble loop, y distinguir ventana fija de ventana dinámica.

**Contenidos:**

- **Cuándo aplica:** cuando se busca «a subset in the current array that we are going to slide across the array to fulfill some conditions» `(3:29:14)` — el dato está en un tramo, no en una posición.
- **Ventana fija vs. dinámica:** en la dinámica, la condición de parada no es un índice sino una restricción sobre el contenido (sin repetidos, a lo sumo k cambios).
- **Los problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 3:32:17 | Best Time to Buy and Sell Stock | mínimo acumulado |
| 3:41:43 | Permutation in String | ventana fija + conteo |
| 3:54:51 | Longest Repeating Character Replacement | ventana dinámica con contador del máximo |
| 4:15:49 | Longest Substring Without Repeating | ventana + set de posiciones |
| 4:26:57 | Sliding Window Maximum ⭐ | deque monotónica |
| 4:46:52 | Minimum Window Substring | ventana dinámica + `required`/`formed` |

- **Idea fuerza:** Sliding Window Maximum es la prueba de que la ventana por sí sola no alcanza: hay que acoplarla a una deque monotónica para que el máximo del tramo sea O(1) amortizado `(4:34:05)`.
- **Idea fuerza:** en Minimum Window Substring la variable `required` (caracteres únicos que hay que cubrir) es la que convierte un O(n²) en O(n) `(5:05:00)`.

**Ejercicio:** implementá Sliding Window Maximum con la deque monotónica en Java, y explicá en tres líneas por qué el total es O(n) aunque haya un `while` interno.

---

### Módulo 4 — Two Pointers (5:09:48 – 7:00:25, 111 min)

**Objetivo:** usar dos índices en lugar de dos loops, y saber cuándo se mueven juntos y cuándo desde extremos.

**Contenidos:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 5:11:14 | Valid Palindrome | extremos hacia adentro |
| 5:20:31 | Two Sum II (array ordenado) | extremos hacia adentro |
| 5:32:59 | 3Sum ⭐ | ordenar + fijar uno + two pointers |
| 5:53:07 | Container With Most Water | extremos + descartar el menor |
| 6:07:59 | Trapping Rain Water ⭐ | prefix max de izquierda y derecha |
| 6:42:31 | Next Permutation | sufijo decreciente |

- **Idea fuerza:** 3Sum obliga a ordenar antes de mover punteros, y el costo de ordenar (n log n) es menor que el O(n³) del triple loop.
- **Idea fuerza:** en Container With Most Water el argumento por el que se descarta el menor (no puede formar parte de una solución mejor) es el tipo de justificación que un entrevistador quiere escuchar, más que el código.

**Ejercicio:** 3Sum en Java sin duplicados, con un comentario por cada puntero explicando por qué se mueve.

---

### Módulo 5 — Strings (7:00:25 – 8:29:27, 89 min)

**Objetivo:** manejar strings como arrays de caracteres con sus costos de concatenación y subcadena; aplicar hashing y palíndromos.

**Contenidos:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 7:06:53 | Concatenation / substring (teoría + problemas) | operaciones base |
| 7:15:23 | (problema de strings de la sección) | hashing |
| 7:24:03 | Encode and Decode Strings (premium) | delimitador con longitud |
| 7:32:22 | Palindromic Substrings | expansión desde el centro |
| 7:45:58 | Longest Palindromic Substring | expansión desde el centro |
| 8:02:51 | Text Justification | simulación con codicia |
| 8:15:38 | Valid Palindrome II (con un borrado) | dos punteros + reintento |

- **Idea fuerza:** Encode/Decode con longitud explícita (no un separador cualquiera) es el ejemplo de serialización que sobrevive a un contenido arbitrario.
- **Idea fuerza:** los problemas de palíndromo se resuelven expandiendo desde el centro: O(n²) para todas las subcadenas, O(n) por palíndromo individual.

**Ejercicio:** implementá Encode/Decode en Java que funcione con strings que contengan cualquier carácter, y demostralo con dos casos de prueba propios.

---

### Módulo 6 — Sorting & Searching (8:29:27 – 11:28:48, 179 min)

**Objetivo:** dominar binary search como patrón (no como búsqueda en array), quicksort/dutch national flag y merge sort.

**Contenidos:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 8:30:25 | Binary Search (plantilla base) | lo/hi, mid y actualización |
| 9:00:29 | Merge Sorted Array | dos punteros desde el final |
| 9:10:31 | Sort Colors ⭐ | dutch national flag (3 punteros) |
| 9:23:31 | Majority Element | hashmap / voting |
| 9:30:09 | Search in a 2D Matrix | binary search sobre matriz ordenada |
| 9:39:11 | Find Minimum in Rotated Sorted Array | binary search con lado ordenado |
| 9:51:51 | Search in Rotated Sorted Array | binary search con lado ordenado |
| 10:05:34 | Sort List | merge sort sobre linked list |
| 10:15:37 | Largest Number | orden con comparador custom |
| 10:28:56 | Koko Eating Bananas ⭐ | binary search sobre la respuesta |
| 10:44:48 | Time Based Key-Value Store | binary search sobre listas de timestamps |
| 11:01:48 | Median of Two Sorted Arrays ⭐ | binary search sobre partición |

- **Idea fuerza:** Koko Eating Bananas es el cambio de mentalidad del módulo: no se busca un índice, sino el menor valor que satisface una condición monótona, y eso también es binary search.
- **Idea fuerza:** la plantilla de binary search que se usa acá evita `mid = (lo+hi)/2` con desborde y fija la condición de corte antes de escribir el cuerpo; es la que hay que memorizar.

**Ejercicio:** implementá Koko Eating Bananas con la plantilla de binary search y escribí la función de verificación `canEat(k)` separada. Entregá la complejidad total (O(n log m), justificando el m).

---

### Módulo 7 — Linked List (11:28:48 – 14:08:48, 160 min)

**Objetivo:** manipular punteros con seguridad, y reconocer los dos patrones: fast/slow y reversión.

**Contenidos:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 11:31:53 | (teoría: singly, doubly, circular, fast/slow) | fundamentos |
| 11:39:59 | Reverse Linked List ⭐ | tres punteros |
| 11:47:50 | Middle of the Linked List | fast/slow |
| 11:58:15 | Linked List Cycle | fast/slow |
| 12:09:40 | Merge Two Sorted Lists | merge |
| 12:20:36 | Remove Nth Node From End | dos punteros con offset |
| 12:31:02 | Add Two Numbers | suma con acarreo |
| 12:56:36 | Find the Duplicate Number ⭐ | ciclo de Floyd sobre índices |
| 13:10:28 | Copy List with Random Pointer | intercalado |
| 13:27:14 | Merge K Sorted Lists ⭐ | heap / divide y vencerás |
| 13:39:06 | Reorder List | mitad + reversión + merge |
| 13:56:22 | (problema de linked list, cierre) | repaso |

- **Idea fuerza:** Find the Duplicate Number es el momento donde linked list deja de ser una estructura y pasa a ser un grafo implícito: los valores son aristas, y el ciclo se detecta con Floyd.
- **Idea fuerza:** Reorder List es la combinación canónica de las tres técnicas del módulo; si sale, el módulo está cerrado.

**Ejercicio:** Reorder List completo en Java, más Find the Duplicate Number con la justificación del grafo implícito.

---

### Módulo 8 — Stack (14:08:47 – 16:43:55, 155 min)

**Objetivo:** stack como herramienta de *parsing* y monotonic stack como herramienta de "el siguiente mayor".

**Contenidos:**

- **Teoría:** `(14:09:08)` qué es un stack, LIFO, implementación con array/list, complejidad de operaciones. «This is a special kind of list that contains a very specific property and that is called leo property that is called last in first out» `(14:09:47)`.
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 14:26:06 | Valid Parentheses | stack de aperturas |
| 14:37:51 | Min Stack | stack con mínimo acumulado |
| 14:47:15 | Max Stack (premium) | stack + estructura auxiliar |
| 14:59:37 | Daily Temperatures ⭐ | monotonic stack |
| 15:13:50 | Car Fleet | monotonic stack / orden |
| 15:20:53 | (problema de stack) | simulación |
| 15:33:03 | (problema de stack) | parsing |
| 15:43:08 | Minimum Remove to Make Valid Parentheses | stack de índices |
| 15:54:11 | (paréntesis bien formados) | repaso |
| 16:09:20 | Evaluate Reverse Polish Notation ⭐ | postfix |
| 16:25:15 | Largest Rectangle in Histogram ⭐ | monotonic stack con alturas |

- **Idea fuerza:** monotonic stack mantiene los índices con alturas decrecientes; cada elemento se pushea y poppea una sola vez, y de ahí sale el O(n) de Largest Rectangle.
- **Idea fuerza:** Min Stack resuelve el problema de "el mínimo después de un pop" guardando el mínimo acumulado junto a cada valor; es la misma idea de sufijo del módulo de arrays.

**Ejercicio:** Daily Temperatures y Largest Rectangle in Histogram en Java; para el segundo, dibujá la pila paso a paso con el ejemplo de alturas `[2,1,5,6,2,3]`.

---

### Módulo 9 — Queue (16:43:55 – 17:58:08, 74 min)

**Objetivo:** FIFO, deque y circular queue; entender por qué la implementación con linked list da O(1).

**Contenidos:**

- **Teoría** `(16:49:09)`: array-based vs. linked-list-based; circular queue y por qué existe el índice modular `(16:50:14)`; deque como doble extremo `(16:50:31)`; introducción a priority queue `(16:51:48)`.
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 16:53:56 | Implement Queue using Stacks | dos stacks |
| 17:03:17 | Implement Stack using Queues | dos queues |
| 17:11:34 | Design Circular Queue | array con punteros front/rear |
| 17:25:14 | Open the Lock | BFS sobre estados |
| 17:42:48 | Dota2 Senate | queue de rondas |

- **Idea fuerza:** Open the Lock es la primera vez que BFS aparece "solapado" en un módulo que no es de grafos; vale registrarlo, porque en el módulo de grafos vuelve con el nombre correcto.
- **Idea fuerza:** Dota2 Senate es el caso donde dos queues se usan como "turnos": el que gana vuelve al final con una ronda extra.

**Ejercicio:** Design Circular Queue en Java con capacidad fija y sin `ArrayDeque`; probá con el caso de capacidad 0 y 1 que pide LeetCode.

---

### Módulo 10 — Priority Queue / Heap (17:58:08 – 20:55:54, 178 min)

**Objetivo:** saber cuándo un heap resuelve "los k mayores/menores" y cómo se construye sobre un array.

**Contenidos:**

- **Teoría** `(17:58:16)`: min heap vs. max heap — «the parent node is always going to be less than the child node» `(17:58:37)`; heap balanceado `(18:01:02)`; por qué un heap no es un BST `(18:00:02)`.
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 18:28:19 | Last Stone Weight | max heap |
| 18:39:10 | Kth Largest Element in an Array ⭐ | min heap de tamaño k |
| 18:47:23 | K Closest Points to Origin | heap por distancia |
| 19:15:56 | (k largest, repaso) | heap |
| 19:28:20 | Task Scheduler | heap + cooldown |
| 19:49:12 | Employee Free Time (premium) | merge de intervalos con heap |
| 20:00:05 | Find Median from Data Stream ⭐ | dos heaps |
| 20:29:57 | Design Twitter | heap sobre feeds |

- **Idea fuerza:** Kth Largest con un min heap de tamaño k es el patrón que más se repite: O(n log k) en lugar de ordenar todo.
- **Idea fuerza:** Find Median from Data Stream con dos heaps balanceados es la prueba de que el heap sirve para mantener un estadístico, no solo para ordenar.

**Ejercicio:** Find Median from Data Stream en Java con un max heap y un min heap balanceados (diferencia máxima de 1) y la explicación de qué invariante se mantiene.

---

### Módulo 11 — Trees (20:55:54 – 25:20:01, 264 min)

**Objetivo:** recorrer árboles con recursión sin miedo, y elegir DFS o BFS según la pregunta.

**Contenidos:**

- **Teoría** `(20:57:59)`: root, parent, child, leaf, subtree, height, depth, degree `(20:58:17 – 21:00:15)`; tipos: general, binario, ternario, n-ario, y BST `(21:00:34)`; la propiedad del BST — izquierda menor que la raíz, derecha mayor `(21:02:11)`.
- **Problemas (DFS, excepto donde se aclara):**

| Tiempo | Problema | Patrón |
|---|---|---|
| 21:18:07 | (recorridos y aplicaciones) | teoría + DFS |
| 21:24:39 | Same Tree | DFS comparando |
| 21:31:44 | Symmetric Tree | DFS espejado |
| 21:39:46 | Invert Binary Tree | DFS swap |
| 21:55:39 | Binary Tree Level Order Traversal | BFS con cola |
| 22:07:53 | Zigzag Level Order Traversal | BFS con dirección |
| 22:23:35 | Binary Tree Right Side View | BFS último de nivel |
| 22:33:43 | Subtree of Another Tree | comparación de árboles |
| 22:41:40 | Count Good Nodes | DFS con máximo en el camino |
| 22:52:45 | Diameter of Binary Tree ⭐ | post-order con altura |
| 23:01:05 | Validate Binary Search Tree | DFS con rango |
| 23:11:14 | Lowest Common Ancestor of a BST | comparar con la raíz |
| 23:21:58 | Kth Smallest Element in a BST | in-order |
| 23:39:14 | Construct Binary Tree from Preorder & Inorder | división de rangos |
| 23:55:05 | Serialize and Deserialize Binary Tree | pre-order con marcadores |
| 24:06:08 | Binary Tree Maximum Path Sum ⭐ | post-order con ganancia |
| 24:21:47 | (trie: introducción) | estructura nueva |
| 24:47:03 | Word Search II ⭐ | trie + DFS/backtracking |
| 25:04:07 | Design Add and Search Words | trie con comodín |

- **Idea fuerza:** Diameter y Maximum Path Sum son el mismo patrón: post-order que devuelve la altura/ganancia hacia arriba y actualiza un máximo global.
- **Idea fuerza:** Word Search II es el puente entre trees, backtracking y trie: sin el trie, el DFS explota.

**Ejercicio:** Binary Tree Maximum Path Sum y Level Order Traversal (en forma zigzag) en Java; entregá también el invariante del post-order en una línea.

---

### Módulo 12 — Graphs (25:20:01 – 32:14:13, 414 min)

**Objetivo:** modelar un problema como grafo, elegir representación y saber cuándo BFS, cuándo DFS, cuándo topological sort y cuándo union-find.

**Contenidos:**

- **Teoría** `(25:20:07)`: nodos y aristas `(25:21:16)`; el ejemplo de la red de amigos de Facebook `(25:21:56)`; tipos: árbol como caso de grafo, dirigido vs. no dirigido, ponderado `(25:23:23)`; representación: matriz de adyacencia vs. lista.
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 25:42:25 | Number of Islands | DFS/BFS sobre grid |
| 26:00:40 | Max Area of Island | DFS sobre grid |
| 26:12:27 | Number of Connected Components | union-find / DFS |
| 26:23:37 | Graph Valid Tree | union-find / DFS con visitados |
| 26:59:17 | Redundant Connection | union-find |
| 27:03:50 | (disjoint set, teoría) | union-find |
| 27:34:45 | Rotting Oranges | BFS multi-fuente |
| 27:49:44 | Walls and Gates | BFS multi-fuente |
| 28:03:43 | Surrounded Regions | DFS desde bordes |
| 28:37:12 | (problema de grafos) | DFS |
| 29:03:19 | Pacific Atlantic Water Flow | DFS desde bordes |
| 29:24:51 | Find the Celebrity (premium) | eliminación |
| 29:42:19 | Word Ladder ⭐ | BFS sobre palabras |
| 29:58:47 | Network Delay Time | Dijkstra |
| 30:16:21 | Min Cost to Connect All Points | Prim / Kruskal |
| 30:36:20 | (MST, teoría) | Prim / Kruskal |
| 30:59:57 | (problema de grafos) | BFS/DFS |
| 31:16:27 | Alien Dictionary ⭐ | topological sort |
| 31:59:50 | Swim in Rising Water | Dijkstra / binary search |

- **Idea fuerza:** Rotting Oranges y Walls and Gates son BFS multi-fuente: se encolan todas las fuentes juntas y cada nivel es un minuto/distancia `(27:36:08)`.
- **Idea fuerza:** la diferencia entre Prim y Kruskal es de estructura, no de objetivo: los dos buscan el árbol de expansión mínimo, uno con heap y otro con union-find `(30:36:42)`.
- **Idea fuerza:** Alien Dictionary es el grafo construido desde las letras de un diccionario; el orden topológico es la respuesta, y el ciclo significa inconsistencia.

**Ejercicio:** Network Delay Time (Dijkstra con heap) y Alien Dictionary (topological sort con detección de ciclo) en Java. Para cada uno, escribí en una línea por qué BFS/Dijkstra y no DFS.

---

### Módulo 13 — Dynamic Programming (32:14:13 – 37:13:04, 299 min)

**Objetivo:** convertir un problema de "todos los caminos posibles" en una tabla; distinguir memoización de tabulación y justificar cuándo DP aplica.

**Contenidos:**

- **Teoría** `(32:14:58)`: DP como técnica de resolución (romper en subproblemas + guardar resultados). «this dynamic programming approach is nothing but a problem-solving technique and this technique involves you of taking a bigger problem and then start breaking into bunch of different smaller sub problems» `(32:14:58)`.
- **La motivación de Fibonacci** `(32:15:56)`: recursión 2ⁿ contando los subproblemas repetidos; tabla O(n). El contraste entre «we go of 2 to the power n» y «bigger of n simply» `(32:18:49)`.
- **Historia** `(32:19:04)`: atribuye DP a "Robert Bellman" en los 50 — el ASR deforma; es **Richard Bellman** (y el mismo del algoritmo Bellman-Ford).
- **Memoización (top-down) vs. tabulación (bottom-up)** `(32:21:08 – 32:23:07)`: cuándo conviene cada una. «So if you only need to do selective calculations in order to calc to generate the result uh then it would make sense to use top- down approach» `(32:24:20)`.
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 32:34:24 | Climbing Stairs | 1D DP |
| 32:44:25 | (introducción a 1D DP) | transición |
| 32:59:00 | House Robber | 1D DP con salto |
| 33:13:40 | Unique Paths | DP de grid |
| 33:25:33 | Pascal's Triangle | DP triangular |
| 33:38:48 | Coin Change ⭐ | unbounded knapsack |
| 34:09:24 | (problema de DP 1D) | LIS / subsecuencia |
| 34:35:30 | Maximum Product Subarray | DP con min y max |
| 34:48:07 | Longest Increasing Subsequence | DP O(n²) → O(n log n) |
| 35:36:34 | Longest Common Subsequence ⭐ | DP 2D |
| 35:53:54 | Word Break | DP sobre prefijos |
| 36:16:34 | Regular Expression Matching ⭐ | DP 2D con `*` y `.` |
| 36:44:34 | Race Car | DP / BFS |

- **Idea fuerza:** Maximum Product Subarray requiere llevar el mínimo además del máximo: el producto de dos negativos puede ser el nuevo máximo.
- **Idea fuerza:** Regular Expression Matching es el problema que separa "sé DP" de "entiendo DP": la tabla 2D y la diagonal son obligatorias `(36:29:16 – 36:40:12)`.
- **Advertencia del expositor:** hay problemas donde DP no es la primera opción, y la elección entre greedy y DP se justifica en el módulo siguiente `(37:16:36)`.

**Ejercicio:** Coin Change (bottom-up) y Longest Common Subsequence (una versión memoizada y una tabulada) en Java. Entregá la tabla de ambas versiones y la diferencia de complejidad.

---

### Módulo 14 — Greedy (37:13:04 – 39:06:36, 114 min)

**Objetivo:** distinguir cuándo una elección local óptima es globalmente óptima, y cuándo hace falta DP.

**Contenidos:**

- **Teoría** `(37:14:26)`: el ejemplo del vuelto de un billete — elegir el mayor billete primero. «take out the biggest chunk by the biggest denomination of money» `(37:14:26)`.
- **Greedy vs. DP** `(37:16:36)`: greedy no explora alternativas, DP sí. La pregunta de decisión: ¿el óptimo local se mantiene?
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 37:21:28 | Maximum Subarray ⭐ | Kadane |
| 37:30:50 | Jump Game | alcance máximo |
| 37:50:49 | Jump Game II | saltos con ventanas |
| 38:05:58 | Partition Labels | última ocurrencia |
| 38:16:30 | Merge Triplets to Form Target Triplet | comparar máximos |
| 38:27:17 | Gas Station ⭐ | total ≥ 0 + punto de reinicio |
| 38:38:51 | Hand of Straights | TreeMap + grupos |

- **Idea fuerza:** Gas Station: si el total de combustible alcanza, el índice donde el acumulado se vuelve positivo por última vez es el arranque válido `(38:33:35)`.
- **Idea fuerza:** Jump Game II es greedy con ventanas delimitadas por `currentEnd` y `currentMax` `(38:02:43)`.

**Ejercicio:** Gas Station y Jump Game II en Java, con un comentario que explique por qué el greedy es correcto (no solo que compila).

---

### Módulo 15 — Intervals (39:06:36 – 40:32:39, 86 min)

**Objetivo:** reconocer overlap, mergear, y elegir entre sort por inicio y sort por fin.

**Contenidos:**

- **Qué es un intervalo** `(39:06:57)`: `[inicio, fin)`, con aplicaciones reales (agendas, reservas de salas).
- **Regla de solapamiento** `(39:10:51)`: si `start` cae dentro de otro intervalo, hay solape; el ejemplo del 20/20 muestra que el extremo compartido **no** cuenta como solape.
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 39:07:32 | Meeting Rooms (premium) | sort por inicio |
| 39:18:18 | Merge Intervals ⭐ | sort + merge |
| 39:55:02 | Non-overlapping Intervals | sort por fin |
| 40:09:56 | Remove Interval (premium) | partir intervalos |
| 40:17:39 | Meeting Rooms II (premium) | sort + heap |

- **Idea fuerza:** Merge Intervals ordena por inicio y toma el `max` del fin; Non-overlapping Intervals ordena por fin, que es lo que minimiza los que hay que borrar. La elección del criterio de orden es la solución.
- **Idea fuerza:** Meeting Rooms II es un conteo de máximo de intervalos simultáneos, y se resuelve con un min heap de fines.

**Ejercicio:** Merge Intervals y Non-overlapping Intervals en Java; entregá por qué el criterio de orden es distinto en cada uno, en dos líneas.

---

### Módulo 16 — Backtracking (40:32:39 – 42:45:51, 133 min)

**Objetivo:** construir todas las soluciones de un problema con la plantilla elegir / explorar / deshacer.

**Contenidos:**

- **Por qué backtracking** `(40:40:10)`: recursión + deshacer. Sin el deshacer, se exploran caminos que no vuelven.
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 40:40:10 | Subsets ⭐ | incluir / no incluir |
| 41:03:00 | Permutations | elegir de lo restante |
| 41:18:26 | Letter Combination of a Phone Number | cartesiano | 
| 41:29:26 | Combination Sum | elegir con repetición |
| 41:52:23 | Combination Sum II | ordenar + saltar duplicados |
| 42:05:23 | Palindrome Partitioning | cortar y validar |
| 42:22:46 | N-Queens | restricciones por fila/diagonal |

- **Idea fuerza:** la plantilla de Subsets (`elegir` / `no elegir`) es el esqueleto de todos los demás; Permutations solo cambia qué se elige.
- **Idea fuerza:** N-Queens es la prueba de que el backtracking es búsqueda con poda: las restricciones de columna y diagonales son lo que vuelve factible un problema de 8! posibilidades.

**Ejercicio:** Combinar Subsets y N-Queens en Java con la misma plantilla; anotar en cada línea cuál es el "deshacer".

---

### Módulo 17 — Math & Geometry (42:45:51 – 43:42:30, 57 min)

**Objetivo:** las aritméticas que aparecen en entrevista y no son DP: suma con acarreo, exponenciación, números como ciclos.

**Contenidos:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 42:46:54 | Plus One | acarreo sobre dígitos |
| 42:53:15 | Happy Number | detección de ciclo sobre dígitos |
| 43:01:46 | Pow(x, n) ⭐ | exponenciación rápida |
| 43:10:22 | Multiply Strings | multiplicación por dígitos |
| 43:21:16 | Detect Squares | hashmap de puntos |

- **Idea fuerza:** Pow(x,n) es binary search disfrazado de matemática: exponenciar al cuadrado divide el exponente a la mitad.
- **Idea fuerza:** Happy Number es Floyd otra vez, pero sobre la suma de cuadrados de dígitos.

**Ejercicio:** Pow(x,n) en Java con exponenciación rápida y sin usar `Math.pow`; explicá qué pasa con exponente negativo.

---

### Módulo 18 — Matrix (43:42:30 – 45:55:06, 133 min)

**Objetivo:** recorrer matrices sin pisar la celda equivocada; marcar el estado dentro de la propia matriz.

**Contenidos:**

- **Qué es una matriz** `(43:42:35)`: extensión 2D del array, representación de imágenes, grids y grafos.
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 43:43:27 | Set Matrix Zeroes ⭐ | marcar con fila/columna 0 |
| 44:00:56 | Spiral Matrix | cuatro bordes |
| 44:20:26 | Rotate Image | transponer + invertir |
| 44:36:29 | (problema de matriz) | recorrido |
| 44:55:12 | (problema de matriz) | simulación |
| 45:17:24 | Word Search | DFS + backtracking |
| 45:32:08 | Longest Increasing Path in a Matrix ⭐ | DFS + memoización |

- **Idea fuerza:** Set Matrix Zeroes en O(1) espacio usa la primera fila y la primera columna como marcadores; el "truco" es ver la matriz como su propio array auxiliar.
- **Idea fuerza:** Longest Increasing Path combina DP con DFS sobre grid: la memoización sobre celdas es lo que la vuelve lineal.

**Ejercicio:** Spiral Matrix y Set Matrix Zeroes en Java; para el segundo, demostrá que no se usa espacio auxiliar.

---

### Módulo 19 — Design (45:55:06 – 47:22:33, 87 min)

**Objetivo:** responder "diseñá una clase que soporte X en O(1)" eligiendo la estructura correcta y combinándolas.

**Contenidos:**

- **Qué es un problema de design** `(45:55:19)`: mezcla de DSA con escenario real; no es system design.
- **Problemas:**

| Tiempo | Problema | Estructura |
|---|---|---|
| 45:56:27 | Moving Average from Data Stream | cola + suma acumulada |
| 46:08:07 | (design, continuación) | estructura + invariante |
| 46:22:36 | Design Tic-Tac-Toe (premium) | conteos por fila/columna/diagonal |
| 46:42:04 | Insert Delete GetRandom O(1) ⭐ | array + hashmap |
| 46:59:39 | LRU Cache ⭐ | hashmap + lista doblemente enlazada |

- **Idea fuerza:** Insert Delete GetRandom O(1) es la combinación que resuelve la contradicción: el array da acceso aleatorio y el hashmap da acceso por valor.
- **Idea fuerza:** LRU Cache es el problema de design más pedido: la lista doblemente enlazada da O(1) para mover al frente.

**Ejercicio:** LRU Cache en Java sin `LinkedHashMap`: implementá la lista doblemente enlazada a mano y explicá por qué cada operación es O(1).

---

### Módulo 20 — Bit Manipulation (47:22:33 – 48:48:17, 86 min)

**Objetivo:** resolver con operadores de bits los problemas que aparecen ocasionalmente.

**Contenidos:**

- **Advertencia del expositor** `(47:22:46)`: es el tema de menor probabilidad en entrevista, y la calidad del video es peor porque es de sus primeros registros. La tabla de verdad de las compuertas (AND, OR, NAND, etc.) está en pantalla.
- **Problemas:**

| Tiempo | Problema | Patrón |
|---|---|---|
| 47:24:30 | Single Number ⭐ | XOR |
| 47:43:59 | Reverse Bits | desplazamiento |
| 48:11:36 | Sum of Two Integers | suma sin `+` con carry |
| 48:27:36 | Reverse Integer | acarreo + overflow |
| 48:33:45 | Counting Bits | `dp[i] = dp[i>>1] + (i&1)` |

- **Idea fuerza:** Single Number con XOR funciona porque `a XOR a = 0` y `a XOR 0 = a`: todo se cancela salvo el que aparece una vez.
- **Idea fuerza:** Counting Bits es DP sobre bits: la representación de `i` es la de `i>>1` más el bit menos significativo.

**Ejercicio:** Single Number, Reverse Bits y Counting Bits en Java; para Counting Bits, escribí la recurrencia.

---

### Módulo 21 — Cierre (48:48:17 – 48:50:00)

Mensaje final: el curso termina sin resumen metodológico. Lo que sigue después son los créditos y la mención a los sponsors.

---

## Ejercicios por bloque

Un bloque se cierra cuando los cuatro ítems están hechos. Sin el ítem 4, no está cerrado.

- [ ] **Fundamentos (M1)**: cinco complejidades justificadas + tabla de perspectiva verificada a mano.
- [ ] **Arrays (M2)**: los 4 problemas del ejercicio + tabla de patrones completada.
- [ ] **Sliding Window (M3)**: deque monotónica implementada y explicada.
- [ ] **Two Pointers (M4)**: 3Sum sin duplicados.
- [ ] **Strings (M5)**: Encode/Decode con casos límite propios.
- [ ] **Sorting & Searching (M6)**: Koko Eating Bananas con `canEat` separado.
- [ ] **Linked List (M7)**: Reorder List + Find the Duplicate Number.
- [ ] **Stack (M8)**: Daily Temperatures + Largest Rectangle, con dibujo de la pila.
- [ ] **Queue (M9)**: Circular Queue a mano, con capacidad 0 y 1.
- [ ] **Heap (M10)**: Find Median from Data Stream con dos heaps.
- [ ] **Trees (M11)**: Maximum Path Sum + Level Order, con invariante.
- [ ] **Graphs (M12)**: Network Delay Time + Alien Dictionary.
- [ ] **DP (M13)**: Coin Change + LCS en dos versiones.
- [ ] **Greedy (M14)**: Gas Station + Jump Game II justificados.
- [ ] **Intervals (M15)**: Merge + Non-overlapping, con criterio de orden explicado.
- [ ] **Backtracking (M16)**: Subsets + N-Queens con la misma plantilla.
- [ ] **Math (M17)**: Pow(x,n) sin `Math.pow`.
- [ ] **Matrix (M18)**: Spiral Matrix + Set Matrix Zeroes en O(1).
- [ ] **Design (M19)**: LRU Cache sin `LinkedHashMap`.
- [ ] **Bit (M20)**: Single Number + Counting Bits con recurrencia.

## Banco de preguntas para estudiar con el usuario

1. ¿Por qué la misma entrada (n=1.000) tarda 1 s en O(1) y un número de 301 dígitos de operaciones en O(2ⁿ), y qué significa eso para elegir un algoritmo en una entrevista?
2. Un array y una linked list tienen las mismas operaciones pero distinta complejidad: ¿cuál usás para búsqueda por índice, cuál para inserción en el medio, y por qué?
3. En Sliding Window Maximum, ¿qué hace la deque que un `max` sobre la ventana no puede hacer? ¿Cómo se mantiene O(n)?
4. ¿Cuándo el patrón es "ordenar y dos punteros" y cuándo es "hashmap"? Pensalo con 3Sum y Two Sum II.
5. Binary search no siempre busca en un array: Koko Eating Bananas y Median of Two Sorted Arrays, ¿qué comparten y qué los hace binary search?
6. DFS y BFS visitan lo mismo, pero eligen distinto: ¿cuándo BFS es obligatorio y cuándo DFS es más barato?
7. DP y greedy resuelven problemas de optimización: ¿qué pregunta contestás para decidir entre uno y otro?
8. En tu opinión, ¿cuál de los 20 temas es el que más te cuesta y qué harías esta semana para bajar esa deuda?

## Notas editoriales

- **Nombre del expositor.** El ASR lo transcribe «Parvas» en el minuto 2:05; la descripción del video atribuye el curso a *Parth* de Destination FAANG, y su propio canal es `@DestinationEngineer`. Se usa **Parth**, y la transcripción queda con el error del ASR sin editar (está en el glosario).
- **Empresa actual.** Al minuto 2:05 dice "solutions architect for Cinniplex"; a partir de 3:12:44 dice "cloud solutions architect at Microsoft". Ambas cosas pueden ser ciertas en momentos distintos del video (los segmentos son grabaciones sueltas unidas, con frases de apertura que cambian) pero el video no lo aclara. **No se usa como dato de CV.**
- **Atribución de DP.** El video dice "Robert Bellman" (32:19:27). Es **Richard Bellman**. Error del expositor, no del ASR.
- **Duración de los módulos.** El mapa oficial tiene 29 entradas, pero los límites internos de algunos módulos arrancan unos minutos antes del timestamp oficial (por ejemplo Stack a las 14:08:47 cuando el índice dice 14:08:48, o la teoría de Queue a las 16:49 y el índice dice 16:43:55). Se respetan los timestamps oficiales en el mapa y se marca el inicio real de la teoría donde difiere.
- **Problemas premium.** Meeting Rooms, Meeting Rooms II, Employee Free Time, Encode/Decode Strings, Find the Celebrity, Design Tic-Tac-Toe y Max Stack son de LeetCode Premium. El video los explica completo, pero en LeetCode no se pueden practicar sin suscripción; el repo de soluciones en Java cubre el código.
- **Promesa no cumplida.** El expositor dice «close to 200» problemas `(0:01:30)` y luego «25 most popular» para arrays `(0:58:06)`; el conteo real de problemas con timestamp identificable en la transcripción es de ~150. No es un error grave, pero la promesa de 200 no se verifica con el video.
- **Números del módulo Big O.** La tabla de perspectiva `(0:30:03)` es del propio expositor y no se verificó contra una fuente externa: son ilustrativos de crecimiento, no mediciones. No se copian como hechos.
- **Orden de estudio.** El orden del video es el oficial y está bien como recorrido completo. El orden por tramos de esta clase es una propuesta editorial para quien no vaya a hacer las 49 horas seguidas.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
