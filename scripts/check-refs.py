#!/usr/bin/env python3
"""
check-refs.py - Verifica que las rutas citadas en los docs existan de verdad.

Por que existe: docs/AGENTS-DETALLE.md citaba `scripts/pr-thread-brief.sh` como
la "verificacion mecanica" de una regla dura (atribucion por login), y ese
script nunca existio. Una regla que dice tener respaldo sin tenerlo es peor que
una regla sin respaldo: da confianza falsa. Este chequeo hace visible esa clase
de pudricion antes de que alguien confie en ella.

Que revisa: rutas con backticks que empiezan con scripts/ o docs/ y apuntan a
un archivo con extension. Los directorios, los placeholders (<...>) y las lineas
de uso con argumentos se ignoran a proposito.

Uso:
    check-refs.py [archivos...]     por default, los docs del agente
    check-refs.py --all             ademas, todos los docs/*.md
Salida: exit 0 si todo existe, 1 si hay rutas rotas.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULTS = ["README.md", "AGENTS.md", "USER.md", "MEMORY.md", "SOUL.md", "IDENTITY.md", "SKILLS-INDEX.md"]

# Ruta entre backticks que empieza con scripts/ o docs/ Y termina en extension.
# El primer grupo es la ruta; el `!` evita capturar espacios internos.
REF = re.compile(r"`((?:scripts|docs)/[^\s`]+\.(?:sh|py|js|cjs|md|json|txt|pdf|yml))`")

# Link markdown `[texto](destino)`. El REF de arriba solo mira backticks y solo
# scripts/docs: por eso los links `./skills/.../SKILL.md` de AGENTS.md podian
# apuntar a la nada sin que nada lo dijera (encontrado 2026-09-26: 5 de 6 rotos
# tras mover skills a agents/<rol>/skills). Un link es una afirmacion de que el
# archivo existe; este regex la verifica.
LINK = re.compile(r"\]\(([^)\s]+)\)")

# Espacios de nombres que este repo puede resolver. Un destino fuera de estos
# (o externo, o ancla) no se revisa: no es una promesa sobre este arbol.
LINK_PREFIXES = ("skills/", "agents/", "scripts/", "docs/", "./", "../")

# Lo que NO es una ruta literal y no debe reportarse.
SKIP_IF = [
    lambda r: "<" in r or ">" in r,       # placeholders: docs/feedback/<repo>-<n>.md
    lambda r: r.endswith("/"),            # directorios
    lambda r: "*" in r,                   # globs
]


def is_link_skippable(target: str) -> bool:
    """Un link que no promete nada sobre este arbol no se verifica."""
    if any(c in target for c in ("<", ">", "*", "{")):
        return True
    if target.startswith(("http://", "https://", "mailto:", "#", "/")):
        return True
    if not target.startswith(LINK_PREFIXES):
        return True
    # Un link que termina en `/` promete que ese DIRECTORIO existe. Antes se
    # saltaba con el criterio "link a directorio, no a archivo", y eso tapaba
    # 42 links rotos de SKILLS-INDEX.md (apuntaban a `skills/<slug>/`, que ya
    # no existe: las skills viven en `agents/<rol>/skills/`). Un directorio
    # inexistente es una promesa rota igual que un archivo inexistente.
    return False


def resolves(source: Path, target: str) -> bool:
    """Resuelve el destino con las dos convenciones que usa este repo.

    Markdown puro resuelve relativo al doc que cita. Pero el workspace escribe
    `./skills/...` anclado a la raiz tambien dentro de docs/ (asi esta en
    docs/pipeline/). Aceptar cualquiera de las dos evita el falso positivo de
    una convencion valida, sin dejar pasar un link que no existe en ninguna.
    """
    if (ROOT / target).exists():
        return True
    return (source.parent / target).resolve().exists()

# Directorios historicos: se leen como se escribieron, no se corrigen. Una
# ruta rota ahi es un dato del pasado, no una promesa vigente.
SKIP_DIRS = ("docs/archives/", "docs/history/", "docs/conversations/")


def is_skippable(ref: str) -> bool:
    return any(f(ref) for f in SKIP_IF)


def files_to_scan(argv):
    if argv and argv[0] == "--all":
        extra = sorted(p for p in (ROOT / "docs").rglob("*.md"))
        return [ROOT / f for f in DEFAULTS] + extra
    if argv:
        return [Path(a) if Path(a).is_absolute() else ROOT / a for a in argv]
    return [ROOT / f for f in DEFAULTS]


def main():
    # OJO: no filtrar los flags aca. `--all` es un flag y a la vez la senal
    # de modo; descartar los args que empiezan con "-" antes de mirarlo hacia
    # que `--all` cayera al default en silencio y el chequeo reportara OK sin
    # haber escaneado los docs extra. (Bug real, cazado por el propio test.)
    argv = sys.argv[1:]
    files = files_to_scan(argv)

    broken = []
    checked = 0

    for path in files:
        if not path.exists():
            continue
        rel_str = str(path.relative_to(ROOT))
        if any(rel_str.startswith(d) for d in SKIP_DIRS):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            for ref in REF.findall(line):
                if is_skippable(ref):
                    continue
                checked += 1
                if not (ROOT / ref).exists():
                    broken.append((path.relative_to(ROOT), line_no, ref))
            for target in LINK.findall(line):
                if is_link_skippable(target):
                    continue
                checked += 1
                if not resolves(path, target):
                    broken.append((path.relative_to(ROOT), line_no, target))

    if broken:
        print(f"RUTAS ROTAS ({len(broken)} de {checked} revisadas):")
        for f, ln, ref in broken:
            print(f"  {f}:{ln}  ->  {ref}")
        print()
        print("Cada ruta citada deberia existir, o no se cita.")
        return 1

    print(f"OK: {checked} rutas citadas, todas existen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
