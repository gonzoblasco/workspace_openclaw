#!/usr/bin/env python3
"""
check-adr-integrity.py - Verifica que el corpus de ADRs y su indice esten reconciliados.

Por que existe: ADR-063 existia y estaba commiteado, pero no tenia fila en
docs/adr/README.md. Un ADR fuera del indice es un ADR que nadie encuentra, y
NADA lo detectaba: check-refs.py valida que las rutas citadas existan, no la
relacion inversa (que todo ADR este indexado). Se detecto leyendo, no con un
chequeo. Este script cierra ese hueco.

Que revisa:
  1. EN DISCO SIN INDICE    - un ADR que no se puede encontrar. (el caso ADR-063)
  2. LINK ROTO EN EL INDICE - una fila que promete un archivo que no esta.
  3. NUMERO DUPLICADO       - dos decisiones con una direccion: una cita
                              resuelve ambigua, que es peor que un hueco.
  4. REF CRUZADA ROTA       - el corpus cita un ADR-NNN que no existe.
  5. HUECOS DE NUMERACION   - informativo: no falla. Un hueco puede ser una
                              decision retirada a proposito; un duplicado nunca
                              es intencional.

Las rutas son inyectables (`adr_dir` como parametro) para que los tests puedan
construir un corpus falso en un directorio temporal. La version anterior del
chequeo se probaba modificando el README real y restaurandolo con git checkout:
si el test fallaba a mitad, dejaba el indice roto. Sembrar el defecto en un
corpus desechable verifica lo mismo sin arriesgar el real.

Uso:
    check-adr-integrity.py
Salida: exit 0 si esta reconciliado, 1 si hay defectos.
"""

import re
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
ADR_DIR = ROOT / "docs" / "adr"

# Archivo de ADR: ADR-063-kanam-insight-python-langchain.md
FILE_RE = re.compile(r"^ADR-(\d+)-.+\.md$")

# Fila del indice: | ADR-063 | [titulo](./ADR-063-archivo.md) | workspace |
ROW_RE = re.compile(r"^\|\s*ADR-(\d+)\s*\|\s*\[([^\]]*)\]\(([^)]+)\)")

# Cita de un ADR en cualquier parte del corpus.
CITE_RE = re.compile(r"ADR-(\d+)")


def disk_by_number(adr_dir: Path):
    """Numero -> nombres de archivo. Mas de uno = duplicado."""
    out = {}
    for p in sorted(adr_dir.glob("ADR-*.md")):
        m = FILE_RE.match(p.name)
        if m:
            out.setdefault(int(m.group(1)), []).append(p.name)
    return out


def index_by_number(index: Path):
    """Numero -> lista de (titulo, link) de las filas del indice."""
    out = {}
    if not index.exists():
        return out
    for line in index.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if m:
            out.setdefault(int(m.group(1)), []).append((m.group(2), m.group(3)))
    return out


def citations(adr_dir: Path):
    """(archivo, linea, numero) por cada cita ADR-NNN dentro del corpus."""
    out = []
    for p in sorted(adr_dir.glob("*.md")):
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for ln, line in enumerate(text.splitlines(), 1):
            for m in CITE_RE.finditer(line):
                out.append((p.name, ln, int(m.group(1))))
    return out


def find_defects(adr_dir: Path = ADR_DIR, index: Optional[Path] = None):
    """Devuelve la lista de defectos. Vacia = corpus reconciliado."""
    adr_dir = Path(adr_dir)
    index = Path(index) if index is not None else adr_dir / "README.md"

    errors = []
    disk = disk_by_number(adr_dir)
    idx = index_by_number(index)

    # 1. En disco sin fila en el indice.
    for num, files in sorted(disk.items()):
        if num not in idx:
            for f in files:
                errors.append(
                    f"EN DISCO SIN INDICE: {f} "
                    f"(falta la fila `| ADR-{num:03d} |` en el README)"
                )

    # 2. Fila del indice que promete un archivo inexistente.
    for num, rows in sorted(idx.items()):
        for _title, target in rows:
            if not (adr_dir / target.lstrip("./")).exists():
                errors.append(
                    f"LINK ROTO EN EL INDICE: ADR-{num:03d} -> {target} "
                    f"(la fila existe, el archivo no)"
                )

    # 3. Numero duplicado: dos decisiones con una direccion.
    for num, files in sorted(disk.items()):
        if len(files) > 1:
            errors.append(
                f"NUMERO DUPLICADO ADR-{num:03d}: {', '.join(files)} "
                f"(una cita resuelve ambiguo)"
            )

    # 4. Cita a un ADR que no existe. Se agrupa por numero: si falta, el dato
    # util es donde se lo cita. Las citas se leen una sola vez.
    cites = citations(adr_dir)
    for num in sorted({n for _f, _l, n in cites} - set(disk)):
        where = [f"{n}:{l}" for n, l, x in cites if x == num]
        errors.append(
            f"REF CRUZADA ROTA: se cita ADR-{num:03d} y no existe "
            f"({len(where)} cita/s: {', '.join(where[:3])}"
            f"{' ...' if len(where) > 3 else ''})"
        )

    return errors


def main(argv=None):
    """argv permite apuntar a otro corpus (uso: tests). Default: el real."""
    argv = sys.argv[1:] if argv is None else argv
    adr_dir = Path(argv[0]) if argv else ADR_DIR
    errors = find_defects(adr_dir)
    if errors:
        print(f"CORPUS DE ADRs DESRECONCILIADO ({len(errors)} defecto/s):")
        for e in errors:
            print(f"  {e}")
        print()
        print("El indice y el corpus son una sola cosa: si no coinciden, uno miente.")
        return 1

    disk = disk_by_number(adr_dir)
    nums = sorted(disk)
    if not nums:
        print("ERROR no hay ADRs en el corpus que revisar; no se pudo correr (exit 3)",
              file=sys.stderr)
        return 3
    print(f"OK: {len(nums)} ADRs, todos indexados, sin duplicados ni refs rotas.")
    gaps = [n for n in range(1, nums[-1] + 1) if n not in disk] if nums else []
    if gaps:
        # Informativo a proposito: un hueco puede ser una decision retirada.
        print(f"     Huecos de numeracion (informativo): {gaps}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
