#!/usr/bin/env python3
"""Tests for workspace HANDOFF merge and per-course HANDOFF destination.

Run from the workspace root:
    python3 scripts/test-handoff-merge.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "session-handoff.py"


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


def workspace_close(handoff_dir, summary, steps):
    return run(
        "--project", "workspace",
        "--summary", summary,
        "--next-steps", steps,
        "--handoff-dir", str(handoff_dir),
    )


def test_course_destination():
    """--course writes studies/<slug>/HANDOFF.md with the course title."""
    slug = "__tmp_course_test__"
    course_dir = ROOT / "studies" / slug
    course_dir.mkdir(parents=True, exist_ok=True)
    try:
        result = run("--course", slug, "--summary", "Curso test")
        assert result.returncode == 0, result.stderr
        handoff = course_dir / "HANDOFF.md"
        assert handoff.is_file(), "no se creo el HANDOFF del curso"
        text = handoff.read_text(encoding="utf-8")
        assert f"# HANDOFF - Curso {slug}" in text, "titulo de curso incorrecto"
        assert "**Proyecto:** " + slug in text
    finally:
        shutil.rmtree(course_dir, ignore_errors=True)


def test_course_slug_rejection():
    """Path separators and parent refs are rejected."""
    for bad in ("bad/slug", "..", "a\\b"):
        result = run("--course", bad, "--summary", "x")
        assert result.returncode != 0, f"slug aceptado: {bad}"


def test_workspace_merge_preserves_items():
    """A step from the previous close survives a new close."""
    handoff_dir = ROOT / ".tmp-handoff-merge"
    shutil.rmtree(handoff_dir, ignore_errors=True)
    handoff_dir.mkdir()
    try:
        assert workspace_close(handoff_dir, "Primera", "1. Paso A").returncode == 0
        assert workspace_close(handoff_dir, "Segunda", "2. Paso B").returncode == 0
        text = (handoff_dir / "HANDOFF.md").read_text(encoding="utf-8")
        assert "Paso A" in text, "se perdio el paso heredado"
        assert "Paso B" in text, "no se agrego el paso nuevo"
    finally:
        shutil.rmtree(handoff_dir, ignore_errors=True)


def test_workspace_merge_dedupes():
    """The same step reported twice appears once."""
    handoff_dir = ROOT / ".tmp-handoff-dedupe"
    shutil.rmtree(handoff_dir, ignore_errors=True)
    handoff_dir.mkdir()
    try:
        assert workspace_close(handoff_dir, "Primera", "1. Paso repetido").returncode == 0
        assert workspace_close(handoff_dir, "Segunda", "1. Paso repetido").returncode == 0
        text = (handoff_dir / "HANDOFF.md").read_text(encoding="utf-8")
        assert text.count("Paso repetido") == 1, "el paso quedo duplicado"
    finally:
        shutil.rmtree(handoff_dir, ignore_errors=True)


def _section(text, title):
    start = text.index(f"## {title}")
    end = text.find("\n## ", start + 1)
    return text[start:end if end != -1 else len(text)]


def test_workspace_merge_keeps_five_summaries():
    """The history keeps at most five entries and drops the oldest."""
    handoff_dir = ROOT / ".tmp-handoff-limit"
    shutil.rmtree(handoff_dir, ignore_errors=True)
    handoff_dir.mkdir()
    try:
        for i in range(7):
            result = workspace_close(handoff_dir, f"Resumen {i}", f"{i + 1}. Paso {i}")
            assert result.returncode == 0, result.stderr
        text = (handoff_dir / "HANDOFF.md").read_text(encoding="utf-8")
        history = _section(text, "Que se hizo en esta sesion")
        assert history.count("### ") <= 5, "mas de cinco entradas en Que se hizo"
        assert "Resumen 0" not in history, "la entrada mas vieja no se podo"
        assert "Resumen 6" in history, "la entrada mas nueva no esta"
    finally:
        shutil.rmtree(handoff_dir, ignore_errors=True)


def test_project_no_merge():
    """A normal project HANDOFF still overwrites (no merge)."""
    project_dir = ROOT / "projects" / "__tmp_project_test__"
    shutil.rmtree(project_dir, ignore_errors=True)
    try:
        first = run("--project", "__tmp_project_test__", "--summary", "Primer", "--next-steps", "1. Paso X")
        assert first.returncode == 0, first.stderr
        second = run("--project", "__tmp_project_test__", "--summary", "Segundo", "--next-steps", "2. Paso Y")
        assert second.returncode == 0, second.stderr
        text = (project_dir / ".knowledge" / "HANDOFF.md").read_text(encoding="utf-8")
        assert "Paso Y" in text
        assert "Paso X" not in text, "un proyecto normal no debe fusionar"
    finally:
        shutil.rmtree(project_dir, ignore_errors=True)


if __name__ == "__main__":
    test_course_destination()
    test_course_slug_rejection()
    test_workspace_merge_preserves_items()
    test_workspace_merge_dedupes()
    test_workspace_merge_keeps_five_summaries()
    test_project_no_merge()
    print("All 6 HANDOFF tests passed.")
