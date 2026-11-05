#!/usr/bin/env python3
"""check-handoff-merge.py - Impide que un cierre PISE pendientes heredados.

POR QUE EXISTE (2026-11-04). La regla estaba escrita en `session-close-handoff` paso 3:
"leer el HANDOFF vigente antes de generarlo, clasificar cada seccion en sigue-vivo /
hecho / cambio, y fusionar en los flags". Kanam la salteo igual y el HANDOFF de las 21:14
borro 8 pendientes de la sesion de las 16:10. Una regla escrita y no verificada se viola
sola: es el mismo defecto que origino `check-pipeline-enforcement.py`.

Que hace: compara el HANDOFF nuevo contra el anterior y falla si un pendiente o una decision
del anterior DESAPARECIO sin estar declarado como cerrado.

Como declarar un cierre legitimo: agregar el item al bloque/seccion CERRADOS del HANDOFF,
o pasar `--closed "<texto>"` (una vez por item). Sin eso, la desaparicion es un error.

Uso:
    python3 scripts/check-handoff-merge.py --new .knowledge/HANDOFF.md \\
        [--prev .knowledge/handoff-history/<anterior>.md] [--json]

    # sin --prev: toma el backup mas reciente del historial que no sea el nuevo
    # exit 0 = fusion ok,exit 1 = hay pendientes perdidos,exit 2 = error de uso
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import sys

# Palabras que no aportan identidad a un item
STOP = set("""
para por que con sin sobre entre desde hasta donde cuando como cual cuales
esta estan este esto estos estas sean sera ser esta fueron fue son del las los
una uno unos unas mas menos muy poco mucho todo toda todos todas
hay sea puede pueden debe deben hacer hecho hacerlo
ademas tambien solo cada otro otra mismos mismas mismo misma
""".split())

SEC_RE = re.compile(r"^##\s+(.+)$", re.M)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def sections(text: str) -> dict[str, str]:
    """Devuelve {titulo_normalizado: cuerpo}."""
    out: dict[str, str] = {}
    matches = list(SEC_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = m.group(1).strip().lower()
        out[title] = text[start:end]
    return out


def find_section(secs: dict[str, str], *needles: str) -> str:
    for title, body in secs.items():
        if any(n in title for n in needles):
            return body
    return ""


def strip_comments(t: str) -> str:
    return COMMENT_RE.sub(" ", t)


def split_items(body: str) -> list[str]:
    """Parte un bloque en items: vinetas, 'N)' y 'N.' al inicio de segmento."""
    raw = strip_comments(body)
    raw = raw.replace("\r", "")
    # separadores: vineta, 'N)', 'N.' (con o sin salto antes). El 'N)' interno
    # tambien separa, porque el generador pega varios pendientes en una linea.
    parts = re.split(r"(?:^|\n)\s*(?:[-*]\s+|\d+[.)]\s*)|\s(?:\d+)\)\s+", raw)
    items = []
    for p in parts:
        p = " ".join(p.split())
        p = p.strip(" .;,")
        if len(p) > 12:
            items.append(p)
    return items


def fingerprint(item: str) -> set[str]:
    words = re.findall(r"[a-z0-9][a-z0-9._/-]{3,}", item.lower())
    return {w for w in words if w not in STOP and not w.isdigit()}


def coverage(fp: set[str], haystack: str) -> float:
    if not fp:
        return 1.0
    hits = sum(1 for w in fp if w in haystack)
    return hits / len(fp)


def analyze(new_text: str, prev_text: str, closed_extra: list[str],
            threshold: float = 0.55) -> dict:
    new_secs = sections(new_text)
    prev_secs = sections(prev_text)

    closed_block = find_section(new_secs, "cerrad", "done", "closed").lower()
    closed_extra_low = " ".join(closed_extra).lower()
    haystack = strip_comments(new_text).lower() + " " + closed_extra_low

    checks = []
    for label, needles in (("pendientes", ("proximo", "next", "pendient")),
                           ("decisiones", ("decision",))):
        prev_body = find_section(prev_secs, *needles)
        if not prev_body.strip():
            continue
        for item in split_items(prev_body):
            fp = fingerprint(item)
            if not fp:
                continue
            cov = coverage(fp, haystack)
            in_closed = coverage(fp, closed_block) >= threshold
            checks.append({
                "seccion": label,
                "item": item[:160],
                "cobertura": round(cov, 2),
                "declarado_cerrado": in_closed,
                "ok": cov >= threshold or in_closed,
            })

    missing = [c for c in checks if not c["ok"]]
    return {"checks": checks, "missing": missing, "ok": not missing}


NAME_TS_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})-(\d{2})(\d{2})(?:-(\d+))?-HANDOFF\.md$")


def _name_key(p: pathlib.Path) -> tuple:
    """Clave de orden por la FECHA DEL NOMBRE, no por mtime.

    Por que (medido 2026-11-04): el HANDOFF anterior se elegia por `st_mtime`, y
    al restaurar con `git restore` tres backups viejos del 27/10, esos archivos
    pasaron a tener mtime de HOY. El gate eligio un backup de 8 dias antes como
    "el anterior" y reporto 7 pendientes perdidos que nunca existieron. El nombre
    del archivo lleva la fecha real y no la toca ninguna operacion de git.
    """
    m = NAME_TS_RE.search(p.name)
    if not m:
        return (0, 0, 0, 0, 0, 0)
    y, mo, d, hh, mm, n = m.groups()
    return (int(y), int(mo), int(d), int(hh), int(mm), int(n or 0))


def pick_prev(new_path: pathlib.Path) -> pathlib.Path | None:
    hist = new_path.parent / "handoff-history"
    if not hist.is_dir():
        return None
    cands = sorted(hist.glob("*-HANDOFF.md"), key=_name_key, reverse=True)
    return cands[0] if cands else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", default=".knowledge/HANDOFF.md")
    ap.add_argument("--prev", default="")
    ap.add_argument("--closed", action="append", default=[])
    ap.add_argument("--threshold", type=float, default=0.55)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    newp = pathlib.Path(a.new)
    if not newp.exists():
        print(f"error: no existe {newp}", file=sys.stderr)
        return 2
    prevp = pathlib.Path(a.prev) if a.prev else pick_prev(newp)
    if prevp is None or not prevp.exists():
        # primer HANDOFF: nada que comparar
        if a.json:
            print(json.dumps({"ok": True, "reason": "sin HANDOFF previo"}))
        else:
            print("OK - sin HANDOFF previo para comparar")
        return 0

    res = analyze(newp.read_text(), prevp.read_text(), a.closed, a.threshold)

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res["ok"] else 1

    total = len(res["checks"])
    print(f"HANDOFF merge check  (prev: {prevp.name})")
    print(f"  items heredados: {total}")
    print(f"  conservados:     {total - len(res['missing'])}")
    print(f"  perdidos:        {len(res['missing'])}")

    if res["missing"]:
        print("\nPERDIDOS SIN DECLARAR CIERRE:")
        for m in res["missing"]:
            print(f"  [{m['seccion']}] cov={m['cobertura']}  {m['item']}")
        print("\nFusiona el item en los flags, o declara el cierre con --closed \"<texto>\".")
        return 1

    print("\nOK - fusion completo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
