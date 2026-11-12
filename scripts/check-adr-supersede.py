#!/usr/bin/env python3
"""
check-adr-supersede.py - Verifica que la relacion de supersede sea consistente.

POR QUE EXISTE (2026-10-09). El corpus de ADRs acumulo "datos pisados": un ADR
declara que supersede a otro, pero el superseded queda con su estado viejo
("Aceptado") y su Decision se sigue leyendo como estado vigente. Casos testigo:
ADR-075 (su cabecera decia "Aceptado" mientras ADR-098 lo habia reemplazado) y
ADR-006 (superseded por ADR-040, con la nota escondida en un sidecar `.appendix`
que nadie lee).

Nada lo detectaba: check-adr-integrity.py reconcilia indice vs disco (que el ADR
se encuentre), no la DIRECCION de la relacion (que el superseded lo diga). Un ADR
"encontrable" pero "pisado" es peor que uno ausente: se lee como ley vigente.

REGLA. Una relacion de supersede TOTAL (declarada en el header del que reemplaza,
en un campo `Supersede` / `Revierte` / `Reemplaza` sin marca de parcialidad, o en
el estado del reemplazado) exige que el reemplazado lleve `superseded` en **su
campo de estado** - el lugar canonico (README, "Campos del header": `Estado` =
`Aceptado` / `Superseded por ADR-NNN` / `Rechazado`).

Por que el ESTADO y no un bloque en el cuerpo: el estado es lo primero que se lee.
Un aviso `> SUPERSEDED` enterrado 200 lineas abajo no evita que la cabecera mienta.
El cuerpo es secundario; la cabecera es el contrato.

Una relacion PARCIAL (un apartado, una seccion, una practica) no exige marca: no
reemplaza la decision entera (ej. ADR-053 supersede la seccion de thinking de
ADR-040, pero ADR-040 sigue gobernando la seleccion por tipo de tarea).

FUENTE DE VERDAD DE LA RELACION. Los campos de header del que REEMPLAZA
(`**Supersede:**` / `**Revierte:**` / `**Reemplaza:**`) Y ADEMAS el campo generico
`**Relacionado:**` cuando este declara un reemplazo TOTAL: es donde un decisor
dice "yo reemplazo a X", y la flecha apunta hacia afuera (al reemplazado).

  Por que tambien `Relacionado`: verificado 2026-10-12 durante la auditoria de
  solapamiento, dos reemplazos TOTALES vivian SOLO ahi y el guard no los veia -
  ADR-098 (`ADR-075 (superseded)`) y ADR-091 (`ADR-068 (... superado)`). Un campo
  generico que declara un reemplazo total es una relacion de primera clase; el
  target tiene que estar marcado igual que si el origen hubiera usado un campo
  dedicado. Solo cuenta si el contexto del ADR citado (el parentesis) trae una
  señal de reemplazo y NO una de parcialidad: `ADR-084 (... reemplaza la lista de
  directorios historicos)` y `ADR-053 (... superseded parcialmente)` son parciales
  y no exigen marca.

  El aviso en el CUERPO del ADR reemplazado (un bloque `> SUPERSEDED por ADR-N`) sigue
  sin usarse para construir el grafo: una nota en el cuerpo puede marcar un APARTADO
y no la decision entera (ADR-040 tiene su seccion de thinking superseded por ADR-053 y
sigue gobernando la seleccion por tipo de tarea). Construir el grafo desde el cuerpo
daria ese falso positivo, y ademas invertir la flecha es trivial de errar ahi
(`superseded por ADR-N` significa N supersede a este, al reves de la frase). La
fuente del header no tiene esa ambiguedad.

SEGUNDA REGLA - SIDECARS. Un archivo no-`.md` en `docs/adr/` (ej. `.appendix`) es
invisible para todo lector y todo guard: ni el indice lo lista, ni check-refs lo
escanea, ni check-adr-integrity lo ve. Si lleva contenido de un ADR (una nota de
supersede, un anexo), tiene que vivir en el ADR, no al lado.

TERCERA REGLA - SUFIJO `-archived`. El estado dice si la decision rige; el nombre
del archivo lo dice tambien, para quien mira un `ls` o un `grep` de rutas. Un ADR
cuyo estado NO es `Aceptado`/`Accepted` (`Superseded`, `ARCHIVADO`, `Rechazado`)
tiene que llamarse `ADR-NNN-slug-archived.md`. La inversa tambien: un archivo con
el sufijo y el estado `Aceptado` es una mentira en la otra direccion -quien lo ve
por nombre lo saltea, y sigue gobernando-. Un `Aceptado` con un apartado superseded
NO lleva sufijo: sigue gobernando su materia.

Uso:
    check-adr-supersede.py
Salida: exit 0 si el grafo es consistente, 1 si hay un superseded sin marcar o un sidecar.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent
ADR_DIR = ROOT / "docs" / "adr"

FILE_RE = re.compile(r"^ADR-(\d+)-.+\.md$")
ADR_CITE = re.compile(r"ADR-(\d+)")

# Sufijo que marca un ADR fuera del espacio de decision (convencion en
# docs/adr/README.md, "Nombre del archivo").
ARCHIVED_SUFFIX = "-archived"

# Estados que SI rigen. Cualquier otro (`Superseded`, `ARCHIVADO`, `Rechazado`)
# exige el sufijo en el nombre.
ACCEPTED_STATUS = re.compile(r"^\s*(aceptado|accepted)\b", re.I)

# Campos de header donde A declara superseder a otros. El valor tiene que ser
# una relacion TOTAL: si nombra un apartado/seccion/practica, es parcial.
FULL_FIELDS = ("Supersede", "Revierte", "Reemplaza")

# El campo generico `Relacionado` tambien puede declarar un reemplazo TOTAL, sin
# ser un campo dedicado (casos reales ADR-098 -> ADR-075 y ADR-091 -> ADR-068).
REL_FIELD = "Relacionado"
REL_TOTAL = re.compile(r"superad|supersed|reemplaz|replaces", re.I)

# Senal de parcialidad: si el contexto la trae, NO es reemplazo total. Cubre tanto
# los campos dedicados ("el apartado de X", "la seccion de Y") como el generico
# ("reemplaza la lista de directorios historicos", "superseded parcialmente").
PARTIAL_HINT = re.compile(
    r"parcial|apartado|seccion|practica|skill|docs/|lista|directorio|historic", re.I
)

# `ADR-NNN (contexto)` dentro de un campo generico: el parentesis es el contexto
# que decide si la relacion es total o parcial.
REL_ITEM = re.compile(r"ADR-(\d+)\s*\(([^)]*)\)")

# "superseded por ADR-N" / "supersede a ADR-N" en el estado o el cuerpo.
SUPERSEDED_BY_RE = re.compile(r"supersed(?:ed|e)\s*por\s*ADR-(\d+)", re.I)


def adr_number(p: Path):
    m = FILE_RE.match(p.name)
    return int(m.group(1)) if m else None


def declared_status(text: str) -> str:
    for pat in (r"^\*\*Estado:\*\*\s*(.+)$", r"^\*\*Status:\*\*\s*(.+)$", r"^status:\s*(.+)$"):
        m = re.search(pat, text, re.M)
        if m:
            return m.group(1).strip()
    return ""


def status_marks_superseded(text: str) -> bool:
    return bool(re.search(r"supersed", declared_status(text), re.I))


def is_accepted(text: str) -> bool:
    """True si el estado declara que la decision sigue rigiendo."""
    return bool(ACCEPTED_STATUS.match(declared_status(text)))


def has_archived_suffix(p: Path) -> bool:
    return p.stem.endswith(ARCHIVED_SUFFIX)


def _field_value(text: str, field: str):
    m = re.search(r"^\*\*" + re.escape(field) + r":\*\*\s*(.+)$", text, re.M)
    return m.group(1) if m else None


def supersedes_others(text: str) -> Set[int]:
    """Los ADRs que ESTE documento supersede (relacion total, desde el header)."""
    out: Set[int] = set()
    for field in FULL_FIELDS:
        val = _field_value(text, field)
        if val and not PARTIAL_HINT.search(val):
            out |= {int(n) for n in ADR_CITE.findall(val)}
    # El campo generico tambien puede declarar un reemplazo total (contexto del
    # parentesis sin señal de parcialidad).
    rel = _field_value(text, REL_FIELD)
    if rel:
        for m in REL_ITEM.finditer(rel):
            ctx = m.group(2)
            if REL_TOTAL.search(ctx) and not PARTIAL_HINT.search(ctx):
                out.add(int(m.group(1)))
    return out


def find_violations(adr_dir: Path = ADR_DIR) -> List[str]:
    adr_dir = Path(adr_dir)
    files: Dict[int, Path] = {}
    for p in sorted(adr_dir.glob("ADR-*.md")):
        n = adr_number(p)
        if n is not None:
            files[n] = p

    text = {n: p.read_text(encoding="utf-8") for n, p in files.items()}

    violations: List[str] = []
    for src, t in sorted(text.items()):
        for tgt in sorted(supersedes_others(t)):
            if tgt not in text:
                continue  # cita a un ADR inexistente: lo cubre check-adr-integrity
            if not status_marks_superseded(text[tgt]):
                violations.append(
                    "ADR-%03d supersede a ADR-%03d, pero el estado de ADR-%03d es "
                    "'%s': su cabecera se lee como ley vigente."
                    % (src, tgt, tgt, declared_status(text[tgt]) or "(vacio)")
                )

    # Segunda regla: sidecars invisibles.
    for p in sorted(adr_dir.iterdir()):
        if p.is_file() and p.suffix != ".md":
            violations.append(
                "sidecar invisible: %s (un archivo no-.md en docs/adr/ no lo ve "
                "ningun lector ni guard; su contenido debe vivir en el ADR)"
                % p.name
            )

    # Tercera regla: el nombre tiene que acompanar al estado.
    for n, p in sorted(files.items()):
        accepted = is_accepted(text[n])
        suffixed = has_archived_suffix(p)
        if accepted and suffixed:
            violations.append(
                "ADR-%03d: el archivo lleva el sufijo `-archived` pero su estado es "
                "'%s'. Quien lo ve por nombre lo saltea y la decision sigue rigiendo: "
                "sacar el sufijo o corregir el estado."
                % (n, declared_status(text[n]) or "(vacio)")
            )
        elif not accepted and not suffixed:
            violations.append(
                "ADR-%03d: su estado es '%s' pero el archivo no lleva el sufijo "
                "`-archived`. Renombrar con `git mv` a %s-archived.md."
                % (n, declared_status(text[n]) or "(vacio)", p.stem)
            )

    return violations


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    adr_dir = Path(argv[0]) if argv else ADR_DIR
    if not adr_dir.is_dir() or not any(adr_dir.glob('ADR-*.md')):
        print(f"ERROR no hay ADRs en {adr_dir}; no se pudo correr (exit 3)",
              file=sys.stderr)
        return 3
    violations = find_violations(adr_dir)
    if violations:
        print(f"CORPUS DE ADRs CON DATOS PISADOS ({len(violations)}):")
        for v in violations:
            print(f"  {v}")
        print()
        print("Un ADR reemplazado debe decirlo en su cabecera. Si no, el corpus tiene dos leyes.")
        return 1

    print("OK: el grafo de supersede es consistente (todo superseded esta marcado en su estado).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
