import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "agents/kanam-planner/scripts/program_plan.py"
CONTRACT = ROOT / "agents/kanam-planner/scripts/dispatch_contract.py"


class ProgramPlanTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = {**os.environ, "PROGRAM_PLAN_DIR": self.tmp.name}

    def tearDown(self):
        self.tmp.cleanup()

    def run_cmd(self, *args, script=PROGRAM):
        return subprocess.run(
            [sys.executable, str(script), *args],
            capture_output=True,
            text=True,
            env=self.env,
        )

    def init_program(self, slug="demo"):
        result = self.run_cmd(
            "init",
            slug,
            "--title",
            "Demo",
            "--objective",
            "Probar el programa",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_happy_path(self):
        self.init_program()
        result = self.run_cmd(
            "add-step",
            "demo",
            "Implementar",
            "--role",
            "dev",
            "--exit",
            "Test verde",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        lint = self.run_cmd("lint", "demo", "--json")
        self.assertEqual(lint.returncode, 0, lint.stderr)
        self.assertTrue(json.loads(lint.stdout)["ok"])

        brief = self.run_cmd("brief")
        self.assertIn("Demo", brief.stdout)
        self.assertIn("Implementar", brief.stdout)

        status = self.run_cmd("status", "--json")
        payload = json.loads(status.stdout)
        self.assertEqual(payload["programs"][0]["progress"]["total"], 1)

    def test_completed_requires_evidence(self):
        self.init_program()
        self.run_cmd(
            "add-step", "demo", "Implementar", "--role", "dev", "--exit", "Test verde"
        )
        result = self.run_cmd("update", "demo", "1", "completed")
        self.assertEqual(result.returncode, 1)
        self.assertIn("evidence", result.stderr)

        result = self.run_cmd(
            "update", "demo", "1", "completed", "--evidence", "pytest ok"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cycle_detection(self):
        self.init_program()
        self.run_cmd(
            "add-step", "demo", "A", "--role", "dev", "--exit", "A", "--depends", "2"
        )
        self.run_cmd(
            "add-step", "demo", "B", "--role", "dev", "--exit", "B", "--depends", "1"
        )
        result = self.run_cmd("lint", "demo", "--json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Ciclo", result.stdout)

    def test_close_gate(self):
        self.init_program()
        self.run_cmd(
            "add-step", "demo", "Implementar", "--role", "dev", "--exit", "Test verde"
        )
        result = self.run_cmd("close", "demo")
        self.assertEqual(result.returncode, 1)
        self.assertIn("no terminales", result.stderr)

        self.run_cmd(
            "update", "demo", "1", "completed", "--evidence", "pytest ok"
        )
        result = self.run_cmd("close", "demo")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_dispatch_contract(self):
        self.init_program()
        self.run_cmd(
            "add-step", "demo", "Implementar", "--role", "dev", "--exit", "Test verde"
        )
        result = self.run_cmd("demo", "1", "--format", "json", script=CONTRACT)
        self.assertEqual(result.returncode, 0, result.stderr)
        contract = json.loads(result.stdout)
        self.assertEqual(contract["program"], "demo")
        self.assertEqual(contract["agentId"], "kanam-dev")
        self.assertIn("gpt-oss", contract["model"])
        self.assertEqual(contract["exit_criteria"], "Test verde")
        self.assertIn("## Spawn", contract["markdown"])

    def test_gate_edit(self):
        self.init_program()
        self.run_cmd(
            "add-step", "demo", "Implementar", "--role", "dev", "--exit", "Test verde"
        )
        result = self.run_cmd("set-gates", "demo", "critic,auditor")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_cmd("set-gate", "demo", "1", "critic")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((Path(self.tmp.name) / "demo.json").read_text())
        self.assertEqual(data["gates"], ["critic", "auditor"])
        self.assertEqual(data["steps"][0]["gate"], "critic")


if __name__ == "__main__":
    unittest.main()
