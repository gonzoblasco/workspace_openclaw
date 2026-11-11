#!/usr/bin/env python3
"""check-unsourced-claims.py - flag magnitude claims in governance docs that carry no source.

Born from the CS50 2026 class (studies/cs50-harvard-2026/ADOPCION.md): a model writes
"p95 12,65 ms" or "51 de 57 runs" with total confidence, and nothing in the repo fails
when the number is invented. This gate does not prove the number right; it proves
somebody said where it came from.

Scope: docs/adr/, .knowledge/*/HANDOFF.md, .knowledge/*/STATUS.md, docs/STATUS*.md
A line is CLEAN when it carries, on the same line or the immediately previous one:
  - a source marker: "fuente", "source:", "segun", "verificado", "medido", "segun el repo"
  - a URL or an explicit path (a/b.py, a/b.md)
  - a backticked command (npm run build, git log, python3 x.py)
  - the escape hatch: <!-- sin-verificar -->
  - it is a table header/separator, a code fence, or inside a code block
Signal: a percentage, a duration in ms/s, a size in MB/GB, "N de M", "N veces",
an explicit version pin (v1.2.3 / 4.7.2), or a "N tests" count.

Exit 0 clean, 1 findings, 2 no files.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MAGNITUDE = re.compile(
    r"(\d+(?:[.,]\d+)?\s?%"                # percentage
    r"|\d+(?:[.,]\d+)?\s?m?s\b"            # ms
    r"|\d+(?:[.,]\d+)?\s?s\b"              # seconds
    r"|\d+(?:[.,]\d+)?\s?[MG]B\b"          # MB / GB
    r"|\b\d+\s+de\s+\d+\b"                # N de M
    r"|\b\d+\s+(?:tests?|pruebas?)\b"     # N tests
    r"|\b\d+(?:[.,]\d+)?\s?veces\b"       # N veces
    r"|\bv?\d+\.\d+\.\d+\b"              # version pin
    r"|\b\d{2,}\s+(?:runs?|corridas?|filas?|cues|palabras)\b)",
    re.IGNORECASE,
)

CLEAN = re.compile(
    r"(fuente|source:|origen:|seg[uú]n|verificad|medido|medid[ao]|"
    r"https?://|"
    r"`[^`]+`|"
    r"[\w./-]+\.(?:py|sh|mjs|js|md|json|db|ts|gd)\b|"
    r"<!--\s*sin-verificar\s*-->)",
    re.IGNORECASE,
)

SKIP_LINE = re.compile(r"^\s*(\||#{1,6}\s|```|>|---)")


def targets():
    files = []
    adr = ROOT / "docs" / "adr"
    if adr.is_dir():
        files += sorted(adr.glob("*.md"))
    for status in sorted((ROOT / "docs").glob("STATUS*.md")):
        files.append(status)
    for handoff in sorted(ROOT.glob(".knowledge/*/HANDOFF.md")):
        files.append(handoff)
    for status in sorted(ROOT.glob(".knowledge/*/STATUS.md")):
        files.append(status)
    return files


def scan(path):
    findings = []
    in_fence = False
    prev = ""
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            prev = line
            continue
        if in_fence:
            prev = line
            continue
        if SKIP_LINE.match(line):
            prev = line
            continue
        hit = MAGNITUDE.search(line)
        if not hit:
            prev = line
            continue
        if CLEAN.search(line) or CLEAN.search(prev):
            prev = line
            continue
        findings.append((n, hit.group(0), line.strip()[:110]))
        prev = line
    return findings


def main():
    files = targets()
    if not files:
        print("check-unsourced-claims: no targets found")
        return 2
    total = 0
    for path in files:
        findings = scan(path)
        if not findings:
            continue
        rel = path.relative_to(ROOT)
        for n, sig, text in findings:
            print(f"{rel}:{n}: cifra sin fuente '{sig}' -> {text}")
            total += 1
    print(f"\ncheck-unsourced-claims: {len(files)} files, {total} unsourced magnitude claims")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
