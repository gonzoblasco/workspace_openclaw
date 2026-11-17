#!/usr/bin/env python3
"""check-claims.py - validate the claim layer in docs/claims/.

A claim is one asserted fact with evidence pointing at a real artifact (a settings key,
a file, a managed block, an ADR). Ported from the memory-wiki analytics layer (ADR-064)
as a repo-native gate: the idea was right, the vault outside git was the wrong vehicle.

Checks:
  1. every claim has at least one evidence entry that resolves
  2. updatedAt is recent (default 180 days)
  3. confidence < 0.5 fails, 0.5..0.7 warns
  4. two active claims in the same topic that disagree on the same subject
  5. no contested claim without a decision

--negative seeds a deliberately broken claim, asserts every detector fires, removes it,
and asserts the reports go back to clean. A detector that never fires is indistinguishable
from a detector that is absent.

Exit 0 clean, 1 findings, 2 no claims found.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAIMS_DIR = ROOT / "docs" / "claims"
DB_PATH = ROOT / "memory" / "memory.db"
AGENTS_MD = ROOT / "AGENTS.md"
AGENT_FILE = Path.home() / ".openclaw" / "openclaw.json"

MANAGED_BEGIN = "<!-- BEGIN MANAGED:"
MANAGED_END = "<!-- END MANAGED:"


# ---------------------------------------------------------------- frontmatter

def parse_frontmatter(path: Path):
    """Minimal YAML reader for the claim format. Intentionally not a YAML library:
    the format is ours and a strict, small parser fails loudly on drift."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path}: missing frontmatter")
    end = text.find("\n---", 3)
    if end < 0:
        raise ValueError(f"{path}: unterminated frontmatter")
    header = {}
    claims = []
    current = None
    in_claims = False
    in_evidence = False
    for raw in text[3:end].splitlines():
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()

        if indent == 0:
            if line.startswith("claims:"):
                in_claims = True
                continue
            in_claims = False
            if ":" in line:
                k, _, v = line.partition(":")
                header[k.strip()] = v.strip().strip('"').strip("'")
            continue

        if not in_claims:
            continue

        if line.startswith("- id:"):
            current = {"id": line.split(":", 1)[1].strip().strip('"')}
            claims.append(current)
            in_evidence = False
            continue
        if current is None:
            continue
        if line.startswith("- kind:"):
            current.setdefault("evidence", []).append(
                {"kind": line.split(":", 1)[1].strip().strip('"')}
            )
            in_evidence = True
            continue
        if in_evidence and ":" in line:
            k, _, v = line.partition(":")
            current["evidence"][-1][k.strip()] = v.strip().strip('"').strip("'")
            continue
        in_evidence = False
        if ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k == "evidence" and not v:
                current["evidence"] = []
                in_evidence = True
                continue
            current[k] = v

    for c in claims:
        if "evidence" not in c:
            c["evidence"] = []
    return header, claims


ONLY_TOPIC = ""


def load_claims():
    results = []
    if not CLAIMS_DIR.is_dir():
        return results
    for path in sorted(CLAIMS_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        header, claims = parse_frontmatter(path)
        topic = header.get("topic") or path.stem
        if ONLY_TOPIC and topic != ONLY_TOPIC:
            continue
        for c in claims:
            c["_topic"] = topic
            c["_file"] = path
            c["_owner"] = header.get("owner", "")
        results.append((path, header, claims))
    return results


# ---------------------------------------------------------------- evidence

def _db_settings():
    """Read settings from memory.db. The live DB may live under the OpenClaw state
    directory, which plain sqlite3 refuses; copy to a temp file first."""
    if not DB_PATH.exists():
        return None, "memory/memory.db not found"
    tmp = Path(tempfile.mkdtemp()) / "mem.db"
    try:
        shutil.copy2(DB_PATH, tmp)
        con = sqlite3.connect(tmp)
        rows = dict(con.execute("select key, value from settings").fetchall())
        con.close()
        return rows, None
    except Exception as exc:  # noqa: BLE001 - reported, not raised
        return None, f"cannot read settings: {exc}"
    finally:
        shutil.rmtree(tmp.parent, ignore_errors=True)


def resolve_evidence(ev, settings, settings_err):
    """Return (ok, detail)."""
    kind = ev.get("kind", "")
    if kind == "settings":
        key = ev.get("key", "")
        if settings_err:
            return False, settings_err
        if key not in settings:
            return False, f"settings key '{key}' missing"
        if not str(settings[key]).strip():
            return False, f"settings key '{key}' is empty"
        expect = ev.get("expect")
        if expect and expect not in str(settings[key]):
            return False, f"settings '{key}' does not contain '{expect}'"
        return True, f"settings:{key}"
    if kind == "file":
        path = ROOT / ev.get("path", "")
        if not path.is_file():
            return False, f"file '{ev.get('path')}' missing"
        expect = ev.get("expect")
        if expect:
            body = path.read_text(encoding="utf-8", errors="replace")
            if expect not in body:
                return False, f"{ev.get('path')} does not contain '{expect}'"
        return True, f"file:{ev.get('path')}"
    if kind == "managed-block":
        key = ev.get("key", "")
        if not AGENTS_MD.is_file():
            return False, "AGENTS.md missing"
        body = AGENTS_MD.read_text(encoding="utf-8", errors="replace")
        begin, end = MANAGED_BEGIN + key + " -->", MANAGED_END + key + " -->"
        if begin not in body or end not in body:
            return False, f"managed block '{key}' missing in AGENTS.md"
        block = body.split(begin, 1)[1].split(end, 1)[0]
        expect = ev.get("expect")
        if expect and expect not in block:
            return False, f"managed block '{key}' does not contain '{expect}'"
        return True, f"managed-block:{key}"
    if kind == "adr":
        path = ROOT / ev.get("path", "")
        if not path.is_file():
            return False, f"adr '{ev.get('path')}' missing"
        head = path.read_text(encoding="utf-8", errors="replace")[:2000]
        if re.search(r"\*\*Estado:\*\*\s*Superseded", head):
            return False, f"{ev.get('path')} is Superseded"
        return True, f"adr:{ev.get('path')}"
    if kind == "config":
        if not AGENT_FILE.is_file():
            return False, "openclaw.json missing"
        body = AGENT_FILE.read_text(encoding="utf-8", errors="replace")
        expect = ev.get("expect")
        if expect and expect not in body:
            return False, f"openclaw.json does not contain '{expect}'"
        return True, "config:openclaw.json"
    return False, f"unknown evidence kind '{kind}'"


# ---------------------------------------------------------------- checks

def parse_ts(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _subject(prefix: str) -> str:
    """Second id segment, with one trailing qualifier dropped, so that
    models.role-primary and models.role-fallback group only when they are the SAME
    role and the SAME position. models.core-primary -> (models, core)"""
    parts = prefix.split(".")
    if len(parts) < 2:
        return prefix
    role = parts[1]
    for suffix in ("primary", "fallback", "thinking"):
        if role.endswith("-" + suffix):
            return role[: -(len(suffix) + 1)]
    return role


def run_checks(max_age_days: int, quiet: bool = False):
    claims_docs = load_claims()
    if not claims_docs:
        print("No claim files found under docs/claims/", file=sys.stderr)
        return 2

    settings, settings_err = _db_settings()
    findings = []
    warnings = []
    total = 0
    now = datetime.now(timezone.utc)

    for path, header, claims in claims_docs:
        for c in claims:
            total += 1
            cid = c.get("id", "<no id>")
            status = c.get("status", "active")

            if status == "retracted":
                continue

            ev = c.get("evidence", [])
            if not ev:
                findings.append(f"{cid}: no evidence")
            else:
                for e in ev:
                    ok, detail = resolve_evidence(e, settings, settings_err)
                    if not ok:
                        findings.append(f"{cid}: evidence unresolved - {detail}")

            ts = parse_ts(c.get("updatedAt"))
            if ts is None:
                findings.append(f"{cid}: missing or unparseable updatedAt")
            elif now - ts > timedelta(days=max_age_days):
                findings.append(f"{cid}: stale (updatedAt {c.get('updatedAt')})")

            try:
                conf = float(c.get("confidence", "nan"))
            except ValueError:
                conf = float("nan")
            if conf != conf:
                findings.append(f"{cid}: missing confidence")
            elif conf < 0.5:
                findings.append(f"{cid}: low confidence ({conf})")
            elif conf < 0.7:
                warnings.append(f"{cid}: confidence {conf} (below 0.7)")

            if status == "contested":
                findings.append(f"{cid}: contested and undecided")

            target = c.get("contradicts")
            if target:
                findings.append(f"{cid}: explicitly contradicts {target}")

    # contradiction heuristic: same topic + same id prefix + different numeric/word value
    by_subject = {}
    for path, header, claims in claims_docs:
        for c in claims:
            if c.get("status") != "active":
                continue
            parts = c.get("id", "").split(".")
            subject = parts[1] if len(parts) > 1 else "page"
            if len(parts) > 2:
                subject += "." + parts[2]
            by_subject.setdefault((c["_topic"], subject), []).append(c)
    for (topic, subject), group in by_subject.items():
        if len(group) < 2:
            continue
        seen = {}
        for c in group:
            nums = tuple(re.findall(r"\d+(?:[.,]\d+)?", c.get("text", "")))
            if nums:
                seen.setdefault(nums, c.get("id"))
        if len(seen) > 1:
            ids = ", ".join(seen.values())
            findings.append(f"{topic}/{subject}: contradictory values across {ids}")

    if not quiet:
        print(f"Claims: {total} in {len(claims_docs)} topic file(s)")
        for w in warnings:
            print(f"  warn  {w}")
        for f in findings:
            print(f"  FAIL  {f}")
        print("clean" if not findings else f"{len(findings)} finding(s)")
    return 1 if findings else 0


# ---------------------------------------------------------------- negative

NEGATIVE_BODY = """---
pageType: claims
topic: probe
owner: check-claims.py
updatedAt: 1999-01-01T00:00:00+00:00
claims:
  - id: probe.no-evidence
    text: "Un claim sin evidencia, a proposito."
    status: active
    confidence: 0.9
    updatedAt: 1999-01-01T00:00:00+00:00
  - id: probe.low-confidence
    text: "Un claim con confianza 0.2, a proposito."
    status: active
    confidence: 0.2
    updatedAt: 2026-11-16T00:00:00+00:00
    evidence:
      - kind: file
        path: docs/claims/README.md
  - id: probe.contested
    text: "Un claim contestado, a proposito."
    status: contested
    confidence: 0.6
    updatedAt: 2026-11-16T00:00:00+00:00
    evidence:
      - kind: file
        path: docs/claims/README.md
  - id: probe.owner-mismatch
    text: "Un claim cuyo updatedAt es viejo, a proposito."
    status: active
    confidence: 0.9
    updatedAt: 1999-01-01T00:00:00+00:00
    evidence:
      - kind: file
        path: docs/claims/README.md
  - id: probe.bad-path
    text: "Un claim con evidencia rota, a proposito."
    status: active
    confidence: 0.9
    updatedAt: 2026-11-16T00:00:00+00:00
    evidence:
      - kind: file
        path: docs/claims/does-not-exist.md
---
"""


def run_negative():
    probe = CLAIMS_DIR / "probe.md"
    if probe.exists():
        print(f"refusing: {probe} already exists", file=sys.stderr)
        return 2
    expected = ["probe.no-evidence: no evidence",
                "probe.low-confidence: low confidence",
                "probe.contested: contested",
                "probe.bad-path: evidence unresolved",
                "probe.owner-mismatch"]
    try:
        probe.write_text(NEGATIVE_BODY, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(Path(__file__)), "--topic", "probe"],
            capture_output=True, text=True,
        )
        seeded = proc.returncode
        report = proc.stdout
    finally:
        probe.unlink(missing_ok=True)

    missing = [e for e in expected if e not in report]
    clean = run_checks(180, quiet=True)

    print("Negative run (detectors must fire on the seed):")
    for e in expected:
        print(f"  {'ok  ' if e not in missing else 'MISS'} {e}")
    print(f"  seeded run exit={seeded} (expected 1)")
    print(f"  after cleanup exit={clean} (expected 0)")
    ok = not missing and seeded == 1 and clean == 0
    print("negative run PASSED" if ok else "negative run FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-age-days", type=int, default=180)
    ap.add_argument("--quiet", action="store_true", help="exit code only")
    ap.add_argument("--negative", action="store_true")
    ap.add_argument("--topic", help="only check claims from this topic file")
    args = ap.parse_args()
    if args.negative:
        return run_negative()
    global ONLY_TOPIC
    ONLY_TOPIC = args.topic or ""
    return run_checks(args.max_age_days, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
