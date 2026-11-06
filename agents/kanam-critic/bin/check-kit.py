#!/usr/bin/env python3
"""
check-kit.py - Verifica la salud del kit del Critic (el agente como entregable).

POR QUE EXISTE (2026-11-06).
El Critic se pidio a si mismo un veredicto real (T1) y el sujeto no fue un
proyecto de producto: fue EL AGENTE. Un agente no se audita leyendo su prosa,
se audita verificando hechos. Este script es la maquina de hechos del kit:
si algo del kit se rompe, lo dice con el comando exacto que lo reproduce.

QUE VERIFICA (todo con evidencia, no con opinion):
  1. Identidad propia: el workspace del agente tiene sus archivos de bootstrap
     (AGENTS/SOUL/IDENTITY/USER) y su propio MEMORY.md.
  2. Registro: las dos skills del Critic estan en el catalogo del workspace.
  3. Promesas: no queda ninguna referencia a `openclaw skill run` (comando que
     no existe; el CLI real es `openclaw skills`).
  4. Evidencia: el lab `evidence-hunter` corre y da GLOBAL=aprobado (5/5).
  5. Registro durable: `memory/verdicts.jsonl` existe y tiene al menos un
     veredicto REAL (no fixture de test).
  6. Respaldo: cada veredicto real tiene fila en el ledger Y reporte publicado
     con citas (`bin/verify-verdict.py`). Un veredicto reportado y no registrado
     NO existe.
  7. Disparadores: el agente tiene al menos un disparador configurado
     (heartbeat por agente o automatizacion programada).
  8. Presupuesto de bootstrap: los archivos del agente entran bajo el cap de
     inyeccion (20.000 por archivo, 4.000 para USER.md, 60.000 total).

Uso:
    python3 agents/kanam-critic/bin/check-kit.py            # tabla humana
    python3 agents/kanam-critic/bin/check-kit.py --json     # JSON
Salida: exit 0 si todo verde, 1 si hay algo rojo.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = AGENT_DIR.parent.parent
CATALOG = WORKSPACE_ROOT / ".knowledge" / "skills-catalog.tsv"
LAB_DIR = AGENT_DIR / "tests" / "evidence-hunter"

PER_FILE_CAP = 20_000
USER_CAP = 4_000
TOTAL_CAP = 60_000
BOOTSTRAP_FILES = ("AGENTS.md", "SOUL.md", "IDENTITY.md", "USER.md", "MEMORY.md")


def utf16_len(text: str) -> int:
    return len(text.encode("utf-16-le")) // 2


def check_identity() -> list[dict]:
    rows = []
    for name in ("AGENTS.md", "SOUL.md", "IDENTITY.md", "USER.md", "MEMORY.md"):
        p = AGENT_DIR / name
        if p.exists():
            rows.append({"check": f"identidad propia: {name}", "status": "verde",
                         "evidence": str(p.relative_to(WORKSPACE_ROOT))})
        else:
            rows.append({"check": f"identidad propia: {name}", "status": "rojo",
                         "evidence": "falta en el workspace del agente"})
    return rows


def check_catalog() -> list[dict]:
    rows = []
    if not CATALOG.exists():
        return [{"check": "catalogo de skills", "status": "rojo", "evidence": f"no existe {CATALOG}"}]
    text = CATALOG.read_text(encoding="utf-8")
    for skill in ("evidence-hunter", "sharp-adversarial-review"):
        lines = [l for l in text.splitlines() if l.split("\t")[0] == skill]
        if lines:
            rows.append({"check": f"catalogo: {skill}", "status": "verde",
                         "evidence": lines[0].split("\t")[1] if "\t" in lines[0] else lines[0]})
        else:
            rows.append({"check": f"catalogo: {skill}", "status": "rojo",
                         "evidence": "no esta en .knowledge/skills-catalog.tsv"})
    return rows


def check_promises() -> list[dict]:
    hits = []
    for p in AGENT_DIR.rglob("*.md"):
        if "memory/" in str(p) or "/.dreams/" in str(p):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if "openclaw skill run" not in line:
                continue
            # Solo cuentan las referencias que PROMETEN el comando. Las menciones
            # historicas (diagnostico, correccion, nota) no son promesas rotas.
            if any(k in line for k in ("prometen", "prometia", "prometía", "Corregido",
                                       "no existe", "promesa", "históric", "historico")):
                continue
            hits.append(f"{p.relative_to(WORKSPACE_ROOT)}:{i}")
    if hits:
        return [{"check": "promesas rotas: 'openclaw skill run'", "status": "rojo",
                 "evidence": ", ".join(hits)}]
    return [{"check": "promesas rotas: 'openclaw skill run'", "status": "verde",
             "evidence": "sin referencias vivas"}]


def check_lab() -> list[dict]:
    if not LAB_DIR.exists():
        return [{"check": "lab evidence-hunter", "status": "rojo", "evidence": "no existe el lab"}]
    try:
        subprocess.run([sys.executable, "scaffold.py"], cwd=LAB_DIR, capture_output=True, timeout=60)
        subprocess.run([sys.executable, "build_assertions.py"], cwd=LAB_DIR, capture_output=True, timeout=60)
        out = Path("/tmp/kit-assertions.yaml")
        with out.open("w") as fh:
            subprocess.run([sys.executable, "build_assertions.py"], cwd=LAB_DIR,
                           timeout=60, stdout=fh, stderr=subprocess.DEVNULL)
        ev = Path("/tmp/kit-evidence.json")
        with ev.open("w") as fh:
            r = subprocess.run([sys.executable, str(AGENT_DIR / "bin" / "evidence-hunter.py"), str(out)],
                               text=True, timeout=120, stdout=fh, stderr=subprocess.PIPE)
        if r.returncode != 0:
            return [{"check": "lab evidence-hunter", "status": "rojo",
                     "evidence": f"runner rc={r.returncode}: {r.stderr.strip()[:120]}"}]
        v = subprocess.run([sys.executable, "validate.py", str(ev)], cwd=LAB_DIR,
                           capture_output=True, text=True, timeout=60)
        tail = [l for l in v.stdout.splitlines() if l.startswith("GLOBAL=")]
        status = "verde" if "aprobado" in (tail[0] if tail else "") else "rojo"
        return [{"check": "lab evidence-hunter", "status": status,
                 "evidence": tail[0] if tail else v.stdout.strip()[-120:]}]
    except Exception as exc:  # noqa: BLE001
        return [{"check": "lab evidence-hunter", "status": "bloqueado",
                 "evidence": f"{type(exc).__name__}: {exc}"}]


def check_verdicts() -> list[dict]:
    p = AGENT_DIR / "memory" / "verdicts.jsonl"
    if not p.exists():
        return [{"check": "veredictos reales registrados", "status": "rojo", "evidence": "no existe verdicts.jsonl"}]
    real, fixtures = 0, 0
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        art = (rec.get("artifact") or "").lower()
        if any(k in art for k in ("sample", "test", "fixture", "verify_by_core", "demo")):
            fixtures += 1
        else:
            real += 1
    status = "verde" if real >= 1 else "rojo"
    return [{"check": "veredictos reales registrados", "status": status,
             "evidence": f"{real} real(es), {fixtures} fixture(s)"}]


def check_verdict_backing() -> list[dict]:
    """Un veredicto no existe hasta que tiene fila Y reporte con citas (ADR del guard)."""
    guard = AGENT_DIR / "bin" / "verify-verdict.py"
    if not guard.exists():
        return [{"check": "veredictos con respaldo (verify-verdict.py)", "status": "rojo",
                 "evidence": "falta bin/verify-verdict.py"}]
    r = subprocess.run([sys.executable, str(guard)], capture_output=True, text=True, timeout=120)
    tail = [l for l in r.stdout.splitlines() if l.startswith("GLOBAL=")]
    status = "verde" if r.returncode == 0 and tail and "aprobado" in tail[0] else "rojo"
    detail = tail[0] if tail else r.stdout.strip().splitlines()[-1][:120]
    if r.returncode != 0:
        reds = [l for l in r.stdout.splitlines() if l.startswith("ROJO")]
        if reds:
            detail = reds[0][:140]
    return [{"check": "veredictos con respaldo (verify-verdict.py)", "status": status,
             "evidence": detail}]


def check_triggers() -> list[dict]:
    rows = []
    cfg = Path.home() / ".openclaw" / "openclaw.json"
    hb = False
    if cfg.exists():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
            entry = data.get("agents", {}).get("entries", {}).get("kanam-critic", {})
            hb = bool(entry.get("heartbeat", {}).get("every"))
        except json.JSONDecodeError:
            pass
    rows.append({"check": "disparador: heartbeat por agente", "status": "verde" if hb else "rojo",
                 "evidence": "agents.entries.kanam-critic.heartbeat" if hb else "sin heartbeat configurado"})
    return rows


def check_budget() -> list[dict]:
    rows = []
    total = 0
    for name in BOOTSTRAP_FILES:
        p = AGENT_DIR / name
        if not p.exists():
            continue
        n = utf16_len(p.read_text(encoding="utf-8"))
        total += n
        cap = USER_CAP if name.lower() == "user.md" else PER_FILE_CAP
        rows.append({"check": f"presupuesto: {name}", "status": "verde" if n <= cap else "rojo",
                     "evidence": f"{n} / {cap} caracteres"})
    rows.append({"check": "presupuesto: total", "status": "verde" if total <= TOTAL_CAP else "rojo",
                 "evidence": f"{total} / {TOTAL_CAP} caracteres"})
    return rows


def main() -> int:
    as_json = "--json" in sys.argv
    rows: list[dict] = []
    for fn in (check_identity, check_catalog, check_promises, check_lab,
               check_verdicts, check_verdict_backing, check_triggers, check_budget):
        rows.extend(fn())
    red = [r for r in rows if r["status"] != "verde"]
    if as_json:
        print(json.dumps({"checks": rows, "red": len(red)}, ensure_ascii=False, indent=2))
    else:
        for r in rows:
            mark = {"verde": "OK  ", "rojo": "ROJO", "bloqueado": "BLOQ"}[r["status"]]
            print(f"[{mark}] {r['check']:<52} {r['evidence']}")
        print("-" * 100)
        print(f"GLOBAL={'aprobado' if not red else 'veto'}  ({len(rows) - len(red)}/{len(rows)} checks verdes)")
    return 0 if not red else 1


if __name__ == "__main__":
    sys.exit(main())
