```python
from datetime import datetime, timedelta

def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("days must be greater than 0")

    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()

    if start_date > end_date:
        return []

    chunks = []
    current_start = start_date
    while current_start <= end_date:
        current_end = current_start + timedelta(days=days - 1)
        if current_end > end_date:
            current_end = end_date
        
        chunks.append((current_start.isoformat(), current_end.isoformat()))
        current_start = current_end + timedelta(days=1)

    return chunks
```