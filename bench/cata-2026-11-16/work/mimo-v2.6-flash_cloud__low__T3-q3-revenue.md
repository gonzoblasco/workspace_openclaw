TOTAL: 235.74

Filas excluidas o deduplicadas:
- `3,2026-08-01,USD,99.99` (segunda aparición) → id repetido, se contó solo la primera.
- `4,2026-08-20,EUR,250.00` → moneda no USD.
- `7,2026-10-01,USD,999.00` → fuera de 2026-Q3 (después del 30/09).

Filas incluidas: 1 (120.50), 2 (−30.00), 3 (99.99), 5 (0.00), 6 (45.25) → 120.50 − 30.00 + 99.99 + 0.00 + 45.25 = 235.74.