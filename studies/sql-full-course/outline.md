# Clase: SQL Full Course for Beginners (30 Hours) – From Zero to Hero

- Fuente: https://www.youtube.com/watch?v=SSKVgrwhzus
- Canal: Data with Baraa (`@DataWithBaraa`)
- Expositor: Baraa (se presenta al inicio como "Baraa…, I lead big data projects at Mercedes-Benz"; el ASR lo escribe «Barzalini»)
- Duración: 29:48:27 (107.307 s) — 30 horas
- Publicado: 2025-03-27
- Idioma: inglés · Transcript: `transcripcion.md` (subtítulos automáticos `en-orig`, 48.358 cues, ~364.000 palabras, con timestamps `[hh:mm:ss]`)
- Capítulos: los 41 oficiales de la descripción, agrupados en los tres niveles que declara el propio curso (Beginner / Intermediate / Advanced) + proyectos
- Material del curso: https://www.datawithbaraa.com/wiki/sql (handbook, datasets, scripts) — no verificado desde acá
- Clase creada: 2026-11-11

## Tesis de la clase

**SQL no se aprende escribiendo sintaxis: se aprende entendiendo qué hace el motor debajo.** El curso es explícito en el minuto 0 de la intro: "not only you will learn how to write SQL codes, but more important than that, you will learn how exactly SQL works behind the scenes" (00:00:19). De ahí sale la forma del curso: animaciones para cada concepto, y una regla de oro que reaparece en el bloque de performance — *una buena práctica no vale nada si no se prueba con el execution plan* (21:44:18).

La segunda mitad del curso cambia de registro: deja de enseñar sintaxis y arma **tres proyectos completos** sobre el mismo dataset — un data warehouse medallion (bronze/silver/gold), un análisis exploratorio, y analítica avanzada de negocio. Ese tramo es el que convierte un curso de SQL en un curso de ingeniería de datos.

## Resultado esperado

Al terminar la clase se puede:

1. Explicar qué es una query y por qué `SELECT` no modifica nada, y ordenar las cláusulas por el orden en que las piensa el motor, no por el orden en que se escriben.
2. Crear y modificar estructura con DDL (`CREATE`, `ALTER`, `DROP`) y manipular datos con DML (`INSERT`, `UPDATE`, `DELETE`), distinguiendo cuál de los dos es declarativo y cuál es una transacción sobre filas.
3. Filtrar con `WHERE`, combinar columnas con los cinco tipos de join, combinar filas con los cuatro set operators (`UNION`, `UNION ALL`, `EXCEPT`, `INTERSECT`) y saber por qué elegir uno u otro cambia el costo.
4. Manejar `NULL` como *ausencia de valor*, no como cero ni cadena vacía, y usar las funciones que lo tratan (`ISNULL`/`COALESCE`, `NULLIF`).
5. Escribir funciones de ventana en las cuatro familias: agregadas, ranking (`ROW_NUMBER`, `RANK`, `DENSE_RANK`), de valor (`LAG`, `LEAD`, `FIRST_VALUE`) y de distribución (`PERCENT_RANK`, `CUME_DIST`), entendiendo `PARTITION BY` + `ORDER BY` como el eje.
6. Elegir entre las cinco técnicas de reutilización — subquery, CTE, view, CTAS/tabla temporal, tabla temporal — por la dimensión que discute el curso: **storage, lifetime, y costo de mantenimiento**, no por preferencia.
7. Encapsular lógica con stored procedures y automatizar reacción a eventos con triggers, sabiendo que un trigger es una stored procedure que corre sola y por lo tanto oculta efectos.
8. Diseñar índices con criterio: clustered vs non-clustered (estructura), row store vs column store (storage), unique y filtered (función), y leer un **execution plan** para verificar si el motor realmente los usó.
9. Particionar tablas y explicar por qué la partición es organización física (file groups) antes que una cláusula SQL.
10. Aplicar el criterio de performance del curso: **escribir legible, medir con el plan, optimizar solo lo que se midió lento**. Las 30 tips son un catálogo, no un mandato.
11. Usar IA como copiloto con disciplina: intentar resolver primero, y saber cuándo y dónde el modelo se equivocó en SQL.
12. Construir un data warehouse medallion end-to-end: analizar el source system, cargar bronze con full load sin transformaciones, integrar y modelar en silver, y armar gold como dimensiones y hechos con nombres amigables, documentado (data flow, data model, data dictionary).
13. Correr un EDA con SQL puro (profiling con agregaciones) y un análisis avanzado (tendencias, estacionalidad, segmentación, reporting) sobre el mismo warehouse.

## Mapa temporal

| Tiempo | Bloque | Nivel |
|---|---|---|
| 00:00:00 | Intro y por qué el curso es distinto | — |
| 00:07:38 | Introduction to SQL | 🟢 |
| 00:22:33 | Setup Your Environment (SQL Server + management studio) | 🟢 |
| 00:34:01 | Query Data (SELECT) — 58 min, la base de todo | 🟢 |
| 01:32:31 | DDL Commands | 🟢 |
| 01:43:44 | DML Commands | 🟢 |
| 02:08:03 | Filtering Data | 🟡 |
| 02:47:57 | SQL Joins (Basics) | 🟡 |
| 03:27:29 | SQL Joins (Advanced) | 🟡 |
| 04:02:09 | Set Operators | 🟡 |
| 04:47:41 | SQL Functions (marco general) | 🟡 |
| 04:52:58 | String Functions | 🟡 |
| 05:18:44 | Numeric Functions | 🟡 |
| 05:22:48 | Date and Time Functions — 96 min, el bloque más largo del nivel | 🟡 |
| 06:59:06 | NULL Functions — 68 min | 🟡 |
| 08:07:50 | Case Statement | 🟡 |
| 08:43:36 | Aggregate Functions | 🟡 |
| 08:50:11 | Window Functions Basics | 🟡 |
| 09:47:00 | Window Aggregate | 🟡 |
| 10:53:09 | Window Ranking | 🟡 |
| 11:56:05 | Window Value | 🟡 |
| 12:40:34 | Advanced SQL Techniques (el problema que resuelven las 5 técnicas) | 🔴 |
| 12:58:04 | Subqueries | 🔴 |
| 14:18:08 | Common Table Expressions (CTE) | 🔴 |
| 15:35:02 | Views | 🔴 |
| 16:36:40 | CTAS and Temp Tables | 🔴 |
| 17:17:31 | Compare Advanced Techniques (tabla comparativa) | 🔴 |
| 17:27:04 | Stored Procedures | 🔴 |
| 18:12:58 | Triggers | 🔴 |
| 18:23:42 | Indexes — 116 min, el bloque técnico más profundo | 🔴 |
| 20:20:31 | Execution Plan | 🔴 |
| 21:11:03 | Partitions | 🔴 |
| 21:43:39 | 30x Performance Tips | 🔴 |
| 22:24:25 | AI and SQL | 🔴 |
| 23:21:04 | Project: SQL Data Warehouse | 🔴 Proyecto 1 |
| 24:32:54 | Project DWH \| Bronze | 🔴 Proyecto 1 |
| 25:10:09 | Project DWH \| Silver — 97 min, el bloque más largo del curso | 🔴 Proyecto 1 |
| 26:47:46 | Project DWH \| Gold | 🔴 Proyecto 1 |
| 27:41:51 | Project: Exploratory Data Analysis (EDA) | 🔴 Proyecto 2 |
| 28:30:38 | Project: Advanced Data Analytics | 🔴 Proyecto 3 |
| 29:47:24 | Thank You | — |

## Módulos

### 🟢 Nivel Beginner (00:07:38 – 02:08:03)

**1. Introduction to SQL (07:38).** Qué es una base de datos relacional, qué es una query, por qué SQL es declarativo: se pide *qué*, no *cómo*.

**2. Setup Your Environment (22:33).** SQL Server + management studio. El curso es **SQL Server**, no Postgres: es una declaración de plataforma, no un detalle. Todo el resto (`GETDATE`, `TOP`, `ISNULL`, `IDENTITY`, file groups, clustered index por defecto) depende de eso. *(Nota para el workspace: portar los ejercicios a Postgres no es copiar el script, es reescribirlo.)*

**3. Query Data / SELECT (34:01).** 58 minutos para la sentencia más simple, porque el curso explica la *forma* de la query: cláusulas como piezas, y el orden lógico de evaluación distinto del orden de escritura. Es el módulo donde se instala el modelo mental que sostiene los joins y las ventanas después.

**4. DDL Commands (1:32:31).** `CREATE TABLE` con tipos y columnas, `ALTER`, `DROP`. La estructura antes que los datos.

**5. DML Commands (1:43:44).** `INSERT` (dos vías: valores manuales y desde otra tabla), `UPDATE`, `DELETE`. Primera aparición del riesgo real: el `WHERE` que falta en un `UPDATE`.

### 🟡 Nivel Intermediate (02:08:03 – 12:40:34)

**6. Filtering Data (2:08:03).** `WHERE`, operadores, `LIKE`, `BETWEEN`, `IN`, y el primer choque con `NULL`.

**7. SQL Joins, Basics (2:47:57) y Advanced (3:27:29).** Dos bloques: primero el modelo mental (inner, left, right, full), después los casos que rompen la intuición (duplicados por cardinalidad, join con `NULL`, join múltiple).

**8. Set Operators (4:02:09).** `UNION`, `UNION ALL`, `EXCEPT`, `INTERSECT`. La distinción que el curso remarca: los joins combinan **columnas**, los set operators combinan **filas**.

**9. Funciones (4:47:41 marco general → 5:22:48 Date and Time).** El tramo más largo del nivel intermedio. String, numéricas, y **96 minutos de fecha y hora** — desproporcionado a propósito: en analítica de negocio casi toda métrica se agrupa por tiempo.

**10. NULL Functions (6:59:06).** 68 minutos sobre un solo concepto: `NULL` **no es igual a nada**, ni a cero ni a string vacío. "It tells us there is no value and it is missing" (6:59:44). Es el módulo que explica por qué `= NULL` nunca es verdadero.

**11. Case Statement (8:07:50) y Aggregate Functions (8:43:36).** Categorización condicional y las cinco agregadas clásicas. Cortos y densos.

**12. Window Functions (8:50:11 – 12:40:34).** Cuatro bloques de ~1 h: Basics, Aggregate, Ranking, Value. El eje es siempre `PARTITION BY` + `ORDER BY`: qué se agrupa y en qué orden se mira la ventana. En Ranking, el curso dedica tiempo a la diferencia práctica entre `ROW_NUMBER`, `RANK` y `DENSE_RANK` y a los percentiles (`PERCENT_RANK`, `CUME_DIST`).

### 🔴 Nivel Advanced (12:40:34 – 22:24:25)

**13. Advanced SQL Techniques (12:40:34).** No enseña nada nuevo: plantea **el problema** que las próximas cinco técnicas resuelven. Analistas sin acceso al modelo físico preguntando lo mismo una y otra vez al equipo de base de datos, cada uno reinventando la misma lógica compleja: redundancia, inconsistencia, performance y seguridad. Ese es el criterio con el que después se elige.

**14. Las cinco técnicas (12:58:04 – 17:27:04).** Subqueries → CTE → Views → CTAS/Temp Tables, y un bloque de 9 minutos que las compara **lado a lado** en storage, lifetime, y mantenimiento. Ese bloque (`Compare Advanced Techniques`) es el que hay que releer antes de decidir cuál usar en un proyecto real.

**15. Stored Procedures (17:27:04) y Triggers (18:12:58).** Encapsular vs. automatizar. La analogía del café: pedir todo el pedido cada vez vs. "dame lo de siempre". El trigger es esa misma stored procedure, pero disparada por un evento sin que nadie la llame — y el curso es claro en que eso es poder y riesgo a la vez.

**16. Indexes (18:23:42, 116 min).** El bloque más profundo del nivel. Tres ejes: **estructura** (clustered / non-clustered), **storage** (row store / column store), **función** (unique / filtered). Con la advertencia que ordena todo: cada índice mejora lecturas y **encarece escrituras** — es un trade-off, no una mejora.

**17. Execution Plan (20:20:31).** La herramienta de verificación del curso. La analogía del mapas: el motor planifica ruta (scan o index, hash join o loop join) y después ejecuta; el plan se cachea. Ejemplo medido en el video: un heap scan lee ~60.000 filas para devolver 12, el índice lee 12. *(Ese contraste es el experimento que hay que reproducir para creerle a cualquier tip.)*

**18. Partitions (21:11:03) y 30x Performance Tips (21:43:39).** Partición como organización física: primero file groups (contenedores lógicos de archivos), después las particiones sobre ellos. Y la **regla de oro** de las 30 tips, en palabras del curso: "always test using the execution plan… always write the query to be understandable, and only optimize it if you notice it is slow" (21:44:42). La conclusión práctica: si dos queries dan el mismo plan, elegir la más legible.

**19. AI and SQL (22:24:25).** El bloque más opinionado y el más útil para este workspace. Tres cosas que dice:
- **Disciplina primero:** resolver solo, y consultar a la IA solo cuando no quedan ideas. Si se salta ese paso "you won't develop skills in order to understand when and where the AI was wrong" (22:25:12).
- **Qué son** ChatGPT y GitHub Copilot: mismo family de modelos, distinta forma de uso (chat standalone vs. sugerencia en el editor).
- **Cómo pedirle SQL:** el curso muestra un prompt real con rol, esquema, formato esperado de salida, pedido de comentarios solo en lo no obvio, y pedido de **tres versiones con evaluación de legibilidad y performance**. Es un prompt de ingeniería, no un "hacé esto".

### 🔴 Proyectos (23:21:04 – 29:48:27)

**20. Project 1 — SQL Data Warehouse.** El orden del curso es el orden correcto de ingeniería:
1. **Analizar el source system** (6 archivos, dos fuentes) antes de escribir código.
2. **Bronze:** full load, truncate + insert, **cero transformaciones**, sin modelo.
3. **Silver (97 min, el bloque más largo del curso):** integración y limpieza.
4. **Gold:** identificar los business objects, clasificar cada tabla (dimensión, hecho, flat), renombrar columnas a nombres de consumidor, validar conectividad y datos, y **documentar**: data flow diagram, data model, data dictionary.

**21. Project 2 — Exploratory Data Analysis (27:41:51).** Data profiling con agregaciones simples sobre el dataset del proyecto 1. La habilidad que se lleva: formular preguntas y contestarlas con SQL básico.

**22. Project 3 — Advanced Data Analytics (28:30:38).** El uso real de las ventanas y CTEs: tendencia año a año, después drill-down a mes (estacionalidad: diciembre el mejor, febrero el peor en el dataset del curso), segmentación y reporting.

## Citas verificadas

Cada cita se buscó en `transcripcion.md`; los timestamps son del cue que la contiene.

- **La promesa del curso** — `[00:00:21]`: "not only you will learn how to write SQL codes, but more important than that, you will learn how exactly SQL works behind the scenes".
- **Disciplina con IA** — `[22:25:12]`: "Always try to solve the task on your own and only turn to AI if you don't have any more ideas on how to solve the task"; y la razón: "you won't develop skills in order to understand when and where the AI was wrong".
- **La regla de oro de performance** — `[21:44:18]`: "always you have to test using the execution plan… always write the query to be understandable and only optimize it if you notice it is slow".
- **Qué es un índice** — `[18:23:46]`: "an index is a data structure that provides a quick access to the rows to improve the speed of your queries".
- **El trade-off de los índices** — `[18:26:29]`: "each index type has its own strings but as well there is always a tradeoff. Some might improve their read performance. The other one might improve the insert and update operations".
- **Qué es un execution plan** — `[20:22:09]`: el plan se construye "based on your query and as well the statistics", elige scan o index y tipo de join, y después "the database engine is going to take this execution plan and store it at the cache".
- **El experimento del heap scan** — `[20:35:49]`: con index "we are reading only 12 in order to get 12… the SQL was very happy about it and used it in order to fast find our data".
- **Qué es `NULL`** — `[6:59:44]`: "a null means nothing unknown. It is not equal to anything. So it is not equal to zero or empty string or blank space."
- **Set operators vs. joins** — `[4:02:27]`: "if you want to combine the columns, we use the joins… if we want to combine the rows of two tables, we can use the set operators".
- **Trigger** — `[18:13:24]`: "triggers in SQL they are special stored procedure that automatically runs or let's say fired in response to a specific event that happens on a table".
- **La especificación de bronze** — `[24:38:34]`: "we are doing a full load. So that means we are truncating and then inserting the data. There will be no data transformations at all in the bronze layer. And as well we will not be creating any data model."
- **El proceso de gold** — `[26:49:04]`: identificar business objects → clasificar tabla (dimensión/hecho/flat) → renombrar columnas a lenguaje del consumidor → validar → documentar (diagrama de modelo, data dictionary, data flow).

## Banco de preguntas

1. ¿Por qué el curso dice que `SELECT` no cambia la estructura ni los datos, y qué dos cosas sí cambian una tabla entonces?
2. ¿Cuál es la diferencia operativa entre combinar tablas con un join y con un set operator?
3. `WHERE col = NULL` devuelve 0 filas. ¿Por qué, y con qué se escribe lo que el autor quiso decir?
4. ¿Qué hace `PARTITION BY` que no hace `GROUP BY`, y por qué eso obliga a las funciones de ventana?
5. `ROW_NUMBER`, `RANK` y `DENSE_RANK` sobre precios con un empate: ¿cuál deja huecos y cuál no?
6. Nombrá las cinco técnicas de reutilización del curso y ordenalas por *lifetime* de lo más corto a lo más largo.
7. Un analista pide una view "para no repetir la lógica". ¿Qué gana y qué no, comparado con un CTAS?
8. ¿Por qué una view no ocupa storage y un CTAS sí?
9. Un trigger `AFTER DELETE` que inserta en una tabla de auditoría: ¿qué pasa si la auditoría falla, y cómo se detecta eso sin mirar el código del trigger?
10. Tres criterios para clasificar índices, y un ejemplo de cada uno.
11. Tenés una tabla con 50 millones de filas y una query que tarda 8 segundos: ¿cuál es el primer paso, antes de crear ningún índice?
12. El plan muestra un heap scan leyendo 60.000 filas para devolver 12. ¿Qué dos cosas pueden estar pasando?
13. Según la regla de oro del curso, ¿cuándo ganar performance no es razón suficiente para cambiar una query?
14. ¿Por qué el curso recomienda pedirle a la IA tres versiones de una query y que ella misma las evalúe?
15. En el proyecto DWH, ¿por qué la carga bronze es truncate + insert y no un merge con transformaciones?
16. ¿Qué tres documentos deja el paso de gold, y para quién es cada uno?
17. La capa silver del curso dura 97 minutos de video. ¿Qué tipo de trabajo justifica eso, y en qué se distingue de gold?
18. Un EDA con SQL puro: ¿qué cuatro agregaciones armás primero y qué pregunta contesta cada una?

## Notas editoriales

- **El transcript son subtítulos automáticos de YouTube** (`en-orig`), no ASR local: 48.358 cues deduplicados de 96.716 eventos. Tiene timestamps reales y cubre los 30 h completos.
- **Errores de ASR esperables y sistemáticos:** «Barzalini» es **Baraa**; «shippet / shad / shajibet» es **ChatGPT**; «store procedure» es **stored procedure**; «CDS» es **CTAS**; «cities» es **CTEs**; «shajivity» es ChatGPT otra vez. El outline usa los términos correctos; las citas se dejan tal como salieron cuando el error no cambia el sentido.
- **Plataforma:** el curso es **SQL Server** (management studio, `GETDATE`, `TOP`, `ISNULL`, file groups). Portar a Postgres requiere traducir, no copiar.
- **La duración del reproductor (29:48:27) no coincide con el último capítulo:** `Thank You` cierra en 29:48:27, 107.307 s. El video es efectivamente 30 h.
- **Fecha de grabación:** el propio video se delata en el bloque de fechas — "currently it is July 18, 2024". Publicado en marzo de 2025.
- **Material descargable no verificado:** el enlace a `datawithbaraa.com/wiki/sql` se toma de la descripción; no se descargó ni se auditó el contenido.
- **Cobertura:** los 41 capítulos se leyeron; el outline condensa el transcript, no lo repite. Para los bloques de proyecto, el paso a paso real está en el video y en los scripts del curso.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
