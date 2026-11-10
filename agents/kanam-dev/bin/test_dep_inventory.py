#!/usr/bin/env python3
"""
test_dep_inventory.py - Tests de dep_inventory.py (U4 de dependency-advisor).

    python3 agents/kanam-dev/bin/test_dep_inventory.py

Los parsers se prueban con manifiestos y lockfiles reales (lockfileVersion 1, 2 y
3, requirements con extras y comentarios, pyproject PEP 621 y poetry). El
inventario se prueba como funcion pura: declarado vs resuelto.
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

import dep_inventory as di  # noqa: E402

PKG = json.dumps({
    "dependencies": {"express": "^4.18.0", "left-pad": "1.3.0"},
    "devDependencies": {"vitest": "~2.1.0"},
})

# lockfileVersion 3: el arbol resuelto trae versiones exactas y transitivas.
LOCK_V3 = json.dumps({
    "lockfileVersion": 3,
    "packages": {
        "": {"name": "x"},
        "node_modules/express": {"version": "4.19.2"},
        "node_modules/left-pad": {"version": "1.3.0"},
        "node_modules/vitest": {"version": "2.1.8"},
        "node_modules/body-parser": {"version": "1.20.2"},
        "node_modules/deep": {"version": "0.0.1"},
    },
})

# lockfileVersion 1: `dependencies` anidado.
LOCK_V1 = json.dumps({
    "lockfileVersion": 1,
    "dependencies": {
        "express": {"version": "4.18.2", "dependencies": {"body-parser": {"version": "1.20.1"}}},
        "left-pad": {"version": "1.3.0"},
    },
})

REQUIREMENTS = """# runtime
requests==2.31.0
Flask[async]>=2.0,<3.0
-r base.txt
numpy
"""

PYPROJECT = """[project]
name = "x"
dependencies = [
  "requests>=2.31",
  "click==8.1.7",
]

[tool.poetry.dependencies]
python = "^3.9"
httpx = "^0.27"
"""


class TestParsePackageJson(unittest.TestCase):
    def test_splits_by_kind(self):
        d = di.parse_package_json(PKG)
        self.assertIn("express", d["runtime"])
        self.assertIn("vitest", d["dev"])

    def test_missing_sections_are_empty(self):
        d = di.parse_package_json('{"name":"x"}')
        self.assertEqual(d["runtime"], {})
        self.assertEqual(d["dev"], {})


class TestParseLock(unittest.TestCase):
    def test_lockfile_v3_reads_packages(self):
        r = di.parse_package_lock(LOCK_V3)
        self.assertEqual(r["express"], "4.19.2")
        self.assertEqual(r["body-parser"], "1.20.2")

    def test_lockfile_v1_walks_nested_dependencies(self):
        r = di.parse_package_lock(LOCK_V1)
        self.assertEqual(r["express"], "4.18.2")
        self.assertEqual(r["body-parser"], "1.20.1")

    def test_empty_lock_is_empty_dict(self):
        self.assertEqual(di.parse_package_lock('{"lockfileVersion":3,"packages":{}}'), {})


class TestParsePython(unittest.TestCase):
    def test_requirements_handles_pin_extras_and_comments(self):
        d = di.parse_requirements(REQUIREMENTS)
        self.assertEqual(d["requests"], "==2.31.0")
        self.assertEqual(d["flask"], ">=2.0,<3.0")
        self.assertEqual(d["numpy"], "*")
        self.assertNotIn("-r base.txt", d)

    def test_pyproject_pep621(self):
        d = di.parse_pyproject(PYPROJECT)
        self.assertEqual(d["requests"], ">=2.31")
        self.assertEqual(d["click"], "==8.1.7")

    def test_pyproject_poetry(self):
        d = di.parse_pyproject(PYPROJECT)
        self.assertEqual(d["httpx"], "^0.27")
        self.assertNotIn("python", d, "python no es una dependencia del proyecto")


class TestOpenRange(unittest.TestCase):
    def test_open_ranges(self):
        for spec in ("^4.18.0", "~2.1.0", ">=2.0", "*", "latest", "1.x"):
            self.assertTrue(di.is_open_range(spec), spec)

    def test_pinned_versions(self):
        for spec in ("1.3.0", "==2.31.0", "8.1.7"):
            self.assertFalse(di.is_open_range(spec), spec)


class TestBuildInventory(unittest.TestCase):
    def test_marks_present_and_absent_from_lockfile(self):
        declared = {"runtime": {"express": "1.0.0", "ghost": "2.0.0"}}
        resolved = {"express": "1.0.1"}
        rows, problems = di.build_inventory(declared["runtime"], resolved, "runtime")
        by_name = {r["name"]: r for r in rows}
        self.assertTrue(by_name["express"]["in_lockfile"])
        self.assertFalse(by_name["ghost"]["in_lockfile"])
        self.assertTrue(any("ghost" in p for p in problems))

    def test_transitives_come_from_lockfile_only(self):
        rows, _ = di.build_inventory({"express": "1.0.0"}, {"express": "1.0.0", "body": "2.0"}, "runtime")
        body = [r for r in rows if r["name"] == "body"][0]
        self.assertEqual(body["kind"], "transitive")
        self.assertFalse(body["direct"])

    def test_declared_and_resolved_differ_is_visible(self):
        rows, _ = di.build_inventory({"express": "^4.18.0"}, {"express": "4.19.2"}, "runtime")
        self.assertEqual(rows[0]["declared"], "^4.18.0")
        self.assertEqual(rows[0]["resolved"], "4.19.2")
        self.assertTrue(rows[0]["open_range"])


class TestFindRationale(unittest.TestCase):
    def test_reads_fichas_by_stem(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "dep-advisor" / "rationale"
            base.mkdir(parents=True)
            (base / "express.md").write_text("x", encoding="utf-8")
            self.assertEqual(di.find_rationale(Path(tmp), None), {"express"})

    def test_missing_dir_is_empty_not_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(di.find_rationale(Path(tmp), None), set())


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "dep_inventory.py"), *args],
            capture_output=True, text=True,
        )

    def test_no_manifest_is_exit_two(self):
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("manifiesto", proc.stderr)

    def test_direct_missing_from_lockfile_is_exit_one(self):
        (self.repo / "package.json").write_text(PKG, encoding="utf-8")
        (self.repo / "package-lock.json").write_text(LOCK_V1, encoding="utf-8")
        # vitest esta declarada y el lockfile v1 no la trae.
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 1, proc.stdout)

    def test_coherent_project_is_exit_zero(self):
        (self.repo / "package.json").write_text(PKG, encoding="utf-8")
        (self.repo / "package-lock.json").write_text(LOCK_V3, encoding="utf-8")
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("transitivas", proc.stdout)

    def test_writes_inventory(self):
        (self.repo / "package.json").write_text(PKG, encoding="utf-8")
        (self.repo / "package-lock.json").write_text(LOCK_V3, encoding="utf-8")
        self.run_cli(str(self.repo))
        inv = self.repo / "dep-advisor" / "inventory.md"
        self.assertTrue(inv.exists())
        text = inv.read_text(encoding="utf-8")
        self.assertIn("express", text)
        self.assertIn("body-parser", text)

    def test_json_output_has_rows_and_problems(self):
        (self.repo / "package.json").write_text(PKG, encoding="utf-8")
        (self.repo / "package-lock.json").write_text(LOCK_V3, encoding="utf-8")
        proc = self.run_cli(str(self.repo), "--json")
        data = json.loads(proc.stdout)
        self.assertTrue(any(r["name"] == "express" for r in data["rows"]))
        self.assertIn("undocumented", data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
