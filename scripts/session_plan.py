#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Configuración
# Ruta derivada del propio script (no absoluta): el workspace vive solo en la
# Mac Mini (ADR-085), pero un path relativo lo hace portable y testeable. El
# plan vive en .knowledge/ (estado durable del workspace, no cruft de raiz) y
# es sobrescribible con SESSION_PLAN_PATH para los tests.
WORKSPACE = Path(__file__).resolve().parent.parent
PLAN_PATH = Path(os.environ.get("SESSION_PLAN_PATH", WORKSPACE / ".knowledge" / "session_plan.json"))

def load_plan():
    if not PLAN_PATH.exists():
        return None
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_plan(plan):
    with open(PLAN_PATH, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

def init_plan(objective, steps):
    plan = {
        "session_id": datetime.now().strftime("%Y%m%d%H%M"),
        "objective": objective,
        "status": "active",
        "steps": [
            {"id": i+1, "task": s, "status": "pending", "blocker": None, "timestamp": None} 
            for i, s in enumerate(steps)
        ],
        "metadata": {
            "started_at": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat()
        }
    }
    save_plan(plan)
    print(f"✅ Plan de sesión inicializado: {objective}")

def update_step(step_id, status, blocker=None):
    plan = load_plan()
    if not plan:
        print("Error: No hay un plan activo.")
        return

    for step in plan["steps"]:
        if step["id"] == step_id:
            step["status"] = status
            step["blocker"] = blocker
            step["timestamp"] = datetime.now().isoformat()
            break
    
    plan["metadata"]["last_update"] = datetime.now().isoformat()
    save_plan(plan)
    print(f"✅ Step {step_id} actualizado a {status}")

def close_plan():
    """Cierra el plan activo: lo marca completado y lo archiva.

    Idempotente y no destructivo: si no hay plan (o ya estaba cerrado), sale 0
    sin tocar nada, para que el hook de cierre de sesion nunca rompa con
    `set -e`. El plan archivado queda en .knowledge/archive/ con su session_id,
    como historial; el path principal vuelve a quedar sin plan activo.
    """
    plan = load_plan()
    if not plan:
        print("Sin plan activo que cerrar.")
        return 0
    if plan.get("status") == "completed":
        print("El plan ya estaba cerrado.")
        return 0

    plan["status"] = "completed"
    plan["metadata"]["last_update"] = datetime.now().isoformat()
    plan["metadata"]["closed_at"] = plan["metadata"]["last_update"]
    save_plan(plan)

    archive_dir = PLAN_PATH.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = archive_dir / f"session_plan_{plan['session_id']}.json"
    with open(archived, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    PLAN_PATH.unlink(missing_ok=True)

    done = sum(1 for s in plan["steps"] if s["status"] == "completed")
    print(
        f"✅ Plan cerrado y archivado: {plan['objective']} "
        f"({done}/{len(plan['steps'])} pasos completados) -> {archived.name}"
    )
    return 0


def get_summary():
    plan = load_plan()
    if not plan:
        return "No hay plan activo."
    
    summary = f"🎯 Objetivo: {plan['objective']}\n"
    summary += "Pasos:\n"
    for s in plan["steps"]:
        mark = "✅" if s["status"] == "completed" else "⏳" if s["status"] == "pending" else "🚧"
        summary += f"  {mark} {s['id']}. {s['task']} ({s['status']})\n"
    
    return summary

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 session_plan.py <action> [args...]")
        print("Acciones: init <obj> <step1,step2...>, update <id> <status> [blocker], summary, close")
        sys.exit(1)

    action = sys.argv[1]

    if action == "init":
        obj = sys.argv[2]
        steps = sys.argv[3].split(",")
        init_plan(obj, steps)
    elif action == "update":
        s_id = int(sys.argv[2])
        stat = sys.argv[3]
        block = sys.argv[4] if len(sys.argv) > 4 else None
        update_step(s_id, stat, block)
    elif action == "summary":
        print(get_summary())
    elif action == "close":
        sys.exit(close_plan())
    else:
        print(f"Accion desconocida: {action}")
        sys.exit(1)
