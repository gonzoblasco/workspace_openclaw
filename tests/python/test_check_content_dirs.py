"""Tests for scripts/check-content-dirs.py (existencia de directorios de contenido).

El checker existe porque el commit `dfa94759` ("cleanup: remove studies, tmp dirs")
borro TODO `studies/` y se pusheo a origin/main sin que ninguna guarda lo viera:
check-refs verifica rutas CITADAS (un borrado en bloque no rompe citas) y
check-adr-integrity cubre docs/adr/. Los directorios de contenido quedaron sin
cobertura. Una guarda que verifica referencias no es una guarda que verifica
existencia.

Propiedades criticas: cazar el directorio que desaparece, NO reportar un arbol
limpio, y - sobre todo - probar la CLASE: que el check falla cuando un directorio
cualquiera de la lista se va, no solo cuando desaparece el caso que lo motivo
(studies/). Por eso cada test SIEMBRA el defecto en arboles falsos en tmp_path.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-content-dirs.py"


def load():
    spec = importlib.util.spec_from_file_location("check_content_dirs", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def clean_root(tmp_path, mod):
    """Un root donde todos los directorios de contenido existen."""
    for name in mod.CONTENT_DIRS:
        (tmp_path / name).mkdir(parents=True, exist_ok=True)
    return tmp_path


# --- el caso limpio: el check no inventa violaciones ---

def test_clean_tree_has_no_violations(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    assert mod.find_violations(tmp_path) == []


# --- la causa raiz: el directorio borrado en bloque ---

def test_missing_dir_is_reported(tmp_path):
    """El caso que motiva el check: `studies/` desaparece."""
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "studies").rmdir()

    violations = mod.find_violations(tmp_path)
    assert any("studies" in v for v in violations), violations


# --- la CLASE, no el caso: cualquier directorio de la lista ---

def test_the_class_is_covered_not_just_the_motivating_case(tmp_path):
    """Un directorio cualquiera de la lista, no solo `studies/`.

    Si el check solo cazara el caso que lo motivo, el proximo borrado masivo
    (`design/`, `prompts/`) pasaria igual. Se prueba cada nombre de la lista.
    """
    mod = load()
    for name in mod.CONTENT_DIRS:
        clean_root(tmp_path, mod)
        (tmp_path / name).rmdir()
        violations = mod.find_violations(tmp_path)
        assert any(name in v for v in violations), (name, violations)


# --- la lista no esta vacia ni es derivada ---

def test_content_dirs_is_a_nonempty_explicit_list():
    mod = load()
    assert len(mod.CONTENT_DIRS) >= 5
    assert "studies" in mod.CONTENT_DIRS


# --- end-to-end: el script real corre y reporta ---

def test_passes_on_real_workspace():
    """El workspace real debe tener todos sus directorios de contenido."""
    r = subprocess.run(
        [sys.executable, str(CHECKER)], cwd=ROOT, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_script_reports_and_fails_on_missing_dir(tmp_path):
    """El script real, con un root falso incompleto, sale 1 y nombra el faltante.

    Se corre el script de verdad (no solo la funcion) contra un arbol temporal
    armado con la misma lista, para probar el contrato de salida (exit code +
    mensaje), que es lo que lee el pre-commit.
    """
    mod = load()
    for name in mod.CONTENT_DIRS:
        (tmp_path / name).mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts").mkdir(exist_ok=True)
    # El script resuelve ROOT desde su propia ubicacion: se copia a un root falso.
    script_copy = tmp_path / "scripts" / "check-content-dirs.py"
    script_copy.write_text(CHECKER.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "design").rmdir()

    r = subprocess.run(
        [sys.executable, str(script_copy)], cwd=tmp_path, capture_output=True, text=True
    )
    assert r.returncode == 1, r.stdout + r.stderr
    assert "design" in r.stdout
