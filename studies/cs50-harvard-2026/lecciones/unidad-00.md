# Unidad 0 — Scratch: el modelo mental

> **Duración en el curso:** 00:00:00 → 01:57:40 (Lecture 0).
> **Lo que tenés que poder hacer al terminar:** explicar por qué una computadora solo necesita ceros y unos, escribir un algoritmo en pseudocódigo, y ver en un programa de Scratch las mismas piezas que después aparecen en C, Python y SQL.
> **Prácticas ejecutables:** `practicas/u00/` — cinco scripts, todos en verde. Correr con `cd practicas/u00 && python3 test_practicas.py`.
> **Nota de método:** esto no es un resumen del video. El video es la fuente; esto es la clase *trabajada*: qué queda, qué hay que hacer, y dónde el curso se queda corto.

---

## 1. La premisa del curso (00:00:00 → 00:14:00)

Malan abre con el elefante en la habitación: la IA ya escribe código, y eso no vuelve obsoleta la clase.

La frase que lo sostiene: `«you still really need to understand the fundamentals»` (00:02:30). El argumento no es "la IA no sirve" ni "tenés que saberlo todo": es que **el cuello de botella nunca fueron las horas de tipeo, fueron las horas de decisión**. La IA comprime la segunda, no elimina la primera.

**Lo que esto significa operativamente, y el curso no lo dice:** un modelo te da diez soluciones plausibles. Elegir una exige saber qué es un puntero, qué es O(n log n), qué hace un `JOIN`. La IA no reemplaza el criterio; lo pone bajo presión.

**El pato de goma** (`«rubber duck»`, 00:11:41): verbalizar la confusión es ya depurar. Es el primer depurador, el más barato, y el que más se saltea. Cierra la lecture de IA (18:04) con la versión virtual: CS50 Duck es un pato que **no te da la respuesta**, te lleva a ella. Esa restricción es el diseño.

---

## 2. Todo es bits (00:15:00 → 00:40:00)

### El experimento de los dedos

Cinco dedos, tres valores por dedo: 7. Cinco dedos, **posición** por dedo: 31 (32 combinaciones menos la de "todo apagado").

```
unario:     1 dedo = 1, 2 dedos = 2      -> N dedos = N
posicional: 1 dedo = 1, 2 dedos = 3      -> N dedos = 2^N - 1
```

La diferencia no es la cantidad de dedos: es **darle significado a la posición**. El dedo de la izquierda vale más que el de la derecha.

Eso es todo el binario. `2^0 = 1`, `2^1 = 2`, `2^2 = 4`. El "por qué 31 y no 5" de las preguntas del outline queda respondido acá: porque no estás contando dedos, estás contando **patrones**.

### Por qué base 2 y no base 10

Esto es lo que el curso mejor enseña y lo que más se saltea al estudiar:

> Construir hardware con diez niveles de electricidad distintos se puede. Es difícil y caro. Distinguir **encendido de apagado** es trivial.

`«it's a nice simple world that way»` (00:22:41). El binario no es una preferencia matemática: es una consecuencia de qué es fácil de construir en silicio. La restricción física **eligió** la representación, no al revés. Esa idea reaparece en todo el curso: un hash table es más rápido porque es más fácil de indexar; un trie es rápido por la misma razón física.

### De número a letra

Una letra necesita **identidad como entero** (00:29:00). `A` = 65, `a` = 97, `!` = 33. Eso es ASCII, y el curso lo hace con la audiencia levantando manos en tres rondas: el "programa" es humano, las manos son bits.

El ejercicio mental que vale: **"hi!"** son 72, 73, 33 - tres bytes, 24 bits. Si escribís un mensaje, estás mandando números. No hay magia.

### De letra a imagen

RGB: tres bytes por píxel. Un cuadrado de 3 píxeles es 9 bytes. Una foto de 1600×900 son 1600 × 900 × 3 = **4.320.000 bytes** = 4,1 MB crudos. El JPEG es un acuerdo sobre qué *no* guardar.

**Y acá está el primer ancla al repo:** un BMP es exactamente eso, un array de bytes con un encabezado. En la Unidad 4 (Memory) vas a invertirle los colores a mano. Si hoy no entendiste el "todo es un array de bytes", ahí se cierra.

---

## 3. Algoritmo, no programa (00:45:00 → 01:10:00)

### El problema de la guía telefónica

Malan busca "John Harvard" de tres formas; la tercera es binaria (abrir al medio, ir a un lado, repetir). Y ahí viene la frase clave:

`«It's not just about writing correct code or getting the job done, but doing it well and doing it quickly»` (01:00:15).

Tres algoritmos que **dan el mismo resultado** y no son equivalentes. Esa es la primera vez en el curso -y en la vida de casi cualquiera- que "funciona" deja de ser el criterio.

### Pseudocódigo (00:65:00)

`«pseudo code is not one formal thing»` (01:05:07). No hay sintaxis, no hay intérprete, no hay compilador. Es **el algoritmo escrito para una persona**, y por eso no es un lenguaje: no tiene un ejecutor que le diga a vos si está bien.

Esto responde la tercera pregunta del outline con un matiz que el curso no hace explícito: pseudocódigo **sí es un lenguaje** en el sentido de que comunica, pero **no es un lenguaje de programación** porque no se puede ejecutar. La distinción no es de prestigio: es de verificación. Un algoritmo en pseudocódigo no se puede testear.

---

## 4. Scratch: las piezas del oficio (01:10:00 → 01:57:40)

El curso dedica cuarenta y cinco minutos a arrastrar bloques. Se siente lento y es el punto: **Scratch es C sin el compilador**, y ver los bloques antes de las llaves hace explícitas las piezas.

| Pieza de Scratch | En C | En Python | En SQL |
|---|---|---|---|
| `say` (decir) | `printf` | `print()` | `SELECT` (devuelve filas) |
| variable | `int x = 0;` | `x = 0` | columna |
| `if / else` | `if (...) {} else {}` | `if: else:` | `WHERE` |
| `repeat N` | `for (int i=0; i<N; i++)` | `for i in range(N):` | - |
| `forever` | `while (1)` | `while True:` | - |
| bloque propio (función) | `void foo(void) {}` | `def foo():` | vista / CTE |
| bandera verde (evento) | `int main(void)` | `if __name__` | `ON CONFLICT` |
| argumento | parámetro | parámetro | - |
| valor de retorno | `return` | `return` | - |

El curso insiste en los **indentados** y las **llaves** (`«just like in Scratch the say is sort of indented»`, 02:55:01). No es estética: es que la computadora no ve el formato, ve el alcance. Scratch te enseña el alcance **antes** de enseñarte la sintaxis que lo esconde.

### Lo que la demo de Scratch enseña de verdad

Tres programas, en orden:

1. **Hablar** (77:30 → 80:00): un bloque, un side effect. La computadora no "piensa", ejecuta.
2. **Preguntar y responder** (80:00): `ask` + `answer`. La variable sin nombre es el "por qué existe la variable".
3. **La canción del hambre** (90:00): tres bloques idénticos pegados, después refactorizados en `repeat` + `wait`. Esto es **el primer refactor del curso** y no lo nombra: es "tres cosas iguales" → "un bucle". Y la primera vez que te dice que copiar y pegar algo tres veces debería darte mala espina (16:33, en la unidad de SQL, lo dirá explícitamente).

Y el juego final (`Oscar`, 105:00): un sprite que cambia de traje cuando el mouse está encima. Es **un estado** (tocando sí/no) que dispara **una transición** (traje abierto/cerrado). Eso es, literalmente, una máquina de estados de dos estados. La vas a volver a ver en Flask (U9) como sesión y en SQL (U7) como transacción.

---

## 5. Lo que el curso no dice en esta unidad

Tres huecos que el video deja abiertos y que vas a necesitar:

**1. Scratch no enseña a depurar.** Malan muestra programas que funcionan. Nunca muestra un bloque mal puesto. **Depurar es el 80% del trabajo**, y la Unidad 0 no lo cubre. Lo vas a aprender en la Unidad 2 (`debug50`, `valgrind`) - pero entre hoy y entonces, no tenés el hábito.

**2. Unicidad del Unicode no aparece.** ASCII es 7 bits (128 caracteres). Unicode es más de 150.000, de ancho variable. `á` en UTF-8 son **dos bytes**, no uno. El curso lo menciona de pasada y no lo ejercita; el primer bug real de strings en C (U2) va a venir de ahí.

**3. Nada de versionado.** El curso abstrae git detrás de `check50`. En la Unidad 10 Malan mismo lo dice: *"en CS50 abstraemos git"*. Si venís de este curso y no sabés `git`, te falta una pieza que ninguna otra unidad da.

---

## 6. Ejercicios de la unidad

**Todos resueltos y ejecutables** en `practicas/u00/`. La respuesta de papel está en el script; la verificación también.

```bash
cd studies/cs50-harvard-2026/practicas/u00
python3 test_practicas.py    # 18 checks, 0 fallos
```

### 6.1 — Binario a mano (15 min) → `e1_binario.py`

Sin calculadora ni computadora, escribí:

| Decimal | Binario (8 bits) |
|---|---|
| 1 | |
| 7 | |
| 65 | |
| 128 | |
| 255 | |

Y respondé: **¿por qué 255 y no 256 con 8 bits?** (Malan lo responde en el quiz final del curso, 24:17:08: porque se empieza a contar desde el cero y eso consume una combinación. Ese es el mismo motivo por el que un array de `n` elementos va de `0` a `n-1`.)

### 6.2 — ASCII a mano (10 min) → `e2_ascii.py`

Decodificá estos tres bytes: `72`, `73`, `33`. Después decodificá `104`, `105`, `33`. ¿Qué te dice la diferencia de 32 entre mayúscula y minúscula sobre la tabla?

<details><summary>Respuesta</summary>

72=`H`, 73=`I`, 33=`!` → **HI!**
104=`h`, 105=`i`, 33=`!` → **hi!**

La diferencia mayúscula/minúscula es exactamente 32 (`a`=97, `A`=65). Y 32 es `2^5`, un solo bit. Eso significa que en ASCII **cambiar mayúscula a minúscula es tocar un bit**, y por eso `toLower()` es tan barato. No todas las tablas de caracteres tienen esa propiedad; ASCII la tiene por diseño.

</details>

### 6.3 — El ejercicio del outline: ordernar 8 cartas en pseudocódigo (30 min) → `e3_cartas.py`

> **Corrido:** `python3 e3_cartas.py --shuffle-seed 42` → `[11, 2, 1, 5, 4, 9, 12, 6]` queda en `[1, 2, 4, 5, 6, 9, 11, 12]` con **4 intercambios** y **28 comparaciones** (n(n-1)/2). El script imprime el pseudocódigo, cada vuelta y el total.

Ocho cartas boca arriba. Escribí los pasos para ordenarlas de menor a mayor, **en castellano**, sin buscar C, Python ni SQL.

Restricciones:
- No podés usar "ordenar" como paso. Si tu algoritmo dice "ordenar las cartas", no hiciste nada.
- Cada paso tiene que ser algo que una persona con dos manos pueda hacer sin pensar.

Guardalo en un archivo. En la Unidad 3 (Algorithms) se va a llamar **selection sort** o **bubble sort**, y vas a poder comparar tu versión con la de Malan. **La diferencia que encuentres es la lección de esa unidad.**

<details><summary>Un esqueleto de respuesta (no la única)</summary>

```
para cada posición i de 0 a 7:
    buscar la carta más chica entre i y 7
    recordar su posición
    intercambiar la carta de i con la de esa posición
```

Esto es selection sort. Va a ser O(n²) en la Unidad 3.

</details>

### 6.4 — Ancla al repo (20 min) → `e4_bytes.py`

> **Medido en esta máquina:** `'á'` → `c3 a1`, **2 bytes** en UTF-8 y **1 byte** en Latin-1. `'canción'` → **7 caracteres, 8 bytes**. Un programa en C que cuente bytes va a decir 8. Ese es el bug de la U2, ya medido.

La idea del curso es **"todo es un array de bytes"**. Verificalo en tu propia máquina:

```bash
printf 'hi!' | xxd
```

Deberías ver `68 69 21` y el final de línea `0a`. Ahora:

```bash
printf 'hi!' | wc -c
```

Tres bytes (sin contar el `\n` que agrega `printf`). Si hiciste bien 6.2, sabés exactamente qué estás mirando.

Después, la parte que importa: **¿qué pasa con un carácter fuera de ASCII?**

```bash
printf 'á' | xxd
printf 'á' | wc -c
```

Vas a ver **dos bytes** (`c3 a1`), no uno. Ese es el hueco del punto 5.2, medido en tu terminal en dos comandos. Cuando en la Unidad 2 escribas un programa en C que cuente caracteres de un string, va a contar **bytes**, no caracteres. Vas a tener el bug antes de que la clase te lo enseñe.

---

## 7. Preguntas de la unidad

1. ¿Por qué cinco dedos dan 31 valores y no 5? ¿Qué cambió?
2. ¿Por qué las computadoras usan base 2 y no base 10? La respuesta no es "porque sí".
3. `A` = 65 y `a` = 97. ¿Cuántos bits los separan? ¿Qué implica eso?
4. ¿Por qué el curso usa Scratch en la semana 0 y no C?
5. ¿Pseudocódigo es un lenguaje? Contestá las dos versiones: en qué sentido sí y en qué sentido no.
6. Tres algoritmos dan el mismo resultado en la búsqueda de la guía telefónica. ¿Cuál fue el criterio para preferir uno?
7. Un mensaje de 100 palabras, promedio 5 letras por palabra. ¿Cuántos bytes viajan, como mínimo, en ASCII? ¿Y si fuera UTF-8 con acentos?
8. El "todo es un array de bytes" ¿cómo explica que un JPEG ocupe menos que un BMP?

<details><summary>Respuestas breves</summary>

1. Porque se le da significado a la **posición** (ponderación), no al índice. 2^5 = 32 combinaciones, menos la de todo apagado.
2. Distinguir on/off es trivial en hardware; distinguir diez niveles no. La restricción física eligió la base.
3. 32 bits = 2^5 = un solo bit. Cambiar caja es barato - y por eso el `toLower()` de la Unidad 2 no es magia.
4. Porque Scratch hace **visible** el alcance y las piezas (bloques anidados) antes de que la sintaxis de C lo esconda detrás de llaves e indentación.
5. Sí: comunica a un humano. No: no hay ejecutor que verifique.
6. La eficiencia: cuántos pasos da en el peor caso. "Funciona" dejó de ser el único criterio.
7. 100 × 5 × 8 = 4.000 bits = 500 bytes. Con acentos, depende de UTF-8: más bytes por carácter, y **no un número fijo**.
8. JPEG es un acuerdo sobre qué se puede perder sin que el ojo lo note. BMP dice todo. Ambos son arrays de bytes; uno es más honesto y mucho más grande.

</details>

---

## 8. Checklist de la unidad

- [x] Puedo convertir 1, 7, 65, 128, 255 a binario sin calculadora.
- [x] Sé explicar por qué 255 y no 256 con 8 bits.
- [x] Sé decodificar "hi!" a mano desde ASCII.
- [x] Escribí el algoritmo de las 8 cartas sin usar "ordenar" como paso.
- [x] Corrí `printf 'á' | xxd` y sé qué significa `c3 a1`.
- [x] Puedo decir, sin leer, tres cosas que el curso **no** enseña en esta unidad.
- [x] Los cinco scripts de `practicas/u00/` corren con `EXIT 0`.
- [x] El test del algoritmo **roto** falla: el test prueba algo.

Cuando las ocho estén tildadas, la Unidad 1 (C) te va a parecer fácil: es Scratch con llaves.

---

_Sesión de estudio 2026-11-11. Fuente de las citas: `transcripcion.md` (00:00:00 → 01:57:40). El ejercicio 6.1 es inventado para la clase; los 6.3 y 6.4 salen del outline del curso._

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
