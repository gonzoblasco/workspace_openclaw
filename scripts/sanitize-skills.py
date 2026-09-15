#!/usr/bin/env python3
"""sanitize-skills.py - Sanitiza una copia publica de skills, in place.

Separa lo que SALE de lo que SE QUEDA (ver docs/AGENTS-DETALLE.md):

  SALE (se reemplaza por texto generico):
    - datos personales: Gonzo, Gonzalo, @gonzoblasco, /Users/gonzoblasco/
    - proyectos internos: a11y-fixer, workspace_openclaw, soporteml, kanam-lab, ...

  SE QUEDA (no se toca):
    - la marca Kanam (nombre del PRODUCTO publicado, no una identidad personal)
    - la identidad de instalacion del repo: gonzoblasco/kanam-skills (README, docs, web)

Uso:
  python3 scripts/sanitize-skills.py <dir> [--check]

  --check  solo reporta, no escribe.

Exit: 0 ok | 2 quedan referencias personales o de proyectos internos.
"""
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".sh", ".py", ".json", ".yml", ".yaml", ".txt", ".toml", ".mjs", ".js", ".ts", ".tsx"}

# Identidad de instalacion del repo: excepcion legitima, nunca se toca.
PROTECTED = "gonzoblasco/kanam-skills"
PLACEHOLDER = "\x00REPO_IDENTITY\x00"

# --- personal -----------------------------------------------------------------
PERSONAL = [
    (re.compile(r"\bGonzo\b"), "the user"),
    (re.compile(r"\bGonzalo\b"), "the user"),
    (re.compile(r"@gonzoblasco"), "@user"),
    (re.compile(r"/Users/gonzoblasco/"), "/Users/user/"),
    # Handle desnudo en URLs: github.com/gonzoblasco/<repo> (kanam-skills ya esta
    # protegido por PROTECTED, que corre antes).
    (re.compile(r"gonzoblasco/([A-Za-z0-9._-]+)"), r"user/\1"),
    (re.compile(r"\bgonzoblasco\b"), "user"),
]

# --- proyectos internos (nunca se nombran en el publico) ----------------------
# OJO: kanam-skills NO va aca (es la identidad del repo publicado).
INTERNAL = [
    (re.compile(r"\ba11y-fixer\b"), "a project"),
    (re.compile(r"\ba11y-playground\b"), "a project"),
    (re.compile(r"\bworkspace_openclaw\b"), "the workspace repo"),
    (re.compile(r"\bprojects_openclaw\b"), "the aggregate repo"),
    (re.compile(r"\bsoporteml(?:-v[0-9])?\b"), "a project"),
    (re.compile(r"\bkanam-lab\b"), "a project"),
    (re.compile(r"\bkanam-pulse\b"), "a project"),
    (re.compile(r"\bkanam-story\b"), "a project"),
    (re.compile(r"\bkanam-studio\b"), "a project"),
    (re.compile(r"\bkanam-forge\b"), "a project"),
    (re.compile(r"\bkanam-insight\b"), "a project"),
    (re.compile(r"\bkanam-tetris\b"), "a project"),
    (re.compile(r"\bkanam-solitaires\b"), "a project"),
    (re.compile(r"\bkanam-mind\b"), "a project"),
    (re.compile(r"\bensulugar\b"), "a project"),
    (re.compile(r"\bultimo-turno\b"), "a novel"),
]

PERSONAL_DETECT = re.compile(r"\bGonzo\b|\bGonzalo\b|gonzoblasco|/Users/gonzoblasco")
INTERNAL_DETECT = re.compile(
    r"\ba11y-fixer\b|\ba11y-playground\b|\bworkspace_openclaw\b|\bprojects_openclaw\b|"
    r"\bsoporteml(?:-v[0-9])?\b|\bkanam-(?!skills\b)(?:lab|pulse|story|studio|forge|insight|tetris|solitaires|mind)\b|"
    r"\bensulugar\b|\bultimo-turno\b"
)


def sanitize(text: str) -> tuple[str, int]:
    """Devuelve (texto_limpio, cantidad_de_reemplazos)."""
    original = text
    text = text.replace(PROTECTED, PLACEHOLDER)
    n = 0
    for rx, repl in PERSONAL + INTERNAL:
        text, k = rx.subn(repl, text)
        n += k
    text = text.replace(PLACEHOLDER, PROTECTED)
    return text, (0 if text == original else n)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    if not args:
        print("Uso: sanitize-skills.py <dir> [--check]", file=sys.stderr)
        return 1
    root = Path(args[0])
    if not root.is_dir():
        print(f"No existe el directorio: {root}", file=sys.stderr)
        return 1

    changed = 0
    total = 0
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        clean, n = sanitize(text)
        if n == 0:
            continue
        total += n
        changed += 1
        if check:
            print(f"  se sanitizaria: {f.relative_to(root)} ({n})")
        else:
            f.write_text(clean, encoding="utf-8")
            print(f"  sanitizado: {f.relative_to(root)} ({n})")

    mode = "se sanitizarian" if check else "sanitizados"
    print(f"  archivos {mode}: {changed} | reemplazos: {total}")

    # Verificacion final sobre el arbol completo
    p = i = 0
    for f in root.rglob("*"):
        if not f.is_file() or f.suffix not in TEXT_SUFFIXES:
            continue
        try:
            t = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        t = t.replace(PROTECTED, "")
        p += len(PERSONAL_DETECT.findall(t))
        i += len(INTERNAL_DETECT.findall(t))
    print(f"  restantes -> personales: {p} | proyectos internos: {i}")
    return 2 if (p or i) else 0


if __name__ == "__main__":
    sys.exit(main())
