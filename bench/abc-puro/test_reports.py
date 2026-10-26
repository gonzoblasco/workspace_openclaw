import datetime as dt
import unittest

import reports


class FakeSession:
    """A minimal mock session that returns deterministic data.

    ``calls`` counts the number of *backend fetches*: it is the observable
    that proves whether the cache was actually used (defects 8 and 9 of the
    review: tests that only compare returned values cannot tell a cache hit
    from a second fetch).
    """

    def __init__(self, data):
        self._data = data
        self.calls = 0

    def fetch(self, page, per_page):
        self.calls += 1
        return reports.paginate(self._data, page, per_page)


SAMPLE_REPORTS = [
    {"id": 1, "date": "2023-01-01", "amount": 100, "status": "open"},
    {"id": 2, "date": "2023-01-05", "amount": 200, "status": "closed"},
    {"id": 3, "date": "2023-02-10", "amount": 150, "status": "open"},
    {"id": 4, "date": "2023-03-15", "amount": 300, "status": "pending"},
    {"id": 5, "date": "2023-04-20", "amount": "bad", "status": "closed"},
]


class TestPaginate(unittest.TestCase):
    def test_basic_pagination(self):
        items = list(range(10))
        self.assertEqual(reports.paginate(items, page=1, per_page=3), [0, 1, 2])
        self.assertEqual(reports.paginate(items, page=2, per_page=3), [3, 4, 5])
        self.assertEqual(reports.paginate(items, page=4, per_page=3), [9])

    def test_page_out_of_range_returns_empty(self):
        self.assertEqual(reports.paginate([1, 2, 3], page=5, per_page=2), [])

    def test_invalid_per_page_raises(self):
        """Spec: 'per_page invalido (0, negativo o no int) lanza ValueError'.

        Before this was strengthened the test only covered 0 and -1, so the
        "no int" half of the criterion was never enforced by any test.
        """
        # non-positive integers
        for bad in (0, -1, -10):
            with self.subTest(per_page=bad):
                with self.assertRaises(ValueError):
                    reports.paginate([1, 2, 3], page=1, per_page=bad)
        # non-int values (floats, strings, None, containers, objects)
        for bad in (2.5, 2.0, "3", "", None, [1], (1,), {"a": 1}, object()):
            with self.subTest(per_page=bad):
                with self.assertRaises(ValueError):
                    reports.paginate([1, 2, 3], page=1, per_page=bad)
        # bool is a subclass of int, but it is not a valid page size:
        # True must not be silently accepted as 1.
        for bad in (True, False):
            with self.subTest(per_page=bad):
                with self.assertRaises(ValueError):
                    reports.paginate([1, 2, 3], page=1, per_page=bad)

    def test_invalid_per_page_raises_even_with_out_of_range_page(self):
        """The per_page validation must not be short-circuited by an
        out-of-range page (which returns [] for a *valid* per_page)."""
        for bad in (0, -1, "3", 2.5, None, True):
            with self.subTest(per_page=bad):
                with self.assertRaises(ValueError):
                    reports.paginate([1, 2, 3], page=99, per_page=bad)

    def test_valid_per_page_is_accepted(self):
        """Guard against over-correcting: valid per_page values must work."""
        self.assertEqual(reports.paginate([1, 2, 3], page=1, per_page=1), [1])
        self.assertEqual(reports.paginate([1, 2, 3], page=1, per_page=3), [1, 2, 3])
        self.assertEqual(reports.paginate([1, 2, 3], page=1, per_page=10), [1, 2, 3])


class TestFilterByDate(unittest.TestCase):
    def test_inclusive_bounds(self):
        since = dt.date(2023, 1, 5)
        until = dt.date(2023, 3, 15)
        filtered = reports.filter_by_date(SAMPLE_REPORTS, since, until)
        self.assertCountEqual([r["id"] for r in filtered], [2, 3, 4])

    def test_datetime_inputs(self):
        since = dt.datetime(2023, 1, 5, 12, 0)
        until = dt.datetime(2023, 3, 15, 23, 59)
        filtered = reports.filter_by_date(SAMPLE_REPORTS, since, until)
        self.assertCountEqual([r["id"] for r in filtered], [2, 3, 4])


class TestCachedReports(unittest.TestCase):
    def setUp(self):
        self.session = FakeSession(SAMPLE_REPORTS)

    def test_cache_hit_within_ttl(self):
        """A hit must mean: NO new fetch to the backend.

        The previous version only asserted ``first == second``; with the cache
        disabled there are two fetches and the two results are still equal, so
        the assertion passed even with no cache at all (review defect 8).
        """
        now = dt.datetime.utcnow()
        first = reports.cached_reports(
            self.session, page=1, per_page=2, ttl_seconds=10, now=now
        )
        self.assertEqual(self.session.calls, 1, "la primera llamada debe hacer un fetch")
        second = reports.cached_reports(
            self.session,
            page=1,
            per_page=2,
            ttl_seconds=10,
            now=now + dt.timedelta(seconds=5),
        )
        self.assertEqual(
            self.session.calls,
            1,
            "un hit dentro del TTL NO debe volver a llamar al backend",
        )
        self.assertEqual(first, second)
        self.assertEqual(len(second), 2)

    def test_cache_hit_within_ttl_is_really_served_from_cache(self):
        """Stronger variant: the second call must not even be able to see the
        backend.  The session raises if fetched again."""
        now = dt.datetime.utcnow()
        reports.cached_reports(self.session, page=1, per_page=2, ttl_seconds=10, now=now)

        class ExplodingSession(FakeSession):
            def fetch(self, page, per_page):
                raise AssertionError("el backend fue consultado: no hubo hit de cache")

        exploding = ExplodingSession(SAMPLE_REPORTS)
        exploding._report_cache = self.session._report_cache
        out = reports.cached_reports(
            exploding, page=1, per_page=2, ttl_seconds=10,
            now=now + dt.timedelta(seconds=5),
        )
        self.assertEqual(len(out), 2)

    def test_cache_miss_after_ttl(self):
        """After the TTL expires there MUST be a new fetch.

        The previous version only compared the returned values, which are equal
        whether the cache expired correctly, never expired, or did not exist
        at all (review defect 9).  This test asserts on the fetch count.
        """
        now = dt.datetime.utcnow()
        first = reports.cached_reports(
            self.session, page=1, per_page=2, ttl_seconds=1, now=now
        )
        self.assertEqual(self.session.calls, 1, "la primera llamada debe hacer un fetch")
        later = reports.cached_reports(
            self.session,
            page=1,
            per_page=2,
            ttl_seconds=1,
            now=now + dt.timedelta(seconds=2),
        )
        self.assertEqual(
            self.session.calls,
            2,
            "pasado el TTL debe haber un fetch NUEVO (el cache no debe servir datos viejos)",
        )
        self.assertEqual(first, later)
        self.assertEqual(len(later), 2)

    def test_cache_miss_after_ttl_refetches_fresh_data(self):
        """The refreshed call must go to the backend and return the new data,
        proving it is a miss and not a stale hit."""
        now = dt.datetime.utcnow()
        reports.cached_reports(self.session, page=1, per_page=2, ttl_seconds=1, now=now)

        # The backend now returns different data: a stale cache hit would show
        # the OLD rows.
        self.session._data = [
            {"id": 10, "date": "2024-01-01", "amount": 1, "status": "open"},
            {"id": 11, "date": "2024-01-02", "amount": 2, "status": "open"},
        ]
        later = reports.cached_reports(
            self.session, page=1, per_page=2, ttl_seconds=1,
            now=now + dt.timedelta(seconds=2),
        )
        self.assertEqual(self.session.calls, 2)
        self.assertEqual([r["id"] for r in later], [10, 11], "no debe devolver datos viejos")

    def test_cache_never_expires_is_detected(self):
        """A cache that never expires must be caught by the miss test."""
        now = dt.datetime.utcnow()
        reports.cached_reports(self.session, page=1, per_page=2, ttl_seconds=1, now=now)
        reports.cached_reports(
            self.session, page=1, per_page=2, ttl_seconds=1,
            now=now + dt.timedelta(seconds=1000),
        )
        self.assertEqual(self.session.calls, 2, "el cache no puede vivir para siempre")

    def test_negative_ttl_raises(self):
        now = dt.datetime.utcnow()
        with self.assertRaises(ValueError):
            reports.cached_reports(self.session, 1, 2, -5, now)


class TestSummarize(unittest.TestCase):
    def test_basic_summary(self):
        summary = reports.summarize(SAMPLE_REPORTS)
        self.assertEqual(summary["count"], 5)
        self.assertAlmostEqual(summary["total_amount"], 750.0)
        self.assertDictEqual(
            summary["by_status"],
            {"open": 2, "closed": 2, "pending": 1},
        )


if __name__ == "__main__":
    unittest.main()
