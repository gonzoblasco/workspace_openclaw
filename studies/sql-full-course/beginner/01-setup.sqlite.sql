-- Setup del sandbox: SQLite (el curso es SQL Server; acá va la traducción)
-- Ejecutar con python: ver `run.py` en esta carpeta.

DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;

CREATE TABLE people (
    id          INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    birth_date  TEXT,
    phone       TEXT,
    country     TEXT
);

INSERT INTO people (id, name, birth_date, phone, country) VALUES
 (1, 'Ana Pérez',      '1990-03-12', '11-5555-1001', 'AR'),
 (2, 'Bruno Díaz',     '1985-07-01', NULL,           'AR'),
 (3, 'Carla Ruiz',     NULL,         '11-5555-1003', 'UY'),
 (4, 'Diego Sosa',     '1978-11-23', '11-5555-1004', 'CL'),
 (5, 'Elena Vidal',    '1995-01-09', NULL,           'AR');

CREATE TABLE customers (
    id     INTEGER PRIMARY KEY,
    name   TEXT NOT NULL,
    city   TEXT
);
INSERT INTO customers (id, name, city) VALUES
 (1, 'Ana Pérez',  'Buenos Aires'),
 (2, 'Bruno Díaz', 'Córdoba'),
 (3, 'Carla Ruiz',  'Montevideo');

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    amount      REAL    NOT NULL,
    order_date  TEXT    NOT NULL
);
INSERT INTO orders (id, customer_id, amount, order_date) VALUES
 (1, 1,  150.00, '2026-01-05'),
 (2, 1,   89.50, '2026-02-11'),
 (3, 2, 1200.00, '2026-02-20'),
 (4, 5,  300.00, '2026-03-02'),
 (5, 3,   45.00, '2026-03-15');

CREATE TABLE regions (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
INSERT INTO regions (id, name) VALUES (1,'AR'),(2,'UY'),(3,'CL'),(4,'BR');
