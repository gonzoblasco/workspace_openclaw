#!/usr/bin/env python3
"""check-audit-due.py - Dice que proyectos cruzaron un hito de version sin auditar.

La auditoria de camino se dispara por HITO (0.1, 0.2, 0.5, 1.0) o por decision de producto,
no por calendario. Este script solo responde: "de cuales toca ahora?"

Uso:
    python3 scripts/check-audit-due.py [--json]

Exit: 0 = nada pendiente, 1 = hay hitos sin auditar.

Fuente: projects/<slug>/.knowledge/STATUS.md (version declarada o etapa) y .knowledge/AUDIT.md.
Los STATUS no comparten formato: se aceptan **Version:**, **Version:**, **Ciclo:**, **Etapa actual:**.
"""
from __future__ import annotations
import json
import re
import sys
import pathlib
import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"

VER_RE = re.compile(r"\*\*(?:Versi[oó]n|Ciclo|Etapa actual|State):?\*\*:?\s*(.+)", re.I)
SEMVER_RE = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")
AUDIT_VER_RE = re.compile(r"\*\*(?:Version|Versi[oó]n) auditada:?\*\*:?\s*(\S+)", re.I)
AUDIT_DATE_RE = re.compile(r"\*\*Fecha:?\*\*:?\s*(\d{4}-\d{2}-\d{2})", re.I)


def read_first(path: pathlib.Path, limit: int = 40) -> str:
    try:
        return "\n".join(path.read_text().splitlines()[:limit])
    except OSError:
        return ""


def project_state(p: pathlib.Path) -> dict | None:
    status = p / ".knowledge" / "STATUS.md"
    if not status.exists():
        return None
    head = read_first(status)
    m = VER_RE.search(head)
    raw = (m.group(1).strip() if m else "")
    ver = SEMVER_RE.search(raw)
    version = f"{ver.group(1)}.{ver.group(2)}" if ver else None

    audit = p / ".knowledge" / "AUDIT.md"
    audited_version = None
    audited_date = None
    if audit.exists():
        t = read_first(audit, 15)
        am = AUDIT_VER_RE.search(t)
        if am:
            av = SEMVER_RE.search(am.group(1) or "")
            audited_version = f"{av.group(1)}.{av.group(2)}" if av else None
        adm = AUDIT_DATE_RE.search(t)
        if adm:
            audited_date = adm.group(1)

    return {
        "slug": p.name,
        "raw": raw, "version": version,
        "audited_version": audited_version,
        "audited_date": audited_date,
        "has_audit": audit.exists(),
    }


def main() -> int:
    as_json = "--json" in sys.argv
    rows, due = [], []
    if PROJECTS.is_dir():
        for p in sorted(PROJECTS.iterdir()):
            if not p.is_dir() or p.name.startswith("."):
                continue
            st = project_state(p)
            if not st:
                continue
            rows.append(st)
            needs = False
            reason = ""
            # 0.0.x = linea de fixes: no genera hito (regla de Gonzo 2026-11-04)
            es_fix_line = st["version"] == "0.0"
            if es_fix_line:
                st["fix_line"] = True
            elif not st["has_audit"]:
                needs, reason = True, "nunca auditado"
            elif st["version"] and st["audited_version"] != st["version"]:
                needs, reason = True, f"minor {st['audited_version'] or '?'} -> {st['version']} sin auditar"
            if needs:
                st["reason"] = reason
                due.append(st)

    if as_json:
        print(json.dumps({"projects": rows, "due": due}, ensure_ascii=False, indent=2))
        return 1 if due else 0

    if not rows:
        print("sin proyectos con .knowledge/STATUS.md")
        return 0

    print(f"{'proyecto':22} {'version':10} {'auditada':10} {'fecha':12} estado")
    for r in rows:
        estado = "AL DIA"
        if any(d["slug"] == r["slug"] for d in due):
            estado = "TOCA AUDITAR"
        elif r.get("fix_line"):
            estado = "fix (no aplica)"
        print(f"{r['slug']:22} {r['version'] or '-':10} {r['audited_version'] or '-':10} "
              f"{r['audited_date'] or '-':12} {estado}")

    if due:
        print("\nPendientes:")
        for d in due:
            print(f"  - {d['slug']}: {d['reason']}")
        return 1
    print("\nTodos al dia.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
