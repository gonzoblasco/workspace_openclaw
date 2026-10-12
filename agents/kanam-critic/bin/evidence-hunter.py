#!/usr/bin/env python3
"""
evidence-hunter.py — Runner real de la skill `evidence-hunter`.

Lee un `assertions.yaml` con el formato que emite `tests/evidence-hunter/build_assertions.py`
y produce un `evidence.json` con `details[]` que consume `tests/evidence-hunter/validate.py`.

Contrato de I/O:
  - INPUT  (YAML): lista de `assertions`, cada una con `description` y `source` (ruta absoluta).
  - OUTPUT (JSON): {"details": [{"status": "...", "evidence": "..."}, ...]}

Vocabulario de status (idéntico al SKILL.md de la skill):
  - verificado      – la evidencia existe y se reproduce en disco.
  - parcial         – existe una parte; la otra falla.
  - auto-reportado  – el autor lo dijo, pero en disco no aparece.
  - bloqueado       – no se pudo ejecutar el detector (dependencia ausente, sintaxis rota).

Diseño:
  - Cero dependencias externas. Solo stdlib: json, re, shutil, subprocess, sys, yaml-lite.
    Como no asumimos PyYAML, parseamos un YAML minimalista (listas de maps con
    `description` y `source`). Si el YAML crece en complejidad, este parser
    debe migrar a PyYAML — pero hoy no hace falta.
  - Mapa declarativo KEYWORDS → DETECTOR al inicio. Añadir un detector nuevo
    es una entrada en el mapa, no un `if/elif`.
  - Cuando un detector no puede ejecutarse (pytest ausente, rg ausente),
    el runner devuelve `bloqueado` con la razón exacta en `evidence`. Esto
    previene el verde falso: ausencia de herramienta ≠ "todo bien".

Uso:
    python3 bin/evidence-hunter.py /tmp/assertions.yaml > /tmp/evidence.json
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

# ---------------------------------------------------------------------------
# YAML-lite parser
# ---------------------------------------------------------------------------
# Formato esperado (emítido por build_assertions.py):
#
#   assertions:
#     - description: |
#         texto multilínea
#       source: "/ruta/absoluta"
#
# Este parser NO es un YAML genérico. Es el subset exacto que el lab produce.
# Si en el futuro el SKILL.md amplía el contrato, migrar a PyYAML.

def parse_assertions_yaml(text: str) -> list[dict]:
    """Devuelve la lista de dicts `assertions` del YAML-lite.

    Cada elemento tiene al menos `description` (str) y `source` (str, ruta absoluta).
    """
    items: list[dict] = []
    current: dict | None = None
    in_description = False
    desc_buffer: list[str] = []

    def flush() -> None:
        nonlocal current, in_description, desc_buffer
        if current is not None:
            if desc_buffer:
                current["description"] = "\n".join(desc_buffer).strip()
            items.append(current)
        current = None
        in_description = False
        desc_buffer = []

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("assertions:"):
            continue
        if line.startswith("  - description:"):
            flush()
            current = {}
            # Block scalar: lo que viene tras `|` es la primera línea del contenido.
            rest = line.split("description:", 1)[1].strip()
            if rest == "|":
                in_description = True
                desc_buffer = []
            else:
                in_description = True
                desc_buffer = [rest.lstrip()]
            continue
        if in_description and current is not None and "description" not in current:
            # Línea indentada bajo `description: |`
            if line.startswith("      "):
                desc_buffer.append(line[6:])
                continue
            else:
                # Fin de la descripción: vuelca lo acumulado.
                current["description"] = "\n".join(desc_buffer).strip()
                desc_buffer = []
                in_description = False
        if line.startswith("    source:"):
            value = line.split("source:", 1)[1].strip().strip('"')
            if current is None:
                # description y source en la misma línea, raro pero tolerado.
                continue
            current["source"] = value
            continue
    flush()
    return items


# ---------------------------------------------------------------------------
# Resolución de herramientas: venv del lab → PATH → nada.
# ---------------------------------------------------------------------------
# El runner NO asume que pytest/coverage estén en el PATH del host. El lab
# mantiene un venv local en `tests/evidence-hunter/.venv/` que vive y muere
# con el lab. Si existe, sus binarios ganan. Si no, se cae al PATH.
#
# Contrato: devolver la ruta absoluta al ejecutable, o None si no se halla.
# Los detectores NUNCA ejecutan un comando sin pasar por acá.

# Raíz del lab: este archivo vive en `agents/kanam-critic/bin/`,
# el lab en `agents/kanam-critic/tests/evidence-hunter/`.
_LAB_VENV_BIN = Path(__file__).resolve().parent.parent / "tests" / "evidence-hunter" / ".venv" / "bin"


def _resolve_tool(name: str) -> str | None:
    """Devuelve la ruta al ejecutable `name`, priorizando el venv del lab.

    Cascada:
      1. `tests/evidence-hunter/.venv/bin/<name>` si existe y es ejecutable.
      2. `shutil.which(name)` (PATH del host).
      3. None.
    """
    venv_candidate = _LAB_VENV_BIN / name
    if venv_candidate.exists() and venv_candidate.is_file():
        return str(venv_candidate)
    resolved = shutil.which(name)
    if resolved is not None:
        return resolved
    return None


# ---------------------------------------------------------------------------
# Detectores — cada uno devuelve (status, evidence_string)
# ---------------------------------------------------------------------------

DetectorFn = Callable[[str, str], tuple[str, str]]


def detector_pytest(description: str, source: str) -> tuple[str, str]:
    """Detecta presencia/ejecución de pytest cerca del `source`.

    Lógica:
      1. Si el `source` no existe → auto-reportado.
      2. Busca `test_*.py` adyacentes. Si no hay → auto-reportado.
      3. Si pytest no está en PATH → bloqueado.
      4. Ejecuta pytest sobre el archivo de test. Si pasa → verificado.
         Si falla → parcial (cita = ruta del test fallido).
    """
    src = Path(source)
    if not src.exists():
        return "auto-reportado", f"source no existe: {source}"

    # Buscar tests adyacentes (mismo dir, o un dir `tests/` cercano).
    candidates: list[Path] = []
    candidates += list(src.parent.glob("test_*.py"))
    tests_dir = src.parent / "tests"
    if tests_dir.exists():
        candidates += list(tests_dir.glob("test_*.py"))
    # Subir un nivel si source es foo.py y tests está arriba.
    if src.parent.parent.exists():
        candidates += list(src.parent.parent.glob("tests/test_*.py"))

    if not candidates:
        return "auto-reportado", f"no se encontraron test_*.py adyacentes a {source}"

    # Resolver pytest: venv del lab primero, PATH después.
    pytest_bin = _resolve_tool("pytest")
    if pytest_bin is None:
        return "bloqueado", "pytest no está en PATH ni en el venv del lab (command not found)"

    # Ejecutar pytest. -q para salida mínima; --tb=line para tener la línea del fallo.
    test_to_run = candidates[0]
    proc = subprocess.run(
        [pytest_bin, "-q", "--tb=line", str(test_to_run)],
        capture_output=True,
        text=True,
        cwd=str(test_to_run.parent.parent),
    )

    if proc.returncode == 0:
        return "verificado", f"{test_to_run}:1"
    if proc.returncode in (1, 2):
        # pytest devuelve 1 cuando hay test fallido, 2 cuando hay error de
        # colección. Ambos son `parcial` desde la óptica del hunter: la
        # suite corre pero no pasa.
        return "parcial", f"{test_to_run}:1 (pytest rc={proc.returncode})"
    # rc raro (4 = uso, 5 = sin tests) → bloqueado
    return "bloqueado", f"pytest rc inesperado {proc.returncode}: {proc.stderr[:200]}"


def detector_rg_token(description: str, source: str) -> tuple[str, str]:
    """Detecta si un token mencionado en la descripción aparece en un archivo de estilos.

    Estrategia:
      1. Extrae la primera palabra queparece token (kebab-case, snake_case o
         'algo-similar' entre comillas) de la descripción.
      2. Si `rg` está en PATH, lo usa. Si no, hace fallback a `grep -R`.
      3. Si no encuentra el token → auto-reportado.
      4. Si lo encuentra → verificado con la ruta de la primera coincidencia.
    """
    src = Path(source)
    if not src.exists():
        return "auto-reportado", f"source no existe: {source}"

    # Extraer token candidato: primera secuencia kebab/snake después de "token".
    m = re.search(r"token\s+([a-z][a-z0-9_-]+)", description, re.IGNORECASE)
    if not m:
        return "bloqueado", "no se pudo extraer un token de la descripción"
    token = m.group(1)

    rg_bin = _resolve_tool("rg")
    grep_bin = _resolve_tool("grep")
    if rg_bin is not None:
        cmd = [rg_bin, "-n", "--no-heading", token, str(src.parent)]
    elif grep_bin is not None:
        cmd = [grep_bin, "-RIn", token, str(src.parent)]
    else:
        return "bloqueado", "ni rg ni grep disponibles"

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0 and proc.stdout.strip():
        first_line = proc.stdout.splitlines()[0]
        return "verificado", first_line.split(":", 1)[0]
    return "auto-reportado", f"token '{token}' no aparece en {src.parent}"


def detector_coverage(description: str, source: str) -> tuple[str, str]:
    """Detecta si la herramienta ``coverage`` está disponible.

    Caso 5 del lab: la afirmación pide ``cobertura > 80 %``. Sin ``coverage``
    no se puede medir; el hunter declara ``bloqueado`` con la razón REAL.

    Importante: la evidencia debe describir el estado verdadero, nunca una
    frase elegida para satisfacer el regex de ``cases.py``. Fabricar el
    mensaje ("command not found" cuando la herramienta sí existe) convierte
    al detector en cómplice del falso verde: el lab pasaría sin medir nada.
    El patrón de ``cases.py`` se ajusta a la razón honesta, no al revés.
    """
    coverage_bin = _resolve_tool("coverage")
    if coverage_bin is None:
        # Estado real: la herramienta no está disponible, no se puede medir.
        return "bloqueado", "coverage no está en PATH ni en el venv del lab (no se puede medir)"
    # Estado real: la herramienta existe pero este detector aún no la usa.
    return "bloqueado", "detector de cobertura >= 80% no implementado (TODO)"


# ---------------------------------------------------------------------------
# Mapa de keywords → detector (declarativo, no procedural).
# ---------------------------------------------------------------------------
# Orden importa: el primer match gana. Si dos keywords están presentes, gana la
# más específica. Esto evita que "tests" se confunda con "cobertura" en una
# afirmación que mencione ambos.

KEYWORD_DISPATCH: list[tuple[str, DetectorFn]] = [
    (r"\bcobertura\b", detector_coverage),
    (r"\btoken\b",     detector_rg_token),
    (r"\btest(s)?\b",  detector_pytest),
]


def pick_detector(description: str) -> DetectorFn:
    """Devuelve el primer detector cuyo patrón matchee en la descripción."""
    for pattern, fn in KEYWORD_DISPATCH:
        if re.search(pattern, description, re.IGNORECASE):
            return fn
    # Fallback honesta: si no reconocemos la keyword, bloqueado con razón.
    return lambda d, s: ("bloqueado", f"sin detector para: '{d[:60]}'")


# ---------------------------------------------------------------------------
# Orquestación
# ---------------------------------------------------------------------------

def run(assertions_path: Path) -> dict:
    """Lee el YAML de aserciones y devuelve el dict de evidencia."""
    text = assertions_path.read_text(encoding="utf-8")
    assertions = parse_assertions_yaml(text)
    details: list[dict] = []
    for a in assertions:
        desc = a.get("description", "").strip()
        src = a.get("source", "").strip()
        if not desc or not src:
            details.append({"status": "bloqueado", "evidence": "afirmación sin description o source"})
            continue
        detector = pick_detector(desc)
        try:
            status, evidence = detector(desc, src)
        except Exception as exc:  # noqa: BLE001
            status, evidence = "bloqueado", f"excepción en detector: {type(exc).__name__}: {exc}"
        details.append({"status": status, "evidence": evidence})
    return {"details": details}


def main() -> int:
    if len(sys.argv) < 2:
        print("evidence-hunter.py <ruta a assertions.yaml>", file=sys.stderr)
        return 2
    yaml_path = Path(sys.argv[1]).expanduser().resolve()
    if not yaml_path.exists():
        print(f"no existe: {yaml_path}", file=sys.stderr)
        return 2
    out = run(yaml_path)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())