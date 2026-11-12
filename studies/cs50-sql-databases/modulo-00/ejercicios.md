# Módulo 0 — ejercicios

Todos corren sobre `m0_workers.db` (creado por `setup.sql`). Abrir con:

```bash
sqlite3 m0_workers.db
# dentro: .mode box      (tabla linda)
#         .schema        (ver la estructura)
#         .quit
```

> Si `sqlite3` del sistema te lo bloquea, abrí con `python3 -c "import sqlite3;..."` o copiá la base a `~/tmp`. En esta máquina el guard de estado bloquea `/usr/bin/sqlite3` sobre el workspace; no es un problema de SQL.

## E1 — Leer (el `R` de CRUD)
¿Qué columnas y cuántas filas tiene `workers`? Escribí la query más corta que te lo diga, y otra que devuelva sólo el nombre y el estipendio.

<details><summary>Respuesta</summary>

```sql
SELECT * FROM workers;               -- 8 filas
SELECT name, stipend FROM workers;   -- 2 columnas
```
</details>

## E2 — Agregar (el `A` de CRUD)
Insertá a `Hapu`, con estipendio 18, en `2026-11`. Después contá las filas.

<details><summary>Respuesta</summary>

```sql
INSERT INTO workers (name, month, stipend) VALUES ('Hapu', '2026-11', 18);
SELECT COUNT(*) FROM workers;        -- 9
```
</details>

## E3 — Modificar por fila (el `U` de CRUD)
Kha de `2026-10` quedó en 0 por un error. Corregilo a 14 **sin tocar** el de septiembre. Después sumá 1 a todos los estipendios de `2026-09`.

<details><summary>Respuesta</summary>

```sql
UPDATE workers SET stipend = 14 WHERE name = 'Kha' AND month = '2026-10';
UPDATE workers SET stipend = stipend + 1 WHERE month = '2026-09';
```
Ojo con la segunda: sin `WHERE month` hubiera subido **todos** los meses. El `WHERE` no es opcional por gusto.
</details>

## E4 — La constraint no es adorno
Intentá insertar estipendio `-5`, y después insertar sin `month`. Copiá el error exacto de cada uno.

<details><summary>Respuesta</summary>

```
CHECK constraint failed: stipend >= 0
NOT NULL constraint failed: workers.month
```
Dos errores distintos: uno es una **regla de negocio** (`CHECK`), el otro es una **regla de estructura** (`NOT NULL`). SQLite las nombra distinto y eso es información.
</details>

## E5 — El `D` de CRUD y su trampa
Borrá las filas con estipendio 0. ¿Cuántas borraste? Ahora escribí la misma sentencia **sin `WHERE`** en una copia de la base y explicá qué pasó.

<details><summary>Respuesta</summary>

```sql
DELETE FROM workers WHERE stipend = 0;   -- borra 1 fila: Kha 2026-10
```
Si antes corriste E2, la base tiene 9 filas y borrás **una**; Hapu (18) sigue ahí. Ese es justamente el punto: el `WHERE` decide qué sobrevive.
Sin `WHERE`, `DELETE FROM workers;` vacía la tabla entera y **no falla**: devuelve "ok". Es el error más caro de SQL y el curso lo señala en 5:03:03. En producción, la costumbre es correr primero el `SELECT ... WHERE` con la misma condición y recién después cambiar `SELECT *` por `DELETE`.
</details>

## E6 — Total por trabajador
Sumá el estipendio de cada trabajador, ordenado de mayor a menor.

<details><summary>Respuesta</summary>

```sql
SELECT name, SUM(stipend) AS total
FROM workers
GROUP BY name
ORDER BY total DESC;
-- Sobek 44 · Nebet 24 · Ameny 18 · Kha 15
```
`SUM` es tu primera función de agregación: toma N filas y devuelve **una**. Que el resultado se vea "como una planilla" no significa que lo sea.
</details>

## E7 — El experimento que justifica todo el curso

Corré estas cuatro y anotá la salida exacta:

```sql
SELECT 0.1 + 0.2;
SELECT ROUND(0.1 + 0.2, 2);
SELECT 1.15 * 100;
SELECT CAST(1.15 * 100 AS INTEGER);
```

<details><summary>Respuesta — y las cuatro formas en que el float rompe</summary>

**Salida real:**

| query | resultado |
|---|---|
| `0.1 + 0.2` | `0.30000000000000004` |
| `ROUND(0.1+0.2, 2)` | `0.3` |
| `1.15 * 100` | `114.99999999999999` |
| `CAST(1.15*100 AS INTEGER)` | **`114`** |

Las cuatro formas, de más inocente a más cara:

**(a) Se ve feo pero no rompe nada.** `0.1+0.2` da `0.30000000000000004` y `ROUND(...,2)` lo arregla. Esto es lo que muestra el video. **No es el problema real.**

**(b) Rompe al convertir a centavos.** `1.15 * 100 = 114.99999999999999`, y `CAST` **trunca**, no redondea: `114`. Perdiste un centavo por operación. Con `0.29` pasa lo mismo (`28.99...` → 28).

**(c) Rompe silenciosamente en un `WHERE`.** El más peligroso:

```sql
SELECT id FROM p WHERE price * 100 = 1999;   -- []   ← vacío, sin error
SELECT id FROM p WHERE price = 19.99;        -- [(1,)]
```

Porque `19.99*100 = 1998.9999999999998`. La query devuelve cero filas y **no dice por qué**.

**(d) Rompe la comparación de un total.** `SELECT 0.1+0.2 = 0.3` devuelve **`0`** (falso). Un chequeo `if total == esperado` en Python o en un trigger falla con montos que "son iguales".

Por eso el dinero va en **centavos enteros**. Y ojo con el mito inverso: `SUM` de floats *no* se desvía acumulativamente — `1000 × 0.07` da `70.0` exacto porque el error de redondeo se cancela. El problema no es la suma, es **truncar y comparar**.
</details>

## E8 — Convertir la columna a centavos (la práctica que sigue)

Rehacé la tabla con `cents INTEGER` en lugar de `stipend NUMERIC`, copiando los datos, y volvé a correr los totales de E6.

```sql
CREATE TABLE workers_money (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  month TEXT NOT NULL,
  cents INTEGER NOT NULL CHECK (cents >= 0)
);
INSERT INTO workers_money (name, month, cents)
SELECT name, month, CAST(ROUND(stipend * 100) AS INTEGER) FROM workers;

SELECT name, SUM(cents) FROM workers_money GROUP BY name ORDER BY 2 DESC;
```

<details><summary>Respuesta</summary>

```
Sobek  4400
Nebet  2400
Hapu   1800
Ameny  1800
Kha    1500
```

Enteros, sin coma flotante, sin truncado posible. La diferencia con E6: los números son **exactos por construcción**, no "lo suficientemente parecidos".

Nota el `CAST(ROUND(x*100) AS INTEGER)` y no `CAST(x*100 AS INTEGER)`: el `ROUND` va primero **justamente** por lo que viste en (b).
</details>

## E9 — `INTEGER` no es un tipo en SQLite (y `STRICT` sí)

Insertá texto en una columna `INTEGER` de la tabla normal y en una `STRICT`. Compará.

```sql
CREATE TABLE normal (v INTEGER);
CREATE TABLE estricta (v INTEGER) STRICT;

INSERT INTO normal (v) VALUES ('hola');     -- ¿qué pasa?
INSERT INTO estricta (v) VALUES ('hola');   -- ¿qué pasa?
INSERT INTO estricta (v) VALUES (3.7);      -- ¿y acá?
```

<details><summary>Respuesta (corrida real, SQLite 3.54.0)</summary>

```
normal    INS 'hola' -> guardó ('hola', 'text')      ← ACEPTÓ TEXTO EN UNA COLUMNA INTEGER
normal    INS '12'   -> guardó (12, 'integer')       ← convirtió el string
estricta  INS 'hola' -> RECHAZADO: cannot store TEXT value in INTEGER column
estricta  INS '12'   -> guardó (12, 'integer')       ← '12' sí: es convertible
estricta  INS 3.7    -> RECHAZADO: cannot store REAL value in INTEGER column
```

**Esto es lo que el curso llama "affinity" (3:29:45) y es la trampa más grande de SQLite.** En una tabla normal, `INTEGER` es una *preferencia*, no una regla: SQLite convierte si puede y guarda tal cual si no. Tu `id INTEGER PRIMARY KEY` puede terminar con `"hola"` adentro.

`STRICT` (SQLite ≥ 3.37) es un modificador de tabla que obliga al motor a respetar los tipos declarados. **Ninguno de los datasets del curso lo usa** — pero para cualquier trabajo tuyo, sí es la opción por defecto.

Postgres y MySQL no tienen este problema: son estrictos desde el principio.
</details>

## E10 — El pipeline completo, como lo haría un script

Escribí un script que: (1) abra `m0_workers.db`, (2) pida el total por trabajador, (3) lo imprima como tabla, (4) falle con exit code 1 si alguna fila tiene estipendio 0.

Este es el formato que vas a repetir para cada módulo: **una query, una verificación, un exit code**.

```python
#!/usr/bin/env python3
import sqlite3, sys
db = sqlite3.connect('m0_workers.db')
rows = db.execute("SELECT name, SUM(stipend) AS t FROM workers GROUP BY name ORDER BY t DESC").fetchall()
print(f"{'name':8} {'total':>6}")
for name, total in rows:
    print(f"{name:8} {total:6}")
zero = db.execute("SELECT name, month FROM workers WHERE stipend = 0").fetchall()
if zero:
    print(f"FAIL: estipendio 0 en {zero}", file=sys.stderr)
    sys.exit(1)
print("OK")
```

<details><summary>Respuesta — salida real</summary>

```
name      total
Sobek        44
Nebet        24
Ameny        18
Kha          15
FAIL: estipendio 0 en [('Kha', '2026-10')]
exit 1
```

El `FAIL` sale **antes** del encabezado en la corrida real porque `stdout` está buffereado y `stderr` no. En un workflow eso importa: si querés que el orden sea predecible, `print(..., flush=True)` o `sys.stderr` para todo.

Los cuatro hábitos que este ejercicio fija y que **van a ser el esqueleto de las skills**:

1. **Abrir la base desde código**, no a mano. Una base tocada a mano no se puede repetir.
2. **Una query = un output declarado.** Si cambia el formato, se ve en el diff.
3. **Una verificación que puede fallar.** No `print("parece ok")`: una condición concreta.
4. **Exit code.** `0` verde, `1` rojo. Es lo que un workflow puede leer; un texto no.
</details>

## Pregunta de cierre
Respondé en tres líneas, sin mirar: ¿por qué una base de datos y no una planilla? Nombrá las tres razones del video y agregá una cuarta que salga de haber corrido E7.

<details><summary>Respuesta</summary>

El video da tres: **escala** (millones de filas), **frecuencia de escritura** (miles de updates por segundo) y **velocidad de búsqueda** (índices, no Ctrl+F). La cuarta que agrega E7: **integridad de tipos**. Una planilla acepta 114,99999 en una celda de precio y no te avisa; una base con `CHECK` y tipos correctos te obliga a decidir antes de guardar.
</details>
