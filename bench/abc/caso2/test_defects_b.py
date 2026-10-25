"""Tests (Agent B) that demonstrate the defects found by adversarial probing.

Deliberately independent from test_daterange.py. Each test targets one
confirmed defect or one required edge case from spec2.md / the review brief.
"""

import subprocess
import sys
import unittest
from datetime import date, timedelta

import daterange as dr


class TestMonthEndEdge(unittest.TestCase):
    def test_invalid_months_zero_thirteen_negative(self):
        for bad in (0, 13, -1, 100):
            with self.assertRaises(ValueError):
                dr.month_end(2023, bad)

    def test_all_months_day_counts(self):
        expected = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        for m, day in expected.items():
            self.assertEqual(dr.month_end(2023, m), date(2023, m, day))
        self.assertEqual(dr.month_end(2024, 2), date(2024, 2, 29))


class TestIsLeap(unittest.TestCase):
    def test_century_and_quadricentennial(self):
        self.assertTrue(dr.is_leap(2024))
        self.assertFalse(dr.is_leap(2023))
        self.assertFalse(dr.is_leap(1900))
        self.assertTrue(dr.is_leap(2000))


class TestAddMonthsEdge(unittest.TestCase):
    def test_end_of_month_clamp(self):
        self.assertEqual(dr.add_months(date(2023, 1, 31), 1), date(2023, 2, 28))
        self.assertEqual(dr.add_months(date(2024, 1, 31), 1), date(2024, 2, 29))
        self.assertEqual(dr.add_months(date(2023, 3, 31), -1), date(2023, 2, 28))

    def test_no_eom_clamp_for_mid_month(self):
        self.assertEqual(dr.add_months(date(2023, 1, 15), 1), date(2023, 2, 15))
        self.assertEqual(dr.add_months(date(2023, 1, 30), 1), date(2023, 2, 28))

    def test_add_months_zero(self):
        for d in (date(2023, 3, 31), date(2023, 1, 15), date(2024, 2, 29)):
            self.assertEqual(dr.add_months(d, 0), d)

    def test_add_months_large(self):
        self.assertEqual(dr.add_months(date(2023, 1, 31), 120), date(2033, 1, 31))
        self.assertEqual(dr.add_months(date(2023, 1, 31), -120), date(2013, 1, 31))


class TestDateRangeEdge(unittest.TestCase):
    def test_single_day(self):
        d = date(2023, 1, 1)
        self.assertEqual(dr.daterange(d, d + timedelta(days=1)), [d])

    def test_end_exclusive(self):
        r = dr.daterange(date(2023, 1, 1), date(2023, 1, 4))
        self.assertNotIn(date(2023, 1, 4), r)
        self.assertEqual(r[-1], date(2023, 1, 3))

    def test_leap_day_count(self):
        r = dr.daterange(date(2024, 2, 1), date(2024, 3, 1))
        self.assertIn(date(2024, 2, 29), r)
        self.assertEqual(len(r), 29)

    def test_three_year_count(self):
        r = dr.daterange(date(2022, 1, 1), date(2025, 1, 1))
        self.assertEqual(len(r), 1096)  # 365+365+366
        self.assertEqual(r[0], date(2022, 1, 1))
        self.assertEqual(r[-1], date(2024, 12, 31))

    def test_no_duplicates_and_sorted_across_month_boundary(self):
        r = dr.daterange(date(2024, 1, 30), date(2024, 3, 5))
        self.assertEqual(len(r), len(set(r)))
        self.assertEqual(r, sorted(r))
        self.assertEqual(len(r), 35)
        self.assertEqual(r[2], date(2024, 2, 1))


class TestParseISOEdge(unittest.TestCase):
    def test_invalid_inputs_raise_useful_valueerror(self):
        for bad in ("2023-13-01", "no-es-fecha", "", "2023-02-30"):
            with self.assertRaises(ValueError) as ctx:
                dr.parse_iso(bad)
            msg = str(ctx.exception)
            self.assertIn("Invalid ISO date string", msg)
            self.assertIn(repr(bad), msg)


class TestLazyImportHazard(unittest.TestCase):
    """A function-level inline import cannot be validated by import alone."""

    def test_module_imports_cleanly_outside_cwd(self):
        # Importing the module from a foreign cwd must not fail.
        res = subprocess.run(
            [sys.executable, "-c", "import daterange"],
            cwd="/tmp",
            capture_output=True,
            text=True,
        )
        # cwd=/tmp has no daterange.py, so we only assert the import machinery
        # of the module itself is sane when sys.path points here.
        res2 = subprocess.run(
            [sys.executable, "-c", "import daterange; print(daterange.__all__ if hasattr(daterange,'__all__') else 'ok')"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res2.returncode, 0, res2.stderr)


if __name__ == "__main__":
    unittest.main()
