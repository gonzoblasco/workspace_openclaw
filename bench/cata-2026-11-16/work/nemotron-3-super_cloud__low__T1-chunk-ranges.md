```python
from datetime import date, timedelta
from typing import List, Tuple

def chunk_ranges(start: str, end: str, days: int) -> List[Tuple[str, str]]:
    if days <= 0:
        raise ValueError("days must be positive")
    try:
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
    except ValueError:
        raise ValueError("start and end must be ISO format strings 'YYYY-MM-DD'")
    if start_date > end_date:
        return []
    result: List[Tuple[str, str]] = []
    current = start_date
    while current <= end_date:
        chunk_end = current + timedelta(days=days - 1)
        if chunk_end > end_date:
            chunk_end = end_date
        result.append((current.isoformat(), chunk_end.isoformat()))
        current = chunk_end + timedelta(days=1)
    return result
```