#!/usr/bin/env python3
"""
test_metrics_scan.py - Tests de metrics_scan.py (U4 de code-metrics).

    python3 agents/kanam-dev/bin/test_metrics_scan.py

El parseo y el armado de la fila se prueban con salidas REALES de c8, coverage.py y
vitest, copiadas tal cual. La deteccion de stack se prueba con repos temporales.
La ejecucion real se prueba donde hay herramienta; si no hay, se declara.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import metrics_scan  # noqa: E402

# Salidas reales, con las columnas y el espaciado que emiten.
C8 = """-------------------|---------|----------|---------|---------|-------------------
File               | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
-------------------|---------|----------|---------|---------|-------------------
All files          |   85.71 |    66.66 |     100 |   85.71 |
 src               |   85.71 |    66.66 |     100 |   85.71 |
  app.js           |   85.71 |    66.66 |     100 |   85.71 | 12-14
-------------------|---------|----------|---------|---------|-------------------
"""

COVERAGE_PY = """Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
app.py                  20      3    85%   12-14
test_app.py              5      0   100%
--------------------------------------------------
TOTAL                   25      3    88%
"""

VITEST = """ % Coverage report from v8
-------------------|---------|----------|---------|---------|-------------------
File               | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
-------------------|---------|----------|---------|---------|-------------------
All files          |   85.71 |    66.66 |     100 |   85.71 |
-------------------|---------|----------|---------|---------|-------------------
"""


class TestParseCoverage(unittest.TestCase):
    def test_parses_c8_all_files(self):
        value, why = metrics_scan.parse_coverage_total(C8)
        self.assertEqual(value, 85.71)
        self.assertEqual(why, "")

    def test_parses_coverage_py_total(self):
        value, why = metrics_scan.parse_coverage_total(COVERAGE_PY)
        self.assertEqual(value, 88.0)
        self.assertEqual(why, "")

    def test_parses_vitest_all_files(self):
        value, _ = metrics_scan.parse_coverage_total(VITEST)
        self.assertEqual(value, 85.71)

    def test_strips_ansi_before_parsing(self):
        ansi = "\x1b[32mAll files\x1b[0m          |   \x1b[1m72.50\x1b[0m |   50 |"
        value, _ = metrics_scan.parse_coverage_total(ansi)
        self.assertEqual(value, 72.5)

    def test_returns_none_when_no_percentage(self):
        value, why = metrics_scan.parse_coverage_total("3 tests failed, no report")
        self.assertIsNone(value)
        self.assertIn("no trae", why)


class TestBuildRow(unittest.TestCase):
    def test_above_threshold_cumple(self):
        row = metrics_scan.build_row("node", "vitest", 90.0, {"threshold": 80})
        self.assertEqual(row.status, "cumple")

    def test_below_threshold_viola(self):
        row = metrics_scan.build_row("node", "vitest", 65.0, {"threshold": 80})
        self.assertEqual(row.status, "viola")

    def test_none_value_is_sin_medir_never_cumple(self):
        row = metrics_scan.build_row("node", "vitest", None, {"threshold": 80, "reason": "x"})
        self.assertEqual(row.status, "sin-medir")

    def test_threshold_lower_than_value(self):
        row = metrics_scan.build_row("python", "coverage", 80.0, {"threshold": 80})
        self.assertEqual(row.status, "cumple")


class TestDetectStack(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_vitest_project_with_coverage_package(self):
        (self.repo / "package.json").write_text(
            '{"devDependencies": {"vitest": "^2.0.0", "@vitest/coverage-v8": "^2.0.0"}}',
            encoding="utf-8")
        self.assertEqual(metrics_scan.detect_stack(self.repo), ("node", "vitest"))

    def test_c8_project(self):
        (self.repo / "package.json").write_text(
            '{"devDependencies": {"c8": "^9.0.0"}}', encoding="utf-8")
        self.assertEqual(metrics_scan.detect_stack(self.repo), ("node", "c8"))

    def test_node_without_coverage_tool(self):
        (self.repo / "package.json").write_text('{"devDependencies": {}}', encoding="utf-8")
        self.assertEqual(metrics_scan.detect_stack(self.repo), ("node", None))

    def test_unknown_stack(self):
        self.assertEqual(metrics_scan.detect_stack(self.repo), ("desconocido", None))


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "metrics_scan.py"), *args],
            capture_output=True, text=True,
        )

    def test_unknown_stack_is_exit_two(self):
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("desconocido", proc.stderr)

    def test_node_without_tool_is_exit_two_not_zero(self):
        (self.repo / "package.json").write_text('{"devDependencies": {}}', encoding="utf-8")
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("sin herramienta", proc.stderr)

    def test_dry_run_reports_tool_without_running(self):
        (self.repo / "package.json").write_text(
            '{"devDependencies": {"vitest": "^2", "@vitest/coverage-v8": "^2"}}',
            encoding="utf-8")
        proc = self.run_cli(str(self.repo), "--dry-run")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("vitest", proc.stdout)

    def test_missing_dir_is_exit_two(self):
        proc = self.run_cli("/ruta/que/no/existe")
        self.assertEqual(proc.returncode, 2)




class TestMissingCoverageDependency(unittest.TestCase):
    """Verificado en preflight: vitest existe y el paquete de cobertura no."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_vitest_without_coverage_package_is_not_detected_as_a_tool(self):
        (self.repo / "package.json").write_text(
            '{"devDependencies": {"vitest": "^2.0.0"}}', encoding="utf-8")
        stack, tool = metrics_scan.detect_stack(self.repo)
        self.assertEqual(stack, "node")
        self.assertIsNone(tool, "vitest sin @vitest/coverage-v8 no puede medir cobertura")

    def test_vitest_with_coverage_package_is_detected(self):
        (self.repo / "package.json").write_text(
            '{"devDependencies": {"vitest": "^2.0.0", "@vitest/coverage-v8": "^2.0.0"}}',
            encoding="utf-8")
        self.assertEqual(metrics_scan.detect_stack(self.repo), ("node", "vitest"))

    def test_missing_dependency_is_exit_two_with_the_package_named(self):
        (self.repo / "package.json").write_text(
            '{"devDependencies": {"vitest": "^2.0.0"}}', encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(HERE / "metrics_scan.py"), str(self.repo)],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("cobertura", proc.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
