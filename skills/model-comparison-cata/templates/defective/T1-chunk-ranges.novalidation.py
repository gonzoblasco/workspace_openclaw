from datetime import date, timedelta


def chunk_ranges(start, end, days):
    s, e = date.fromisoformat(start), date.fromisoformat(end)
    out, cur = [], s
    while cur <= e:
        last = min(cur + timedelta(days=days - 1), e)
        out.append((cur.isoformat(), last.isoformat()))
        cur = last + timedelta(days=1)
    return out
