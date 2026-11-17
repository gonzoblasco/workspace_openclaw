TOTAL: 235.74

Filas excluidas o deduplicadas:
- Fila 4 (`id=3`, 2026-08-01, USD, 99.99) — duplicado de `id=3`; se contó solo la primera aparición.
- Fila 5 (`id=4`, 2026-08-20, EUR, 250.00) — moneda distinta de USD.
- Fila 8 (`id=7`, 2026-10-01, USD, 999.00) — fuera del rango 2026-Q3 (posterior al 30/09).

Incluidas: `id=1` (120.50), `id=2` (-30.00), `id=3` (99.99), `id=5` (0.00), `id=6` (45.25, 30/09 inclusive) → 120.50 − 30.00 + 99.99 + 0.00 + 45.25 = **235.74**.