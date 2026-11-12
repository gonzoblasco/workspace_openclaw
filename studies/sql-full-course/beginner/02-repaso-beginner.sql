-- Repaso ejecutable del Nivel Beginner. Datos: el sandbox del curso.
-- Correr: python3 run.py --reset   y luego pegar los bloques, o usar -q.

-- ---------- SELECT ----------
SELECT name, country FROM people;                       -- 5 filas
SELECT * FROM people;

-- ---------- Alias ----------
SELECT name AS nombre FROM people ORDER BY nombre;       -- OK
-- SELECT name AS nombre FROM people WHERE nombre='Ana'; -- SQL Server: FALLA. SQLite: lo acepta (no portable)

-- ---------- DISTINCT ----------
SELECT DISTINCT country FROM people;                     -- 3: AR, UY, CL
SELECT DISTINCT country, name FROM people;               -- 5: DISTINCT es sobre todo el conjunto

-- ---------- NULL ----------
SELECT name FROM people WHERE phone != '11-5555-1001';   -- 2 filas, NO 4
SELECT name FROM people WHERE phone IS NOT '11-5555-1001'; -- 4 filas
SELECT name, COALESCE(phone,'sin dato') FROM people;
SELECT COUNT(*) AS total, COUNT(phone) AS con_tel FROM people; -- 5 / 3

-- ---------- Filtros ----------
SELECT name FROM people WHERE country='AR' AND birth_date IS NOT NULL;  -- 3
SELECT id FROM orders WHERE amount BETWEEN 100 AND 400;                 -- 2 filas: 150, 300
SELECT name FROM customers WHERE city IN ('Córdoba','Montevideo');      -- 2
-- Precedencia: AND antes que OR
SELECT name FROM people WHERE country='AR' OR country='UY' AND birth_date IS NULL;        -- 4 (!)
SELECT name FROM people WHERE (country='AR' OR country='UY') AND birth_date IS NULL;      -- 1

-- ---------- Joins ----------
SELECT c.name, o.id FROM customers c INNER JOIN orders o ON o.customer_id=c.id;   -- 4
SELECT o.id FROM orders o LEFT JOIN customers c ON c.id=o.customer_id WHERE c.id IS NULL; -- 1: huérfana
SELECT c.name, COUNT(o.id) FROM customers c LEFT JOIN orders o ON o.customer_id=c.id GROUP BY c.name;

-- ---------- Set operators (requiere regions: ver 01-setup.sqlite.sql) ----------
SELECT country FROM people UNION ALL SELECT name FROM regions;   -- 9 filas
SELECT country FROM people UNION SELECT name FROM regions;       -- 4
SELECT name FROM regions EXCEPT SELECT country FROM people;      -- BR
SELECT country FROM people INTERSECT SELECT name FROM regions;   -- AR, CL, UY

-- ---------- CASE ----------
SELECT id, amount, CASE WHEN amount>=500 THEN 'alto' WHEN amount>=100 THEN 'medio' ELSE 'bajo' END AS tramo
FROM orders;                                                     -- 1 alto, 2 medio, 2 bajo
SELECT COUNT(CASE WHEN amount>=500 THEN 1 END) AS altos FROM orders;  -- 1

-- ---------- Agregados ----------
SELECT COUNT(*), ROUND(SUM(amount),2), ROUND(AVG(amount),2) FROM orders;  -- 5, 1784.5, 356.9

-- ---------- DDL / DML ----------
CREATE TABLE IF NOT EXISTS demo (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL DEFAULT 0);
INSERT INTO demo (name, price) VALUES ('x', 1), ('y', 2);
UPDATE demo SET price = price * 2 WHERE name='x';
SELECT COUNT(*) FROM demo WHERE name='y';   -- antes de borrar
DELETE FROM demo WHERE name='y';
DROP TABLE demo;
