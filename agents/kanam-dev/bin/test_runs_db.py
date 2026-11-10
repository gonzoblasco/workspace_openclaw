#!/usr/bin/env python3
"""
test_runs_db.py - Tests de runs_db.py (v0.3, hito 5.1).

    python3 agents/kanam-dev/bin/test_runs_db.py

Cada test usa una base temporal propia: la real vive en el workspace y no se toca
desde un test. Los casos que importan son los de honestidad: una corrida detenida
NO puede registrarse como completa, y una base vacia no es un verde.
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

import runs_db  # noqa: E402


def make_run(records: list[dict], template: str = "task") -> dict:
    return {
        "context": {"template": template, "dir": "/tmp/repo"},
        "records": records,
        "started": 1700000000.0,
        "intake": "/tmp/intake.json",
    }


class TestOutcome(unittest.TestCase):
    def test_all_green_is_completo(self):
        outcome, stopped = runs_db.outcome_of(
            [{"station": "intake", "status": "ok"},
             {"station": "verify", "status": "ok"}], "task")
        self.assertEqual(outcome, "completo")
        self.assertIsNone(stopped)

    def test_failed_station_stops_the_run(self):
        outcome, stopped = runs_db.outcome_of(
            [{"station": "intake", "status": "ok"},
             {"station": "verify", "status": "failed"},
             {"station": "review", "status": "ok"}], "task")
        self.assertEqual(outcome, "detenido")
        self.assertEqual(stopped, "verify")

    def test_infra_is_distinct_from_detenido(self):
        outcome, stopped = runs_db.outcome_of(
            [{"station": "verify", "status": "infra"}], "audit")
        self.assertEqual(outcome, "infra")
        self.assertEqual(stopped, "verify")

    def test_missing_station_stops_the_run(self):
        outcome, stopped = runs_db.outcome_of(
            [{"station": "handoff", "status": "missing"}], "task")
        self.assertEqual(outcome, "detenido")
        self.assertEqual(stopped, "handoff")

    def test_not_applicable_does_not_stop(self):
        outcome, _ = runs_db.outcome_of(
            [{"station": "slice", "status": "not-applicable"}], "audit")
        self.assertEqual(outcome, "completo")


class TestDb(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "runs.db"
        self.run_path = Path(self.tmp.name) / "run.json"

    def tearDown(self):
        self.tmp.cleanup()

    def write_run(self, records: list[dict], template: str = "task") -> Path:
        self.run_path.write_text(json.dumps(make_run(records, template)), encoding="utf-8")
        return self.run_path

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "runs_db.py"), *args, "--db", str(self.db)],
            capture_output=True, text=True,
        )

    def test_record_and_history(self):
        self.write_run([{"station": "intake", "status": "ok", "exit": 0, "output": "ok"}])
        self.assertEqual(self.run_cli("record", str(self.run_path)).returncode, 0)
        proc = self.run_cli("history")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("task", proc.stdout)

    def test_stopped_run_is_recorded_as_detenido(self):
        self.write_run([{"station": "verify", "status": "failed", "exit": 1, "output": "1 failing"}])
        self.run_cli("record", str(self.run_path))
        proc = self.run_cli("history")
        self.assertIn("detenido@verify", proc.stdout)

    def test_show_lists_stations(self):
        self.write_run([
            {"station": "intake", "status": "ok", "exit": 0, "output": ""},
            {"station": "verify", "status": "failed", "exit": 1, "output": "3 failing tests"},
        ])
        self.run_cli("record", str(self.run_path))
        proc = self.run_cli("show", "1")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("intake", proc.stdout)
        self.assertIn("3 failing tests", proc.stdout)

    def test_show_unknown_id_is_one(self):
        self.assertEqual(self.run_cli("show", "99").returncode, 1)

    def test_history_empty_is_one_not_zero(self):
        proc = self.run_cli("history")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("sin corridas", proc.stdout)

    def test_stats_counts_by_template(self):
        self.write_run([{"station": "intake", "status": "ok"}], "task")
        self.run_cli("record", str(self.run_path))
        self.write_run([{"station": "intake", "status": "ok"}], "audit")
        self.run_cli("record", str(self.run_path))
        proc = self.run_cli("stats")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("task", proc.stdout)
        self.assertIn("audit", proc.stdout)

    def test_stats_empty_is_one(self):
        self.assertEqual(self.run_cli("stats").returncode, 1)

    def test_output_is_truncated(self):
        long_output = "x" * 5000
        self.write_run([{"station": "verify", "status": "failed", "exit": 1, "output": long_output}])
        self.run_cli("record", str(self.run_path))
        import sqlite3
        conn = sqlite3.connect(str(self.db))
        stored = conn.execute("SELECT output FROM stations").fetchone()[0]
        conn.close()
        self.assertEqual(len(stored), runs_db.OUTPUT_CAP)

    def test_record_without_template_is_two(self):
        broken = {"context": {}, "records": []}
        self.run_path.write_text(json.dumps(broken), encoding="utf-8")
        self.assertEqual(self.run_cli("record", str(self.run_path)).returncode, 2)

    def test_record_missing_file_is_two(self):
        self.assertEqual(self.run_cli("record", "/tmp/no-existe-run.json").returncode, 2)

    def test_prune_keeps_the_most_recent(self):
        for i in range(5):
            self.write_run([{"station": "intake", "status": "ok"}])
            self.run_cli("record", str(self.run_path))
        proc = self.run_cli("prune", "--keep", "2")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        import sqlite3
        conn = sqlite3.connect(str(self.db))
        n = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        conn.close()
        self.assertEqual(n, 2)

    def test_prune_when_nothing_to_do_is_zero(self):
        self.write_run([{"station": "intake", "status": "ok"}])
        self.run_cli("record", str(self.run_path))
        self.assertEqual(self.run_cli("prune", "--keep", "10").returncode, 0)

    def test_history_filters_by_template(self):
        self.write_run([{"station": "intake", "status": "ok"}], "task")
        self.run_cli("record", str(self.run_path))
        self.write_run([{"station": "intake", "status": "ok"}], "audit")
        self.run_cli("record", str(self.run_path))
        proc = self.run_cli("history", "--template", "audit")
        self.assertIn("audit", proc.stdout)
        self.assertNotIn(" task ", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
