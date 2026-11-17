TOTAL: 235.74

Filas excluidas / deduplicadas:
- `3,2026-08-01,USD,99.99` (segunda aparición) — deduplicada: el id 3 ya fue contado en su primera aparición.
- `4,2026-08-20,EUR,250.00` — excluida: moneda EUR, solo se suman USD.
- `7,2026-10-01,USD,999.00` — excluida: fecha fuera del rango 2026-Q3 (1 de julio – 30 de septiembre).

Nota: la fila `5,2026-09-10,USD,0.00` sí se incluyó (es USD y está en rango), pero no altera el total por ser monto 0.00.