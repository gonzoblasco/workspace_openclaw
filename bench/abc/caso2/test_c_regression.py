"""Agent C – red de seguridad de tests (regresion) para :mod:`daterange`.

Este archivo NO duplica lo ya cubierto por ``test_daterange.py``,
``test_defects_b.py`` y ``test_daterange_internals_b.py``. Cada test apunta a
una invariante concreta del spec ``spec2.md`` y esta disenado para fallar ante
una mutacion especifica del codigo de produccion.

Invariantes protegidas (marcadas con ``MUT`` el mutante que mata el test):

* ``MUT-ME-FIXED31``  - ``month_end`` debe usar ``calendar.monthrange``, no 31 dias fijos.
* ``MUT-ME-MONTHVAL`` - ``month_end`` debe rechazar meses fuera de 1..12.
* ``MUT-AM-EOMALWAYS``- ``add_months`` solo clampea si el original era fin de mes.
* ``MUT-AM-NOCLAMP``  - ``add_months`` nunca debe overflowing a un dia inexistente.
* ``MUT-AM-GUARD``    - ``add_months`` con n negativo debe restar, no fallar.
* ``MUT-DR-INCLEND``  - ``daterange`` es half-open: ``[start, end)``.
* ``MUT-DR-NOVALID``  - ``daterange`` con ``start > end`` lanza ``ValueError``.
* ``MUT-PI-NORAISE``  - ``parse_iso`` siempre lanza ``ValueError`` con input invalido.
* ``MUT-LEAP-JULIAN`` - ``is_leap`` aplica el gregoriano completo (siglos/400).
"""

import unittest
from datetime import date, timedelta

import daterange as dr


# --------------------------------------------------------------------------
# month_end
# --------------------------------------------------------------------------

class TestMonthEndRegressions(unittest.TestCase):
    """MUT-ME-FIXED31, MUT-ME-MONTHVAL."""

    def test_month_end_matches_monthrange_for_every_month(self):
        """MUT-ME-FIXED31: 31 dias fijos rompe febrero/meses de 30."""
        import calendar

        for year in (1900, 1999, 2000, 2023, 2024, 2100, 2400):
            for month in range(1, 13):
                expected_day = calendar.monthrange(year, month)[1]
                self.assertEqual(
                    dr.month_end(year, month),
                    date(year, month, expected_day),
                    f"month_end({year}, {month})",
                )

    def test_month_end_february_non_leap_is_28(self):
        """MUT-ME-FIXED31: ``date(y, 2, 31)`` ni siquiera es una fecha valida."""
        self.assertEqual(dr.month_end(2023, 2), date(2023, 2, 28))
        self.assertEqual(dr.month_end(1900, 2), date(1900, 2, 28))
        self.assertEqual(dr.month_end(2100, 2), date(2100, 2, 28))

    def test_month_end_february_leap_is_29(self):
        self.assertEqual(dr.month_end(2024, 2), date(2024, 2, 29))
        self.assertEqual(dr.month_end(2000, 2), date(2000, 2, 29))
        self.assertEqual(dr.month_end(2400, 2), date(2400, 2, 29))

    def test_month_end_thirty_day_months(self):
        for year in (2023, 2024):
            for month in (4, 6, 9, 11):
                self.assertEqual(dr.month_end(year, month), date(year, month, 30))

    def test_month_end_rejects_invalid_months(self):
        """MUT-ME-MONTHVAL: 0, 13, -1 y 100 deben lanzar ValueError."""
        for bad in (0, 13, -1, 100, -12, 1000):
            with self.assertRaises(ValueError):
                dr.month_end(2023, bad)

    def test_month_end_rejects_invalid_months_in_leap_year(self):
        for bad in (0, 13, -1, 100):
            with self.assertRaises(ValueError):
                dr.month_end(2024, bad)

    def test_month_end_invalid_month_message_mentions_month(self):
        with self.assertRaises(ValueError) as ctx:
            dr.month_end(2023, 13)
        self.assertIn("13", str(ctx.exception))


# --------------------------------------------------------------------------
# is_leap
# --------------------------------------------------------------------------

class TestIsLeapRegressions(unittest.TestCase):
    """MUT-LEAP-JULIAN: regla gregoriana completa."""

    def test_century_years_not_divisible_by_400_are_common(self):
        for year in (1700, 1800, 1900, 2100, 2200, 2300, 2500, 3000):
            self.assertFalse(dr.is_leap(year), f"{year} no debe ser bisiesto")

    def test_century_years_divisible_by_400_are_leap(self):
        for year in (1600, 2000, 2400, 2800, 3200):
            self.assertTrue(dr.is_leap(year), f"{year} debe ser bisiesto")

    def test_common_four_year_years_are_not_leap(self):
        for year in (2021, 2022, 2023, 2025, 2026, 2027):
            self.assertFalse(dr.is_leap(year), f"{year} no debe ser bisiesto")

    def test_leap_four_year_years_are_leap(self):
        for year in (2020, 2024, 2028, 2032, 2004, 1996):
            self.assertTrue(dr.is_leap(year), f"{year} debe ser bisiesto")

    def test_is_leap_agrees_with_february_length(self):
        """Coherencia total: la longitud de febrero debe seguir a is_leap."""
        for year in (1900, 1996, 1999, 2000, 2023, 2024, 2100, 2400):
            expected = 29 if dr.is_leap(year) else 28
            self.assertEqual(dr.month_end(year, 2).day, expected, str(year))


# --------------------------------------------------------------------------
# add_months
# --------------------------------------------------------------------------

class TestAddMonthsRegressions(unittest.TestCase):
    """MUT-AM-EOMALWAYS, MUT-AM-NOCLAMP, MUT-AM-GUARD."""

    def test_mid_month_day_is_preserved(self):
        """MUT-AM-EOMALWAYS: clampear siempre al fin de mes rompe los dias 15."""
        self.assertEqual(dr.add_months(date(2023, 1, 15), 1), date(2023, 2, 15))
        self.assertEqual(dr.add_months(date(2023, 1, 15), 4), date(2023, 5, 15))
        self.assertEqual(dr.add_months(date(2023, 2, 27), 1), date(2023, 3, 27))
        self.assertEqual(dr.add_months(date(2024, 2, 28), 1), date(2024, 3, 28))

    def test_day_before_end_of_month_is_not_clamped(self):
        """Un dia que no es el ultimo del mes no puede saltar al ultimo."""
        self.assertEqual(dr.add_months(date(2023, 1, 30), 1), date(2023, 2, 28))
        self.assertEqual(dr.add_months(date(2023, 1, 29), 1), date(2023, 2, 28))
        self.assertEqual(dr.add_months(date(2023, 4, 29), 1), date(2023, 5, 29))

    def test_end_of_month_is_preserved_across_months(self):
        """MUT-AM-NOCLAMP: sin clampeo, 31-ene + 1 -> 31-feb (invalido)."""
        self.assertEqual(dr.add_months(date(2023, 1, 31), 1), date(2023, 2, 28))
        self.assertEqual(dr.add_months(date(2023, 1, 31), 2), date(2023, 3, 31))
        self.assertEqual(dr.add_months(date(2023, 1, 31), 3), date(2023, 4, 30))
        self.assertEqual(dr.add_months(date(2023, 3, 31), -1), date(2023, 2, 28))
        self.assertEqual(dr.add_months(date(2023, 5, 31), 1), date(2023, 6, 30))

    def test_end_of_month_preserved_into_leap_february(self):
        self.assertEqual(dr.add_months(date(2024, 1, 31), 1), date(2024, 2, 29))
        self.assertEqual(dr.add_months(date(2023, 1, 31), 1), date(2023, 2, 28))

    def test_negative_n_subtracts_months(self):
        """MUT-AM-GUARD: un guardia invertido hace fallar todo n positivo/negativo."""
        self.assertEqual(dr.add_months(date(2023, 3, 15), -1), date(2023, 2, 15))
        self.assertEqual(dr.add_months(date(2023, 1, 15), -1), date(2022, 12, 15))
        self.assertEqual(dr.add_months(date(2023, 1, 15), -13), date(2021, 12, 15))
        self.assertEqual(dr.add_months(date(2023, 1, 15), 13), date(2024, 2, 15))

    def test_add_months_zero_is_identity(self):
        for d in (date(2023, 1, 31), date(2023, 1, 15), date(2024, 2, 29),
                  date(2023, 2, 28), date(2023, 4, 30)):
            self.assertEqual(dr.add_months(d, 0), d, str(d))

    def test_add_months_across_year_boundary(self):
        self.assertEqual(dr.add_months(date(2023, 12, 15), 1), date(2024, 1, 15))
        self.assertEqual(dr.add_months(date(2023, 12, 15), 12), date(2024, 12, 15))
        self.assertEqual(dr.add_months(date(2023, 1, 15), -1), date(2022, 12, 15))
        self.assertEqual(dr.add_months(date(2023, 1, 15), -12), date(2022, 1, 15))

    def test_add_months_never_raises_for_valid_inputs(self):
        """Ningun overflow: el resultado siempre es una fecha real."""
        base = date(2023, 1, 1)
        for n in range(-60, 61):
            for day in (1, 15, 28, 29, 30, 31):
                d = date(2023, 1, day)
                result = dr.add_months(d, n)
                self.assertIsInstance(result, date)
                self.assertLessEqual(
                    result.day, dr.month_end(result.year, result.month).day
                )

    def test_property_target_month_is_correct(self):
        """Propiedad: el mes destino es siempre el correcto (n en rango amplio)."""
        bases = [
            date(2023, 1, 31), date(2024, 2, 29), date(2023, 2, 28),
            date(2023, 3, 15), date(2023, 12, 31), date(2000, 1, 1),
            date(2100, 6, 30), date(2023, 5, 31),
        ]
        for d in bases:
            for n in range(-48, 49):
                result = dr.add_months(d, n)
                total = d.year * 12 + (d.month - 1) + n
                expected_year, expected_month_index = divmod(total, 12)
                self.assertEqual(
                    (result.year, result.month),
                    (expected_year, expected_month_index + 1),
                    f"add_months({d}, {n}) -> {result}",
                )

    def test_property_result_day_never_exceeds_month_end(self):
        """Propiedad: el dia resultante es <= month_end(anio, mes) del destino."""
        for d in (date(2023, 1, 31), date(2023, 3, 31), date(2024, 1, 31),
                  date(2023, 5, 31), date(2023, 8, 31), date(2023, 10, 31)):
            for n in range(-36, 37):
                result = dr.add_months(d, n)
                self.assertLessEqual(
                    result.day,
                    dr.month_end(result.year, result.month).day,
                    f"add_months({d}, {n}) -> {result} desborda el mes",
                )

    def test_property_end_of_month_is_preserved(self):
        """Propiedad: si la entrada es fin de mes, la salida tambien lo es."""
        eoms = []
        for year in (2023, 2024, 1900, 2000, 2100):
            for month in range(1, 13):
                eoms.append(dr.month_end(year, month))
        for d in eoms:
            for n in range(-24, 25):
                result = dr.add_months(d, n)
                self.assertEqual(
                    result,
                    dr.month_end(result.year, result.month),
                    f"add_months({d}, {n}) = {result} perdio el fin de mes",
                )


# --------------------------------------------------------------------------
# daterange
# --------------------------------------------------------------------------

class TestDaterangeRegressions(unittest.TestCase):
    """MUT-DR-INCLEND, MUT-DR-NOVALID."""

    def test_end_date_is_excluded(self):
        """MUT-DR-INCLEND: con ``<=`` el rango incluye ``end``."""
        result = dr.daterange(date(2023, 1, 1), date(2023, 1, 4))
        self.assertEqual(len(result), 3)
        self.assertNotIn(date(2023, 1, 4), result)
        self.assertEqual(result[-1], date(2023, 1, 3))

    def test_single_day_range_has_one_element(self):
        d = date(2023, 5, 5)
        self.assertEqual(dr.daterange(d, d + timedelta(days=1)), [d])

    def test_empty_range_when_start_equals_end(self):
        for d in (date(2023, 1, 1), date(2024, 2, 29), date(2023, 6, 30)):
            self.assertEqual(dr.daterange(d, d), [])

    def test_inverted_range_raises_value_error(self):
        """MUT-DR-NOVALID: sin validacion devolveria lista vacia silenciosa."""
        with self.assertRaises(ValueError):
            dr.daterange(date(2023, 1, 2), date(2023, 1, 1))
        with self.assertRaises(ValueError):
            dr.daterange(date(2023, 1, 2), date(2022, 12, 31))

    def test_inverted_range_never_returns_empty_list(self):
        """Un rango invertido debe fallar, jamas devolver ``[]``."""
        try:
            result = dr.daterange(date(2023, 1, 5), date(2023, 1, 1))
        except ValueError:
            return
        self.fail(f"se esperaba ValueError, se obtuvo {result!r}")

    def test_property_length_equals_end_minus_start(self):
        """Propiedad: ``len(daterange(s, e)) == (e - s).days`` siempre."""
        cases = [
            (date(2023, 1, 1), date(2023, 1, 1)),
            (date(2023, 1, 1), date(2023, 1, 2)),
            (date(2023, 1, 1), date(2023, 1, 31)),
            (date(2024, 2, 1), date(2024, 3, 1)),
            (date(2023, 12, 20), date(2024, 1, 10)),
            (date(2023, 1, 31), date(2023, 2, 1)),
            (date(2022, 1, 1), date(2025, 1, 1)),
        ]
        for start, end in cases:
            result = dr.daterange(start, end)
            self.assertEqual(len(result), (end - start).days, f"{start}..{end}")

    def test_property_dates_are_consecutive(self):
        """Propiedad: cada elemento es exactamente 1 dia posterior al anterior."""
        for start, end in [
            (date(2023, 1, 1), date(2023, 1, 20)),
            (date(2024, 2, 25), date(2024, 3, 5)),
            (date(2023, 1, 30), date(2023, 2, 3)),
        ]:
            result = dr.daterange(start, end)
            for previous, current in zip(result, result[1:]):
                self.assertEqual(current - previous, timedelta(days=1),
                                 f"{previous} -> {current} no es consecutive")

    def test_property_first_and_last_elements(self):
        for start, end in [
            (date(2023, 1, 1), date(2023, 1, 10)),
            (date(2024, 2, 27), date(2024, 3, 2)),
        ]:
            result = dr.daterange(start, end)
            self.assertEqual(result[0], start)
            self.assertEqual(result[-1], end - timedelta(days=1))
            self.assertTrue(all(start <= d < end for d in result))

    def test_leap_day_is_included_when_crossed(self):
        result = dr.daterange(date(2024, 2, 27), date(2024, 3, 2))
        self.assertIn(date(2024, 2, 29), result)
        self.assertEqual(len(result), 4)


# --------------------------------------------------------------------------
# parse_iso
# --------------------------------------------------------------------------

class TestParseIsoRegressions(unittest.TestCase):
    """MUT-PI-NORAISE."""

    INVALID_INPUTS = [
        "",
        "2023-13-01",
        "2023-00-10",
        "2023-02-30",
        "2023-04-31",
        "01/01/2023",
        "2023-1-1",
        "2023-01-1",
        "2023-1-01",
        "not-a-date",
        " 2023-01-01",
        "2023-01-01 ",
        "2023/01/01",
        "2023-01-01T00:00:00Z",
        "2023-01-0",
        "2023-01-011",
        "20230101",
        "abcd-ef-gh",
        "2023-01-01-01",
        "15-07-2023",
    ]

    def test_invalid_inputs_raise_value_error(self):
        """MUT-PI-NORAISE: cada input invalido debe lanzar ValueError."""
        for bad in self.INVALID_INPUTS:
            with self.subTest(input=bad):
                with self.assertRaises(ValueError):
                    dr.parse_iso(bad)

    def test_invalid_inputs_message_is_informative(self):
        for bad in self.INVALID_INPUTS:
            with self.subTest(input=bad):
                with self.assertRaises(ValueError) as ctx:
                    dr.parse_iso(bad)
                message = str(ctx.exception)
                self.assertIn("Invalid ISO date string", message)
                self.assertIn(repr(bad), message)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            dr.parse_iso("")

    def test_valid_inputs_parse_exactly(self):
        cases = {
            "2023-01-01": date(2023, 1, 1),
            "2024-02-29": date(2024, 2, 29),
            "1999-12-31": date(1999, 12, 31),
            "2000-02-29": date(2000, 2, 29),
        }
        for text, expected in cases.items():
            self.assertEqual(dr.parse_iso(text), expected, text)

    def test_parse_iso_roundtrip_with_daterange(self):
        """Coherencia entre parse_iso y daterange."""
        start = dr.parse_iso("2024-02-28")
        end = dr.parse_iso("2024-03-02")
        result = dr.daterange(start, end)
        self.assertEqual([d.isoformat() for d in result],
                         ["2024-02-28", "2024-02-29", "2024-03-01"])


if __name__ == "__main__":
    unittest.main()
