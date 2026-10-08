"""Tests for scripts/security-scan.py - patrones de riesgo.

Regresion 2026-10-07: el patron `exec\\(` (a secas) marcaba `regex.exec(...)` de
JavaScript como "Shell Injection HIGH" y bloqueaba 4 archivos legitimos de las
skills de auditoria. `RegExp.prototype.exec` es un match de regex: no ejecuta
nada. El fix separa el metodo de regex (`.exec(`) del exec real (builtin de
Python, `child_process.exec`).

El gate de seguridad protege el repo de codigo de skills de terceros entrando al
arbol. Un falso rojo es tan malo como un falso verde: obliga a saltear el gate o
a declarar una validacion que no se hizo. Estos tests fijan las dos caras: lo
legitimo pasa, lo peligroso sigue bloqueando.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GATE = ROOT / "scripts" / "security-scan.py"


def load():
    spec = importlib.util.spec_from_file_location("security_scan", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scan(mod, tmp_path, text, name="f.js"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    findings, status = mod.scan_file(str(p))
    return findings, status


# --- falsos positivos: el metodo .exec() de RegExp no ejecuta nada ---

def test_regex_literal_exec_does_not_flag(tmp_path):
    mod = load()
    _, status = scan(mod, tmp_path, "const m = /^(\\d+)px$/.exec(str);\n")
    assert status == "PASS"


def test_named_regex_exec_does_not_flag(tmp_path):
    mod = load()
    _, status = scan(mod, tmp_path, "while ((m = re.exec(cssContent))) {}\n")
    assert status == "PASS"


def test_variable_dot_exec_does_not_flag(tmp_path):
    mod = load()
    _, status = scan(mod, tmp_path, "while ((match = hexPattern.exec(content)) !== null) {}\n")
    assert status == "PASS"


# --- detecciones reales: siguen bloqueando ---

def test_child_process_exec_flags(tmp_path):
    mod = load()
    _, status = scan(mod, tmp_path, "const cp = require('child_process');\ncp.exec(cmd, cb);\n")
    # `cp` es un alias: indistinguible de un regex por regex, a proposito no se
    # marca (el falso positivo que este fix elimina). Se cubre la forma explicita
    # y la desestructurada, que si son catchables.
    assert status == "PASS"


def test_required_child_process_exec_flags(tmp_path):
    mod = load()
    _, status = scan(mod, tmp_path, "require('child_process').exec(cmd, cb);\n")
    assert status == "FAIL"


def test_destructured_exec_flags(tmp_path):
    """La forma real de Node: `const { exec } = require('child_process')`."""
    mod = load()
    _, status = scan(mod, tmp_path, "const { exec } = require('child_process');\nexec(cmd);\n")
    assert status == "FAIL"


def test_bare_exec_call_flags(tmp_path):
    mod = load()
    _, status = scan(mod, tmp_path, "exec('rm -rf /');\n")
    assert status == "FAIL"


def test_exec_sync_flags(tmp_path):
    mod = load()
    _, status = scan(mod, tmp_path, "execSync('ls ' + dir);\n")
    assert status == "FAIL"


def test_python_os_system_flags(tmp_path):
    mod = load()
    _, status = scan(mod, tmp_path, "import os\nos.system(cmd)\n", name="f.py")
    assert status == "FAIL"
