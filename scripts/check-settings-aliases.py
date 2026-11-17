#!/usr/bin/env python3
"""check-settings-aliases.py - the same setting must not live under two keys.

ADR-090 §1 documents the trap: the `settings` table in memory.db keeps the same
model assignment under three keys (`model_by_agent`, `model_triple`, `model.triple`)
and fixing only the ones you remember leaves a live copy of the old value. It
happened twice in one session on 2026-11-04 (glm4:9b, then planner/studio) and
nobody noticed until the aliases drifted again on 2026-11-04 and stayed drifted
for twelve days.

Aliases are grouped here so the check is structural, not a memory test:

    model_by_agent == model_triple == model.triple

The group is only as real as the aliases listed. When a key is added by
`managed-blocks.py set` (which inserts blindly), it shows up here as an
orphan - a settings key that is not a known alias and not referenced by any
managed block template. That is how `model.triple` survived: valid key, valid
value, read by nobody.

Modes:
    check (default)   report drift, exit 1 if any group disagrees
    --fix             copy the canonical value into the drifted aliases, re-check
    --list            print the alias groups and the orphan keys

Canonical member: `model_by_agent`, because that is the key the AGENTS.md
managed block reads (verified 2026-10-06; setting `model.triple` updates
docs/SETUP.md and leaves AGENTS.md stale).

Exit 0 clean, 1 drift, 2 cannot read the DB.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sqlite3
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "memory" / "memory.db"

# The alias groups. Adding a key here is the only way a new copy becomes
# "expected"; anything else in `settings` that looks like this group is an orphan.
ALIAS_GROUPS = {
    "model_by_agent": ["model_by_agent", "model_triple", "model.triple"],
}

# Keys a managed block template reads. Anything else in `settings` is either an
# orphan of an alias group or dead weight - both are reported, neither is fatal
# unless it is in an alias group with a different value.
BLOCK_KEYS = {
    "model_primary", "model_auxiliary", "model_alternative", "thinking_default",
    "model_pipeline", "model_pipeline_a", "model_pipeline_b", "model_pipeline_c",
    "model_pipeline_prefilter", "model_by_agent",
}

# Not settings, but rows in the same table that belong to other subsystems.
NON_MODEL_KEYS = {"session_retention_days", "backup_retention_days"}


def load_settings():
    if not DB_PATH.exists():
        return None, "memory/memory.db not found"
    tmp_dir = pathlib.Path(tempfile.mkdtemp())
    tmp = tmp_dir / "mem.db"
    try:
        shutil.copy2(DB_PATH, tmp)
        con = sqlite3.connect(tmp)
        rows = dict(con.execute("select key, value from settings").fetchall())
        con.close()
        return rows, None
    except Exception as exc:  # noqa: BLE001 - reported, not raised
        return None, f"cannot read settings: {exc}"
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def write_settings(updates: dict[str, str]):
    """Write through a copy and swap it back, because plain sqlite3 refuses the
    live DB under the OpenClaw state directory."""
    tmp_dir = pathlib.Path(tempfile.mkdtemp())
    tmp = tmp_dir / "mem.db"
    try:
        shutil.copy2(DB_PATH, tmp)
        con = sqlite3.connect(tmp)
        for key, value in updates.items():
            con.execute(
                """INSERT INTO settings (key, value, description, updated_at)
                   VALUES (?,?,?,datetime('now'))
                   ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=datetime('now')""",
                (key, value, "aligned by check-settings-aliases.py"),
            )
        con.commit()
        con.close()
        shutil.copy2(tmp, DB_PATH)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def audit(settings):
    drift = []
    for canonical, aliases in ALIAS_GROUPS.items():
        if canonical not in settings:
            drift.append(f"group {canonical}: canonical key missing")
            continue
        expected = settings[canonical]
        for alias in aliases:
            if alias == canonical:
                continue
            if alias not in settings:
                drift.append(f"group {canonical}: alias '{alias}' missing")
            elif settings[alias] != expected:
                drift.append(
                    f"group {canonical}: '{alias}' differs\n"
                    f"    canonical {canonical}: {expected}\n"
                    f"    drifted   {alias}: {settings[alias]}"
                )
    known = set(BLOCK_KEYS)
    for aliases in ALIAS_GROUPS.values():
        known.update(aliases)
    orphans = sorted(
        k for k in settings
        if k not in known and k not in NON_MODEL_KEYS and "model" in k.lower()
    )
    return drift, orphans


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fix", action="store_true", help="copy the canonical value into drifted aliases")
    ap.add_argument("--list", action="store_true", help="print groups and orphan keys")
    args = ap.parse_args()

    settings, err = load_settings()
    if settings is None:
        print(f"ERROR {err}", file=sys.stderr)
        return 2

    if args.list:
        for canonical, aliases in ALIAS_GROUPS.items():
            print(f"group {canonical}: {', '.join(aliases)}")
            for alias in aliases:
                print(f"  {alias:16} = {settings.get(alias, '<missing>')}")
        _, orphans = audit(settings)
        print(f"\norphan model keys (not in a group, not read by a block): {orphans or 'none'}")
        return 0

    drift, orphans = audit(settings)
    if args.fix and drift:
        updates = {}
        for canonical, aliases in ALIAS_GROUPS.items():
            if canonical not in settings:
                continue
            for alias in aliases:
                if alias != canonical and settings.get(alias) != settings[canonical]:
                    updates[alias] = settings[canonical]
        if updates:
            write_settings(updates)
            print(f"aligned {len(updates)} alias(es): {', '.join(updates)}")
            settings, err = load_settings()
            if settings is None:
                print(f"ERROR after write: {err}", file=sys.stderr)
                return 2
            drift, orphans = audit(settings)

    print(f"Alias groups: {len(ALIAS_GROUPS)}   settings keys: {len(settings)}")
    for line in drift:
        print(f"  FAIL  {line}")
    if orphans:
        for o in orphans:
            print(f"  warn  orphan model key '{o}' (not in a group, not read by a block)")
    print("clean" if not drift else f"{len(drift)} drift finding(s)")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
