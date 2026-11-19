#!/usr/bin/env python3
"""gate-evidence.py — produce la evidencia de un gate SIN narrador.

El juez de un gate no puede inventar evidencia: este programa corre los
comandos declarados en un spec y emite él mismo la tabla de resultados, los
conteos de pytest y un veredicto final. Si un caso no se corrió, no aparece
como PASS. Si el spec no permite verificar nada, es inválido (exit 2).

Contrato de I/O
---------------
INPUT  (JSON, lo escribe quien pide el gate — nunca el juez)::

    {
      "name": "objective-extractor",
      "repo_root": "../..",              # opcional; relativo al spec
      "bin": "agents/kanam-critic/bin/objective-extractor.py",  # opcional
      "pytest": ["agents/kanam-critic/tests/objective-extractor/"],  # opcional
      "cases": [
        {"name": "pipe escapado",
         "cmd": ["python3", "{BIN}", "{TMP}/pipe.md"],
         "files": {"{TMP}/pipe.md": "contenido"},
         "expect_exit": 0,
         "expect_stdout_contains": ["verificado"],
         "expect_stderr_contains": ["RESUMEN: 1 filas"],
         "timeout": 120}
      ]
    }

Sustituciones (en `cmd`, claves y valores de `files`):

  {BIN}   ruta absoluta de `repo_root/bin`
  {TMP}   directorio temporal propio del caso
  {ROOT}  ruta absoluta de `repo_root`

Los `files` se materializan antes de correr el caso. Una clave relativa se
resuelve dentro de {TMP}.

OUTPUT (stdout, markdown canónico; con `--json`, un objeto JSON)::

    ## Evidencia de gate — <name> <timestamp ISO>
    | Caso | exit esperado | exit real | stdout | stderr | resultado |
    ...
    ### pytest
    ...
    GATE-EVIDENCE: PASS (X casos, Y tests)   # o FAIL (motivo)

Exit codes:
  0  todos los casos coinciden en exit y en los `contains`, y toda suite de
     pytest pasa con al menos un test colectado.
  1  al menos un caso o suite de pytest falla (se reporta, no se oculta).
  2  spec inválido: JSON ilegible, caso sin `expect_exit`, lista de
     expectativas vacía, claves desconocidas, etc.

REGLA DURA: una expectativa ausente o vacía NO es una aprobación. Por eso
`expect_exit` es obligatorio y una lista presente pero vacía invalida el spec.

Diseño: stdlib puro, mapa declarativo de claves conocidas, sin estado global.
Misma spec ⇒ mismo veredicto (el timestamp cambia; el veredicto no).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

SPEC_KEYS = {"name", "repo_root", "bin", "pytest", "cases", "description"}
CASE_KEYS = {
    "name",
    "cmd",
    "files",
    "expect_exit",
    "expect_stdout_contains",
    "expect_stderr_contains",
    "timeout",
}
DEFAULT_TIMEOUT = 120
STREAM_PREVIEW_LINES = 20
CELL_LIMIT = 300


class SpecError(Exception):
    """Spec ilegible o inseguro: no se puede emitir un veredicto honesto."""


# ---------------------------------------------------------------------------
# Validación
# ---------------------------------------------------------------------------

def _nonempty_str(value, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SpecError(f"{where} debe ser un string no vacío")
    return value


def _str_list(value, where: str, *, allow_empty: bool = False) -> list:
    if not isinstance(value, list):
        raise SpecError(f"{where} debe ser una lista de strings")
    if not value and not allow_empty:
        raise SpecError(f"{where} está vacía: una expectativa vacía no verifica nada")
    out = []
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item:
            raise SpecError(f"{where}[{i}] debe ser un string no vacío")
        out.append(item)
    return out


def _normalize_case(raw, idx: int) -> dict:
    where = f"spec.cases[{idx}]"
    if not isinstance(raw, dict):
        raise SpecError(f"{where} debe ser un objeto JSON")

    unknown = set(raw) - CASE_KEYS
    if unknown:
        raise SpecError(
            f"{where} tiene claves desconocidas: {', '.join(sorted(unknown))}"
        )

    name = _nonempty_str(raw.get("name"), f"{where}.name")
    cmd = _str_list(raw.get("cmd"), f"{where}.cmd")

    if "expect_exit" not in raw:
        raise SpecError(
            f"{where}.expect_exit es obligatorio: un caso sin exit esperado "
            f"no verifica nada (no se acepta 'ver qué pasa')"
        )
    expect_exit = raw["expect_exit"]
    if isinstance(expect_exit, bool) or not isinstance(expect_exit, int):
        raise SpecError(f"{where}.expect_exit debe ser un entero")

    stdout_contains = []
    if "expect_stdout_contains" in raw:
        stdout_contains = _str_list(
            raw["expect_stdout_contains"], f"{where}.expect_stdout_contains"
        )
    stderr_contains = []
    if "expect_stderr_contains" in raw:
        stderr_contains = _str_list(
            raw["expect_stderr_contains"], f"{where}.expect_stderr_contains"
        )

    files = {}
    if "files" in raw:
        raw_files = raw["files"]
        if not isinstance(raw_files, dict):
            raise SpecError(f"{where}.files debe ser un objeto {{ruta: contenido}}")
        for key, value in raw_files.items():
            if not isinstance(key, str) or not key:
                raise SpecError(f"{where}.files tiene una clave no válida")
            if not isinstance(value, str):
                raise SpecError(f"{where}.files[{key!r}] debe ser un string")
            files[key] = value

    timeout = raw.get("timeout", DEFAULT_TIMEOUT)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
        raise SpecError(f"{where}.timeout debe ser un número > 0")

    return {
        "name": name,
        "cmd": cmd,
        "files": files,
        "expect_exit": expect_exit,
        "expect_stdout_contains": stdout_contains,
        "expect_stderr_contains": stderr_contains,
        "timeout": timeout,
    }


def normalize_spec(raw, spec_path: Path) -> dict:
    if not isinstance(raw, dict):
        raise SpecError("el spec debe ser un objeto JSON")

    unknown = set(raw) - SPEC_KEYS
    if unknown:
        raise SpecError(
            f"claves desconocidas en el spec: {', '.join(sorted(unknown))}"
        )

    name = raw.get("name")
    if name is None:
        name = spec_path.stem
    else:
        name = _nonempty_str(name, "spec.name")

    spec_dir = spec_path.parent.resolve()
    repo_root = None
    if "repo_root" in raw:
        root_value = _nonempty_str(raw["repo_root"], "spec.repo_root")
        root_path = Path(root_value).expanduser()
        if not root_path.is_absolute():
            root_path = spec_dir / root_path
        repo_root = root_path.resolve()
        if not repo_root.is_dir():
            raise SpecError(f"spec.repo_root no es un directorio: {repo_root}")

    bin_rel = None
    if "bin" in raw:
        bin_rel = _nonempty_str(raw["bin"], "spec.bin")
    if bin_rel is not None and repo_root is None:
        raise SpecError("spec.bin requiere spec.repo_root")

    pytest_paths = None
    if "pytest" in raw:
        pytest_paths = _str_list(raw["pytest"], "spec.pytest")

    raw_cases = raw.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise SpecError("spec.cases debe ser una lista no vacía")
    cases = [_normalize_case(c, i) for i, c in enumerate(raw_cases)]

    uses_bin = False
    uses_root = False
    for case in cases:
        texts = list(case["cmd"]) + list(case["files"].keys()) + list(case["files"].values())
        for text in texts:
            if "{BIN}" in text:
                uses_bin = True
            if "{ROOT}" in text:
                uses_root = True

    if uses_bin and bin_rel is None:
        raise SpecError("{BIN} requiere spec.bin y spec.repo_root")
    if uses_root and repo_root is None:
        raise SpecError("{ROOT} requiere spec.repo_root")

    bin_path = (repo_root / bin_rel).resolve() if bin_rel is not None else None

    return {
        "name": name,
        "spec_dir": spec_dir,
        "repo_root": repo_root,
        "bin_path": bin_path,
        "pytest": pytest_paths,
        "cases": cases,
    }


def load_spec(spec_path: Path) -> dict:
    try:
        text = spec_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SpecError(f"no se pudo leer el spec {spec_path}: {exc}")
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SpecError(f"spec no es JSON válido: {exc}")
    return normalize_spec(raw, spec_path)


# ---------------------------------------------------------------------------
# Ejecución
# ---------------------------------------------------------------------------

def _substitute(text: str, subs: dict) -> str:
    for key in ("{BIN}", "{ROOT}", "{TMP}"):
        if key in subs:
            text = text.replace(key, subs[key])
    return text


def _as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return value


def run_case(case: dict, ctx: dict) -> dict:
    tmp_dir = Path(tempfile.mkdtemp(prefix="gate-evidence-")).resolve()
    subs = {"{TMP}": str(tmp_dir)}
    if ctx["repo_root"] is not None:
        subs["{ROOT}"] = str(ctx["repo_root"])
    if ctx["bin_path"] is not None:
        subs["{BIN}"] = str(ctx["bin_path"])

    result = {
        "name": case["name"],
        "expect_exit": case["expect_exit"],
        "exit": None,
        "stdout": "",
        "stderr": "",
        "failures": [],
        "passed": False,
    }

    try:
        for rel_path, content in case["files"].items():
            target = Path(_substitute(rel_path, subs))
            if not target.is_absolute():
                target = tmp_dir / target
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(_substitute(content, subs), encoding="utf-8")

        cmd = [_substitute(part, subs) for part in case["cmd"]]
        result["cmd"] = cmd
        cwd = ctx["repo_root"] if ctx["repo_root"] is not None else ctx["spec_dir"]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(cwd),
                timeout=case["timeout"],
            )
            result["exit"] = proc.returncode
            result["stdout"] = proc.stdout or ""
            result["stderr"] = proc.stderr or ""
        except subprocess.TimeoutExpired as exc:
            result["stdout"] = _as_text(exc.stdout)
            result["stderr"] = _as_text(exc.stderr) + (
                f"\n[gate-evidence] timeout tras {case['timeout']}s"
            )
            result["failures"].append(
                f"timeout tras {case['timeout']}s (esperaba exit {case['expect_exit']})"
            )
        except OSError as exc:
            result["stderr"] = f"[gate-evidence] no se pudo ejecutar {cmd[0]!r}: {exc}"
            result["failures"].append(f"no se pudo ejecutar: {exc}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    if result["exit"] != case["expect_exit"]:
        real = "N/A" if result["exit"] is None else result["exit"]
        result["failures"].append(
            f"exit real {real} != esperado {case['expect_exit']}"
        )

    for expected in case["expect_stdout_contains"]:
        if expected not in result["stdout"]:
            result["failures"].append(f"stdout no contiene {expected!r}")
    for expected in case["expect_stderr_contains"]:
        if expected not in result["stderr"]:
            result["failures"].append(f"stderr no contiene {expected!r}")

    result["passed"] = not result["failures"] and result["exit"] is not None
    return result


PYTEST_COUNT_RE = {
    "passed": re.compile(r"(\d+) passed"),
    "failed": re.compile(r"(\d+) failed"),
    "errors": re.compile(r"(\d+) errors?"),
}


def _parse_pytest_counts(text: str) -> dict:
    counts = {"passed": 0, "failed": 0, "errors": 0}
    for key, pattern in PYTEST_COUNT_RE.items():
        match = pattern.search(text)
        if match:
            counts[key] = int(match.group(1))
    return counts


def _parse_pytest_junit(xml_path: Path) -> dict | None:
    """Cuenta tests desde el JUnit XML de pytest.

    El repo configura `addopts = -q`; sumarle nuestro `-q` da `-qq`, que
    suprime la línea "N passed". El XML no depende de la verbosidad ni del
    summary, así que es la fuente de verdad de los conteos.
    """
    if not xml_path.is_file():
        return None
    try:
        import xml.etree.ElementTree as ET

        root = ET.parse(xml_path).getroot()
    except Exception:  # noqa: BLE001
        return None

    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    if not suites:
        return None
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for suite in suites:
        for key in totals:
            try:
                totals[key] += int(suite.get(key, "0") or 0)
            except ValueError:
                return None
    totals["passed"] = max(
        totals["tests"] - totals["failures"] - totals["errors"] - totals["skipped"],
        0,
    )
    return totals


def run_pytest_suites(paths: list, ctx: dict) -> dict:
    suites = []
    total_passed = 0
    total_failed = 0
    ok = True

    cwd = ctx["repo_root"] if ctx["repo_root"] is not None else ctx["spec_dir"]
    for path in paths:
        junit_dir = Path(tempfile.mkdtemp(prefix="gate-evidence-pytest-"))
        junit_path = junit_dir / "report.xml"
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            f"--junitxml={junit_path}",
            path,
        ]
        entry = {"path": path, "cmd": cmd, "exit": None, "stdout": "", "stderr": "",
                 "passed": 0, "failed": 0, "ok": False, "label": ""}
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(cwd), timeout=1800
            )
            entry["exit"] = proc.returncode
            entry["stdout"] = proc.stdout or ""
            entry["stderr"] = proc.stderr or ""
        except subprocess.TimeoutExpired:
            entry["stderr"] = "[gate-evidence] timeout tras 1800s"
        except OSError as exc:
            entry["stderr"] = f"[gate-evidence] no se pudo ejecutar pytest: {exc}"

        xml_counts = _parse_pytest_junit(junit_path)
        shutil.rmtree(junit_dir, ignore_errors=True)
        if xml_counts is not None:
            counts = {
                "passed": xml_counts["passed"],
                "failed": xml_counts["failures"],
                "errors": xml_counts["errors"],
            }
        else:
            counts = _parse_pytest_counts(entry["stdout"] + "\n" + entry["stderr"])
        entry["passed"] = counts["passed"]
        entry["failed"] = counts["failed"]
        total_passed += counts["passed"]
        total_failed += counts["failed"]

        if entry["exit"] == 0 and counts["failed"] == 0 and counts["passed"] > 0:
            entry["ok"] = True
            entry["label"] = f"{counts['passed']} passed"
        else:
            ok = False
            if counts["failed"] or counts["errors"]:
                bad = counts["failed"] + counts["errors"]
                entry["label"] = f"{bad} failed"
            elif entry["exit"] == 5:
                entry["label"] = "sin tests colectados (no verifica nada)"
            else:
                entry["label"] = (
                    f"error de pytest (exit {entry['exit']})"
                    if entry["exit"] is not None
                    else "pytest no se pudo ejecutar"
                )

        suites.append(entry)

    return {
        "declared": paths,
        "suites": suites,
        "passed": total_passed,
        "failed": total_failed,
        "ok": ok,
    }


def build_result(spec: dict) -> dict:
    ctx = {
        "repo_root": spec["repo_root"],
        "bin_path": spec["bin_path"],
        "spec_dir": spec["spec_dir"],
    }

    case_results = [run_case(case, ctx) for case in spec["cases"]]
    pytest_result = run_pytest_suites(spec["pytest"] or [], ctx)

    failing_cases = [c["name"] for c in case_results if not c["passed"]]
    all_pass = not failing_cases and pytest_result["ok"]

    if all_pass:
        verdict = "PASS"
        reason = ""
    else:
        reasons = []
        if failing_cases:
            reasons.append(
                f"{len(failing_cases)} caso(s) fallido(s): {', '.join(failing_cases)}"
            )
        if pytest_result["declared"] and not pytest_result["ok"]:
            labels = "; ".join(
                f"{s['path']}: {s['label']}" for s in pytest_result["suites"]
            )
            reasons.append(f"pytest: {labels}")
        verdict = "FAIL"
        reason = " | ".join(reasons)

    return {
        "spec": spec["name"],
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "cases": case_results,
        "pytest": pytest_result,
        "verdict": verdict,
        "reason": reason,
        "exit_code": 0 if all_pass else 1,
    }


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def _cell(text: str, limit: int = CELL_LIMIT) -> str:
    if not text.strip():
        return "_(vacío)_"
    flat = text.replace("\r\n", "\n").replace("\n", " ⏎ ").replace("|", "\\|").rstrip()
    if len(flat) > limit:
        flat = flat[:limit] + "…"
    return flat


def _fence(text: str) -> list:
    body = "\n".join(text.splitlines()[:STREAM_PREVIEW_LINES])
    return ["````text", body, "````"]


def render_markdown(result: dict) -> str:
    lines = [f"## Evidencia de gate — {result['spec']} {result['timestamp']}", ""]
    lines.append("| Caso | exit esperado | exit real | stdout | stderr | resultado |")
    lines.append("|---|---|---|---|---|---|")
    for case in result["cases"]:
        real_exit = "N/A" if case["exit"] is None else case["exit"]
        lines.append(
            "| {} | {} | {} | {} | {} | {} |".format(
                _cell(case["name"]),
                case["expect_exit"],
                real_exit,
                _cell(case["stdout"]),
                _cell(case["stderr"]),
                "PASS" if case["passed"] else "FAIL",
            )
        )
    lines.append("")

    failing = [c for c in result["cases"] if not c["passed"]]
    if failing:
        lines.append("### Fallos")
        for case in failing:
            lines.append(f"- **{case['name']}**: " + "; ".join(case["failures"]))
        lines.append("")

    lines.append(
        f"<details><summary>stdout / stderr por caso "
        f"(primeras {STREAM_PREVIEW_LINES} líneas)</summary>"
    )
    lines.append("")
    for case in result["cases"]:
        lines.append(f"**{case['name']} — stdout**")
        lines.append("")
        lines.extend(_fence(case["stdout"]))
        lines.append("")
        lines.append(f"**{case['name']} — stderr**")
        lines.append("")
        lines.extend(_fence(case["stderr"]))
        lines.append("")
    lines.append("</details>")
    lines.append("")

    lines.append("### pytest")
    lines.append("")
    pytest_result = result["pytest"]
    if not pytest_result["declared"]:
        lines.append("_Sin suites declaradas en el spec._")
    else:
        for suite in pytest_result["suites"]:
            lines.append(
                f"- `{suite['path']}` → **{suite['label']}** (rc={suite['exit']})"
            )
        lines.append("")
        lines.append(
            f"Total: {pytest_result['passed']} passed, "
            f"{pytest_result['failed']} failed."
        )
        broken = [s for s in pytest_result["suites"] if not s["ok"]]
        if broken:
            lines.append("")
            lines.append("<details><summary>salida de pytest con fallos</summary>")
            lines.append("")
            for suite in broken:
                lines.append(f"**{suite['path']}**")
                lines.append("")
                lines.extend(_fence(suite["stdout"] + "\n" + suite["stderr"]))
                lines.append("")
            lines.append("</details>")
    lines.append("")

    if result["verdict"] == "PASS":
        lines.append(
            f"GATE-EVIDENCE: PASS ({len(result['cases'])} casos, "
            f"{pytest_result['passed']} tests)"
        )
    else:
        lines.append(f"GATE-EVIDENCE: FAIL ({result['reason']})")
    return "\n".join(lines) + "\n"


def render_json(result: dict) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Corre los casos de un gate y emite la evidencia canónica."
    )
    parser.add_argument("--spec", required=True, type=Path, help="ruta al spec JSON")
    parser.add_argument(
        "--json", action="store_true", help="emitir JSON en vez de markdown"
    )
    args = parser.parse_args(argv)

    spec_path = args.spec.expanduser().resolve()
    try:
        spec = load_spec(spec_path)
    except SpecError as exc:
        print(f"gate-evidence: spec inválida: {exc}", file=sys.stderr)
        if args.json:
            sys.stdout.write(
                json.dumps(
                    {"verdict": "SPEC-INVALIDA", "reason": str(exc), "exit_code": 2},
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n"
            )
        else:
            print(f"GATE-EVIDENCE: SPEC-INVALIDA ({exc})")
        return 2

    result = build_result(spec)
    sys.stdout.write(render_json(result) if args.json else render_markdown(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
