# Bloque 1 — Qué es SQL y qué es una query

**Curso:** 00:07:38 – 00:34:01 (Introduction to SQL + entrada de Query Data)
**Sandbox:** `python3 run.py --reset` y después `python3 run.py -q "…"`

## La idea que ordena todo

SQL es **declarativo**: describís *qué* querés, el motor decide *cómo*. El mismo `SELECT` puede tardar milisegundos o segundos sin cambiar una coma, porque el "cómo" lo elige el optimizador. Todo lo demás del curso cuelga de acá.

## `SELECT` no modifica nada

```sql
SELECT id, name, phone
FROM people;
```

`SELECT` = qué columnas · `FROM` = de dónde · `;` = fin de la sentencia.

## Orden de escritura ≠ orden de evaluación

| Escribís | El motor evalúa |
|---|---|
| 1. `SELECT` | 4. proyecta columnas |
| 2. `FROM` | 1. lee las tablas |
| 3. `WHERE` | 2. filtra filas |
| 4. `GROUP BY` | 3. agrupa |

**Consecuencia práctica:** no podés usar un alias del `SELECT` dentro del `WHERE` (el alias todavía no existe cuando filtra), pero sí en `ORDER BY`.

## Ejercicio 1 — resuelto

```sql
-- 1. solo dos columnas
SELECT name, country FROM people;

-- 2. todas las columnas, con el atajo
SELECT * FROM people;

-- 3. dos conteos en una sola pasada
SELECT (SELECT COUNT(*) FROM orders) AS n_orders,
       (SELECT COUNT(*) FROM people) AS n_people;
```
→ 5 / 5. `*` es un atajo de exploración, no de producción: trae columnas que no necesitás y no se puede usar el resultado en un índice cubriente.

## La trampa del NULL (adelanto del Bloque 3)

```sql
SELECT name, phone FROM people WHERE phone != '11-5555-1001';
```
Devuelve **2 filas** (Carla, Diego), no 4. Bruno y Elena quedan afuera.

**Por qué:** `NULL` no es un valor, es la *ausencia* de valor. Toda comparación con `NULL` da `UNKNOWN`, y `WHERE` solo deja pasar `TRUE`. `NULL != 'x'` no es `TRUE`: es `UNKNOWN`, que se descarta.

La versión que sí trae los 4:

```sql
SELECT name FROM people WHERE phone IS NOT '11-5555-1001';
```

`IS NOT` compara identidad, no valor: trata el `NULL` como un caso que puede ser verdadero. Es la diferencia entre *"el teléfono es distinto de X"* y *"no es el caso de que el teléfono sea X"*.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

# Bloque 2 — `SELECT` a fondo

**Curso:** 00:34:01 – 01:32:31 (Query Data, 58 min — el bloque más largo del nivel Beginner)

## Alias: dónde sí y dónde no

```sql
SELECT name AS nombre, country AS pais FROM people ORDER BY nombre;
```
Funciona: `ORDER BY` corre después del `SELECT`.

```sql
SELECT name AS nombre FROM people WHERE nombre = 'Ana Pérez';
```
**En SQL Server y en SQL estándar esto falla.** El alias no existe todavía cuando el `WHERE` filtra.

**Ojo — trampa de herramienta:** SQLite **acepta** esa query (lo probé: devuelve 1 fila). Es una extensión suya, no SQL estándar. Si escribís así, el día que corras contra Postgres o SQL Server te explota. **Regla:** si el sandbox lo acepta pero el estándar no, no lo adoptes.

*Verificado:* MySQL Reference Manual B.3.4.4 — "Standard SQL disallows references to column aliases in a WHERE clause. This restriction is imposed because when the WHERE clause is evaluated, the column value may not yet have been determined."

## Las variantes que hay que tener en los dedos

```sql
-- todas las columnas (exploración, no producción)
SELECT * FROM people;

-- columnas repetidas en filas: DISTINCT
SELECT DISTINCT country FROM people;      -- AR, UY, CL  (3 filas)

-- ordenar y recortar
SELECT name, birth_date FROM people ORDER BY birth_date LIMIT 2;
-- SQL Server:  SELECT TOP 2 name, birth_date FROM ... ORDER BY ...
-- y en Postgres/SQLite: LIMIT 2 OFFSET 3

-- expresiones y concatenación
SELECT name, country || ' · ' || name AS etiqueta FROM people;
-- SQL Server: country + ' · ' + name   (|| no existe ahí)
```

`DISTINCT` actúa sobre **el conjunto de columnas que proyectás**, no sobre la primera. `SELECT DISTINCT country, name` devuelve 5 filas aunque solo haya 3 países.

**`LIMIT` sin `ORDER BY` no tiene sentido:** sin orden explícito, qué filas trae es decisión del motor y puede cambiar entre ejecuciones.

**Trampa del orden, probada:** `SELECT name, birth_date FROM people ORDER BY birth_date LIMIT 2` devuelve **Carla Ruiz (NULL) y Diego Sosa**. En SQLite el `NULL` va **primero** al ordenar ascendente; en Postgres va **último** (NULLS LAST es el default) y SQL Server también lo pone primero. Misma query, resultado distinto según el motor: si el orden importa, se explicita con `NULLS LAST`/`NULLS FIRST` (Postgres) o con `CASE WHEN col IS NULL THEN 1 ELSE 0 END` (portable).

## Por qué `*` es un atajo y no una costumbre

1. Trae columnas que no usás — más I/O, más memoria, más red.
2. Rompe el código cuando alguien agrega una columna.
3. No puede usar un **índice cubriente** (un índice que ya tiene todas las columnas pedidas y evita tocar la tabla). Ese concepto llega en el bloque de Indexes, pero la razón se siembra acá.

## Ejercicio 2 — resuelto

```sql
-- a. países distintos, ordenados alfabéticamente
SELECT DISTINCT country FROM people ORDER BY country;

-- b. los 3 nombres más largos
SELECT name, LENGTH(name) AS largo FROM people ORDER BY largo DESC LIMIT 3;

-- c. etiqueta legible por persona
SELECT id || ' — ' || name || ' (' || country || ')' AS ficha FROM people;
```
→ a: AR, CL, UY (3 filas) · b: **Elena Vidal (11)**, Bruno Díaz y Carla Ruiz (10) · c: 5 fichas.

**Nota:** a ojo conté Bruno como el nombre más largo y me equivoqué; `LENGTH()` lo desmiente. Elena Vidal son 11 caracteres porque el espacio cuenta. Es exactamente el motivo por el que se corre, no se estima.

**Pregunta de criterio:** en (b) `LENGTH(name)` cuenta caracteres en SQLite; en SQL Server se usa `LEN()` y **no** cuenta espacios finales. ¿Qué pasa con un nombre con espacio al final en cada motor? Esa es la clase de diferencia que después rompe un `GROUP BY`.

---

# Bloque 3 — `NULL`: el módulo de 68 minutos

**Curso:** 06:59:06 – 08:07:50 (NULL Functions)

## La definición, textual

> "a null means nothing unknown. It is not equal to anything. So it is not equal to zero or empty string or blank space."
> — `transcripcion.md` [6:59:44]

`NULL` = **ausencia de valor**. No es cero (cero es un número). No es `''` (eso es una cadena vacía de longitud 0). No es `FALSE`.

## Lógica de tres valores

Toda comparación con `NULL` devuelve `UNKNOWN`, no `TRUE` ni `FALSE`. Y `WHERE` solo deja pasar las filas donde la condición es `TRUE`.

| Expresión | Resultado |
|---|---|
| `NULL = NULL` | `UNKNOWN` |
| `NULL = 0` | `UNKNOWN` |
| `NULL != 'x'` | `UNKNOWN` |
| `NULL IS NULL` | **`TRUE`** |

*Probado en el sandbox:* `WHERE phone != '11-5555-1001'` devuelve 2 filas (Carla y Diego). Bruno y Elena —los dos con teléfono `NULL`— **no aparecen**, porque no cumplen `TRUE`: quedan en `UNKNOWN`.

## Las funciones que hay que saber

| Para | Postgres / SQLite | SQL Server |
|---|---|---|
| reemplazar `NULL` por un valor | `COALESCE(phone,'s/d')` | `ISNULL(phone,'s/d')` o `COALESCE` |
| `NULL` si es igual a X | `NULLIF(x, 0)` | `NULLIF(x, 0)` |
| preguntar | `IS NULL` / `IS NOT NULL` | igual |

`COALESCE` es estándar y acepta N argumentos (`COALESCE(a, b, c)` = el primero no nulo). `ISNULL` de SQL Server toma solo dos — si algún día lo portás, `COALESCE` es el camino.

`NULLIF(x, 0)` es el truco clásico para **evitar división por cero**: `amount / NULLIF(quantity, 0)` devuelve `NULL` en vez de reventar.

## Ejercicio 3 — resuelto

```sql
-- a. teléfono o 'sin dato'
SELECT name, COALESCE(phone, 'sin dato') AS contacto FROM people;

-- b. quiénes NO tienen teléfono (las dos formas)
SELECT name FROM people WHERE phone IS NULL;
SELECT name FROM people WHERE phone IS NOT NULL;   -- los otros 3

-- c. contar nulos y no nulos en una pasada
SELECT COUNT(*) AS total,
       COUNT(phone) AS con_telefono,          -- COUNT(col) IGNORA los NULL
       COUNT(*) - COUNT(phone) AS sin_telefono
FROM people;
```
→ 5 / 3 / 2. **`COUNT(*)` y `COUNT(col)` no son lo mismo:** `COUNT(*)` cuenta filas, `COUNT(col)` cuenta valores no nulos. Es el error más común en un primer reporte.

**Trampa para probar:** `SELECT AVG(amount) FROM orders WHERE amount > 0;` — si metés un `WHERE` que descarta filas por un `NULL`, el promedio se calcula sobre otro denominador. Los agregados ignoran `NULL` **salvo `COUNT(*)`**.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

# Bloque 4 — DDL: la estructura antes que los datos

**Curso:** 01:32:31 – 01:43:44 (DDL Commands)

DDL = **Data Definition Language**: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`. Define la *forma* de la base, no su contenido.

```sql
CREATE TABLE products (
    id      INTEGER PRIMARY KEY,
    name    TEXT    NOT NULL,
    price   REAL    NOT NULL,
    stock   INTEGER DEFAULT 0,
    created TEXT
);
```

Tres piezas de la definición que no son decorativas:

| Pieza | Qué garantiza | Qué pasa si falta |
|---|---|---|
| `NOT NULL` | la columna siempre tiene valor | entra `NULL` y las comparaciones empiezan a mentir |
| `DEFAULT` | valor si no se especifica | queda `NULL` (que no es lo mismo que dejar el default vacío) |
| `PRIMARY KEY` | identidad única y no nula | duplicados silenciosos |

**Probado en el sandbox:** `INSERT INTO products (name, price) VALUES (NULL, 10);` → `sqlite3.IntegrityError: NOT NULL constraint failed: products.name`. La constraint no es documentación: es el motor frenando el dato malo antes de que entre.

```sql
-- agregar una columna a una tabla con datos
ALTER TABLE products ADD COLUMN category TEXT;

-- borrar estructura (y sus datos, sin vuelta)
DROP TABLE perifericos;
```

**Equivalencias entre motores:** `INTEGER PRIMARY KEY` en SQLite autoincrementa. En SQL Server es `INT IDENTITY(1,1) PRIMARY KEY`; en Postgres, `SERIAL PRIMARY KEY` (o `GENERATED ALWAYS AS IDENTITY`, preferido hoy). Los tipos también cambian: `TEXT` de SQLite vs `NVARCHAR(100)` de SQL Server vs `VARCHAR`/`TEXT` de Postgres.

---

# Bloque 5 — DML: meter y cambiar datos

**Curso:** 01:43:44 – 02:08:03 (DML Commands)

DML = `INSERT`, `UPDATE`, `DELETE`, y `SELECT` cuando se lo agrupa como lenguaje de manipulación.

```sql
-- insert de varias filas en una
INSERT INTO products (name, price) VALUES ('Teclado', 45.5), ('Mouse', 22.0), ('Monitor', 199.99);

-- insert desde el resultado de otra tabla (el segundo método del curso)
INSERT INTO perifericos (name, price)
SELECT name, price FROM products WHERE category = 'periférico';

-- update acotado
UPDATE products SET category = 'periférico' WHERE name IN ('Teclado', 'Mouse');

-- delete acotado
DELETE FROM products WHERE name = 'Monitor';
```

**El peligro real de DML no es la sintaxis, es el `WHERE` que falta.** Un `UPDATE products SET stock = 0` sin `WHERE` toca las 3 filas y no pide confirmación. Un `DELETE FROM orders` deja la tabla vacía.

**Protocolo que voy a exigirte de acá en adelante, y que después va derecho a la skill:** antes de un `UPDATE`/`DELETE`, correr el mismo filtro como `SELECT COUNT(*)`. Si el número no es el que esperabas, no se ejecuta.

```sql
SELECT COUNT(*) FROM products WHERE name = 'Monitor';   -- 1 → adelante
```
Probado: el conteo previo al `DELETE` daba 1 y el `DELETE` afectó exactamente 1. El mismo conteo sobre "un update sin where" daba 3, que es la señal de alarma.

**Detalle de SQLite:** el runner hace commit explícito. En otros motores, sin `COMMIT` la transacción no persiste — y `DELETE` no tiene `UNDO`. Antes de un DML destructivo en algo que no sea el sandbox: backup o transacción con `ROLLBACK` ensayado.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

# Bloque 6 — Filtrar datos

**Curso:** 02:08:03 – 02:47:57 (Filtering Data)

```sql
-- AND / OR / IS NOT NULL
SELECT name, country FROM people
WHERE country = 'AR' AND birth_date IS NOT NULL;

-- BETWEEN es inclusivo en los dos extremos
SELECT id, amount FROM orders WHERE amount BETWEEN 100 AND 400;   -- 150 y 300

-- IN reemplaza una cadena de OR
SELECT name, city FROM customers WHERE city IN ('Córdoba', 'Montevideo');

-- LIKE: % = cualquier cantidad de caracteres, _ = exactamente uno
SELECT name FROM people WHERE name LIKE 'A%';      -- Ana Pérez
SELECT name FROM people WHERE name LIKE '%Ruiz%';  -- Carla Ruiz
```

## La trampa que más bugs produce: precedencia de `AND` sobre `OR`

```sql
SELECT name, country, birth_date FROM people
WHERE country = 'AR' OR country = 'UY' AND birth_date IS NULL;
```
El motor lee `A OR (B AND C)`, no `(A OR B) AND C`. **Devuelve 4 filas:** todos los de AR (sin importar la fecha) más Carla (UY + sin fecha).

Si la intención es "argentinos y uruguayos sin fecha de nacimiento":

```sql
WHERE (country = 'AR' OR country = 'UY') AND birth_date IS NULL
```
→ **1 fila** (Carla).

**Regla:** si en un `WHERE` hay un `OR`, van paréntesis. Siempre. Aunque no haga falta.

---

# Bloque 7 — Joins (básicos)

**Curso:** 02:47:57 – 03:27:29

Un join combina **columnas** de dos tablas. (Los set operators del bloque 8 combinan **filas** — esa distinción vale tenerla desde ahora.)

```sql
SELECT c.name, o.id, o.amount
FROM customers c
INNER JOIN orders o ON o.customer_id = c.id;
```

**El dataset tiene un dato de prueba escondido:** `orders` tiene una orden con `customer_id = 5`, y `customers` solo llega a id 3. Esa orden **no tiene cliente**.

| Tipo | Qué devuelve | Probado |
|---|---|---|
| `INNER JOIN` | solo las filas que matchean en las dos | **4 filas** — la orden huérfana desaparece |
| `LEFT JOIN` desde `customers` | todos los clientes, con o sin pedidos | 3 filas |
| `LEFT JOIN` desde `orders` | todos los pedidos, con o sin cliente | **5 filas** — el huérfano aparece con `name = NULL` |

Ese es el uso legítimo del `LEFT JOIN`: **encontrar lo que falta**. Si querés detectar datos huérfanos:

```sql
SELECT o.id, o.amount
FROM orders o LEFT JOIN customers c ON c.id = o.customer_id
WHERE c.id IS NULL;   -- → orden 4, 300.00, sin cliente
```

## Dos trampas que el curso marca y que acá se ven

**1. `COUNT(*)` en un `LEFT JOIN` miente.** Si un cliente no tiene pedidos, `LEFT JOIN` le crea **una fila con `NULL`**, y `COUNT(*)` la cuenta como 1.

```sql
SELECT c.name, COUNT(*) AS count_star, COUNT(o.id) AS count_o ...
```
→ En este dataset todos tienen pedidos, así que ambos dan igual. **Pero si agregás un cliente sin pedidos:** `count_star` da 1, `count_o` da 0. `COUNT(col)` ignora `NULL`; `COUNT(*)` cuenta filas. En un `LEFT JOIN` esa diferencia es la respuesta correcta vs. el bug de reporte.

**2. El join no filtra cardinalidad, la expone.** Si `customers` tuviera dos filas con el mismo `id`, cada pedido aparecería dos veces y el total se duplicaría. Un join es una operación sobre conjuntos: si las claves no son únicas del lado derecho, las filas se multiplican. Antes de sumar, se verifica que la clave del lado "uno" sea única.

## Ejercicio 7 — resuelto

```sql
-- total por cliente, incluyendo los que no compraron
SELECT c.name,
       r.name AS region,
       COUNT(o.id) AS pedidos,
       COALESCE(SUM(o.amount), 0) AS total
FROM customers c
LEFT JOIN people p   ON p.name = c.name
LEFT JOIN regions r  ON r.name = p.country
LEFT JOIN orders o   ON o.customer_id = c.id
GROUP BY c.name, r.name
ORDER BY total DESC;
```
→ Bruno 1200.0 · Ana 239.5 · Carla 45.0. El `COALESCE(SUM(...), 0)` es obligatorio: sin pedidos, `SUM` devuelve `NULL` y el total se ve vacío en vez de 0.

`FULL OUTER JOIN` existe en SQLite ≥ 3.39, Postgres y SQL Server; no existe en MySQL (se simula con `UNION` de dos `LEFT JOIN`).

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

# Bloque 8 — Set operators: combinar filas

**Curso:** 04:02:09 – 04:47:41

Joins combinan **columnas**; set operators combinan **filas**. Las dos consultas tienen que tener la misma cantidad de columnas y tipos compatibles (el nombre del resultado lo da la primera).

```sql
-- UNION: saca duplicados
SELECT country FROM people UNION SELECT name FROM regions ORDER BY 1;
-- → AR, BR, CL, UY  (4)

-- UNION ALL: no saca nada (más barato)
SELECT country FROM people UNION ALL SELECT country FROM people;
-- → 10 filas (los 5 de nuevo)
```

**La diferencia no es cosmética:** `UNION` tiene que ordenar o hashear todo para deduplicar. `UNION ALL` solo concatena. **Si sabés que no hay duplicados, `UNION ALL` es la respuesta correcta** y a veces la única viable sobre millones de filas.

```sql
-- EXCEPT: lo que está en la primera y no en la segunda
SELECT name FROM regions EXCEPT SELECT country FROM people;
-- → BR

-- INTERSECT: lo que está en las dos
SELECT country FROM people INTERSECT SELECT name FROM regions;
-- → AR, CL, UY
```

**Trampa del NULL:** `EXCEPT` e `INTERSECT` tratan dos `NULL` como *iguales* para decidir pertenencia — lo contrario de `=`. Si el conjunto tiene nulos, el resultado puede sorprender.

`MINUS` en Oracle es `EXCEPT`. MySQL no tiene `INTERSECT`/`EXCEPT` hasta 8.0.31; antes se simulaban con `IN`/`NOT IN` o joins.

---

# Bloque 9 — `CASE` y agregados

**Curso:** 08:07:50 – 08:50:11 (Case Statement + Aggregate Functions)

## `CASE`: el `if` de SQL, y se puede usar en cualquier cláusula

```sql
SELECT id, amount,
       CASE WHEN amount >= 500 THEN 'alto'
            WHEN amount >= 100 THEN 'medio'
            ELSE 'bajo' END AS tramo
FROM orders;
```
→ 1200 = alto · 300 y 150 = medio · 89.5 y 45 = bajo.

**El orden de los `WHEN` importa:** se evalúan de arriba abajo y **gana el primero que da verdadero**. Sin `ELSE`, el resultado es `NULL` — no `FALSE`.

**Caso portable:** ordenar con los `NULL` al final sin depender del motor:

```sql
SELECT name, birth_date FROM people
ORDER BY CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END, birth_date;
```
→ Diego, Bruno, Ana, Elena, y **Carla al final**. Ese `CASE` es el `NULLS LAST` portátil.

**`CASE` también sirve para contar condicionalmente** — el patrón de pivote:

```sql
SELECT COUNT(CASE WHEN amount >= 500 THEN 1 END) AS altos,
       COUNT(CASE WHEN amount < 500 THEN 1 END)  AS resto
FROM orders;
```
→ 1 y 4. (Sí: también se puede con `SUM(CASE WHEN … THEN 1 ELSE 0 END)`.)

## Agregados

```sql
SELECT COUNT(*) AS n, ROUND(SUM(amount),2) AS total,
       ROUND(AVG(amount),2) AS promedio, MIN(amount) AS minimo, MAX(amount) AS maximo
FROM orders;
```
→ 5 · 1784.5 · 356.9 · 45.0 · 1200.0

| Regla | Detalle |
|---|---|
| `COUNT(*)` cuenta filas | incluidos los `NULL` |
| el resto **ignora `NULL`** | `AVG` promedia solo valores no nulos: divide por `COUNT(col)`, no por `COUNT(*)` |
| agregados sin `GROUP BY` | devuelven **una sola fila**, aunque la tabla tenga 0 filas (`COUNT` = 0, `SUM` = `NULL`) |
| combinarlos con columnas | sin `GROUP BY` falla: no se puede mezclar una columna con un agregado en el mismo `SELECT` |

**El error que más se ve:** `AVG(amount)` con `NULL` en la columna da un promedio más alto del que parece, porque el divisor es más chico. Si el `NULL` significa "cero" para el negocio, hay que decidirlo explícitamente con `COALESCE(amount, 0)`.

**`GROUP BY` lo cubro en el bloque 12** (Window Functions), porque el curso mete `GROUP BY` junto con las ventanas para poder contrastarlos: `GROUP BY` **colapsa** filas, la ventana **las conserva**.

## Sandbox

`regions` (AR, UY, CL, BR) quedó incorporada a `01-setup.sqlite.sql`, así que `--reset` la recrea. Corrigo acá un aviso anterior: sí se perdía, y no debía.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
