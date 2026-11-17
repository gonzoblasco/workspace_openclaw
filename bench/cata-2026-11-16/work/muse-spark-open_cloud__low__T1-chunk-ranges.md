```python
from datetime import datetime, timedelta

def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("days must be > 0")
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    except Exception:
        raise
    if start_date > end_date:
        return []
    result = []
    current = start_date
    delta = timedelta(days=days - 1)
    step = timedelta(days=days)
    while current <= end_date:
        chunk_end = current + delta
        if chunk_end > end_date:
            chunk_end = end_date
        result.append((current.isoformat(), chunk_end.isoformat()))
        current = chunk_end + timedelta(days=1)
        # Alternative increment to avoid drift: current += step
        # But using chunk_end+1 ensures no gaps even if last chunk was short
    return result
```