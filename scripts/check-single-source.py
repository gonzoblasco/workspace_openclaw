#!/usr/bin/env python3
"""
check-single-source.py - Un dato, un dueno. Detecta la segunda copia.

POR QUE EXISTE (2026-10-20). Gonzo: "necesitamos definir una unica fuente de la
verdad y no tantos md que pueden chocarse y lo hacen a diario". El diagnostico
real no era "hay muchos markdown": era que ningun archivo tenia dueno de un
dato, y los gates existentes verificaban que las RUTAS citadas existieran, no
que las AFIRMACIONES fueran unicas. Resultado: cinco contradicciones vivas el
mismo dia.

Caso testigo, medido antes de escribir este gate:
  - `docs/SETUP.md` declaraba "Kanam en thinking max; agentes A/B en high" y a
    la vez "SUPERSEDED por ADR-090". Dos afirmaciones incompatibles en el mismo
    bloque de un archivo que se lee como referencia de entorno.
  - `AGENTS.md` citaba `knowledge-management`, `incremental-implementation`,
    `background-execution` y `a11y-at-validation` como skills "mas usadas".
    Ninguna de las cuatro existia en ningun arbol (ni `skills/` ni
    `agents/*/skills/`). check-refs no las veia porque no eran rutas.
  - `MEMORY.md` repetia iconos, pagos, pre-commit y validacion UI, que ya vivian
    en `AGENTS.md`. Dos copias = drift garantizado.
  - `SKILLS-INDEX.md` listaba 70+ skills retiradas; decia "(27)" y el arbol
    tenia 27, pero las secciones de rol arrastraban fantasmas.

Que verifica (dos clases, ambas baratas):
  1. REPETICION LITERAL - una linea normativa (>= MIN_CHARS) que aparece en dos
     archivos normativos con similitud >= THRESHOLD es una segunda copia. Se
     permite solo lo declarado en ALLOW (pares archivo-archivo o regex).
  2. MODELO FUERA DE CASA - los tags de modelo se declaran en `memory.db` y se
     propagan a los bloques MANAGED. Un tag de modelo escrito a mano en un
     archivo normativo es una copia que el propagador no puede corregir.
     Dueno: AGENTS.md y docs/SETUP.md, y solo entre marcadores MANAGED.

Salida: exit 0 si no hay segundas copias, 1 si las hay.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Archivos normativos: los que definen conducta, entorno o estado vigente.
# La historia congelada (dailies, records, archive) queda FUERA a proposito:
# se lee como se escribio y no es una promesa sobre el arbol de hoy.
NORMATIVE = [
    "AGENTS.md",
    "USER.md",
    "MEMORY.md",
    "SOUL.md",
    "IDENTITY.md",
    "docs/AGENTS-DETALLE.md",
    "docs/SETUP.md",
    "docs/NORTH.md",
    "docs/ROADMAP.md",
    # El perfil y los hechos de carrera entraron al alcance el 2026-10-20: al
    # medirlos se encontro que MEMORY.md y user-profile.md tenian 13 reglas
    # identicas. Un dueno fuera del gate es un dueno que nadie verifica.
    "memory/career-facts.md",
    "memory/user-profile.md",
]

# Duplicaciones legitimas: el mismo texto en dos lugares por una razon escrita.
ALLOW = [
    # El detalle ampliado cita el titulo de la regla para enlazarla. El titulo
    # es el nombre, no la regla: repetirlo es como repetir un nombre de archivo.
    (r"^#{2,3} ", r"^#{2,3} "),
]

MIN_CHARS = 60          # debajo de esto, una linea es un rotulo, no una regla
THRESHOLD = 0.55        # jaccard de tokens

# Tag de modelo: `nombre:cloud`, `nombre:120b-cloud`, `gemma4:e4b-mlx`, etc.
MODEL_TAG = re.compile(r"`([a-z][a-z0-9.\-]*:(?:cloud|[0-9]+b[a-z0-9\-]*|latest))`")

# Donde SI puede vivir un tag de modelo.
# AGENTS.md: solo entre marcadores MANAGED (es la asignacion por agente, y la
# propaga managed-blocks.py).
# SETUP.md: es el DUENO del catalogo de modelos instalados en Ollama - que
# existe, con que dimensiones y con que capacidades. Dato distinto de la
# asignacion por rol, que es la que se propaga. Por eso queda libre.
MODEL_OWNERS = {
    "AGENTS.md": "managed",
    "docs/SETUP.md": "free",
}
# Marca explicita para una linea que cita un modelo como HISTORIA (benchmark,
# decision superada). Sin la marca, el gate la trata como copia viva.
HISTORY_MARK = "<!-- modelo: historico -->"
MODEL_FREE_FILES = (
    "docs/adr/",
    "memory/",          # historial: registro de decisiones pasadas
    "docs/CHANGELOG.md",
    "docs/archive/",
    "docs/archives/",
    "docs/records/",
    "docs/learnings/",
    "docs/ecosystem/",
    "docs/insights/",
)


def tokens(text: str):
    norm = re.sub(r"[`*_\[\]()<>|]", " ", text.lower())
    norm = re.sub(r"\s+", " ", norm)
    return set(w for w in re.findall(r"[a-z0-9áéíóúñ\-\.]{4,}", norm))


def jaccard(a, b) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def is_allowed(a: str, b: str) -> bool:
    for pa, pb in ALLOW:
        if (re.search(pa, a) and re.search(pb, b)) or (re.search(pb, a) and re.search(pa, b)):
            return True
    return False


def normative_lines(root: Path):
    """(archivo, numero de linea, texto) de las lineas con contenido normativo."""
    out = []
    for rel in NORMATIVE:
        path = root / rel
        if not path.exists():
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            s = line.strip()
            if len(s) < MIN_CHARS:
                continue
            if s.startswith(("|", "```", ">")):
                continue
            out.append((rel, n, s))
    return out


def find_duplicates(root: Path):
    lines = normative_lines(root)
    by_file = {}
    for rel, n, s in lines:
        by_file.setdefault(rel, []).append((n, s, tokens(s)))

    dups = []
    files = sorted(by_file)
    for i, fa in enumerate(files):
        for fb in files[i + 1:]:
            for na, sa, ta in by_file[fa]:
                if len(ta) < 6:
                    continue
                for nb, sb, tb in by_file[fb]:
                    if len(tb) < 6:
                        continue
                    if jaccard(ta, tb) >= THRESHOLD and not is_allowed(sa, sb):
                        dups.append((fa, na, fb, nb, jaccard(ta, tb), sa, sb))
    return dups


def managed_spans(text: str):
    """Rangos (inicio, fin) de los bloques MANAGED dentro de un archivo."""
    spans = []
    open_at = None
    for n, line in enumerate(text.splitlines(), 1):
        if "BEGIN MANAGED:" in line:
            open_at = n
        elif "END MANAGED:" in line and open_at is not None:
            spans.append((open_at, n))
            open_at = None
    return spans


def find_stray_models(root: Path):
    """Tags de modelo escritos a mano fuera de su dueno."""
    stray = []
    for rel in NORMATIVE:
        path = root / rel
        if not path.exists():
            continue
        owner = MODEL_OWNERS.get(rel)
        if owner == "free":
            continue
        text = path.read_text(encoding="utf-8")
        spans = managed_spans(text)
        for n, line in enumerate(text.splitlines(), 1):
            tags = MODEL_TAG.findall(line)
            if not tags:
                continue
            if HISTORY_MARK in line:
                continue
            inside = any(a <= n <= b for a, b in spans)
            if inside:
                continue
            stray.append((rel, n, tags))
    return stray


def main(argv=None):
    root = ROOT if argv is None else Path(argv[0])
    dups = find_duplicates(root)
    stray = find_stray_models(root)

    if not dups and not stray:
        print("OK: un dato, un dueno. Sin segundas copias en los archivos normativos.")
        return 0

    if dups:
        print(f"SEGUNDAS COPIAS ({len(dups)}):\n")
        for fa, na, fb, nb, score, sa, sb in dups:
            print(f"  [{score:.2f}] {fa}:{na}")
            print(f"         {sa[:110]}")
            print(f"         {fb}:{nb}")
            print(f"         {sb[:110]}\n")
        print("Una de las dos copias se borra y se cita el dueno (AGENTS.md, seccion 0).\n")

    if stray:
        print(f"MODELOS ESCRITOS A MANO ({len(stray)}):\n")
        for rel, n, tags in stray:
            print(f"  {rel}:{n}  {', '.join(tags)}")
        print("\nLos tags de modelo se declaran en `memory.db` y se propagan con")
        print("`scripts/managed-blocks.py apply`. A mano se desincronizan solos.")

    return 1


if __name__ == "__main__":
    sys.exit(main())
