"""Siembra bugs conocidos en `reports.py` para medir recall/precision del revisor B.

La verdad esta en `bench/GROUND_TRUTH.md`. IMPORTANTE: este script y el ground
truth NO deben estar en el working directory del agente revisor B, o el
benchmark deja de medir nada.

Uso:
    python3 bench/seed_bugs.py <dir_destino>
    # espera: <dir_destino>/reports.py debe ser una copia limpia de
    # bench/base/reports.py
"""
import pathlib
import sys

dst = pathlib.Path(sys.argv[1])
src = dst / "reports.py"
text = src.read_text()

BUGS = [
    # (id, needle viejo, needle nuevo, visible en los tests de A o no)
    (
        "BUG-1",
        "if not isinstance(per_page, int) or per_page <= 0:",
        "if not isinstance(per_page, int) or per_page < 0:",
        "visible",
    ),
    (
        "BUG-2",
        "if since_date <= rec_date <= until_date:",
        "if since_date <= rec_date < until_date:",
        "visible",
    ),
    (
        "BUG-3",
        "        age = (now - cached_at).total_seconds()",
        "        age = (cached_at - now).total_seconds()",
        "oculto",
    ),
    (
        "BUG-4",
        "        if age <= ttl_seconds:\n            return list(data)",
        "        if age <= ttl_seconds:\n            return data",
        "oculto",
    ),
]

for bug_id, old, new, kind in BUGS:
    if old not in text:
        print(f"!! {bug_id}: no match")
        sys.exit(1)
    text = text.replace(old, new, 1)
    print(f"   sembrado {bug_id} ({kind})")

src.write_text(text)
print(f"OK -> {src}")
