# Módulo 1 — práctica (ejercicios 8.1 a 8.4)

Todo lo de acá se corre de verdad. Nada de "la respuesta es O(n)" sin medir.

```
practica/m1/
├── ejercicio-8.1.py       tabla de crecimiento + corrector de respuestas
├── respuestas-8.1.txt     mi respuesta de ejemplo (corregida OK)
├── java/
│   ├── Busqueda.java      ejercicio 8.3: lineal vs binaria, midiendo
│   ├── Bloques.java       ejercicio 8.2: los cinco bloques y su costo real
│   └── Duplicado.java     ejercicio 8.4: la pregunta de entrevista
└── RESULTADOS.md          este archivo
```

---

## 8.1 — La tabla, a mano

```
$ python3 ejercicio-8.1.py
Tabla de crecimiento para n = 1000

Complejidad         Operaciones
--------------------------------
O(1)                          1
O(log n)                     10
O(n)                      1,000
O(n log n)                9,966
O(n^2)                1,000,000

¿Cuántas veces más lento es O(n^2) que O(n log n)?
  1,000,000 / 9,966 = 100.3 veces

Para comparar, a n = 10.000 el mismo ratio es:
  100,000,000 / 132,877 = 752.6 veces
```

**El número que hay que retener: 100 veces a n=1.000, 752 veces a n=10.000.** El factor crece con n, y a escala de producción esa es la diferencia entre un servidor y setecientos.

Verificado con el corrector: `6 bien, 0 con problemas`. El corrector acepta 5% de tolerancia (la pregunta es de orden de magnitud: 10.000 y 9.966 son la misma respuesta, 1.000 no).

---

## 8.2 — Cinco bloques

`java/Bloques.java` corre los cinco y **mide** los tres que se pueden medir. Los resultados cambian la lectura ingenua:

| Bloque | Teoría | Medido | Dónde está la diferencia |
|---|---|---|---|
| A `getFirst` | O(1) | **3,2 ns/llamada** con 1.000.000 de llamadas (3,2 ms total) | Constante pura: el costo no depende de n ni del tamaño del array. |
| B `buscar` | O(n) peor | **0,17 ns/elemento** con n=1.000.000 (0,17 ms) | 0,17 ns por elemento es la CPU leyendo 4 bytes de una línea de 64 y adivinando el índice siguiente. |
| C `pares` | O(n²) | **n=1e6 → 5,00 × 10¹¹ iteraciones** | A 1 ns por iteración serían **500 s (0,14 h)** solo contando el loop vacío. Con dos accesos a array adentro, el costo real es mayor todavía. |
| D `fib` recursivo | O(2ⁿ) tiempo, O(n) espacio | **ratio 1,56 - 1,68 por paso** (medido con n de 32 a 38) | Es φ = 1,618, no 2. Ver abajo. |
| E `new int[n]` | O(n) tiempo, O(n) espacio | **0,30 ms** a n=1.000.000 | "Crear un array" se siente O(1): el runtime escribe 1.000.000 de ceros. |

### El conteo real del bloque C

```
n =   1.000  ->       499.500 pares   n²/2 =       499.500   ratio 0,4995
n =  10.000  ->    49.995.000 pares   n²/2 =    49.995.000   ratio 0,5000
n = 100.000  -> 4.999.950.000 pares   n²/2 = 4.999.950.000   ratio 0,5000
```

**El loop interno arranca en `i+1`, o sea corre n(n−1)/2 veces = exactamente la mitad de n².** Y en Big O eso sigue siendo O(n²), porque el ½ se tira. Ese es el punto exacto donde el video da el resultado pero no la regla: **el conteo real es n²/2, la notación es O(n²), y las dos cosas son ciertas.**

### El detalle de Fibonacci

`f(n) = f(n-1) + f(n-2)` recursivo: T(n) = T(n-1) + T(n-2) + O(1). La recurrencia tiene raíz φ = (1+√5)/2 ≈ 1,618, así que **T(n) ≈ φⁿ = 1,618ⁿ**, no 2ⁿ.

Medido, con n de 32 a 38, salto de 1:

```
fib(32)  3,879 ms
fib(33)  6,042 ms   x1,558
fib(34) 10,171 ms   x1,684
fib(35) 15,869 ms   x1,560
fib(36) 25,350 ms   x1,597
fib(37) 40,486 ms   x1,597
fib(38) 66,209 ms   x1,635
```

El ratio oscila alrededor de **1,6**, no de 2. 2ⁿ es la **cota superior** correcta (y por eso el video no está mal al decir 2ⁿ en Big O), pero el crecimiento real es el número áureo. Saber esa diferencia es gratis y te distingue.

**Y el espacio:** O(n) por la pila de llamadas, aunque el código no declare ni un array. Ese es el "espacio que se subestima" de la lección.

---

## 8.3 — La misma tarea, dos algoritmos (medido de verdad)

`java/Busqueda.java`. Los números reales de esta máquina (OpenJDK 27.0.1, Apple Silicon):

```
=== JIT (compilado) ===
         n    lineal (ms)   binaria (ms)      ns/elem    veces mas
      1000         0,0033       0,000321       3,2417           10x
     10000         0,0026       0,000040       0,2602           66x
    100000         0,0291       0,000110       0,2906          263x
   1000000         0,2039       0,000054       0,2039         3766x

=== INTERPRETE (-Xint, sin JIT) ===
         n    lineal (ms)   binaria (ms)      ns/elem    veces mas
      1000         0,0049       0,000137       4,8541           35x
     10000         0,0396       0,000173       3,9548          229x
    100000         0,4693       0,000210       4,6928         2231x
   1000000         4,6945       0,000252       4,6945        18625x
```

### Qué enseñan estos números, y por qué hubo que corregir el primer intento

**La primera versión del benchmark decía que la búsqueda lineal era casi O(1):** con n=100.000 tardaba lo mismo que con n=10.000, y con n=1.000.000 no crecía 10×. Lo primero que dice un buen instinto es "el benchmark está mal". Y estaba mal, en dos lugares:

1. **El loop se podía borrar.** El JIT demostró que la condición `if (acc == Integer.MIN_VALUE)` era siempre falsa y podía eliminar la suma entera — y con ella las llamadas. Se arregló con un `static volatile long sumidero`.
2. **El JIT vectoriza.** Con un array de enteros y comparación contra una constante, el compilador genera código SIMD: 4 u 8 elementos por instrucción. Ahí la lineal ya no es ~1 ns por elemento: es **0,2 ns**, y en n=1.000.000 recorre 4 MB a decenas de GB/s.

**La complejidad no cambió. Cambió la máquina.** Por eso el mismo programa corrido con `-Xint` (intérprete, sin JIT) sí muestra la forma: `ns/elem` plano en ~4,7 y `veces mas` creciendo de 35× a 18.625×.

### La lectura correcta

- **La columna `ns/elem` plana en el intérprete (4,85 → 3,95 → 4,69 → 4,69) es la firma de O(n).** El costo por elemento no crece con n.
- **La razón `veces mas` crece linealmente con n** — porque el lineal escala O(n) y el binario escala O(log n). A n=1.000.000 la diferencia es **18.625×** en el intérprete, y como log₂(1.000.000) ≈ 20, se esperaba ~1.000.000/20 = 50.000. El valor medido es **2,7× menor** que el teórico, y el motivo es medible: cada una de las 20 iteraciones de la binaria hace más trabajo por paso (`mid`, dos comparaciones, dos saltos) que una comparación de la lineal, que es un solo `if` sobre memoria contigua. La asintótica dice la forma; las constantes por operación dicen el número, y para n moderado **la constante todavía manda**.
- **La lección de método, que vale más que el número:** Big O predice la **forma**, el cronómetro mide la **máquina**. Cuando el cronómetro contradice la teoría, primero se sospecha del benchmark — y casi siempre tiene razón la teoría.

---

## 8.4 — La pregunta de entrevista

> "Esto está lento con 100.000 registros. ¿Por qué y cómo lo mejorarías?"

```java
boolean hayDuplicado(int[] a) {
    for (int i = 0; i < a.length; i++)
        for (int j = i + 1; j < a.length; j++)
            if (a[i] == a[j]) return true;
    return false;
}
```

### Respuesta, en tres frases

1. **La complejidad actual es O(n²).** El loop interno corre n(n−1)/2 veces y cada comparación es O(1): con 100.000 registros son ~5 mil millones de comparaciones, y por eso tarda.
2. **Un `HashSet` lo baja a O(n) promedio en tiempo.** Se recorre una sola vez, se pregunta "¿ya está?" en O(1) esperado y se inserta si no está: el primer duplicado corta la búsqueda.
3. **Se paga O(n) de espacio** (un set con hasta n elementos, ~16-48 bytes por entrada en Java), así que si el entrevistador restringe la memoria a O(1), esta respuesta no vale — y la alternativa es ordenar (`O(n log n)`, O(log n) si el sort es in-place) en lugar de hashear.

### Medido

`java/Duplicado.java`, peor caso de cada solución (array **sin** duplicado: se recorre entero):

```
         n   fuerza (ms)   hashset (ms)      sort (ms)    speedup
    10.000         7,5293        0,08958         0,0366        84x
   100.000       723,6633        0,31506         0,0788      2297x
   200.000      2953,9129        0,63674         0,0787      4639x

HashSet con 200.000 enteros: +12,6 MB de heap (~63 bytes/entrada)
```

**Los números cuentan la historia del módulo entero:**

- Duplicar n de 100.000 a 200.000 **multiplica el tiempo por 4,1** en la fuerza bruta (723 → 2.954 ms). Esa es la firma de O(n²), medida en la máquina.
- El hashset **multiplica por 2,0** (0,315 → 0,637 ms). Firma de O(n).
- El `sort` **multiplica por 1,0** (0,079 → 0,079 ms). Pero eso **no** es O(1): es que el array ya entra ordenado desde la primera iteración y `Arrays.sort` de primitivos es dual-pivot quicksort, que sobre datos ya ordenados es prácticamente lineal. Es un artefacto del benchmark, y anotarlo es la diferencia entre medir y creer que se midió.
- **El sort gana al hashset en los tres tamaños**, contrariamente a lo que la teoría ingenua sugiere. El motivo: `HashSet<Integer>` paga *boxing* (cada `int` se envuelve en un objeto `Integer`), `hashCode`, resolución de buckets y punteros sueltos que rompen la localidad de caché. `Arrays.sort` sobre `int[]` primitivo ordena memoria contigua sin un solo objeto. **La constante de la notación es 10× acá, y Big O no la ve.** Por eso "a misma complejidad, la estructura importa" no es un cliché.

### La respuesta de entrevista, completa

1. **O(n²)**: n(n−1)/2 comparaciones, ~5 × 10⁹ para 100.000 registros — 723 ms medidos.
2. **HashSet → O(n) promedio**, 0,3 ms medidos, 2.297× más rápido.
3. **Lo que se paga: +63 bytes por entrada** (12,6 MB para 200.000). Y si el array es grande de verdad, eso es lo que no entra.

**Pero la respuesta *correcta* en la entrevista es preguntar dos cosas:** ¿puedo mutar el array? y ¿hay límite de memoria? Porque si puedo mutar, `Arrays.sort` sobre `int[]` es **más rápido que el hashset y no pide memoria** — y esa solución es la que el 90% de los candidatos no da, porque va directo al hashset que memorizó.

**Regla que sale de esto:** *hashmap para O(1) promedio, array contiguo para la constante más baja.* El hashset gana en complejidad y pierde en rendimiento real más veces de las que uno cree.

---

## Lo que quedó aprendido (y no estaba en el video)

1. **Big O predice la forma; el cronómetro mide la máquina.** Y cuando no coinciden, el bug suele estar en el benchmark.
2. **Un benchmark sin `volatile` mide el loop que el JIT no borró**, no el algoritmo.
3. **El JIT vectoriza:** una lineal de 1.000.000 de int puede correr a 0,2 ns por elemento. La complejidad sigue siendo O(n); la constante se derrumbó.
4. **n²/2 sigue siendo O(n²).** Las constantes se tiran, y el conteo real del loop interno con `i+1` es exactamente la mitad.
5. **Fibonacci recursivo crece φⁿ ≈ 1,618ⁿ, no 2ⁿ.** 2ⁿ es la cota superior correcta; el número real es otro.
6. **"Pago O(n) de espacio" es mitad de la respuesta.** Sin eso, la solución del hashset es incompleta.
7. **A misma complejidad, la constante decide.** El hashset es O(n) y el sort O(n log n), y el sort gana: boxing y localidad de caché valen más que un exponente.
8. **Un benchmark puede mentir sin error de código.** El sort "medía" O(1) porque el input ya estaba ordenado. Verificar el supuesto del input es parte de medir.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
