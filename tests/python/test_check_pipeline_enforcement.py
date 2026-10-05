"""Tests for scripts/check-pipeline-enforcement.py (pacto del pipeline A/B).

El checker existe porque el CORE delego una sesion entera con un solo agente y el
modelo por defecto del rol, en vez de A/B con los modelos del pacto (ADR-077). La
regla estaba escrita y nada la verificaba; el router era un chequeo voluntario.

Propiedades criticas: cazar (1) una fuente que no declara el pacto, (2) dos fuentes
que declaran distinto, y (3) la asimetria rota (A == B).

Un chequeo que solo corre contra un arbol limpio NO esta probado. Por eso cada test
SIEMBRA el defecto en arboles falsos en tmp_path. El ultimo test exige que el check
DISTINGA el caso limpio del sucio (que pueda fallar).
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-pipeline-enforcement.py"


def load():
    spec = importlib.util.spec_from_file_location("check_pipeline_enforcement", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def clean_root(tmp_path, mod):
    """Un root donde las cuatro fuentes declaran el pacto vigente e identico."""
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "skills" / "agent-orchestration-pipeline-model-arbitration").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "adr").mkdir(parents=True, exist_ok=True)

    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_ab": "%s / %s"}}\'\n' % (mod.A_ROLE, mod.B_ROLE),
        encoding="utf-8",
    )
    (tmp_path / "scripts" / "managed-blocks.py").write_text(
        'DEFAULTS = {\n'
        '    "model_pipeline_a": "%s",\n'
        '    "model_pipeline_b": "%s",\n'
        '}\n' % (mod.A_ROLE, mod.B_ROLE),
        encoding="utf-8",
    )
    (tmp_path / "skills" / "agent-orchestration-pipeline-model-arbitration" / "SKILL.md").write_text(
        "A usa `%s` y B usa `%s`.\n" % (mod.A_ROLE, mod.B_ROLE),
        encoding="utf-8",
    )
    (tmp_path / "docs" / "adr" / "ADR-077-pipeline-ab-asimetrico.md").write_text(
        "pipeline_ab -> %s / %s\n" % (mod.A_ROLE, mod.B_ROLE),
        encoding="utf-8",
    )
    return tmp_path


def test_clean_tree_has_no_violations(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    assert mod.find_violations(tmp_path) == []


def test_missing_router_route_is_reported(tmp_path):
    """Sin la ruta en el router, no hay fuente de verdad del modelo."""
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "scripts" / "model-router.sh").write_text('ROUTES=\'{"routes": {}}\'\n', encoding="utf-8")

    violations = mod.find_violations(tmp_path)
    assert any("model-router.sh" in v for v in violations), violations


def test_two_truths_are_reported(tmp_path):
    """Router y managed-blocks en desacuerdo: el pacto tiene dos verdades."""
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "scripts" / "managed-blocks.py").write_text(
        'DEFAULTS = {\n    "model_pipeline_a": "glm-5.3-flash:cloud",\n'
        '    "model_pipeline_b": "%s",\n}\n' % mod.B_ROLE,
        encoding="utf-8",
    )

    violations = mod.find_violations(tmp_path)
    assert any("dos verdades" in v for v in violations), violations


def test_broken_asymmetry_is_reported(tmp_path):
    """A == B: el revisor deja de ver mas que el ejecutor."""
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_ab": "%s / %s"}}\'\n' % (mod.A_ROLE, mod.A_ROLE),
        encoding="utf-8",
    )
    (tmp_path / "scripts" / "managed-blocks.py").write_text(
        'DEFAULTS = {\n    "model_pipeline_a": "%s",\n    "model_pipeline_b": "%s",\n}\n'
        % (mod.A_ROLE, mod.A_ROLE),
        encoding="utf-8",
    )

    violations = mod.find_violations(tmp_path)
    assert any("asimetria rota" in v for v in violations), violations


def test_skill_not_naming_models_is_reported(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "skills" / "agent-orchestration-pipeline-model-arbitration" / "SKILL.md").write_text(
        "sin modelos.\n", encoding="utf-8"
    )

    violations = mod.find_violations(tmp_path)
    assert any("skill de arbitraje" in v for v in violations), violations


def test_exit_codes_distinguish_clean_from_dirty(tmp_path):
    """El check tiene que PODER fallar: exit 0 limpio, exit 1 con el defecto."""
    mod = load()
    clean_root(tmp_path, mod)
    assert mod.main(["check", str(tmp_path)]) == 0

    (tmp_path / "scripts" / "model-router.sh").write_text('ROUTES=\'{"routes": {}}\'\n', encoding="utf-8")
    assert mod.main(["check", str(tmp_path)]) == 1
