#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Configuración
PLAN_PATH = Path("/Users/gonzoblasco/.openclaw/workspace/.session_plan.json")

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
        print("Acciones: init <obj> <step1,step2...>, update <id> <status> [blocker], summary")
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
