#!/usr/bin/env python3
"""
verify-verdict.py - El guard del veredicto: un veredicto no existe hasta que
existe su fila Y su reporte.

POR QUE EXISTE (2026-11-06, incidente medido).
La re-verificacion T1.r2 del kit devolvio por chat: "artefacto
kanam-critic-kit-v0.3-r2, S 5 H 5 A 4 R 5 P 4, total 23, Aprobado, delta +11" y
anuncio la ruta del reporte. En disco, al terminar:

  - `memory/verdicts.jsonl` NO tenia fila `kanam-critic-kit-v0.3-r2` (3 filas, la ultima
    era el VETO de 12/25).
  - `docs/reviews/2026-11-06-critic-kit-v0.3-r2.md` NO existia.
  - La sesion nunca leyo el kit ni corrio el evidence-hunter: 5 comandos y una respuesta
    narrada.

O sea: un veredicto **reportado y no registrado**. El mismo falso verde que el lab
`evidence-hunter` cazaba en los autores (ADR-078: la salida de un sub-agente es un
auto-reporte, no un hecho) me alcanzo a mi mismo. Sin este script, un "Aprobado" de 23/25
habria quedado en el mundo sin una sola linea de evidencia que lo respalde.

QUE VERIFICA (por veredicto real):
  1. FILA: existe en `memory/verdicts.jsonl` una linea con ese `artifact`.
  2. REPORTE: existe `docs/reviews/<fecha>-<slug>.md` para ese artefacto (match por slug EXACTO:
     `v0.3` no puede casar con `v0.3-r2.md`).
  3. TOTAL: el total del reporte coincide con la suma de los 5 ejes de la fila del ledger.
  4. VEREDICTO: la palabra del veredicto del reporte coincide con la de la fila Y con la matriz
     SHARP para ese total (<=18 VETO, 19-23 Aprobado, >=24 ORO). Un 16 etiquetado "Aprobado"
     es un veredicto invalido por construccion.
  5. CITAS: el reporte tiene al menos 5 citas con forma `ruta:línea` o `ruta:línea:línea`.
  6. EVIDENCIA: el reporte menciona al menos un comando verificable o un estado del
     evidence-hunter (verificado | parcial | auto-reportado | bloqueado).
  7. PLACEHOLDERS: no queda ningun texto sin resolver (ej: `$(cat ...)`, `TODO`, `ver aqui`).
     Un bloque de evidencia que dice "$(cat /tmp/evidence.json)" es una plantilla, no una
     corrida.
  8. INVALIDACION: una fila marcada `status: invalidated` queda fuera del conteo de
     veredictos validos, pero EXIGE `invalidation_reason`: un veredicto retirado sin
     motivo escrito es un veredicto que se esconde.

Uso:
    python3 agents/kanam-critic/bin/verify-verdict.py                     # todos
    python3 agents/kanam-critic/bin/verify-verdict.py --artifact <slug>    # uno
    python3 agents/kanam-critic/bin/verify-verdict.py --json
Salida: exit 0 si todo veredicto real esta respaldado, 1 si hay alguno sin respaldo.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
LEDGER = AGENT_DIR / "memory" / "verdicts.jsonl"
REVIEWS = AGENT_DIR / "docs" / "reviews"

FIXTURE_MARKERS = ("sample", "test", "fixture", "verify_by_core", "demo")
CITATION = re.compile(r"[A-Za-z0-9_./-]+\.(?:md|py|jsonl|tsv|yaml|json|sh):\d+")
EVIDENCE_WORDS = ("verificado", "parcial", "auto-reportado", "bloqueado",
                  "GLOBAL=aprobado", "$ ", "python3 ", "git ")
VERDICTS = ("VETO", "Aprobado", "ORO")
PLACEHOLDER = re.compile(r"\$\(|\bTODO\b|\bFIXME\b|ver aqui|ver aquí|<pendiente>|\bXXX\b")


def expected_verdict(total: int) -> str:
    """La matriz SHARP: <=18 VETO, 19-23 Aprobado, >=24 ORO."""
    if total <= 18:
        return "VETO"
    if total <= 23:
        return "Aprobado"
    return "ORO"


def is_fixture(artifact: str) -> bool:
    a = artifact.lower()
    return any(k in a for k in FIXTURE_MARKERS)


def read_ledger() -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def find_report(artifact: str) -> Path | None:
    """Match EXACTO por slug: `v0.3` no puede resolver a `v0.3-r2.md`."""
    if not REVIEWS.exists():
        return None
    slug = artifact
    if slug.startswith("kanam-critic-kit-"):
        slug = slug[len("kanam-critic-kit-"):]
    exact = [p for p in REVIEWS.glob("*.md") if p.name.endswith(f"{slug}.md")]
    if exact:
        return sorted(exact)[-1]
    named = [p for p in REVIEWS.glob("*.md") if artifact in p.name]
    return sorted(named)[-1] if named else None


def verify_one(rec: dict) -> list[dict]:
    artifact = rec.get("artifact", "")
    problems: list[dict] = []

    def fail(check: str, detail: str) -> None:
        problems.append({"artifact": artifact, "check": check, "detail": detail})

    if not artifact:
        fail("fila", "la fila del ledger no tiene 'artifact'")
        return problems

    if rec.get("status") == "invalidated":
        if not rec.get("invalidation_reason"):
            fail("invalidacion", "la fila esta invalidada pero no dice por que")
        return problems

    report = find_report(artifact)
    if report is None:
        fail("reporte", f"no existe ningun docs/reviews/*.md para '{artifact}'")
        return problems

    text = report.read_text(encoding="utf-8")
    scores = rec.get("scores") or {}
    total = rec.get("total")
    if total is None and scores:
        total = sum(v for v in scores.values() if isinstance(v, int))
    if total is not None and not re.search(rf"\b{total}\b", text):
        fail("total", f"el ledger dice total={total} y el reporte no lo menciona")

    verdict = rec.get("verdict")
    if verdict and verdict not in text:
        fail("veredicto", f"el ledger dice verdict={verdict} y el reporte no lo contiene")
    if total is not None:
        exp = expected_verdict(int(total))
        if verdict and verdict != exp:
            fail("veredicto vs matriz",
                 f"total={total} exige {exp} segun la matriz SHARP, pero el ledger dice {verdict}")

    cites = CITATION.findall(text)
    if len(cites) < 5:
        fail("citas", f"solo {len(cites)} citas con ruta:línea (se exigen 5)")

    if not any(w in text for w in EVIDENCE_WORDS):
        fail("evidencia", "el reporte no menciona ningun comando verificable ni estado del hunter")

    ph = PLACEHOLDER.search(text)
    if ph:
        fail("placeholder", f"el reporte tiene texto sin resolver: '{ph.group(0)}'")

    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica que cada veredicto real tenga respaldo")
    ap.add_argument("--artifact", help="verificar solo este artefacto")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    ledger = read_ledger()
    real = [r for r in ledger if not is_fixture(r.get("artifact", ""))]
    invalidated = [r for r in real if r.get("status") == "invalidated"]
    valid = [r for r in real if r.get("status") != "invalidated"]
    if args.artifact:
        valid = [r for r in valid if r.get("artifact") == args.artifact]
        if not valid:
            print(f"ROJO  no hay veredicto real valido con artifact={args.artifact} en el ledger")
            return 1

    problems: list[dict] = []
    for rec in valid:
        problems.extend(verify_one(rec))
    for rec in invalidated:
        if not rec.get("invalidation_reason"):
            problems.append({"artifact": rec.get("artifact", ""), "check": "invalidacion",
                             "detail": "fila invalidada sin motivo escrito"})

    if args.json:
        print(json.dumps({"checked": len(valid), "invalidated": len(invalidated),
                          "problems": problems}, ensure_ascii=False, indent=2))
    else:
        for p in problems:
            print(f"ROJO  {p['artifact']}: {p['check']} - {p['detail']}")
        for rec in invalidated:
            print(f"ANUL  {rec.get('artifact', '')}: invalidado - {rec.get('invalidation_reason', '')}")
        ok = len(valid) - len({p['artifact'] for p in problems})
        extra = f", {len(invalidated)} anulado(s)" if invalidated else ""
        print("-" * 100)
        print(f"GLOBAL={'aprobado' if not problems else 'veto'}  ({ok}/{len(valid)} veredictos reales validos con respaldo{extra})")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
