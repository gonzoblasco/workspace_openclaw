"""test_c_regressions.py - Red de regresion del Agente C (ABC pipeline).

Tests de regresion para los defectos de produccion reportados por el revisor B
y corregidos por el autor A.  Cada test falla si el bug correspondiente
regresa.

Invariantes cubiertos (por test, en el docstring de cada uno):

  R1  filter_by_date es INCLUSIVO en `until` y en `since`.
  R2  paginate(per_page=0) lanza ValueError.
  R3  cached_reports no devuelve un valor cacheado mas viejo que ttl_seconds
      (TTL respetado en ambas direcciones: nunca expira antes de tiempo ni
      nunca expira nunca / hit eterno).
  R4  cached_reports devuelve una COPIA: el llamador no puede contaminar el
      cache interno.
  R5  El cache NO se comparte entre sesiones distintas (no se colisiona por
      id(session) ni existe un cache global de modulo).
  R6  summarize ignora booleanos como `amount` (bool es subclase de int).
  R7  summarize no aborta ni infla el total con `amount` infinito / no numerico.
  R8  paginate(per_page=True) lanza ValueError (bool no es un per_page valido).
"""

import datetime as dt
import unittest

import reports


class FakeSession:
    """Sesion minima con contador de llamadas al backend."""

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

T0 = dt.datetime(2026, 10, 25, 12, 0, 0)


class TestR1FilterByDateInclusive(unittest.TestCase):
    """R1: los extremos del rango son inclusivos."""

    def test_until_edge_is_included(self):
        out = reports.filter_by_date(SAMPLE_REPORTS, dt.date(2023, 1, 5), dt.date(2023, 3, 15))
        self.assertIn(4, [r["id"] for r in out], "el registro en la fecha `until` debe entrar")

    def test_since_edge_is_included(self):
        out = reports.filter_by_date(SAMPLE_REPORTS, dt.date(2023, 1, 5), dt.date(2023, 12, 31))
        self.assertIn(2, [r["id"] for r in out], "el registro en la fecha `since` debe entrar")

    def test_single_day_range_is_not_empty(self):
        out = reports.filter_by_date(SAMPLE_REPORTS, dt.date(2023, 1, 5), dt.date(2023, 1, 5))
        self.assertEqual([r["id"] for r in out], [2], "since == until debe devolver ese dia")

    def test_outside_bounds_are_excluded(self):
        out = reports.filter_by_date(SAMPLE_REPORTS, dt.date(2023, 1, 5), dt.date(2023, 3, 15))
        ids = [r["id"] for r in out]
        self.assertNotIn(1, ids)
        self.assertNotIn(5, ids)


class TestR2PerPageZero(unittest.TestCase):
    """R2: per_page = 0 lanza ValueError (no devuelve [] silenciosamente)."""

    def test_per_page_zero_raises(self):
        with self.assertRaises(ValueError):
            reports.paginate([1, 2, 3], page=1, per_page=0)

    def test_per_page_zero_raises_even_on_out_of_range_page(self):
        with self.assertRaises(ValueError):
            reports.paginate([1, 2, 3], page=99, per_page=0)


class TestR3TtlRespected(unittest.TestCase):
    """R3: el TTL se respeta; el cache no expira temprano ni nunca."""

    def test_entry_expires_after_ttl(self):
        s = FakeSession(SAMPLE_REPORTS)
        reports.cached_reports(s, 1, 2, ttl_seconds=10, now=T0)
        reports.cached_reports(s, 1, 2, ttl_seconds=10, now=T0 + dt.timedelta(seconds=30))
        self.assertEqual(s.calls, 2, "pasado el TTL debe haber un fetch nuevo")

    def test_entry_is_still_valid_just_below_ttl(self):
        s = FakeSession(SAMPLE_REPORTS)
        reports.cached_reports(s, 1, 2, ttl_seconds=10, now=T0)
        reports.cached_reports(s, 1, 2, ttl_seconds=10, now=T0 + dt.timedelta(seconds=9))
        self.assertEqual(s.calls, 1, "antes de cumplir el TTL debe haber hit")

    def test_future_timestamp_does_not_produce_a_hit(self):
        """Un `now` anterior al timestamp cacheado no debe servir la entrada."""
        s = FakeSession(SAMPLE_REPORTS)
        reports.cached_reports(s, 1, 2, ttl_seconds=60, now=T0)
        reports.cached_reports(s, 1, 2, ttl_seconds=60, now=T0 - dt.timedelta(days=365))
        self.assertEqual(s.calls, 2, "una entrada 'del futuro' debe tratarse como miss")

    def test_ttl_zero_never_serves_stale_data(self):
        """ttl=0: nunca se puede servir una entrada (ni siquiera de edad 0)."""
        s = FakeSession(SAMPLE_REPORTS)
        reports.cached_reports(s, 1, 2, ttl_seconds=0, now=T0)
        reports.cached_reports(s, 1, 2, ttl_seconds=0, now=T0)
        self.assertGreaterEqual(
            s.calls, 2,
            "con ttl=0 no se puede servir nada cacheado: debe haber fetch en cada llamada",
        )

    def test_entry_older_than_ttl_is_never_served(self):
        """Propiedad del spec: NUNCA devolver un valor mas viejo que ttl."""
        s = FakeSession(SAMPLE_REPORTS)
        reports.cached_reports(s, 1, 2, ttl_seconds=10, now=T0)
        reports.cached_reports(s, 1, 2, ttl_seconds=10, now=T0 + dt.timedelta(seconds=11))
        self.assertEqual(s.calls, 2, "una entrada de edad > ttl debe descartarse")

    def test_ttl_boundary_age_equal_to_ttl(self):
        """AMBIGUEDAD documentada (ver reporte del Agente C).

        El spec dice 'no devuelve un valor cacheado mas viejo que ttl_seconds',
        lo que ADMITE servir una entrada de edad exactamente == ttl.  El codigo
        actual usa la ventana estricta 0 <= edad < ttl y la descarta.
        Este test NO fija una de las dos semanticas (seria sobre-constreir al
        codigo contra el spec); verifica solo el invariante que ambas
        comparten: lo que se devuelve nunca es mas viejo que el TTL.
        """
        s = FakeSession(SAMPLE_REPORTS)
        reports.cached_reports(s, 1, 2, ttl_seconds=10, now=T0)
        out = reports.cached_reports(s, 1, 2, ttl_seconds=10, now=T0 + dt.timedelta(seconds=10))
        self.assertEqual([r["id"] for r in out], [1, 2], "el contenido devuelto debe ser el correcto")
        self.assertIn(s.calls, (1, 2), "edad == ttl: hit o miss, pero nunca datos viejos/corruptos")

    def test_different_page_is_a_different_cache_entry(self):
        s = FakeSession(SAMPLE_REPORTS)
        reports.cached_reports(s, 1, 2, ttl_seconds=60, now=T0)
        reports.cached_reports(s, 2, 2, ttl_seconds=60, now=T0)
        self.assertEqual(s.calls, 2, "la clave de cache debe incluir la pagina")


class TestR4CacheNotContaminable(unittest.TestCase):
    """R4: el hit devuelve una copia; el llamador no puede mutar el cache."""

    def test_mutating_the_returned_list_does_not_corrupt_the_cache(self):
        """Defecto 10: el hit devolvia la lista interna por referencia.

        Lo que el spec exige es que el llamador no pueda *corromper el cache*
        (agregar/quitar elementos).  La copia es superficial: los dicts
        individuales siguen siendo compartidos, comportamiento que el spec no
        regula y que por eso NO se afirma aqui (ver nota en el reporte).
        """
        s = FakeSession(SAMPLE_REPORTS)
        # 1er hit: la entrada ya esta en el cache, el retorno proviene del cache.
        reports.cached_reports(s, 1, 2, ttl_seconds=60, now=T0)  # miss
        hit = reports.cached_reports(s, 1, 2, ttl_seconds=60, now=T0 + dt.timedelta(seconds=1))
        self.assertEqual(s.calls, 1, "el segundo acceso debe ser un hit (sin fetch nuevo)")
        # El llamador corrompe lo que recibio en el HIT.
        hit.append({"id": "INJECTED"})
        hit.clear()
        # 3er hit: debe devolver la entrada INTACTA del cache.
        second = reports.cached_reports(s, 1, 2, ttl_seconds=60, now=T0 + dt.timedelta(seconds=2))
        self.assertEqual(s.calls, 1, "el tercer acceso tambien debe ser un hit")
        self.assertEqual(len(second), 2, "el cache interno no debe crecer ni vaciarse por mutacion externa")
        self.assertNotIn("INJECTED", [r.get("id") for r in second])
        self.assertEqual([r["id"] for r in second], [1, 2])

    def test_returned_list_is_not_the_internal_object(self):
        s = FakeSession(SAMPLE_REPORTS)
        a = reports.cached_reports(s, 1, 2, ttl_seconds=60, now=T0)
        b = reports.cached_reports(s, 1, 2, ttl_seconds=60, now=T0 + dt.timedelta(seconds=1))
        self.assertIsNot(a, b, "cada hit debe devolver una lista nueva")


class TestR5CacheIsolatedPerSession(unittest.TestCase):
    """R5: no hay colision por id(session) ni cache global compartido."""

    def test_two_sessions_do_not_share_cache_entries(self):
        s1 = FakeSession(SAMPLE_REPORTS)
        s2 = FakeSession([{"id": 99, "date": "2024-01-01", "amount": 1, "status": "x"}])
        out1 = reports.cached_reports(s1, 1, 2, ttl_seconds=3600, now=T0)
        out2 = reports.cached_reports(s2, 1, 2, ttl_seconds=3600, now=T0)
        self.assertEqual([r["id"] for r in out1], [1, 2])
        self.assertEqual([r["id"] for r in out2], [99], "la sesion 2 no puede leer el cache de la sesion 1")
        self.assertEqual(s1.calls, 1)
        self.assertEqual(s2.calls, 1)

    def test_poisoned_module_level_cache_is_ignored(self):
        """Simula un id(session) reciclado: un _CACHE global pre-cargado no debe ganar."""
        s = FakeSession(SAMPLE_REPORTS)
        reports._CACHE[(id(s), 1, 2)] = (T0, [{"id": "STALE-FROM-OTHER-SESSION"}])
        try:
            out = reports.cached_reports(s, 1, 2, ttl_seconds=3600, now=T0 + dt.timedelta(seconds=1))
        finally:
            reports._CACHE.pop((id(s), 1, 2), None)
        self.assertNotEqual(
            out, [{"id": "STALE-FROM-OTHER-SESSION"}],
            "el resultado no puede provenir de una entrada ajena a la sesion",
        )
        self.assertEqual([r["id"] for r in out], [1, 2])
        self.assertEqual(s.calls, 1, "debe haber hecho fetch a la sesion propia")

    def test_recycled_id_does_not_leak_between_sessions(self):
        """Dos sesiones distintas, una liberada: la segunda no hereda el cache."""
        s1 = FakeSession(SAMPLE_REPORTS)
        reports.cached_reports(s1, 1, 2, ttl_seconds=3600, now=T0)
        del s1
        s2 = FakeSession([{"id": 77, "date": "2024-05-05", "amount": 7, "status": "z"}])
        out = reports.cached_reports(s2, 1, 2, ttl_seconds=3600, now=T0 + dt.timedelta(seconds=1))
        self.assertEqual([r["id"] for r in out], [77])
        self.assertEqual(s2.calls, 1)


class TestR6SummarizeBoolAmount(unittest.TestCase):
    """R6: un bool no es un monto valido (bool es subclase de int)."""

    def test_true_amount_does_not_contribute_to_total(self):
        summary = reports.summarize([{"id": 1, "amount": True, "status": "open"}])
        self.assertAlmostEqual(summary["total_amount"], 0.0, msg="True no puede sumar 1.0")

    def test_false_amount_does_not_contribute_to_total(self):
        summary = reports.summarize([{"id": 1, "amount": False, "status": "open"}])
        self.assertAlmostEqual(summary["total_amount"], 0.0)

    def test_bool_amount_still_counts_the_record(self):
        summary = reports.summarize([{"id": 1, "amount": True, "status": "open"}])
        self.assertEqual(summary["count"], 1)
        self.assertEqual(summary["by_status"], {"open": 1})

    def test_mixed_bool_and_numeric_amounts(self):
        summary = reports.summarize(
            [
                {"id": 1, "amount": 100, "status": "open"},
                {"id": 2, "amount": True, "status": "open"},
                {"id": 3, "amount": 50, "status": "closed"},
            ]
        )
        self.assertAlmostEqual(summary["total_amount"], 150.0)
        self.assertEqual(summary["count"], 3)


class TestR7SummarizeMalformedAmounts(unittest.TestCase):
    """R7: montos no numericos o infinitos no abortan ni inflan el total."""

    def test_infinite_amount_does_not_inflate_total(self):
        summary = reports.summarize([{"id": 1, "amount": "1e999", "status": "open"}])
        self.assertNotEqual(summary["total_amount"], float("inf"))
        self.assertFalse(summary["total_amount"] != summary["total_amount"])  # no NaN
        self.assertAlmostEqual(summary["total_amount"], 0.0)

    def test_non_numeric_amount_is_ignored(self):
        summary = reports.summarize(
            [{"id": 1, "amount": "bad", "status": "closed"}, {"id": 2, "amount": 10, "status": "open"}]
        )
        self.assertAlmostEqual(summary["total_amount"], 10.0)
        self.assertEqual(summary["count"], 2)
        self.assertEqual(summary["by_status"], {"closed": 1, "open": 1})

    def test_none_amount_is_ignored(self):
        summary = reports.summarize([{"id": 1, "amount": None, "status": "open"}])
        self.assertAlmostEqual(summary["total_amount"], 0.0)
        self.assertEqual(summary["count"], 1)

    def test_missing_amount_is_ignored(self):
        summary = reports.summarize([{"id": 1, "status": "open"}])
        self.assertAlmostEqual(summary["total_amount"], 0.0)
        self.assertEqual(summary["count"], 1)
        self.assertEqual(summary["by_status"], {"open": 1})


class TestR8PerPageBoolRejected(unittest.TestCase):
    """R8: per_page=True debe lanzar ValueError (bool es subclase de int)."""

    def test_per_page_true_raises(self):
        with self.assertRaises(ValueError):
            reports.paginate([1, 2, 3], page=1, per_page=True)

    def test_per_page_false_raises(self):
        with self.assertRaises(ValueError):
            reports.paginate([1, 2, 3], page=1, per_page=False)

    def test_per_page_bool_is_not_silently_accepted_as_one(self):
        """Si alguien 'arregla' el chequeo a `isinstance(per_page, int)`, True pasa
        como 1 y el bug reaparece."""
        try:
            out = reports.paginate([1, 2, 3], page=1, per_page=True)
        except ValueError:
            return
        self.fail(f"per_page=True deberia lanzar ValueError, devolvio {out!r}")


if __name__ == "__main__":
    unittest.main()
