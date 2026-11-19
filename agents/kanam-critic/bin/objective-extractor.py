#!/usr/bin/env python3
"""Objective extractor utility (test‑first, strict).

The script reads a markdown file, looks for one or more blocks delimited by
``<!-- objetivos:begin -->`` and ``<!-- objetivos:end -->``. Inside each block a
markdown table with exactly three columns (Objetivo, Entregable, Cita) must be
present. Rows from every block are concatenated in document order.

Cells may escape a literal pipe as ``\\|``; the row splitter honours the escape
so an escaped pipe never changes the column count.

Output is a markdown table with six columns:

| Objetivo | Entregable | Fuente | Evidencia (ruta:línea) | Lo que dice la línea | Estado |

* ``Fuente`` is the markdown document being processed.
* ``Evidencia`` is the citation exactly as the author wrote it (surrounding
  backticks and whitespace removed, nothing else). Relative citation paths are
  resolved for validation only; the printed evidence stays relative.

  Relative citation resolution order (first existing path wins):

  1. Against the repository root: the closest ancestor of the markdown file
     containing ``.git``, obtained with ``git rev-parse --show-toplevel`` and a
     manual upward walk as fallback when git is missing or fails.
  2. Against the directory of the markdown file (previous behaviour), used when
     the document has no detectable repository root or when the citation does
     not exist under the root.

  Absolute citation paths are used as-is. A citation that exists under none of
  those bases is still reported as ``archivo inexistente``.
* ``Estado`` is ``verificado`` when the file exists, the line number is within the
  file and the line is non‑empty. Otherwise it is ``auto‑reportado`` and the
  reason is placed in the ``Lo que dice la línea`` column.

Line numbers must be plain ASCII digits (``[0-9]+``); ``1_0`` or ``+3`` are
auto‑reported as invalid citations.

The program prints the header and separator even when there are no rows, and
always writes a ``RESUMEN: ...`` line to stderr, including on error paths.

Exit codes:

* ``0`` – every row verified, or no rows at all.
* ``1`` – at least one row is auto‑reportado (``--no‑strict`` forces 0 here).
* ``2`` – the document is malformed or unreadable: unreadable file, missing
  closing marker, empty table, unexpected header, row with a column count other
  than three.

All operations use only the Python standard library.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

BEGIN = "<!-- objetivos:begin -->"
END = "<!-- objetivos:end -->"

HEADER = "| Objetivo | Entregable | Fuente | Evidencia (ruta:línea) | Lo que dice la línea | Estado |"
SEPARATOR = "|---|---|---|---|---|---|"


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def split_row(line: str) -> list[str]:
    """Split a markdown table row on unescaped pipes.

    ``\\|`` is kept as literal cell content (still escaped, so re‑emitting the
    value inside a table stays valid markdown). The outer pipes are dropped.
    """
    cells: list[str] = []
    buf: list[str] = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            buf.append(ch)
            buf.append(line[i + 1])
            i += 2
            continue
        if ch == "|":
            cells.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
        i += 1
    cells.append("".join(buf))
    if cells and cells[0].strip() == "":
        cells.pop(0)
    if cells and cells[-1].strip() == "":
        cells.pop()
    return [c.strip() for c in cells]


def is_separator(row: list[str]) -> bool:
    """True if every cell looks like a markdown alignment/separator cell."""
    return bool(row) and all(re.fullmatch(r":?-{3,}:?", c) for c in row)


def extract_blocks(content: str) -> list[str]:
    """Return the text of every begin/end block, in order.

    Raises ``ValueError`` if a begin marker has no matching end marker.
    """
    blocks: list[str] = []
    pos = 0
    while True:
        start = content.find(BEGIN, pos)
        if start == -1:
            return blocks
        start += len(BEGIN)
        stop = content.find(END, start)
        if stop == -1:
            raise ValueError("bloque objetivos:begin sin objetivos:end")
        blocks.append(content[start:stop])
        pos = stop + len(END)


def parse_table(block: str) -> list[tuple[str, str, str]]:
    """Parse one markdown table block.

    Returns a list of ``(objetivo, entregable, cita)`` tuples. Raises
    ``ValueError`` with a human readable reason if the table is malformed.
    """
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    if not lines:
        raise ValueError("bloque sin tabla")
    header = split_row(lines[0])
    if not any(re.search(r"objetivo", c, re.IGNORECASE) for c in header):
        raise ValueError("header inesperado")
    if len(header) != 3:
        raise ValueError(f"header con {len(header)} columnas, se esperaban 3")

    data_start = 1
    if len(lines) > 1 and is_separator(split_row(lines[1])):
        data_start = 2

    rows: list[tuple[str, str, str]] = []
    for ln in lines[data_start:]:
        cols = split_row(ln)
        if len(cols) != 3:
            raise ValueError(f"fila con número incorrecto de columnas ({len(cols)}): {ln}")
        rows.append((cols[0], cols[1], cols[2]))
    return rows


def clean_cita(cita: str) -> tuple[str, str]:
    """Return ``(path_str, line_str)`` from a citation.

    Surrounding backticks and whitespace are stripped; the space stripping
    happens after the backticks are removed so `` ` a.txt:3 ` `` works.
    """
    cleaned = cita.strip().strip("`").strip()
    if ":" not in cleaned:
        raise ValueError("cita sin ':'")
    path_str, line_str = cleaned.rsplit(":", 1)
    path_str = path_str.strip()
    line_str = line_str.strip()
    if not path_str:
        raise ValueError("cita sin ruta")
    return path_str, line_str


def find_repo_root(start: Path) -> Path | None:
    """Return the closest ancestor of ``start`` that looks like a repo root.

    Tries ``git rev-parse --show-toplevel`` first (handles worktrees and
    submodules); falls back to a manual upward walk looking for ``.git`` when
    git is unavailable, too slow or the directory is not a repository. Returns
    ``None`` when no root is detectable.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(start),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            top = result.stdout.strip()
            if top:
                return Path(top)
    except (OSError, subprocess.SubprocessError):
        pass

    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def candidate_paths(path_str: str, base_dir: Path, repo_root: Path | None) -> list[Path]:
    """Return the filesystem candidates for a citation path, in priority order.

    Absolute paths are used as-is. Relative paths are tried against the repo
    root first and the markdown directory second, without duplicates.
    """
    path = Path(path_str)
    if path.is_absolute():
        return [path]
    candidates: list[Path] = []
    if repo_root is not None:
        candidates.append(repo_root / path)
    local = base_dir / path
    if local not in candidates:
        candidates.append(local)
    return candidates


def validate_cita(cita: str, base_dir: Path, repo_root: Path | None = None):
    """Validate a citation string.

    Returns ``(evidencia, linea_texto, estado)``. ``evidencia`` is the author's
    citation without backticks. Relative paths are resolved against the repo
    root first and ``base_dir`` second, for checking only.
    """
    evidencia = cita.strip().strip("`").strip()
    try:
        path_str, line_str = clean_cita(cita)
    except Exception as exc:
        return evidencia, f"cita invalida: {exc}", "auto-reportado"

    if not re.fullmatch(r"[0-9]+", line_str):
        return evidencia, "cita invalida: numero de linea no valido", "auto-reportado"
    line_no = int(line_str)

    path = next(
        (c for c in candidate_paths(path_str, base_dir, repo_root) if c.exists()),
        None,
    )

    if path is None:
        return evidencia, "archivo inexistente", "auto-reportado"
    try:
        with path.open(encoding="utf-8") as f:
            lines = f.readlines()
        total = len(lines)
        if line_no < 1 or line_no > total:
            return evidencia, f"linea fuera de rango ({line_no} de {total})", "auto-reportado"
        raw = lines[line_no - 1].rstrip("\n").strip()
        if raw == "":
            return evidencia, "linea vacia", "auto-reportado"
        display = (raw[:77] + "...") if len(raw) > 80 else raw
        return evidencia, display, "verificado"
    except Exception as exc:
        return evidencia, f"error al leer: {exc}", "auto-reportado"


def print_table(rows: list[tuple[str, str, str, str, str, str]]) -> None:
    print(HEADER)
    print(SEPARATOR)
    for r in rows:
        print("| " + " | ".join(r) + " |")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract and validate objectives.")
    parser.add_argument("markdown", type=Path, help="Markdown file to process")
    parser.add_argument("--no-strict", action="store_true", help="Exit 0 instead of 1 on auto-reported rows")
    args = parser.parse_args()

    def finish(total: int, auto: int, code: int) -> int:
        verified = total - auto
        eprint(f"RESUMEN: {total} filas, {verified} verificadas, {auto} auto-reportadas")
        return code

    try:
        content = args.markdown.read_text(encoding="utf-8")
    except Exception as exc:
        print_table([])
        eprint(f"ERROR: documento ilegible en {args.markdown}: {exc}")
        return finish(0, 0, 2)

    try:
        blocks = extract_blocks(content)
    except ValueError as ve:
        print_table([])
        eprint(f"ERROR: documento malformado en {args.markdown}: {ve}")
        return finish(0, 0, 2)

    if not blocks:
        print_table([])
        eprint(f"sin bloque objetivos:begin/end en {args.markdown}")
        return finish(0, 0, 0)

    rows: list[tuple[str, str, str]] = []
    for block in blocks:
        try:
            rows.extend(parse_table(block))
        except ValueError as ve:
            print_table([])
            eprint(f"ERROR: tabla malformada en {args.markdown}: {ve}")
            return finish(0, 0, 2)

    base_dir = args.markdown.parent
    try:
        repo_root = find_repo_root(base_dir.resolve())
    except OSError:
        repo_root = None
    out_rows: list[tuple[str, str, str, str, str, str]] = []
    auto = 0
    for objetivo, entregable, cita in rows:
        evidencia, linea_texto, estado = validate_cita(cita, base_dir, repo_root)
        out_rows.append((objetivo, entregable, str(args.markdown), evidencia, linea_texto, estado))
        if estado == "auto-reportado":
            auto += 1

    print_table(out_rows)

    if auto and not args.no_strict:
        return finish(len(out_rows), auto, 1)
    return finish(len(out_rows), auto, 0)


if __name__ == "__main__":
    sys.exit(main())
