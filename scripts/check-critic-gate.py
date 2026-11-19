#!/usr/bin/env python3
"""
check-critic-gate.py - El veredicto del Critic como gate, no como relato.

POR QUE EXISTE (T5.2 del programa critic-v0.3).
Hasta hoy el veredicto vivia en el ledger y en un reporte, y su unica barrera era
`verify-verdict.py`, que corre dentro del step del kit. Eso verifica la INTEGRIDAD del
ledger, no habilita una decision: ningun consumidor podia preguntar "puede pasar este
artefacto?" y recibir un exit code. Este script es esa pregunta.

QUE VERIFICA (por artifact, en este orden):
  1. FILA      existe al menos una fila para el artifact en el ledger.
  2. VIGENTE   la ultima fila NO invalidada tiene verdict en {Aprobado, ORO}.
               Si es VETO: exit 3. Si todas las filas del artifact estan invalidadas: no
               hay veredicto vigente y es exit 4 (no 0: un veredicto retirado no habilita).
  3. REPORTE   el reporte de esa fila existe y su nombre termina en el slug.
  4. CITAS     el reporte tiene >=5 citas `ruta:linea` cuyo archivo exista.
               La linea NO se valida aca: eso es trabajo de verify-verdict.py, que abre
               el archivo y lee la linea. Este gate es barato a proposito.

REGLA DE REVISIONES (caso real, 2026-11-19; no es hipotetico).
El mismo dia, `T4.1-objective-extractor` recibio VETO 18/25 y su re-verificacion se publico
como `T4.1-objective-extractor-r2` con 20/25 Aprobado. Las dos filas conviven en el ledger:
la revision NO invalida ni sobrescribe a la anterior. Consecuencias, decididas aca:

  a) El match es EXACTO por `artifact`. Preguntar por `T4.1-objective-extractor` devuelve
     su VETO historico (exit 3), no el Aprobado de su revision.
  b) Un `-rN` NO se hereda hacia el slug base. El ledger no tiene campo `supersedes` ni
     `revises`: inferir que r2 "mejora" al base seria inventar una relacion que el ledger no
     declara. Y peor: permitiria borrar un VETO renombrando el artefacto, que es la forma
     mas barata de fabricar un verde.
  c) El consumidor que quiera gatear la version vigente pasa el slug vigente (`...-r2`).
     El gate lo dice: cuando falla, lista las revisiones posteriores que encuentra, para que
     nadie confunda "el gate de este slug esta en rojo" con "el artefacto no tiene arreglo".
  d) `--all` usa la convencion `-rN` con un solo proposito: decidir que filas son HISTORIA
     (SKIP) y no heads. No la usa para aprobar nada.

DOS MODOS, DOS PREGUNTAS DISTINTAS:
  * `<slug>`      "puede pasar ESTE artefacto?" -> gate duro, exit 0/3/4/2.
  * `--all`       "todo artifact del ledger tiene veredicto con respaldo?" -> barrido de
                  integridad, exit 0/4/2. Un VETO es un veredicto: en `--all` se informa y
                  se cuenta, pero NO pinta el repo de rojo. El criterio de aceptacion del
                  programa lo dice asi: "un run sin veredicto falla; con veredicto pasa".
                  Bloquear el repo entero por un VETO historico a un documento convertiria
                  el CI en un recordatorio permanente y lo haria ignorable.

SALIDAS: 0 PASS | 3 VETO | 4 MISSING | 2 ERROR (uso incorrecto o ledger ilegible).
No escribe nada: es una barrera, no un emisor. No crear filas, no tocar reportes.

Uso:
    python3 scripts/check-critic-gate.py <artifact-slug>
    python3 scripts/check-critic-gate.py <artifact-slug> --ledger RUTA --reviews DIR
    python3 scripts/check-critic-gate.py --all
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "agents" / "kanam-critic" / "memory" / "verdicts.jsonl"
DEFAULT_REVIEWS = ROOT / "agents" / "kanam-critic" / "docs" / "reviews"

APPROVED = ("Aprobado", "ORO")
KNOWN_VERDICTS = ("Aprobado", "ORO", "VETO")
FIXTURE_MARKERS = ("sample", "test", "fixture", "verify_by_core", "demo")
REVISION = re.compile(r"^(?P<base>.+)-r(?P<n>\d+)$")

CITATION = re.compile(
    r"(?<![\w./-])([A-Za-z0-9_./-]+\.(?:md|py|jsonl|tsv|yaml|yml|json|sh|js|mjs|ts|txt)):(\d+)"
)

EXIT_PASS, EXIT_ERROR, EXIT_VETO, EXIT_MISSING = 0, 2, 3, 4


class LedgerError(Exception):
    pass


def load_ledger(path: Path) -> list[dict]:
    """Lee el JSONL. Una linea ilegible es un error, no un skip: el ledger es el sujeto del gate."""
    if not path.exists():
        raise LedgerError(f"ledger inexistente: {path}")
    rows: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LedgerError(f"ledger ilegible: {path} ({exc})") from exc
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LedgerError(f"ledger ilegible: {path}:{n} no es JSON ({exc.msg})") from exc
        if not isinstance(rec, dict):
            raise LedgerError(f"ledger ilegible: {path}:{n} no es un objeto JSON")
        rows.append(rec)
    return rows


def is_fixture(artifact: str) -> bool:
    low = artifact.lower()
    return any(k in low for k in FIXTURE_MARKERS)


def total_of(rec: dict) -> int | None:
    total = rec.get("total")
    if isinstance(total, int):
        return total
    scores = rec.get("scores") or {}
    vals = [v for v in scores.values() if isinstance(v, int)]
    return sum(vals) if vals else None


def slug_suffixes(slug: str) -> tuple[str, ...]:
    """Sufijos validos del nombre de reporte para un slug.

    El prefijo `kanam-critic-kit-` es la unica excepcion heredada: los reportes de ese kit se
    llaman `2026-11-06-critic-kit-v0.3-r4.md` (sin el `kanam-`). Es la misma equivalencia que
    aplica verify-verdict.py; sin ella, dos filas reales del ledger quedarian sin respaldo por
    el nombre, no por falta de evidencia. Sigue siendo match por SUFIJO, no por contencion.
    """
    suffixes = [slug]
    if slug.startswith("kanam-critic-kit-"):
        suffixes.append(slug[len("kanam-critic-kit-"):])
    return tuple(suffixes)


def resolve_report(rec: dict, slug: str, reviews: Path) -> tuple[Path | None, str]:
    """Reporte de la fila. El nombre debe TERMINAR en el slug.

    `...-T4.1-objective-extractor-r2.md` no es el reporte de `T4.1-objective-extractor`:
    un match por contencion le regalaria al slug base el veredicto de su revision, que es
    exactamente el falso verde que este gate existe para impedir.
    """
    suffixes = slug_suffixes(slug)
    declared = rec.get("report")
    if declared:
        path = Path(declared)
        path = path if path.is_absolute() else ROOT / path
        if not path.exists():
            return None, f"la fila declara report={declared} y ese archivo no existe"
        if not path.stem.endswith(suffixes):
            return None, f"report={declared} no lleva el slug '{slug}' en el nombre"
        return path, ""

    if not reviews.is_dir():
        return None, f"no existe el directorio de reportes: {reviews}"
    exact = sorted(p for p in reviews.glob("*.md") if p.stem.endswith(suffixes))
    if exact:
        return exact[-1], ""
    return None, f"no hay reporte en {reviews.name}/ cuyo nombre termine en '{slug}'"


def count_citations(report: Path) -> tuple[int, list[str]]:
    """Citas `ruta:linea` con archivo existente. Deduplicadas: 5 repeticiones de la misma
    cita no son cinco piezas de evidencia."""
    try:
        text = report.read_text(encoding="utf-8")
    except OSError as exc:
        return 0, [f"reporte ilegible: {report} ({exc})"]

    seen: set[tuple[str, str]] = set()
    bad: list[str] = []
    for raw_path, line in CITATION.findall(text):
        key = (raw_path, line)
        if key in seen:
            continue
        seen.add(key)
        candidates = []
        p = Path(raw_path)
        candidates.append(p if p.is_absolute() else ROOT / p)
        candidates.append(report.parent / p)
        if not any(c.exists() for c in candidates):
            bad.append(f"{raw_path}:{line}")
    return len(seen) - len(bad), bad


def gate_artifact(slug: str, rows: list[dict], reviews: Path) -> tuple[int, str, list[str]]:
    """Devuelve (exit_code, estado, lineas) para un slug exacto."""
    lines: list[str] = []
    mine = [r for r in rows if r.get("artifact") == slug]
    if not mine:
        return EXIT_MISSING, "MISSING", [f"ROJO  fila: no hay ninguna fila para '{slug}' en el ledger"]

    valid = [r for r in mine if r.get("status") != "invalidated"]
    dropped = len(mine) - len(valid)
    if dropped:
        lines.append(f"OK    invalidacion: {dropped} fila(s) invalidada(s) descartada(s)")
    if not valid:
        lines.append(f"ROJO  fila: todas las filas de '{slug}' estan invalidadas")
        return EXIT_MISSING, "MISSING", lines

    rec = valid[-1]
    verdict = rec.get("verdict")
    total = total_of(rec)
    stamp = str(rec.get("timestamp", ""))[:19]
    lines.append(f"OK    fila vigente: verdict={verdict} total={total} ts={stamp}")
    if verdict not in KNOWN_VERDICTS:
        lines.append(f"ROJO  veredicto: '{verdict}' no es un veredicto conocido {KNOWN_VERDICTS}")
        return EXIT_ERROR, "ERROR", lines
    if verdict == "VETO":
        note = str(rec.get("notes", "")).strip()
        suffix = f": {note}" if note else ""
        lines.append(f"ROJO  veredicto: VETO vigente{suffix}")
        return EXIT_VETO, "VETO", lines

    report, why = resolve_report(rec, slug, reviews)
    if report is None:
        lines.append(f"ROJO  reporte: {why}")
        return EXIT_MISSING, "MISSING", lines
    lines.append(f"OK    reporte: {report.relative_to(ROOT) if report.is_relative_to(ROOT) else report}")

    cites, bad = count_citations(report)
    if cites < 5:
        detail = f"solo {cites} cita(s) ruta:linea con archivo existente (se exigen 5)"
        if bad:
            detail += "; sin archivo: " + ", ".join(bad[:3])
        lines.append(f"ROJO  citas: {detail}")
        return EXIT_MISSING, "MISSING", lines
    lines.append(f"OK    citas: {cites} con archivo existente")
    return EXIT_PASS, "PASS", lines


def heads_of(rows: list[dict]) -> tuple[list[dict], list[tuple[str, str]], list[str]]:
    """Heads: ultima fila por artifact, sin invalidados, sin bases superadas por una revision."""
    by_artifact: dict[str, list[dict]] = {}
    for rec in rows:
        art = rec.get("artifact")
        if not isinstance(art, str) or not art:
            continue
        by_artifact.setdefault(art, []).append(rec)
    latest = {art: recs[-1] for art, recs in by_artifact.items()}
    # Un artifact con al menos una fila NO invalidada sigue teniendo veredicto vigente: la
    # invalidacion retira una fila, no el artefacto. Solo se cae si todas sus filas cayeron.
    retired = [art for art, recs in by_artifact.items()
               if not any(r.get("status") != "invalidated" for r in recs)]
    superseded: list[tuple[str, str]] = []
    bases = {m.group("base") for m in (REVISION.match(a) for a in latest) if m}
    for base in sorted(bases):
        revisions = [a for a in latest if REVISION.match(a) and REVISION.match(a).group("base") == base]
        live = [a for a in revisions if latest[a].get("status") != "invalidated"]
        if live and base in latest:
            superseded.append((base, sorted(live)[-1]))

    skip = {b for b, _ in superseded}
    heads = [rec for art, rec in latest.items()
             if art not in skip and art not in retired and not is_fixture(art)]
    return heads, superseded, retired


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Gate del veredicto del Critic: exit 0 solo con veredicto vigente y respaldo")
    ap.add_argument("artifact", nargs="?", help="slug exacto del artifact")
    ap.add_argument("--all", action="store_true", help="barrido de integridad de todo el ledger")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    ap.add_argument("--reviews", default=str(DEFAULT_REVIEWS))
    args = ap.parse_args(argv)

    if bool(args.artifact) == bool(args.all):
        print("ROJO  uso: pasá exactamente uno de <artifact-slug> o --all")
        print(f"CRITIC-GATE: ERROR  ({args.artifact or ('--all' if args.all else 'sin argumento')})")
        return EXIT_ERROR

    ledger, reviews = Path(args.ledger), Path(args.reviews)
    try:
        rows = load_ledger(ledger)
    except LedgerError as exc:
        print(f"ROJO  ledger: {exc}")
        print(f"CRITIC-GATE: ERROR  ({args.artifact or '--all'})")
        return EXIT_ERROR

    if args.artifact:
        code, state, lines = gate_artifact(args.artifact, rows, reviews)
        for line in lines:
            print(line)
        if state in ("VETO", "MISSING"):
            later = [r for r in rows
                     if r.get("status") != "invalidated"
                     and (m := REVISION.match(str(r.get("artifact", ""))))
                     and m.group("base") == args.artifact]
            if later:
                got = ", ".join(f"{r['artifact']}={r.get('verdict')}" for r in later)
                print(f"NOTA  existe revision posterior: {got} (slug distinto: pedila por su nombre)")
        print(f"CRITIC-GATE: {state}  ({args.artifact})")
        return code

    heads, superseded, retired = heads_of(rows)
    if not heads:
        print("ROJO  ledger: no hay ningun artefacto evaluable")
        print("CRITIC-GATE: MISSING  (--all)")
        return EXIT_MISSING

    approved = vetoed = 0
    failures: list[str] = []
    errored: list[str] = []
    for rec in heads:
        slug = rec["artifact"]
        _code, state, lines = gate_artifact(slug, rows, reviews)
        total = total_of(rec)
        if state == "PASS":
            approved += 1
            print(f"OK    {slug}  {rec.get('verdict')} {total}")
        elif state == "VETO":
            vetoed += 1
            print(f"VETO  {slug}  VETO {total}")
        else:
            (errored if state == "ERROR" else failures).append(slug)
            print(f"ROJO  {slug}  {state}")
            for line in lines:
                print("      " + line)

    skipped = latest_fixtures(rows)
    for base, by in superseded:
        print(f"SKIP  {base}  historia: superado por {by}")
    for art in retired:
        print(f"SKIP  {art}  invalidado: su fila vigente fue retirada con motivo")
    for fx in skipped:
        print(f"SKIP  {fx}  fixture del ledger (no es artefacto)")

    scope = (f"heads={len(heads)} aprobados={approved} vetados={vetoed} "
             f"fuera_de_alcance={len(superseded) + len(skipped) + len(retired)}")
    if errored:
        print(f"ROJO  ledger: verdict fuera de {KNOWN_VERDICTS} en {', '.join(errored)}")
        print(f"CRITIC-GATE: ERROR  (--all, {scope})")
        return EXIT_ERROR
    if failures:
        print(f"ROJO  integridad: {len(failures)} head(s) sin veredicto respaldado: {', '.join(failures)}")
        print(f"CRITIC-GATE: MISSING  (--all, {scope})")
        return EXIT_MISSING
    print(f"CRITIC-GATE: PASS  (--all, {scope})")
    return EXIT_PASS


def latest_fixtures(rows: list[dict]) -> list[str]:
    seen: list[str] = []
    for rec in rows:
        art = rec.get("artifact")
        if isinstance(art, str) and art and is_fixture(art) and art not in seen:
            seen.append(art)
    return seen


if __name__ == "__main__":
    sys.exit(main())
