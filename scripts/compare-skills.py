#!/usr/bin/env python3
"""compare-skills.py - Compara el workspace (fuente) contra el repo publico (artefacto).

El publico esta SANITIZADO: por eso un `diff` crudo reporta diferencias falsas en
toda skill que mencionaba un dato personal o un proyecto interno. Este script aplica
la misma sanitizacion a la fuente EN MEMORIA y recien ahi compara.

Uso:
  python3 scripts/compare-skills.py <src-dir> <dst-dir> [skill ...]

Salida: una linea por skill que difiere de verdad. Exit 0 si no hay ninguna.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "san", str(Path(__file__).resolve().parent / "sanitize-skills.py")
)
san = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(san)

# Archivos que nunca se publican (deben coincidir con EXCLUDES del shell script).
SKIP_NAMES = {".DS_Store"}
SKIP_DIRS = {"__pycache__", "node_modules", ".venv", ".knowledge"}


def rel_files(root: Path):
    out = {}
    for f in root.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if f.name in SKIP_NAMES or f.suffix in {".pyc", ".db"}:
            continue
        out[rel] = f
    return out


def main() -> int:
    if len(sys.argv) < 3:
        print("Uso: compare-skills.py <src-dir> <dst-dir> [skill ...]", file=sys.stderr)
        return 1
    src_root, dst_root = Path(sys.argv[1]), Path(sys.argv[2])
    only = sys.argv[3:]

    names = only if only else sorted(
        d.name for d in dst_root.iterdir() if d.is_dir() and (src_root / d.name).is_dir()
    )

    differ = []
    for n in names:
        s, d = src_root / n, dst_root / n
        if not (s / "SKILL.md").is_file() or not d.is_dir():
            continue
        sf, df = rel_files(s), rel_files(d)

        # Archivos que faltan o sobran
        missing = sorted(str(r) for r in sf if r not in df)
        extra = sorted(str(r) for r in df if r not in sf)
        if missing or extra:
            differ.append((n, f"archivos: -{missing} +{extra}"))
            continue

        # Contenido: sanitizar la fuente antes de comparar
        for rel, fp in sorted(sf.items()):
            try:
                a = fp.read_text(encoding="utf-8")
                b = df[rel].read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # binario: comparacion directa
                if fp.read_bytes() != df[rel].read_bytes():
                    differ.append((n, f"binario distinto: {rel}"))
                continue
            clean, _ = san.sanitize(a)
            if clean != b:
                differ.append((n, f"contenido distinto: {rel}"))
                break

    for n, why in differ:
        print(f"  {n}: {why}")
    print(f"skills que difieren de verdad: {len(differ)}")
    return 0 if not differ else 2


if __name__ == "__main__":
    sys.exit(main())
