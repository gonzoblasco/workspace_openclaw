# Clase: Harvard CS50's Intro to Databases with SQL

- **Fuente:** https://www.youtube.com/watch?v=WXk7yDqsKxs (playlist `WL`, Watch Later)
- **Canal:** freeCodeCamp.org
- **Curso original:** [CS50's Introduction to Databases with SQL](https://cs50.harvard.edu/sql/) (Harvard University)
- **Expositor:** Carter Zenke, con introducción de David J. Malan
- **Publicado:** 2025-10-09 · **Duración:** 11:08:48 (40.128 s)
- **Idioma:** inglés · **Transcript:** `transcripcion.md` (subtítulos automáticos `en-orig`, 14.819 cues, ~107.654 palabras, timestamps `[hh:mm:ss]`, cobertura verificada: último cue 11:08:36)
- **Motores:** SQLite (el curso completo), PostgreSQL (`psql`, última clase) y MySQL (una clase completa)
- **Clase creada:** 2026-11-12

> **Nota de escala.** Son once horas: no se consume de una sentada, se estudia por módulo. Este outline es un mapa para navegar el video y un currículum para ejercitar, no un resumen que lo reemplace. Cada módulo dice dónde está, qué enseña, qué tenés que poder hacer al cerrarlo y qué ejercicios lo prueban.

## Tesis de la clase

**SQL no se aprende por sintaxis: se aprende en el orden en que crece un problema real de datos.** El curso sigue una sola línea narrativa de seis semanas — *una tabla* → *varias tablas* → *diseñar el esquema* → *escribir datos* → *verlos de otra forma* → *hacerlos rápidos* → *hacerlos grandes* — y cada semana arranca desde la base de la semana anterior, no desde cero. La segunda mitad (Writing, Viewing, Optimizing, Scaling) deja de ser un curso de consultas y se convierte en un curso de ingeniería de datos: transacciones, triggers, índices con plan de ejecución, réplica y sharding.

La segunda tesis, más sutil y la que más se repite en las preguntas del público: **cada herramienta es un trade-off explícito, no una buena práctica.** Un índice compra velocidad con disco; una vista compra legibilidad con riesgo; una transacción compra consistencia con concurrencia; la normalización compra ausencia de redundancia con joins. El curso nunca dice "usá X", dice *qué pagás* por X.

## Resultado esperado

Al terminar la clase se puede:

1. **Distinguir una base de datos de una planilla** por las razones que da el curso (escala, tipos, relación entre tablas) y elegir un DBMS (SQLite, MySQL, PostgreSQL) por su costo operativo, no por moda.
2. **Consultar una tabla** con `SELECT`, `WHERE`, operadores (`=`, `!=`, `<`, `>`, `AND`, `OR`, `NOT`), `BETWEEN`, `LIKE` con `%` y `_`, `ORDER BY … ASC/DESC`, `LIMIT` y `DISTINCT`, entendiendo qué devuelve cada uno y cuándo el motor no puede usar un índice.
3. **Tratar `NULL` como ausencia de valor**, nunca como cero o cadena vacía, y usar `IS NULL` / `IS NOT NULL` para encontrarla.
4. **Agregar filas con funciones de agregación** (`COUNT`, `AVG`, `SUM`, `MIN`, `MAX`, `ROUND`) y agrupar con `GROUP BY` + `HAVING`, sabiendo que `HAVING` filtra después de agregar y `WHERE` antes.
5. **Relacionar tablas** con claves primarias y foráneas, distinguir uno-a-uno, uno-a-muchos y muchos-a-muchos, y elegir entre `INNER`, `LEFT`, `RIGHT` y `FULL JOIN` por qué filas querés conservar.
6. **Combinar resultados** con `UNION` (y su variante con duplicados), `INTERSECT` y `EXCEPT`.
7. **Diseñar un esquema** con `CREATE TABLE`, tipos y afinidades de SQLite, y las cuatro *column constraints* (`CHECK`, `DEFAULT`, `NOT NULL`, `UNIQUE`) más `PRIMARY KEY` y `FOREIGN KEY`, sabiendo qué garantiza cada una y cuándo conviene normalizar.
8. **Escribir datos** con `INSERT`, `UPDATE` y `DELETE`, incluyendo `INSERT … SELECT`, y manejar las acciones referenciales (`ON DELETE`, `CASCADE`, `RESTRICT`) sin romper integridad.
9. **Automatizar** con `CREATE VIEW`, vistas temporales, CTEs (`WITH`) y triggers (`BEFORE`/`AFTER … INSERT`/`UPDATE`/`DELETE`), y decir cuándo cada uno es la herramienta correcta.
10. **Optimizar** leyendo un plan de ejecución (`EXPLAIN QUERY PLAN`), creando índices (`CREATE INDEX`, covering, parciales) y administrando el archivo (`VACUUM`).
11. **Manejar concurrencia y transacciones** (`BEGIN`, `COMMIT`, `ROLLBACK`, `ISOLATION`, locks), y explicar por qué una transacción es la unidad de todo-o-nada.
12. **Escalar**: replicación (leader/follower, read replicas), sharding, y el costo de cada uno; distinguir tipos de MySQL/PostgreSQL (`ENUM`, `SET`, `VARCHAR`, `DECIMAL`), stored procedures y el delimitador.
13. **Defenderse de SQL injection** con prepared statements y entender por qué concatenar strings de usuario en una query es una vulnerabilidad, no un atajo.

## Mapa temporal

Capítulos oficiales de la descripción. Duración = hasta el capítulo siguiente.

| # | Tiempo | Bloque | Dur. |
|---|---|---|---|
| 1 | 0:00:00 | Intro del curso (qué cubre, quién lo dicta, por qué SQL) | 0:29 |
| 2 | 0:00:29 | **Introduction** (por qué bases de datos) | 2 min |
| 3 | 0:02:35 | **Querying** — una tabla | 1:19:14 |
| 4 | 1:21:49 | **Relating** — varias tablas | 1:41:39 |
| 5 | 3:03:28 | **Designing** — el esquema | 1:21:24 |
| 6 | 4:24:52 | **Writing / Viewing** — insertar, actualizar, borrar, ver (el video une las dos semanas) | 3:05:35 |
| 7 | 7:30:27 | **Optimizing** — tiempo, espacio, concurrencia | 1:28:52 |
| 8 | 8:59:19 | **Scaling** — MySQL, PostgreSQL, réplica, sharding | 2:09:29 |

> Los timestamps de cada módulo abajo salieron de la primer aparición del concepto en el transcript, verificados contra el `[hh:mm:ss]` de `transcripcion.md`.

## Módulos

### M0 · Intro del curso y por qué bases de datos (0:00:00 – 0:16:40)

**Qué enseña.** La introducción de Malan (0:01:07) resume el arco entero: *"You'll master the fundamentals of SQL, including how to create, read, update, and delete data… model real world scenarios by designing tables, normalizing data to reduce redundancy, and joining tables using primary and foreign keys… automate queries with views, accelerate searches with indexes, and connect your database to languages like Python."* Carter retoma en 0:02:53 con la pregunta "¿por qué aprender esto?" y responde con la era de la información: Google, YouTube, los datos que generamos al interactuar.

De ahí sale la primera distinción real del curso: **una tabla no es una planilla**. La tabla existe desde hace miles de años (0:04:00, un registro de estipendios de un templo), pero la planilla falla en tres cosas — redundancia, tipos, y relación entre hojas — y esas tres fallas son exactamente el programa de las seis semanas siguientes.

**Citas verificadas.**

- *"You'll learn to model real world scenarios by designing tables, normalizing data to reduce redundancy, and joining tables using primary and foreign keys."* — 0:00:19
- *"We're living in the information age where we generate so much information, so much data by virtue of interaction with computers and with each other over the internet."* — 0:03:13
- Sobre las bases de datos como software: *"There are other kinds of software, other companies out there that make these ways to interact with a database."* — 0:09:41

**Ejercicios.**

1. Escribí, sin mirar el video, tres razones por las que una planilla no sirve para el catálogo de una biblioteca con préstamos. Después contrastalas contra las que da el video.
2. Instalá SQLite (`sqlite3 --version`) y creá una base vacía; el curso lo hace en 0:15:18 y es el único paso de entorno que pide.

---

### M1 · Querying: una tabla (0:02:35 – 1:21:49)

El módulo más largo del curso y el que enseña el 90 % de lo que se usa a diario. El dataset es `longlist.db`: 78 libros nominados al International Booker Prize (2018–2023) con rating y votos de Goodreads.

| Tema | Primer timestamp | Qué se aprende |
|---|---|---|
| `SELECT` | 0:16:40 | `SELECT *`, `SELECT columna`, alias con `AS` |
| `WHERE` y operadores | 0:18:40 | `=`, `!=`, `<`, `>`, `AND`, `OR`, `NOT`; comillas simples para strings |
| `LIKE` | 0:37:00 | `%` (cualquier cadena) y `_` (un carácter); case-insensitive en SQLite |
| `BETWEEN` | 0:50:00 | rango inclusivo, alternativa a dos comparaciones |
| `NULL` | 0:35:00 | ausencia de valor; `IS NULL`, `IS NOT NULL` |
| `ORDER BY` | 0:56:05 | ascendente por defecto, `ASC`, `DESC`, ordenar por varias columnas para desempatar |
| `LIMIT` | 0:22:39 | truncar resultados |
| Agregaciones | 1:05:51 | `AVG`, `COUNT`, `SUM`, `MIN`, `MAX`; `ROUND(a, n)`; alias de columna |
| `DISTINCT` | 1:18:48 | valores únicos de una columna |
| `GROUP BY` + `HAVING` | 2:55:52 · 1:20:53 | colapsar filas por clave y filtrar grupos |

**Citas verificadas.**

- *"Using select I can get back certain rows or in this case perhaps all of them just to get a taste of what's inside."* — 0:16:43
- Sobre `NULL`: *"We have this type called null where this means that this value doesn't exist."* — 0:35:08
- Sobre agregaciones: *"Aggregate functions… take some number of rows like all my ratings for instance and bring it down to one single cell."* — 1:10:11
- Sobre `ORDER BY`: *"Order by allows us to take the results of our query and order them as it suggests by some column itself."* — 0:56:07
- **Advertencia del curso sobre strings y comillas:** usó comillas dobles para columnas y simples para strings (0:19:54) — en SQLite ambos funcionan, en PostgreSQL no.

**Ejercicios.**

1. Contá cuántos libros del dataset tienen rating mayor a 4.0 **y** más de 10.000 votos (el curso lo hace en 0:52:00). Después contestá: ¿cuántos son si la condición es `OR`?
2. Traé los títulos que empiezan con `The` pero **no** contienen `Love`. Escribilo con `LIKE` y luego con dos condiciones separadas; compará resultados.
3. Encontrá las editoriales (`publisher`) sin repetir y, sobre eso, cuántos libros publicó cada una ordenado de mayor a menor. Es el ejercicio que obliga a encadenar `DISTINCT`/`GROUP BY` + `ORDER BY`.
4. Buscá los libros sin traductor. Explicá en una línea por qué `WHERE translator = NULL` devuelve cero filas.

**Cierre del módulo.** El curso cierra Querying con una demo de *bad design* (0:49:12, la tabla que mezcla todo en una sola celda) que prepara el problema de Relating.

---

### M2 · Relating: varias tablas (1:21:49 – 3:03:28)

**Qué enseña.** El salto de una tabla a un modelo. Empieza con el dataset de libros y sus tablas separadas (`books`, `authors`, `publishers`, `ratings`), y la primera idea que aparece es **la clave**: *"primary key… a unique identifier called an ISBN"* (1:37:28).

| Tema | Primer timestamp | Qué se aprende |
|---|---|---|
| Clave primaria | 1:37:44 | un identificador único por fila |
| Clave foránea | 1:38:54 | la PK de una tabla incluida como columna de otra |
| Diagrama entidad-relación | 1:30:10 | representar personas, lugares y cosas y sus relaciones |
| uno-a-muchos | 1:38:54 | `ratings` → `books` |
| muchos-a-muchos | 1:45:25 | tabla intermedia (*join table*, entidad asociativa) |
| Subconsulta | 1:54:06 | una query dentro de otra |
| `INNER JOIN` | 2:24:09 | sólo filas con coincidencia |
| `LEFT` / `RIGHT` / `FULL JOIN` | 2:28:07 | qué filas se conservan de cada lado |
| `UNION` | 2:40:31 | unir conjuntos de filas |
| `INTERSECT` | 2:39:56 | filas presentes en ambos |
| `EXCEPT` | 2:41:32 | filas de uno ausentes en el otro |
| `GROUP BY` aplicado | 2:55:52 | agregar sobre joins |

**Citas verificadas.**

- *"A foreign key is simply taking a primary key from one table and including it in the column of some other table."* — 1:39:00
- *"A join table also called a junction table or an associative entity…"* — 1:45:25
- *"Inner join"* como caso por defecto: *"So this is our example then of an inner join."* — 2:25:25

**Ejercicios.**

1. Escribí la consulta que devuelve el título y el rating promedio de cada libro, con el nombre del autor. Necesitás tres tablas; el curso lo arma en 2:55:52.
2. Componé `UNION`, `INTERSECT` y `EXCEPT` para: (a) todos los autores y traductores juntos; (b) los que son ambas cosas; (c) los traductores que no son autores. El curso lo demuestra en 2:39:56–2:41:32.
3. Compará `INNER JOIN` vs `LEFT JOIN` sobre libros sin rating: ¿qué fila desaparece y por qué?
4. Respondé sin correr código: si `sea_lions` tiene 5 filas y `migrations` tiene 12, ¿cuántas filas devuelve cada tipo de join? Usá el dataset del video (2:18:00) para comprobar.

**Cierre del módulo.** El curso cierra Relating presentando el problema que no resuelve el join: el esquema está mal diseñado. Eso abre Designing.

---

### M3 · Designing: el esquema (3:03:28 – 4:24:52)

**Qué enseña.** Cómo se construye la base desde cero. El dataset es la red de subte de Boston (MBTA): `riders`, `stations`, `swipes`, `cards`. La clase pasa de "crear tablas" a "crear tablas que no se pueden romper".

| Tema | Primer timestamp | Qué se aprende |
|---|---|---|
| `CREATE TABLE` | 3:10:02 | nombre, columnas, tipos |
| Tipos y afinidades de SQLite | 3:29:45 | `INTEGER`, `REAL`, `TEXT`, `BLOB`, `NUMERIC`; afinidad, no tipo estricto |
| `DROP TABLE` | 3:41:42 | eliminar tabla |
| `ALTER TABLE` | 4:08:40 | `ADD COLUMN`, `RENAME COLUMN`, `DROP COLUMN` |
| Normalización | 3:17:37 | 1NF, 2NF, 3NF — el curso nombra las tres pero no profundiza |
| Constraint de tabla | 3:49:16 | `PRIMARY KEY`, `FOREIGN KEY` a nivel tabla |
| Constraint de columna | 3:57:00 | `CHECK`, `DEFAULT`, `NOT NULL`, `UNIQUE` |
| ER y relaciones | 3:21:00 | cardinalidad uno-a-uno y uno-a-muchos |
| Transacción (introducción) | 4:06:16 | qué es un swipe como transacción |

**Citas verificadas.**

- *"To normalize means…"* — 3:17:40 (el curso define normalizar como reducir redundancia y evitar errores)
- *"There's like first normal form, second normal form, third normal form."* — 3:18:00
- *"Let's introduce one more kind of constraint. This one called a column constraint."* — 3:57:00
- *"Check, default, not null, and unique"* — 3:57:35

**Ejercicios.**

1. Diseñá el esquema de la MBTA con las cuatro tablas y todas las constraints. Después rompé cada constraint a propósito (`INSERT` de un `swipe` con `rider_id` inexistente, `CHECK` de monto negativo) y verificá el error exacto. El curso lo hace en 4:40:00 con `UNIQUE`.
2. Agregá una columna `email` a `riders` con `UNIQUE NOT NULL` y explicá qué pasa con las filas existentes.
3. Escribí tres consultas que muestren por qué la tabla plana del final de Querying tenía redundancia y cómo el nuevo esquema la elimina.
4. Decidí si `cards` debe tener un `id` propio o usar el número de tarjeta como PK, y justificalo con las razones del curso.

---

### M4 · Writing / Viewing: escribir y ver los datos (4:24:52 – 7:30:27)

**Qué enseña.** La semana más larga del video (tres horas) porque une dos capítulos oficiales. El dataset es el Museum of Fine Arts de Boston: `collections`, `artists`, `created`, `transactions`.

| Tema | Primer timestamp | Qué se aprende |
|---|---|---|
| `INSERT INTO … VALUES` | 4:25:26 | fila por fila; PK manual vs `AUTOINCREMENT` |
| `INSERT INTO … SELECT` | 4:57:00 | copiar resultados de una query a una tabla |
| Importar CSV | 4:23:15 · 4:35:46 · 4:47:18 | `.import`, importar a tabla temporal y luego insertar |
| `UPDATE … SET … WHERE` | 5:33:00 | nunca sin `WHERE` |
| `DELETE FROM … WHERE` | 5:03:00 | borrado selectivo |
| `ON DELETE` / `CASCADE` / `RESTRICT` | 5:10:07 · 5:21:50 · 5:20:58 | qué pasa con las filas hijas |
| Funciones escalares | 5:48:00 | `UPPER`, `LOWER`, y el resto de la lista de SQLite |
| `CASE … WHEN … THEN … ELSE … END` | 7:09:59 | columnas calculadas condicionales |
| `TRIGGER` | 5:49:33 | `BEFORE`/`AFTER` sobre `INSERT`, `UPDATE`, `DELETE`; `NEW` y `OLD` |
| `CREATE VIEW` | 6:23:26 | tabla virtual persistente |
| Vista temporal | 6:41:44 | existe por una conexión |
| `DROP VIEW` | 6:48:42 | eliminar vista |
| CTE (`WITH`) | 6:47:08 | view que existe por una sola query |
| Vistas y privacidad | 7:03:00 | `rideshare.db`: qué se expone al compartir una vista |

**Citas verificadas.**

- *"Where is vitally important to this delete from."* — 5:03:03
- *"What we'll see now, though, is how to talk about these things called triggers."* — 5:49:45
- *"So create view given some name as the result of this query gives me a view that is then saved and part of…"* — 6:23:32
- Sobre CTEs: *"A common table expression is simply a view that exists for the duration of a single query."* — 6:47:14
- **Sobre soft delete y ética** (lo más valioso del módulo, 6:07:00): *"It's okay if we're talking about artwork here, but if you're talking about user data, is it right to only soft delete it if they ask you to delete it? And particularly in conversation with new frameworks like GDPR and the right to be forgotten…"*

**Ejercicios.**

1. Cargá un CSV de 10 filas en una tabla temporal (`CREATE TEMPORARY TABLE`) y pasalo a la tabla real con `INSERT … SELECT`. Es el patrón del curso para CSVs que no coinciden exactamente con el esquema (4:54:00).
2. Creá un trigger `AFTER DELETE ON collections` que registre en `transactions` la pieza vendida. Después verificá con `SELECT` que el `INSERT` ocurrió sin que lo escribieras (5:57:00).
3. Escribí una vista que oculte la columna `rider` de `rides` y comprobá qué pasa al intentar `UPDATE` sobre ella (7:00:00: `Cannot modify 2021 because it is a view`). Explicá el motivo.
4. Reescribí el mismo cálculo de "rating promedio por año" con subconsulta, con vista, con vista temporal y con CTE. El curso las compara en 6:51:44.
5. Creá un trigger que haga *soft delete* en lugar de `DELETE` (el curso lo sugiere en 9:58:22) y explicá un caso donde eso sea legalmente incorrecto.

---

### M5 · Optimizing: tiempo, espacio y concurrencia (7:30:27 – 8:59:19)

**Qué enseña.** El módulo con más técnica por minuto. Dataset: IMDb en SQLite (más de 200.000 ratings y 400.000 películas). Tres ejes: **tiempo** (índices, planes), **espacio** (`VACUUM`) y **concurrencia** (locks, transacciones, aislamiento).

| Tema | Primer timestamp | Qué se aprende |
|---|---|---|
| Indexar es buscar en un libro | 7:43:32 | analogía del índice del libro |
| `EXPLAIN QUERY PLAN` | 7:47:32 | leer el plan que arma el motor |
| `CREATE INDEX` | 8:00:16 | índice simple y *covering index* |
| Índice parcial | 8:21:00 | `CREATE INDEX … WHERE year = 2023` |
| Costo del índice | 8:18:00 | espacio y escritura más lentos |
| `VACUUM` | 8:24:28 | recuperar espacio tras borrados |
| Transacción | 8:32:06 | `BEGIN TRANSACTION`, `COMMIT` |
| `ROLLBACK` | 8:45:00 | deshacer todo lo de la transacción |
| Aislamiento | 8:34:14 | qué se ve desde otra conexión mientras hay una transacción abierta |
| Locks | 8:53:10 | qué pasa si dos queries tocan la misma fila |

**Citas verificadas.**

- *"Other DBMS's might call this just simply explain but in SQLite it's explain query plan."* — 7:47:38
- Sobre el índice: *"You can use the index of the book."* — 7:43:38
- Sobre `VACUUM`: *"One other way we can more efficiently use space is to a bit of vacuuming, so to speak."* — 8:24:27
- **Cita de oro del módulo:** el curso muestra que un `EXPLAIN QUERY PLAN` con índice parcial **igual hace `SCAN`**: *"We're going to scan movies, but we're still going to use the index we just created called recents."* — 8:22:37. Es la lección que el curso quiere dejar: el plan es la verdad, no la intención.

**Ejercicios.**

1. Corré `EXPLAIN QUERY PLAN` sobre una query sin índice y con índice, y copiá la diferencia. Si no ves diferencia, el índice no sirve para esa query: explicá por qué.
2. Creá un índice parcial `WHERE year = 2023` y medí con `.timer on` el antes y el después. El curso da la medición (1,3 s) en 8:22:20.
3. Abrí dos conexiones `sqlite3` a la misma base, hacé `BEGIN` en una y `SELECT` desde la otra: ¿qué ves? Repetí con escritura y explicá el lock.
4. Armá una transferencia entre dos cuentas con `BEGIN`/`COMMIT` y una versión que falle a mitad de camino; con `ROLLBACK` dejá la base consistente (8:41:47).
5. Explicá en cinco líneas por qué el módulo dice que un índice "compra tiempo con espacio y con escritura".

---

### M6 · Scaling: MySQL, PostgreSQL y hacerlo grande (8:59:19 – 11:08:48)

**Qué enseña.** La última clase sale de SQLite. Tres bloques: **(a)** MySQL como DBMS con servidor, usuarios y tipos propios; **(b)** PostgreSQL como DBMS relacional robusto; **(c)** escalar por arriba (réplica) y por abajo (sharding), y cerrar con SQL injection.

| Tema | Primer timestamp | Qué se aprende |
|---|---|---|
| Qué es escalabilidad | 9:00:08 | manejar más requests sin cambiar el comportamiento |
| MySQL: conexión y usuarios | 9:05:00 | `mysql -u -h -P`, `root`, `127.0.0.1`, puerto 3306 |
| `CREATE DATABASE` / `USE` | 9:09:00 | separar bases dentro de un servidor |
| Tipos MySQL | 9:24:00 | `INT`, `VARCHAR`, `FLOAT` vs `DOUBLE` (imprecisión), `DECIMAL`, `ENUM`, `SET`, `DATETIME` |
| `AUTO_INCREMENT`, backticks | 9:23:29 | convenciones propias del motor |
| `ALTER TABLE` en MySQL | 9:33:00 | mismas operaciones, otra sintaxis |
| Stored procedures | 9:55:34 | `CREATE PROCEDURE`, `DELIMITER` |
| PostgreSQL / `psql` | 10:18:37 | mismo modelo, otro cliente |
| Replicación | 9:02:24 · 10:36:00 | leader/follower, read replicas |
| Sharding | 9:02:26 | partir los datos entre servidores |
| SQL injection | 10:53:55 | `' OR 1=1`, `UNION` malicioso |
| Prepared statements | 11:01:23 | `PREPARE`, `?`, `EXECUTE … USING` |
| Python / lenguajes | 11:06:55 | por qué los format strings son el mismo problema |

**Citas verificadas.**

- *"For an application to be scalable… it means it can take some number of requests and handle those."* — 9:00:05
- Sobre `ENUM` y `SET` — 9:24:19: *"Enum means I can only have one of these options… but a set would allow me to choose more than one."*
- Sobre réplicas: *"This follower is what's known as a read replica."* — 10:36:57
- **Definición de SQL injection:** *"SQL injection means I have some query and somebody else adds in some malicious code to finish that query for me."* — 10:54:00
- **La cita de cierre:** *"Now, go off and continue your learning. We'll see you later."* — 11:08:34

**Ejercicios.**

1. Levantá un MySQL o PostgreSQL local (Docker) y replicá el `CREATE TABLE` de `stations` del curso: la sintaxis no es la misma. El video muestra las diferencias en 9:24:00.
2. Escribí un `ENUM` y un `SET` para géneros de película y justificá cuál usarías.
3. Explicá cuál es la diferencia entre réplica y shard y cuándo cada uno arregla el problema y cuándo lo empeora. El curso lo discute en 9:02 y lo demuestra en 10:36.
4. Reproducí la inyección `' OR 1=1` sobre una tabla `users` de prueba y después la misma contra un prepared statement. El video lo hace en 10:56 y 11:04.
5. **Ejercicio de cierre, sin código:** respondé con lo del curso por qué *"usá parámetros"* no es una preferencia de estilo sino una garantía de seguridad — y qué falla además de la query (la confidencialidad de *toda* la tabla).

## Banco de preguntas (22)

1. ¿Qué diferencia a una base de datos de una planilla? Nombrá las tres razones del curso.
2. ¿Por qué `SELECT *` es aceptable para explorar y malo para una aplicación?
3. ¿Qué devuelve `WHERE title = NULL` y por qué no es lo mismo que `IS NULL`?
4. ¿Cuál es la diferencia entre `WHERE` y `HAVING`? ¿Y por qué `HAVING` necesita un `GROUP BY` en la mayoría de los motores?
5. ¿`UNION` y `UNION ALL` devuelven lo mismo? ¿Cuál es más caro y por qué?
6. ¿Cuándo `LEFT JOIN` es obligatorio y `INNER JOIN` cambia el resultado de forma incorrecta?
7. ¿Qué hace una clave foránea que no hace un `JOIN`? Pensá en integridad, no en resultado.
8. ¿Qué garantiza `UNIQUE` y qué **no** garantiza? ¿Y `NOT NULL` sobre una columna que ya tiene filas?
9. Explicá las tres formas normales con el ejemplo de la tabla plana del final de Querying.
10. ¿Qué es una tabla intermedia y por qué existe en un muchos-a-muchos?
11. ¿Cuándo un trigger es la herramienta correcta y cuándo oculta un efecto que debería ser explícito?
12. ¿Qué diferencia hay entre vista, vista temporal y CTE? Nombrá el alcance de cada una.
13. ¿Por qué no se puede hacer `UPDATE` sobre una vista en SQLite?
14. ¿Qué muestra `EXPLAIN QUERY PLAN` y por qué el curso dice que es la verdad y no la intención?
15. ¿Cuál es el costo de un índice? Nombrá tiempo, espacio y escritura.
16. ¿Qué es un covering index?
17. ¿Qué hace `BEGIN` y qué hace `ROLLBACK` que `DELETE` no puede hacer?
18. ¿Qué significa aislamiento y qué se ve desde otra conexión durante una transacción abierta?
19. ¿Qué hace `VACUUM` y por qué el archivo no se achica solo al borrar filas?
20. ¿Diferencia entre `FLOAT` y `DOUBLE`, y por qué `DECIMAL` en dinero?
21. ¿Cuándo conviene réplica y cuándo sharding? ¿Qué problema arregla cada uno?
22. ¿Por qué un prepared statement detiene una inyección que un `format()` de Python no?

## Lo que el curso **no** cubre (declarado o verificado en el transcript)

- **Normalización hasta 3NF, sin profundidad:** el curso nombra 1NF, 2NF, 3NF en 3:17:37 y define normalizar, pero no desarrolla dependencias funcionales ni ejemplos de cuarta/quinta forma. Para eso hace falta otra fuente.
- **Window functions:** cero menciones en 11 horas. Si el objetivo es analítica, este curso no las cubre.
- **`COALESCE`, `IFNULL`, `NULLIF`:** no aparecen. El manejo de `NULL` se limita a `IS NULL`/`IS NOT NULL`.
- **`OFFSET`, `GLOB`, `rowid`:** cero menciones.
- **ORM / Django / Flask / Java:** cero. La conexión con lenguajes se menciona en la intro (Python) y se responde en una pregunta del público al final (11:06:55), pero no hay una lección de integración.
- **Los problem sets de CS50:** el video es la grabación de clases, no incluye los assignments (DESE, Fiftyville, Movies, Packages, etc. del sitio de CS50). El material oficial está en https://cs50.harvard.edu/sql/ y **no se auditó desde acá**.
- **Modelado de rendimiento real:** el módulo de Optimizing usa el dataset de IMDb en una máquina del expositor; no hay una metodología de benchmark reproducible ni números que se puedan extrapolar.

## Plan de estudio sugerido

| Sesión | Módulo | Tiempo de video | Entregable |
|---|---|---|---|
| 1 | M0 + M1 (primera mitad) | ~45 min | `longlist.db` cargada + ejercicios 1–2 |
| 2 | M1 (agregaciones, ORDER BY) | ~40 min | ejercicios 3–4 del M1 |
| 3 | M2 | ~1 h | consultas de tres tablas + set operators |
| 4 | M3 | ~1 h | esquema MBTA con constraints, con las violaciones reproducidas |
| 5 | M4 (INSERT/UPDATE/DELETE) | ~1 h | CSV importado + trigger + vista |
| 6 | M4 (vistas, CTE) | ~45 min | las cuatro formas del mismo cálculo |
| 7 | M5 | ~1 h | plan de ejecución antes/después + transacción con rollback |
| 8 | M6 | ~1 h 15 | MySQL/Postgres local + inyección y prepared statement |

> Regla del workspace (Gonzo, 2026-09-30): se estudia por **módulo**, no por lección, y cada módulo cierra con un activo (consulta, esquema, trigger, índice), no con un resumen.

## Recursos oficiales

- Sitio del curso, notas y problem sets: https://cs50.harvard.edu/sql/ (no auditado desde acá)
- Datasets del curso: los `longlist.db`, `mbta.db`, `mfa.db`, `imdb.db`, `rideshare.db` se muestran en el video; el sitio los distribuye.
- CS50 (el curso de ciencias de la computación, previo): https://cs50.harvard.edu/x/

---
*Clase montada el 2026-11-12 desde el transcript completo de los subtítulos automáticos. Las citas están verificadas contra el `[hh:mm:ss]` de `transcripcion.md`; los errores de ASR se corrigieron en la cita (Zeni → Zenke, Postgress/PostQL → PostgreSQL, SQL light → SQLite, CT → CTE).*
