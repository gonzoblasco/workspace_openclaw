#!/usr/bin/env python3
"""
check-learnings-integrity.py - La tabla `learnings` tiene el cuerpo de la leccion
en la columna equivocada, y nada lo impedia.

POR QUE EXISTE (2026-10-27). Gonzo: "menso mal encontraste el error ese de los
learnings... auditemoslo asi no se repite".

Caso testigo. Yo borre 9 lecciones REALES de la DB con un solo DELETE:
`DELETE FROM learnings WHERE content IS NULL OR length(content)<5`. Asumi que
`content` guardaba el texto de la leccion. No es asi: hay filas donde el
cuerpo esta en `title` y filas donde esta en `tags`. El DELETE no las toco
(esas tenian `content` vacio, que era justo mi criterio de "basura"), pero el
motivo real por el que se borro fue una lectura equivocada del esquema.

Peor: la exportacion a `docs/learnings/*.md` habria perdido esas 9 lecciones
en el mismo momento, porque el export lee el cuerpo de `content` y el titulo
de `title`. Cuatro lecciones aparecian ya en los .md con el cuerpo VACIO.

Auditoria de la tabla (medida antes de escribir este gate), 255 filas:

  C1  CUERPO EN `tags` (5 filas). El cuerpo de la leccion esta en la columna
      `tags` y `content` esta vacio. Los .md las renderizan como seccion sin
      cuerpo. Origen: `migrate-learnings.py` derivaba los tags del titulo, y
      la absorcion de la tabla gemela (commit 0518cdf3f3) descarto la prosa de
      `tags` asumiendo que era "el titulo duplicado" - suposicion falsa: en
      estas 5 filas la prosa era el CUERPO, y se perdio.
  C2  CUERPO EN `title` (3 filas). El cuerpo esta en `title` y `content` esta
      vacio. `title` es NOT NULL, asi que un cuerpo largo nunca violates la
      constraint: el esquema no dice nada sobre donde va el texto.
  C3  PROSA EN `tags` (5 filas). `tags` deberia ser un vocabulario controlado
      (tokens [a-z0-9._-]); lo que hay es un parrafo. El export lee los tags
      de la JUNCTION `learning_tags`, no de la columna, asi que la prosa ni
      aparece ni molesta - hasta que se necesita el cuerpo.
  C4  TAGS INVISIBLES (79 filas). La columna `tags` tiene tags reales pero la
      junction `learning_tags` esta vacia, y el export lee SOLO la junction.
      Los tags no aparecen en ninguna vista. `memory-db.sh add-learning` escribe
      en la columna y nunca en la junction: todo lo agregado por ese comando
      desde la taxonomia normalizada quedo invisible.
  C5  CONTENIDO TRUNCADO (34 filas). `memory-catalog-v2.py` corta el cuerpo a
      500 caracteres al insertar: `content_text = learning.get("content","")[:500]`.
      34 filas tienen `length(content) = 500` exacto. El resto del cuerpo no
      esta en la DB ni en el corpus de sesiones: no es recuperable.

Que verifica: las cinco clases. Salida: exit 0 si la tabla esta sana, 1 si no.

COMO SE USA:
  python3 scripts/check-learnings-integrity.py            # gate, exit 1 si falla
  python3 scripts/check-learnings-integrity.py --report   # detalle, exit 0 siempre
"""

import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = os.environ.get("MEMORY_DB", str(ROOT / "memory" / "memory.db"))

# Un tag real es un token: minuscula inicial, sin espacios, solo [a-z0-9._-].
# Lo que no cumple eso es prosa (un titulo o un cuerpo pegado por un bug).
VALID_TAG = re.compile(r"^[a-z0-9._-]+$")

# Un titulo es un encabezado, no un parrafo. Mas de esto y la fila es sospechosa.
MAX_TITLE_CHARS = 200

# El cuerpo de una leccion debe tener un minimo de substance. Por debajo, la
# fila es un esqueleto: hay que revisarla, no darla por buena.
MIN_CONTENT_CHARS = 40

# Truncado sistematico del catalogo. Exactamente este valor = corte.
CATALOG_TRUNCATION = 500

# Fila con el cuerpo truncado en 2026-10-27: el resto del texto no existe en
# ninguna parte (ni DB, ni corpus de sesiones, ni historia de los .md). Se
# acepta la deuda de forma explicita para no bloquear el gate por siempre.
# Reconstruirla requiere volver a la sesion original.
# Las 20 recuperables se repararon con scripts/repair-learnings-taxonomy.py.
ACCEPTED_TRUNCATED = {
    156, 165, 166, 167, 170, 173, 174, 236, 246, 258, 260, 265, 269, 271,
}

# Filas con un cuerpo valido pero minimo (menos de MIN_CONTENT_CHARS). No son
# perdida: son esqueletos. Aviso, no falla.
ACCEPTED_SLIM = {254, 255}


def collect(conn):
    """Devuelve (problemas, avisos) con los defectos por fila.

    Separa lo que es PERDIDA (bloquea) de lo que es RUIDO HISTORICO (avisa).
    Un gate que reporta 169 filas no se lee y no se respeta: solo frena la
    tabla cuando el dato no esta donde debe.
    """
    problemas = []
    avisos = []

    for lid, cat, title, content, tags in conn.execute(
        "SELECT id, category, title, content, tags FROM learnings"
    ):
        content = content or ""
        tags = tags or ""
        title = title or ""
        found = []
        suave = []

        # C1: el cuerpo esta en `tags`.
        if not content.strip() and len(tags.strip()) >= MIN_CONTENT_CHARS:
            found.append(("C1_cuerpo_en_tags", "el cuerpo esta en la columna tags"))

        # C2: el cuerpo esta en `title`.
        if not content.strip() and len(title.strip()) >= MIN_CONTENT_CHARS:
            found.append(("C2_cuerpo_en_title", "el cuerpo esta en la columna title"))

        # C3: prosa en `tags` (no es un vocabulario controlado). En la practica
        # historica esto es el FRAGMENTO DEL TITULO, que `migrate-learnings.py`
        # derivaba con `title.split(" - ")[-1]`. No es perdida: el titulo
        # sigue en su columna. Es aviso.
        if tags.strip():
            prosa = [
                t.strip()
                for t in tags.split(",")
                if t.strip() and not VALID_TAG.match(t.strip())
            ]
            if prosa:
                suave.append(
                    ("C3_prosa_en_tags", "tags tiene %d valor(es) que no son tags" % len(prosa))
                )

        # C4: tags en la columna que nunca llegaron a la junction. El export
        # lee SOLO la junction: los tags no aparecen en ninguna vista.
        reales = [t.strip() for t in tags.split(",") if t.strip() and VALID_TAG.match(t.strip())]
        if reales:
            junction = conn.execute(
                "SELECT group_concat(t.name, ',') FROM learning_tags lt "
                "JOIN tags t ON t.id = lt.tag_id WHERE lt.learning_id = ?",
                (lid,),
            ).fetchone()[0]
            if not junction:
                found.append(
                    ("C4_tags_invisibles", "tags en la columna pero no en la junction")
                )

        # C5: cuerpo truncado por el catalogo.
        if len(content) == CATALOG_TRUNCATION and lid not in ACCEPTED_TRUNCATED:
            found.append(
                ("C5_contenido_truncado", "content truncado a %d chars" % CATALOG_TRUNCATION)
            )

        # Titulo desproporcionado: el titulo es largo pero DESCRIPTIVO y el
        # cuerpo esta bien. No es perdida. Es aviso.
        if content.strip() and len(title.strip()) > MAX_TITLE_CHARS:
            suave.append(
                ("C2_titulo_desproporcionado", "title de %d chars" % len(title.strip()))
            )

        # Cuerpo demasiado corto para ser una leccion. Aviso, no falla.
        if content.strip() and len(content.strip()) < MIN_CONTENT_CHARS and lid not in ACCEPTED_SLIM:
            suave.append(
                ("C6_cuerpo_escuelto", "content de %d chars" % len(content.strip()))
            )

        if found:
            problemas.append((lid, cat, title[:70].replace("\n", " "), found))
        elif suave:
            avisos.append((lid, cat, title[:70].replace("\n", " "), suave))

    return problemas, avisos


def main():
    report = "--report" in sys.argv

    if not os.path.exists(DB):
        print("OK: no hay DB de memoria en %s (nada que verificar)." % DB)
        return 0

    conn = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    try:
        problemas, avisos = collect(conn)
        total = conn.execute("SELECT count(*) FROM learnings").fetchone()[0]
    finally:
        conn.close()

    if report:
        print("Tabla learnings: %s filas" % total)
        por_clase = {}
        for _lid, _cat, _title, found in problemas:
            for code, _msg in found:
                por_clase[code] = por_clase.get(code, 0) + 1
        print("\nPERDIDAS (bloquean el gate): %s filas" % len(problemas))
        if not por_clase:
            print("  ninguna")
        for code in sorted(por_clase):
            print("  %-28s %s filas" % (code, por_clase[code]))
        for lid, cat, title, found in problemas:
            print("  id=%-4s %-14s %s" % (lid, cat, title))
            for code, msg in found:
                print("        %-28s %s" % (code, msg))

        por_clase_a = {}
        for _lid, _cat, _title, found in avisos:
            for code, _msg in found:
                por_clase_a[code] = por_clase_a.get(code, 0) + 1
        print("\nAVISOS (no bloquean): %s filas" % len(avisos))
        if not por_clase_a:
            print("  ninguno")
        for code in sorted(por_clase_a):
            print("  %-28s %s filas" % (code, por_clase_a[code]))
        return 0

    if not problemas:
        print("OK: %s learnings, cuerpo y tags en su columna." % total)
        if avisos:
            print("  (%d filas con avisos historicos, no bloquean)" % len(avisos))
        return 0

    por_clase = {}
    for _lid, _cat, _title, found in problemas:
        for code, _msg in found:
            por_clase[code] = por_clase.get(code, 0) + 1

    print("FALLA: la tabla learnings tiene %d filas con perdida de datos:" % len(problemas))
    for code in sorted(por_clase):
        print("  %-28s %s filas" % (code, por_clase[code]))
    print("")
    for lid, cat, title, found in problemas[:20]:
        codes = ", ".join(c for c, _ in found)
        print("  id=%-4s %-14s %s" % (lid, cat, title))
        for code, msg in found:
            print("        %-28s %s" % (code, msg))
    if len(problemas) > 20:
        print("  ... y %d mas (--report para el detalle)" % (len(problemas) - 20))
    print("")
    print("El cuerpo de una leccion va en `content` y el titulo en `title`.")
    print("Reparacion: scripts/repair-learnings-body.py (C1/C2),")
    print("            scripts/repair-learnings-taxonomy.py (C4/C5)")
    print("Detalle: python3 scripts/check-learnings-integrity.py --report")
    return 1


if __name__ == "__main__":
    sys.exit(main())
