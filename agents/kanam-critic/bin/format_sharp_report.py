#!/usr/bin/env python3
"""format_sharp_report.py - arma el CUERPO de un comentario de PR a partir de
un reporte de revision SHARP y de su fila del ledger `memory/verdicts.jsonl`.

No publica nada: solo produce texto (stdout o --body-file) y un modo --dry-run
que muestra el comando `gh pr comment` que se ejecutaria, sin escribir archivos.

Reglas del cuerpo (contrato de la herramienta):
  1. Primera linea:  **Veredicto: <VETO|Aprobado|ORO> <total>/25** (S<n> H<n> A<n> R<n> P<n>)
  2. Tabla SHARP: una fila por eje, con la justificacion textual del reporte.
  3. Evidencia: secciones crudas del reporte dentro de un <details> colapsado.
  4. Fricciones: lista extraida del reporte; si el reporte no las declara en una
     seccion propia pero hay listas que podrian serlo (Limites conocidos,
     observaciones), se dice "fricciones no declaradas" en vez de afirmar
     que no hay.
  5. Nada se inventa: todo numero/cita sale del reporte y del ledger. Si falta
     un dato requerido, exit 2 nombrando el faltante.
  6. Limite de 60000 caracteres: se trunca SOLO la evidencia (nunca el veredicto
     ni las fricciones) y se avisa en una linea.

Parseo tolerante de la tabla SHARP: los reportes del kit no usan un unico
formato. Se aceptan filas como `| **S** (Sharpness) | 4 | ... |`,
`| **S (Sharpness)** | 5 | ... |`, `| S - Sharpness | 3 | ... |`,
`| Sharpness | 5/5 | ... |`, en cualquier orden y con o sin encabezado.
Sin tabla SHARP el reporte no justifica sus ejes y el tool NO los completa
por su cuenta: exit 2 pidiendo `--allow-ledger-axes`. Con ese flag explicito,
si el total declarado coincide con el total del ledger y con la suma de sus
puntajes, los ejes se toman del ledger y se avisa por stderr y en el cuerpo
(nunca se inventan). El fallback queda asi visible en la linea de comandos:
un reporte sin justificacion no pasa por descuido.

Uso:
  python3 bin/format_sharp_report.py --report <ruta.md> --ledger <verdicts.jsonl> \
      --artifact <slug> [--allow-ledger-axes] [--body-file <ruta>] [--dry-run]
"""

import argparse
import json
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

AXES = ("S", "H", "A", "R", "P")
AXIS_LABELS = {
    "S": "Sharpness",
    "H": "Horizon",
    "A": "Asymmetry",
    "R": "Resistance",
    "P": "Parsimony",
}
VERDICTS = ("VETO", "Aprobado", "ORO")
MAX_BODY_CHARS = 60000
FRICTION_FALLBACK = "sin fricciones bloqueantes"
FRICTION_UNKNOWN = "fricciones no declaradas en el reporte"

EXIT_OK = 0
EXIT_INVALID = 2


class ReportError(Exception):
    """Dato faltante o incoherente: se traduce a exit 2."""


# --------------------------------------------------------------------------
# Helpers de texto
# --------------------------------------------------------------------------

def _fold(text):
    """Normaliza para comparar encabezados (minusculas, sin acentos)."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).lower()


def _clean_cell(text):
    """Deja una celda de tabla en una linea y sin pipes sueltos."""
    text = re.sub(r"\s+", " ", text).strip()
    text = text.rstrip("|").strip()
    return text.replace("|", "\\|")


# --------------------------------------------------------------------------
# Parseo del reporte
# --------------------------------------------------------------------------

def _split_sections(markdown):
    """Devuelve [(titulo, cuerpo)] de las secciones de nivel 2 (##)."""
    sections = []
    current_title = None
    current_lines = []

    for line in markdown.splitlines():
        heading = re.match(r"^##\s+(.*?)\s*$", line)
        if heading and not line.startswith("###"):
            if current_title is not None:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = heading.group(1).strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        sections.append((current_title, "\n".join(current_lines).strip()))
    return sections


def _strip_emphasis(text):
    """Quita el marcado que envuelve una celda: `**`, `__`, backticks."""
    return text.replace("**", "").replace("__", "").replace("`", "").strip()


def _split_row(line):
    """Celdas de una fila de tabla markdown, o None si no es una fila."""
    line = line.strip()
    if not line.startswith("|"):
        return None
    body = line[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", body)]


# Eje al inicio de la celda: 'S', 'S (Sharpness)', 'S - Sharpness'. Se exige
# que la letra no siga con otra letra para no confundir 'Sharpness' con 'S'.
_AXIS_LETTER_RE = re.compile(r"^([SHARP])(?![A-Za-z])")
_AXIS_WORDS = {label.lower(): axis for axis, label in AXIS_LABELS.items()}
# Puntaje: '5', '5/5', '5 / 5', '**5**'. Se rechaza cualquier otro texto.
_SCORE_RE = re.compile(r"^(\d{1,2})\s*(?:/\s*\d{1,2})?$")


def _axis_from_cell(cell):
    text = _strip_emphasis(cell)
    text = re.sub(r"^[^0-9A-Za-z]+", "", text)
    match = _AXIS_LETTER_RE.match(text)
    if match:
        return match.group(1)
    folded = _fold(text)
    for word, axis in _AXIS_WORDS.items():
        if re.search(r"\b{}\b".format(re.escape(word)), folded):
            return axis
    return None


def _score_from_cell(cell):
    text = _strip_emphasis(cell).strip("*_ ")
    match = _SCORE_RE.match(text)
    if not match:
        return None
    value = int(match.group(1))
    return value if 0 <= value <= 25 else None


def _parse_axes(markdown):
    """Extrae {eje: (puntaje, justificacion)} de cualquier tabla SHARP.

    Tolera el eje en la primera celda ('S', '**S**', 'S (Sharpness)',
    '**S (Sharpness)**', 'S - Sharpness', 'Sharpness'), el puntaje como
    '5', '5/5' o '5 / 5', filas en cualquier orden, con o sin encabezado.
    Las filas que no matchean un eje se ignoran.
    """
    axes = {}
    for line in markdown.splitlines():
        cells = _split_row(line)
        if not cells or len(cells) < 2:
            continue
        axis = _axis_from_cell(cells[0])
        if axis is None:
            continue
        score = _score_from_cell(cells[1])
        if score is None:
            continue
        comment = _clean_cell(cells[2]) if len(cells) > 2 else ""
        # La primera aparicion gana; una tabla repetida no debe pisar la buena.
        if axis not in axes:
            axes[axis] = (score, comment)
    return axes


_TOTAL_PATTERNS = (
    # | **Total** | **18** | |
    re.compile(r"\|\s*\**\s*Total\s*\**\s*\|\s*\**\s*(\d{1,3})"),
    # **Total = 23**
    re.compile(r"\*\*Total\s*=\s*(\d{1,3})\s*\*\*"),
    # **Total puntuación:** 20  /  **Total:** 20  /  **Total: 20/25**
    re.compile(r"\*\*Total[^:*\n]*[:=]\s*\**\s*(\d{1,3})"),
    # Total: 20  (solo si la linea no sigue con mas texto)
    re.compile(r"(?m)^\s*Total\s*[:=]\s*\**\s*(\d{1,3})\s*\**\s*$"),
)


def _parse_total(markdown):
    for pattern in _TOTAL_PATTERNS:
        match = pattern.search(markdown)
        if match:
            return int(match.group(1))
    raise ReportError(
        "el reporte no declara el total (se esperaba '**Total = <n>**', "
        "'**Total:** <n>' o una fila '| **Total** | <n> |')"
    )


def _parse_declared_verdict(markdown):
    """Veredicto declarado por el reporte, buscado primero junto al total."""
    patterns = (
        re.compile(r"\*\*Total[^\n]*?\*\*[^\n]{0,160}?\*\*(VETO|Aprobado|ORO)\*\*"),
        re.compile(r"\*\*Veredicto[^:*\n]*:?\s*\**\s*(VETO|Aprobado|ORO)\b"),
    )
    for pattern in patterns:
        match = pattern.search(markdown)
        if match:
            return match.group(1)

    section = None
    for title, body in _split_sections(markdown):
        if "veredicto" in _fold(title):
            section = body
            break
    if section is not None:
        match = re.search(r"\*\*(VETO|Aprobado|ORO)\*\*", section)
        if not match:
            match = re.search(r"\b(VETO|Aprobado|ORO)\b", section)
        if match:
            return match.group(1)

    raise ReportError(
        "el reporte no declara el veredicto (se esperaba '**VETO**', "
        "'**Aprobado**' o '**ORO**' junto al total o en la seccion Veredicto)"
    )


def _evidence_sections(markdown):
    """Secciones crudas: todo menos SHARP, Veredicto y Fricciones."""
    blocks = []
    for title, body in _split_sections(markdown):
        folded = _fold(title)
        if "sharp" in folded or "veredicto" in folded or "friccion" in folded:
            continue
        if not body.strip():
            continue
        blocks.append("#### {}\n\n{}".format(title, body.strip()))
    return blocks


_BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*\S)\s*$")

# Titulos de seccion que suelen contener listas que PODRIAN ser fricciones.
_FRICTION_HINT_TITLES = (
    "friccion",
    "limite",
    "limitacion",
    "observacion",
    "pendiente",
    "riesgo",
    "deuda",
    "bloqueante",
)


def _bullets(body):
    items = []
    for line in body.splitlines():
        match = _BULLET_RE.match(line)
        if match:
            items.append(_clean_cell(match.group(1)))
    return items


def _parse_frictions(markdown):
    """Fricciones del reporte, con el estado explicito de lo que se encontro.

    state:
      - 'declared': hay seccion de fricciones con bullets.
      - 'unknown':  no hay seccion de fricciones, pero hay listas en secciones
                    que podrian declararlas (Limites conocidos, observaciones).
                    No se afirma ausencia.
      - 'none':     no hay seccion de fricciones ni listas candidatas.
    """
    explicit_items = None
    hints = []
    for title, body in _split_sections(markdown):
        folded = _fold(title)
        items = _bullets(body)
        if "friccion" in folded:
            if explicit_items is None:
                explicit_items = items
        elif items and any(hint in folded for hint in _FRICTION_HINT_TITLES):
            hints.append({"title": title.strip(), "count": len(items)})

    if explicit_items is not None:
        if explicit_items:
            return {"state": "declared", "items": explicit_items, "hints": []}
        # Seccion declarada pero vacia: tampoco prueba ausencia.
        return {"state": "unknown", "items": [], "hints": []}
    if hints:
        return {"state": "unknown", "items": [], "hints": hints}
    return {"state": "none", "items": [], "hints": []}


def parse_report(path):
    try:
        markdown = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise ReportError("no se pudo leer el reporte '{}': {}".format(path, exc))

    return {
        "axes": _parse_axes(markdown),
        "axes_source": "report",
        "total": _parse_total(markdown),
        "verdict": _parse_declared_verdict(markdown),
        "evidence": _evidence_sections(markdown),
        "frictions": _parse_frictions(markdown),
    }


def resolve_axes(report, row, allow_ledger_axes=False):
    """Garantiza los 5 ejes. Devuelve 'report' o 'ledger' segun la fuente.

    - Con filas de ejes en el reporte: deben estar los 5; si falta uno, exit 2
      nombrandolo (no se completa desde el ledger).
    - Sin ninguna fila (el reporte omite la tabla SHARP): exit 2 salvo que se
      pase `allow_ledger_axes=True` (`--allow-ledger-axes`). Con el flag, los
      ejes solo se toman del ledger si el total declarado coincide con el del
      ledger y con la suma de sus ejes. Cualquier otra cosa es exit 2: no se
      inventan puntajes.
    """
    axes = report["axes"]
    if axes:
        missing = [axis for axis in AXES if axis not in axes]
        if missing:
            raise ReportError(
                "el reporte no declara los 5 ejes SHARP: falta {} "
                "(encontrados: {})".format(
                    ", ".join(missing), ", ".join(sorted(axes))
                )
            )
        return "report"

    if not allow_ledger_axes:
        raise ReportError(
            "el reporte no declara los 5 ejes SHARP; si aceptas tomarlos del "
            "ledger, usa --allow-ledger-axes"
        )

    ledger_sum = sum(row["scores"][axis] for axis in AXES)
    if report["total"] != row["total"] or report["total"] != ledger_sum:
        raise ReportError(
            "el reporte no declara tabla SHARP y no se puede reconstruir desde "
            "el ledger sin inventar: total reporte={}, total ledger={}, "
            "suma de ejes del ledger={}".format(
                report["total"], row["total"], ledger_sum
            )
        )

    report["axes"] = {axis: (row["scores"][axis], "") for axis in AXES}
    report["axes_source"] = "ledger"
    return "ledger"


# --------------------------------------------------------------------------
# Parseo del ledger
# --------------------------------------------------------------------------

def load_ledger_row(ledger_path, artifact):
    """Devuelve la unica fila del ledger para `artifact`."""
    try:
        raw = Path(ledger_path).read_text(encoding="utf-8")
    except OSError as exc:
        raise ReportError("no se pudo leer el ledger '{}': {}".format(ledger_path, exc))

    rows = []
    for number, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError as exc:
            raise ReportError(
                "ledger '{}' linea {}: JSON invalido ({})".format(ledger_path, number, exc)
            )
        if row.get("artifact") == artifact:
            rows.append(row)

    if not rows:
        raise ReportError(
            "el artifact '{}' no existe en el ledger '{}'".format(artifact, ledger_path)
        )
    if len(rows) > 1:
        raise ReportError(
            "el artifact '{}' aparece {} veces en el ledger '{}'; se esperaba una sola fila".format(
                artifact, len(rows), ledger_path
            )
        )

    row = rows[0]
    if row.get("status") == "invalidated":
        raise ReportError(
            "la fila '{}' del ledger esta invalidada: {}".format(
                artifact, row.get("invalidation_reason", "sin motivo declarado")
            )
        )

    scores = row.get("scores")
    if not isinstance(scores, dict):
        raise ReportError("la fila '{}' del ledger no tiene 'scores'".format(artifact))
    missing = [axis for axis in AXES if not isinstance(scores.get(axis), int)]
    if missing:
        raise ReportError(
            "la fila '{}' del ledger no tiene puntajes para: {}".format(
                artifact, ", ".join(missing)
            )
        )
    if not isinstance(row.get("total"), int):
        raise ReportError("la fila '{}' del ledger no tiene 'total'".format(artifact))
    if row.get("verdict") not in VERDICTS:
        raise ReportError(
            "la fila '{}' del ledger tiene verdict invalido: {!r}".format(
                artifact, row.get("verdict")
            )
        )
    return row


def validate_against_ledger(report, row):
    """Compara reporte vs ledger; cualquier discrepancia es exit 2 con detalle."""
    problems = []
    if report["total"] != row["total"]:
        problems.append(
            "total: reporte={} ledger={}".format(report["total"], row["total"])
        )
    for axis in AXES:
        report_score = report["axes"][axis][0]
        ledger_score = row["scores"][axis]
        if report_score != ledger_score:
            problems.append(
                "eje {}: reporte={} ledger={}".format(axis, report_score, ledger_score)
            )
    if report["verdict"] != row["verdict"]:
        problems.append(
            "veredicto: reporte={} ledger={}".format(report["verdict"], row["verdict"])
        )
    if problems:
        raise ReportError(
            "el reporte y el ledger no coinciden para '{}': {}".format(
                row.get("artifact", "?"), "; ".join(problems)
            )
        )


# --------------------------------------------------------------------------
# Armado del cuerpo
# --------------------------------------------------------------------------

def _header(row):
    scores = row["scores"]
    axes = " ".join("{}{}".format(axis, scores[axis]) for axis in AXES)
    return "**Veredicto: {} {}/25** ({})".format(
        row["verdict"], row["total"], axes
    )


def _sharp_table(report):
    lines = [
        "### Evaluación SHARP",
        "",
        "| Eje | Puntaje | Justificación |",
        "|---|---|---|",
    ]
    from_ledger = report.get("axes_source") == "ledger"
    for axis in AXES:
        score, comment = report["axes"][axis]
        if from_ledger and not comment:
            comment = "(sin justificación: el reporte no declara tabla SHARP)"
        lines.append(
            "| {} ({}) | {}/5 | {} |".format(
                axis,
                AXIS_LABELS[axis],
                score,
                comment or "(sin justificacion en el reporte)",
            )
        )
    if from_ledger:
        lines.extend([
            "",
            "_Ejes tomados del ledger: el reporte no declara tabla SHARP; "
            "los puntajes se contrastaron contra el total declarado._",
        ])
    return "\n".join(lines)


def _frictions_section(report):
    frictions = report["frictions"]
    lines = ["### Fricciones", ""]
    if frictions["state"] == "declared":
        lines.extend("- {}".format(item) for item in frictions["items"])
    elif frictions["state"] == "unknown":
        lines.append("- {}".format(FRICTION_UNKNOWN))
        if frictions["hints"]:
            found = ", ".join(
                "{} ({})".format(hint["title"], hint["count"])
                for hint in frictions["hints"]
            )
            lines.extend([
                "",
                "_El reporte no tiene sección de fricciones; hay bullets en: {}. "
                "No se listan como fricciones porque el reporte no las declara "
                "como tales._".format(found),
            ])
    else:
        lines.append("- {}".format(FRICTION_FALLBACK))
    return "\n".join(lines)


def _evidence_block(evidence_text):
    return (
        "<details>\n"
        "<summary>Evidencia cruda del reporte (comandos y salidas)</summary>\n\n"
        "{}\n"
        "</details>"
    ).format(evidence_text)


def build_body(report, row, limit=MAX_BODY_CHARS):
    """Devuelve (cuerpo, truncado_info|None). Nunca trunca veredicto ni fricciones."""
    head_parts = [_header(row), _sharp_table(report), "### Evidencia"]
    head = "\n\n".join(head_parts) + "\n\n"

    tail = "\n\n" + _frictions_section(report) + "\n"

    evidence_text = "\n\n".join(report["evidence"]).strip()
    if not evidence_text:
        evidence_text = "(el reporte no incluye secciones de evidencia)"

    body = head + _evidence_block(evidence_text) + tail
    if len(body) <= limit:
        return body, None

    total_evidence = len(evidence_text)
    notice_template = (
        "\n\n_Evidencia truncada: se omitieron {n} de {total} caracteres "
        "para respetar el limite de {limit}._"
    )

    # Presupuesto: reservamos el aviso y el esqueleto; recortamos solo evidencia.
    skeleton = head + _evidence_block("") + tail
    notice_len = len(notice_template.format(n=total_evidence, total=total_evidence, limit=limit))
    budget = limit - len(skeleton) - notice_len

    if budget < 0:
        raise ReportError(
            "el cuerpo no cabe en {} caracteres ni vaciando la evidencia "
            "(veredicto + fricciones ocupan {}); el reporte debe acortarse".format(
                limit, len(skeleton)
            )
        )

    cut = evidence_text[:budget]
    boundary = cut.rfind("\n")
    if boundary > 0:
        cut = cut[:boundary]
    cut = cut.rstrip()

    omitted = total_evidence - len(cut)
    notice = notice_template.format(n=omitted, total=total_evidence, limit=limit)
    body = head + _evidence_block(cut + notice) + tail

    # Margen de seguridad por si el corte de linea se quedo corto.
    while len(body) > limit and len(cut) > 0:
        overshoot = len(body) - limit
        cut = cut[: max(0, len(cut) - overshoot - 1)]
        boundary = cut.rfind("\n")
        if boundary > 0:
            cut = cut[:boundary]
        cut = cut.rstrip()
        omitted = total_evidence - len(cut)
        notice = notice_template.format(n=omitted, total=total_evidence, limit=limit)
        body = head + _evidence_block(cut + notice) + tail

    if len(body) > limit:
        raise ReportError(
            "no se pudo truncar la evidencia hasta {} caracteres sin tocar el "
            "veredicto ni las fricciones".format(limit)
        )

    return body, {
        "omitted": omitted,
        "total_evidence": total_evidence,
        "limit": limit,
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _dry_run_summary(artifact, chars, would_write):
    temp_name = "format-sharp-report-{}.md".format(
        re.sub(r"[^A-Za-z0-9._-]+", "-", artifact)
    )
    temp_path = os.path.join(tempfile.gettempdir(), temp_name)
    lines = [
        "[dry-run] no se escribio ningun archivo (ni cuerpo ni temporales)",
        "[dry-run] cuerpo: {} caracteres".format(chars),
        "[dry-run] comando que se ejecutaria:",
        "    gh pr comment <PR> --body-file {}".format(temp_path),
        "[dry-run] pasos reales: --body-file {} y luego el comando con el numero de PR".format(
            temp_path
        ),
    ]
    if would_write:
        lines.append(
            "[dry-run] se ignoro --body-file {}: dry-run no escribe".format(would_write)
        )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Arma el cuerpo de un comentario de PR desde un reporte SHARP + ledger."
    )
    parser.add_argument("--report", required=True, help="reporte de revision (markdown)")
    parser.add_argument("--ledger", required=True, help="ledger JSONL de veredictos")
    parser.add_argument("--artifact", required=True, help="slug del artifact en el ledger")
    parser.add_argument(
        "--allow-ledger-axes",
        action="store_true",
        help=(
            "permite tomar los 5 ejes del ledger cuando el reporte no declara "
            "tabla SHARP (default: exit 2)"
        ),
    )
    parser.add_argument(
        "--body-file",
        default=None,
        help="escribe el cuerpo en esta ruta (default: stdout)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="imprime el cuerpo y el comando gh que se ejecutaria; no escribe nada",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=MAX_BODY_CHARS,
        help="limite del cuerpo (default: 60000)",
    )
    args = parser.parse_args(argv)

    try:
        report = parse_report(args.report)
        row = load_ledger_row(args.ledger, args.artifact)
        axes_source = resolve_axes(report, row, allow_ledger_axes=args.allow_ledger_axes)
        validate_against_ledger(report, row)
        body, truncated = build_body(report, row, limit=args.max_chars)
    except ReportError as exc:
        sys.stderr.write("ERROR: {}\n".format(exc))
        return EXIT_INVALID

    if axes_source == "ledger":
        sys.stderr.write(
            "AVISO: el reporte no declara tabla SHARP; ejes tomados del ledger "
            "(total {} coincide con la suma de ejes)\n".format(report["total"])
        )

    if args.dry_run:
        sys.stdout.write(body)
        if not body.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
        sys.stderr.write("\n" + _dry_run_summary(args.artifact, len(body), args.body_file) + "\n")
        if truncated:
            sys.stderr.write(
                "[dry-run] evidencia truncada: {} de {} caracteres omitidos\n".format(
                    truncated["omitted"], truncated["total_evidence"]
                )
            )
        return EXIT_OK

    if args.body_file:
        target = Path(args.body_file)
        try:
            if target.parent and not target.parent.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8")
        except OSError as exc:
            sys.stderr.write("ERROR: no se pudo escribir '{}': {}\n".format(args.body_file, exc))
            return EXIT_INVALID
        sys.stderr.write(
            "cuerpo escrito en {} ({} caracteres)\n".format(args.body_file, len(body))
        )
        if truncated:
            sys.stderr.write(
                "evidencia truncada: {} de {} caracteres omitidos\n".format(
                    truncated["omitted"], truncated["total_evidence"]
                )
            )
        return EXIT_OK

    sys.stdout.write(body)
    if not body.endswith("\n"):
        sys.stdout.write("\n")
    if truncated:
        sys.stderr.write(
            "evidencia truncada: {} de {} caracteres omitidos\n".format(
                truncated["omitted"], truncated["total_evidence"]
            )
        )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
