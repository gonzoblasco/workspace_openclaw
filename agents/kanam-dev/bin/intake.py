#!/usr/bin/env python3
"""
intake.py - Estacion S1 del pipeline de Kanam DEV.

Recibe un pedido en texto (arg o stdin) y produce un `intake.json` con los cinco
campos minimos del contrato (`PIPELINE-CONTRACTS.md` seccion 2, S1), mas la
plantilla inferida y su razon.

Por que existe: hoy cada pedido arranca leyendo brief, repo y SPEC para descubrir
despues que faltaba un dato. Esta estacion falla ANTES de leer codigo.

Contrato de exit codes (mismo que el resto del pipeline):
  0  intake completo, listo para S2
  1  falta un campo obligatorio (nombra cuales)
  2  error de uso o de entorno (no se pudo leer el pedido)

Cero dependencias externas. Solo stdlib.

Uso:
    intake.py --text "Arreglar el contador de minutos en el cronometro"
    intake.py --file pedido.md
    echo "..." | intake.py
    intake.py --file pedido.md --template task --out /tmp/intake.json

Diseño:
  - La inferencia de plantilla es una funcion PURA (`infer_template`), testeable
    sin IO. Es la pieza que mas va a cambiar: aislarla es lo que permite
    ajustarla sin tocar el CLI.
  - El default ante ambiguedad es `task`, nunca `hotfix`. El rigor es el default
    honesto (contrato seccion 5).
  - Los cinco campos se buscan por marcadores explicitos en el texto. Si el
    pedido no los trae, se reportan como faltantes con su nombre exacto; el
    script NO inventa valores.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Plantillas conocidas (contrato seccion 3).
# ---------------------------------------------------------------------------
TEMPLATES = ("hotfix", "task", "feature", "audit", "docs")

# Campos minimos que exige S1 (contrato seccion 2).
REQUIRED_FIELDS = ("objetivo", "artefacto", "verificacion", "convenciones", "aprobacion")

# Limite duro de `hotfix` (contrato seccion 3.1).
HOTFIX_MAX_FILES = 3
HOTFIX_MAX_LINES = 80

# ---------------------------------------------------------------------------
# Extraccion de los cinco campos.
# ---------------------------------------------------------------------------
# Se aceptan marcadores explicitos en espanol. Si el pedido no usa marcadores,
# los campos quedan faltantes: no se deduce de prosa libre. Deducir "artefacto"
# de texto suelto es exactamente la fabricacion de datos que el contrato prohibe.

# Cada marcador se busca SOLO al inicio de linea y consume hasta el fin de esa
# linea. Sin anclaje, `Objetivo:   \nArtefacto: foo.js` matcheaba el valor de la
# linea siguiente. Un `str` vacio no captura: el `+` exige al menos un caracter.
FIELD_MARKERS = {
    "objetivo": r"^[ \t]*(?:-[ \t]*)?objetivo[ \t]*:[ \t]*([^\n]+)$",
    "artefacto": r"^[ \t]*(?:-[ \t]*)?(?:artefacto|archivo|ruta)[ \t]*:[ \t]*([^\n]+)$",
    "verificacion": r"^[ \t]*(?:-[ \t]*)?(?:verificacion|verificaci[oó]n|c[oó]mo[ \t]+se[ \t]+prueba)[ \t]*:[ \t]*([^\n]+)$",
    "convenciones": r"^[ \t]*(?:-[ \t]*)?(?:convenciones|stack|repo)[ \t]*:[ \t]*([^\n]+)$",
    "aprobacion": r"^[ \t]*(?:-[ \t]*)?(?:aprobacion|aprobaci[oó]n|l[ií]mite)[ \t]*:[ \t]*([^\n]+)$",
}


def extract_fields(text: str) -> dict[str, str]:
    """Extrae los cinco campos por marcador explicito. No inventa valores.

    Devuelve solo los campos encontrados. Un `str` vacio cuenta como faltante.
    """
    found: dict[str, str] = {}
    for name, pattern in FIELD_MARKERS.items():
        m = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if m:
            value = m.group(1).strip()
            if value:
                found[name] = value
    return found


def missing_fields(fields: dict[str, str]) -> list[str]:
    """Los campos obligatorios que no aparecieron, en orden del contrato."""
    return [name for name in REQUIRED_FIELDS if not fields.get(name)]


# ---------------------------------------------------------------------------
# Inferencia de plantilla (funcion pura).
# ---------------------------------------------------------------------------
# Senales, en orden de especificidad. La primera que matchea gana.
# Nota: `hotfix` NO se infiere automaticamente de "arreglar" solo. Requiere
# senal de urgencia explicita Y que el pedido declare un alcance chico. Sin las
# dos cosas, se escala a `task` (contrato seccion 5: el default es el rigor).

_URGENT = re.compile(r"\b(urgente|roto en produccion|produccion caida|hotfix|p0)\b", re.IGNORECASE)
_TINY_SCOPE = re.compile(r"\b(un archivo|una linea|una funci[oó]n|puntual)\b", re.IGNORECASE)
_MEASURE = re.compile(r"\b(medir|medici[oó]n|diagn[oó]stico|auditar|auditor[ií]a|investigar|analizar)\b", re.IGNORECASE)
_DOCS = re.compile(r"\b(documentaci[oó]n|readme|adr|guia|gu[ií]a|changelog|docs)\b", re.IGNORECASE)
_NEW_THING = re.compile(r"\b(nueva?|nuevo|agregar|implementar|crear)\b", re.IGNORECASE)
_CHANGE = re.compile(r"\b(cambiar|modificar|refactorizar|corregir|arreglar|fix)\b", re.IGNORECASE)

# Palabras que sugieren que un pedido de "medir" en realidad pide construir.
_BUILD_HINT = re.compile(r"\b(implementar|construir|escribir|crear|agregar)\b", re.IGNORECASE)


def infer_template(text: str) -> tuple[str, str]:
    """Devuelve (plantilla, razon). Pura: no toca IO ni entorno.

    Reglas, en orden:
      1. Urgencia + alcance chico declarado -> hotfix
      2. Documentacion sin senal de codigo -> docs
      3. Medicion sin senal de construir -> audit
      4. Crear/agregar/implementar -> feature
      5. Cambio -> task
      6. Ambiguedad -> task (default honesto)
    """
    if _URGENT.search(text) and _TINY_SCOPE.search(text):
        return "hotfix", "senal de urgencia y alcance chico declarado"

    if _DOCS.search(text) and not _BUILD_HINT.search(text):
        return "docs", "nombra documentacion y no pide construir codigo"

    if _MEASURE.search(text) and not _BUILD_HINT.search(text):
        return "audit", "pide medir o diagnosticar, no construir"

    if _NEW_THING.search(text):
        return "feature", "pide crear o implementar algo nuevo"

    if _CHANGE.search(text):
        return "task", "pide un cambio acotado"

    return "task", "sin senal suficiente; el default honesto es task, no hotfix"


def hotfix_limit_ok(field_text: str) -> tuple[bool, str]:
    """Verifica el limite duro de hotfix si el pedido declara alcance.

    Acepta declaraciones `archivos: N` y `lineas: N`. Si no las declara, no hay
    nada que verificar aca: el limite real se controla en S3 con el diff.
    """
    files_m = re.search(r"archivos?\s*:\s*(\d+)", field_text, re.IGNORECASE)
    lines_m = re.search(r"lineas?\s*:\s*(\d+)", field_text, re.IGNORECASE)
    if files_m and int(files_m.group(1)) > HOTFIX_MAX_FILES:
        n = files_m.group(1)
        return False, f"hotfix excede el tope de {HOTFIX_MAX_FILES} archivos: declara {n} archivos; escala a task"
    if lines_m and int(lines_m.group(1)) > HOTFIX_MAX_LINES:
        n = lines_m.group(1)
        return False, f"hotfix excede el tope de {HOTFIX_MAX_LINES} lineas: declara {n} lineas; escala a task"
    return True, ""


# ---------------------------------------------------------------------------
# Construccion del intake.
# ---------------------------------------------------------------------------


def build_intake(text: str, template_override: str | None = None) -> tuple[dict, list[str]]:
    """Devuelve (intake, errores). `errores` vacio significa exit 0.

    Si hay un override CORE, la plantilla inferida se conserva como
    `template_inferred` para que el cambio quede auditable (contrato seccion 5,
    punto 3: una vez arrancado, el cambio de plantilla se registra).
    """
    fields = extract_fields(text)
    missing = missing_fields(fields)

    inferred, reason = infer_template(text)
    template = template_override or inferred

    warnings: list[str] = []
    if template_override and template_override != inferred:
        warnings.append(
            f"CORE override: inferida={inferred}, elegida={template_override}"
        )

    if template == "hotfix":
        # El limite se evalua sobre el pedido COMPLETO, no solo sobre los cinco
        # campos: la declaracion de tamano (`archivos: 9`) puede viajar fuera de
        # cualquier marcador y aun asi debe frenar el hotfix.
        ok, why = hotfix_limit_ok(text)
        if not ok:
            warnings.append(why)
            template = "task"

    intake = {
        "template": template,
        "template_inferred": inferred,
        "template_reason": reason if template == inferred else warnings[-1] if warnings else reason,
        "fields": {name: fields.get(name, "") for name in REQUIRED_FIELDS},
        "missing": missing,
        "limits": {
            "hotfix_max_files": HOTFIX_MAX_FILES,
            "hotfix_max_lines": HOTFIX_MAX_LINES,
        },
        "warnings": warnings,
        "status": "complete" if not missing else "incomplete",
    }
    return intake, missing


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def read_request(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="intake.py",
        description="Estacion S1: convierte un pedido en intake.json con los 5 campos minimos.",
    )
    parser.add_argument("--text", help="pedido en linea")
    parser.add_argument("--file", help="archivo con el pedido")
    parser.add_argument("--template", choices=TEMPLATES, help="override de plantilla (CORE confirma)")
    parser.add_argument("--out", help="ruta del intake.json (default: stdout)")
    parser.add_argument("--json", action="store_true", help="salida JSON cruda sin resumen")
    args = parser.parse_args(argv)

    if not args.text and not args.file and sys.stdin.isatty():
        parser.print_usage(sys.stderr)
        print("error: sin pedido. Usa --text, --file o stdin.", file=sys.stderr)
        return 2

    try:
        text = read_request(args)
    except OSError as exc:
        print(f"error: no se pudo leer el pedido: {exc}", file=sys.stderr)
        return 2

    if not text.strip():
        print("error: el pedido esta vacio.", file=sys.stderr)
        return 2

    intake, missing = build_intake(text, args.template)

    payload = json.dumps(intake, ensure_ascii=False, indent=2)

    if args.out:
        try:
            Path(args.out).write_text(payload + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"error: no se pudo escribir {args.out}: {exc}", file=sys.stderr)
            return 2

    if args.json:
        print(payload)
    else:
        print(f"plantilla: {intake['template']} ({intake['template_reason']})")
        for warning in intake["warnings"]:
            print(f"aviso: {warning}")
        if missing:
            print(f"FALTAN CAMPOS: {', '.join(missing)}")
        else:
            print("campos: completos (5/5)")
        if args.out:
            print(f"escrito: {args.out}")

    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
