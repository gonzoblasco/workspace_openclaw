"""Utility functions for date manipulation.

The public API mirrors the specification in ``spec2.md`` and provides:

* :func:`month_end` – Return the last day of a given month.
* :func:`is_leap` – Tell if a year is a leap year.
* :func:`add_months` – Add (or subtract) a number of months to a date while
  preserving the *end‑of‑month* semantics required by the spec.
* :func:`daterange` – Produce a half‑open list of dates ``[start, end)``.
* :func:`parse_iso` – Parse an ``YYYY‑MM‑DD`` string into a :class:`datetime.date`.

All functions use only the Python standard library and include type hints and
docstrings as mandated.
"""

from __future__ import annotations

import calendar
from datetime import date, timedelta
from typing import List


def is_leap(year: int) -> bool:
    """Return ``True`` if *year* is a leap year.

    The implementation delegates to :func:`calendar.isleap` which follows the
    Gregorian calendar rules.
    """

    return calendar.isleap(year)


def month_end(year: int, month: int) -> date:
    """Return the last calendar day of *month* in *year*.

    Parameters
    ----------
    year:
        Four‑digit year.
    month:
        1‑based month number (1 = January, …, 12 = December).

    Raises
    ------
    ValueError
        If *month* is not in the range ``1..12``.
    """

    if not 1 <= month <= 12:
        raise ValueError(f"month must be 1..12, got {month}")
    # ``monthrange`` returns a tuple (weekday_of_first_day, number_of_days).
    _, last_day = calendar.monthrange(year, month)
    return date(year, month, last_day)


def _is_end_of_month(d: date) -> bool:
    """Internal helper: ``True`` if *d* is the last day of its month.

    This is used by :func:`add_months` to decide whether the result should be
    clamped to the target month's end.
    """

    return d.day == month_end(d.year, d.month).day


def add_months(d: date, n: int) -> date:
    """Add *n* months to *d* while preserving *end‑of‑month* semantics.

    The algorithm works in three steps:

    1. Compute the *target* year and month by adding ``n`` months to the
       ``(year, month)`` tuple.
    2. Determine the day component.  If ``d`` is the last day of its original
       month, the result is clamped to the last day of the target month.  This
       mirrors the behaviour required for dates like ``2023‑01‑31``.
    3. Construct and return the new :class:`datetime.date`.

    Parameters
    ----------
    d:
        The original date.
    n:
        Number of months to add (negative values subtract months).
    """

    # Compute target year/month.  ``divmod`` handles negative ``n`` correctly.
    total_months = d.year * 12 + (d.month - 1) + n
    if total_months < 0:
        # ``date`` does not support years <= 0; raise a clear error.
        raise ValueError("Resulting year is out of the supported range (year >= 1)")
    target_year, target_month_index = divmod(total_months, 12)
    target_month = target_month_index + 1

    # Preserve end‑of‑month if applicable.
    if _is_end_of_month(d):
        target_day = month_end(target_year, target_month).day
    else:
        # Normal case – keep the same day if it exists, otherwise clamp to the
        # last day of the target month (e.g., 31 Mar + 1 month → 30 Apr).
        _, max_day = calendar.monthrange(target_year, target_month)
        target_day = min(d.day, max_day)

    return date(target_year, target_month, target_day)


def daterange(start: date, end: date) -> List[date]:
    """Return a list of dates ``[start, end)``.

    The function validates the interval first:

    * ``start == end`` → ``[]`` (empty list).
    * ``start > end`` → raises ``ValueError``.

    The resulting list includes *start* and every subsequent calendar day up to
    but **excluding** *end*.
    """

    if start > end:
        raise ValueError("start date must be before end date for half‑open range")
    if start == end:
        return []

    days: List[date] = []
    current = start
    while current < end:
        days.append(current)
        current += timedelta(days=1)
    return days


def parse_iso(s: str) -> date:
    """Parse an ISO‑format ``YYYY‑MM‑DD`` string into a :class:`datetime.date`.

    The function deliberately uses :class:`datetime.date.fromisoformat` for
    correctness and then re‑raises ``ValueError`` with a custom message so that
    callers get a consistent, spec‑defined error.
    """

    try:
        return date.fromisoformat(s)
    except Exception as exc:
        raise ValueError(f"Invalid ISO date string '{s}': {exc}") from exc

