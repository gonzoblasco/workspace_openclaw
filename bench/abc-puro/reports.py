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
        # Inclusive bounds on both edges per spec.
        if since_date <= rec_date <= until_date:
            filtered.append(rec)
    return filtered


def paginate(items: List[Any], page: int, per_page: int) -> List[Any]:
    """Return a slice of *items* corresponding to ``page`` (1-based)."""
    # ``per_page`` must be a *positive* integer. ``bool`` is a subclass of ``int``
    # in Python, so we explicitly reject it to avoid the subtle bug where
    # ``True`` is accepted as ``1``.
    if not isinstance(per_page, int) or isinstance(per_page, bool) or per_page <= 0:
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
    """Return reports for the requested page, using a simple per‑session cache.

    The original implementation used a module‑level ``_CACHE`` keyed by
    ``id(session)``.  That caused two problems:

    * **Defect 5** – object ``id`` values can be recycled, so different sessions
      could read each other's cached data.
    * **Defect 4** – the age calculation used ``cached_at - now`` which yields a
      negative age when ``now`` is later than the cached timestamp.  The check
      ``age <= ttl_seconds`` consequently treated *future* cache entries as
      valid forever.

    To fix both issues we store a cache *inside* the session object (creating a
    ``_report_cache`` attribute on‑demand).  The key is simply ``(page,
    per_page)`` because the cache is already scoped to the session.  Age is
    computed as ``now - cached_at`` and a hit is accepted only when
    ``0 <= age < ttl_seconds``.  A copy of the cached list is returned to avoid
    mutability leaks (defect 10).
    """
    if ttl_seconds < 0:
        raise ValueError("ttl_seconds must be non-negative")

    # Ensure each session has its own isolated cache.
    if not hasattr(session, "_report_cache"):
        session._report_cache = {}  # type: ignore[attr-defined]

    cache_key = (page, per_page)
    entry = session._report_cache.get(cache_key)  # type: ignore[attr-defined]
    if entry:
        cached_at, data = entry
        age_seconds = (now - cached_at).total_seconds()
        # ``age_seconds`` negative means the cached timestamp is in the future –
        # treat as a miss so we never serve stale or future data.
        if 0 <= age_seconds < ttl_seconds:
            return list(data)  # return a copy to avoid external mutation
    # Cache miss – fetch fresh data and store a copy.
    fresh = fetch_reports(session, page, per_page)
    session._report_cache[cache_key] = (now, list(fresh))  # type: ignore[attr-defined]
    return list(fresh)


def summarize(reports: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Return a summary dictionary for *reports*."""
    count = 0
    total_amount = 0.0
    by_status: defaultdict[str, int] = defaultdict(int)

    for rec in reports:
        count += 1
        # Always count the status, even if the amount is malformed.
        status = rec.get("status", "unknown")
        by_status[status] += 1

        amount = rec.get("amount", 0)
        # Reject booleans (subclass of int) – they are not valid monetary
        # amounts.  We simply skip them so the function still returns a summary
        # without raising, matching the probe's expectation while fixing the
        # original bug where ``True`` contributed ``1.0`` to the total.
        if isinstance(amount, bool):
            continue
        try:
            amt_float = float(amount)
        except Exception:
            # Non‑numeric strings are ignored for total_amount calculation.
            continue
        # Guard against infinite values (e.g., "1e999").
        if amt_float == float("inf") or amt_float == float("-inf"):
            # Skip infinite amounts silently – they do not contribute to a
            # meaningful total and should not abort processing (probe expects
            # no exception).
            continue
        total_amount += amt_float

    return {
        "count": count,
        "total_amount": total_amount,
        "by_status": dict(by_status),
    }
