```python
from datetime import date, timedelta

def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("days debe ser mayor que 0")
    
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)
    
    if start_date > end_date:
        return []
    
    result = []
    current_start = start_date
    
    while current_start <= end_date:
        current_end = min(current_start + timedelta(days=days - 1), end_date)
        result.append((current_start.isoformat(), current_end.isoformat()))
        current_start = current_end + timedelta(days=1)
    
    return result
```