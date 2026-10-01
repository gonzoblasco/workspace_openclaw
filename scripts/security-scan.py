#!/usr/bin/env python3
import re
import sys
import os
from pathlib import Path

# Colores para la terminal
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Definición de patrones de riesgo
RISK_PATTERNS = {
    "HIGH": {
        "Shell Injection": [
            r"os\.system\(", r"subprocess\.Popen\(.*shell=True", r"eval\(", r"exec\("
        ],
        "Path Traversal": [
            r"\.\./\.\./", r"/etc/passwd", r"/etc/shadow", r"C:\\Windows\\"
        ],
        "Obfuscation": [
            r"base64\.b64decode\(", r"zlib\.decompress\(", r"getattr\(.*__"
        ],
        "Exfiltration": [
            r"requests\.post\(", r"curl\s+-X\s+POST", r"wget\s+--post-data"
        ]
    },
    "MEDIUM": {
        "Prompt Override": [
            r"ignore\s+previous\s+instructions", r"you\s+are\s+now\s+an\s+admin", 
            r"system\s+prompt\s+override", r"forget\s+everything\s+you\s+know"
        ],
        "Secret Leak": [
            r"api[_-]?key\s*=\s*['\"][a-zA-Z0-9]{20,}", 
            r"secret\s*=\s*['\"][a-zA-Z0-9]{20,}"
        ]
    }
}

def scan_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}", "WARN"

    findings = []
    overall_status = "PASS"

    for level, categories in RISK_PATTERNS.items():
        for category, patterns in categories.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    findings.append((level, category, pattern))
                    if level == "HIGH":
                        overall_status = "FAIL"
                    elif level == "MEDIUM" and overall_status == "PASS":
                        overall_status = "WARN"

    return findings, overall_status

def main():
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <archivo_o_directorio>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Error: El objetivo {target} no existe.")
        sys.exit(1)

    files_to_scan = []
    if target.is_file():
        files_to_scan.append(target)
    else:
        for root, _, files in os.walk(target):
            for file in files:
                if file.endswith(('.py', '.js', '.sh', '.yml', '.yaml', '.json', '.md')):
                    files_to_scan.append(Path(root) / file)

    print(f"🔎 Escaneando {len(files_to_scan)} archivos...\n")
    
    total_fails = 0
    
    for file in files_to_scan:
        findings, status = scan_file(file)
        
        if status == "PASS":
            continue
        
        color = RED if status == "FAIL" else YELLOW
        print(f"{color}[{status}]{RESET} {file}")
        
        if isinstance(findings, list):
            for level, cat, pat in findings:
                print(f"  - {level}: {cat} (patrón: {pat})")
        else:
            print(f"  - {findings}")
            
        if status == "FAIL":
            total_fails += 1

    print("\n" + "="*30)
    if total_fails > 0:
        print(f"{RED}RESULTADO: FAIL - Se encontraron {total_fails} archivos peligrosos.{RESET}")
        sys.exit(1)
    elif any(status == "WARN" for status in [scan_file(f)[1] for f in files_to_scan]):
        print(f"{YELLOW}RESULTADO: WARN - Se encontraron advertencias.{RESET}")
        sys.exit(0)
    else:
        print(f"{GREEN}RESULTADO: PASS - Todo limpio.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
