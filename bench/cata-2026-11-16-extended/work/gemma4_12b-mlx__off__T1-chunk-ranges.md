```python
from datetime import datetime, timedelta

def chunk_ranges(start, end, days):
    if days <= 0:
        raise ValueError("Days must be greater than 0")
    
    start_dt = datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.strptime(end, '%Y-%m-%d')
    
    if start_dt > end_dt:
        return []
    
    chunks = []
    current_start = start_dt
    
    while current_start <= end_dt:
        current_end = current_start + timedelta(days=days - 1)
        if current_end > end_dt:
            current_end = end_dt
        
        chunks.append((current_start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')))
        current_start = current_end + timedelta(days=1)
        
    return chunks
```