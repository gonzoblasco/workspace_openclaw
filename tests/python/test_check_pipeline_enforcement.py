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
        'ROUTES=\'{"routes": {"pipeline_ab": "%s / %s", "pipeline_abc": "%s / %s / %s", "pipeline_ab_prefilter": "%s"}}\'\n'
        % (mod.A_ROLE, mod.B_ROLE, mod.A_ROLE, mod.B_ROLE, mod.C_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    (tmp_path / "scripts" / "managed-blocks.py").write_text(
        'DEFAULTS = {\n'
        '    "model_pipeline_a": "%s",\n'
        '    "model_pipeline_b": "%s",\n'
        '    "model_pipeline_c": "%s",\n'
        '    "model_pipeline_prefilter": "%s",\n'
        '}\n' % (mod.A_ROLE, mod.B_ROLE, mod.C_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    (tmp_path / "skills" / "agent-orchestration-pipeline-model-arbitration" / "SKILL.md").write_text(
        "A usa `%s` y B usa `%s` y C usa `%s`.\n" % (mod.A_ROLE, mod.B_ROLE, mod.C_ROLE),
        encoding="utf-8",
    )
    (tmp_path / "docs" / "adr" / "ADR-077-pipeline-ab-asimetrico.md").write_text(
        "pipeline_ab -> %s / %s\n" % (mod.A_ROLE, mod.B_ROLE),
        encoding="utf-8",
    )
    # ADR-105 for ABC
    (tmp_path / "docs" / "adr" / "ADR-105-pipeline-abc.md").write_text(
        "pipeline_abc -> %s / %s / %s\n" % (mod.A_ROLE, mod.B_ROLE, mod.C_ROLE),
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


def test_removed_arbitration_skill_is_not_a_source(tmp_path):
    """La skill de arbitraje se elimino el 2026-11-06 (ADR-088).

    Los modelos viven en model-router.sh + managed-blocks.py. Un archivo con ese
    nombre, con contenido arbitrario, no puede introducir ni silenciar violaciones:
    el check ya no lo lee. Este test fija ese contrato.
    """
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "skills" / "agent-orchestration-pipeline-model-arbitration" / "SKILL.md").write_text(
        "sin modelos.\n", encoding="utf-8"
    )

    violations = mod.find_violations(tmp_path)
    assert not any("skill de arbitraje" in v for v in violations), violations


def test_exit_codes_distinguish_clean_from_dirty(tmp_path):
    """El check tiene que PODER fallar: exit 0 limpio, exit 1 con el defecto."""
    mod = load()
    clean_root(tmp_path, mod)
    assert mod.main(["check", str(tmp_path)]) == 0

    (tmp_path / "scripts" / "model-router.sh").write_text('ROUTES=\'{"routes": {}}\'\n', encoding="utf-8")
    assert mod.main(["check", str(tmp_path)]) == 1


def test_missing_prefilter_is_reported(tmp_path):
    """Sin la ruta del pre-filtro (ADR-089) no hay triage declarado."""
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_ab": "%s / %s"}}\'\n' % (mod.A_ROLE, mod.B_ROLE),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("pipeline_ab_prefilter" in v for v in violations), violations


def test_inconsistent_prefilter_is_reported(tmp_path):
    """Router y managed-blocks con pre-filtros distintos."""
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "scripts" / "managed-blocks.py").write_text(
        'DEFAULTS = {\n    "model_pipeline_a": "%s",\n    "model_pipeline_b": "%s",\n'
        '    "model_pipeline_prefilter": "glm4:9b",\n}\n' % (mod.A_ROLE, mod.B_ROLE),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("pre-filtro" in v for v in violations), violations


# --- Regresiones: el reporte de git NO es una violacion del pacto (2026-10-12) ---
# El checker nacio para verificar el pacto A/B. Un workspace sucio (untracked,
# cambios sin commitear) es INFORMATIVO: no rompe el pacto. Antes de este fix, un
# arbol limpio devolvia exit 1 con la unica "violacion" = "Sin cambios detectables."


def test_porcelain_parse_keeps_full_paths(mod=None):
    """parse_porcelain devuelve el path completo, no truncado."""
    mod = load()
    out = (
        " M scripts/check-pipeline-enforcement.py\n"
        "M  memory/2026-10-09.md\n"
        "?? lore_las_tres_sabanas.md\n"
    )
    entries = mod.parse_porcelain(out)
    paths = [p for _, p in entries]
    assert "scripts/check-pipeline-enforcement.py" in paths
    assert "memory/2026-10-09.md" in paths
    assert "lore_las_tres_sabanas.md" in paths
    # Ningun path puede venir cortado por un offset fijo.
    assert all(not p.startswith("cripts/") for p in paths)


def test_dirty_workspace_is_not_a_pact_violation(tmp_path, monkeypatch):
    """Un workspace con untracked NO es violacion: el check sigue en exit 0."""
    import subprocess
    mod = load()
    clean_root(tmp_path, mod)

    # Simula un `git status --porcelain` sucio sin depender de un repo real.
    class _R:
        stdout = "?? archivo_nuevo.md\n M scripts/model-router.sh\n"

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _R())
    assert mod.find_violations(tmp_path) == []
    assert mod.main(["check", str(tmp_path)]) == 0


def test_staged_report_marks_staged_and_untracked(tmp_path, monkeypatch):
    """_git_staged_report separa staged de untracked y no los mezcla."""
    import subprocess
    mod = load()

    class _R:
        stdout = (
            "M  memoria.md\n"          # staged
            "?? nuevo.md\n"            # untracked
        )

    def _run(cmd, *a, **k):
        if cmd[:3] == ["git", "status", "--porcelain"]:
            return _R()
        class _D:
            stdout = ""
        return _D()

    monkeypatch.setattr(subprocess, "run", _run)
    staged, report = mod._git_staged_report(tmp_path)
    assert "memoria.md" in staged
    assert "nuevo.md" not in staged
    assert "Untracked" in report

# New ABC pact tests ---------------------------------------------------------

def test_missing_router_abc_route_is_reported(tmp_path):
    """Router lacks pipeline_abc route."""
    mod = load()
    clean_root(tmp_path, mod)
    # Remove pipeline_abc from router
    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_ab": "%s / %s", "pipeline_ab_prefilter": "%s"}}\'\n'
        % (mod.A_ROLE, mod.B_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("pipeline_abc" in v for v in violations), violations

def test_router_abc_incomplete_models_is_reported(tmp_path):
    """Router declares pipeline_abc with only two models."""
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_abc": "%s / %s", "pipeline_ab": "%s / %s", "pipeline_ab_prefilter": "%s"}}\'\n'
        % (mod.A_ROLE, mod.B_ROLE, mod.A_ROLE, mod.B_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("pipeline_abc" in v and "solo dos modelos" in v for v in violations), violations

def test_missing_model_pipeline_c_in_blocks(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    # Remove model_pipeline_c from managed-blocks defaults
    (tmp_path / "scripts" / "managed-blocks.py").write_text(
        'DEFAULTS = {\n'
        '    "model_pipeline_a": "%s",\n'
        '    "model_pipeline_b": "%s",\n'
        '    "model_pipeline_prefilter": "%s",\n'
        '}\n' % (mod.A_ROLE, mod.B_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("model_pipeline_c" in v for v in violations), violations

def test_removed_skill_cannot_hide_missing_c(tmp_path):
    """C es obligatorio, y su ausencia se detecta por router/blocks/ADR, no por la skill.

    Con la skill eliminada, quitar C del router sigue reportando violacion: la
    fuente de verdad del pacto no depende de un archivo que ya no existe.
    """
    mod = load()
    clean_root(tmp_path, mod)
    (tmp_path / "skills" / "agent-orchestration-pipeline-model-arbitration" / "SKILL.md").write_text(
        "A usa `%s` y B usa `%s`.\n" % (mod.A_ROLE, mod.B_ROLE),
        encoding="utf-8",
    )
    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_ab": "%s / %s", "pipeline_abc": "%s / %s", "pipeline_ab_prefilter": "%s"}}\'\n'
        % (mod.A_ROLE, mod.B_ROLE, mod.A_ROLE, mod.B_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("pipeline_abc" in v and "tres modelos" in v for v in violations), violations

def test_adr_105_missing_models_is_reported(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    # Remove ADR-105 file
    (tmp_path / "docs" / "adr" / "ADR-105-pipeline-abc.md").unlink()
    violations = mod.find_violations(tmp_path)
    assert any("ADR-105" in v for v in violations), violations

def test_router_c_vs_blocks_c_mismatch_is_reported(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    # Change C in router to different value
    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_abc": "%s / %s / glm-5.3-flash:cloud", "pipeline_ab": "%s / %s", "pipeline_ab_prefilter": "%s"}}\'\n'
        % (mod.A_ROLE, mod.B_ROLE, mod.A_ROLE, mod.B_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("modelo C" in v and "distinto" in v for v in violations), violations

def test_asymmetry_a_equals_c_is_reported(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    # Set C equal to A in router
    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_abc": "%s / %s / %s", "pipeline_ab": "%s / %s", "pipeline_ab_prefilter": "%s"}}\'\n'
        % (mod.A_ROLE, mod.B_ROLE, mod.A_ROLE, mod.A_ROLE, mod.B_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("C" in v and "igual" in v for v in violations), violations

def test_asymmetry_b_equals_c_is_reported(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    # Set C equal to B in router
    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_abc": "%s / %s / %s", "pipeline_ab": "%s / %s", "pipeline_ab_prefilter": "%s"}}\'\n'
        % (mod.A_ROLE, mod.B_ROLE, mod.B_ROLE, mod.A_ROLE, mod.B_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("C" in v and "igual" in v for v in violations), violations

def test_router_models_not_canonical_is_reported(tmp_path):
    mod = load()
    clean_root(tmp_path, mod)
    # Change router to non-canonical models
    (tmp_path / "scripts" / "model-router.sh").write_text(
        'ROUTES=\'{"routes": {"pipeline_abc": "glm-5.3-flash:cloud / deepseek-v4.1-flash:cloud / minimax-m3.1-flash:cloud", "pipeline_ab": "%s / %s", "pipeline_ab_prefilter": "%s"}}\'\n'
        % (mod.A_ROLE, mod.B_ROLE, mod.PREFILTER),
        encoding="utf-8",
    )
    violations = mod.find_violations(tmp_path)
    assert any("pipeline_abc" in v and "canon" in v for v in violations), violations
