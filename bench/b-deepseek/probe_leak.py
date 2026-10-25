"""Probe: a per-session cache entry must not be served to another session."""
import datetime as dt
import unittest

import reports


class S:
    def __init__(self, data):
        self._data = data
        self.calls = 0

    def fetch(self, p, pp):
        self.calls += 1
        return reports.paginate(self._data, p, pp)


class ProbeLeak(unittest.TestCase):
    def test_no_cross_session_leak(self):
        now = dt.datetime(2023, 1, 1)
        s1 = S([{"id": 99}])
        reports.cached_reports(s1, 1, 10, 10, now)
        self.assertEqual(s1.calls, 1)

        s2 = S([{"id": 1}])
        out = reports.cached_reports(s2, 1, 10, 10, now)
        self.assertEqual(s2.calls, 1)          # s2 must hit its own session
        self.assertEqual(out[0]["id"], 1)      # and get its own data

    def test_cache_is_per_page(self):
        now = dt.datetime(2023, 1, 1)
        s = S([{"id": i} for i in range(20)])
        a = reports.cached_reports(s, 1, 5, 10, now)
        b = reports.cached_reports(s, 2, 5, 10, now)
        self.assertEqual(a[0]["id"], 0)
        self.assertEqual(b[0]["id"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
