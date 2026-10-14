#!/usr/bin/env python3
"""
changelog-rotate.py - Mantiene el CHANGELOG.md del workspace en una ventana
activa de N dias; lo mas viejo se archiva. Nunca queda desfasado.

POR QUE EXISTE (2026-10-06). El CHANGELOG crecia sin control (310 KB, 2829
lineas, desde julio) y se volvio ilegible. La primera poda se hizo a mano; este
script la automatiza para que no dependa de que alguien se acuerde. El objetivo
no es el tamano por el tamano: es que el archivo activo muestre SOLO el ultimo
mes, y que la historia viva en su archivo sin perderse.

MECANISMO
  CHANGELOG.md (activo)  ->  entradas de los ultimos N dias (default 30)
  docs/archive/CHANGELOG-archive.md  ->  todo lo anterior, acumulado

  - Idempotente: correrlo dos veces no cambia nada la segunda.
  - El header del activo lo regenera el script (corte vigente + link al archivo):
    nadie lo edita a mano.
  - Las entradas se ordenan por fecha descendente, estable (las de la misma
    fecha conservan su orden relativo).

ENFORCEMENT
  - `--check` (lo corre el pre-commit cuando CHANGELOG.md esta staged): exit 1
    si hay entradas fuera de la ventana, para que la rotacion no se olvide.
  - El cierre de sesion (session-end.sh) lo corre sin flags: rota solo.

Uso:
    changelog-rotate.py                 rota (idempotente)
    changelog-rotate.py --check         exit 1 si hay drift (hay que rotar)
    changelog-rotate.py --dry-run       muestra que haria, sin escribir
    changelog-rotate.py --days N        ventana en dias (default 30)
    changelog-rotate.py --today YYYY-MM-DD   fecha de referencia (tests)
Salida: 0 ok / 1 drift (solo --check) / 2 error de uso.
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACTIVE = ROOT / "docs" / "CHANGELOG.md"
ARCHIVE = ROOT / "docs" / "archive" / "CHANGELOG-archive.md"

DEFAULT_DAYS = 14
# `## [YYYY-MM-DD] - Titulo`. El ancla es el header con fecha entre corchetes.
ENTRY = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\]")

ARCHIVE_LINK = "./docs/archive/CHANGELOG-archive.md"


def split_entries(text: str):
    """(header, [(fecha, bloque)]) a partir del texto del archivo.

    `header` es todo lo anterior a la primera entrada. Un bloque incluye su
    header y corre hasta el proximo (o EOF). El orden es el del archivo.
    """
    lines = text.splitlines(keepends=True)
    starts = [i for i, ln in enumerate(lines) if ENTRY.match(ln)]
    if not starts:
        return text, []
    header = "".join(lines[: starts[0]])
    entries = []
    for n, i in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        block = "".join(lines[i:end])
        # Normaliza a un solo newline final para que el dedupe sea estable.
        entries.append((ENTRY.match(lines[i]).group(1), block.rstrip() + "\n"))
    return header, entries


def active_header(days: int, cutoff: str) -> str:
    return (
        "# CHANGELOG.md\n\n"
        "Registro de cambios estructurales del workspace. Contiene las entradas "
        f"de los **últimos {days} días** (corte: {cutoff}). Lo anterior está "
        f"archivado en [`{ARCHIVE_LINK}`]({ARCHIVE_LINK}). No incluye actividad "
        "diaria (ver `memory/`).\n\n"
        "> **Política de rotación:** la mantiene `scripts/changelog-rotate.py` "
        "(pre-commit `--check` + cierre de sesión). Al superar la ventana, el "
        "bloque viejo se mueve al archivo. Reconstruir el activo desde cero "
        "cuando arrastre hipótesis refutadas.\n\n---\n\n"
    )


def archive_header() -> str:
    return (
        "# CHANGELOG (archivo) - historia rotada\n\n"
        "> Rotado desde `CHANGELOG.md`. Contiene la historia anterior al corte "
        "vigente. Mantenido por `scripts/changelog-rotate.py`. Orden: más "
        "reciente primero, igual que el activo.\n\n---\n\n"
    )


def sort_desc(entries):
    """Fecha descendente, estable: mismo dia conserva el orden de origen."""
    return sorted(entries, key=lambda e: e[0], reverse=True)


def dedupe(entries):
    """Sin entradas repetidas (por bloque exacto), preservando el orden dado."""
    seen = set()
    out = []
    for date, block in entries:
        if block not in seen:
            seen.add(block)
            out.append((date, block))
    return out


def plan(days: int, today: dt.date):
    """(active_text, archive_text, needs_rotation, n_active, n_archived)."""
    if not ACTIVE.exists():
        raise SystemExit("Error: no existe CHANGELOG.md")

    cutoff = (today - dt.timedelta(days=days)).isoformat()
    _, entries = split_entries(ACTIVE.read_text(encoding="utf-8"))

    active = sort_desc([e for e in entries if e[0] >= cutoff])
    rotated = [e for e in entries if e[0] < cutoff]

    # El archivo acumula: lo que ya tenia + lo recien rotado, sin duplicar.
    if ARCHIVE.exists():
        _, prev = split_entries(ARCHIVE.read_text(encoding="utf-8"))
    else:
        prev = []
    archive = sort_desc(dedupe(prev + rotated))

    active_text = active_header(days, cutoff) + "\n".join(b for _, b in active).rstrip() + "\n"
    archive_text = archive_header() + "\n".join(b for _, b in archive).rstrip() + "\n"
    needs = bool(rotated) and any(
        b not in {ab for _, ab in prev} for _, b in rotated
    )
    return active_text, archive_text, needs, len(active), len(archive)


def main(argv):
    global ACTIVE, ARCHIVE
    p = argparse.ArgumentParser(description="Rota el CHANGELOG a una ventana activa.")
    p.add_argument("--days", type=int, default=DEFAULT_DAYS)
    p.add_argument("--today", type=str, default=None, help="YYYY-MM-DD (tests)")
    p.add_argument("--root", type=str, default=None, help="workspace root (tests)")
    p.add_argument("--check", action="store_true", help="exit 1 si hay drift")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    if args.root:
        r = Path(args.root).resolve()
        ACTIVE = r / "docs" / "CHANGELOG.md"
        ARCHIVE = r / "docs" / "archive" / "CHANGELOG-archive.md"

    try:
        today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    except ValueError:
        print("Error: --today no es una fecha YYYY-MM-DD valida.")
        return 2
    if args.days < 0:
        print("Error: --days no puede ser negativo.")
        return 2

    active_text, archive_text, needs, n_active, n_archived = plan(args.days, today)
    cutoff = (today - dt.timedelta(days=args.days)).isoformat()

    if args.check:
        if needs:
            print(
                f"CHANGELOG DESFASADO: hay entradas anteriores a {cutoff} "
                f"fuera de la ventana de {args.days} dias.\n"
                "  Rotar:   python3 scripts/changelog-rotate.py\n"
                "  (el cierre de sesion tambien lo hace solo)"
            )
            return 1
        print(f"OK: CHANGELOG en ventana ({args.days} dias, corte {cutoff}; "
              f"{n_active} activas, {n_archived} archivadas).")
        return 0

    if args.dry_run:
        print(f"[dry-run] ventana={args.days}d corte={cutoff} "
              f"activas={n_active} archivadas={n_archived} rota={'si' if needs else 'no'}")
        return 0

    # Canonicaliza: escribir solo si el contenido difiere. Esto normaliza el
    # header aunque no haya nada que rotar (self-heal), y mantiene la
    # idempotencia (segunda corrida: sin diff).
    wrote = []
    if ACTIVE.read_text(encoding="utf-8") != active_text:
        ACTIVE.write_text(active_text, encoding="utf-8")
        wrote.append("activo")
    if (not ARCHIVE.exists()) or (ARCHIVE.read_text(encoding="utf-8") != archive_text):
        ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
        ARCHIVE.write_text(archive_text, encoding="utf-8")
        wrote.append("archivo")

    if wrote:
        print(f"CHANGELOG actualizado ({', '.join(wrote)}): {n_active} activas, "
              f"{n_archived} archivadas (corte {cutoff}).")
    else:
        print(f"OK: CHANGELOG ya en ventana ({n_active} activas, {n_archived} archivadas).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
