"""reports.py

Implementation of the *Unidad U1* – a small, pure-standard-library module that
provides a cached, paginated API for retrieving report data.  The public API is
fully type-annotated and each function includes a concise docstring describing
its contract.
"""

from __future__ import annotations

import datetime as _dt
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Tuple

_CACHE: Dict[Tuple[int, int, int], Tuple[_dt.datetime, List[Dict[str, Any]]]] = {}


def fetch_reports(session: Any, page: int, per_page: int) -> List[Dict[str, Any]]:
    """Retrieve a single page of reports from *session*."""
    if not hasattr(session, "fetch"):
        raise AttributeError("session object must implement a 'fetch' method")
    result = session.fetch(page, per_page)
    return list(result)


def filter_by_date(
    reports: Iterable[Dict[str, Any]],
    since: _dt.datetime | _dt.date,
    until: _dt.datetime | _dt.date,
) -> List[Dict[str, Any]]:
    """Filter *reports* keeping only those whose ``date`` field lies in the range.

    The bounds are **inclusive**.
    """
    if isinstance(since, _dt.datetime):
        since_date = since.date()
    else:
        since_date = since

    if isinstance(until, _dt.datetime):
        until_date = until.date()
    else:
        until_date = until

    filtered: List[Dict[str, Any]] = []
    for rec in reports:
        iso = rec.get("date")
        if not iso:
            continue
        try:
            rec_date = _dt.date.fromisoformat(iso)
        except Exception:
            continue
        if since_date <= rec_date <= until_date:
            filtered.append(rec)
    return filtered


def paginate(items: List[Any], page: int, per_page: int) -> List[Any]:
    """Return a slice of *items* corresponding to ``page`` (1-based)."""
    if not isinstance(per_page, int) or per_page <= 0:
        raise ValueError("per_page must be a positive integer")
    if not isinstance(page, int) or page < 1:
        return []
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]


def cached_reports(
    session: Any,
    page: int,
    per_page: int,
    ttl_seconds: int,
    now: _dt.datetime,
) -> List[Dict[str, Any]]:
    """Return reports for the requested page, using a simple in-memory cache."""
    if ttl_seconds < 0:
        raise ValueError("ttl_seconds must be non-negative")

    cache_key = (id(session), page, per_page)
    entry = _CACHE.get(cache_key)
    if entry:
        cached_at, data = entry
        age = (now - cached_at).total_seconds()
        if age <= ttl_seconds:
            return list(data)
    fresh = fetch_reports(session, page, per_page)
    _CACHE[cache_key] = (now, fresh)
    return list(fresh)


def summarize(reports: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Return a summary dictionary for *reports*."""
    count = 0
    total_amount = 0.0
    by_status: defaultdict[str, int] = defaultdict(int)

    for rec in reports:
        count += 1
        amount = rec.get("amount", 0)
        try:
            total_amount += float(amount)
        except Exception:
            pass
        status = rec.get("status", "unknown")
        by_status[status] += 1

    return {
        "count": count,
        "total_amount": total_amount,
        "by_status": dict(by_status),
    }
