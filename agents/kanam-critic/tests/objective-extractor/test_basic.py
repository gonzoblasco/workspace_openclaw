import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "bin" / "objective-extractor.py"


def run(script_path: Path, md_file: Path, extra=None):
    cmd = [sys.executable, str(script_path), str(md_file)]
    if extra:
        cmd.extend(extra)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def write_md(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "doc.md"
    p.write_text(content, encoding="utf-8")
    return p


def test_verified_row(tmp_path):
    target = tmp_path / "target.txt"
    target.write_text("line one\nline two\n", encoding="utf-8")
    md = write_md(
        tmp_path,
        f"""
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Demo | demo.txt | `{target.name}:2` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 0
    assert "verificado" in res.stdout
    assert "line two" in res.stdout


def test_line_out_of_range(tmp_path):
    target = tmp_path / "file.txt"
    target.write_text("only one line\n", encoding="utf-8")
    md = write_md(
        tmp_path,
        f"""
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Oops | o.txt | `{target.name}:99999` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 1
    assert "auto-reportado" in res.stdout
    assert "fuera de rango" in res.stdout


def test_missing_file(tmp_path):
    md = write_md(
        tmp_path,
        """
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Lost | lost.txt | `does-not-exist.txt:1` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 1
    assert "archivo inexistente" in res.stdout


def test_empty_line(tmp_path):
    target = tmp_path / "empty.txt"
    target.write_text("\nsecond\n", encoding="utf-8")
    md = write_md(
        tmp_path,
        f"""
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Blank | b.txt | `{target.name}:1` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 1
    assert "linea vacia" in res.stdout


def test_no_markers(tmp_path):
    md = write_md(tmp_path, "# No markers here\n")
    res = run(SCRIPT, md)
    assert res.returncode == 0
    lines = res.stdout.strip().splitlines()
    assert lines[0].startswith("| Objetivo")
    assert "sin bloque" in res.stderr


def test_no_strict_flag(tmp_path):
    md = write_md(
        tmp_path,
        """
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Missing | m.txt | `does-not-exist.txt:1` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md, extra=["--no-strict"])
    assert res.returncode == 0



# --- r5 additions -----------------------------------------------------------

def test_escaped_pipe_in_cell(tmp_path):
    target = tmp_path / "t.txt"
    target.write_text("hello\n", encoding="utf-8")
    md = write_md(
        tmp_path,
        f"""
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | A \\| B | file.txt | `{target.name}:1` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 0, res.stderr
    assert "A \\| B" in res.stdout
    assert "verificado" in res.stdout


def test_malformed_table_exit_2(tmp_path):
    md = write_md(
        tmp_path,
        """
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Solo | dos |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 2
    assert "ERROR: tabla malformada" in res.stderr
    assert "0 filas" in res.stderr


def test_two_blocks_are_summed(tmp_path):
    target = tmp_path / "a.txt"
    target.write_text("uno\n", encoding="utf-8")
    md = write_md(
        tmp_path,
        f"""
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | First | a.txt | `{target.name}:1` |
        <!-- objetivos:end -->

        texto intermedio

        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Second | b.txt | `missing-forever.txt:1` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 1
    assert "First" in res.stdout and "Second" in res.stdout
    assert "2 filas" in res.stderr
    assert "1 auto-reportadas" in res.stderr
    assert "archivo inexistente" in res.stdout


def test_resumen_always_present(tmp_path):
    target = tmp_path / "ok.txt"
    target.write_text("ok\n", encoding="utf-8")
    md = write_md(
        tmp_path,
        f"""
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Fine | ok.txt | `{target.name}:1` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 0
    assert "RESUMEN:" in res.stderr


def test_truncated_to_80_chars(tmp_path):
    long_line = "x" * 200
    target = tmp_path / "long.txt"
    target.write_text(long_line + "\n", encoding="utf-8")
    md = write_md(
        tmp_path,
        f"""
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Long | l.txt | `{target.name}:1` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    cell = [c.strip() for c in res.stdout.splitlines()[2].split("|") if c.strip()][4]
    assert len(cell) == 80
    assert cell.endswith("...")
    assert cell == "x" * 77 + "..."


def test_non_ascii_digit_line_number(tmp_path):
    md = write_md(
        tmp_path,
        """
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Bad | x.txt | `x.txt:1_0` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 1
    assert "auto-reportado" in res.stdout
    assert "cita invalida: numero de linea no valido" in res.stdout


def test_text_with_spaces_is_stripped(tmp_path):
    target = tmp_path / "sp.txt"
    target.write_text("   padded content   \n", encoding="utf-8")
    md = write_md(
        tmp_path,
        f"""
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Pad | p.txt | `{target.name}:1` |
        <!-- objetivos:end -->
        """,
    )
    res = run(SCRIPT, md)
    assert res.returncode == 0
    assert "padded content" in res.stdout
    assert "   padded content" not in res.stdout


# --- root resolution additions ---------------------------------------------

def make_repo(tmp_path: Path) -> Path:
    """Create a fake repository root (``.git`` dir) and return it."""
    root = tmp_path / "repo"
    root.mkdir()
    (root / ".git").mkdir()
    return root


def test_cita_repo_relativa_desde_subdirectorio(tmp_path):
    root = make_repo(tmp_path)
    target = root / "agents" / "bin" / "tool.py"
    target.parent.mkdir(parents=True)
    target.write_text("line one\nline two\n", encoding="utf-8")
    docs = root / "agents" / "docs"
    docs.mkdir(parents=True)
    md = docs / "doc.md"
    md.write_text(
        """
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Tool | tool.py | `agents/bin/tool.py:2` |
        <!-- objetivos:end -->
        """,
        encoding="utf-8",
    )
    res = run(SCRIPT, md)
    assert res.returncode == 0, res.stderr + res.stdout
    assert "verificado" in res.stdout
    assert "line two" in res.stdout
    assert "archivo inexistente" not in res.stdout


def test_cita_relativa_al_directorio_del_documento(tmp_path):
    root = make_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir()
    local = docs / "local.txt"
    local.write_text("local line\n", encoding="utf-8")
    md = docs / "doc.md"
    md.write_text(
        """
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Local | local.txt | `local.txt:1` |
        <!-- objetivos:end -->
        """,
        encoding="utf-8",
    )
    res = run(SCRIPT, md)
    assert res.returncode == 0, res.stderr + res.stdout
    assert "verificado" in res.stdout
    assert "local line" in res.stdout


def test_cita_inexistente_en_todas_las_bases(tmp_path):
    root = make_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir()
    md = docs / "doc.md"
    md.write_text(
        """
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Lost | lost.txt | `nowhere/lost.txt:1` |
        <!-- objetivos:end -->
        """,
        encoding="utf-8",
    )
    res = run(SCRIPT, md)
    assert res.returncode == 1
    assert "archivo inexistente" in res.stdout
    assert "auto-reportado" in res.stdout


def test_raiz_del_repo_gana_sobre_directorio_del_documento(tmp_path):
    root = make_repo(tmp_path)
    (root / "winner.txt").write_text("root line\n", encoding="utf-8")
    docs = root / "docs"
    docs.mkdir()
    (docs / "winner.txt").write_text("sub line\n", encoding="utf-8")
    md = docs / "doc.md"
    md.write_text(
        """
        <!-- objetivos:begin -->
        | Objetivo | Entregable | Cita |
        |---|---|---|
        | Tie | winner.txt | `winner.txt:1` |
        <!-- objetivos:end -->
        """,
        encoding="utf-8",
    )
    res = run(SCRIPT, md)
    assert res.returncode == 0, res.stderr + res.stdout
    assert "root line" in res.stdout
    assert "sub line" not in res.stdout
