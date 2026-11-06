#!/usr/bin/env python3
"""
test_intake.py - Tests de la estacion S1 (intake.py).

Cero dependencias: unittest de stdlib. Se corre con:

    python3 agents/kanam-dev/bin/test_intake.py

Por que existe: la inferencia de plantilla es la pieza del pipeline que mas va a
cambiar y la que mas facil se rompe en silencio (un pedido de docs clasificado
como feature no falla, solo desperdicia estaciones). Cada caso de aca falla por
la razon correcta: si la regla cambia, el test dice cual.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import intake  # noqa: E402

COMPLETE_REQUEST = """
Objetivo: Agregar tabla de posiciones al panel de jugadores.
Artefacto: src/ui/leaderboard.js
Verificacion: npm test -- leaderboard
Convenciones: vanilla JS + Vite, cero deps de runtime
Aprobacion: puedo tocar src/ui y test; no publico ni pusheo
"""


class TestExtractFields(unittest.TestCase):
    def test_extracts_all_five_fields(self):
        fields = intake.extract_fields(COMPLETE_REQUEST)
        self.assertEqual(set(fields), set(intake.REQUIRED_FIELDS))

    def test_does_not_invent_missing_fields(self):
        fields = intake.extract_fields("Objetivo: arreglar algo")
        self.assertEqual(fields, {"objetivo": "arreglar algo"})

    def test_empty_marker_counts_as_missing(self):
        fields = intake.extract_fields("Objetivo:   \nArtefacto: foo.js")
        self.assertNotIn("objetivo", fields)
        self.assertIn("artefacto", fields)

    def test_accepts_english_and_spanish_markers(self):
        fields = intake.extract_fields("Ruta: src/core/logic.js\nStack: node\nLimite: no push")
        self.assertEqual(fields["artefacto"], "src/core/logic.js")
        self.assertEqual(fields["convenciones"], "node")
        self.assertEqual(fields["aprobacion"], "no push")


class TestMissingFields(unittest.TestCase):
    def test_reports_missing_in_contract_order(self):
        fields = intake.extract_fields("Objetivo: x")
        missing = intake.missing_fields(fields)
        self.assertEqual(missing, ["artefacto", "verificacion", "convenciones", "aprobacion"])

    def test_complete_request_has_no_missing(self):
        fields = intake.extract_fields(COMPLETE_REQUEST)
        self.assertEqual(intake.missing_fields(fields), [])


class TestInferTemplate(unittest.TestCase):
    def test_urgent_with_tiny_scope_is_hotfix(self):
        template, reason = intake.infer_template("Urgente: el boton no responde en un archivo puntual")
        self.assertEqual(template, "hotfix")
        self.assertIn("urgencia", reason)

    def test_urgent_without_declared_scope_escalates_to_task(self):
        template, _ = intake.infer_template("Urgente: hay un bug en el tablero")
        self.assertEqual(template, "task")

    def test_docs_request_is_docs(self):
        template, _ = intake.infer_template("Actualizar el README con los comandos nuevos")
        self.assertEqual(template, "docs")

    def test_docs_request_that_builds_code_is_not_docs(self):
        template, _ = intake.infer_template("Escribir la documentacion del nuevo endpoint que hay que implementar")
        self.assertNotEqual(template, "docs")

    def test_measurement_is_audit(self):
        template, _ = intake.infer_template("Medir cuantas partidas fuerzan adivinar")
        self.assertEqual(template, "audit")

    def test_measurement_that_also_builds_is_not_audit(self):
        template, _ = intake.infer_template("Medir el costo y crear un generador nuevo")
        self.assertNotEqual(template, "audit")

    def test_new_thing_is_feature(self):
        template, _ = intake.infer_template("Agregar marca de duda a las celdas")
        self.assertEqual(template, "feature")

    def test_change_is_task(self):
        template, _ = intake.infer_template("Corregir el conteo de banderas")
        self.assertEqual(template, "task")

    def test_ambiguous_defaults_to_task_not_hotfix(self):
        template, reason = intake.infer_template("Habria que ver el estado del tablero")
        self.assertEqual(template, "task")
        self.assertIn("default", reason)


class TestHotfixLimit(unittest.TestCase):
    def test_within_limit_passes(self):
        ok, why = intake.hotfix_limit_ok("archivos: 2 lineas: 40")
        self.assertTrue(ok)
        self.assertEqual(why, "")

    def test_exceeding_files_fails(self):
        ok, why = intake.hotfix_limit_ok("archivos: 5")
        self.assertFalse(ok)
        self.assertIn("5 archivos", why)

    def test_exceeding_lines_fails(self):
        ok, why = intake.hotfix_limit_ok("lineas: 200")
        self.assertFalse(ok)
        self.assertIn("200 lineas", why)

    def test_undeclared_scope_passes(self):
        ok, _ = intake.hotfix_limit_ok("no declare tamano")
        self.assertTrue(ok)


class TestBuildIntake(unittest.TestCase):
    def test_complete_request_is_complete(self):
        data, missing = intake.build_intake(COMPLETE_REQUEST)
        self.assertEqual(missing, [])
        self.assertEqual(data["status"], "complete")
        self.assertEqual(set(data["fields"]), set(intake.REQUIRED_FIELDS))

    def test_incomplete_request_lists_missing(self):
        data, missing = intake.build_intake("Objetivo: algo\nArtefacto: foo.js")
        self.assertEqual(data["status"], "incomplete")
        self.assertIn("verificacion", missing)

    def test_core_override_is_recorded(self):
        data, _ = intake.build_intake(COMPLETE_REQUEST, template_override="docs")
        self.assertEqual(data["template"], "docs")
        self.assertEqual(data["template_inferred"], "feature")
        self.assertTrue(any("override" in w.lower() for w in data["warnings"]))

    def test_oversized_hotfix_escalates_to_task(self):
        text = "Urgente: bug en una funcion puntual\narchivos: 9\n"
        data, _ = intake.build_intake(text, template_override="hotfix")
        self.assertEqual(data["template"], "task")
        self.assertTrue(any("excede" in w for w in data["warnings"]))


class TestCli(unittest.TestCase):
    def run_cli(self, *args, stdin_text=None):
        return subprocess.run(
            [sys.executable, str(HERE / "intake.py"), *args],
            capture_output=True,
            text=True,
            input=stdin_text,
        )

    def test_complete_request_exits_zero(self):
        proc = self.run_cli("--text", COMPLETE_REQUEST, "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "complete")

    def test_incomplete_request_exits_one_and_names_missing(self):
        proc = self.run_cli("--text", "Objetivo: cambiar algo")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("FALTAN CAMPOS", proc.stdout)
        self.assertIn("artefacto", proc.stdout)

    def test_empty_request_exits_two(self):
        proc = self.run_cli("--text", "   ")
        self.assertEqual(proc.returncode, 2)

    def test_writes_out_file(self):
        out = Path("/tmp/intake-test-out.json")
        proc = self.run_cli("--text", COMPLETE_REQUEST, "--out", str(out))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(out.exists())
        self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["status"], "complete")
        out.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
