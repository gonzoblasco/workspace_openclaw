#!/usr/bin/env python3
"""check-settings-aliases.py - one setting, one key.

The `settings` table in memory.db once kept the same model assignment under
three keys: `model_by_agent` (the one the AGENTS.md managed block reads),
`model_triple` and `model.triple`. `managed-blocks.py set` wrote to one key at
a time, so "fixing" the assignment left the other two carrying the old value.
It happened twice on 2026-11-04, and `model.triple` drifted again for twelve
days until 2026-11-16: it still said `minimax-m3.1-flash` while ADR-107 had
moved the CORE to `deepseek`.

The first fix (2026-11-16) aligned the three values and watched them. That
treated the copy as normal. One fact, one owner (AGENTS.md section 0) means
the duplicate keys should not exist: `managed-blocks.py` now writes every
alias from `ALIASES` on a single `set`, reads only the canonical one, and
`seed` never creates an alias.

So this gate now enforces the absence:

  1. no alias key exists in `settings`        -> a copy came back, delete it
  2. if a legacy alias exists anyway, it must equal the canonical value
  3. no model-ish key outside the known set   -> an orphan nobody reads

Modes:
    check (default)   report, exit 1 on any finding
    --list            print the alias map, the keys and the canonical values

Exit 0 clean, 1 findings, 2 cannot read the DB.
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

# Must mirror ALIASES in scripts/managed-blocks.py. Duplicating the map here is
# deliberate: if the two disagree, this gate says so instead of silently
# trusting one of them. `--list` prints both so the drift is visible.
EXPECTED_ALIASES = {
    "model_by_agent": ("model_triple", "model.triple"),
}

# Keys a managed block template reads. Anything else model-ish is an orphan.
BLOCK_KEYS = {
    "model_primary", "model_auxiliary", "model_alternative", "thinking_default",
    "model_pipeline", "model_pipeline_a", "model_pipeline_b", "model_pipeline_c",
    "model_pipeline_prefilter", "model_by_agent",
}

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


def aliases_in_code():
    """Read ALIASES from managed-blocks.py without importing it (it parses argv
    on import through argparse in main(), but the module itself is safe)."""
    path = ROOT / "scripts" / "managed-blocks.py"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    block = text.split("ALIASES = {", 1)
    if len(block) < 2:
        return {}
    body = block[1].split("}", 1)[0]
    result = {}
    for line in body.splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        name, _, rest = line.partition(":")
        name = name.strip().strip('"').strip("'")
        keys = tuple(
            k.strip().strip('"').strip("'")
            for k in rest.strip().strip(",").strip("()").split(",")
            if k.strip()
        )
        if name and keys:
            result[name] = keys
    return result


def audit(settings):
    findings = []
    warnings = []

    code_aliases = aliases_in_code()
    if code_aliases is None:
        warnings.append("cannot read ALIASES from scripts/managed-blocks.py")
    elif code_aliases != EXPECTED_ALIASES:
        warnings.append(
            "ALIASES desincronizado: managed-blocks.py="
            f"{code_aliases} vs gate={EXPECTED_ALIASES}"
        )

    for canonical, aliases in EXPECTED_ALIASES.items():
        if canonical not in settings:
            findings.append(f"canonical key '{canonical}' missing")
            continue
        for alias in aliases:
            if alias in settings:
                # The copy exists: the retiro did not hold.
                if settings[alias] != settings[canonical]:
                    findings.append(
                        f"alias '{alias}' exists AND differs from '{canonical}' "
                        f"(alias={settings[alias]!r})"
                    )
                else:
                    findings.append(
                        f"alias '{alias}' exists as a copy of '{canonical}': "
                        "duplicate key, delete it"
                    )

    known = set(BLOCK_KEYS)
    for aliases in EXPECTED_ALIASES.values():
        known.update(aliases)
    for key in sorted(settings):
        if key in known or key in NON_MODEL_KEYS:
            continue
        if "model" in key.lower():
            warnings.append(f"orphan model key '{key}' (not in a group, not read by a block)")

    return findings, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="print the alias map and current keys")
    args = ap.parse_args()

    settings, err = load_settings()
    if settings is None:
        print(f"ERROR {err}", file=sys.stderr)
        return 2

    if args.list:
        print("Regla: un setting, una clave.\n")
        for canonical, aliases in EXPECTED_ALIASES.items():
            print(f"{canonical} = {settings.get(canonical, '<missing>')}")
            for alias in aliases:
                state = "PRESENTE (copia)" if alias in settings else "ausente (ok)"
                print(f"  alias {alias:14} {state}")

    findings, warnings = audit(settings)
    print(f"\nSettings keys: {len(settings)}   canonical groups: {len(EXPECTED_ALIASES)}")
    for w in warnings:
        print(f"  warn  {w}")
    for f in findings:
        print(f"  FAIL  {f}")
    print("clean" if not findings else f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
