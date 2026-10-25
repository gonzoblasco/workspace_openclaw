"""reports.py

Implementation of the *Unidad U1* – a small, pure-standard-library module that
provides a cached, paginated API for retrieving report data.  The public API is
fully type-annotated and each function includes a concise docstring describing
its contract.
"""

from __future__ import annotations

import datetime as _dt
import weakref
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Tuple

# Keyed by the session *object* (weakly), not by ``id(session)``: ids are
# reused after garbage collection and would serve one session's data to
# another.  Entries vanish with their session, so tests cannot leak.
_CACHE: "weakref.WeakKeyDictionary[Any, Dict[Tuple[int, int], Tuple[_dt.datetime, List[Dict[str, Any]]]]]" = (
    weakref.WeakKeyDictionary()
)


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

    # Bounds are inclusive on both ends.  ``until`` may carry a time component,
    # so its calendar date is always included in full.
    filtered: List[Dict[str, Any]] = []
    for rec in reports:
        iso = rec.get("date")
        if not iso:
            continue
        try:
            if isinstance(iso, _dt.datetime):
                rec_date = iso.date()
            elif isinstance(iso, _dt.date):
                rec_date = iso
            else:
                rec_date = _dt.date.fromisoformat(str(iso)[:10])
        except Exception:
            continue
        if since_date <= rec_date <= until_date:
            filtered.append(rec)
    return filtered


def paginate(items: List[Any], page: int, per_page: int) -> List[Any]:
    """Return a slice of *items* corresponding to ``page`` (1-based)."""
    if isinstance(per_page, bool) or not isinstance(per_page, int) or per_page <= 0:
        raise ValueError("per_page must be a positive integer")
    if isinstance(page, bool) or not isinstance(page, int) or page < 1:
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

    cache_key = (page, per_page)
    per_session = _CACHE.get(session)
    entry = per_session.get(cache_key) if per_session is not None else None
    if entry:
        cached_at, data = entry
        age = (now - cached_at).total_seconds()
        # A negative age means the cached stamp is ahead of ``now`` (clock
        # skew): that entry cannot be trusted as fresh.
        if 0 <= age <= ttl_seconds:
            return list(data)
    fresh = fetch_reports(session, page, per_page)
    if per_session is None:
        try:
            per_session = _CACHE.setdefault(session, {})
        except TypeError:  # session not weak-referenceable: skip caching
            return list(fresh)
    per_session[cache_key] = (now, list(fresh))
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
            if not isinstance(amount, bool):
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
