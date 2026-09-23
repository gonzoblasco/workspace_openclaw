"""Tests for scripts/check-refs.py (rutas citadas en los docs).

El checker existe porque docs/AGENTS-DETALLE.md citaba `scripts/pr-thread-brief.sh`
como "verificacion mecanica" de una regla dura, y ese script nunca existio.

Propiedades criticas: detectar una ruta rota, NO reportar falsos positivos
(placeholders, directorios, globs), y no tocar los directorios historicos.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-refs.py"


def load():
    spec = importlib.util.spec_from_file_location("check_refs", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- is_skippable: no reportar lo que no es una ruta literal ---

def test_placeholder_is_skipped():
    mod = load()
    assert mod.is_skippable("docs/feedback/<repo>-<numero>-draft.md")


def test_directory_is_skipped():
    mod = load()
    assert mod.is_skippable("docs/adr/")


def test_glob_is_skipped():
    mod = load()
    assert mod.is_skippable("docs/learnings/*.md")


def test_real_path_is_not_skipped():
    mod = load()
    assert not mod.is_skippable("scripts/memory-db.sh")


# --- el regex de deteccion ---

def test_regex_captures_script_ref():
    mod = load()
    assert "scripts/memory-db.sh" in mod.REF.findall("Ver `scripts/memory-db.sh`.")


def test_regex_captures_docs_ref():
    mod = load()
    assert "docs/SETUP.md" in mod.REF.findall("Ver `docs/SETUP.md`.")


def test_regex_ignores_non_path_backticks():
    mod = load()
    assert mod.REF.findall("Usar `settings` y `todos`.") == []


# --- el comportamiento end-to-end del script ---

def test_passes_on_real_agent_docs():
    """Los docs del agente deben estar limpios."""
    r = subprocess.run(
        [sys.executable, str(CHECKER)], cwd=ROOT, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_passes_on_all_docs():
    """Todos los docs (excluyendo historicos) deben estar limpios."""
    r = subprocess.run(
        [sys.executable, str(CHECKER), "--all"], cwd=ROOT, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_reports_a_broken_ref(tmp_path):
    """Una ruta que no existe debe fallar y nombrarla."""
    bad = ROOT / "docs" / "_refs_test_tmp.md"
    bad.write_text("Ver `scripts/no-existe-jamas-xyz.sh`.\n", encoding="utf-8")
    try:
        r = subprocess.run(
            [sys.executable, str(CHECKER), "--all"], cwd=ROOT, capture_output=True, text=True
        )
        assert r.returncode == 1
        assert "no-existe-jamas-xyz.sh" in r.stdout
    finally:
        bad.unlink(missing_ok=True)


def test_skips_historic_dirs():
    """Una ruta rota en docs/archives/ NO debe reportarse: es historia."""
    mod = load()
    assert any("docs/archives/" in d for d in mod.SKIP_DIRS)
