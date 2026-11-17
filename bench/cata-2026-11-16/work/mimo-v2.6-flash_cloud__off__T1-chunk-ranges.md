```python
from datetime import datetime, timedelta

def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("days must be positive")

    start_date = datetime.strptime(start, "%Y-%m-%d").date()
    end_date = datetime.strptime(end, "%Y-%m-%d").date()

    if start_date > end_date:
        return []

    ranges = []
    current = start_date
    delta = timedelta(days=days - 1)

    while current <= end_date:
        chunk_end = min(current + delta, end_date)
        ranges.append((current.isoformat(), chunk_end.isoformat()))
        current = chunk_end + timedelta(days=1)

    return ranges
```