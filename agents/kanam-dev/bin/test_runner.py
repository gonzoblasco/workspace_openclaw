#!/usr/bin/env python3
"""
test_runner.py - Tests del encadenador de estaciones.

    python3 agents/kanam-dev/bin/test_runner.py

Los casos que importan son los de parada: el runner no debe seguir despues de un
hallazgo ni de un "no pude medir", y debe poder retomar sin repetir estaciones.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import runner  # noqa: E402


def complete_intake(template: str = "task", manual=None) -> dict:
    data = {
        "template": template,
        "template_inferred": template,
        "template_reason": "test",
        "fields": {
            "objetivo": "x",
            "artefacto": "src/x.js",
            "verificacion": "npm test",
            "convenciones": "node",
            "aprobacion": "no push",
        },
        "missing": [],
        "limits": {"hotfix_max_files": 3, "hotfix_max_lines": 80},
        "warnings": [],
        "status": "complete",
    }
    if manual:
        data["manual_evidence"] = manual
    return data


class TestPlan(unittest.TestCase):
    def test_every_template_has_all_stations(self):
        for template in runner.TEMPLATE_MATRIX:
            plan = runner.build_plan(template)
            self.assertEqual([s["station"] for s in plan], list(runner.STATION_ORDER))

    def test_audit_skips_slice_and_build(self):
        plan = {s["station"]: s["mode"] for s in runner.build_plan("audit")}
        self.assertEqual(plan["slice"], "not-applicable")
        self.assertEqual(plan["build"], "not-applicable")
        self.assertEqual(plan["verify"], "blocking")

    def test_feature_makes_discovery_blocking(self):
        self.assertIn("discovery", runner.blocking_stations("feature"))
        self.assertNotIn("discovery", runner.blocking_stations("task"))

    def test_unknown_template_raises(self):
        with self.assertRaises(ValueError):
            runner.build_plan("inventada")


class TestStationExecution(unittest.TestCase):
    def test_not_applicable_does_not_run_anything(self):
        rec = runner.run_station("slice", "not-applicable", {"template": "audit", "dir": "."})
        self.assertEqual(rec["status"], "not-applicable")
        self.assertIsNone(rec["exit"])

    def test_blocking_manual_without_evidence_is_missing(self):
        rec = runner.run_station("slice", "blocking", {"template": "task", "dir": ".", "manual_evidence": {}})
        self.assertEqual(rec["status"], "missing")
        self.assertEqual(rec["exit"], 1)

    def test_blocking_manual_with_evidence_is_declared(self):
        ctx = {"template": "task", "dir": ".", "manual_evidence": {"slice": "commit abc123"}}
        rec = runner.run_station("slice", "manual", ctx)
        self.assertEqual(rec["status"], "declared")

    def test_handoff_without_file_is_manual_missing(self):
        rec = runner.run_station("handoff", "blocking", {"template": "task", "dir": "."})
        self.assertEqual(rec["status"], "missing")


class TestResume(unittest.TestCase):
    def test_resume_points_at_first_failure(self):
        run = {
            "records": [
                {"station": "intake", "status": "ok"},
                {"station": "slice", "status": "failed"},
                {"station": "build", "status": "ok"},
            ]
        }
        idx, why = runner.resume_point(run)
        self.assertEqual(idx, 1)
        self.assertIn("failed", why or "")

    def test_resume_after_infra(self):
        run = {"records": [{"station": "intake", "status": "ok"}, {"station": "verify", "status": "infra"}]}
        idx, _ = runner.resume_point(run)
        self.assertEqual(idx, 1)

    def test_finished_run_resumes_at_end(self):
        run = {"records": [{"station": "intake", "status": "ok"}]}
        idx, why = runner.resume_point(run)
        self.assertEqual(idx, 1)
        self.assertIsNone(why)


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def intake_file(self, data: dict) -> Path:
        p = self.root / "intake.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    def run_cli(self, *args):
        # Base de corridas redirigida: un test no escribe en el historial real.
        env = dict(os.environ, KANAM_DEV_RUNS_DB=str(self.root / "runs.db"))
        return subprocess.run(
            [sys.executable, str(HERE / "runner.py"), *args],
            capture_output=True, text=True, env=env,
        )

    def test_dry_run_prints_plan(self):
        proc = self.run_cli("--intake", str(self.intake_file(complete_intake("audit"))), "--dry-run")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("audit", proc.stdout)
        self.assertIn("not-applicable", proc.stdout)

    def test_incomplete_intake_blocks_before_any_station(self):
        data = complete_intake()
        data["status"] = "incomplete"
        data["missing"] = ["artefacto"]
        proc = self.run_cli("--intake", str(self.intake_file(data)), "--dry-run")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("incompleto", proc.stderr)

    def test_missing_intake_file_is_exit_two(self):
        proc = self.run_cli("--intake", str(self.root / "no.json"))
        self.assertEqual(proc.returncode, 2)

    def test_no_args_is_exit_two(self):
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 2)

    def test_stops_at_first_blocking_station_without_evidence(self):
        # audit exige discovery bloqueante; sin evidencia declarada se detiene
        # ahi y no llega a verify. El orden y la parada son lo que se prueba.
        proc = self.run_cli(
            "--intake", str(self.intake_file(complete_intake("audit"))),
            "--dir", str(self.root),
            "--out", str(self.root / "run.json"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("pipeline detenido", proc.stdout)
        run = json.loads((self.root / "run.json").read_text(encoding="utf-8"))
        self.assertEqual([r["station"] for r in run["records"]], ["intake", "discovery"])

    def test_stops_when_verify_cannot_measure(self):
        # audit CON evidencia de discovery llega a verify, que corre
        # `kanam-dev audit` sobre un dir sin stack: exit 2, detiene.
        data = complete_intake("audit", manual={"discovery": "medido en /tmp, ver informe"})
        proc = self.run_cli(
            "--intake", str(self.intake_file(data)),
            "--dir", str(self.root),
            "--out", str(self.root / "run.json"),
        )
        self.assertEqual(proc.returncode, 2, proc.stdout)
        run = json.loads((self.root / "run.json").read_text(encoding="utf-8"))
        stations = [r["station"] for r in run["records"]]
        self.assertEqual(stations[:3], ["intake", "discovery", "slice"])
        self.assertEqual(stations[-1], "verify")
        self.assertEqual(run["records"][-1]["status"], "infra")
        self.assertNotIn("handoff", stations)
        self.assertEqual(run["records"][-1]["status"], "infra")


if __name__ == "__main__":
    unittest.main(verbosity=2)
