-- Módulo 0 — base de práctica del CS50 SQL (reconstruida, no la del curso)
-- Uso:  sqlite3 m0_workers.db < setup.sql
DROP TABLE IF EXISTS workers;
CREATE TABLE workers (
    id      INTEGER PRIMARY KEY,
    name    TEXT    NOT NULL,
    month   TEXT    NOT NULL,
    stipend NUMERIC NOT NULL CHECK (stipend >= 0)
);
INSERT INTO workers (name, month, stipend) VALUES
    ('Nebet', '2026-09', 12),
    ('Nebet', '2026-10', 12),
    ('Kha',   '2026-09', 15),
    ('Kha',   '2026-10',  0),
    ('Ameny', '2026-09',  9),
    ('Ameny', '2026-10',  9),
    ('Sobek', '2026-09', 22),
    ('Sobek', '2026-10', 22);
