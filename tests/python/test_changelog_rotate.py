"""Tests for scripts/changelog-rotate.py (CHANGELOG active-window rotation).

The critical properties: rotation keeps only the last N days active, moves the
rest to the archive without losing it, is idempotent, and --check reports drift
so the pre-commit can enforce it.
"""
import importlib.util
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "changelog-rotate.py"


def load(tmp_path):
    spec = importlib.util.spec_from_file_location("changelog_rotate", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ws = tmp_path / "ws"
    (ws / "docs" / "archive").mkdir(parents=True)
    mod.ROOT = ws
    mod.ACTIVE = ws / "CHANGELOG.md"
    mod.ARCHIVE = ws / "docs" / "archive" / "CHANGELOG-archive.md"
    return mod, ws


def write_changelog(p, entries):
    body = "# CHANGELOG.md\n\nhead\n\n---\n\n"
    body += "\n".join(f"## [{d}] - {t}\n\nbody {t}\n" for d, t in entries)
    p.write_text(body, encoding="utf-8")


def test_split_entries_reads_header_and_entries(tmp_path):
    mod, ws = load(tmp_path)
    p = ws / "CHANGELOG.md"
    write_changelog(p, [("2026-10-06", "a"), ("2026-08-01", "b")])
    header, entries = mod.split_entries(p.read_text())
    assert "head" in header
    assert [d for d, _ in entries] == ["2026-10-06", "2026-08-01"]


def test_rotation_keeps_window_and_archives_rest(tmp_path):
    mod, ws = load(tmp_path)
    p = ws / "CHANGELOG.md"
    today = dt.date(2026, 10, 6)
    write_changelog(p, [("2026-10-06", "new"), ("2026-09-09", "in"), ("2026-08-01", "old")])
    active, archive, needs, n_a, n_x = mod.plan(30, today)
    assert needs is True
    assert n_a == 2 and n_x == 1
    assert "new" in active and "in" in active and "old" not in active
    assert "old" in archive and "new" not in archive


def test_rotation_is_idempotent(tmp_path):
    mod, ws = load(tmp_path)
    p = ws / "CHANGELOG.md"
    today = dt.date(2026, 10, 6)
    write_changelog(p, [("2026-10-06", "new"), ("2026-08-01", "old")])
    active, archive, needs, _, _ = mod.plan(30, today)
    p.write_text(active, encoding="utf-8")
    mod.ARCHIVE.write_text(archive, encoding="utf-8")
    _, _, needs2, _, _ = mod.plan(30, today)
    assert needs2 is False


def test_archive_accumulates_without_duplicates(tmp_path):
    mod, ws = load(tmp_path)
    p = ws / "CHANGELOG.md"
    today = dt.date(2026, 10, 6)
    write_changelog(p, [("2026-08-01", "old")])
    _, archive1, _, _, _ = mod.plan(30, today)
    mod.ARCHIVE.write_text(archive1, encoding="utf-8")
    # Otra corrida con lo mismo + algo nuevo rotado.
    write_changelog(p, [("2026-08-01", "old"), ("2026-07-01", "older")])
    _, archive2, _, _, _ = mod.plan(30, today)
    assert archive2.count("body old") == 1
    assert "older" in archive2


def test_entries_sorted_desc(tmp_path):
    mod, ws = load(tmp_path)
    p = ws / "CHANGELOG.md"
    today = dt.date(2026, 10, 6)
    write_changelog(p, [("2026-09-09", "b"), ("2026-10-06", "a")])
    active, _, _, _, _ = mod.plan(30, today)
    assert active.index("[2026-10-06]") < active.index("[2026-09-09]")


def test_check_exit_codes(tmp_path):
    mod, ws = load(tmp_path)
    p = ws / "CHANGELOG.md"
    today = dt.date(2026, 10, 6)
    write_changelog(p, [("2026-10-06", "a"), ("2026-08-01", "b")])
    assert mod.main(["--check", "--today", "2026-10-06"]) == 1
    active, archive, _, _, _ = mod.plan(30, today)
    p.write_text(active, encoding="utf-8")
    mod.ARCHIVE.write_text(archive, encoding="utf-8")
    assert mod.main(["--check", "--today", "2026-10-06"]) == 0


def test_dry_run_does_not_write(tmp_path):
    mod, ws = load(tmp_path)
    p = ws / "CHANGELOG.md"
    write_changelog(p, [("2026-08-01", "old")])
    before = p.read_text()
    assert mod.main(["--dry-run", "--today", "2026-10-06"]) == 0
    assert p.read_text() == before
    assert not mod.ARCHIVE.exists()


def test_bad_date_is_usage_error(tmp_path):
    mod, _ = load(tmp_path)
    assert mod.main(["--today", "not-a-date"]) == 2
