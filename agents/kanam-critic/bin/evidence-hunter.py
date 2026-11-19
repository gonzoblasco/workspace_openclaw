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
import ast
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


TOKEN_SHAPE = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)+")


def _extract_token(description: str) -> tuple[str | None, str]:
    """Devuelve (token, razon) del token que la descripcion afirma.

    Regla: solo se considera lo que sigue a la palabra 'token' y solo si tiene
    FORMA de token (kebab-case o snake_case con separador). Si hay mas de un
    candidato, es ambiguo: no se elige uno a dedo (elegir seria fabricar
    evidencia). Medido el 2026-11-06: la asercion "El kit usa el token de
    diseño kana-critical en sus estilos" devolvia `verificado` con la cita
    `bin/record_verdict.py` porque el detector tomaba la preposicion 'de' y
    la encontraba en cualquier lado del repo.
    """
    cands: list[str] = []
    for line in description.splitlines():
        low = line.lower()
        idx = low.find("token")
        if idx == -1:
            continue
        tail = line[idx + len("token"):]
        cands.extend(TOKEN_SHAPE.findall(tail))
    uniq = list(dict.fromkeys(cands))
    if not uniq:
        return None, ("el texto tras 'token' no contiene un token con forma "
                      "(se espera kebab-case o snake_case, tipo 'color-primary'); "
                      "no se puede verificar")
    if len(uniq) > 1:
        return None, (f"la asercion menciona {len(uniq)} tokens posibles "
                      f"({', '.join(uniq)}); es ambigua y no se puede verificar")
    return uniq[0], ""


def detector_rg_token(description: str, source: str) -> tuple[str, str]:
    """Detecta si un token mencionado en la descripción aparece en un archivo de estilos.

    Estrategia:
      1. Extrae el token: la palabra que sigue a 'token', SOLO si tiene forma de token
         (kebab-case o snake_case con separador, tipo `color-primary`). Si lo que sigue
         a 'token' es una palabra comun ("el token **de** diseño ..."), NO hay token
         que verificar: el detector declara `bloqueado` con la razón real. Antes este
         detector tomaba cualquier palabra (incluso 'de'), la buscaba con rg y
         devolvía `verificado` si la palabra aparecia en cualquier lado del repo: un
         verificado fabricado. Medido el 2026-11-06 con la aserción "El kit usa el
         token de diseño kana-critical": devolvio `verificado` con la cita
         `bin/record_verdict.py`, cuando lo unico que habia encontrado era la
         preposición 'de'.
      2. Si `rg` está en PATH, lo usa. Si no, hace fallback a `grep -R`.
      3. Si no encuentra el token → auto-reportado.
      4. Si lo encuentra → verificado con la ruta de la primera coincidencia.
    """
    src = Path(source)
    if not src.exists():
        return "auto-reportado", f"source no existe: {source}"

    token, reason = _extract_token(description)
    if token is None:
        return "bloqueado", reason

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
# Detector horizon — grafo de imports y ciclos (T4.2)
# ---------------------------------------------------------------------------
# Afirmaciones del tipo "no hay imports circulares entre los modulos de X" o
# "el modulo Y no depende de Z". Un `grep import` NO ve un ciclo (ve lineas
# sueltas); hay que resolver los imports a modulos del paquete y recorrer el
# grafo. Todo con `ast` (stdlib): cero dependencias.

HORIZON_SKIP_DIRS = {"__pycache__", "node_modules"}


def _iter_py_files(root: Path) -> list[Path]:
    """Devuelve los .py bajo `root`, sin directorios ocultos ni de build."""
    files: list[Path] = []
    for p in sorted(root.rglob("*.py")):
        rel_parts = p.relative_to(root).parts
        if any(part.startswith(".") or part in HORIZON_SKIP_DIRS for part in rel_parts):
            continue
        files.append(p)
    return files


def _module_name(path: Path, root: Path) -> tuple[str, bool]:
    """Nombre punteado del modulo relativo a `root` y si es un paquete."""
    parts = list(path.relative_to(root).with_suffix("").parts)
    is_package = parts[-1] == "__init__"
    if is_package:
        parts = parts[:-1]
    return ".".join(parts), is_package


def _build_module_index(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for py in _iter_py_files(root):
        name, _ = _module_name(py, root)
        if name:
            index[name] = py
    return index


def _candidate_variants(cand: str, root_pkg: str | None) -> list[str]:
    """Variantes de un path punteado a probar contra el indice.

    El indice se construye relativo al `root`. Si el `root` ES el paquete
    analizado (p. ej. `.../pkg`), un import absoluto `from pkg import b`
    apunta a `pkg.b`, pero en el indice el modulo vive como `b`: se prueba
    tambien la variante sin el primer componente cuando coincide con el
    nombre del root.
    """
    variants = [cand]
    head, _, rest = cand.partition(".")
    if root_pkg and rest and head == root_pkg:
        variants.append(rest)
    return variants


def _import_targets(
    node: ast.stmt,
    module: str,
    is_package: bool,
    index: dict[str, Path],
    root_pkg: str | None = None,
) -> tuple[list[str], int]:
    """Resuelve un `ast.Import`/`ast.ImportFrom` a modulos presentes en `index`.

    Devuelve `(targets, unresolved)`: los modulos destino dentro del root y
    cuantos imports de la sentencia NO se pudieron resolver a un modulo
    interno (paquetes de la stdlib, terceros, alias dinamicos...).

    Un import absoluto se resuelve contra el indice tal cual: con root
    `/tmp/cic`, `from pkg import b` produce el candidato `pkg.b`, que existe
    en el indice porque `pkg/b.py` esta bajo el root. Antes de este fix solo
    se resolvian los relativos y un ciclo por imports absolutos pasaba como
    "sin ciclos" (falso verde).
    """
    if isinstance(node, ast.Import):
        candidates = [alias.name for alias in node.names]
    elif isinstance(node, ast.ImportFrom):
        if node.level:
            # Relativo: se parte del paquete del modulo actual.
            pkg_parts = module.split(".") if is_package else module.split(".")[:-1]
            up = node.level - 1
            if up > len(pkg_parts):
                return [], 1
            pkg_parts = pkg_parts[: len(pkg_parts) - up]
            base = pkg_parts + (node.module.split(".") if node.module else [])
        else:
            # Absoluto: el path punteado ya es completo desde la raiz del
            # arbol de imports (`from pkg import b` -> `pkg.b`).
            base = node.module.split(".") if node.module else []
        candidates = [".".join(base)] if base else []
        candidates += [".".join(base + [alias.name]) for alias in node.names]
    else:
        return [], 0

    seen: list[str] = []
    resolved = False
    for cand in candidates:
        if not cand:
            continue
        for variant in _candidate_variants(cand, root_pkg):
            if variant not in index:
                continue
            resolved = True
            if variant != module and variant not in seen:
                seen.append(variant)
            break
    return seen, 0 if resolved else 1


def _import_label(node: ast.stmt) -> str:
    """Texto legible del import para citarlo en la evidencia."""
    if isinstance(node, ast.Import):
        return "import " + ", ".join(alias.name for alias in node.names)
    names = ", ".join(alias.name for alias in node.names)
    dots = "." * getattr(node, "level", 0)
    module = getattr(node, "module", None) or ""
    return f"from {dots}{module} import {names}"


def _collect_horizon_graph(
    root: Path, index: dict[str, Path]
) -> tuple[
    dict[str, list[tuple[str, str, int]]],
    list[tuple[str, int, str]],
    list[tuple[str, int, str]],
]:
    """Grafo modulo -> [(target, archivo, linea)], errores de sintaxis e
    imports no resueltos [(archivo, linea, path punteado)].
    """
    graph: dict[str, list[tuple[str, str, int]]] = {name: [] for name in index}
    syntax_errors: list[tuple[str, int, str]] = []
    unresolved: list[tuple[str, int, str]] = []
    root_pkg = root.name if root.name.isidentifier() else None
    for module, path in index.items():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            syntax_errors.append((str(path), exc.lineno or 0, exc.msg))
            continue
        except (OSError, UnicodeDecodeError) as exc:
            syntax_errors.append((str(path), 0, str(exc)))
            continue
        _, is_package = _module_name(path, root)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            targets, not_resolved = _import_targets(
                node, module, is_package, index, root_pkg
            )
            if not_resolved:
                unresolved.append((str(path), node.lineno, _import_label(node)))
            for target in targets:
                graph[module].append((target, str(path), node.lineno))
    return graph, syntax_errors, unresolved


def _find_cycle(
    graph: dict[str, list[tuple[str, str, int]]],
) -> tuple[list[str], tuple[str, str, int]] | None:
    """DFS con colores. Devuelve (camino del ciclo, arista que lo cierra)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    parent: dict[str, str] = {}

    def visit(node: str) -> tuple[list[str], tuple[str, str, int]] | None:
        color[node] = GRAY
        for edge in graph[node]:
            target = edge[0]
            if color.get(target, WHITE) == GRAY:
                chain = [node]
                cur = node
                while cur != target and cur in parent:
                    cur = parent[cur]
                    chain.append(cur)
                chain.reverse()
                return chain + [target], edge
            if color.get(target, WHITE) == WHITE:
                parent[target] = node
                found = visit(target)
                if found:
                    return found
        color[node] = BLACK
        return None

    for name in graph:
        if color[name] == WHITE:
            found = visit(name)
            if found:
                return found
    return None


def detector_horizon(description: str, source: str) -> tuple[str, str]:
    """Verifica afirmaciones sobre la estructura de dependencias.

    Estados:
      - verificado     → el grafo se pudo armar, NO tiene ciclos y hay al
                         menos un import interno resuelto (o no hay imports).
                         Cita el ultimo import interno (archivo:linea) y
                         declara cuantos imports quedaron sin resolver.
      - auto-reportado → hay un ciclo: la afirmacion del autor no se sostiene.
                         Cita el import que cierra el ciclo.
      - bloqueado      → sintaxis rota / no hay .py que analizar / TODOS los
                         imports quedaron sin resolver (un grafo vacio no
                         prueba ausencia de ciclos).

    Honestidad de la cita: "sin imports internos" solo se emite cuando el
    codigo realmente no tiene imports. Un archivo con `import os` no puede
    reportarse como "sin imports": se informa "N externos/no resueltos".
    """
    src = Path(source)
    if not src.exists():
        return "auto-reportado", f"source no existe: {source}"
    root = src if src.is_dir() else src.parent
    index = _build_module_index(root)
    if not index:
        return "bloqueado", f"no hay modulos .py bajo {root}"

    graph, syntax_errors, unresolved = _collect_horizon_graph(root, index)
    if syntax_errors:
        path, line, msg = syntax_errors[0]
        return "bloqueado", f"sintaxis rota en {path}:{line}: {msg}"

    cycle = _find_cycle(graph)
    if cycle is not None:
        chain, (target, path, line) = cycle
        return "auto-reportado", (
            f"{path}:{line} el import de '{target}' cierra un ciclo "
            f"({' -> '.join(chain)})"
        )

    edges = sorted(
        (path, line) for node in graph for _, path, line in graph[node]
    )
    n_edges = len(edges)
    n_unres = len(unresolved)
    if edges:
        path, line = edges[-1]
        return "verificado", (
            f"{path}:{line} sin ciclos ({len(index)} modulos, "
            f"{n_edges} imports internos, {n_unres} externos/no resueltos)"
        )
    if n_unres:
        # Sin aristas internas y con imports que no se pudieron resolver: el
        # grafo vacio NO prueba ausencia de ciclos. Estado honesto: bloqueado.
        path, line, label = unresolved[0]
        return "bloqueado", (
            f"{path}:{line} {n_unres} imports externos/no resueltos, "
            f"0 internos ({label}); un grafo vacio no prueba ausencia de ciclos"
        )
    # Cero imports en todo el root: no hay arista que pueda formar un ciclo.
    root_module = sorted(index)[0]
    return "verificado", (
        f"{index[root_module]}:1 sin ciclos ({len(index)} modulos, 0 imports)"
    )


# ---------------------------------------------------------------------------
# Detector resistance — cobertura declarativa de casos borde (T4.2)
# ---------------------------------------------------------------------------
# Afirmaciones del tipo "los casos borde estan cubiertos" o "hay tests para
# entradas invalidas". Los patrones viven en el mapa, no en if/elif: agregar
# una senal de caso borde es una entrada mas.

EDGE_PATTERNS: list[tuple[str, str]] = [
    ("raises",            r"pytest\.raises|unittest\.TestCase\.assertRaises"),
    ("parametrize",       r"@pytest\.mark\.parametrize|@parameterized\.expand"),
    ("edge_case_name",    r"def\s+test_\w*(empty|invalid|none|null|edge|boundary|error|zero|missing)\w*\s*\("),
    ("exception_assert",  r"assertRaises|with\s+raises\("),
]
MIN_EDGE_PATTERNS = 2


def _find_test_files(source: Path) -> list[Path]:
    """Localiza los test_*.py relevantes al `source`."""
    if source.is_dir():
        return sorted(source.rglob("test_*.py"))
    if source.name.startswith("test_") and source.suffix == ".py":
        return [source]
    candidates = sorted(source.parent.glob("test_*.py"))
    tests_dir = source.parent / "tests"
    if tests_dir.exists():
        candidates += sorted(tests_dir.rglob("test_*.py"))
    return candidates


def detector_resistance(description: str, source: str) -> tuple[str, str]:
    """Verifica si los tests cubren casos borde, con patrones declarativos.

    Estados:
      - verificado     → al menos MIN_EDGE_PATTERNS patrones DISTINTOS
                         presentes. Cita archivo:linea del primero.
      - auto-reportado → hay tests pero solo camino feliz.
      - auto-reportado → no hay tests.
    """
    src = Path(source)
    if not src.exists():
        return "auto-reportado", f"source no existe: {source}"

    test_files = _find_test_files(src)
    if not test_files:
        return "auto-reportado", f"sin tests para {source}"

    hits: list[tuple[str, int, str]] = []
    total_tests = 0
    for tf in test_files:
        try:
            lines = tf.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError) as exc:
            return "bloqueado", f"no se pudo leer {tf}: {exc}"
        total_tests += sum(1 for ln in lines if re.match(r"\s*def\s+test_", ln))
        for label, pattern in EDGE_PATTERNS:
            if any(label == h[2] for h in hits):
                continue
            for lineno, line in enumerate(lines, start=1):
                if re.search(pattern, line):
                    hits.append((str(tf), lineno, label))
                    break

    if len(hits) >= MIN_EDGE_PATTERNS:
        path, line, label = hits[0]
        labels = ", ".join(h[2] for h in hits)
        return "verificado", f"{path}:{line} patrones de borde: {labels}"

    first = test_files[0]
    return "auto-reportado", (
        f"solo camino feliz, sin casos borde ({total_tests} tests en {first})"
    )


# ---------------------------------------------------------------------------
# Mapa de keywords → detector (declarativo, no procedural).
# ---------------------------------------------------------------------------
# Orden importa: el primer match gana. Si dos keywords están presentes, gana la
# más específica. Esto evita que "tests" se confunda con "cobertura" en una
# afirmación que mencione ambos.

KEYWORD_DISPATCH: list[tuple[str, DetectorFn]] = [
    (r"\bcobertura\b",              detector_coverage),
    (r"\btoken\b",                  detector_rg_token),
    # Horizon: SOLO afirmaciones de ESTRUCTURA de dependencias. Un `\bdependencias?\b`
    # suelto ("las dependencias estan actualizadas") no es una afirmación sobre
    # ciclos y devolver `verificado` por un grafo acíclico sería un verde fabricado.
    (r"(imports?|dependencias?)\s+circulares?|circulares?\b.*\b(import|depend)|"
     r"\bno\s+depende\s+de\b|\bdepende\s+de\b|\bacoplamiento\b", detector_horizon),
    (r"casos?\s+borde|casos?\s+l[ií]mite|entradas?\s+inv[aá]lidas?|camino\s+feliz",
     detector_resistance),
    (r"\btest(s)?\b",               detector_pytest),
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