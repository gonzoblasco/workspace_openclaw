#!/usr/bin/env python3
"""Evaluador de la suite oculta de una cata (plantilla del kit).

Copiado de la cata 2026-11-16, que paso la validacion en las dos direcciones.
Para una cata nueva: reemplazar T1_CHILD / T2_CHILD / t3_checks por los asserts
de tus tareas, y actualizar CHECKS con sus ids.

Uso:
  python3 evaluate.py --task T1 --file candidato.py
  python3 evaluate.py --task T3 --text respuesta.md
  python3 evaluate.py --selftest          # valida en las dos direcciones

Los asserts viven acá y NO se regeneran: se corrigen a mano y se vuelven a
validar con --selftest (referencia 100% PASS, defectuosas 100% FAIL).
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASKS_PATH = Path(os.environ.get("CATA_TASKS", str(HERE / "tasks.json")))
CHILD_TIMEOUT = 20


# ---------------------------------------------------------------- extraction
def extract_last_python_block(text: str) -> str:
    """Ultimo bloque con `def `, como manda el step 4 (nunca el primero)."""
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, re.S)
    with_def = [b for b in blocks if re.search(r"^\s*def \w+\(", b, re.M)]
    if with_def:
        return with_def[-1]
    if blocks:
        return blocks[-1]
    m = re.search(r"^(\s*def \w+\(.*)$", text, re.M | re.S)
    return m.group(1) if m else ""


# ----------------------------------------------------------------- T1 checks
T1_CHILD = r"""
import json, random, sys
from datetime import date, timedelta
src = open(sys.argv[1]).read()
ns = {}
exec(compile(src, "candidate", "exec"), ns)
f = ns.get("chunk_ranges")
def run():
    if not callable(f):
        return ["no define chunk_ranges"]
    errs = []
    cases = [
        (("2026-01-01", "2026-01-01", 5), [("2026-01-01", "2026-01-01")]),
        (("2026-01-01", "2026-01-10", 5), [("2026-01-01", "2026-01-05"), ("2026-01-06", "2026-01-10")]),
        (("2026-01-01", "2026-01-12", 5), [("2026-01-01", "2026-01-05"), ("2026-01-06", "2026-01-10"), ("2026-01-11", "2026-01-12")]),
        (("2026-02-26", "2026-03-02", 4), [("2026-02-26", "2026-03-01"), ("2026-03-02", "2026-03-02")]),
        (("2026-01-10", "2026-01-01", 3), []),
    ]
    for args, want in cases:
        try:
            got = [tuple(x) for x in f(*args)]
        except Exception as e:
            errs.append(f"{args}: excepcion {type(e).__name__}: {e}")
            continue
        if got != want:
            errs.append(f"{args}: got={got} want={want}")
    try:
        f("2026-01-01", "2026-01-02", 0)
        errs.append("days=0 no lanza ValueError")
    except ValueError:
        pass
    except Exception as e:
        errs.append(f"days=0 lanza {type(e).__name__}, no ValueError")
    # propiedad: 40 rangos aleatorios
    rnd = random.Random(7)
    base = date(2025, 12, 1)
    for _ in range(40):
        s = base + timedelta(days=rnd.randrange(0, 400))
        e = s + timedelta(days=rnd.randrange(0, 60))
        d = rnd.randrange(1, 12)
        try:
            got = [tuple(x) for x in f(s.isoformat(), e.isoformat(), d)]
        except Exception as ex:
            errs.append(f"prop {s}..{e} d={d}: {type(ex).__name__}: {ex}")
            continue
        if not got:
            errs.append(f"prop {s}..{e} d={d}: vacio")
            continue
        if got[0][0] != s.isoformat() or got[-1][1] != e.isoformat():
            errs.append(f"prop {s}..{e} d={d}: no cubre extremos")
            continue
        prev = None
        ok = True
        for a, b in got:
            da, db = date.fromisoformat(a), date.fromisoformat(b)
            if da > db or (db - da).days + 1 > d:
                ok = False; break
            if prev is not None and da != prev + timedelta(days=1):
                ok = False; break
            prev = db
        if not ok:
            errs.append(f"prop {s}..{e} d={d}: tramos invalidos {got[:4]}")
    return errs
errs = run()
print(json.dumps({"pass": not errs, "asserts_failed": errs[:6], "n_fail": len(errs)}))
"""

# ----------------------------------------------------------------- T2 checks
T2_CHILD = r"""
import json, sys
src = open(sys.argv[1]).read()
ns = {}
exec(compile(src, "candidate", "exec"), ns)
f = ns.get("invoice_total")
errs = []
if not callable(f):
    errs.append("no define invoice_total")
else:
    cases = [
        (([(1, 33.333), (1, 33.333), (1, 33.333)], 10, 21), 108.90),
        (([(2, 19.995), (3, 7.775)], 0, 21), 76.61),
        (([(1, 100.0)], 15, 21), 102.85),
        (([], 10, 21), 0.0),
    ]
    for args, want in cases:
        try:
            got = f(*args)
        except Exception as e:
            errs.append(f"{args}: excepcion {type(e).__name__}: {e}"); continue
        if got is None or abs(float(got) - want) > 1e-9:
            errs.append(f"{args}: got={got} want={want}")
print(json.dumps({"pass": not errs, "asserts_failed": errs[:6], "n_fail": len(errs)}))
"""

# ----------------------------------------------------------------- T3 checks
def t3_checks(text: str) -> list[str]:
    errs = []
    t = text.lower().replace("\u00a0", " ")
    nums = re.findall(r"235[.,]74", t)
    if not nums:
        errs.append("no reporta 235.74")
    if not re.search(r"duplicad|\bid\s*[:=]?\s*3\b|fila\s*(con\s*)?id\s*3", t):
        errs.append("no menciona el id duplicado (3)")
    if not re.search(r"\beur\b|fila\s*4", t):
        errs.append("no menciona la fila EUR excluida")
    if not re.search(r"fila\s*7|fuera\s*del\s*(trimestre|q3)|octubre|2026-10-01", t):
        errs.append("no menciona la fila fuera de Q3")
    return errs


CHECKS = {
    "T1-chunk-ranges": ("code", T1_CHILD),
    "T2-invoice-bug": ("code", T2_CHILD),
    "T3-q3-revenue": ("analysis", t3_checks),
}


def evaluate(task_id: str, text: str) -> dict:
    if task_id not in CHECKS:
        raise SystemExit(f"tarea desconocida: {task_id} (registrala en CHECKS)")
    kind, check = CHECKS[task_id]
    if kind == "analysis":
        errs = check(text)
        return {"task": task_id, "pass": not errs, "asserts_failed": errs, "n_fail": len(errs)}
    child = check

    code = text if "```" not in text else extract_last_python_block(text)
    if not code:
        return {"task": task_id, "pass": False, "asserts_failed": ["sin bloque de codigo"], "n_fail": 1}
    with tempfile.TemporaryDirectory() as td:
        cand = Path(td) / "cand.py"
        cand.write_text(code)
        try:
            r = subprocess.run([sys.executable, "-c", child, str(cand)],
                               capture_output=True, text=True, timeout=CHILD_TIMEOUT)
        except subprocess.TimeoutExpired:
            return {"task": task_id, "pass": False, "asserts_failed": ["timeout 20s"], "n_fail": 1}
    try:
        out = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return {"task": task_id, "pass": False,
                "asserts_failed": [f"child fallo: {r.stderr.strip()[:200]}"], "n_fail": 1}
    out["task"] = task_id
    return out


def selftest() -> int:
    refs = HERE / "reference"
    bad = HERE / "defective"
    ok = True
    for f in sorted(refs.iterdir()):
        if f.name.startswith("."):
            continue
        tid = f.name.split(".")[0]
        res = evaluate(tid, f.read_text())
        print(f"REF  {f.name:28s} pass={res['pass']} fails={res['asserts_failed']}")
        ok &= res["pass"]
    for f in sorted(bad.iterdir()):
        if f.name.startswith("."):
            continue
        tid, tag = f.name.split(".")[0], f.name.split(".")[1]
        res = evaluate(tid, f.read_text())
        good = not res["pass"]
        print(f"BAD  {f.name:28s} fails_as_expected={good} fails={res['asserts_failed'][:2]}")
        ok &= good
    print("SELFTEST", "OK" if ok else "FALLA")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--task")
    ap.add_argument("--file")
    ap.add_argument("--text")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    text = a.text if a.text is not None else Path(a.file).read_text()
    print(json.dumps(evaluate(a.task, text), ensure_ascii=False))
