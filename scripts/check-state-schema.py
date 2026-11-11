#!/usr/bin/env python3
"""Gate: todo key que un nodo escribe en el estado tiene que estar declarado.

Por que existe (curso LangGraph, 2026-11-11: Modulo 4 y Modulo 10).
El curso repite dos veces lo mismo: el estado es un `TypedDict`, y **una clave que
no se pasa ni se declara queda en `None`** — LangGraph no valida nada en runtime.
Un nodo que hace `state["clave_nueva"] = ...` con una clave fuera del esquema no
falla: escribe un dato que el checkpointer guarda, que el siguiente nodo puede no
ver, y que ningun tipo documenta. El error aparece semanas despues cuando alguien
lee el estado esperando solo las claves del esquema.

Uso:
    python3 scripts/check-state-schema.py projects/oss-post-graph

Reglas:
  1. Toda clave escrita como `state["k"]` en `src/**.py` debe estar declarada en el
     `TypedDict` de estado (se autodetecta el archivo: el que define `class *State(TypedDict`).
  2. Se excluyen los accesos de un solo nodo si el archivo declara `ALLOWED_UNDECLARED`
     (escape hatch explicito, para no bloquear un refactor en curso).

Exit 0 si esta limpio, 1 si hay claves sin declarar.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

IGNORED_DIRS = {"venv", ".venv", "node_modules", "__pycache__", ".git", "build", "dist"}


def find_state_module(root: Path) -> Path | None:
    """Primer archivo que define `class X(TypedDict...)` bajo src/."""
    for path in sorted((root / "src").rglob("*.py")):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"class\s+\w+State\s*\(TypedDict", text):
            return path
    return None


def declared_keys(state_file: Path) -> set[str]:
    tree = ast.parse(state_file.read_text(encoding="utf-8"))
    keys: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.bases:
            base = ast.unparse(node.bases[0])
            if "TypedDict" in base:
                for stmt in node.body:
                    if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                        keys.add(stmt.target.id)
    return keys


def written_keys(py_file: Path) -> set[str]:
    """Claves escritas como `state["k"] = ...` (no las leidas)."""
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    keys: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == "state"
                and isinstance(target.slice, ast.Constant)
                and isinstance(target.slice.value, str)
            ):
                keys.add(target.slice.value)
    return keys


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1]).resolve()
    state_file = find_state_module(root)
    if state_file is None:
        print(f"FALLA: no encontre un TypedDict de estado bajo {root}/src")
        return 1
    declared = declared_keys(state_file)

    offenders: dict[str, set[str]] = {}
    for path in sorted((root / "src").rglob("*.py")):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path == state_file:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "ALLOWED_UNDECLARED" in text:
            continue
        extra = written_keys(path) - declared
        if extra:
            offenders[str(path.relative_to(root))] = extra

    if not offenders:
        print(f"OK: {len(declared)} claves declaradas, ninguna clave sin declarar.")
        return 0

    total = sum(len(v) for v in offenders.values())
    print(f"FALLA: {total} clave(s) escrita(s) sin declarar en {state_file.name}:")
    for path, keys in offenders.items():
        print(f"\n  {path}")
        for key in sorted(keys):
            print(f"    - {key!r}  <- `state[{key!r}] = ...` sin estar en el TypedDict")
    print(
        "\nArreglo: agregar la clave al TypedDict de estado, o declararla en"
        "\nALLOWED_UNDECLARED si es transitoria y documentada."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
