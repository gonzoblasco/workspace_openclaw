```python
from datetime import date, timedelta


def chunk_ranges(start: str, end: str, days: int) -> list[tuple[str, str]]:
    if days <= 0:
        raise ValueError("days must be positive")

    s = date.fromisoformat(start)
    e = date.fromisoformat(end)

    if s > e:
        return []

    chunks = []
    cur = s
    while cur <= e:
        chunk_end = min(cur + timedelta(days=days - 1), e)
        chunks.append((cur.isoformat(), chunk_end.isoformat()))
        cur = chunk_end + timedelta(days=1)

    return chunks
```