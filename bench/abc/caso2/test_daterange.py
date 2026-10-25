"""Unit tests for :pymod:`daterange`.

The tests exercise the public API defined in ``spec2.md`` and verify the edge
cases required by the specification:

* ``month_end`` for leap‑year February and regular months.
* ``add_months`` with positive, negative and end‑of‑month clamping.
* ``daterange`` half‑open semantics, empty range and error on inverted range.
* ``parse_iso`` correct parsing and clear error messages.
"""

import unittest
from datetime import date

import daterange


class TestMonthEnd(unittest.TestCase):
    def test_february_leap(self):
        self.assertEqual(daterange.month_end(2024, 2), date(2024, 2, 29))

    def test_february_common(self):
        self.assertEqual(daterange.month_end(2023, 2), date(2023, 2, 28))

    def test_april(self):
        self.assertEqual(daterange.month_end(2023, 4), date(2023, 4, 30))

    def test_invalid_month(self):
        with self.assertRaises(ValueError):
            daterange.month_end(2023, 13)


class TestAddMonths(unittest.TestCase):
    def test_positive_end_of_month(self):
        self.assertEqual(
            daterange.add_months(date(2023, 1, 31), 1),
            date(2023, 2, 28),
        )

    def test_negative_end_of_month(self):
        self.assertEqual(
            daterange.add_months(date(2023, 3, 31), -1),
            date(2023, 2, 28),
        )

    def test_regular_add(self):
        self.assertEqual(
            daterange.add_months(date(2023, 5, 15), 3),
            date(2023, 8, 15),
        )

    def test_regular_subtract(self):
        self.assertEqual(
            daterange.add_months(date(2023, 5, 15), -2),
            date(2023, 3, 15),
        )

    def test_overflow_day_clamp(self):
        # 31 Mar + 1 month -> 30 Apr (no end‑of‑month preservation)
        self.assertEqual(
            daterange.add_months(date(2023, 3, 31), 1),
            date(2023, 4, 30),
        )


class TestDateRange(unittest.TestCase):
    def test_empty_range(self):
        self.assertEqual(
            daterange.daterange(date(2023, 1, 1), date(2023, 1, 1)),
            [],
        )

    def test_inverted_range(self):
        with self.assertRaises(ValueError):
            daterange.daterange(date(2023, 1, 2), date(2023, 1, 1))

    def test_basic_range(self):
        expected = [date(2023, 1, 1), date(2023, 1, 2), date(2023, 1, 3)]
        self.assertEqual(
            daterange.daterange(date(2023, 1, 1), date(2023, 1, 4)),
            expected,
        )

    def test_leap_year_inclusion(self):
        # Range that crosses 2024‑02‑29 should include that day.
        start = date(2024, 2, 27)
        end = date(2024, 3, 2)  # exclusive, so includes 27,28,29,1
        expected = [date(2024, 2, 27), date(2024, 2, 28), date(2024, 2, 29), date(2024, 3, 1)]
        self.assertEqual(daterange.daterange(start, end), expected)


class TestParseISO(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(daterange.parse_iso("2023-07-15"), date(2023, 7, 15))

    def test_invalid(self):
        with self.assertRaises(ValueError) as ctx:
            daterange.parse_iso("15-07-2023")
        self.assertIn("Invalid ISO date string", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

