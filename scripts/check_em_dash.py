#!/usr/bin/env python3
"""check_em_dash.py - Detecta guiones largos (em dash U+2014 / en dash U+2013)
antes de publicar texto a GitHub. Regla de Gonzo: guion comun (-) SIEMPRE.

Uso:
  python3 scripts/check_em_dash.py <archivo|directorio>
  cat texto | python3 scripts/check_em_dash.py -

Exit 0 = limpio. Exit 1 = encontro guiones largos (imprime el contexto).
"""
import sys
import os

EM = "\u2014"  # em dash
EN = "\u2013"  # en dash


def check_text(text: str, label: str) -> int:
    lines = text.split("\n")
    found = 0
    for i, line in enumerate(lines, 1):
        for j, ch in enumerate(line):
            if ch == EM or ch == EN:
                name = "em dash U+2014" if ch == EM else "en dash U+2013"
                ctx = line[max(0, j - 30): j + 15]
                print(f"{name} en {label}:{i}: ...{ctx}...")
                found += 1
    return found


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "-":
        # stdin
        text = sys.stdin.read()
        found = check_text(text, "<stdin>")
    else:
        path = sys.argv[1]
        if os.path.isdir(path):
            found = 0
            for root, _dirs, files in os.walk(path):
                for f in files:
                    if not f.endswith((".md", ".txt", ".tsx", ".ts", ".mjs", ".js", ".json")):
                        continue
                    if "node_modules" in root:
                        continue
                    fp = os.path.join(root, f)
                    with open(fp, encoding="utf-8") as fh:
                        found += check_text(fh.read(), fp)
        elif os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                found = check_text(fh.read(), path)
        else:
            print(f"No existe: {path}")
            sys.exit(2)

    if found:
        print(f"\n!! Se encontraron {found} guiones largos. Regla de Gonzo: usar guion comun (-) SIEMPRE.")
        sys.exit(1)
    print("OK: sin guiones largos.")
    sys.exit(0)


if __name__ == "__main__":
    main()
