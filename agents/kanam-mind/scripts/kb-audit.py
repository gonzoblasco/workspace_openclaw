#!/usr/bin/env python3
"""kb-audit.py - Gate ejecutable de evidencia para un brief o una nota (.md).

Por que existe: `source-verification-gate` y `evidence-chain-audit` son procedimiento escrito;
nada probaba que se ejecuto. Este script corre sobre el artefacto y devuelve un veredicto
reproducible (PASS/FAIL) con la lista de defectos, en vez de un auto-reporte.

Que verifica (cada check se puede silenciar con --skip):
  1. links    Cada link http(s) del artefacto resuelve (HEAD, fallback GET). Reporta el status.
  2. paths    Cada cita `path#Lx-Ly` (o `path:linea`) existe en disco, y `#L` no excede el largo.
  3. labels   Cada afirmacion asertiva esta etiquetada [obs] / [inf] / [unk]. Heuristica:
              oraciones asertivas = las que declaran algo sobre el mundo; se permiten dentro de
              fences, tablas de metodo y se excluyen preguntas, bullets de indice y lineas marcadas
              `allowed:`.
  4. dates    Afirmaciones sobre datos volatiles (precio, version, "ultima", fecha, estado de PR)
              deben traer una fecha YYYY-MM-DD en la misma linea o en la cita.

Uso:
  kb-audit.py reports/brief.md                      # audita y no falla el shell
  kb-audit.py reports/brief.md --strict             # exit 1 si FAIL
  kb-audit.py reports/brief.md --offline            # no hace red (links -> unknown)
  kb-audit.py reports/brief.md --json               # salida para el journal

Salida: informe legible + veredicto. Sin red disponible, los links quedan `unknown`, nunca `ok`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

LINK_RE = re.compile(r"https?://[^\s)`\]<>\"']+")
CITE_RE = re.compile(r"(?<![\w/.-])([\w./~@-]+/[^\s:`#]+)#L(\d+)(?:-L(\d+))?")
PATHLINE_RE = re.compile(r"`((?:[\w.~@-]+/)*[\w.~@-]+\.(?:md|py|ts|tsx|js|sh|json|yml|yaml|sql|txt))(?::(\d+))?`")
LABEL_RE = re.compile(r"\[(obs|inf|unk)\]", re.I)
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
VOLATILE_RE = re.compile(
    r"(?i)\b(precio|cuesta|usd|eur|ars|versi[oó]n\s+\d|released?|lanzamiento|"
    r"[uú]ltim[oa]\s+(?:precio|versi[oó]n|release|actualizaci[oó]n)|vigente|actualmente|"
    r"estado del pr|mergead[oa]|est[áa] abiert[oa])\b"
)
ASSERTIVE_START = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+|>\s*)?")


@dataclass
class Finding:
    kind: str
    severity: str  # fail | warn | info | unknown
    line: int
    detail: str
    text: str = ""


@dataclass
class Report:
    artifact: str
    generated_at: str
    findings: list = field(default_factory=list)

    def add(self, kind, severity, line, detail, text=""):
        self.findings.append(Finding(kind, severity, line, detail, text[:180]))

    def count(self, sev):
        return sum(1 for f in self.findings if f.severity == sev)

    @property
    def verdict(self):
        if self.count("fail"):
            return "FAIL"
        if self.count("unknown"):
            return "PARTIAL"
        return "PASS"


def head_ok(url: str, timeout=8):
    """Devuelve (status, nota). status: ok | fail | unknown."""
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "kanam-mind-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return ("ok", str(r.status))
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):  # sitios que rechazan HEAD: intentar GET
            try:
                req2 = urllib.request.Request(url, headers={"User-Agent": "kanam-mind-audit/1.0"})
                with urllib.request.urlopen(req2, timeout=timeout) as r2:
                    return ("ok", str(r2.status))
            except Exception as e2:  # noqa: BLE001
                return ("unknown", f"HEAD {e.code} / GET {type(e2).__name__}")
        if e.code in (401, 429, 503):
            return ("unknown", f"http {e.code}")
        return ("fail", f"http {e.code}")
    except Exception as e:  # noqa: BLE001
        return ("unknown", f"{type(e).__name__}")


def resolve_path(candidate: str, roots: list[str]):
    for root in roots:
        p = candidate if os.path.isabs(candidate) else os.path.join(root, candidate)
        if os.path.exists(p):
            return p
    return None


def audit(path: str, roots: list[str], offline: bool, skip: set[str]) -> Report:
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    rep = Report(os.path.abspath(path), datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    in_fence = False
    seen_links: dict[str, tuple] = {}

    for n, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or line.strip().startswith("#") or "allowed:" in line.lower():
            continue

        # 1. links
        if "links" not in skip:
            for url in LINK_RE.findall(line):
                url = url.rstrip(".,;:")
                if url not in seen_links:
                    seen_links[url] = head_ok(url) if not offline else ("unknown", "offline")
                st, note = seen_links[url]
                if st == "fail":
                    rep.add("link", "fail", n, f"link no resuelve ({note}): {url}")
                elif st == "unknown":
                    rep.add("link", "unknown", n, f"link sin verificar ({note}): {url}")

        # 2. citations path#Lx-Ly
        if "paths" not in skip:
            for m in CITE_RE.finditer(line):
                rel, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
                p = resolve_path(rel, roots)
                if not p:
                    rep.add("path", "fail", n, f"cita apunta a un archivo inexistente: {rel}")
                    continue
                try:
                    with open(p, "r", encoding="utf-8", errors="replace") as fh2:
                        total = sum(1 for _ in fh2)
                except OSError as e:
                    rep.add("path", "fail", n, f"cita ilegible ({e}): {rel}")
                    continue
                if b > total or a < 1:
                    rep.add("path", "fail", n, f"cita fuera de rango: {rel}#L{a}-L{b} (archivo tiene {total})")

        # 2b. `archivo.md` sin linea: solo warn (no es cita)
        if "paths" not in skip:
            for m in PATHLINE_RE.finditer(line):
                candidate = m.group(1)
                if "/" in candidate and not resolve_path(candidate, roots):
                    rep.add("path", "warn", n, f"archivo mencionado que no existe: {candidate}")

        # 3. labels sobre oraciones asertivas
        text = ASSERTIVE_START.sub("", line).strip()
        if "labels" not in skip and text and len(text) > 40:
            is_assertive = (
                text[0].isupper() or text[0] in "¿¡"
            ) and not text.endswith("?") and not text.startswith(("- [ ]", "|"))
            if is_assertive and not LABEL_RE.search(line):
                rep.add("label", "fail", n, "afirmacion sin etiqueta [obs|inf|unk]", text)

        # 4. fechas en datos volatiles
        if "dates" not in skip and VOLATILE_RE.search(line) and len(text) > 25:
            if not DATE_RE.search(line) and not CITE_RE.search(line):
                rep.add("date", "warn", n, "dato volatil sin fecha ni cita datada", text)

    if rep.count("fail") == 0 and rep.count("label") == 0:
        pass
    return rep


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("artifact")
    ap.add_argument("--root", action="append", default=[], help="raiz extra para resolver citas")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--skip", default="", help="checks a saltar, separados por coma: links,paths,labels,dates")
    args = ap.parse_args()

    if not os.path.isfile(args.artifact):
        print(f"artifact no existe: {args.artifact}", file=sys.stderr)
        return 2
    roots = args.root or [os.path.dirname(os.path.abspath(args.artifact)), os.getcwd()]
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    rep = audit(args.artifact, roots, args.offline, skip)

    if args.json:
        print(json.dumps({
            "artifact": rep.artifact, "generated_at": rep.generated_at, "verdict": rep.verdict,
            "counts": {s: rep.count(s) for s in ("fail", "warn", "unknown", "info")},
            "findings": [asdict(f) for f in rep.findings],
        }, ensure_ascii=False, indent=1))
    else:
        print(f"EVIDENCE AUDIT · {rep.verdict} · {os.path.relpath(rep.artifact)}")
        print(f"  fail={rep.count('fail')} unknown={rep.count('unknown')} warn={rep.count('warn')}")
        for f in rep.findings:
            print(f"  [{f.severity}] L{f.line} <{f.kind}> {f.detail}")
            if f.text:
                print(f"           {f.text}")

    if args.strict and rep.verdict == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
