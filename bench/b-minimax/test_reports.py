import datetime as dt
import unittest

import reports


class FakeSession:
    """A minimal mock session that returns deterministic data."""

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
        with self.assertRaises(ValueError):
            reports.paginate([1, 2, 3], page=1, per_page=0)
        with self.assertRaises(ValueError):
            reports.paginate([1, 2, 3], page=1, per_page=-1)


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
        now = dt.datetime.utcnow()
        first = reports.cached_reports(
            self.session, page=1, per_page=2, ttl_seconds=10, now=now
        )
        second = reports.cached_reports(
            self.session,
            page=1,
            per_page=2,
            ttl_seconds=10,
            now=now + dt.timedelta(seconds=5),
        )
        self.assertEqual(first, second)

    def test_cache_miss_after_ttl(self):
        now = dt.datetime.utcnow()
        first = reports.cached_reports(
            self.session, page=1, per_page=2, ttl_seconds=1, now=now
        )
        later = reports.cached_reports(
            self.session,
            page=1,
            per_page=2,
            ttl_seconds=1,
            now=now + dt.timedelta(seconds=2),
        )
        self.assertEqual(first, later)

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


class TestCacheCorrectness(unittest.TestCase):
    """Regression tests for defects found in the original implementation."""

    def setUp(self):
        self.session = FakeSession(SAMPLE_REPORTS)
        self.now = dt.datetime(2023, 1, 1)

    def test_cache_hit_does_not_refetch(self):
        reports.cached_reports(self.session, 1, 2, 10, self.now)
        reports.cached_reports(self.session, 1, 2, 10, self.now + dt.timedelta(seconds=5))
        self.assertEqual(self.session.calls, 1)

    def test_cache_miss_after_ttl_refetches(self):
        reports.cached_reports(self.session, 1, 2, 1, self.now)
        later = reports.cached_reports(
            self.session, 1, 2, 1, self.now + dt.timedelta(seconds=2)
        )
        self.assertEqual(self.session.calls, 2)
        self.assertEqual(later, SAMPLE_REPORTS[:2])

    def test_cache_is_not_shared_between_sessions(self):
        class Other(FakeSession):
            pass

        first = Other(SAMPLE_REPORTS)
        second = Other([{"id": 99, "date": "2023-01-01", "amount": 1, "status": "x"}])
        reports.cached_reports(first, 1, 5, 100, self.now)
        got = reports.cached_reports(second, 1, 5, 100, self.now)
        self.assertEqual(got[0]["id"], 99)

    def test_recycled_session_id_does_not_leak_cache(self):
        # Simulate the case where a new session object happens to reuse the
        # id() of a previously cached (and garbage collected) one: the cache
        # entry must not be served to the unrelated session.
        class Other(FakeSession):
            pass

        stale_session = Other(SAMPLE_REPORTS)
        reports.cached_reports(stale_session, 1, 5, 100, self.now)
        stale_payload = SAMPLE_REPORTS[:5]
        shape = len(reports._CACHE[(id(stale_session), 1, 5)])
        del stale_session

        second = Other([{"id": 99, "date": "2023-01-01", "amount": 1, "status": "x"}])
        # Simulate id() recycling by pointing the key of ``second`` at the
        # entry that belonged to the discarded session.
        if shape == 3:
            poison = (None, self.now, stale_payload)
        else:
            poison = (self.now, stale_payload)
        reports._CACHE[(id(second), 1, 5)] = poison
        got = reports.cached_reports(second, 1, 5, 100, self.now)
        self.assertEqual(got[0]["id"], 99)

    def test_caller_cannot_mutate_cached_payload(self):
        payload = reports.cached_reports(self.session, 1, 2, 100, self.now)
        payload.append({"injected": True})
        again = reports.cached_reports(self.session, 1, 2, 100, self.now)
        self.assertEqual(len(again), 2)

    def test_future_timestamp_does_not_serve_stale_entry(self):
        reports.cached_reports(self.session, 1, 2, 10, self.now)
        reports.cached_reports(
            self.session, 1, 2, 10, self.now - dt.timedelta(hours=1)
        )
        self.assertEqual(self.session.calls, 2)


class TestPaginateValidation(unittest.TestCase):
    def test_non_int_per_page_raises(self):
        for bad in ("3", 3.0, None):
            with self.assertRaises(ValueError):
                reports.paginate([1, 2, 3], page=1, per_page=bad)


class TestFilterByDateEdges(unittest.TestCase):
    def test_until_bound_is_inclusive(self):
        data = [{"id": 1, "date": "2023-03-15"}]
        got = reports.filter_by_date(data, dt.date(2023, 1, 1), dt.date(2023, 3, 15))
        self.assertEqual([r["id"] for r in got], [1])

    def test_since_bound_is_inclusive(self):
        data = [{"id": 1, "date": "2023-01-01"}]
        got = reports.filter_by_date(data, dt.date(2023, 1, 1), dt.date(2023, 3, 15))
        self.assertEqual([r["id"] for r in got], [1])

    def test_datetime_bounds_truncate_to_date(self):
        data = [{"id": 1, "date": "2023-03-15"}]
        got = reports.filter_by_date(
            data, dt.datetime(2023, 1, 1, 0, 0), dt.datetime(2023, 3, 15, 23, 59)
        )
        self.assertEqual([r["id"] for r in got], [1])


if __name__ == "__main__":
    unittest.main()
