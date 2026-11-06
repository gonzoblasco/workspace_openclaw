#!/usr/bin/env python3
"""
test_docs_sync.py - Tests de F1 (docs_sync.py).

    python3 agents/kanam-dev/bin/test_docs_sync.py

Los extractores y comparadores se prueban con repos temporales reales: el script
compara contra el disco y contra la suite, y mockear los dos probaria el mock.
Los casos que importan son los que fallan por la razon correcta: un doc que dice
un numero falso DEBE generar drift.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import docs_sync  # noqa: E402


class TestExtractTestClaims(unittest.TestCase):
    def test_historical_reference_is_not_a_suite_claim(self):
        """BRIEF cuenta los tests de OTRO producto ("llego con 102 tests")."""
        line = "`a11y-fixer` llego feature-complete con 102 tests verdes y 0 usuarios."
        claims = docs_sync.extract_test_claims(Path("BRIEF.md"), line)
        self.assertEqual(claims, [])

    def test_stage_level_count_is_not_a_suite_claim(self):
        """STATUS cuenta por etapa ("7 tests") despues de un commit."""
        line = "| S2 - La asercion | **Completado** | Commit `fb931ea`. 7 tests. Verificado. |"
        claims = docs_sync.extract_test_claims(Path("STATUS.md"), line)
        self.assertEqual(claims, [])

    def test_delta_comment_is_not_a_suite_claim(self):
        """"quedo 5 tests atras" es un delta, no un total."""
        line = "El STATUS quedó 5 tests atrás: se agregaron tests después."
        claims = docs_sync.extract_test_claims(Path("AUDIT.md"), line)
        self.assertEqual(claims, [])

    def test_extracts_number_before_noun(self):
        claims = docs_sync.extract_test_claims(Path("STATUS.md"), "Corrimos 168 tests, todos verde")
        self.assertEqual([c.declared for c in claims], ["168"])

    def test_extracts_number_after_noun(self):
        claims = docs_sync.extract_test_claims(Path("X.md"), "tests: 42")
        self.assertEqual([c.declared for c in claims], ["42"])

    def test_ignores_lines_about_a_single_test_file(self):
        claims = docs_sync.extract_test_claims(Path("X.md"), "test/foo.test.js tiene 8 tests")
        self.assertEqual(claims, [])

    def test_records_line_number(self):
        text = "linea uno\nlinea dos con 12 tests\n"
        claims = docs_sync.extract_test_claims(Path("X.md"), text)
        self.assertEqual(claims[0].line, 2)


class TestExtractTokens(unittest.TestCase):
    def test_extracts_css_variable_and_value(self):
        claims = docs_sync.extract_token_claims(Path("DESIGN.md"), "`--line: #2a303a` como borde")
        self.assertEqual(claims[0].declared, "--line=#2a303a")

    def test_ignores_tokens_without_hex(self):
        claims = docs_sync.extract_token_claims(Path("D.md"), "--line: var(--x)")
        self.assertEqual(claims, [])


class TestExtractCommandsAndPaths(unittest.TestCase):
    def test_extracts_npm_run_command(self):
        claims = docs_sync.extract_command_claims(Path("README.md"), "Corre `npm run build` antes.")
        self.assertEqual(claims[0].declared, "npm run build")

    def test_extracts_repo_relative_path(self):
        claims = docs_sync.extract_path_claims(Path("README.md"), "El motor vive en `src/core/logic.js`.")
        self.assertEqual(claims[0].declared, "src/core/logic.js")

    def test_does_not_claim_absolute_paths(self):
        claims = docs_sync.extract_path_claims(Path("R.md"), "`/tmp/foo` no es del repo")
        self.assertEqual(claims, [])


class TestCompareOnRealRepo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        (self.repo / "src").mkdir()
        (self.repo / "src" / "styles.css").write_text(":root {\n  --line: #2a303a;\n}\n", encoding="utf-8")
        (self.repo / "src" / "app.js").write_text("// x\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_token_mismatch_is_drift(self):
        (self.repo / "DESIGN.md").write_text("--line: #ffffff\n", encoding="utf-8")
        drift, errors = docs_sync.compare(self.repo, [self.repo / "DESIGN.md"])
        self.assertEqual(errors, [])
        self.assertTrue(any(d["kind"] == "token" for d in drift))
        self.assertEqual(drift[0]["actual"], "#2a303a")

    def test_token_match_is_clean(self):
        (self.repo / "DESIGN.md").write_text("--line: #2a303a\n", encoding="utf-8")
        drift, errors = docs_sync.compare(self.repo, [self.repo / "DESIGN.md"])
        self.assertEqual(errors, [])
        self.assertEqual(drift, [])

    def test_missing_path_is_drift(self):
        (self.repo / "README.md").write_text("Vive en `src/no-existe.js`.\n", encoding="utf-8")
        drift, _ = docs_sync.compare(self.repo, [self.repo / "README.md"])
        self.assertTrue(any(d["kind"] == "path" for d in drift))

    def test_existing_path_is_clean(self):
        (self.repo / "README.md").write_text("Vive en `src/app.js`.\n", encoding="utf-8")
        drift, _ = docs_sync.compare(self.repo, [self.repo / "README.md"])
        self.assertEqual(drift, [])

    def test_missing_npm_script_is_drift(self):
        (self.repo / "package.json").write_text('{"scripts": {"test": "true"}}\n', encoding="utf-8")
        (self.repo / "README.md").write_text("Corre `npm run deploy`.\n", encoding="utf-8")
        drift, _ = docs_sync.compare(self.repo, [self.repo / "README.md"])
        self.assertTrue(any(d["kind"] == "command" for d in drift))


class TestMeasurementErrors(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_unknown_stack_measuring_tests_is_an_error_not_zero(self):
        (self.repo / "README.md").write_text("Hay 10 tests.\n", encoding="utf-8")
        drift, errors = docs_sync.compare(self.repo, [self.repo / "README.md"])
        self.assertEqual(drift, [])
        self.assertTrue(any("test_count" in e for e in errors))

    def test_missing_css_measuring_tokens_is_an_error(self):
        (self.repo / "DESIGN.md").write_text("--line: #2a303a\n", encoding="utf-8")
        _, errors = docs_sync.compare(self.repo, [self.repo / "DESIGN.md"])
        self.assertTrue(any("token" in e for e in errors))


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "docs_sync.py"), *args],
            capture_output=True, text=True,
        )

    def test_no_docs_is_exit_two(self):
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 2)

    def test_missing_dir_is_exit_two(self):
        proc = self.run_cli("/ruta/que/no/existe")
        self.assertEqual(proc.returncode, 2)

    def test_check_with_drift_exits_one(self):
        (self.repo / "src").mkdir()
        (self.repo / "src" / "app.js").write_text("x\n", encoding="utf-8")
        (self.repo / "README.md").write_text("Vive en `src/falta.js`.\n", encoding="utf-8")
        proc = self.run_cli(str(self.repo), "--check")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("DRIFT", proc.stdout)

    def test_check_clean_exits_zero(self):
        (self.repo / "src").mkdir()
        (self.repo / "src" / "app.js").write_text("x\n", encoding="utf-8")
        (self.repo / "README.md").write_text("Vive en `src/app.js`.\n", encoding="utf-8")
        proc = self.run_cli(str(self.repo), "--check")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)




class TestRegressionsFromRealRun(unittest.TestCase):
    """Casos que la primera corrida real sobre kanam-fixer expuso.

    Los tres son verdes en fixtures y rojos en la realidad: ANSI en la salida de
    vitest, directorios citados como rutas, y citas de otro repo.
    """

    def test_ansi_codes_do_not_hide_the_test_count(self):
        ansi = "\x1b[2mTests  \x1b[22m \x1b[32m22 passed\x1b[39m \x1b[2m|\x1b[22m 4 skipped (26)"
        cleaned = docs_sync.ANSI_RE.sub("", ansi)
        m = __import__("re").search(r"Tests\s+(\d+)\s+passed", cleaned)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "22")

    def test_npm_silent_would_hide_the_count(self):
        """Documenta por que NO se usa --silent: suprime el resumen a leer."""
        self.assertIn("--silent", "npm test --silent")
        # El contrato real: la salida sin --silent trae "Tests N passed".
        sample = " Test Files  4 passed (4)\n      Tests  22 passed | 4 skipped (26)\n"
        m = __import__("re").search(r"Tests\s+(\d+)\s+passed", sample)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "22")

    def test_subset_count_is_not_a_suite_claim(self):
        for line in (
            "**7 tests**, incluidos 3 de mutacion mas uno que verifica todo.",
            "# 8 tests de caracterizacion del driver virtual.",
            "los 51 tests pasaban en verde - pero VoiceOver no anunciaba nada",
        ):
            self.assertEqual(docs_sync.extract_test_claims(Path("X.md"), line), [], line)

    def test_doc_about_other_repo_is_not_a_suite_claim(self):
        line = "El `a11y-fixer` llego con 102 tests verdes y 0 usuarios."
        self.assertEqual(docs_sync.extract_test_claims(Path("BRIEF.md"), line), [])

    def test_directory_path_claim_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs" / "adr").mkdir(parents=True)
            (repo / "README.md").write_text("Vive en `docs/adr/`.\n", encoding="utf-8")
            drift, _ = docs_sync.compare(repo, [repo / "README.md"])
            self.assertEqual(drift, [])

    def test_path_regex_tolerates_trailing_slash_inside_backticks(self):
        claims = docs_sync.extract_path_claims(Path("R.md"), "`docs/adr/` y `src/app.js`")
        self.assertEqual([c.declared for c in claims], ["docs/adr/", "src/app.js"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
