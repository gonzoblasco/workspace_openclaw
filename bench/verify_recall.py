"""Verifica el recall de un revisor B contra el ground truth.

NO debe estar en el working directory del agente revisor.

Uso:
    python3 bench/verify_recall.py bench/b-deepseek bench/b-beam bench/b-minimax
"""
import datetime as dt
import importlib.util
import pathlib
import sys


def load(directory: str):
    path = pathlib.Path(directory) / "reports.py"
    spec = importlib.util.spec_from_file_location("m_" + pathlib.Path(directory).name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(directory: str) -> dict:
    m = load(directory)
    result = {}

    # BUG-1: per_page=0 debe lanzar ValueError.
    try:
        m.paginate([1, 2, 3], 1, 0)
        result["BUG-1"] = "NO corregido (no lanza)"
    except ValueError:
        result["BUG-1"] = "OK"
    except Exception as exc:  # noqa: BLE001
        result["BUG-1"] = f"NO corregido ({type(exc).__name__})"

    # BUG-2: el limite `until` debe ser inclusivo.
    got = [
        r["id"]
        for r in m.filter_by_date(
            [{"id": 1, "date": "2023-03-15"}], dt.date(2023, 1, 1), dt.date(2023, 3, 15)
        )
    ]
    result["BUG-2"] = "OK" if got == [1] else f"NO corregido (>{got}<)"

    # BUG-3: el TTL tiene que expirar.
    class Counting:
        def __init__(self):
            self.calls = 0

        def fetch(self, page, per_page):
            self.calls += 1
            return [{"id": self.calls}]

    session = Counting()
    now = dt.datetime(2026, 1, 1)
    m.cached_reports(session, 1, 2, 1, now)
    m.cached_reports(session, 1, 2, 1, now + dt.timedelta(seconds=10))
    result["BUG-3"] = "OK" if session.calls == 2 else f"NO corregido (calls={session.calls})"

    # BUG-4: el hit debe devolver una copia defensiva.
    class Simple:
        def fetch(self, page, per_page):
            return [{"id": 1}]

    simple = Simple()
    m.cached_reports(simple, 1, 2, 60, now)  # miss
    hit = m.cached_reports(simple, 1, 2, 60, now)  # hit
    hit.append({"x": 1})
    again = m.cached_reports(simple, 1, 2, 60, now)
    result["BUG-4"] = "OK" if len(again) == 1 else "NO corregido (cache contaminado)"

    return result


def main() -> int:
    dirs = sys.argv[1:] or ["bench/b-deepseek", "bench/b-beam", "bench/b-minimax"]
    for directory in dirs:
        result = check(directory)
        found = sum(1 for v in result.values() if v == "OK")
        detail = "  ".join(f"{k}={v}" for k, v in result.items())
        print(f"{directory:22s} RECALL={found}/4   {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
