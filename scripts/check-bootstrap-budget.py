#!/usr/bin/env python3
"""
check-bootstrap-budget.py - Verifica que los archivos de BOOTSTRAP entren bajo el
cap de inyeccion del runtime de OpenClaw.

POR QUE EXISTE (2026-10-06, ROADMAP 0.1). Los archivos que OpenClaw inyecta en
CADA arranque de sesion (AGENTS.md, MEMORY.md, USER.md, SOUL.md, IDENTITY.md)
tienen un cap. Lo que lo supera SE TRUNCA EN SILENCIO: el agente arranca sin esas
reglas y no lo sabe. Es la deuda mas cara y la mas invisible: se paga en cada
turno y no deja rastro. El 2026-10-06 AGENTS/MEMORY/USER estaban los tres sobre
su cap; AGENTS ya bajo una vez (2026-09-14) y USER.md regreso (3.986 -> 4.582).
Una regla escrita sin guarda se viola sola.

DE DONDE SALEN LOS NUMEROS (verificado contra el codigo instalado, OpenClaw
2026.9.8, `dist/bootstrap-*.mjs`):
  - DEFAULT_BOOTSTRAP_MAX_CHARS  = 2e4  -> 20.000 por archivo (AGENTS/MEMORY/SOUL/IDENTITY)
  - USER_BOOTSTRAP_MAX_CHARS     = 4e3  -> 4.000 SOLO para USER.md (cap fijo, no configurable)
  - DEFAULT_BOOTSTRAP_TOTAL_MAX_CHARS = 6e4 -> 60.000 sumando todos
No se derivan de config: no hay override en `openclaw.json` (verificado), asi que
aplican los defaults. Si algun dia se agrega `bootstrapMaxChars`, los numeros de
aca hay que alinearlos.

QUE MIDE: caracteres como los cuenta el runtime, no bytes. El runtime mide
`.length` de JavaScript, que son unidades UTF-16: un caracter sobre U+FFFF (emoji,
por ejemplo) cuenta 2. `wc -c` (bytes) SOBREESTIMA en espanol por los acentos:
USER.md medido con `wc -c` daba 3.976 (margen 24), medido como el runtime 3.933
(margen 67). Medir en bytes da un falso rojo y un margen equivocado.

Uso:
    check-bootstrap-budget.py
Salida: exit 0 si todos entran bajo cap; 1 si alguno supera el suyo o el total.
"""

import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent

# Cap por archivo. USER.md tiene cap fijo propio (4.000); el resto comparte 20.000.
PER_FILE_CAP = 20_000
USER_CAP = 4_000
TOTAL_CAP = 60_000

# Orden = orden de inyeccion. La lista es EXPLICITA: el check existe para atrapar
# un archivo que crece de mas, y una lista derivada de "los .md que hay en la raiz"
# confundiria el bootstrap con documentacion cualquiera.
BOOTSTRAP_FILES = ("AGENTS.md", "MEMORY.md", "USER.md", "SOUL.md", "IDENTITY.md")


def utf16_len(text: str) -> int:
    """Largo como lo mide JS (`.length`): unidades UTF-16, astrales cuentan 2."""
    return len(text.encode("utf-16-le")) // 2


def cap_for(name: str) -> int:
    return USER_CAP if name.lower() == "user.md" else PER_FILE_CAP


def measure(root: Path) -> List[dict]:
    """Mide cada archivo de bootstrap que exista.

    Ausente = se omite a propósito: la existencia la cubren otras guardas, y un
    archivo ausente no tiene cap que violar. Pero si NINGUNO existe, no hay nada
    que medir y el check no puede dar verde: main() lo reporta como no corrible.
    (Regla 1 de skills/verification-gates: cero casos corridos no es verde.)
    """
    rows: List[dict] = []
    for name in BOOTSTRAP_FILES:
        path = root / name
        if not path.is_file():
            continue
        chars = utf16_len(path.read_text(encoding="utf-8"))
        cap = cap_for(name)
        rows.append({"name": name, "chars": chars, "cap": cap, "margin": cap - chars})
    return rows


def find_violations(root: Path) -> List[str]:
    rows = measure(root)
    violations: List[str] = []
    for r in rows:
        if r["chars"] > r["cap"]:
            violations.append(
                "%s: %d chars > cap %d (sobra %d) - se trunca en silencio en cada "
                "arranque. Mover el detalle a docs/ o memory/."
                % (r["name"], r["chars"], r["cap"], r["chars"] - r["cap"])
            )
    total = sum(r["chars"] for r in rows)
    if total > TOTAL_CAP:
        violations.append(
            "TOTAL: %d chars > cap %d (sobra %d)." % (total, TOTAL_CAP, total - TOTAL_CAP)
        )
    return violations


def main() -> int:
    rows = measure(ROOT)
    if not rows:
        print("ERROR no hay archivos de bootstrap que medir; "
              "no se pudo correr (exit 3)", file=sys.stderr)
        return 3
    total = sum(r["chars"] for r in rows)
    violations = find_violations(ROOT)
    if violations:
        print("BOOTSTRAP SOBRE CAP:")
        for v in violations:
            print(f"  {v}")
        print()
        print("Un archivo de bootstrap es contexto que se inyecta en cada turno:")
        print("lo que lo supera NO se pierde con un warning, se pierde callado.")
        print("El detalle va a docs/ o memory/ (que memory_search si indexa).")
        return 1

    head = " " + "  ".join(
        f"{r['name']}={r['chars']}/{r['cap']}(+{r['margin']})" for r in rows
    )
    print(f"OK: {len(rows)} archivos de bootstrap bajo cap; total {total}/{TOTAL_CAP}.")
    print(head)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
