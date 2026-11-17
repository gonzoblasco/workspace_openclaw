TOTAL: 235.74

Filas excluidas / deduplicadas:
- `3,2026-08-01,USD,99.99` (segunda aparición): deduplicada, el id 3 ya fue contado en su primera aparición.
- `4,2026-08-20,EUR,250.00`: excluida por moneda distinta de USD.
- `7,2026-10-01,USD,999.00`: excluida por fecha fuera del rango 2026-Q3 (es 2026-10-01).

Detalle del cálculo (filas incluidas):
- id 1: +120.50
- id 2: −30.00 (reembolso, se suma tal cual)
- id 3: +99.99
- id 5: +0.00 (incluida, no afecta el total)
- id 6: +45.25
- Suma: 120.50 − 30.00 + 99.99 + 0.00 + 45.25 = **235.74**