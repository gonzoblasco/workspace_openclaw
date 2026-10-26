"""probe_defects.py - Evidencias de defectos en reports.py (no modifica nada).

Invariantes protegidos:
  P1  filter_by_date es INCLUSIVO en `until` (criterio de aceptacion del spec).
  P2  paginate(per_page=0) lanza ValueError (criterio de aceptacion del spec).
  P3  paginate(per_page no int) lanza ValueError (criterio de aceptacion del spec).
  P4  cached_reports no devuelve un valor mas viejo que ttl_seconds.
  P5  cache de cached_reports NO se contamina entre sesiones distintas.
"""

import datetime as dt

import reports


class FakeSession:
    def __init__(self, data, calls_counter=None):
        self._data = data
        self.calls = 0
        self._counter = calls_counter

    def fetch(self, page, per_page):
        self.calls += 1
        if self._counter is not None:
            self._counter[0] += 1
        return reports.paginate(self._data, page, per_page)


REPORTS = [
    {"id": 1, "date": "2023-01-01", "amount": 100, "status": "open"},
    {"id": 2, "date": "2023-01-05", "amount": 200, "status": "closed"},
    {"id": 3, "date": "2023-02-10", "amount": 150, "status": "open"},
    {"id": 4, "date": "2023-03-15", "amount": 300, "status": "pending"},
    {"id": 5, "date": "2023-04-20", "amount": "bad", "status": "closed"},
]


def banner(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def p1_until_inclusive():
    banner("P1: filter_by_date inclusivo en `until` (reports.py:54)")
    got = [r["id"] for r in reports.filter_by_date(
        REPORTS, dt.date(2023, 1, 5), dt.date(2023, 3, 15))]
    print("esperado: [2, 3, 4]   (el 4 esta en la fecha `until`, debe entrar)")
    print("obtenido:", got)
    print("FALLA P1" if 4 not in got else "OK P1")

    # caso borde: un solo dia, since == until
    got_same = [r["id"] for r in reports.filter_by_date(
        REPORTS, dt.date(2023, 1, 5), dt.date(2023, 1, 5))]
    print("since == until == 2023-01-05 -> esperado [2], obtenido:", got_same)
    print("FALLA P1 (rango de un dia vacio)" if not got_same else "OK P1-same")
    print("NOTA: la suite no lo detecta porque test_inclusive_bounds FALLA; "
          "no hay test que aforce el caso inclusivo superior.")


def p2_per_page_zero():
    banner("P2.1: paginate(per_page=0) debe lanzar ValueError (reports.py:61)")
    try:
        out = reports.paginate([1, 2, 3], page=1, per_page=0)
        print("NO lanzo ValueError. retorno:", out)
        print("FALLA P2.1 (division degenerada: devuelve [] silenciosamente)")
    except ValueError as exc:
        print("OK P2.1:", exc)

    banner("P2.2: paginate(per_page=-1) lanza ValueError (correcto)")
    try:
        reports.paginate([1, 2, 3], page=1, per_page=-1)
        print("FALLA P2.2")
    except ValueError as exc:
        print("OK P2.2:", exc)


def p3_per_page_not_int():
    banner("P3: paginate(per_page no int) debe lanzar ValueError (reports.py:61)")
    for bad in (
        3.0,
        "3",
        True,
    ):
        try:
            out = reports.paginate([1, 2, 3, 4], page=2, per_page=bad)
            print(f"per_page={bad!r}: NO lanzo ValueError. retorno={out}")
            print(f"FALLA P3 ({bad!r})")
        except ValueError as exc:
            print(f"per_page={bad!r}: OK ValueError: {exc}")

    banner("P3.bis: page no int (bug espejo, no cubierto por el spec explicitamente)")
    out = reports.paginate([1, 2, 3, 4], page=2.5, per_page=1)
    print("page=2.5 -> retorno:", out, "(se descarta silenciosamente a [])")
    out = reports.paginate([1, 2, 3, 4], page=2.0, per_page=1)
    print("page=2.0 -> retorno:", out, "(flota, is int False -> [] silencioso)")


def p4_ttl_direction():
    banner("P4: cached_reports y la direccion del TTL (reports.py:85)")
    session = FakeSession(REPORTS)
    t0 = dt.datetime(2026, 10, 25, 12, 0, 0)

    # caso A: now anterior a la entrada de cache (reloj retrocede / llamadas
    # con `now` monotonico mal usado). age negativo <= ttl -> hit eterno.
    reports.cached_reports(session, 1, 2, 60, t0)
    calls_after_first = session.calls
    reports.cached_reports(session, 1, 2, 60, t0 - dt.timedelta(days=365))
    print(f"now 1 anio ANTES del timestamp cacheado, ttl=60s -> "
          f"calls={session.calls} (esperado 2, hubo fetch? {session.calls > calls_after_first})")
    if session.calls == calls_after_first:
        print("FALLA P4: age negativo (<= ttl) produce hit con datos 'del futuro'.")

    # caso B: ttl=0 debe forzar miss SIEMPRE (el valor no puede tener edad > 0
    # si se respeta la semantica estricta de 'no mas viejo que ttl').
    session2 = FakeSession(REPORTS)
    b = dt.datetime(2026, 10, 25, 12, 0, 0)
    reports.cached_reports(session2, 1, 2, 0, b)
    reports.cached_reports(session2, 1, 2, 0, b)
    print(f"ttl=0, dos llamadas con el mismo `now` -> calls={session2.calls} "
          f"(esperado 2 por semantica estricta; obtenido {'hit' if session2.calls == 1 else 'miss'})")
    print("NOTA: con age=0 <= 0 hay hit; aceptable si ttl=0 se interpreta como "
          "'instantaneo'. Se reporta como ambiguedad BAJA, no como bug duro.")

    # caso C: la condicion usa <= en vez de <. Con age == ttl exacto devuelve hit.
    session3 = FakeSession(REPORTS)
    c = dt.datetime(2026, 10, 25, 12, 0, 0)
    reports.cached_reports(session3, 1, 2, 10, c)
    reports.cached_reports(session3, 1, 2, 10, c + dt.timedelta(seconds=10))
    print(f"age == ttl exactamente (10s)== > calls={session3.calls} "
          f"(<= devuelve hit; '<' habria hecho miss). Off-by-one de borde.")


def p5_cache_key_id_leak():
    banner("P5: la clave de cache usa id(session) (reports.py:81)")
    s1 = FakeSession(REPORTS)
    t = dt.datetime(2026, 10, 25, 12, 0, 0)
    reports.cached_reports(s1, 1, 2, 3600, t)
    first_calls = s1.calls
    del s1
    # Otro objeto puede reutilizar el mismo id: simulamos con un mock que
    # reporta un id identico (pathologico pero legal en CPython al reciclar id).
    s2 = FakeSession([{"id": 99, "date": "2024-01-01", "amount": 1, "status": "x"}])
    reports._CACHE[(id(s2), 1, 2)] = (t, [{"id": "STALE-FROM-OTHER-SESSION"}])
    out = reports.cached_reports(s2, 1, 2, 3600, t + dt.timedelta(seconds=1))
    print("sesion distinta con id reciclado -> retorno:", out)
    print(f"s2.calls={s2.calls} (esperado 1: debio fetchear de la sesion nueva)")
    print("FALLA P5" if out == [{"id": "STALE-FROM-OTHER-SESSION"}] else "OK P5")
    print("NOTA: ademas el cache es un dict GLOBAL de modulo sin eviction -> "
          "crecimiento sin limite y estado compartido entre tests.")


def p6_summarize_silent():
    banner("P6: summarize traga errores de amount silenciosamente (reports.py:102-105)")
    data = [{"amount": "bad"}, {"amount": None}, {"amount": "1e999"}, {"amount": True}]
    print("input:", data)
    print("summary:", reports.summarize(data))
    print("NOTA: count=4 y total_amount cuenta como 0/1.0 sin avisar; '1e999' -> inf.")
    print("'amount': True suma 1.0 (bool es int). No es violacion del spec, "
          "pero es un riesgo de reporte financiero silenciosamente incorrecto (BAJO/MEDIO).")


def p7_mutability():
    banner("P7: cached_reports devuelve la lista cacheada por referencia (reports.py:87)")
    s = FakeSession(REPORTS)
    t = dt.datetime(2026, 10, 25, 12, 0, 0)
    a = reports.cached_reports(s, 1, 2, 3600, t)
    a.append({"id": "INJECTED"})
    b = reports.cached_reports(s, 1, 2, 3600, t + dt.timedelta(seconds=1))
    print("tras mutar el retorno del primer hit, segundo hit len =", len(b))
    print("FALLA P7: el caller corrompe el cache compartido." if len(b) != 2 else "OK P7")
    print("NOTA: en el miss path hace list(fresh) (linea 90) pero en el hit path "
          "devuelve `data` crudo (linea 87). Inconsistente.")


if __name__ == "__main__":
    p1_until_inclusive()
    p2_per_page_zero()
    p3_per_page_not_int()
    p4_ttl_direction()
    p5_cache_key_id_leak()
    p6_summarize_silent()
    p7_mutability()
