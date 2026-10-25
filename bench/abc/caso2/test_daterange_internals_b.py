"""Agent B: tests that pin down the real defects inside daterange()."""
import ast
import unittest
from datetime import date, timedelta

import daterange as dr


class TestDaterangeLoopHygiene(unittest.TestCase):
    def test_no_function_level_inline_import(self):
        """Inline imports inside functions defeat module-level validation."""
        with open(dr.__file__, encoding="utf-8") as fh:
            src = fh.read()
        tree = ast.parse(src)
        offenders = []
        for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
            for sub in ast.walk(fn):
                if isinstance(sub, (ast.Import, ast.ImportFrom)):
                    offenders.append(f"{fn.name}:{sub.lineno}")
        self.assertEqual(offenders, [], f"inline imports inside functions: {offenders}")

    def test_daterange_does_not_use_add_months_as_noop(self):
        """add_months(d, 0) inside the loop is dead work; count the calls."""
        calls = []
        original = dr.add_months

        def spy(d, n):
            calls.append((d, n))
            return original(d, n)

        dr.add_months = spy
        try:
            r = dr.daterange(date(2023, 1, 1), date(2023, 1, 11))
        finally:
            dr.add_months = original
        self.assertEqual(len(r), 10)
        self.assertEqual(calls, [], "daterange must not call add_months in its day loop")


class TestDaterangeEquivalence(unittest.TestCase):
    def test_matches_naive_reference_across_leap_and_month_boundaries(self):
        for start, days in [
            (date(2024, 2, 1), 60),
            (date(2023, 12, 25), 40),
            (date(2023, 1, 30), 35),
        ]:
            end = start + timedelta(days=days)
            expected = [start + timedelta(days=i) for i in range(days)]
            self.assertEqual(dr.daterange(start, end), expected, f"{start}+{days}d")


if __name__ == "__main__":
    unittest.main()
