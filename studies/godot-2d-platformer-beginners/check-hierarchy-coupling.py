#!/usr/bin/env python3
"""Gate: ninguna referencia a otro nodo de la escena por profundidad fija.

Por que existe (curso Godot 2D platformer, 2026-11-11: Modulos 4, 7 y 8).
El curso resuelve la comunicacion entre nodos de dos maneras:

  (a) subiendo por la jerarquia una cantidad fija de padres
      (`get_parent().get_parent().get_node("CheckpointManager")`, 00:13:56)
  (b) bajando por nombre desde un nodo ya conocido
      (`runner.get_parent().get_node("World")`, `get_parent().get_node("Floor")`)

Ambas dependen de **la forma del arbol de escena**, no de un contrato. Mover ese nodo
un nivel arriba, renombrarlo o empaquetarlo en una escena propia no da error de
compilacion: da un error en runtime, y solo cuando se ejecuta esa rama. El modulo 4
del curso lo muestra en vivo con `get_parent().get_parent()`; el proyecto
`reinos-de-la-frontera` ya tiene el mismo patron en `view/hud.gd`, `view/overlay.gd`
y `view/world_view.gd`.

Uso:
    python3 studies/godot-2d-platformer-beginners/check-hierarchy-coupling.py projects/reinos-de-la-frontera

Reglas:
  1. `get_parent().get_parent()...` (dos o mas `get_parent()` encadenados) siempre
     falla: es la referencia por profundidad fija.
  2. `get_parent().get_node(...)` / `get_parent().get_node_or_null(...)` tambien
     falla: depende de que el hermano siga llamandose igual y siga siendo hermano.
  3. `get_parent()` solo (una llamada, sin `get_node`) no falla: es el caso del nodo
     que pide su contenedor directo, que es estable por construccion.
  4. Se excluyen `tests/` (el test arma su propia escena y conoce la forma a proposito)
     y los directorios ignorados.

Exit 0 si esta limpio, 1 si hay referencias por jerarquia.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

IGNORED_DIRS = {".git", "build", "dist", "node_modules", "__pycache__", "tests", "spike"}

CHAIN = re.compile(r"(get_parent\(\)\s*\.\s*){2,}")
SIBLING = re.compile(r"get_parent\(\)\s*\.\s*get_node(?:_or_null)?\s*\(")


def scan(root: Path) -> list[tuple[Path, int, str, str]]:
    hits: list[tuple[Path, int, str, str]] = []
    for path in sorted(root.rglob("*.gd")):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1
        ):
            code = line.split("#", 1)[0]
            if CHAIN.search(code):
                hits.append((path, lineno, "CHAIN", line.strip()))
            elif SIBLING.search(code):
                hits.append((path, lineno, "SIBLING", line.strip()))
    return hits


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = Path(argv[1]).resolve()
    if not root.is_dir():
        print(f"FAIL: no existe el directorio {root}")
        return 2

    hits = scan(root)
    if not hits:
        print(f"OK: sin referencias por jerarquia en {root}")
        return 0

    print(f"FAIL: {len(hits)} referencia(s) por jerarquia en {root}")
    for path, lineno, kind, code in hits:
        rel = path.relative_to(root)
        why = (
            "cadena de get_parent() (profundidad fija)"
            if kind == "CHAIN"
            else "get_parent() + get_node (depende del nombre y del hermano)"
        )
        print(f"  - {rel}:{lineno}  [{why}]")
        print(f"      {code}")
    print()
    print("Arreglo: sacar el nodo de la busqueda por jerarquia.")
    print("  - preferir una senal emitida por el hijo y conectada desde el padre")
    print("  - o un `@export var` / `NodePath` exportado, asignado en el editor")
    print("  - o un autoload con el dato compartido (puntaje, checkpoint, estado)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
