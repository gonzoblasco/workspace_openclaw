# Caso 2 - `date_range`

Módulo `daterange.py`, stdlib only, type hints y docstrings en funciones públicas.

## API
- `month_end(year: int, month: int) -> date` - último día del mes dado.
- `add_months(d: date, n: int) -> date` - suma `n` meses conservando el "fin de mes" si el original era fin de mes.
- `is_leap(year: int) -> bool`
- `daterange(start: date, end: date) -> list[date]` - lista de fechas en `[start, end)`.
- `parse_iso(s: str) -> date`

## Comportamiento requerido
1. `month_end` maneja meses de 30, 31 y febrero (bisiesto y no bisiesto).
2. `add_months` con `n` negativo resta meses. Si la fecha original era el último día de su mes, el resultado también debe ser el último día del mes destino (clampeo, no overflow).
3. `daterange` es **half-open**: `[start, end)`. Si `start == end`, devuelve lista vacía. Si `start > end`, lanza `ValueError` (no lista vacía silenciosa).
4. `parse_iso` acepta `YYYY-MM-DD` y lanza `ValueError` con mensaje claro ante input inválido.

## Criterios de aceptación
- `month_end(2024, 2) == date(2024, 2, 29)`; `month_end(2023, 2) == date(2023, 2, 28)`.
- `month_end(2023, 4) == date(2023, 4, 30)`.
- `add_months(date(2023,1,31), 1) == date(2023,2,28)` (fin de mes clampeado).
- `add_months(date(2023,3,31), -1) == date(2023,2,28)`.
- `daterange(date(2023,1,1), date(2023,1,1)) == []`.
- `daterange(date(2023,1,2), date(2023,1,1))` lanza `ValueError`.
- `daterange` sobre un rango que cruza el 29/02 de 2024 incluye ese día y el conteo es correcto.
