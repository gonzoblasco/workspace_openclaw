"""Tests de bin/format_sharp_report.py.

Se invoca el script como subproceso: lo que importa es el contrato del CLI
(exit code, stdout/stderr y efectos en disco), no los helpers internos.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "bin" / "format_sharp_report.py"

SHARP_ROWS = [
    ("**S (Sharpness)**", 5, "Todos los casos reportan estado y cita correctos."),
    ("**H (Horizon)**", 5, "Incluye deteccion de ciclos en CI."),
    ("**A (Asymmetry)**", 4, "Evita falsos verdes en el caso de imports absolutos."),
    ("**R (Resistance)**", 5, "Pruebas de borde verificadas."),
    ("**P (Parsimony)**", 4, "Implementacion concisa."),
]


def make_report(total=23, verdict="Aprobado", axes=None, evidence="```\npytest -q\n30 passed\n```",
                frictions=None):
    axes = axes or {row[0][2]: row[1] for row in SHARP_ROWS}
    lines = ["# Revision de prueba", "", "## Evaluacion SHARP", "",
             "| Eje | Puntuacion (1-5) | Comentario |", "|---|---|---|"]
    for label, score, comment in SHARP_ROWS:
        axis = label[2]
        lines.append("| {} | {} | {} |".format(label, axes[axis], comment))
    lines.append("")
    lines.append("**Total = {}** -> **{}**.".format(total, verdict))
    lines.append("")
    lines.append("## Veredicto")
    lines.append("")
    lines.append("Se emite veredicto **{}**.".format(verdict))
    lines.append("")
    lines.append("## Evidencia")
    lines.append("")
    lines.append(evidence)
    lines.append("")
    if frictions is not None:
        lines.append("## Fricciones")
        lines.append("")
        lines.extend("- {}".format(item) for item in frictions)
        lines.append("")
    return "\n".join(lines)


def make_ledger(path, artifact="demo", total=23, verdict="Aprobado", scores=None,
                status=None):
    scores = scores or {"S": 5, "H": 5, "A": 4, "R": 5, "P": 4}
    row = {
        "artifact": artifact,
        "scores": scores,
        "total": total,
        "verdict": verdict,
        "notes": "",
        "timestamp": "2026-11-19T15:20:50.636930Z",
    }
    if status:
        row["status"] = status
    path.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def run(tmp_path, report_text, ledger_path, artifact="demo", extra=None):
    report_path = tmp_path / "report.md"
    report_path.write_text(report_text, encoding="utf-8")
    cmd = [
        sys.executable, str(SCRIPT),
        "--report", str(report_path),
        "--ledger", str(ledger_path),
        "--artifact", artifact,
    ] + (extra or [])
    return subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)


def test_cuerpo_valido_con_veredicto_y_cinco_filas(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    result = run(tmp_path, make_report(), ledger)

    assert result.returncode == 0, result.stderr
    first = result.stdout.splitlines()[0]
    assert first == "**Veredicto: Aprobado 23/25** (S5 H5 A4 R5 P4)"
    for axis, label in [("S", "Sharpness"), ("H", "Horizon"), ("A", "Asymmetry"),
                        ("R", "Resistance"), ("P", "Parsimony")]:
        assert "| {} ({}) |".format(axis, label) in result.stdout
    assert "Todos los casos reportan estado y cita correctos." in result.stdout
    assert "<details>" in result.stdout


def test_total_distinto_falla_exit_2_con_detalle(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl", total=23)
    result = run(tmp_path, make_report(total=21), ledger)

    assert result.returncode == 2
    assert "total" in result.stderr
    assert "reporte=21" in result.stderr
    assert "ledger=23" in result.stderr
    assert result.stdout == ""


def test_eje_distinto_falla_exit_2(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    axes = {"S": 5, "H": 5, "A": 3, "R": 5, "P": 4}
    result = run(tmp_path, make_report(axes=axes), ledger)

    assert result.returncode == 2
    assert "eje A" in result.stderr
    assert "reporte=3" in result.stderr
    assert "ledger=4" in result.stderr


def test_artifact_inexistente_falla_exit_2(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl", artifact="otro")
    result = run(tmp_path, make_report(), ledger, artifact="no-existe")

    assert result.returncode == 2
    assert "no-existe" in result.stderr
    assert "no existe en el ledger" in result.stderr


def test_artifact_duplicado_falla_exit_2(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "artifact": "demo", "scores": {"S": 5, "H": 5, "A": 4, "R": 5, "P": 4},
            "total": 23, "verdict": "Aprobado",
        }) + "\n")
    result = run(tmp_path, make_report(), ledger)

    assert result.returncode == 2
    assert "2 veces" in result.stderr


def test_sin_seccion_fricciones_dice_sin_fricciones_bloqueantes(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    result = run(tmp_path, make_report(frictions=None), ledger)

    assert result.returncode == 0, result.stderr
    assert "sin fricciones bloqueantes" in result.stdout


def test_fricciones_del_reporte_se_listan(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    result = run(tmp_path, make_report(frictions=["Cubrir imports externos.", "Falta caso borde."]), ledger)

    assert result.returncode == 0, result.stderr
    assert "- Cubrir imports externos." in result.stdout
    assert "- Falta caso borde." in result.stdout
    assert "sin fricciones bloqueantes" not in result.stdout


def test_cuerpo_mayor_a_60000_trunca_solo_evidencia(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    huge = "\n".join("linea de evidencia {} {}".format(i, "x" * 80) for i in range(900))
    report = make_report(evidence=huge, frictions=["Arreglar el detector de ciclos."])
    result = run(tmp_path, report, ledger)

    assert result.returncode == 0, result.stderr
    body = result.stdout
    assert len(body) <= 60000
    assert body.startswith("**Veredicto: Aprobado 23/25** (S5 H5 A4 R5 P4)")
    assert "Evidencia truncada" in body
    assert "### Fricciones" in body
    assert "- Arreglar el detector de ciclos." in body


def test_dry_run_no_escribe_archivos(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    target = tmp_path / "cuerpo.md"
    result = run(tmp_path, make_report(), ledger,
                 extra=["--dry-run", "--body-file", str(target)])

    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("**Veredicto:")
    assert "gh pr comment" in result.stderr
    assert "no se escribio ningun archivo" in result.stderr
    assert not target.exists()
    assert sorted(path.name for path in tmp_path.iterdir()) == ["report.md", "verdicts.jsonl"]


def test_body_file_escribe_el_cuerpo(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    target = tmp_path / "cuerpo.md"
    result = run(tmp_path, make_report(), ledger, extra=["--body-file", str(target)])

    assert result.returncode == 0, result.stderr
    assert result.stdout == ""
    written = target.read_text(encoding="utf-8")
    assert written.startswith("**Veredicto: Aprobado 23/25**")


# --------------------------------------------------------------------------
# Parseo tolerante: los reportes del kit no usan un unico formato de tabla.
# --------------------------------------------------------------------------

def report_with_rows(rows, total_line="**Total = 23**", verdict="Aprobado",
                     extra_sections="", sharp_heading="## Evaluación SHARP"):
    """Reporte armado a mano para fijar un formato de tabla concreto."""
    lines = ["# Reporte de prueba", ""]
    if sharp_heading:
        lines.extend([sharp_heading, ""])
    lines.extend(rows)
    lines.extend(["", total_line, "", "## Veredicto", "",
                  "Se emite veredicto **{}**.".format(verdict), ""])
    if extra_sections:
        lines.extend([extra_sections, ""])
    lines.extend(["## Evidencia", "", "```", "pytest -q", "30 passed", "```", ""])
    return "\n".join(lines)


def test_formato_t41_r2_eje_con_asteriscos_y_puntaje_entero(tmp_path):
    """`| **S** (Sharpness) | 4 | ...` — el formato de T4.1 r2."""
    ledger = make_ledger(tmp_path / "verdicts.jsonl", total=20,
                         scores={"S": 4, "H": 4, "A": 4, "R": 4, "P": 4})
    rows = [
        "| Eje | Puntuación (1-5) | Justificación |",
        "|---|---|---|",
        "| **S** (Sharpness) | 4 | Reporta errores de formato y citas invalidas. |",
        "| **H** (Horizon) | 4 | Integrado en CI. |",
        "| **A** (Asymmetry) | 4 | Detecta falsos verdes. |",
        "| **R** (Resistance) | 4 | Maneja entradas malformadas. |",
        "| **P** (Parsimony) | 4 | Codigo conciso. |",
    ]
    report = report_with_rows(rows, total_line="**Total puntuación:** 20")
    result = run(tmp_path, report, ledger)

    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[0] == "**Veredicto: Aprobado 20/25** (S4 H4 A4 R4 P4)"
    for axis in ("S", "H", "A", "R", "P"):
        assert "| {} (".format(axis) in result.stdout
    assert "Reporta errores de formato y citas invalidas." in result.stdout


def test_formato_t42_sigue_valido(tmp_path):
    """`| **S (Sharpness)** | 5 | ...` sin pipe final — el formato de T4.2."""
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    rows = [
        "| Eje | Puntuación (1-5) | Comentario |",
        "|-----|------------------|------------|",
        "| **S (Sharpness)** | 5 | Todos los casos reportan estado y cita correctos.",
        "| **H (Horizon)** | 5 | Incluye deteccion de ciclos en CI.",
        "| **A (Asymmetry)** | 4 | Evita falsos verdes.",
        "| **R (Resistance)** | 5 | Pruebas de borde verificadas.",
        "| **P (Parsimony)** | 4 | Implementacion concisa.",
    ]
    report = report_with_rows(rows, total_line="**Total = 23** → rango 19-23 → **Aprobado**.")
    result = run(tmp_path, report, ledger)

    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[0] == "**Veredicto: Aprobado 23/25** (S5 H5 A4 R5 P4)"
    assert "| A (Asymmetry) | 4/5 | Evita falsos verdes. |" in result.stdout


def test_ejes_en_otro_orden_y_puntaje_x_de_5(tmp_path):
    """Filas desordenadas, sin encabezado, puntajes '5/5' y '4 / 5'."""
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    rows = [
        "| **P** (Parsimony) | 4/5 | Conciso. |",
        "| **A** (Asymmetry) | 4 / 5 | Sin falsos verdes. |",
        "| **R** (Resistance) | 5/5 | Borde cubierto. |",
        "| **H** (Horizon) | 5 / 5 | CI. |",
        "| **S** (Sharpness) | 5/5 | Citas correctas. |",
    ]
    report = report_with_rows(rows, sharp_heading="")
    result = run(tmp_path, report, ledger)

    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[0] == "**Veredicto: Aprobado 23/25** (S5 H5 A4 R5 P4)"
    assert "| S (Sharpness) | 5/5 | Citas correctas. |" in result.stdout


def test_eje_por_nombre_completo_y_guion(tmp_path):
    """'Sharpness' solo y 'S - Sharpness' tambien cuentan como eje."""
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    rows = [
        "| Sharpness | **5** | Citas correctas. |",
        "| **H - Horizon** | **5** | CI. |",
        "| Asymmetry | 4 | Sin falsos verdes. |",
        "| **R** | 5 | Borde cubierto. |",
        "| Parsimony | 4 | Conciso. |",
        "| Eje | Puntuacion | Comentario |",
        "|---|---|---|",
    ]
    report = report_with_rows(rows)
    result = run(tmp_path, report, ledger)

    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[0] == "**Veredicto: Aprobado 23/25** (S5 H5 A4 R5 P4)"


def test_falta_un_eje_real_exit_2_nombra_el_que_falta(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    rows = [
        "| Eje | Puntuacion | Comentario |",
        "|---|---|---|",
        "| **S (Sharpness)** | 5 | Citas correctas. |",
        "| **H (Horizon)** | 5 | CI. |",
        "| **A (Asymmetry)** | 4 | Sin falsos verdes. |",
        "| **R (Resistance)** | 5 | Borde cubierto. |",
    ]
    report = report_with_rows(rows)
    result = run(tmp_path, report, ledger)

    assert result.returncode == 2
    assert result.stdout == ""
    assert "falta P" in result.stderr
    assert "encontrados: A, H, R, S" in result.stderr


def test_sin_tabla_sharp_toma_ejes_del_ledger_si_el_total_coincide(tmp_path):
    """T4.1 r2 real: sin tabla SHARP, total 20 == suma de ejes del ledger."""
    ledger = make_ledger(tmp_path / "verdicts.jsonl", total=20,
                         scores={"S": 4, "H": 4, "A": 4, "R": 4, "P": 4})
    report = "# Revision\n\n**Total puntuación:** 20\n\n## Veredicto\n\n**Veredicto:** Aprobado\n"
    result = run(tmp_path, report, ledger)

    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[0] == "**Veredicto: Aprobado 20/25** (S4 H4 A4 R4 P4)"
    assert "sin justificación: el reporte no declara tabla SHARP" in result.stdout
    assert "AVISO: el reporte no declara tabla SHARP" in result.stderr


def test_sin_tabla_sharp_y_total_incoherente_exit_2(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl", total=20,
                         scores={"S": 5, "H": 5, "A": 4, "R": 5, "P": 4})
    report = "# Revision\n\n**Total puntuación:** 20\n\n**Veredicto:** Aprobado\n"
    result = run(tmp_path, report, ledger)

    assert result.returncode == 2
    assert result.stdout == ""
    assert "no se puede reconstruir desde el ledger" in result.stderr


def test_limites_conocidos_con_bullets_no_afirma_sin_fricciones(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    extra = (
        "## Límites conocidos\n\n"
        "- Solo valida citas declaradas en tablas.\n"
        "- No hay verificacion en CI.\n"
    )
    report = report_with_rows(
        ["| **S (Sharpness)** | 5 | ok |",
         "| **H (Horizon)** | 5 | ok |",
         "| **A (Asymmetry)** | 4 | ok |",
         "| **R (Resistance)** | 5 | ok |",
         "| **P (Parsimony)** | 4 | ok |"],
        extra_sections=extra,
    )
    result = run(tmp_path, report, ledger)

    assert result.returncode == 0, result.stderr
    assert "sin fricciones bloqueantes" not in result.stdout
    assert "fricciones no declaradas en el reporte" in result.stdout
    assert "Límites conocidos (2)" in result.stdout


def test_puntos_de_friccion_en_lista_se_listan(tmp_path):
    ledger = make_ledger(tmp_path / "verdicts.jsonl")
    extra = "## Puntos de fricción\n\n- Falta caso borde de imports externos.\n"
    report = report_with_rows(
        ["| **S (Sharpness)** | 5 | ok |",
         "| **H (Horizon)** | 5 | ok |",
         "| **A (Asymmetry)** | 4 | ok |",
         "| **R (Resistance)** | 5 | ok |",
         "| **P (Parsimony)** | 4 | ok |"],
        extra_sections=extra,
    )
    result = run(tmp_path, report, ledger)

    assert result.returncode == 0, result.stderr
    assert "- Falta caso borde de imports externos." in result.stdout
    assert "sin fricciones bloqueantes" not in result.stdout
