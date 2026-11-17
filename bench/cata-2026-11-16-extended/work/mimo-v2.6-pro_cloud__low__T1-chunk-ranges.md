```python
from datetime import date, timedelta


def chunk_ranges(start: str, end: str, days: int) -> list[tuple[str, str]]:
    """Parte el rango inclusivo [start, end] en tramos consecutivos e inclusivos
    de a lo sumo `days` días cada uno.

    Args:
        start: fecha inicial ISO 'YYYY-MM-DD'.
        end: fecha final ISO 'YYYY-MM-DD' (inclusiva).
        days: longitud máxima de cada tramo, en días (>= 1).

    Returns:
        Lista de tuplas (inicio, fin) como strings ISO. El último tramo puede
        ser más corto. Si start > end devuelve []. Si days <= 0 lanza ValueError.
    """
    if days <= 0:
        raise ValueError("days debe ser un entero positivo (>= 1)")

    s = date.fromisoformat(start)
    e = date.fromisoformat(end)

    if s > e:
        return []

    span = timedelta(days=days - 1)  # inclusivo: un tramo de N días cubre N-1 deltas
    chunks: list[tuple[str, str]] = []
    cur = s
    while cur <= e:
        chunk_end = min(cur + span, e)
        chunks.append((cur.isoformat(), chunk_end.isoformat()))
        cur = chunk_end + timedelta(days=1)

    return chunks
```