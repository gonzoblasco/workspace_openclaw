#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime

# Configuración
BASELINE_PATH = Path("/Users/gonzoblasco/.openclaw/workspace/.knowledge/quality_baseline.json")
S_LOWER_BOUND = 13 # Umbral de mediocridad
DELTA_WARN = 3
DELTA_FAIL = 6

def load_baseline():
    if not BASELINE_PATH.exists():
        return {}
    with open(BASELINE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_baseline(data):
    with open(BASELINE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def calculate_score(scores_dict):
    return sum(scores_dict.values())

def check_regression(component_name, current_scores):
    baseline = load_baseline()
    
    if component_name not in baseline:
        print(f"ℹ️  {component_name}: Sin baseline previo. Estableciendo nueva base.")
        save_baseline({**baseline, component_name: current_scores})
        return "NEW_BASELINE", 0

    prev_scores = baseline[component_name]
    prev_total = calculate_score(prev_scores)
    curr_total = calculate_score(current_scores)
    delta = prev_total - curr_total
    
    print(f"📊 {component_name}: {prev_total} $\rightarrow$ {curr_total} (Delta: {delta})")

    if delta <= 0:
        # Mejora o estabilidad
        save_baseline({**baseline, component_name: current_scores})
        return "PASS", delta
    elif delta < DELTA_WARN:
        return "PASS", delta
    elif delta < DELTA_FAIL:
        return "WARN", delta
    else:
        return "FAIL", delta

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 regression_gate.py <componente> <s,h,a,r,p>")
        print("Ejemplo: python3 regression_gate.py 'design-system' '5,4,5,3,5'")
        sys.exit(1)

    comp = sys.argv[1]
    try:
        scores = dict(zip(['s','h','a','r','p'], map(int, sys.argv[2].split(','))))
    except ValueError:
        print("Error: Los scores deben ser 5 enteros separados por coma.")
        sys.exit(1)

    status, delta = check_regression(comp, scores)
    
    if status == "FAIL":
        print(f"\n❌ REGRESSION DETECTED: {comp} ha caído {delta} puntos.")
        print("Bloqueo de integración activado. Requiere revisión manual.")
        sys.exit(1)
    elif status == "WARN":
        print(f"\n⚠️ QUALITY ALERT: {comp} ha caído {delta} puntos.")
        print("Integración permitida, pero se debe registrar deuda técnica.")
    else:
        print(f"\n✅ QUALITY CHECK: {comp} es estable o ha mejorado.")
```
