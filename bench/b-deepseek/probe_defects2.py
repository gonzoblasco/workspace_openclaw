"""Probes #2: lying tests + cache staleness."""
import datetime as dt
import unittest
from unittest import mock

import reports


class CountingSession:
    """Returns DIFFERENT data per call, so a stale cache is detectable."""

    def __init__(self):
        self.calls = 0

    def fetch(self, page, per_page):
        self.calls += 1
        return [{"id": self.calls, "date": "2023-01-01", "amount": 1,
                 "status": "s"}]


class ProbeTwo(unittest.TestCase):
    # A) test_cache_miss_after_ttl asserts first == later, which is TRUE even
    #    if the cache never expires (same data). Prove the cache is not
    #    actually refetched after ttl.
    def test_cache_is_refetched_after_ttl(self):
        s = CountingSession()
        now = dt.datetime(2023, 1, 1)
        reports.cached_reports(s, 1, 10, ttl_seconds=1, now=now)
        out = reports.cached_reports(s, 1, 10, ttl_seconds=1,
                                    now=now + dt.timedelta(seconds=5))
        self.assertEqual(s.calls, 2)
        self.assertEqual(out[0]["id"], 2)

    # B) ttl boundary: a value exactly ttl seconds old is at the limit.
    #    Spec: "no devuelve un valor cacheado mas viejo que ttl_seconds".
    #    Exactly equal is NOT older -> must be a hit.
    def test_ttl_boundary_is_hit(self):
        s = CountingSession()
        now = dt.datetime(2023, 1, 1)
        reports.cached_reports(s, 1, 10, ttl_seconds=10, now=now)
        reports.cached_reports(s, 1, 10, ttl_seconds=10,
                               now=now + dt.timedelta(seconds=10))
        self.assertEqual(s.calls, 1)

    # C) negative-age bug: age computed as (cached_at - now) lets a future-
    #    stamped entry look fresh forever. Demonstrate with a real scenario:
    #    the caller passes a wall clock that moves backwards (NTP step).
    def test_backwards_clock_does_not_freeze_cache(self):
        s = CountingSession()
        base = dt.datetime(2023, 1, 1, 12, 0)
        reports.cached_reports(s, 1, 10, ttl_seconds=10, now=base)
        # clock stepped back 1 hour, then forwards past the original stamp
        reports.cached_reports(s, 1, 10, ttl_seconds=10,
                               now=base - dt.timedelta(hours=1))
        self.assertEqual(s.calls, 2)

    # D) per_page=True (non-int semantics) and per_page="3"
    def test_per_page_string_raises_valueerror(self):
        with self.assertRaises(ValueError):
            reports.paginate([1, 2, 3], page=1, per_page="3")

    def test_per_page_float_raises_valueerror(self):
        with self.assertRaises(ValueError):
            reports.paginate([1, 2, 3], page=1, per_page=2.5)

    # E) paginate with a page past the end on a per_page>0 must be []
    def test_page_out_of_range_nonempty(self):
        self.assertEqual(reports.paginate([1, 2, 3], page=2, per_page=3), [])

    # F) filter_by_date: since > until must return [] not crash
    def test_reversed_range_is_empty(self):
        self.assertEqual(
            reports.filter_by_date(
                [{"id": 1, "date": "2023-02-01"}],
                dt.date(2023, 3, 1), dt.date(2023, 1, 1)), [])

    # G) summarize: amount given as bool must not be summed as 1/0
    def test_summarize_bool_amount_not_summed(self):
        out = reports.summarize([{"amount": True, "status": "a"}])
        self.assertEqual(out["total_amount"], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
