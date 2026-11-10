#!/usr/bin/env python3
"""
test_handoff_gate.py - Tests de S7 (handoff_gate.py).

    python3 agents/kanam-dev/bin/test_handoff_gate.py

El gate existe para rechazar handoffs que suenan completos. Cada test de rechazo
es el caso que alguien va a intentar: "lo di por hecho", "lo omito y no lo digo",
"declaro verde un comando que fallo".
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

import handoff_gate  # noqa: E402


def valid_handoff() -> dict:
    return {
        "summary": "Se agrego la estacion S7 y sus tests",
        "status": "completo",
        "artifact": "agents/kanam-dev/bin/handoff_gate.py",
        "verified": [
            {"command": "python3 bin/test_handoff_gate.py", "exit": 0, "output": "25 tests OK"}
        ],
        "inferred": [],
        "openDecisions": [],
        "skipped": [],
    }


class TestValid(unittest.TestCase):
    def test_complete_handoff_is_valid(self):
        self.assertEqual(handoff_gate.validate(valid_handoff()), [])

    def test_partial_with_decisions_is_valid(self):
        data = valid_handoff()
        data["status"] = "parcial"
        data["openDecisions"] = ["si el limite de hotfix es 3 archivos"]
        self.assertEqual(handoff_gate.validate(data), [])

    def test_skipped_with_reason_is_valid(self):
        data = valid_handoff()
        data["skipped"] = [{"station": "review", "reason": "hotfix de una linea"}]
        self.assertEqual(handoff_gate.validate(data), [])


class TestMissingFields(unittest.TestCase):
    def test_each_required_field_is_reported(self):
        for field in handoff_gate.REQUIRED:
            data = valid_handoff()
            del data[field]
            problems = handoff_gate.validate(data)
            self.assertTrue(any(field in p for p in problems), f"no reporto falta de {field}")

    def test_empty_summary_is_invalid(self):
        data = valid_handoff()
        data["summary"] = "   "
        self.assertTrue(any("summary" in p for p in handoff_gate.validate(data)))

    def test_empty_artifact_is_invalid(self):
        data = valid_handoff()
        data["artifact"] = ""
        self.assertTrue(any("artifact" in p for p in handoff_gate.validate(data)))

    def test_invalid_status_is_rejected(self):
        data = valid_handoff()
        data["status"] = "listo"
        self.assertTrue(any("status" in p for p in handoff_gate.validate(data)))


class TestVerified(unittest.TestCase):
    def test_empty_verified_is_invalid(self):
        data = valid_handoff()
        data["verified"] = []
        problems = handoff_gate.validate(data)
        self.assertTrue(any("verificado" in p or "verified" in p for p in problems))

    def test_claim_without_output_is_invalid(self):
        data = valid_handoff()
        data["verified"] = [{"command": "npm test", "exit": 0}]
        problems = handoff_gate.validate(data)
        self.assertTrue(any("salida" in p for p in problems))

    def test_claim_with_blank_output_is_invalid(self):
        data = valid_handoff()
        data["verified"] = [{"command": "npm test", "exit": 0, "output": "  "}]
        self.assertTrue(handoff_gate.validate(data))

    def test_failing_command_cannot_count_as_verified(self):
        data = valid_handoff()
        data["verified"] = [{"command": "npm test", "exit": 1, "output": "3 failing"}]
        problems = handoff_gate.validate(data)
        self.assertTrue(any("no verifica" in p for p in problems))

    def test_non_integer_exit_is_rejected(self):
        data = valid_handoff()
        data["verified"] = [{"command": "x", "exit": "0", "output": "ok"}]
        self.assertTrue(handoff_gate.validate(data))


class TestSkipped(unittest.TestCase):
    def test_skipped_without_reason_is_invalid(self):
        data = valid_handoff()
        data["skipped"] = [{"station": "review"}]
        problems = handoff_gate.validate(data)
        self.assertTrue(any("motivo" in p for p in problems))

    def test_skipped_with_blank_reason_is_invalid(self):
        data = valid_handoff()
        data["skipped"] = [{"station": "review", "reason": " "}]
        self.assertTrue(handoff_gate.validate(data))

    def test_unknown_station_is_rejected(self):
        data = valid_handoff()
        data["skipped"] = [{"station": "loquesea", "reason": "x"}]
        self.assertTrue(any("desconocida" in p for p in handoff_gate.validate(data)))


class TestContradictions(unittest.TestCase):
    def test_complete_with_open_decisions_is_rejected(self):
        data = valid_handoff()
        data["status"] = "completo"
        data["openDecisions"] = ["falta decidir el limite"]
        problems = handoff_gate.validate(data)
        self.assertTrue(any("completo" in p for p in problems))

    def test_blank_inferred_entry_is_rejected(self):
        data = valid_handoff()
        data["inferred"] = ["  "]
        self.assertTrue(handoff_gate.validate(data))


class TestCli(unittest.TestCase):
    def write(self, data: dict) -> Path:
        tmp = Path(tempfile.mkdtemp()) / "handoff.json"
        tmp.write_text(json.dumps(data), encoding="utf-8")
        return tmp

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "handoff_gate.py"), *args],
            capture_output=True, text=True,
        )

    def test_valid_file_exits_zero(self):
        proc = self.run_cli(str(self.write(valid_handoff())))
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_invalid_file_exits_one(self):
        data = valid_handoff()
        data["verified"] = []
        proc = self.run_cli(str(self.write(data)))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("INVALIDO", proc.stdout)

    def test_missing_file_exits_two(self):
        proc = self.run_cli("/tmp/no-existe-handoff.json")
        self.assertEqual(proc.returncode, 2)

    def test_invalid_json_exits_two(self):
        tmp = Path(tempfile.mkdtemp()) / "bad.json"
        tmp.write_text("{no es json", encoding="utf-8")
        proc = self.run_cli(str(tmp))
        self.assertEqual(proc.returncode, 2)

    def test_template_is_itself_valid(self):
        proc = self.run_cli("--template")
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(handoff_gate.validate(data), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
