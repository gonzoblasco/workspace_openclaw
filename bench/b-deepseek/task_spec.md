# Unidad U1 - Endpoint de reportes con caché y paginación

Implementá un módulo de reportes en Python (stdlib only) con estos requisitos:

## Requisitos
1. `fetch_reports(session, page, per_page)` - trae una página de reportes desde la API.
2. `filter_by_date(reports, since, until)` - filtra por fecha inclusiva en ambos extremos.
3. `paginate(items, page, per_page)` - pagina en base 1 (page 1 es la primera).
4. `cached_reports(session, page, per_page, ttl_seconds, now)` - cachea el resultado por `ttl_seconds`.
5. `summarize(reports)` - devuelve `{"count": N, "total_amount": X, "by_status": {...}}`.

## Criterios de aceptación
- `paginate` con `page` fuera de rango devuelve lista vacía (no lanza).
- `per_page` inválido (0, negativo o no int) lanza `ValueError`.
- `cached_reports` no devuelve un valor cacheado más viejo que `ttl_seconds`.
- `filter_by_date` es inclusivo en `since` y en `until`.
- Todo debe ser testeable sin red (inyectá la sesión).

## Restricciones
- Solo stdlib.
- Type hints en todas las funciones públicas.
- Docstrings en todas las funciones públicas.
- Tests con `unittest`, en `test_reports.py`, cubriendo los criterios de aceptación.
