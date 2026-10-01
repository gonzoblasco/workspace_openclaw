#!/usr/bin/env python3
import yaml
import sys
import subprocess
from pathlib import Path

# Colores
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def run_skill(skill_cmd, input_text):
    """Ejecuta la skill pasando el input y captura el output."""
    try:
        # Asumimos que la skill es un script ejecutable que recibe input por stdin o arg
        result = subprocess.run(
            skill_cmd, 
            input=input_text, 
            text=True, 
            capture_output=True, 
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

def evaluate_skill(eval_file):
    with open(eval_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    skill_name = config["skill"]
    # Intentamos localizar el ejecutable de la skill (simplificado: buscamos en scripts/)
    skill_cmd = ["python3", f"scripts/{skill_name}.py"]
    
    print(f"🧪 Evaluando skill: {skill_name}...")
    
    overall_status = "PASS"
    results = []

    for ass in config["assertions"]:
        print(f"  Running {ass['id']} ({ass['description']})...", end=" ")
        
        actual = run_skill(skill_cmd, ass["input"])
        
        # Verificación de Esperados (contiene)
        passes_expected = ass["expected"] in actual if ass.get("expected") else True
        # Verificación de Prohibidos (NO contiene)
        passes_forbidden = all(f not in actual for f in ass.get("forbidden", []))

        if passes_expected and passes_forbidden:
            print(f"{GREEN}PASS{RESET}")
            results.append(("PASS", ass["id"]))
        else:
            status = "FAIL_CRITICAL" if ass.get("critical") else "FAIL_SOFT"
            print(f"{RED}{status}{RESET}")
            results.append((status, ass["id"]))
            if status == "FAIL_CRITICAL":
                overall_status = "FAIL"
            elif overall_status == "PASS":
                overall_status = "WARN"

    return overall_status, results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 eval-engine.py <archivo_eval.yaml>")
        sys.exit(1)

    eval_path = Path(sys.argv[1])
    if not eval_path.exists():
        print(f"Error: {eval_path} no existe.")
        sys.exit(1)

    status, res = evaluate_skill(eval_path)
    
    print("\n" + "="*30)
    if status == "FAIL":
        print(f"{RED}RESULTADO FINAL: FAIL - La skill no es estable.{RESET}")
        sys.exit(1)
    elif status == "WARN":
        print(f"{YELLOW}RESULTADO FINAL: WARN - La skill es funcional pero tiene fallos no críticos.{RESET}")
        sys.exit(0)
    else:
        print(f"{GREEN}RESULTADO FINAL: PASS - La skill está estabilizada.{RESET}")
        sys.exit(0)
