"""Tests for scripts/check-agent-skill-boundary.py (frontera CORE vs arbol de rol).

El checker existe porque el CORE escribio codigo de produccion durante una sesion
entera, con las 9 skills del ciclo SDD a la vista en `skills/`. La regla estaba
escrita y nada la verificaba.

Propiedades criticas: cazar la causa raiz (ciclo SDD en el arbol del CORE), el
duplicado (una skill en dos arboles), y el ciclo incompleto.

Un chequeo que solo corre contra un arbol limpio NO esta probado: puede reportar OK
sin mirar nada. Por eso cada test SIEMBRA el defecto en arboles falsos en tmp_path.
Y el ultimo test verifica que el check PUEDE fallar: se le da el caso limpio y el
caso sucio y se exige que distinga.
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-agent-skill-boundary.py"


def load():
    spec = importlib.util.spec_from_file_location("check_agent_skill_boundary", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_skill(root, tree, name):
    """Crea `<root>/<tree>/<name>/SKILL.md`."""
    d = root / tree / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text("---\nname: %s\n---\n" % name, encoding="utf-8")


def clean_root(tmp_path, mod):
    """Un root donde el ciclo SDD esta completo en su rol y ausente del CORE."""
    for name in mod.SDD_CYCLE:
        make_skill(tmp_path, "agents/kanam-dev/skills", name)
    make_skill(tmp_path, "skills", "session-lifecycle")
    return tmp_path


def test_clean_tree_has_no_violations(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    assert mod.find_violations(tmp_path) == []


def test_sdd_skill_in_core_tree_is_reported(tmp_path):
    """La causa raiz: el playbook de ingenieria a la vista del CORE."""
    mod = load()
    clean_root(tmp_path, mod)
    make_skill(tmp_path, "skills", "hermes-builder")

    violations = mod.find_violations(tmp_path)
    assert any("SDD skill in the Core tree" in v and "hermes-builder" in v for v in violations), violations


def test_skill_in_two_trees_is_reported(tmp_path):
    """Un duplicado anula la separacion: el CORE la vuelve a ver."""
    mod = load()
    clean_root(tmp_path, mod)
    make_skill(tmp_path, "skills", "hermes-qa")

    violations = mod.find_violations(tmp_path)
    assert any("two trees" in v and "hermes-qa" in v for v in violations), violations


def test_incomplete_sdd_cycle_is_reported(tmp_path):
    """Un movimiento a medias pierde etapas sin que nada lo diga."""
    mod = load()
    clean_root(tmp_path, mod)
    import shutil

    shutil.rmtree(tmp_path / "agents/kanam-dev/skills/hermes-release")

    violations = mod.find_violations(tmp_path)
    assert any("SDD cycle incomplete" in v and "hermes-release" in v for v in violations), violations


def test_skill_in_two_role_trees_is_reported(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    make_skill(tmp_path, "agents/kanam-mind/skills", "hermes-discovery")

    violations = mod.find_violations(tmp_path)
    assert any("two role trees" in v and "hermes-discovery" in v for v in violations), violations


def test_exit_codes_distinguish_clean_from_dirty(tmp_path):
    """El check tiene que PODER fallar: exit 0 limpio, exit 1 con el defecto."""
    mod = load()
    clean_root(tmp_path, mod)
    assert mod.main(["check", str(tmp_path)]) == 0

    make_skill(tmp_path, "skills", "hermes-builder")
    assert mod.main(["check", str(tmp_path)]) == 1
