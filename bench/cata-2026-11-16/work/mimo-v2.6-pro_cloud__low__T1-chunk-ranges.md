```python
from datetime import date, timedelta
from typing import List, Tuple


def chunk_ranges(start: str, end: str, days: int) -> List[Tuple[str, str]]:
    """Parte el rango inclusivo [start, end] en tramos consecutivos e inclusivos
    de a lo sumo `days` días cada uno.

    Args:
        start: fecha ISO 'YYYY-MM-DD' inicial (inclusiva).
        end:   fecha ISO 'YYYY-MM-DD' final (inclusiva).
        days:  longitud máxima de cada tramo, en días (>= 1).

    Returns:
        Lista de tuplas (inicio, fin) como strings ISO. El último tramo puede
        ser más corto. Sin huecos ni superposiciones. [] si start > end.

    Raises:
        ValueError: si days <= 0.
    """
    if days <= 0:
        raise ValueError("days must be a positive integer, got %r" % (days,))

    s = date.fromisoformat(start)
    e = date.fromisoformat(end)

    if s > e:
        return []

    span = timedelta(days=days - 1)   # desplazamiento máximo dentro del tramo
    one_day = timedelta(days=1)

    chunks: List[Tuple[str, str]] = []
    cur = s
    while cur <= e:
        chunk_end = cur + span
        if chunk_end > e:
            chunk_end = e
        chunks.append((cur.isoformat(), chunk_end.isoformat()))
        cur = chunk_end + one_day

    return chunks
```