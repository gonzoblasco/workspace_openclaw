"""Tests de las puertas del veredicto: bin/emit-verdict.py y bin/verify-verdict.py.

Los dos scripts resuelven el ledger desde su propia ubicacion (`AGENT_DIR/memory/
verdicts.jsonl`), asi que cada test arma un arbol temporal con una COPIA del script
y su propio ledger. Nunca se toca `agents/kanam-critic/memory/verdicts.jsonl`.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EMIT = REPO_ROOT / "bin" / "emit-verdict.py"
VERIFY = REPO_ROOT / "bin" / "verify-verdict.py"

CITATIONS = "\n".join(
    "- src/modulo{}.py:{} salida verificada".format(i, i) for i in range(1, 6)
)


def clean_report(total=20, verdict="Aprobado", extra=""):
    """Reporte que pasa TODAS las validaciones de emit-verdict."""
    return """# Revision sintetica de prueba

Artefacto de prueba con evidencia pegada de punta a punta. El reporte describe el
recorrido completo: se leyo el codigo, se corrieron los tests y se pego la salida
real de cada comando en el bloque de evidencia, sin referencias a corridas previas.

## Evidencia

```
python3 -m pytest tests/ -q
{count} passed
```

{citations}

{extra}

**Total = {total}** -> **{verdict}**.

## Veredicto

Se emite veredicto **{verdict}**: el total {total} cae en la banda de la matriz
SHARP y cada eje tiene su justificacion textual en la tabla de arriba.
""".format(total=total, verdict=verdict, citations=CITATIONS, count=51, extra=extra)


def tree(tmp_path):
    """Arbol temporal con la estructura agents/kanam-critic/{bin,memory,docs}."""
    agent = tmp_path / "agents" / "kanam-critic"
    (agent / "bin").mkdir(parents=True)
    (agent / "memory").mkdir(parents=True)
    (agent / "docs" / "reviews").mkdir(parents=True)
    return agent


def copy_script(agent, script):
    target = agent / "bin" / script.name
    shutil.copy(script, target)
    return target


def run_emit(agent, report, scores=(4, 4, 4, 4, 4), artifact="prueba-emit"):
    report_path = agent / "report.md"
    report_path.write_text(report, encoding="utf-8")
    cmd = [
        sys.executable, str(agent / "bin" / "emit-verdict.py"),
        "--artifact", artifact,
        "--S", str(scores[0]), "--H", str(scores[1]), "--A", str(scores[2]),
        "--R", str(scores[3]), "--P", str(scores[4]),
        "--report", str(report_path),
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def ledger_lines(agent):
    path = agent / "memory" / "verdicts.jsonl"
    if not path.exists():
        return []
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# --------------------------------------------------------------------------
# F32/F33: emit-verdict rechaza evidencia elidida
# --------------------------------------------------------------------------

def test_emit_verdict_report_limpio_registra_exit_0(tmp_path):
    agent = tree(tmp_path)
    copy_script(agent, EMIT)
    result = run_emit(agent, clean_report(total=20))

    assert result.returncode == 0, result.stderr + result.stdout
    assert "GLOBAL=aprobado" in result.stdout
    rows = [json.loads(line) for line in ledger_lines(agent)]
    assert len(rows) == 1 and rows[0]["artifact"] == "prueba-emit"


def test_emit_verdict_omitted_for_brevity_exit_2_sin_escribir_ledger(tmp_path):
    agent = tree(tmp_path)
    copy_script(agent, EMIT)
    report = clean_report(total=20, extra="... (omitted for brevity) ...")
    result = run_emit(agent, report)

    assert result.returncode == 2, result.stdout
    assert "evidencia elidida" in result.stdout
    assert "omitted for brevity" in result.stdout
    assert ledger_lines(agent) == []


def test_emit_verdict_verificado_en_ejecucion_anterior_exit_2(tmp_path):
    agent = tree(tmp_path)
    copy_script(agent, EMIT)
    for phrase in ("(verificado en ejecucion anterior)",
                   "(verificado en una ejecucion anterior)",
                   "verificado anteriormente",
                   "truncado por brevedad",
                   "(sin ejecutar)",
                   "placeholder de evidencia"):
        result = run_emit(agent, clean_report(total=20, extra=phrase))
        assert result.returncode == 2, (phrase, result.stdout)
        assert "evidencia elidida" in result.stdout, phrase
    assert ledger_lines(agent) == []


def test_emit_verdict_puntos_suspensivos_solos_no_bloquean(tmp_path):
    """Un '...' de markdown legitimo (celda truncada por el tool) no es elision."""
    agent = tree(tmp_path)
    copy_script(agent, EMIT)
    report = clean_report(total=20, extra="| S | 4 | salida truncada ... |")
    result = run_emit(agent, report)

    assert result.returncode == 0, result.stderr + result.stdout
    assert len(ledger_lines(agent)) == 1


# --------------------------------------------------------------------------
# F33: verify-verdict exige los cinco ejes con puntaje
# --------------------------------------------------------------------------

def verify_report(total=20, verdict="Aprobado", axes_block="", legacy_note=""):
    return """# Revision sintetica

{legacy_note}

## Evidencia

```
python3 -m pytest tests/ -q
51 passed
```

{citations}

{axes_block}

**Total = {total}** -> **{verdict}**.

## Veredicto

Se emite veredicto **{verdict}**.
""".format(total=total, verdict=verdict, citations=CITATIONS,
           axes_block=axes_block, legacy_note=legacy_note)


def run_verify(agent):
    cmd = [sys.executable, str(agent / "bin" / "verify-verdict.py")]
    return subprocess.run(cmd, capture_output=True, text=True)


def install_verdict(agent, artifact, report_text, total=20):
    (agent / "docs" / "reviews" / "2026-11-19-{}.md".format(artifact)).write_text(
        report_text, encoding="utf-8")
    row = {"artifact": artifact,
           "scores": {"S": 4, "H": 4, "A": 4, "R": 4, "P": 4},
           "total": total, "verdict": "Aprobado",
           "timestamp": "2026-11-19T12:00:00Z",
           "report": "agents/kanam-critic/docs/reviews/2026-11-19-{}.md".format(artifact)}
    (agent / "memory" / "verdicts.jsonl").write_text(
        json.dumps(row) + "\n", encoding="utf-8")


TABLA = """## Evaluacion SHARP

| Eje | Puntaje | Justificacion |
|---|---|---|
| **S (Sharpness)** | 4 | Citas correctas. |
| **H (Horizon)** | 4 | CI. |
| **A (Asymmetry)** | 4 | Sin falsos verdes. |
| **R (Resistance)** | 4 | Borde cubierto. |
| **P (Parsimony)** | 4 | Conciso. |
"""

BULLETS = """## Puntuacion por eje

- **S (Sharpness):** 4 - Citas correctas.
- **H (Horizon):** 4 - CI.
- **A (Asymmetry):** 4 - Sin falsos verdes.
- **R (Resistance):** 4 - Borde cubierto.
- **P (Parsimony)** = 4 - Conciso.
"""


def test_verify_verdict_con_tabla_sharp_pasa(tmp_path):
    agent = tree(tmp_path)
    copy_script(agent, VERIFY)
    install_verdict(agent, "artefacto-nuevo", verify_report(axes_block=TABLA))
    result = run_verify(agent)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "GLOBAL=aprobado" in result.stdout


def test_verify_verdict_acepta_ejes_en_bullets(tmp_path):
    """Parser tolerante: el eje no tiene que estar en tabla."""
    agent = tree(tmp_path)
    copy_script(agent, VERIFY)
    install_verdict(agent, "artefacto-nuevo", verify_report(axes_block=BULLETS))
    result = run_verify(agent)

    assert result.returncode == 0, result.stdout
    assert "GLOBAL=aprobado" in result.stdout


def test_verify_verdict_sin_tabla_sharp_es_invalido(tmp_path):
    agent = tree(tmp_path)
    copy_script(agent, VERIFY)
    install_verdict(agent, "artefacto-nuevo", verify_report(axes_block=""))
    result = run_verify(agent)

    assert result.returncode == 1
    assert "reporte sin tabla SHARP" in result.stdout
    assert "GLOBAL=veto" in result.stdout


def test_verify_verdict_con_un_eje_faltante_es_invalido(tmp_path):
    agent = tree(tmp_path)
    copy_script(agent, VERIFY)
    parcial = "\n".join(line for line in BULLETS.splitlines() if "(Parsimony)" not in line)
    install_verdict(agent, "artefacto-nuevo", verify_report(axes_block=parcial))
    result = run_verify(agent)

    assert result.returncode == 1
    assert "reporte sin tabla SHARP" in result.stdout
    assert "P" in result.stdout


def test_verify_verdict_legacy_sin_tabla_se_informa_y_no_invalida(tmp_path):
    agent = tree(tmp_path)
    copy_script(agent, VERIFY)
    install_verdict(agent, "docs-NORTH", verify_report(axes_block=""))
    result = run_verify(agent)

    assert result.returncode == 0, result.stdout
    assert "LEGACY  docs-NORTH" in result.stdout
    assert "GLOBAL=aprobado" in result.stdout
