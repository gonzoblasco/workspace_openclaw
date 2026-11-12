# Módulo 1 — Big O y cómo juzgar un algoritmo (00:00:00 → 00:50:21)

> **Duración en el video:** 50 minutos de los capítulos `Introducción`, `Entrevistas técnicas 101`, `Cómo juzgar un algoritmo`, `Qué es la complejidad temporal`, `Qué es Big O`, `Big O para bloques de código`, `Ejemplo de complejidad espacial`, `Cómo volverse bueno resolviendo problemas de DSA`, `Tipos de estructuras de datos` y `Repaso rápido` (0:00:00 → 0:50:21).
> **Lo que tenés que poder hacer al terminar:** mirar un bloque de código y decir su complejidad de tiempo y espacio con una justificación de una línea, y explicar por qué la misma idea resuelta de dos maneras distintas no es la misma solución.
> **Nota de método:** esto no es un resumen del video. El video es la fuente principal; acá está la clase **trabajada**: qué queda, qué hay que ejercitar, y dónde el expositor se queda corto o se equivoca. Lo que aporto de afuera está marcado como **[externo]**.

---

## 1. La pregunta del módulo (00:00:00 → 00:08:02)

El video abre con una frase que vale más que todo el resto del capítulo:

> «These interviews often hinge on your ability to confidently solve problems using data structures and algorithms» `(0:00:00)`

Y a los siete minutos define el criterio con el que va a juzgar todo lo demás:

> «there are three things that we are looking for» `(0:07:03)`

Los tres: **exactitud**, **complejidad temporal**, **complejidad espacial**. El orden importa. Sin el primero, los otros dos son optimizar un algoritmo que hace la cosa equivocada — el error más caro y el más frecuente.

Lo que el módulo entero construye es esto:

> «Time complexity is nothing but how much» `(0:07:21)`

...y sigue, en el bloque siguiente: «longer will it take for you to complete your algorithm or your task if the number of inputs keeps on growing larger and larger» `(0:07:40)`.

Leelo dos veces. **No es cuánto tarda. Es cómo crece cuando la entrada crece.** Un algoritmo que tarda 10 segundos con 10 elementos y sigue tardando 10 segundos con un millón es mejor que uno que tarda un milisegundo con 10 y tres días con un millón — para el problema del millón. La pregunta de la entrevista nunca es "¿es rápido?", es "¿qué pasa cuando esto se hace diez mil veces más grande?"

**[externo] El matiz que el video no hace explícito.** Big O describe el crecimiento **asintótico** y por eso ignora constantes. Eso tiene un costo real: un O(n) con una constante de 1.000 es más lento que un O(n log n) con constante de 1 hasta n ≈ 2^1000. Es decir: **Big O no decide qué es más rápido en tu máquina hoy**, decide qué escala. Y como en una entrevista te preguntan por el futuro del sistema, no por el benchmark de hoy, la convención está bien — pero conviene saber que es una convención, no una ley física.

---

## 2. Las cinco complejidades, con el ejemplo físico de cada una (00:08:02 → 00:18:42)

El expositor no define las complejidades con fórmulas: las define con objetos. Es una decisión pedagógica buena, y conviene quedarse con los objetos.

| Complejidad | El objeto del video | Qué la vuelve esa complejidad |
|---|---|---|
| **O(1)** | Bandeja de garbanzos numerada: la posición 5 tiene 5 garbanzos `(0:11:16)` | La respuesta está en una **posición**, no en una búsqueda |
| **O(log n)** | Buscar una carta en un mazo ordenado abriendo por el medio `(0:10:20)` | Cada paso descarta la mitad: «we are essentially eliminating 50% of all the inputs in one go» `(0:10:33)` |
| **O(n)** | Buscar un valor en un array sin ordenar `(0:22:16)` | Hay que mirar cada elemento una vez |
| **O(n²)** | Emparejar dos mazos: por cada carta del primero, buscar su par en el segundo `(0:13:28)` | «loop within a loop» |
| **O(2ⁿ)** | Tirar monedas: cada moneda nueva duplica las combinaciones `(0:14:18)` | Cada decisión binaria **abre** la anterior |
| **O(n!)** | Tres personas en tres asientos: 3×2×1 `(0:16:04)` | Cada elección **reduce** el conjunto de las siguientes |

### El detalle que casi nadie retiene: 2ⁿ y n! son parientes

Los dos crecen por encima de cualquier polinomio, pero **desde direcciones opuestas**:

- En **O(2ⁿ)** (Fibonacci recursivo) el árbol se *ensancha*: hojas de más y más ramas, cada una un subproblema **repetido**. Ahí está la cura: DP (memorizar los subproblemas).
- En **O(n!)** (permutaciones) el árbol se *profundiza*: cada elegido saca una opción. Acá no hay subproblema repetido — cada permutación es distinta — y DP no alcanza; la cura es **poda** (backtracking con restricciones), que es exactamente lo que hace N-Queens en el módulo 16.

Esta distinción es la que después decide qué patrón usar. El video la deja implícita; vale tenerla explícita ahora, porque el módulo 13 (DP) y el 16 (backtracking) la van a necesitar.

### Por qué se llama Big O (00:18:42)

> «we are trying to calculate the upper bound of growth rate for the given algorithm» `(0:18:57)`

La **O** es de *order*. Es una cota superior: "no crece más rápido que". Por eso O(n) **también es** O(n²) — que es pedirle al barrendero que barra la manzana y después limpie el universo. **La nota que se escribe es la más ajustada que podés demostrar**, no cualquier cota válida. Eso no está dicho en el video y es la fuente de casi todas las confusiones con la notación.

**[externo] Las cuatro letras, porque aparecen en los libros.** O es cota superior (peor caso, la que se responde); Ω (*omega*) es cota inferior (mejor caso); Θ (*theta*) es cota ajustada, cuando superior e inferior coinciden; o minúscula es cota estricta. En entrevista se responde **O**, y cuando se puede se dice "es Θ de" para marcar que es justa. El video usa O para todo, que es lo que hace todo el mundo: está bien, mientras sepas que en rigor estás afirmando una cota superior.

---

## 3. Big O de bloques de código (00:20:20 → 00:33:08) — acá está la parte que se usa todos los días

El expositor pasa nueve bloques, de O(1) a O(n!). Los cuatro que se repiten en toda entrevista:

**a) Acceso a un elemento: O(1)**
> «we can call this as big O of one or constant time complexity for this code block» `(0:20:44)`

**b) Búsqueda binaria: O(log n).** El bloque que importa, porque es el que hace O(1) → O(log n) por una sola decisión de forma.

**c) Búsqueda lineal: O(n).** Y la frase que hay que tatuarse:
> «we might have to iterate over the entire array before we find the appropriate value» `(0:22:16)`

Eso es **peor caso**. La búsqueda lineal puede terminar en el primer intento, pero se responde por el peor: si el dato no está o está al final, recorrés todo.

**d) Merge sort: O(n log n).**
> «this code block is an example of go of n log n work» `(0:24:25)`

Y acá hay un detalle de lectura que el video pasa rápido y que conviene detenerse a entender: *¿de dónde salen los dos factores?* El **n** es "ordenar cada tarjeta" (hay n de ellas). El **log n** es cuántas veces podés partir el mazo a la mitad antes de llegar a una. Multiplicados dan el costo total. Es decir: **n log n no es un símbolo, es "una operación por elemento, repetida log n rondas"**. Y esa intuición se vuelve a usar en binary search sobre la respuesta (Koko, módulo 6) y en divide y vencerás (Merge K Sorted Lists, módulo 7).

### La tabla de perspectiva: usala, no la memorices (00:30:03)

El video arma una tabla de "cuánto tarda" con n = 10, 100 y 1.000. Esa tabla es **ilustrativa**, no medición: supone 1 unidad de tiempo por operación, que es una ficción cómoda. No la voy a copiar como dato (y el propio outline lo aclara en las notas editoriales). Lo que sí vale es la escala, y la verifico yo:

| n | O(1) | O(log n) | O(n log n) | O(n²) | O(2ⁿ) |
|---|---|---|---|---|---|
| 10 | 1 | 3,3 | 33 | 100 | 1.024 |
| 100 | 1 | 6,6 | 664 | 10.000 | ≈1,27 × 10³⁰ |
| 1.000 | 1 | 10 | 9.966 | 1.000.000 | ≈1,07 × 10³⁰¹ |
| 10.000 | 1 | 13,3 | 132.900 | 100.000.000 | (301 dígitos) |

El número que hay que *sentir*: **2ⁿ con n = 1.000 tiene 302 dígitos.** Si cada operación tardara un segundo, serían ~3,4 × 10²⁹³ años — el universo tiene ~1,4 × 10¹⁰. No es "lento": está fuera de la escala en la que el tiempo signifique algo. Un algoritmo así no está "lento": **no existe** como solución en la práctica, y por eso la entrevista te pide bajarlo.

Y la lectura inversa, que es la que se usa en el trabajo real: **de O(n²) a O(n log n) es la mejora que importa**, porque es la que separa un sistema que aguanta de uno que se cae con el doble de datos. Bajar de 2ⁿ a n² también, pero cuando estás en 2ⁿ el problema no es optimizar: es **cambiar el enfoque** (memoizar, o podar).

---

## 4. Complejidad espacial (00:33:08 → 00:35:04)

El ejemplo es bueno y el video lo cierra demasiado rápido: dos frascos, garbanzos negros y blancos, hay que intercambiarlos.

- **Sin espacio extra:** mover uno por uno a un lado, clasificando a ojo → O(n²) tiempo, O(1) espacio.
- **Con un tercer frasco:** una pasada, cada garbanzo va a su destino → O(n) tiempo, **O(n) espacio** (el frasco).

Eso es el *trade-off* en su forma más desnuda, y es la decisión que vas a tomar en Product of Array Except Self (no podés dividir: necesitás espacio para el prefijo), en Set Matrix Zeroes (usás la primera fila/columna como espacio propio para evitar el O(m·n)) y en LRU Cache. **No hay una respuesta correcta sin saber qué restringió el entrevistador.** Si pidió O(1) de espacio, la solución del tercer frasco no vale, aunque sea más rápida.

**[externo] La trampa del espacio que los candidatos subestiman: la recursión cuenta.** Un DFS sobre un árbol balanceado de 1.000 nodos tiene espacio O(log n) — la pila de llamadas. Sobre una lista enlazada de 1.000 nodos, **O(n)**. Dos algoritmos con el mismo código y "O(1) de espacio" en apariencia difieren según la forma de la entrada. Cuando digas "espacio O(1)", preguntate si dejaste recursión adentro.

---

## 5. Cómo se vuelve bueno alguien en esto (00:35:04 → 00:37:34)

Tres pasos, y el tercero es el que casi todos saltean:

1. Entender el problema **en los términos más simples**.
2. Buscar **patrones que se repiten** entre problemas.
3. Resolverlo **primero con fuerza bruta**:
> «try to solve it using the most simplest terms or even the brute force approach even if it is not optimized for speed or anything else» `(0:35:42)`

**[externo] Por qué la fuerza bruta primero no es pereza, es método.** Una solución que da la respuesta correcta a la velocidad del oso es *una especificación ejecutable* contra la que podés testear la optimización. Optimizar sin tener el oráculo es cómo se pierden las horas en la entrevista: no sabés si el bug está en la idea nueva o en la vieja. Y hay un beneficio menos evidente: la fuerza bruta **revela el patrón**, porque te obliga a ver qué estás recalculando de más — y ese recálculo es exactamente lo que la optimización elimina.

El orden operativo que se desprende: **correcto → claro → rápido**, y nunca al revés.

---

## 6. Tipos de estructuras (00:37:34 → 00:48:48)

Tres familias, y la tercera es la que rompe el molde:

> «A linear data structure is a data structure where basically all the elements are typically sequential» `(0:37:43)`

| Familia | Miembros | Lo que comparten |
|---|---|---|
| **Lineal** | array, linked list, stack, queue | Un orden secuencial: "el siguiente" existe |
| **No lineal / jerárquica** | tree, graph | Un elemento apunta a varios; no hay "el siguiente" |
| **Hash-based** | hashmap, hashset | La posición la calcula una función, no el orden |

De la tercera el video dice que en un hashmap no recorrés para buscar: `(0:45:32)` — el acceso es directo por hash. **[externo] El costo que el video no menciona:** el hash "directo" es O(1) **promedio**. Con colisiones patológicas (todas las claves cayendo en el mismo bucket) degenera a O(n). Por eso un hashmap no es una bala de plata: es O(1) esperado, O(n) peor caso. En una entrevista, decir "hashmap, O(1) prometido" te distingue de decir "hashmap, O(1)".

---

## 7. Dónde el video se queda corto (lo que tenés que saber y no está)

Lo que el expositor **no** cubre en este módulo y vas a necesitar:

1. **La aritmética de Big O.** `O(n) + O(n) = O(n)`; `O(n) + O(n²) = O(n²)`; `O(2n) = O(n)`. La regla: **queda el término dominante y se tiran las constantes.** El video muestra bloques y dice el resultado, pero nunca da el procedimiento para combinarlos. Sin esto, un bloque con tres loops no se puede resolver.
2. **Logaritmo de qué base.** En Big O la base es irrelevante (log₂ n y log₁₀ n difieren por una constante). Por eso "O(log n)" sin base está bien escrito.
3. **Complejidad amortizada.** Vector que crece al doble: una inserción es O(n) cuando copia, pero **en promedio O(1)**. Es lo que hace que `append` sea barato. El video no lo nombra en este módulo; aparece de hecho en el módulo de colas.
4. **Dos variables de entrada.** O(m + n), O(m·n) — el video no las trata acá, y son la mitad de los problemas de grafos y matrices.
5. **Medir en vez de adivinar.** `System.nanoTime()` en Java y un gráfico. Big O dice la forma; medir dice la constante.

---

## 8. Ejercicios del módulo

Cerrar el módulo es tener los cuatro. El cuarto lo corrijo yo contra tu respuesta.

### 8.1 — La tabla, a mano (20 min)

Sin calculadora, completá para n = 1.000:

| Complejidad | Operaciones (orden de magnitud) |
|---|---|
| O(1) | |
| O(log n) | |
| O(n) | |
| O(n log n) | |
| O(n²) | |

Después respondé: **¿cuántas veces más lento es O(n²) que O(n log n) con n = 1.000?** (Con el número, no con "mucho".)

<details><summary>Respuesta</summary>

1; ~10; 1.000; ~10.000; 1.000.000.

O(n²) es **~100 veces** más lento: 1.000.000 / 9.966 ≈ 100,3. Y ese factor crece con n: a n = 10.000 es 100.000.000 / 132.900 ≈ **752 veces**. La moraleja: una diferencia de notación que a n = 10 parece un detalle, a escala de producción es la diferencia entre un servidor y doscientos.

</details>

### 8.2 — Cinco bloques, sin correr nada (25 min)

Para cada uno: complejidad temporal **y** espacial, con una línea de justificación.

```java
// A
int getFirst(int[] a) { return a[0]; }

// B
int buscar(int[] a, int x) {
    for (int i = 0; i < a.length; i++)
        if (a[i] == x) return i;
    return -1;
}

// C
void pares(int[] a) {
    for (int i = 0; i < a.length; i++)
        for (int j = i + 1; j < a.length; j++)
            System.out.println(a[i] + "," + a[j]);
}

// D
int f(int n) { return n <= 1 ? n : f(n-1) + f(n-2); }

// E
int[] nuevo(int n) { return new int[n]; }
```

<details><summary>Respuesta</summary>

**A** — O(1) tiempo, O(1) espacio. Acceso por índice: no depende de `a.length`.

**B** — O(n) peor caso / O(1) mejor, O(1) espacio. Si el elemento no está, recorre todo. Es el ejemplo del video.

**C** — O(n²) tiempo. El loop interno arranca en `i+1`, así que corre n(n−1)/2 veces: la mitad de n², que en Big O **sigue siendo O(n²)** porque las constantes se tiran. O(1) espacio. **Este es el punto donde el video da el resultado pero no la regla:** contar los pares como n²/2 y no dejarlo en n² es el error de bulto típico.

**D** — O(2ⁿ) tiempo: cada llamada abre dos y los subproblemas **se repiten**. O(n) espacio: la pila más profunda es n. Ese espacio es el que hace tan deseable el memoizado: se paga O(n) para que el tiempo baje de exponencial a O(n).

**E** — O(n) tiempo (inicializar el array no es gratis), O(n) espacio. La trampa: "crear un array" se siente O(1), y en Java no lo es, porque el runtime tiene que escribir ceros en n posiciones.

</details>

### 8.3 — La misma tarea, tres algoritmos (30 min)

El video lo dice y no lo ejercita: buscar un elemento en un array da el mismo resultado con lineal y con binario, y no son equivalentes. Escribí en Java:

1. Búsqueda **lineal** sobre un array desordenado.
2. Búsqueda **binaria** sobre el mismo array ya ordenado.
3. Un `main` que mida las dos con `System.nanoTime()` sobre 1.000.000 de elementos, buscando el último, y muestre la diferencia.

Entregá: el código y **el número real** de la diferencia en tu máquina. Te anticipo que va a ser una diferencia de ~5 órdenes de magnitud (log₂ 1.000.000 ≈ 20 comparaciones contra 1.000.000). Si no lo es, algo raro pasó y lo vemos.

### 8.4 — La pregunta de entrevista (10 min, escrito)

Un entrevistador te da este código y te dice *"esto está lento con 100.000 registros, ¿por qué y cómo lo mejorarías?"*

```java
boolean hayDuplicado(int[] a) {
    for (int i = 0; i < a.length; i++)
        for (int j = i + 1; j < a.length; j++)
            if (a[i] == a[j]) return true;
    return false;
}
```

Respondé en tres frases: **cuál es la complejidad actual y por qué**, **qué estructura lo baja y a cuánto**, **qué pagás por eso**. Ese último punto — lo que pagás — es la mitad de la respuesta en una entrevista real, y es lo que hoy casi nadie contesta.

---

## 9. Banco de preguntas para repasar (las hago yo cuando digas)

1. ¿Por qué O(n) también es O(n²) y por qué no lo escribimos así?
2. `2ⁿ` y `n!` crecen los dos por encima de cualquier polinomio: ¿por qué la cura de uno es DP y la del otro es poda?
3. ¿Qué diferencia hay entre "tarda menos" y "crece más lento", y por qué una entrevista pregunta lo segundo?
4. Un merge sort es O(n log n): ¿de dónde sale cada uno de los dos factores?
5. Tu solución recursiva de un árbol dice "espacio O(1)": ¿en qué caso es mentira?
6. ¿Por qué la búsqueda lineal se responde por su peor caso y no por su promedio?
7. ¿Cuándo un hashmap deja de ser O(1)?
8. ¿Qué le pagás al espacio cuando cambiás O(n²) por O(n) con un hashset?

---

## 10. Fuera del video: qué verificar y qué ya verifiqué

- **La tabla de perspectiva `(0:30:03)` es del expositor y no es medición.** No la usé como dato; recalculé los valores con Python y dejé la tabla propia en §3.
- **La atribución de DP a "Robert Bellman" `(32:19:27)` es un error del expositor:** es **Richard Bellman**. No toca este módulo, pero el dato queda corregido en el outline.
- **Pendiente de research en Vane** (si querés, te paso el prompt): cuál es el estado 2026 de las guías de entrevista sobre "complejidad amortizada" y si los entrevistadores de FAANG piden Θ además de O. No bloquea el módulo: es contexto.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
