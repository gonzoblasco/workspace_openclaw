#!/usr/bin/env python3
"""
check-content-dirs.py - Verifica que los directorios de CONTENIDO de primer nivel
sigan existiendo.

POR QUE EXISTE (2026-09-30). El commit `dfa94759` ("cleanup: remove studies, tmp
dirs") del 2026-09-28 borro TODO `studies/` - 5 archivos, un estudio cerrado dos
dias antes - y se pusheo a `origin/main`. NINGUNA guarda lo vio:

  - `check-refs.py` verifica que las rutas CITADAS en docs existan. Un directorio
    borrado en bloque no rompe ninguna cita: las citas viven en el commit
    anterior, que ya no se escanea.
  - `check-adr-integrity.py` cubre `docs/adr/`. Los directorios de contenido
    (`studies/`, `design/`, `prompts/`) quedaron sin cobertura.
  - El resultado no fue un error: fue silencio. El estudio estuvo dos dias
    borrado de `origin/main` y lo detecto la observacion de Gonzo ("no hay commit
    ni nada nuevo"), no el sistema.

Una guarda que verifica REFERENCIAS no es una guarda que verifica EXISTENCIA. Es
el mismo falso verde que el skip de links a directorio (learning 223): la guarda
cubria la forma, no la clase. Un `git rm -r` de una carpeta entera no deja rastro
- no hay ruta citada rota, no hay ADR desindexado.

Que revisa: cada directorio de CONTENIDO de primer nivel existe en disco.

La lista es EXPLICITA y no derivada, igual que SDD_CYCLE en
check-agent-skill-boundary.py. Deliberado: el check existe para atrapar un
borrado, y derivar la lista de "lo que hay en disco" lo dejaria siempre verde.

No cubre `sandbox/` (gitignored, 0 archivos trackeados: su ausencia es correcta)
ni los directorios de configuracion (`.github`, `.knowledge`, `.openclaw`), que
son del tooling y tienen sus propios contratos.

La raiz es inyectable (`root` como parametro) para que los tests construyan
arboles falsos en un directorio temporal, y para poder probar la clase (un
directorio que desaparece) sin tocar el workspace real.

Uso:
    check-content-dirs.py
Salida: exit 0 si todos los directorios existen, 1 si falta alguno.
"""

import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent

# Directorios de contenido de primer nivel. Contenido = trabajo que vive en el
# repo y no es configuracion del tooling. La lista esta explicita a proposito
# (ver el docstring): una lista derivada se auto-confirma.
CONTENT_DIRS: Tuple[str, ...] = (
    "agents",
    "design",
    "docs",
    "media",
    "memory",
    "prompts",
    "scripts",
    "skills",
    "studies",
    "tests",
)


def find_violations(root: Path) -> List[str]:
    """Devuelve los directorios de contenido que faltan, listos para imprimir."""
    violations: List[str] = []
    for name in CONTENT_DIRS:
        path = root / name
        if not path.is_dir():
            violations.append(
                "content directory missing: %s/ - this directory holds tracked "
                "content. If it was deleted on purpose, remove it from "
                "CONTENT_DIRS in the same change." % name
            )
    return violations


def main() -> int:
    violations = find_violations(ROOT)
    if violations:
        print("DIRECTORIOS DE CONTENIDO FALTANTES:")
        for v in violations:
            print(f"  {v}")
        print()
        print("Un directorio de contenido que desaparece no rompe ninguna cita:")
        print("solo deja de estar. Si el borrado es deliberado, sacarlo de la")
        print("lista en el mismo commit.")
        return 1

    # Una lista vacía no es verde: el check no revisó nada.
    if not CONTENT_DIRS:
        print("ERROR la lista de directorios de contenido está vacía; no se pudo correr "
              "(exit 3)", file=sys.stderr)
        return 3
    print(f"OK: {len(CONTENT_DIRS)} directorios de contenido, todos existen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
