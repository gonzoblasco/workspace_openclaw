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
  DREAMS.md (activo)                        ->  entradas del mes en curso
  memory/archive/dreaming/DREAMS-YYYY-MM.md ->  los meses anteriores, por mes

  Cada AGENTE tiene su propio diario (`agents/<nombre>/DREAMS.md`) y archiva en
  su propio directorio hermano:
  agents/<nombre>/DREAMS.md
    ->  memory/archive/dreaming/agents/<nombre>/DREAMS-YYYY-MM.md

  El script ENUMERA las instancias (raiz + agents/*/) y aplica la misma
  politica a todas. Verificado 2026-11-18: existian 8 diarios, de los cuales 4
  (dev, critic, auditor, mind) conservaban meses viejos y el `--check` daba
  verde porque solo miraba el de la raiz. Un gate que cubre una instancia de un
  doc que ahora existe N veces es un gate verde sobre archivos que crecen solos:
  al agregar un agente, su diario entra en la rotacion sin tocar el script.

  - Idempotente: correrlo dos veces no cambia nada la segunda.
  - Solo toca el contenido ENTRE los marcadores del diary
    (`openclaw:dreaming:diary:start/end`). El resto del archivo no se toca.
  - Una entrada sin fecha parseable NO se archiva: se deja en el activo.
  - Un archivo sin marcadores se reporta y se saltea (no se destruye nada):
    exit 2 si ninguno tiene marcadores, aviso al stderr si es uno de varios
    (ese archivo queda FUERA de la rotacion: el `--check` no lo ve).
  - Orden seguro: primero se persiste el archivo y recien despues se reescribe
    el activo, con escritura atomica (tmp + os.replace). Un fallo de I/O deja
    el activo intacto y no pierde entradas; ese error reporta exit 2.

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
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_DIRNAME = Path("memory") / "archive" / "dreaming"

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


class NoMarkers(Exception):
    """El archivo no tiene los marcadores del diary: no se puede rotar."""


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


def instances(root: Path):
    """[(activo, dir_archivo, etiqueta)] de cada DREAMS.md que existe.

    Enumera en vez de asumir: el plugin crea el diario de cada agente y un
    rotador que solo mira la raiz deja los demas creciendo en silencio.
    """
    found = []
    root_active = root / "DREAMS.md"
    if root_active.exists():
        found.append((root_active, root / ARCHIVE_DIRNAME, ""))
    agents = root / "agents"
    if agents.is_dir():
        for d in sorted(agents.iterdir()):
            active = d / "DREAMS.md"
            if d.is_dir() and active.exists():
                found.append(
                    (active, root / ARCHIVE_DIRNAME / "agents" / d.name, d.name)
                )
    return found


def plan_one(active: Path, archive_dir: Path, today: dt.date):
    """(active_text, {month: archive_text}, needs, n_active, n_archived)."""
    if not active.exists():
        return None
    text = active.read_text(encoding="utf-8")
    sp = split_diary(text)
    if sp is None:
        raise NoMarkers(str(active))
    prefix, lead, entries, suffix = sp

    current = f"{today.year:04d}-{today.month:02d}"
    kept, old = [], []
    for e in entries:
        em = entry_month(e)
        if em is None or em >= current:
            kept.append(e)
        else:
            old.append(e)

    # Reconstruye el activo preservando el encabezado previo a la 1ra entrada.
    active_text = prefix + lead + "".join(kept).rstrip() + "\n" + suffix.lstrip("\n")
    if not kept:
        active_text = prefix + "\n" + suffix.lstrip("\n")

    # Agrupa los viejos por mes y arma el texto de cada archivo (append).
    by_month = {}
    for e in old:
        by_month.setdefault(entry_month(e), []).append(e)
    archives = {}
    for month, es in by_month.items():
        p = archive_dir / f"DREAMS-{month}.md"
        prev = p.read_text(encoding="utf-8") if p.exists() else None
        block = "".join(es).rstrip() + "\n"
        if prev is None:
            head = (
                f"# DREAMS (archivo) - {month}\n\n"
                f"> Rotado desde `{active.name}` por `scripts/dreams-rotate.py`.\n\n---\n"
            )
            archives[month] = head + block
        elif block.strip() and block.strip() in prev:
            # Ya archivado (p.ej. una corrida anterior archivo bien y murio antes
            # de reescribir el activo): no duplicar el bloque.
            archives[month] = prev
        else:
            archives[month] = prev.rstrip() + "\n" + block

    needs = bool(old)
    return active_text, archives, needs, len(kept), len(old)


def tag(label: str) -> str:
    return f"[{label}] " if label else ""


def atomic_write(path: Path, text: str) -> None:
    """Escribe tmp + os.replace: nunca deja el destino a medio escribir."""
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def main(argv):
    p = argparse.ArgumentParser(description="Rota el Dream Diary por mes.")
    p.add_argument("--today", type=str, default=None, help="YYYY-MM-DD (tests)")
    p.add_argument("--root", type=str, default=None, help="workspace root (tests)")
    p.add_argument("--check", action="store_true", help="exit 1 si hay drift")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    root = Path(args.root).resolve() if args.root else ROOT

    try:
        today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    except ValueError:
        print("Error: --today no es una fecha YYYY-MM-DD valida.")
        return 2

    found = instances(root)
    if not found:
        if args.check:
            print("OK: no hay DREAMS.md (nada que rotar).")
            return 0
        print("OK: no existe DREAMS.md.")
        return 0

    plans = []
    for active, archive_dir, label in found:
        try:
            result = plan_one(active, archive_dir, today)
        except NoMarkers as exc:
            print(f"Aviso: {exc} no tiene los marcadores del diary; se saltea "
                  "(queda fuera de la rotacion y el --check no lo ve).",
                  file=sys.stderr)
            continue
        if result is None:
            continue
        plans.append((active, archive_dir, label, result))

    if not plans:
        print("Error: ninguno de los DREAMS.md encontrados tiene los marcadores "
              "del diary.")
        return 2

    total_active = sum(r[3] for _, _, _, r in plans)
    total_old = sum(r[4] for _, _, _, r in plans)

    if args.check:
        stale = [(label, r[4]) for _, _, label, r in plans if r[2]]
        if stale:
            detalle = ", ".join(
                f"{label or 'raiz'}={n}" for label, n in stale
            )
            print(
                f"DREAMS DESFASADO: {total_old} entradas de meses anteriores siguen "
                f"en los activos ({detalle}).\n"
                "  Rotar:   python3 scripts/dreams-rotate.py"
            )
            return 1
        inst = f"{len(plans)} diario{'s' if len(plans) != 1 else ''}"
        print(f"OK: DREAMS en el mes en curso ({inst}, {total_active} entradas activas).")
        return 0

    if args.dry_run:
        for _, _, label, r in plans:
            print(
                f"[dry-run] {tag(label)}activas={r[3]} a_archivar={r[4]} "
                f"rota={'si' if r[2] else 'no'}"
            )
        return 0

    wrote = []
    failed = []
    for active, archive_dir, label, (active_text, archives, needs, n_active, n_old) in plans:
        name = label or "raiz"
        try:
            # 1) El archivo PRIMERO: mientras lo viejo no este a salvo, el activo
            #    no se toca. Al reves, un fallo entre ambos pasos borra entradas
            #    para siempre y el --check posterior sale verde (el activo ya
            #    esta "limpio"). Verificado 2026-11-18 por revision B.
            for month, text in archives.items():
                archive_dir.mkdir(parents=True, exist_ok=True)
                dest = archive_dir / f"DREAMS-{month}.md"
                if (not dest.exists()) or dest.read_text(encoding="utf-8") != text:
                    atomic_write(dest, text)
                    wrote.append(f"{name}:archivo:{month}")
            # 2) El activo despues, y solo si lo viejo ya se persistio.
            if active.read_text(encoding="utf-8") != active_text:
                atomic_write(active, active_text)
                wrote.append(f"{name}:activo")
        except OSError as exc:
            # Una instancia que falla no aborta el lote: se reporta y se sigue.
            failed.append(f"{name}: {exc}")

    if wrote:
        print(f"DREAMS actualizado ({', '.join(wrote)}): {total_active} activas, "
              f"{total_old} archivadas.")
    elif not failed:
        print(f"OK: DREAMS ya en el mes en curso ({total_active} activas, "
              f"{total_old} archivadas).")
    if failed:
        for f in failed:
            print(f"Error: no se pudo rotar {f}", file=sys.stderr)
        print("  El activo de esas instancias quedo intacto (no se perdieron "
              "entradas).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
