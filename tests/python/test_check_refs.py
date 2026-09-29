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


def test_skills_index_is_scanned():
    """SKILLS-INDEX.md debe estar en la lista default: es un doc de promesas vivas.

    Si queda fuera, sus links a `skills/<slug>/` rotos no se ven (el motivo por
    el que se agregaron los links al checker en primer lugar).
    """
    mod = load()
    assert "SKILLS-INDEX.md" in mod.DEFAULTS


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
    """Una ruta rota en un directorio historico NO debe reportarse: es historia.

    `docs/archives/` se renombro a `docs/history/` (reorg 2026-09-28); SKIP_DIRS
    debe seguir ambos, o el historico se escanea como si fuera una promesa viva.
    """
    mod = load()
    assert any("docs/archives/" in d for d in mod.SKIP_DIRS)
    assert any("docs/history/" in d for d in mod.SKIP_DIRS)


# --- links markdown: la clase de pudricion que motiva la extension (2026-09-26) ---
#
# El REF de backticks solo miraba scripts/ y docs/. Los links `./skills/...`
# de AGENTS.md apuntaban a 5 skills inexistentes tras moverlas a agents/ y
# nada lo decia. Estos tests fijan esa cobertura.

def test_link_regex_captures_relative_skill_link():
    mod = load()
    line = "Ver [`x`](./skills/session-lifecycle/SKILL.md)."
    assert "./skills/session-lifecycle/SKILL.md" in mod.LINK.findall(line)


def test_external_link_is_skipped():
    mod = load()
    assert mod.is_link_skippable("https://docs.openclaw.ai")


def test_anchor_and_absolute_are_skipped():
    mod = load()
    assert mod.is_link_skippable("#essential-checks")
    assert mod.is_link_skippable("/reference/AGENTS.default")


def test_directory_link_is_checked():
    """Un link a un DIRECTORIO se verifica: promete que el directorio existe.

    Antes se saltaba ("link a directorio, no a archivo"), y eso tapo 42 links
    rotos de SKILLS-INDEX.md que apuntaban a `skills/<slug>/` inexistentes.
    """
    mod = load()
    assert not mod.is_link_skippable("skills/session-lifecycle/")
    assert not mod.is_link_skippable("agents/kanam-dev/skills/a11y-at-validation/")


def test_reports_a_broken_directory_link(tmp_path):
    """Un link a un directorio inexistente debe fallar y nombrarlo."""
    bad = ROOT / "docs" / "_refs_dir_tmp.md"
    bad.write_text("Ver [x](./skills/no-existe-dir-xyz/).\n", encoding="utf-8")
    try:
        r = subprocess.run(
            [sys.executable, str(CHECKER), "--all"], cwd=ROOT, capture_output=True, text=True
        )
        assert r.returncode == 1
        assert "no-existe-dir-xyz" in r.stdout
    finally:
        bad.unlink(missing_ok=True)


def test_repo_root_link_is_checked():
    mod = load()
    assert not mod.is_link_skippable("agents/kanam-dev/skills/a11y-at-validation/SKILL.md")


def test_relative_link_resolves_from_source_dir(tmp_path):
    """`./x` se resuelve contra el doc que lo cita, no contra la raiz."""
    mod = load()
    sub = ROOT / "docs" / "_refs_test_sub"
    sub.mkdir(exist_ok=True)
    doc = sub / "a.md"
    try:
        (sub / "sibling.md").write_text("x", encoding="utf-8")
        doc.write_text("x", encoding="utf-8")
        assert mod.resolves(doc, "./sibling.md")
        assert not mod.resolves(doc, "./no-existe-xyz.md")
    finally:
        for p in sub.iterdir():
            p.unlink()
        sub.rmdir()


def test_reports_a_broken_relative_link(tmp_path):
    """Un link relativo a la nada debe fallar y nombrarlo."""
    bad = ROOT / "docs" / "_refs_link_tmp.md"
    bad.write_text("Ver [x](./skills/no-existe-link-xyz/SKILL.md).\n", encoding="utf-8")
    try:
        r = subprocess.run(
            [sys.executable, str(CHECKER), "--all"], cwd=ROOT, capture_output=True, text=True
        )
        assert r.returncode == 1
        assert "no-existe-link-xyz" in r.stdout
    finally:
        bad.unlink(missing_ok=True)


def test_links_on_root_anchored_convention_pass():
    """`./skills/...` escrito en un doc de docs/ se ancla a la raiz si ahi vive."""
    mod = load()
    doc = ROOT / "docs" / "pipeline" / "kanam-product-pipeline.md"
    assert mod.resolves(doc, "./skills/session-lifecycle/SKILL.md")
