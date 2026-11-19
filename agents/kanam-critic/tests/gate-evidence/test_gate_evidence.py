import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "bin" / "gate-evidence.py"


def run_gate(tmp_path: Path, spec: dict, extra=None):
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    cmd = [sys.executable, str(SCRIPT), "--spec", str(spec_path)]
    if extra:
        cmd.extend(extra)
    return subprocess.run(cmd, capture_output=True, text=True)


def py(code: str):
    return [sys.executable, "-c", code]


def two_case_spec(tmp_path: Path) -> dict:
    """Un caso PASS y uno FAIL: el veredicto global debe ser FAIL (exit 1)."""
    return {
        "name": "dos casos",
        "repo_root": str(tmp_path),
        "cases": [
            {
                "name": "ok",
                "cmd": py("print('hola')"),
                "expect_exit": 0,
                "expect_stdout_contains": ["hola"],
            },
            {
                "name": "roto",
                "cmd": py("import sys; sys.exit(3)"),
                "expect_exit": 0,
            },
        ],
    }


def test_one_pass_one_fail_is_exit_1_and_reports_both(tmp_path):
    res = run_gate(tmp_path, two_case_spec(tmp_path))
    assert res.returncode == 1, res.stderr
    assert "GATE-EVIDENCE: FAIL" in res.stdout
    assert "1 caso(s) fallido(s): roto" in res.stdout
    # Ambos casos aparecen en la tabla.
    assert "| ok | 0 | 0 |" in res.stdout
    assert "| roto | 0 | 3 |" in res.stdout
    assert "PASS |" in res.stdout and "FAIL |" in res.stdout


def test_all_pass_is_exit_0(tmp_path):
    spec = {
        "name": "todo verde",
        "repo_root": str(tmp_path),
        "cases": [
            {"name": "a", "cmd": py("print('alpha')"), "expect_exit": 0,
             "expect_stdout_contains": ["alpha"]},
            {"name": "b", "cmd": py("print('beta')"), "expect_exit": 0,
             "expect_stdout_contains": ["beta"]},
        ],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 0, res.stderr
    assert "GATE-EVIDENCE: PASS (2 casos, 0 tests)" in res.stdout


def test_missing_expect_exit_is_invalid_spec(tmp_path):
    spec = {
        "name": "sin exit",
        "cases": [{"name": "x", "cmd": py("print('x')")}],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 2
    assert "expect_exit" in res.stderr
    assert "GATE-EVIDENCE: SPEC-INVALIDA" in res.stdout


def test_empty_contains_list_is_invalid_spec(tmp_path):
    spec = {
        "name": "lista vacía",
        "cases": [
            {"name": "x", "cmd": py("print('x')"), "expect_exit": 0,
             "expect_stdout_contains": []},
        ],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 2
    assert "está vacía" in res.stderr


def test_unknown_case_key_is_invalid_spec(tmp_path):
    spec = {
        "name": "typo",
        "cases": [
            {"name": "x", "cmd": py("print('x')"), "expect_exit": 0,
             "expect_stdout_contain": ["x"]},
        ],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 2
    assert "claves desconocidas" in res.stderr


def test_unreadable_spec_is_invalid(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{no es json", encoding="utf-8")
    res = subprocess.run(
        [sys.executable, str(SCRIPT), "--spec", str(bad)],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 2
    assert "JSON válido" in res.stderr


def test_tmp_and_bin_substitution(tmp_path):
    artifact = tmp_path / "bin" / "artifact.py"
    artifact.parent.mkdir()
    artifact.write_text(
        "import sys\nfrom pathlib import Path\n"
        "print(Path(sys.argv[1]).read_text().strip())\n"
        "print('cwd=' + str(Path.cwd()))\n",
        encoding="utf-8",
    )
    spec = {
        "name": "sustituciones",
        "repo_root": str(tmp_path),
        "bin": "bin/artifact.py",
        "cases": [
            {
                "name": "lee tmp y ve root",
                "cmd": [sys.executable, "{BIN}", "{TMP}/data.txt"],
                "files": {"{TMP}/data.txt": "contenido-de-prueba"},
                "expect_exit": 0,
                "expect_stdout_contains": ["contenido-de-prueba", f"cwd={tmp_path}"],
            }
        ],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "GATE-EVIDENCE: PASS (1 casos, 0 tests)" in res.stdout
    # {TMP} no debe quedar literal ni en cmd ni en la evidencia.
    assert "{TMP}" not in res.stdout


def test_stderr_contains_works(tmp_path):
    spec = {
        "name": "stderr",
        "repo_root": str(tmp_path),
        "cases": [
            {
                "name": "escribe stderr",
                "cmd": py("import sys; sys.stderr.write('boom\\n')"),
                "expect_exit": 0,
                "expect_stderr_contains": ["boom"],
            }
        ],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "boom" in res.stdout


def test_stderr_missing_contains_fails(tmp_path):
    spec = {
        "name": "stderr ausente",
        "repo_root": str(tmp_path),
        "cases": [
            {
                "name": "sin boom",
                "cmd": py("print('nada')"),
                "expect_exit": 0,
                "expect_stderr_contains": ["boom"],
            }
        ],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 1
    assert "stderr no contiene 'boom'" in res.stdout


def _write_test_file(tmp_path: Path, body: str) -> None:
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "test_sample.py").write_text(body, encoding="utf-8")


def test_pytest_suite_passing_is_exit_0(tmp_path):
    _write_test_file(tmp_path, "def test_ok():\n    assert True\n")
    spec = {
        "name": "pytest verde",
        "repo_root": str(tmp_path),
        "pytest": ["tests"],
        "cases": [
            {"name": "trivial", "cmd": py("print('ok')"), "expect_exit": 0,
             "expect_stdout_contains": ["ok"]},
        ],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "1 passed" in res.stdout
    assert "GATE-EVIDENCE: PASS (1 casos, 1 tests)" in res.stdout


def test_pytest_suite_failing_is_exit_1(tmp_path):
    _write_test_file(tmp_path, "def test_bad():\n    assert False\n")
    spec = {
        "name": "pytest rojo",
        "repo_root": str(tmp_path),
        "pytest": ["tests"],
        "cases": [
            {"name": "trivial", "cmd": py("print('ok')"), "expect_exit": 0},
        ],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 1, res.stdout + res.stderr
    assert "1 failed" in res.stdout
    assert "GATE-EVIDENCE: FAIL" in res.stdout
    assert "pytest: tests: 1 failed" in res.stdout


def test_pytest_without_tests_fails_instead_of_auto_approving(tmp_path):
    (tmp_path / "tests").mkdir()
    spec = {
        "name": "pytest vacío",
        "repo_root": str(tmp_path),
        "pytest": ["tests"],
        "cases": [
            {"name": "trivial", "cmd": py("print('ok')"), "expect_exit": 0},
        ],
    }
    res = run_gate(tmp_path, spec)
    assert res.returncode == 1
    assert "sin tests colectados" in res.stdout


def test_json_mode_has_same_verdict(tmp_path):
    res = run_gate(tmp_path, two_case_spec(tmp_path), extra=["--json"])
    assert res.returncode == 1
    payload = json.loads(res.stdout)
    assert payload["verdict"] == "FAIL"
    assert payload["exit_code"] == 1
    assert [c["name"] for c in payload["cases"]] == ["ok", "roto"]
    assert payload["cases"][0]["passed"] is True
    assert payload["cases"][1]["passed"] is False
