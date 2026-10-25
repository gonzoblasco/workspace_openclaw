"""Adversarial probes for reports.py. Each probe FAILS if the defect exists."""
import datetime as dt
import unittest

import reports


class FakeSession:
    def __init__(self, data):
        self._data = data
        self.calls = 0

    def fetch(self, page, per_page):
        self.calls += 1
        return reports.paginate(self._data, page, per_page)


DATA = [
    {"id": 1, "date": "2023-01-05", "amount": 100, "status": "open"},
    {"id": 2, "date": "2023-03-15", "amount": 200, "status": "closed"},
]


class Probe(unittest.TestCase):
    # 1. per_page == 0 must raise ValueError -> currently silently returns []
    def test_per_page_zero_raises(self):
        self.assertRaises(ValueError, reports.paginate, [1, 2, 3], 1, 0)

    # 2. per_page non-int must raise ValueError -> currently TypeError/works
    def test_per_page_non_int_raises(self):
        self.assertRaises(ValueError, reports.paginate, [1, 2, 3], 1, "3")

    # 2b. bool is an int subclass: True would be accepted as 1
    def test_per_page_bool_raises(self):
        self.assertRaises(ValueError, reports.paginate, [1, 2, 3], 1, True)

    # 3. until must be inclusive -> id 2 (2023-03-15) is dropped
    def test_until_inclusive(self):
        out = reports.filter_by_date(DATA, dt.date(2023, 1, 1), dt.date(2023, 3, 15))
        self.assertEqual([r["id"] for r in out], [1, 2])

    # 4. cache must expire when now is BEFORE the cache timestamp (clock skew /
    #    cached in the "future" relative to now) -> age is negative, <= ttl
    def test_cache_expiry_with_earlier_now(self):
        s = FakeSession(DATA)
        base = dt.datetime(2023, 1, 1, 12, 0)
        reports.cached_reports(s, 1, 10, ttl_seconds=10, now=base)
        self.assertEqual(s.calls, 1)
        # now is 1h earlier: impossible for a real caller, but the age math
        # must never produce a "fresh" hit from a negative age
        reports.cached_reports(s, 1, 10, ttl_seconds=10,
                               now=base - dt.timedelta(hours=1))
        self.assertEqual(s.calls, 2)

    # 5. cache key uses id(session): a garbage-collected session's id can be
    #    reused, serving another session's data. Also: id() is not stable.
    def test_cache_does_not_cross_sessions_with_reused_id(self):
        s1 = FakeSession([{"id": 99, "date": "2023-01-05", "amount": 1, "status": "x"}])
        now = dt.datetime(2023, 1, 1)
        reports.cached_reports(s1, 1, 10, 10, now)
        sid = id(s1)
        del s1
        # emulate CPython reusing the freed address for a new object
        s2 = FakeSession([{"id": 1, "date": "2023-01-05", "amount": 1, "status": "x"}])
        if id(s2) != sid:
            self.skipTest("id not reused on this interpreter")
        out = reports.cached_reports(s2, 1, 10, 10, now)
        self.assertEqual(out[0]["id"], 1)

    # 6. cached value is returned by reference: caller mutation corrupts cache
    def test_cached_result_not_shared_mutable(self):
        s = FakeSession(DATA)
        now = dt.datetime(2023, 1, 1)
        first = reports.cached_reports(s, 1, 10, 10, now)
        first.append({"id": "mutated"})
        second = reports.cached_reports(s, 1, 10, 10, now)
        self.assertEqual(len(second), 2)

    # 7. summarize must skip non-numeric amounts entirely AND must not
    #    silently accept booleans; more importantly: count vs sum consistency
    def test_summarize_ignores_bad_amount_but_counts(self):
        out = reports.summarize([{"amount": "bad", "status": "a"},
                                 {"amount": 10, "status": "a"}])
        self.assertEqual(out["count"], 2)
        self.assertEqual(out["total_amount"], 10.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
