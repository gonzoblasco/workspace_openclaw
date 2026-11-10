#!/usr/bin/env python3
"""
test_kanam_dev.py - Tests del despachador (F0).

Cero dependencias: unittest de stdlib.

    python3 agents/kanam-dev/bin/test_kanam_dev.py

Lo que se prueba aca es el CONTRATO, no la salida de las herramientas
delegadas: que un faltante sea exit 2 y nunca 0, que `help` liste todo
subcomando registrado, y que un subcomando desconocido no devuelva verde.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
DISPATCHER = HERE / "kanam-dev"


class TestDispatch(unittest.TestCase):
    def run_cli(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, str(DISPATCHER), *args],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

    def test_help_exits_zero(self):
        proc = self.run_cli("help")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Exit codes", proc.stdout)

    def test_help_lists_every_registered_subcommand(self):
        proc = self.run_cli("help")
        self.assertEqual(proc.returncode, 0)
        for name in ("intake", "audit", "a11y", "review", "docs", "handoff", "history", "status", "help"):
            self.assertIn(name, proc.stdout)

    def test_no_args_shows_help_and_exits_zero(self):
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0)
        self.assertIn("kanam-dev", proc.stdout)

    def test_unknown_subcommand_is_exit_two_not_zero(self):
        proc = self.run_cli("noexiste")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("desconocido", proc.stdout)

    def test_missing_directory_is_exit_two(self):
        proc = self.run_cli("status", "/ruta/que/no/existe")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("INFRA", proc.stdout)

    def test_audit_on_unknown_stack_is_exit_two(self):
        proc = self.run_cli("audit", "/tmp")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("stack", proc.stdout)

    def test_docs_delegates_to_docs_sync(self):
        # F1 ya existe: el despachador debe delegar y propagar su exit code.
        # Un /tmp sin docs da exit 2 (no se pudo medir), nunca 0.
        proc = self.run_cli("docs", "/tmp")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("INFRA", proc.stdout)

    def test_a11y_without_target_is_exit_two(self):
        proc = self.run_cli("a11y")
        self.assertEqual(proc.returncode, 2)

    def test_review_without_gh_is_exit_two(self):
        proc = self.run_cli("review", "o/r", "1")
        self.assertEqual(proc.returncode, 2)

    def test_intake_delegates_and_propagates_exit_one(self):
        proc = self.run_cli("intake", "--text", "Objetivo: x")
        # --text no es posicional de intake aqui: debe fallar por uso, no por 0.
        self.assertIn(proc.returncode, (1, 2))

    def test_history_is_wired_and_reports(self):
        # El despachador delega en runs_db. No se prueba "base vacia" porque la
        # base real del workspace no esta vacia: ese contrato se prueba en
        # test_runs_db con una base temporal propia.
        proc = self.run_cli("history")
        self.assertIn(proc.returncode, (0, 1))
        self.assertTrue(proc.stdout.strip(), "history no imprimio nada")

    def test_handoff_without_args_is_exit_two(self):
        proc = self.run_cli("handoff")
        self.assertEqual(proc.returncode, 2)

    def test_handoff_validates_its_own_template(self):
        template = self.run_cli("handoff", "--template")
        self.assertEqual(template.returncode, 0, template.stdout + template.stderr)
        out = Path("/tmp/kd-handoff-template.json")
        # Con --template el stdout es JSON puro: el veredicto va a stderr para
        # que el archivo escrito sea parseable sin cirugia.
        json.loads(template.stdout)
        out.write_text(template.stdout, encoding="utf-8")
        proc = self.run_cli("handoff", str(out))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("OK", proc.stdout)

    def test_handoff_invalid_is_exit_one(self):
        bad = Path("/tmp/kd-bad-handoff.json")
        bad.write_text('{"summary": "x", "status": "completo", "artifact": "a"}', encoding="utf-8")
        proc = self.run_cli("handoff", str(bad))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("FALLA", proc.stdout)

    def test_status_on_non_git_dir_is_zero_not_infra(self):
        proc = self.run_cli("status", "/tmp")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("no es un repo git", proc.stdout)


class TestStatusRiskyFiles(unittest.TestCase):
    def test_reports_local_data_files(self):
        # Solo si /tmp/kanam-dev-test-repo se puede crear y usar git.
        repo = Path("/tmp/kanam-dev-test-repo")
        subprocess.run(["rm", "-rf", str(repo)], check=False)
        repo.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=False)
        (repo / ".env").write_text("SECRET=1\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(DISPATCHER), "status", str(repo)],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("RIESGO", proc.stdout)
        self.assertIn(".env", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
