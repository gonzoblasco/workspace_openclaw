#!/usr/bin/env python3
"""check-voz.py - Gate de reglas prohibidas para textos de salida (voz de Gonzo).

Uso:
    python3 skills/voz-gonzo/check-voz.py <archivo> [--json]
    cat texto.txt | python3 skills/voz-gonzo/check-voz.py -

Exit: 0 = limpio, 1 = violaciones, 2 = error de uso.

Las reglas salen de docs/voz-gonzo.md (casos reales). Si el corpus cambia, actualizar aca
y en la SKILL.md a la vez: son la misma regla en dos formatos.
"""
from __future__ import annotations
import re
import sys
import json
import pathlib

PROHIBIDAS = [
    (r"\bestimad[oa]s?\b", "registro corporativo ('Estimado')"),
    (r"\bme alegro\b", "servilismo de apertura"),
    (r"\bexcelente oportunidad\b", "relleno"),
    (r"\bno dud[eé]s? en contactar", "cortesia vacia"),
    (r"\bquedo a (la )?(entera )?disposici[oó]n\b", "sumision"),
    (r"\bser[ií]a un honor\b", "epica decorativa"),
    (r"\bun abrazo grande\b", "cierre de relleno"),
    (r"\bsaludos cordiales\b", "cierre de plantilla"),
]

# Numeracion 1. 2. 3. en un texto corto = formato de documento metido en un chat
NUM_RE = re.compile(r"^\s*\d+[.)]\s+", re.M)


def check(text: str) -> dict:
    low = text.lower()
    viol = []
    for pat, why in PROHIBIDAS:
        for m in re.finditer(pat, low):
            viol.append({"regla": m.group(0), "motivo": why, "pos": m.start()})

    # numeracion solo si el texto es corto (chat). En documento formal es correcta.
    chars = len(text.strip())
    lineas_num = len(NUM_RE.findall(text))
    if lineas_num >= 2 and chars < 1200:
        viol.append({
            "regla": f"numeracion ({lineas_num} items)",
            "motivo": "vineta en chat, numeracion solo en documento",
            "pos": 0,
        })

    return {
        "ok": len(viol) == 0,
        "violaciones": viol,
        "chars": chars,
        "parrafos": len([p for p in text.split("\n\n") if p.strip()]),
    }


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv
    if not args:
        print(__doc__)
        return 2
    src = args[0]
    try:
        text = sys.stdin.read() if src == "-" else pathlib.Path(src).read_text()
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    r = check(text)
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        if r["ok"]:
            print(f"OK - sin violaciones ({r['chars']} chars)")
        else:
            print(f"VIOLACIONES: {len(r['violaciones'])}")
            for v in r["violaciones"]:
                print(f"  - {v['regla']!r}: {v['motivo']}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
