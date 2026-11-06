#!/usr/bin/env python3
"""handoff-gate.py - Gate de evidencia en el borde del pipeline (no un paso mas).

Por que existe (2026-11-06). El pipeline actual verifica el CODIGO (A escribe, B revisa,
el CORE corre build/tests) pero nadie verifica las AFIRMACIONES que entran y salen: un
revisor B puede afirmar "esto ya estaba resuelto" sin cita (paso el 2026-11-06, ver la
leccion `delegation-result-verification`), y un brief puede salir con links sin abrir.
Agregar un agente mas resuelve lo mismo que agregar una skill mas: infla. Lo que falta es
un gate que se evalua como el build.

Dos modos, un solo comando:

  out  - antes de marcar un handoff como entregado: audita el artefacto (kb-audit).
  in   - al recibir un handoff: verifica que cada claim citado resuelve y que trae veredicto.

Salida: JSON estable (pensado para `pipeline-track.sh note` y para CI).
Exit: 0 PASS/PARTIAL sin --strict, 1 FAIL con --strict, 2 error de uso.

Uso:
  handoff-gate.py out --role kanam-mind --artifact reports/brief.md [--strict] [--json]
  handoff-gate.py in  --handoff reports/handoff.json [--offline]
  handoff-gate.py in  --claims claims.json          # [{"text","source","date"?}, ...]

El handoff de entrada es el contrato de la skill `research-brief-protocol`:
  {"role": "...", "artifact": "path", "verdict": "PASS|PARTIAL|FAIL",
   "claims": [{"text": "...", "source": "path#Lx-Ly | URL", "date": "YYYY-MM-DD"}]}
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

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "kb-audit.py")
CITE_RE = re.compile(r"^(?P<path>.+)#L(?P<a>\d+)(?:-L(?P<b>\d+))?$")


def audit_out(artifact: str) -> dict:
    p = subprocess.run([sys.executable, AUDIT, artifact, "--json"], capture_output=True, text=True, timeout=300)
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"verdict": "FAIL", "findings": [{"kind": "audit", "severity": "fail", "line": 0,
                                                 "detail": f"kb-audit no devolvio JSON: {p.stderr[:200]}"}]}


def check_source(src: str, offline: bool, roots: list[str] | None = None) -> tuple[str, str]:
    """ok | fail | unknown + nota."""
    if src.startswith(("http://", "https://")):
        if offline:
            return "unknown", "offline"
        req = urllib.request.Request(src, method="HEAD", headers={"User-Agent": "kanam-mind-gate/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=8) as r:
                return "ok", str(r.status)
        except urllib.error.HTTPError as e:
            return ("unknown", f"http {e.code}") if e.code in (401, 403, 405, 429, 501, 503) else ("fail", f"http {e.code}")
        except Exception as e:  # noqa: BLE001
            return "unknown", type(e).__name__
    m = CITE_RE.match(src)
    path = m.group("path") if m else src
    if not os.path.isfile(path):
        roots = roots or []
        for root in roots:
            cand = path if os.path.isabs(path) else os.path.join(root, path)
            if os.path.isfile(cand):
                path = cand
                break
        else:
            return "fail", "archivo inexistente"
    if m:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                total = sum(1 for _ in fh)
        except OSError:
            return "fail", "ilegible"
        b = int(m.group("b") or m.group("a"))
        if not (1 <= int(m.group("a")) <= b <= total):
            return "fail", f"fuera de rango (archivo {total} lineas)"
    return "ok", "cita"


def evaluate_claims(claims: list[dict], offline: bool, roots: list[str] | None = None) -> tuple[str, list[dict]]:
    results = []
    worst = "ok"
    for c in claims:
        text = c.get("text", "")
        src = c.get("source", "")
        if not src:
            results.append({"claim": text, "state": "fail", "why": "sin fuente"})
            worst = "fail"
            continue
        st, why = check_source(src, offline, roots)
        if st == "fail":
            worst = "fail"
        elif st == "unknown" and worst == "ok":
            worst = "unknown"
        results.append({"claim": text[:120], "source": src, "state": st, "why": why, "date": c.get("date")})
    return worst, results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)

    o = sub.add_parser("out")
    o.add_argument("--role", required=True)
    o.add_argument("--artifact", required=True)
    o.add_argument("--strict", action="store_true")

    i = sub.add_parser("in")
    i.add_argument("--handoff")
    i.add_argument("--claims")
    i.add_argument("--offline", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.mode == "out":
        if not os.path.isfile(args.artifact):
            print(json.dumps({"error": f"artifact inexistente: {args.artifact}"}), file=sys.stderr)
            return 2
        rep = audit_out(args.artifact)
        verdict = rep.get("verdict", "FAIL")
        out = {"gate": "handoff-out", "role": args.role, "artifact": os.path.abspath(args.artifact),
               "verdict": verdict, "counts": rep.get("counts", {}),
               "findings": [f for f in rep.get("findings", []) if f.get("severity") == "fail"]}
    else:
        if args.claims:
            with open(args.claims, "r", encoding="utf-8") as fh:
                payload = json.load(fh)
            claims = payload if isinstance(payload, list) else payload.get("claims", [])
            verdict_declared = payload.get("verdict") if isinstance(payload, dict) else None
        elif args.handoff:
            with open(args.handoff, "r", encoding="utf-8") as fh:
                payload = json.load(fh)
            claims = payload.get("claims", [])
            verdict_declared = payload.get("verdict")
        else:
            print(json.dumps({"error": "falta --handoff o --claims"}), file=sys.stderr)
            return 2
        roots = [os.path.dirname(os.path.abspath(args.handoff or args.claims)), os.environ.get("MIND_ROOT", os.getcwd())]
        worst, results = evaluate_claims(claims, args.offline, roots)
        fails = [r for r in results if r["state"] == "fail"]
        if fails:
            verdict = "FAIL"
        elif worst == "unknown" or verdict_declared in (None, "PARTIAL"):
            verdict = "PARTIAL"
        else:
            verdict = "PASS"
        out = {"gate": "handoff-in", "verdict": verdict, "declared": verdict_declared,
               "claims": len(claims), "fails": fails, "results": results}

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print(f"HANDOFF GATE · {out['gate']} · {out['verdict']}")
        if out["gate"] == "handoff-out":
            print(f"  artifact={out['artifact']} counts={out['counts']}")
            for f in out["findings"]:
                print(f"  [fail] L{f['line']} <{f['kind']}> {f['detail']}")
        else:
            print(f"  claims={out['claims']} declared={out['declared']}")
            for r in out["results"]:
                print(f"  [{r['state']}] {r['source']} ({r['why']})")

    if args.mode == "out" and args.strict and out["verdict"] == "FAIL":
        return 1
    if args.mode == "in" and out["verdict"] == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
