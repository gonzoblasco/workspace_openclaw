```python
from datetime import datetime, timedelta

def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("days must be > 0")
    s = datetime.strptime(start, "%Y-%m-%d").date()
    e = datetime.strptime(end, "%Y-%m-%d").date()
    if s > e:
        return []
    result = []
    cur = s
    delta = timedelta(days=days - 1)
    step = timedelta(days=1)
    while cur <= e:
        chunk_end = cur + delta
        if chunk_end > e:
            chunk_end = e
        result.append((cur.isoformat(), chunk_end.isoformat()))
        cur = chunk_end + step
    return result
```