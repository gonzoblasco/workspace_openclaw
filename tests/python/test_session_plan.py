"""Tests para scripts/session_plan.py (hooks de planificacion de sesion).

Este script deja de ser un experimento huerfano: pasa a ser el objeto de
"memoria de intencion" que el arranque lee y el cierre archiva (Kanam OS Etapa 2,
session-planning-hooks). Por eso lo que se prueba es el CONTRATO que consumen
los hooks, no detalles internos:

  - el path del plan es portable y sobreescribible (SESSION_PLAN_PATH), no un
    /Users/... hardcodeado;
  - `close` es idempotente y NO rompe si no hay plan (el hook de cierre corre
    bajo `set -e`: un exit != 0 abortaria el cierre de sesion);
  - `close` archiva el plan y deja el path principal sin plan activo.

El defecto se siembra en directorios temporales (tmp_path), nunca en el
workspace real.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "session_plan.py"


def load():
    spec = importlib.util.spec_from_file_location("session_plan", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def point_at(monkeypatch, tmp_path):
    """Redirige el modulo al plan de un directorio temporal."""
    mod = load()
    plan = tmp_path / "session_plan.json"
    monkeypatch.setattr(mod, "PLAN_PATH", plan)
    return mod, plan


def test_path_derives_from_script_and_is_overridable(monkeypatch):
    """El plan se deriva del script (portable), no de una constante clavada;
    y respeta SESSION_PLAN_PATH para tests/aislamiento."""
    mod = load()
    assert mod.PLAN_PATH == mod.WORKSPACE / ".knowledge" / "session_plan.json"
    assert mod.PLAN_PATH.name == "session_plan.json"

    monkeypatch.setenv("SESSION_PLAN_PATH", "/tmp/otro/plan.json")
    mod2 = load()  # re-import: el modulo lee la env en import-time
    assert mod2.PLAN_PATH == Path("/tmp/otro/plan.json")


def test_init_writes_plan(monkeypatch, tmp_path):
    mod, plan = point_at(monkeypatch, tmp_path)
    mod.init_plan("objetivo", ["paso uno", "paso dos"])
    assert plan.exists()
    data = json.loads(plan.read_text(encoding="utf-8"))
    assert data["objective"] == "objetivo"
    assert data["status"] == "active"
    assert [s["id"] for s in data["steps"]] == [1, 2]
    assert all(s["status"] == "pending" for s in data["steps"])


def test_close_archives_and_clears(monkeypatch, tmp_path):
    mod, plan = point_at(monkeypatch, tmp_path)
    mod.init_plan("objetivo", ["a", "b"])
    mod.update_step(1, "completed")

    rc = mod.close_plan()
    assert rc == 0
    # El plan activo desaparece; el archivado conserva el historial.
    assert not plan.exists()
    archived = list((tmp_path / "archive").glob("session_plan_*.json"))
    assert len(archived) == 1
    data = json.loads(archived[0].read_text(encoding="utf-8"))
    assert data["status"] == "completed"
    assert data["metadata"].get("closed_at")


def test_close_is_idempotent_and_safe_without_plan(monkeypatch, tmp_path):
    """Bajo `set -e`, cerrar sin plan o cerrar dos veces NO debe fallar."""
    mod, _ = point_at(monkeypatch, tmp_path)
    assert mod.close_plan() == 0  # sin plan
    mod.init_plan("objetivo", ["a"])
    assert mod.close_plan() == 0
    assert mod.close_plan() == 0  # segunda vez


def test_cli_close_exit_code_is_zero(tmp_path, monkeypatch):
    """El hook invoca `session_plan.py close`; debe salir 0 siempre."""
    env = {"SESSION_PLAN_PATH": str(tmp_path / "session_plan.json")}
    import os

    full_env = {**os.environ, **env}
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "close"],
        capture_output=True, text=True, env=full_env, cwd=ROOT,
    )
    assert r.returncode == 0, r.stdout + r.stderr
