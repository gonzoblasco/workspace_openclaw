#!/usr/bin/env python3
"""
test_compat_matrix.py - Tests de compat_matrix.py (U4 de compatibility-testing).

    python3 agents/kanam-dev/bin/test_compat_matrix.py

El parser de tablas y el cruce se prueban puros. El CLI se prueba sobre repos
temporales con matriz y resultados reales en disco.

El caso que mas importa: una combinacion declarada SIN resultado no puede salir
verde. Es el defecto que la skill existe para atrapar.
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

import compat_matrix as cm  # noqa: E402

MATRIX = """# Matriz

| entorno | motor | version | soporte | prioridad |
|---|---|---|---|---|
| chrome-desktop | Chromium | 131 | soportada | alta |
| safari-desktop | WebKit | 18 | degradada | media |
| ie11 | Trident | 11 | fuera de alcance | baja |
"""


class TestParseMdTable(unittest.TestCase):
    def test_reads_rows_by_header(self):
        rows = cm.parse_md_table(MATRIX)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["entorno"], "chrome-desktop")

    def test_tolerates_column_order(self):
        swapped = """| prioridad | entorno | motor |
|---|---|---|
| alta | chrome | Chromium |
"""
        rows = cm.parse_md_table(swapped)
        self.assertEqual(cm.column(rows[0], "entorno"), "chrome")

    def test_skips_separator_and_short_rows(self):
        text = """| entorno | motor |
|---|---|
| ok | Chromium |
| incompleta |
"""
        rows = cm.parse_md_table(text)
        self.assertEqual(len(rows), 1)

    def test_no_table_is_empty(self):
        self.assertEqual(cm.parse_md_table("sin tabla"), [])


class TestParseMatrix(unittest.TestCase):
    def test_builds_combinations(self):
        combos = cm.parse_matrix(MATRIX)
        self.assertEqual(combos[0].environment, "chrome-desktop")
        self.assertEqual(combos[0].engine, "Chromium")
        self.assertEqual(combos[0].priority, "alta")

    def test_out_of_scope_is_lowercased(self):
        combos = cm.parse_matrix(MATRIX)
        self.assertIn("fuera de alcance", combos[2].support)

    def test_row_without_environment_is_dropped(self):
        text = """| entorno | motor |
|---|---|
|  | Chromium |
"""
        self.assertEqual(cm.parse_matrix(text), [])


class TestParseResult(unittest.TestCase):
    def test_normalizes_english_keys(self):
        r = cm.parse_result(Path("a.json"), {"environment": "chrome", "engine": "Chromium",
                                            "engine_version": "131", "date": "2026-11-09",
                                            "status": "pass"})
        self.assertEqual(r.environment, "chrome")
        self.assertEqual(r.date, "2026-11-09")

    def test_normalizes_spanish_keys(self):
        r = cm.parse_result(Path("a.json"), {"entorno": "safari", "motor": "WebKit",
                                             "fecha": "2026-11-09", "estado": "pass"})
        self.assertEqual(r.engine, "WebKit")

    def test_result_without_environment_is_none(self):
        self.assertIsNone(cm.parse_result(Path("a.json"), {"status": "pass"}))

    def test_result_that_is_not_a_dict_is_none(self):
        self.assertIsNone(cm.parse_result(Path("a.json"), ["nope"]))


class TestCross(unittest.TestCase):
    def setUp(self):
        self.combos = cm.parse_matrix(MATRIX)

    def test_declared_without_result_is_a_gap(self):
        rows, gaps, warnings = cm.cross(self.combos, [])
        # Tres combinaciones sin resultado, pero solo dos son huecos: la que esta
        # fuera de alcance produce advertencia, no hueco. Ese es el contrato.
        self.assertEqual(len(gaps), 2)
        self.assertEqual(len(warnings), 1)
        # La fila fuera de alcance tiene su propio estado, no "sin-evidencia":
        # no es un hueco, es una decision ya tomada.
        states = {r["environment"]: r["state"] for r in rows}
        self.assertEqual(states["chrome-desktop"], "sin-evidencia")
        self.assertEqual(states["ie11"], "fuera-de-alcance")

    def test_out_of_scope_without_result_is_a_warning_not_a_gap(self):
        _, gaps, warnings = cm.cross(self.combos, [])
        self.assertFalse(any("ie11" in g for g in gaps))
        self.assertTrue(any("ie11" in w for w in warnings))

    def test_result_without_date_is_a_gap(self):
        results = [cm.Result("chrome-desktop", "Chromium", "131", "", "pass", "c.json")]
        _, gaps, _ = cm.cross(self.combos, results)
        self.assertTrue(any("sin fecha" in g for g in gaps))

    def test_result_for_unknown_environment_is_a_gap(self):
        results = [cm.Result("firefox", "Gecko", "120", "2026-11-09", "pass", "f.json")]
        _, gaps, _ = cm.cross(self.combos, results)
        self.assertTrue(any("no esta en la matriz" in g for g in gaps))

    def test_complete_evidence_has_no_gaps(self):
        results = [
            cm.Result("chrome-desktop", "Chromium", "131", "2026-11-09", "pass", "c.json"),
            cm.Result("safari-desktop", "WebKit", "18", "2026-11-09", "pass", "s.json"),
        ]
        rows, gaps, _ = cm.cross(self.combos, results)
        self.assertEqual(gaps, [])
        self.assertEqual([r["state"] for r in rows][:2], ["pass", "pass"])

    def test_blocking_rows_exclude_out_of_scope(self):
        rows, _, _ = cm.cross(self.combos, [])
        blocking = cm.blocking_rows(rows)
        self.assertFalse(any(r["environment"] == "ie11" for r in blocking))


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.compat = self.repo / "compat"
        (self.compat / "results").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write_matrix(self):
        (self.compat / "matrix.md").write_text(MATRIX, encoding="utf-8")

    def write_result(self, name: str, data: dict):
        (self.compat / "results" / name).write_text(json.dumps(data), encoding="utf-8")

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "compat_matrix.py"), *args],
            capture_output=True, text=True,
        )

    def test_no_matrix_is_exit_two(self):
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("matriz", proc.stderr)

    def test_matrix_without_results_is_exit_one(self):
        self.write_matrix()
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("HUECO", proc.stdout)

    def test_full_evidence_is_exit_zero(self):
        self.write_matrix()
        self.write_result("c.json", {"environment": "chrome-desktop", "engine": "Chromium",
                                     "engine_version": "131", "date": "2026-11-09", "status": "pass"})
        self.write_result("s.json", {"environment": "safari-desktop", "engine": "WebKit",
                                     "engine_version": "18", "date": "2026-11-09", "status": "pass"})
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_out_of_scope_missing_does_not_block_by_default(self):
        self.write_matrix()
        self.write_result("c.json", {"environment": "chrome-desktop", "date": "2026-11-09", "status": "pass"})
        self.write_result("s.json", {"environment": "safari-desktop", "date": "2026-11-09", "status": "pass"})
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("AVISO", proc.stdout)

    def test_strict_makes_out_of_scope_block(self):
        self.write_matrix()
        self.write_result("c.json", {"environment": "chrome-desktop", "date": "2026-11-09", "status": "pass"})
        self.write_result("s.json", {"environment": "safari-desktop", "date": "2026-11-09", "status": "pass"})
        proc = self.run_cli(str(self.repo), "--strict")
        self.assertEqual(proc.returncode, 1, proc.stdout)

    def test_writes_coverage_file(self):
        self.write_matrix()
        self.run_cli(str(self.repo))
        self.assertTrue((self.compat / "coverage.md").exists())

    def test_malformed_result_json_is_exit_two(self):
        self.write_matrix()
        (self.compat / "results" / "bad.json").write_text("{no json", encoding="utf-8")
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
