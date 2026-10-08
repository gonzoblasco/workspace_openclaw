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

# Extensiones que se escanean cuando el objetivo es un directorio.
SCAN_EXTS = ('.py', '.js', '.cjs', '.mjs', '.sh', '.yml', '.yaml', '.json', '.md')
# Extensiones de codigo ejecutable: el gate --staged solo mira estas. Un SKILL.md
# que cita "ignore previous instructions" como *documentacion* de un patron de
# seguridad es un falso positivo; un .sh/.py/.js que lo ejecuta, no.
CODE_EXTS = ('.py', '.js', '.cjs', '.mjs', '.sh')

# Definición de patrones de riesgo
RISK_PATTERNS = {
    "HIGH": {
        "Shell Injection": [
            r"os\.system\(",
            r"subprocess\.Popen\(.*shell=True",
            r"eval\(",
            # `exec(` a secas = el builtin de Python o un exec destructured de
            # child_process. El lookbehind descarta `.exec(` de JS, que es
            # `RegExp.prototype.exec` (un match de regex, no ejecuta nada).
            # Encontrado 2026-10-07: 4 archivos legitimos de las skills de
            # auditoria (color.js, tokens.js, comparator.js, enforcer.js)
            # quedaban bloqueados como "Shell Injection HIGH" por usar
            # `/patron/.exec(str)`.
            r"(?<!\.)\bexec\(",
            # `require('child_process').exec(...)` / `child_process.exec(...)`: el
            # modulo seguido del metodo. Se permiten pocos caracteres en medio
            # (los parentesis y la comilla del require). Un `.exec(` suelto sobre
            # un objeto desconocido es ambiguo y NO se marca: ahi esta el falso
            # positivo que este fix elimina.
            r"child_process[^\n]{0,8}\.exec\(",
            r"execSync\(",
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

def staged_code_files():
    """Archivos de codigo staged que viven bajo un arbol de skills.

    Es el caso real del gate: codigo de skills de afuera entrando al repo. El
    codigo propio del workspace (scripts/) NO se escanea aca: se auto-marca
    falsos positivos (security-scan.py cita /etc/passwd como patron, los
    triggers .js usan exec(, test-skills.sh navega ./../..). `git diff --cached`
    con -z separa por NUL (robusto a espacios).
    """
    import subprocess

    try:
        out = subprocess.run(
            ["git", "-C", str(Path(__file__).resolve().parent.parent),
             "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
            capture_output=True, text=True, check=False,
        ).stdout
    except Exception:
        return []
    files = []
    for rel in out.split("\0"):
        rel = rel.strip()
        if not rel or not rel.endswith(CODE_EXTS):
            continue
        if "/skills/" not in rel and not rel.startswith("skills/"):
            continue
        files.append(Path(__file__).resolve().parent.parent / rel)
    return files


def main():
    argv = sys.argv[1:]
    staged = "--staged" in argv
    argv = [a for a in argv if a != "--staged"]

    if staged:
        files_to_scan = staged_code_files()
        if not files_to_scan:
            print(f"{GREEN}RESULTADO: PASS - sin codigo de skills staged.{RESET}")
            return
        print(f"🔎 Escaneando {len(files_to_scan)} archivo(s) de skills staged...\n")
    else:
        if not argv:
            print(f"Uso: {sys.argv[0]} <archivo_o_directorio> | --staged")
            sys.exit(1)
        target = Path(argv[0])
        if not target.exists():
            print(f"Error: El objetivo {target} no existe.")
            sys.exit(1)
        files_to_scan = []
        if target.is_file():
            files_to_scan.append(target)
        else:
            for root, _, files in os.walk(target):
                for file in files:
                    if file.endswith(SCAN_EXTS):
                        files_to_scan.append(Path(root) / file)
        print(f"🔎 Escaneando {len(files_to_scan)} archivos...\n")

    total_fails = 0
    total_warns = 0

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
        elif status == "WARN":
            total_warns += 1

    print("\n" + "="*30)
    if total_fails > 0:
        print(f"{RED}RESULTADO: FAIL - {total_fails} archivo(s) peligroso(s).{RESET}")
        sys.exit(1)
    elif total_warns > 0:
        print(f"{YELLOW}RESULTADO: WARN - {total_warns} advertencia(s).{RESET}")
        sys.exit(0)
    else:
        print(f"{GREEN}RESULTADO: PASS - Todo limpio.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
