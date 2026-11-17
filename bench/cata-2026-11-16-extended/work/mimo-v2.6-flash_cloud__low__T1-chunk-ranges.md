```python
from datetime import date, timedelta


def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("days must be positive")

    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)

    if start_date > end_date:
        return []

    ranges = []
    current = start_date
    step = timedelta(days=days)

    while current <= end_date:
        chunk_end = min(current + step - timedelta(days=1), end_date)
        ranges.append((current.isoformat(), chunk_end.isoformat()))
        current = chunk_end + timedelta(days=1)

    return ranges
```