# CS50 2026 — Outline de estudio

**Fuente:** [Harvard CS50 (2026) – Full Computer Science University Course](https://www.youtube.com/watch?v=gmuTjeQUbTM) · freeCodeCamp.org · David J. Malan · 24:29:14 · CC BY-NC-SA 4.0.

**Cómo usar este outline.** La duración es el problema: son 24 horas de clase en vivo, con demos, preguntas del público y pausas. No se ve de corrido ni se resume: se estudia **por unidad**, cada una con su artefacto de salida. Las nueve unidades no son acumulativas en el mismo sentido que un curso de programación normal - cada una introduce un lenguaje o una capa nueva (Scratch → C → Python → SQL → JS → Flask) y el hilo conductor es el mismo problema (un *phone book*, un *speller*, una app web) resuelto con herramientas cada vez más abstractas.

**Lo que el curso NO es.** No enseña a construir un sistema: no hay testing, no hay deploy, no hay observabilidad, no hay trabajo en equipo sobre un repo. Enseña a *pensar* y a *leer y escribir* código; la ingeniería de software real queda afuera. Tampoco es la versión con los problem sets oficiales: los ejercicios de este outline son derivados, no los de `cs50.harvard.edu/x`.

**Requisito de hardware.** Todo lo de C requiere un entorno con `clang`, `make` y `valgrind`. En la Mac mini: `brew install clang-format` no alcanza - hace falta `Xcode Command Line Tools` (`xcode-select --install`) y `valgrind` **no corre en Apple Silicon** (usar `CS50` en la nube, Docker `cs50/cli`, o `AddressSanitizer` con `-fsanitize=address`).

---

## Unidad 0 — Scratch: el modelo mental (00:00:00 → 01:57:40)

**Objetivo:** entender qué es un algoritmo antes de tocar un compilador. Scratch es la excusa; lo que queda son las piezas (función, argumento, valor de retorno, variable, bucle, condicional, evento) que reaparecen en los once lenguajes siguientes.

**Bloques:**
- La premisa del curso y el elefante en la habitación: la IA cambia cómo se escribe código, no qué se quiere resolver. `«If you want to learn about computer science and the art of programming, this course is where to start.»` (00:00:00)
- El pato de goma y CS50 Duck (`«rubber duck»`, 00:11:41): verbalizar la confusión es el primer depurador. Es la semilla de la lecture de IA.
- Unario → binario (`«what I started to do there is something called base 2»`, 00:16:36): contar con dedos como sistema de pesos posicionales.
- Representación: ASCII, Unicode, RGB, y la idea de que **todo es bits**.
- Pseudocódigo (`«pseudo code is not one formal thing»`, 01:05:07) - el puente entre idea y código.
- Scratch como implementación de todo lo anterior (`«languages like Scratch, which we'll»`, 00:02:52).

**Ejercicio:** escribir en pseudocódigo el algoritmo de ordenar 8 cartas de menor a mayor, sin mirar los lenguajes. Guardarlo: se reescribe en C, Python y SQL en las unidades siguientes, y la diferencia entre las cuatro versiones es el contenido real del curso.

**Preguntas:** ¿por qué 32 combinaciones con 5 dedos y no 5? · ¿qué diferencia hay entre abstracción y ofuscación? · ¿por qué pseudocódigo no es un lenguaje?

---

## Unidad 1 — C: el primer contacto con la máquina (01:57:40 → 04:27:58)

**Objetivo:** bajar un nivel. El compilador, el `make`, los tipos, y el primer bug que importa (overflow).

**Bloques:**
- La meta del curso en una frase: `«fire hose, such as that picture here»` (01:59:05) - la sensación de estar bajo un chorro de agua es esperada, no un fracaso personal.
- Qué hace un compilador (`«is called a compiler»`, 02:02:22) y `clang` en la práctica (`«clang spacehello.c»`, 05:10:17).
- `cs50.h` y `get_string` (`«Get string. A string in»`, 02:28:43): la librería del curso esconde `scanf` a propósito; entender qué esconde es el punto del final de la unidad.
- Tipos, booleanos y condicionales; `if/else` como el mismo bloque de Scratch con otra sintaxis (`«just like in Scratch the say is sort of indented»`, 02:55:01).
- **Overflow**: `«overflow is a term of art whereby you can overflow an integer»` (04:17:27). Es el primer ejemplo de que el modelo mental (matemática) y la máquina (32 bits) no coinciden.

**Ejercicio:** reescribir el algoritmo de orden de la Unidad 0 en C, con `get_string` primero y con `scanf` después. Correr `make` sobre los dos y comparar. Después provocar el overflow de un `int` en un bucle y ver el signo cambiar.

**Preguntas:** ¿qué oculta `cs50.h`? · ¿por qué `make` y no `clang` directo? · ¿por qué el overflow no lanza un error?

---

## Unidad 2 — Arrays (04:27:58 → 06:53:32)

**Objetivo:** memoria contigua, strings como arrays de `char`, y el primer `valgrind`.

**Bloques:**
- Arrays y la indexación (`«how do I index into the array at»`, 05:45:48): el índice es aritmética de punteros disfrazada, aunque todavía no se diga.
- Strings en C: `char *` sin longitud incorporada, el `\0` como terminador.
- Command-line arguments (`argc`/`argv`): el primer programa que no le pide nada al usuario, lo recibe del sistema.
- Cifrado (Caesar, `crypt`): el problema canónico de la unidad, y el primero con una respuesta "correcta" falsificable.
- Debugging con `debug50` y `valgrind` (`«going to then do Valgrind space»`, 10:10:41): el curso introduce la herramienta antes de que el alumno la necesite.

**Ejercicio:** un programa que reciba un texto por `argv` y devuelva su cifrado César con la clave en un segundo argumento. Debe rechazar argumentos inválidos con código de salida ≠ 0. Verificarlo con `echo $?`.

**Preguntas:** ¿por qué `argv[0]` es el nombre del programa? · ¿qué pasa si no hay `\0`? · ¿qué cuenta `valgrind` que no cuenta un test?

---

## Unidad 3 — Algorithms (06:53:32 → 08:53:07)

**Objetivo:** la única unidad que es matemática aplicada. Búsqueda, orden y la notación que permite hablar de ambas sin medir.

**Bloques:**
- Búsqueda lineal y binaria (`«algorithms known as linear search»`, 07:13:03; `«binary search, as we call that»`, 07:16:53).
- Notación Big O (`«to use what's called big O notation»`, 07:22:14) y Omega/Theta (`«Omega, a capital omega symbol here»`, 07:29:30): O es cota superior, Omega inferior, Theta ambas.
- Orden: bubble, selection (`«selection sort, whereby on each»`, 08:03:08), merge (`«Merge sort is really all three of these»`, 08:42:35).
- Recursión (`«Recursion is a technique in mathematics»`, 08:22:57) - y por qué el dibujo de los algoritmos ordenando (la animación de la apertura) es el mejor material del curso para entender merge sort.

**Ejercicio:** implementar los tres ordenamientos en Python (por velocidad de iteración) y medir con `time` sobre 10.000 enteros aleatorios. La tabla de tiempos debe reproducir el orden O(n²), O(n²), O(n log n). Si no lo reproduce, el merge sort está mal.

**Preguntas:** ¿por qué binary search necesita orden previo? · ¿cuándo conviene un O(n²) sobre un O(n log n)? · ¿por qué la notación ignora constantes y eso puede mentir?

---

## Unidad 4 — Memory (08:53:07 → 11:13:02)

**Objetivo:** la unidad más difícil del curso y la que más se recuerda. Punteros, `malloc`, archivos.

**Bloques:**
- Hexadecimal (`«digits, aka base 16»`, 09:00:03; el prefijo `0x` en 09:06:15): la notación que hace legible una dirección.
- Direcciones de memoria (`«is to just get the address of a variable»`, 09:09:22) y punteros (`«today more so than ever might feel like a bit of a fire hose»`, 09:11:21 - Malan lo dice explícitamente de *esta* clase).
- `malloc`/`free`, y el `valgrind` de la unidad anterior como detector de fugas.
- File I/O: `fopen`/`fread`/`fwrite`, JPEG y BMP como formatos leídos byte a byte.
- `swap` con y sin punteros: el ejemplo que hace caer la ficha.

**Ejercicio:** un programa que lea un BMP, invierta sus colores y escriba un archivo nuevo. Después correrlo con `valgrind` y con `-fsanitize=address` (en macOS, porque `valgrind` no corre en Apple Silicon) y comparar qué reporta cada uno. **Este es el ejercicio de hardware de la clase.**

**Preguntas:** ¿por qué `malloc` puede devolver `NULL` y casi nadie lo chequea? · ¿qué es un puntero a puntero y cuándo el curso lo usa? · ¿por qué un archivo es apenas un array de bytes?

---

## Unidad 5 — Data Structures (11:13:02 → 13:19:15)

**Objetivo:** pasar de "un array" a "la estructura correcta para el acceso que necesitás". Es la antesala del speller, el problem set más famoso de CS50.

**Bloques:**
- Listas enlazadas (`«So, a linked list is»`, 11:49:44) y `node` (`«A node is just a generic»`, 11:51:44).
- Diccionarios y tablas hash (`«So-called hash table»`, 13:03:24): el tradeoff entre memoria y tiempo, en vivo.
- Tries: la estructura que gana el speller, y la razón por la que gana.
- Colas y pilas (`«a stack. When he reached for something»`, 11:15:40).

**Ejercicio:** el speller completo (dictionary + load + check + unload) con las cuatro estructuras, midiendo tiempo de carga y de búsqueda sobre un diccionario real. La tabla de los cuatro tiempos es el entregable; el código es medio.

**Preguntas:** ¿cuándo una hash table es peor que un array? · ¿por qué el trie gana en el speller y por qué no sirve siempre? · ¿qué tradeoff esconde "O(1) promedio"?

---

## Unidad 6 — Python (13:19:15 → 15:48:46)

**Objetivo:** la misma clase de problemas, en un lenguaje que hace el trabajo sucio. Se lee rápido y se olvida rápido si no se contrasta con C.

**Bloques:**
- Interpretado vs compilado (`«Python being»` / interpreter, 13:21:10): por qué el mismo código corre sin `make`.
- Las estructuras de C convertidas en nativas: listas, dicts, sets.
- Librerías: `csv` (`«CSV stands for commaepparated values»`, 10:57:31 - dicho en la unidad de Memoria, aplicado acá), `Pillow`, reconocimiento facial.
- `pip` y el ecosistema.

**Ejercicio:** tomar el phonebook de CSV de la Unidad 4 y reescribirlo en Python usando `csv.DictReader`. Después comparar líneas de código y tiempo de ejecución. La conclusión esperada -"Python gana en expresividad, pierde en velocidad"- hay que **medirla**, no asumirla.

**Preguntas:** ¿qué paga Python por ser interpretado? · ¿cuándo el GIL importa de verdad? · ¿por qué el curso enseña C *antes* de Python?

---

## Unidad 7 — SQL (15:48:46 → 18:04:19)

**Objetivo:** el tercer paradigma. C y Python dicen *cómo*; SQL dice *qué*. Es la unidad más directamente aplicable al trabajo diario.

**Bloques:**
- SQL como lenguaje declarativo (`«SQL as we'll see is a different sort of programming language»`).
- `SELECT` (16:14:47) y el modelo relacional: tablas, filas, columnas - y por qué la tabla "ancha" de la demo se vuelve inmanejable (`«it just feels like it's going to get messy»`).
- `JOIN` (16:58:59) y normalización.
- Índices (16:07:45) y por qué una consulta rápida puede serlo por el índice y no por la consulta.
- **Inyección SQL** (17:47:28): el mismo `--` que comenta en SQL, usado como arma. Es la primera vez en el curso que un concepto de seguridad aparece con un exploit en vivo.
- SQLite frente a MySQL/Postgres: el curso usa SQLite porque no hay servidor que levantar.

**Ejercicio:** reproducir la inyección de la clase (`' OR 1=1 --`) sobre una base SQLite propia, y después escribir la versión parametrizada. Verificar con `EXPLAIN QUERY PLAN` que un índice cambia el plan. **Es la unidad con más valor inmediato para el workspace.**

**Preguntas:** ¿por qué el parámetro y no el escape de comillas? · ¿qué decide el planner de SQLite? · ¿cuándo denormalizar es correcto?

---

## Unidad IA — Artificial Intelligence (18:04:19 → 18:52:07)

**Objetivo:** la clase más corta y la más fechada. Es una introducción conceptual, no práctica.

**Bloques:**
- El pato de goma virtualizado (`«we sort of virtualized that rubber duck»`, 18:06:00) y CS50 Duck como tutor.
- IA generativa a grandes rasgos (`«generative artificial intelligence»`, 18:07:21).
- Árboles de decisión (`«decision trees are a»`, 18:25:11): el puente con la búsqueda de la Unidad 3.
- LLMs (`«large language models»`, 18:43:02) y **alucinaciones** (`«we'll call lastly hallucinations»`, 18:50:34).
- Final projects y el cierre de la clase (`«get to your final projects»`, 18:15:31).

**Ejercicio:** ninguno de código - la unidad no lo pide. El ejercicio es de criterio: leer la sección de alucinaciones y escribir cinco preguntas que un LLM respondería con seguridad y sin evidencia, y cómo detectarlo.

**Preguntas:** ¿qué diferencia un árbol de decisión de un prompt? · ¿por qué la alucinación es un problema de diseño y no solo de modelo? · ¿qué significa "tutor" en el pato virtual y qué no?

---

## Unidad 8 — HTML, CSS, JavaScript (18:52:07 → 21:14:19)

**Objetivo:** el navegador como plataforma. La primera vez en el curso que el output es algo que se ve.

**Bloques:**
- HTML como estructura, CSS como presentación (`«a language called CSS which»`, 18:53:32), JS como comportamiento.
- HTTP (`«dive in then to this acronym HTTP»`, 19:14:18): request, response, métodos, códigos.
- El DOM (`«document object model or DOM for short»`, 20:45:12) y `document.querySelector` (20:50:06): el navegador ya implementó un árbol para vos, la misma idea que el trie de la Unidad 5.
- JS como lenguaje de eventos: callbacks, asincronía.

**Ejercicio:** un formulario HTML + CSS + JS que valide el input en el cliente **y** en un servidor mínimo; después desactivar JS y ver qué se rompe. Es la diferencia entre "funciona para mí" y "funciona".

**Preguntas:** ¿por qué validar en el cliente no alcanza? · ¿qué es el DOM que SQL no tiene? · ¿por qué el curso deja React para afuera?

---

## Unidad 9 — Flask (21:14:19 → 23:40:54)

**Objetivo:** juntar todo. Una app web con base de datos, sesiones y API - las mismas piezas que una app real, sin las herramientas de producción.

**Bloques:**
- Flask y rutas (`«to use something called flask»`, 21:19:14): el framework mínimo para que la app sea una app.
- Jinja (`«The people who came up with ginger used»`, 21:53:12): templates server-side, el contrapunto del DOM.
- Cookies y sesiones (`«planting a cookie on your computer»`, 23:12:36; `«called sessions»`, 23:16:09): estado sin base de datos, y por qué la cookie no puede tener el contenido.
- APIs (`«creating essentially my own API»`, 23:34:56): devolver JSON en vez de HTML.
- El formulario con CSRF - el punto donde el curso muestra que la seguridad no es opcional.

**Ejercicio:** una app de phonebook con Flask + SQLite: un formulario que cree un contacto, una lista que lo muestre, una ruta `/api/contacts` que devuelva JSON. Sin CSRF primero, con CSRF después. **Este es el entregable integrador de todo el curso.**

**Preguntas:** ¿qué agrega Flask sobre Python puro? · ¿por qué la sesión en cookie firmada y no en la base? · ¿qué falta acá para que esto sea producción? (La pregunta importa: falta casi todo, y el curso no lo cubre.)

---

## Unidad 10 — The End (23:40:54 → 24:29:14)

**Objetivo:** el cierre. No enseña nada nuevo; ordena lo aprendido y explica qué sigue.

**Bloques:**
- De "menos cómodo" a "más cómodo" (`«if you started the class among those less comfortable»`, 23:42:00): el eje de la clase es la comodidad, no la nota.
- Final projects (`«taken into account come final projects»`, 23:42:24).
- El repaso por los once lenguajes y el argumento de que la diferencia entre ellos es de modelo mental, no de sintaxis.

**Ejercicio:** sin ejercicio. El curso se cierra con la Unidad 9.

---

## Banco de preguntas

1. ¿Qué oculta `cs50.h` y qué se aprende al verlo por dentro?
2. Un `int` de 32 bits y un `long` de 64: ¿cuándo el segundo no alcanza tampoco?
3. ¿Por qué `valgrind` no corre en Apple Silicon y qué lo reemplaza?
4. Explicá con un ejemplo por qué `O(n log n)` puede perder contra `O(n²)`.
5. ¿Qué significa que un puntero sea un número y por qué eso no es una simplificación?
6. ¿Cuál es la diferencia entre una lista enlazada y un array en términos de qué operación se vuelve caras?
7. ¿Por qué el trie gana el speller y por qué no se usa para todo?
8. ¿Qué gana y qué pierde Python frente a C, medido y no asumido?
9. ¿Por qué `SELECT *` en una tabla con columnas opcionales es un smell de diseño?
10. `JOIN` vs `IN`: ¿cuándo preferirías el segundo?
11. Reproducí una inyección SQL y escribí su fix parametrizado. ¿Por qué el escape no es la respuesta?
12. ¿Qué hace el DOM que SQL no hace y por qué son la misma idea de árbol?
13. ¿Qué diferencia a un árbol de decisión de un prompt de LLM?
14. ¿Por qué la alucinación de un LLM es un problema de producto y no solo de modelo?
15. ¿Por qué validar en el cliente no alcanza?
16. ¿Qué agrega Flask sobre Python puro, y qué no agrega?
17. Sesión en cookie firmada vs sesión en base de datos: qué ataca cada una.
18. ¿Qué le falta a la app de la Unidad 9 para ser producción? Nombrá cinco cosas.
19. ¿Por qué el curso enseña C antes de Python?
20. El hilo del phone book: reescribílo en C, Python, SQL y Flask, y decí qué aprendiste en cada salto que la sintaxis no explica.

---

## Lo que el curso NO cubre

- **Testing:** el curso no escribe un solo test automatizado. Ni unitario, ni de integración. Los "checks" de CS50 son externos (`check50`), no enseñados.
- **Deploy:** la app de Flask corre en `localhost` y no se despliega en ninguna parte.
- **Git y colaboración:** no se ve `git`, `git merge`, ni cómo se trabaja sobre un repo con otra gente.
- **Observabilidad:** logs, métricas, trazas: no aparecen.
- **Gestión de dependencias seria:** `pip` sí, lockfiles y entornos reproducibles no.
- **Seguridad como disciplina:** aparece un *exploit* en vivo (SQL injection, CSRF) pero no un modelo de amenazas.
- **Accesibilidad:** nada de a11y en la unidad web. Para el trabajo de Gonzo con CPACC esto es un hueco, no un detalle.

El hueco más relevante para este workspace: **el curso enseña a escribir código que hace lo que el autor quiso, no código que otro pueda verificar.** Todo lo que el workspace tiene de gates, ADRs y verificación cubre exactamente lo que acá no se enseña.

---

_Clase montada 2026-11-11. Transcript: `transcripcion.md`. Fuente de verdad del mapa temporal: la descripción oficial del video (12 capítulos 1:1)._

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
