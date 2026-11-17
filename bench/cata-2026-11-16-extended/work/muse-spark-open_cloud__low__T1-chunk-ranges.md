```python
from datetime import datetime, timedelta

def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("days debe ser > 0")
    if start > end:
        return []
    s = datetime.strptime(start, "%Y-%m-%d").date()
    e = datetime.strptime(end, "%Y-%m-%d").date()
    if s > e:
        return []
    result = []
    cur = s
    step = timedelta(days=days)
    one_day = timedelta(days=1)
    while cur <= e:
        chunk_end = cur + step - one_day
        if chunk_end > e:
            chunk_end = e
        result.append((cur.isoformat(), chunk_end.isoformat()))
        cur = chunk_end + one_day
    return result
```