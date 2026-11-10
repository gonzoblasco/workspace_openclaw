#!/usr/bin/env python3
"""
test_bench_compare.py - Tests de bench_compare.py (U4 de performance-benchmark).

    python3 agents/kanam-dev/bin/test_bench_compare.py

El caso central: un cambio puede MEJORAR y aun no cumplir el objetivo, y puede
CUMPLIR y aun haber empeorado. Aprobar cualquiera de los dos en silencio es como
se acumula una regresion que dos releases despues rompe el contrato.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bench_compare as bc  # noqa: E402


def run(metric="p95", value=100.0, unit="ms", runs=5, env="m1, node 22") -> dict:
    return {"metric": metric, "value": value, "unit": unit, "runs": runs, "env": env}


class TestCompareLowerIsBetter(unittest.TestCase):
    def test_improves_and_meets(self):
        v = bc.compare(300, 180, 200, lower_is_better=True)
        self.assertTrue(v["meets_threshold"])
        self.assertEqual(v["direction"], "mejora")
        self.assertEqual(v["verdict"], "cumple")

    def test_improves_but_still_over_threshold(self):
        v = bc.compare(300, 210, 200, lower_is_better=True)
        self.assertFalse(v["meets_threshold"])
        self.assertEqual(v["direction"], "mejora")
        self.assertEqual(v["verdict"], "no-cumple")

    def test_meets_but_worse_than_before(self):
        # 120 -> 190 con umbral 200: cumple, pero perdio 58 %.
        v = bc.compare(120, 190, 200, lower_is_better=True)
        self.assertTrue(v["meets_threshold"])
        self.assertEqual(v["direction"], "empeora")
        self.assertEqual(v["verdict"], "cumple-con-regresion")

    def test_no_change(self):
        v = bc.compare(150, 150, 200, lower_is_better=True)
        self.assertEqual(v["direction"], "sin-cambio")
        self.assertEqual(v["delta"], 0)

    def test_delta_percentage(self):
        v = bc.compare(300, 180, 200, lower_is_better=True)
        self.assertEqual(v["delta"], -120)
        self.assertEqual(v["delta_pct"], -40.0)


class TestCompareHigherIsBetter(unittest.TestCase):
    def test_throughput_improves(self):
        v = bc.compare(1000, 1500, 1200, lower_is_better=False)
        self.assertEqual(v["direction"], "mejora")
        self.assertEqual(v["verdict"], "cumple")

    def test_higher_is_better_regression_that_still_passes(self):
        v = bc.compare(2000, 1300, 1200, lower_is_better=False)
        self.assertTrue(v["meets_threshold"])
        self.assertEqual(v["verdict"], "cumple-con-regresion")


class TestVerdictExit(unittest.TestCase):
    def test_cumple_is_zero(self):
        self.assertEqual(bc.verdict_exit(bc.compare(300, 180, 200, True)), 0)

    def test_no_cumple_is_one(self):
        self.assertEqual(bc.verdict_exit(bc.compare(300, 250, 200, True)), 1)

    def test_regression_that_still_cumple_is_one(self):
        self.assertEqual(bc.verdict_exit(bc.compare(120, 190, 200, True)), 1)


class TestLoadRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name: str, data) -> Path:
        p = self.dir / name
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    def test_valid_run(self):
        data, err = bc.load_run(self.write("a.json", run()))
        self.assertEqual(err, "")
        self.assertEqual(data["value"], 100.0)

    def test_value_must_be_numeric(self):
        _, err = bc.load_run(self.write("a.json", {"metric": "p95", "value": "100"}))
        self.assertIn("no es un numero", err)

    def test_missing_value(self):
        _, err = bc.load_run(self.write("a.json", {"metric": "p95"}))
        self.assertIn("value", err)

    def test_missing_metric(self):
        _, err = bc.load_run(self.write("a.json", {"value": 1}))
        self.assertIn("metric", err)

    def test_boolean_is_not_a_number(self):
        _, err = bc.load_run(self.write("a.json", {"metric": "p95", "value": True}))
        self.assertIn("no es un numero", err)

    def test_bad_json(self):
        p = self.dir / "bad.json"
        p.write_text("{no", encoding="utf-8")
        _, err = bc.load_run(p)
        self.assertIn("invalido", err)


class TestSameMetric(unittest.TestCase):
    def test_same_metric_and_unit(self):
        ok, _ = bc.same_metric(run(), run())
        self.assertTrue(ok)

    def test_different_metric_refuses(self):
        ok, why = bc.same_metric(run(metric="p95"), run(metric="p99"))
        self.assertFalse(ok)
        self.assertIn("metricas distintas", why)

    def test_different_unit_refuses(self):
        ok, why = bc.same_metric(run(unit="ms"), run(unit="s"))
        self.assertFalse(ok)
        self.assertIn("unidades distintas", why)

    def test_missing_unit_is_tolerated(self):
        ok, _ = bc.same_metric(run(unit="ms"), run(unit=None))
        self.assertTrue(ok)


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.out = self.dir / "bench"

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name: str, data) -> Path:
        p = self.dir / name
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "bench_compare.py"), *args],
            capture_output=True, text=True,
        )

    def base_args(self, before=300, after=180, threshold=200):
        return [
            "--baseline", str(self.write("b.json", run(value=before))),
            "--candidate", str(self.write("c.json", run(value=after))),
            "--threshold", str(threshold),
            "--lower-is-better",
            "--out", str(self.out),
        ]

    def test_improvement_exits_zero(self):
        proc = self.run_cli(*self.base_args())
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_no_improvement_enough_exits_one(self):
        proc = self.run_cli(*self.base_args(after=250))
        self.assertEqual(proc.returncode, 1, proc.stdout)

    def test_regression_under_threshold_exits_one(self):
        proc = self.run_cli(*self.base_args(before=120, after=190))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("cumple-con-regresion", proc.stdout)

    def test_writes_report(self):
        self.run_cli(*self.base_args())
        report = self.out / "report.md"
        self.assertTrue(report.exists())
        text = report.read_text(encoding="utf-8")
        self.assertIn("Antes: 300", text)
        self.assertIn("Veredicto", text)

    def test_low_run_count_warns(self):
        args = self.base_args()
        args[1] = str(self.write("b.json", run(value=300, runs=1)))
        args[3] = str(self.write("c.json", run(value=180, runs=1)))
        proc = self.run_cli(*args)
        self.assertIn("ruido", proc.stdout)

    def test_missing_file_exits_two(self):
        proc = self.run_cli("--baseline", "/tmp/no.json", "--candidate", "/tmp/no2.json",
                            "--threshold", "200")
        self.assertEqual(proc.returncode, 2)

    def test_different_metric_exits_two(self):
        b = self.write("b.json", run(metric="p95"))
        c = self.write("c.json", run(metric="p99"))
        proc = self.run_cli("--baseline", str(b), "--candidate", str(c), "--threshold", "200")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("metricas distintas", proc.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
