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


if __name__ == "__main__":
    unittest.main()
