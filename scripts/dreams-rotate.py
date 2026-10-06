#!/usr/bin/env python3
"""
dreams-rotate.py - Mantiene el Dream Diary (DREAMS.md) por mes; meses viejos
se archivan. El activo muestra solo el mes en curso.

POR QUE EXISTE (2026-10-06). `DREAMS.md` lo escribe `memory-core` (plugin de
dreaming) de forma append-only: una entrada por fase con material. Igual que el
CHANGELOG, crece sin techo. No hay knob de retencion nativo para el diary (el
doc solo expone `enabled`/`frequency`/`model`), asi que la rotacion es propia.

Que es seguro tocar: el doc de dreaming dice que el diary es "para lectura
humana, no una fuente de promocion". Solo se recorta la narracion vieja; los
marcadores del plugin y el bloque `Deep Sleep` quedan intactos. El plugin sigue
agregando entradas nuevas sin saber de esta rotacion.

MECANISMO
  DREAMS.md (activo)                       ->  entradas del mes en curso
  memory/archive/dreaming/DREAMS-YYYY-MM.md ->  los meses anteriores, por mes

  - Idempotente: correrlo dos veces no cambia nada la segunda.
  - Solo toca el contenido ENTRE los marcadores del diary
    (`openclaw:dreaming:diary:start/end`). El resto del archivo no se toca.
  - Una entrada sin fecha parseable NO se archiva: se deja en el activo.

Uso:
    dreams-rotate.py                rota (idempotente)
    dreams-rotate.py --check        exit 1 si hay meses viejos sin archivar
    dreams-rotate.py --dry-run      muestra que haria, sin escribir
    dreams-rotate.py --today YYYY-MM-DD   fecha de referencia (tests)
    dreams-rotate.py --root DIR     workspace raiz (tests)
Salida: 0 ok / 1 drift (solo --check) / 2 error.
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACTIVE = ROOT / "DREAMS.md"
ARCHIVE_DIR = ROOT / "memory" / "archive" / "dreaming"

DIARY_START = "<!-- openclaw:dreaming:diary:start -->"
DIARY_END = "<!-- openclaw:dreaming:diary:end -->"

MONTHS = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11,
    "December": 12,
}

# Cada entrada empieza con una linea tipo `*September 9, 2026 at 5:34 AM GMT-3*`.
ENTRY_ANCHOR = re.compile(r"(?=\n\*[A-Z][a-z]+ \d{1,2}, \d{4} at )")
ENTRY_DATE = re.compile(r"\*([A-Z][a-z]+) (\d{1,2}), (\d{4}) at ")


def entry_month(entry: str):
    """'YYYY-MM' de la entrada, o None si no tiene fecha parseable."""
    m = ENTRY_DATE.search(entry)
    if not m or m.group(1) not in MONTHS:
        return None
    return f"{int(m.group(3)):04d}-{MONTHS[m.group(1)]:02d}"


def split_diary(text: str):
    """(prefix, [entradas], suffix) alrededor de los marcadores del diary.

    prefix incluye el marcador de inicio; suffix incluye el de fin y todo lo
    que sigue (el bloque Deep Sleep). El contenido fuera de los marcadores no
    se altera.
    """
    s = text.find(DIARY_START)
    e = text.find(DIARY_END)
    if s == -1 or e == -1 or e < s:
        return None
    prefix = text[: s + len(DIARY_START)]
    body = text[s + len(DIARY_START): e]
    suffix = text[e:]
    parts = ENTRY_ANCHOR.split(body)
    # parts[0] es el separador/encabezado previo a la primera entrada (p.ej. "\n---\n").
    lead = parts[0]
    entries = [p for p in parts[1:] if p.strip()]
    return prefix, lead, entries, suffix


def plan(days: int, today: dt.date):
    """(active_text, {month: archive_text}, needs, n_active, n_archived).

    `days` no se usa: la unidad es el mes (se conserva el mes en curso).
    Se acepta por simetria con changelog-rotate; el corte es `today`'s month.
    """
    if not ACTIVE.exists():
        return None
    text = ACTIVE.read_text(encoding="utf-8")
    sp = split_diary(text)
    if sp is None:
        raise SystemExit("Error: DREAMS.md no tiene los marcadores del diary.")
    prefix, lead, entries, suffix = sp

    current = f"{today.year:04d}-{today.month:02d}"
    active, old = [], []
    for e in entries:
        em = entry_month(e)
        if em is None or em >= current:
            active.append(e)
        else:
            old.append(e)

    # Reconstruye el activo preservando el encabezado previo a la 1ra entrada.
    active_text = prefix + lead + "".join(active).rstrip() + "\n" + suffix.lstrip("\n")
    if not active:
        active_text = prefix + "\n" + suffix.lstrip("\n")

    # Agrupa los viejos por mes y arma el texto de cada archivo (append).
    by_month = {}
    for e in old:
        by_month.setdefault(entry_month(e), []).append(e)
    archives = {}
    for month, es in by_month.items():
        p = ARCHIVE_DIR / f"DREAMS-{month}.md"
        prev = p.read_text(encoding="utf-8") if p.exists() else None
        block = "".join(es).rstrip() + "\n"
        if prev is None:
            head = (
                f"# DREAMS (archivo) - {month}\n\n"
                "> Rotado desde `DREAMS.md` por `scripts/dreams-rotate.py`.\n\n---\n"
            )
            archives[month] = head + block
        else:
            archives[month] = prev.rstrip() + "\n" + block

    needs = bool(old)
    return active_text, archives, needs, len(active), len(old)


def main(argv):
    global ACTIVE, ARCHIVE_DIR
    p = argparse.ArgumentParser(description="Rota el Dream Diary por mes.")
    p.add_argument("--today", type=str, default=None, help="YYYY-MM-DD (tests)")
    p.add_argument("--root", type=str, default=None, help="workspace root (tests)")
    p.add_argument("--days", type=int, default=31, help="(sin efecto; simetria)")
    p.add_argument("--check", action="store_true", help="exit 1 si hay drift")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    if args.root:
        r = Path(args.root).resolve()
        ACTIVE = r / "DREAMS.md"
        ARCHIVE_DIR = r / "memory" / "archive" / "dreaming"

    try:
        today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    except ValueError:
        print("Error: --today no es una fecha YYYY-MM-DD valida.")
        return 2

    result = plan(args.days, today)
    if result is None:
        if args.check:
            print("OK: no hay DREAMS.md (nada que rotar).")
            return 0
        print("OK: no existe DREAMS.md.")
        return 0

    active_text, archives, needs, n_active, n_old = result

    if args.check:
        if needs:
            print(
                f"DREAMS DESFASADO: {n_old} entradas de meses anteriores siguen "
                "en el activo.\n"
                "  Rotar:   python3 scripts/dreams-rotate.py"
            )
            return 1
        print(f"OK: DREAMS en el mes en curso ({n_active} entradas activas).")
        return 0

    if args.dry_run:
        print(f"[dry-run] activas={n_active} a_archivar={n_old} rota={'si' if needs else 'no'}")
        return 0

    wrote = []
    if ACTIVE.read_text(encoding="utf-8") != active_text:
        ACTIVE.write_text(active_text, encoding="utf-8")
        wrote.append("activo")
    for month, text in archives.items():
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        dest = ARCHIVE_DIR / f"DREAMS-{month}.md"
        if (not dest.exists()) or dest.read_text(encoding="utf-8") != text:
            dest.write_text(text, encoding="utf-8")
            wrote.append(f"archivo:{month}")

    if wrote:
        print(f"DREAMS actualizado ({', '.join(wrote)}): {n_active} activas, "
              f"{n_old} archivadas.")
    else:
        print(f"OK: DREAMS ya en el mes en curso ({n_active} activas, {n_old} archivadas).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
