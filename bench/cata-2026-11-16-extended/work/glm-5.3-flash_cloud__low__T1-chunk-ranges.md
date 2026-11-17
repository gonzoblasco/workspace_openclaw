```python
from datetime import date, timedelta


def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("days debe ser mayor que 0")
    d0 = date.fromisoformat(start)
    d1 = date.fromisoformat(end)
    if d0 > d1:
        return []
    chunks = []
    cur = d0
    while cur <= d1:
        chunk_end = min(cur + timedelta(days=days - 1), d1)
        chunks.append((cur.isoformat(), chunk_end.isoformat()))
        cur = chunk_end + timedelta(days=1)
    return chunks
```