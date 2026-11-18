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
# Rutas que este repo puede resolver y que un doc puede prometer. Un destino
# fuera de estos (o externo, o ancla) no se revisa: no es una promesa sobre
# este arbol.
# `projects/` faltaba: el 2026-10-29 se borro `projects/kanam-tetris/` y NORTH.md
# siguio citando `projects/kanam-tetris/.knowledge/ROADMAP-TETRIS.md` durante
# semanas con el guard en verde ("744 rutas, todas existen"). El guard no mentia:
# nunca miro esa ruta. Los patrones (`projects/*`, `projects/<slug>`) los filtra
# SKIP_IF, asi que agregar el prefijo no llena el reporte de falsos positivos.
REF = re.compile(r"`((?:scripts|docs|projects)/[^\s`]+\.(?:sh|py|js|cjs|md|json|txt|pdf|yml))`")

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

# Una ruta que el texto declara PROPUESTA no es una promesa de que existe. El
# caso testigo: docs/pipeline/roadmap-ingresos-a11y-2026-11.md dice "Script
# propuesto `scripts/watch-devto-trends.sh` (a crear)" y el gate lo marcaba roto,
# bloqueando commits que no tenian nada que ver. Un roadmap que no puede nombrar
# lo que todavia no existe no puede planear. Se mira la misma linea, solo la
# vecindad inmediata del backtick: "propuesto" tres parrafos arriba no aplica.
PROPOSED = (
    "propuesto", "propuesta", "a crear", "por crear", "todavia no existe",
    "aun no existe", "planned", "to be created", "does not exist yet",
)


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

# Historia congelada: se lee como se escribio, no se corrige. `docs/records/`
# reemplaza a los viejos `docs/conversations/` y `docs/history/` (ADR-084),
# que eran dos casas para el mismo genero. `docs/archives/` ya no existe
# (rename a `docs/history/` el 2026-09-28, luego consolidado en `docs/records/`).
# `docs/archive/` (2026-10-06) guarda bloques rotados de documentos vivos
# (CHANGELOG, etc.); su texto cita rutas de la epoca - p.ej. un ADR que luego
# se renombro - y no se reescribe. Misma politica que records/: la historia
# congelada no es una promesa sobre el arbol actual.
# `docs/CHANGELOG.md` (movido a docs/ el 2026-10-14) es el ACTIVO, no archivo:
# su texto tambien cita rutas de la epoca y esta en rotacion permanente, asi que
# se le da el mismo trato que al bloque rotado (no es una promesa sobre el arbol).
SKIP_FILES = ("docs/CHANGELOG.md",)
SKIP_DIRS = ("docs/records/", "docs/archive/", "docs/archives/", "docs/insights/")


# Proyectos archivados: el 2026-10-29 se borro el local de 18 proyectos con copia
# verificada en GitHub (limpieza de projects/ 21 -> 3). Los docs que los citaban
# quedaron apuntando a rutas que ya no existen, y este guard no las veia porque su
# regex solo cubria scripts/ y docs/. Al ampliarlo a projects/, salieron 21.
#
# La regla NO es "toda ruta a projects/ esta bien": es la misma que ya rige para
# docs/archive y docs/records. Un doc que cita un proyecto ARCHIVADO esta citando
# historia, no prometiendo que ese arbol exista. Un doc que cita un proyecto VIVO
# y yerra la ruta sigue siendo un roto, y se reporta. `projects/<slug>/` existente
# se verifica igual que cualquier otro path.
def is_archived_project_ref(ref: str) -> bool:
    """True si la ref apunta a un proyecto que ya no vive en el arbol."""
    if not ref.startswith("projects/"):
        return False
    slug = ref.split("/", 1)[1].split("/", 1)[0] if "/" in ref else ""
    return bool(slug) and not (ROOT / "projects" / slug).exists()


_PROPOSED_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(w) for w in PROPOSED) + r")\b"
)


def matches_proposed(window: str) -> bool:
    """Whole-word match on purpose. Substring matching hid a real bug once:
    'propuesto' is a prefix of nothing harmless, but 'a crear' inside
    'hay que a crear' style text would silently whitelist a dead path. The
    negative run in tests/python pins it."""
    return bool(_PROPOSED_RE.search(window))


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
    archived = 0

    for path in files:
        if not path.exists():
            continue
        rel_str = str(path.relative_to(ROOT))
        if rel_str in SKIP_FILES:
            continue
        if any(rel_str.startswith(d) for d in SKIP_DIRS):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        prev_line = ""
        for line_no, line in enumerate(text.splitlines(), 1):
            for ref in REF.findall(line):
                if is_skippable(ref):
                    continue
                if is_archived_project_ref(ref):
                    # Cita a un proyecto archivado: es historia, no una promesa.
                    # Se cuenta aparte para que el numero siga siendo honesto.
                    archived += 1
                    continue
                checked += 1
                if not (ROOT / ref).exists():
                    # La declaracion de "propuesto" puede estar en la misma linea o
                    # en la anterior, como mucho: un roadmap largo no gana licencia
                    # para citar rutas muertas por tener la palabra lejos.
                    window = (line + " " + (prev_line or "")).lower()
                    if matches_proposed(window):
                        continue
                    broken.append((path.relative_to(ROOT), line_no, ref))
            prev_line = line
            for target in LINK.findall(line):
                if is_link_skippable(target):
                    continue
                checked += 1
                if not resolves(path, target):
                    broken.append((path.relative_to(ROOT), line_no, target))

    # Cero refs revisadas no es verde: los archivos no se encontraron (rename,
    # checkout parcial, cwd equivocado) y el check no leyó nada. Regla 1 de
    # skills/verification-gates. Cazado al promover el gate de honestidad.
    if checked == 0:
        print(f"ERROR no se revisó ninguna ruta en {len(files)} archivo(s) candidato(s); "
              f"no se pudo correr (exit 3)", file=sys.stderr)
        return 3

    if broken:
        print(f"RUTAS ROTAS ({len(broken)} de {checked} revisadas):")
        for f, ln, ref in broken:
            print(f"  {f}:{ln}  ->  {ref}")
        print()
        print("Cada ruta citada deberia existir, o no se cita.")
        return 1

    if archived:
        # Se informa para que el numero sea auditable: si sube, es que mas docs
        # empezaron a citar proyectos que ya no estan.
        print(f"{archived} refs a proyectos archivados (historia, no se verifican).")
        print()

    print(f"OK: {checked} rutas citadas, todas existen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
