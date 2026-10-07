"""Tests for scripts/check-bootstrap-budget.py.

El checker existe porque los archivos de bootstrap (los que OpenClaw inyecta en
cada arranque) se truncan EN SILENCIO al superar su cap: el agente arranca sin
esas reglas y no lo sabe. El 2026-10-06 los tres estaban sobre cap; AGENTS ya
habia bajado una vez y USER.md regreso. Una regla sin guarda se viola sola.

Propiedades criticas: medir en caracteres como el runtime (UTF-16), NO en bytes
(`wc -c` sobreestima en espanol y da un margen falso); usar el cap correcto por
archivo (USER.md = 4.000, el resto 20.000); cubrir la CLASE (cualquier archivo de
la lista, no solo el que lo motivo) y el total. Por eso cada test siembra el
defecto en arboles falsos en tmp_path.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-bootstrap-budget.py"


def load():
    spec = importlib.util.spec_from_file_location("check_bootstrap_budget", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def clean_root(tmp_path, mod, sizes=None):
    """Un root con todos los archivos de bootstrap bajo cap.

    sizes: dict opcional name -> nro de chars del contenido.
    """
    sizes = sizes or {}
    for name in mod.BOOTSTRAP_FILES:
        n = sizes.get(name, 100)
        (tmp_path / name).write_text("x" * n, encoding="utf-8")
    return tmp_path


# --- el caso limpio: el check no inventa violaciones ---

def test_clean_tree_has_no_violations(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    assert mod.find_violations(tmp_path) == []


# --- la causa raiz: un archivo sobre su cap ---

def test_over_cap_file_is_reported(tmp_path):
    """AGENTS.md en 20.001 chars: el caso que motiva el check."""
    mod = load()
    clean_root(tmp_path, mod, {"AGENTS.md": 20_001})
    violations = mod.find_violations(tmp_path)
    assert any("AGENTS.md" in v for v in violations), violations


# --- la CLASE: cualquier archivo de la lista ---

def test_the_class_is_covered_not_just_the_motivating_case(tmp_path):
    """Cada archivo de bootstrap sobre su propio cap debe ser cazado."""
    mod = load()
    for name in mod.BOOTSTRAP_FILES:
        clean_root(tmp_path, mod)
        cap = mod.cap_for(name)
        (tmp_path / name).write_text("x" * (cap + 1), encoding="utf-8")
        violations = mod.find_violations(tmp_path)
        assert any(name in v for v in violations), (name, violations)


# --- USER.md tiene cap propio, mas chico ---

def test_user_md_uses_its_own_smaller_cap(tmp_path):
    mod = load()
    assert mod.cap_for("USER.md") == 4_000
    assert mod.cap_for("AGENTS.md") == 20_000
    # 5.000 chars: bajo el cap general pero SOBRE el de USER.md.
    clean_root(tmp_path, mod, {"USER.md": 5_000})
    violations = mod.find_violations(tmp_path)
    assert any("USER.md" in v for v in violations), violations


# --- a exactamente el cap NO es violacion (borde) ---

def test_exactly_at_cap_is_ok(tmp_path):
    mod = load()
    clean_root(tmp_path, mod, {"AGENTS.md": 20_000, "USER.md": 4_000})
    assert mod.find_violations(tmp_path) == []


# --- mide en caracteres como el runtime, no en bytes ---

def test_measures_utf16_units_like_runtime(tmp_path):
    """Un emoji (astral) cuenta 2 unidades UTF-16 aunque sea 1 code point.

    Si el check midiera en bytes UTF-8, 'é' (2 bytes) inflaria el numero y daria
    un falso rojo. Mide como el runtime: unidades UTF-16 de JS.
    """
    mod = load()
    assert mod.utf16_len("abc") == 3
    assert mod.utf16_len("é") == 1        # 2 bytes UTF-8, 1 unidad UTF-16
    assert mod.utf16_len("😀") == 2       # 1 code point, 2 unidades UTF-16
    # 2.000 emojis = 4.000 unidades: justo en el cap de USER.md.
    txt = "😀" * 2_000
    assert len(txt) == 2_000              # code points
    assert mod.utf16_len(txt) == 4_000    # unidades UTF-16


# --- el TOTAL tambien tiene cap ---

def test_total_cap_is_enforced(tmp_path):
    """4 archivos de 20.000 = 80.000 > 60.000 total, aunque ninguno exceda su cap."""
    mod = load()
    clean_root(tmp_path, mod, {"AGENTS.md": 20_000, "MEMORY.md": 20_000,
                               "SOUL.md": 20_000, "IDENTITY.md": 20_000, "USER.md": 100})
    violations = mod.find_violations(tmp_path)
    assert any("TOTAL" in v for v in violations), violations


# --- la lista no esta vacia ni es derivada ---

def test_bootstrap_files_is_nonempty_explicit(tmp_path):
    mod = load()
    assert set(mod.BOOTSTRAP_FILES) >= {"AGENTS.md", "MEMORY.md", "USER.md"}
    assert mod.PER_FILE_CAP == 20_000
    assert mod.USER_CAP == 4_000
    assert mod.TOTAL_CAP == 60_000


# --- end-to-end: el script real corre y reporta ---

def test_passes_on_real_workspace():
    r = subprocess.run(
        [sys.executable, str(CHECKER)], cwd=ROOT, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_script_reports_and_fails_on_over_cap(tmp_path):
    """El script real, contra un root falso con un archivo sobre cap, sale 1."""
    mod = load()
    clean_root(tmp_path, mod, {"MEMORY.md": 25_000})
    (tmp_path / "scripts").mkdir(exist_ok=True)
    script_copy = tmp_path / "scripts" / "check-bootstrap-budget.py"
    script_copy.write_text(CHECKER.read_text(encoding="utf-8"), encoding="utf-8")

    r = subprocess.run(
        [sys.executable, str(script_copy)], cwd=tmp_path, capture_output=True, text=True
    )
    assert r.returncode == 1, r.stdout + r.stderr
    assert "MEMORY.md" in r.stdout
