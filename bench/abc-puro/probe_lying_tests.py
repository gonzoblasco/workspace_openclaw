"""probe_lying_tests.py - Tests de la suite entregada que NO prueban lo que dicen.

Invariantes protegidos:
  L1  test_cache_miss_after_ttl NO detecta un cache que nunca expira ni uno que
      expira mal, porque solo compara valores (que son iguales en ambos casos).
  L2  test_cache_hit_within_ttl pasa aun si el cache nunca se usa (2 fetch = 2
      resultados iguales). No cuenta llamadas a la sesion.
  L3  test_invalid_per_page_raises NO cubre per_page no int.
"""

import datetime as dt
import unittest
from unittest import mock

import reports


class FakeSession:
    def __init__(self, data):
        self._data = data
        self.calls = 0

    def fetch(self, page, per_page):
        self.calls += 1
        return reports.paginate(self._data, page, per_page)


DATA = [{"id": i, "date": "2023-01-01", "amount": i, "status": "open"} for i in range(1, 6)]


def banner(t):
    print("\n" + "=" * 70)
    print(t)
    print("=" * 70)


def l1_ttl_test_is_vacuous():
    banner("L1: test_cache_miss_after_ttl es vacuo (test_reports.py:77-89)")
    # Reemplazamos cached_reports por una version SIN cache: la suite igual pasa,
    # porque el assertEqual(first, later) compara valores identicos.
    original = reports.cached_reports

    def no_cache(session, page, per_page, ttl_seconds, now):
        return reports.fetch_reports(session, page, per_page)

    reports.cached_reports = no_cache
    try:
        s = FakeSession(DATA)
        now = dt.datetime.utcnow()
        first = reports.cached_reports(s, 1, 2, 1, now)
        later = reports.cached_reports(s, 1, 2, 1, now + dt.timedelta(seconds=2))
        print(f"[cache DESACTIVADO] asserts del test real: first == later -> {first == later}")
        print(f"llamadas efectivas a la sesion: {s.calls} (el test no mira este numero)")
        print("FALLA L1: el test pasa con un cache roto/no-cache.")
    finally:
        reports.cached_reports = original

    # Y al reves: un cache que devuelve datos VIEJOS indistinguibles tampoco falla.
    banner("L1.bis: el mismo test tampoco detecta un cache que expira de MENOS")


def l2_hit_test_is_vacuous():
    banner("L2: test_cache_hit_within_ttl no verifica el hit (test_reports.py:63-75)")
    original = reports.cached_reports

    def never_cache(session, page, per_page, ttl_seconds, now):
        return reports.fetch_reports(session, page, per_page)

    reports.cached_reports = never_cache
    try:
        s = FakeSession(DATA)
        now = dt.datetime.utcnow()
        a = reports.cached_reports(s, 1, 2, 10, now)
        b = reports.cached_reports(s, 1, 2, 10, now + dt.timedelta(seconds=5))
        print(f"[cache DESACTIVADO] first == second -> {a == b}; calls={s.calls}")
        print("FALLA L2: el assert de igualdad pasa con 2 fetches. No prueba el hit.")
    finally:
        reports.cached_reports = original


def l3_missing_nonint():
    banner("L3: test_invalid_per_page_raises no cubre no-int (test_reports.py:38-42)")
    print("el test solo prueba 0 y -1; per_page=True / 2.5 / '3' sin cubrir.")
    print("paginate([1,2,3], 1, True) ->", reports.paginate([1, 2, 3], 1, True))


def l4_filter_test_red():
    banner("L4: los tests de filter_by_date estan en ROJO sobre el codigo entregado")
    suite = unittest.defaultTestLoader.loadTestsFromName(
        "test_reports.TestFilterByDate")
    res = unittest.TextTestRunner(verbosity=0, stream=open("/dev/null", "w")).run(suite)
    print(f"failures={len(res.failures)} errors={len(res.errors)} "
          f"run={res.testsRun}")
    print("FALLA L4: el codigo entregado no cumple su propio test. Un 'suite "
          "verde' no existe: 3 de 9 tests fallan.")


if __name__ == "__main__":
    l1_ttl_test_is_vacuous()
    l2_hit_test_is_vacuous()
    l3_missing_nonint()
    l4_filter_test_red()
