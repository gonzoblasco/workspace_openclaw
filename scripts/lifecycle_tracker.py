#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Configuración
# Ruta derivada del propio script (no absoluta). El workspace vive solo en la
# Mac Mini (ADR-085), pero un path relativo lo hace portable y testeable.
WORKSPACE = Path(__file__).resolve().parent.parent
TRACKER_PATH = WORKSPACE / ".knowledge" / "skill_lifecycle.json"

def load_tracker():
    if not TRACKER_PATH.exists():
        return {}
    with open(TRACKER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tracker(data):
    with open(TRACKER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_skill(skill_name, status="STABLE", fail_inc=False, model="deepseek-v4.1-flash"):
    data = load_tracker()
    
    if skill_name not in data:
        data[skill_name] = {
            "last_stabilized": datetime.now().strftime("%Y-%m-%d"),
            "failure_count": 0,
            "model_version": model,
            "status": "STABLE"
        }

    if fail_inc:
        data[skill_name]["failure_count"] += 1
        if data[skill_name]["failure_count"] >= 3:
            data[skill_name]["status"] = "DEGRADED"
            print(f"⚠️ ALERT: Skill {skill_name} ha entrado en estado DEGRADED. Triggering REPAIR.")
    
    if status:
        data[skill_name]["status"] = status
        if status == "STABLE":
            data[skill_name]["last_stabilized"] = datetime.now().strftime("%Y-%m-%d")
            data[skill_name]["failure_count"] = 0

    save_tracker(data)
    print(f"✅ Tracker actualizado para {skill_name}: Status={data[skill_name]['status']}")

def check_obsolescence():
    data = load_tracker()
    today = datetime.now().strftime("%Y-%m-%d")
    suggestions = []
    
    for skill, info in data.items():
        # Simplificado: si la skill tiene más de 30 días, sugerir research
        # (En un sistema real compararíamos fechas)
        if info["status"] == "STABLE":
            suggestions.append(f"Sugerencia: {skill} podría beneficiarse de Autoresearch.")
            
    return suggestions

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 lifecycle_tracker.py <skill_name> [status] [fail_inc (1/0)]")
        sys.exit(1)

    name = sys.argv[1]
    stat = sys.argv[2] if len(sys.argv) > 2 else None
    f_inc = sys.argv[3] == "1" if len(sys.argv) > 3 else False
    
    update_skill(name, stat, f_inc)
