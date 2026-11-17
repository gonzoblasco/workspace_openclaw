from datetime import date, timedelta

def chunk_ranges(start: str, end: str, days: int):
    if days <= 0:
        raise ValueError("days must be positive")
    try:
        s = date.fromisoformat(start)
        e = date.fromisoformat(end)
    except ValueError:
        raise ValueError("Invalid date format; expected YYYY-MM-DD")

    if s > e:
        return []

    result = []
    current = s
    while current <= e:
        next_end = current + timedelta(days=days - 1)
        chunk_end = min(next_end, e)
        result.append((current.isoformat(), chunk_end.isoformat()))
        current = chunk_end + timedelta(days=1)
    return result