```python
from datetime import date, timedelta


def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("days debe ser mayor que 0")

    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)

    if start_date > end_date:
        return []

    ranges = []
    current = start_date

    while current <= end_date:
        chunk_end = min(end_date, current + timedelta(days=days - 1))
        ranges.append((current.isoformat(), chunk_end.isoformat()))
        current = chunk_end + timedelta(days=1)

    return ranges
```