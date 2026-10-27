#!/usr/bin/env python3
"""
repair-learnings-taxonomy.py - Tags a la junction, cuerpos truncados al corpus.

Dos defectos medidos el 2026-10-27 (ver scripts/check-learnings-integrity.py):

  C4  TAGS INVISIBLES (79 filas). La columna `learnings.tags` tiene tags reales
      pero la junction `learning_tags` esta vacia, y el export lee SOLO la
      junction. Los tags no aparecen en ninguna vista. `memory-db.sh
      add-learning` escribe en la columna y nunca en la junction: todo lo
      agregado por ese comando desde la taxonomia normalizada quedo invisible.

  C5  CONTENIDO TRUNCADO (34 filas). `memory-catalog-v2.py` corta el cuerpo a
      500 caracteres al insertar (`content_text = learning.get("content","")[:500]`).
      24 de las 34 son RECUPERABLES: el texto completo sigue en
      `sessions_relacional.content_bare` o en `daily_notes.content`. Las 10
      restantes no existen en ningun lado y quedan como deuda aceptada.

Se corre sobre una COPIA primero (--db) y recien despues sobre la real.
Idempotente: correrlo dos veces no cambia nada la segunda vez.
"""
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = sys.argv[sys.argv.index("--db") + 1] if "--db" in sys.argv else str(ROOT / "memory" / "memory.db")
DRY = "--dry" in sys.argv

VALID_TAG = re.compile(r"^[a-z0-9._-]+$")
CATALOG_TRUNCATION = 500


def _secciones_de_extract_learnings(texto):
    """Reimplementa `extract_learnings` de memory-catalog-v2.py.

    No se puede inventar la segmentacion: el catalogo acumulo las lineas de
    una seccion hasta el PROXIMO encabezado `###`, y las uni con un espacio
    inicial. Si la recuperacion usa otro corte, devuelve el documento entero
    (medido: una leccion de 500 chars salia como una de 72.174).

    Devuelve {titulo: cuerpo} con el mismo formato que la tabla.
    """
    out = {}
    actual = None
    lineas = []
    for linea in texto.split("\n"):
        linea = linea.strip()
        m = re.match(r"^###\s+(.+?)\s*$", linea)
        if m:
            if actual is not None and lineas:
                out[actual] = " ".join(lineas).strip()
            actual = m.group(1)
            lineas = []
        elif actual is not None and linea:
            lineas.append(linea)
    if actual is not None and lineas:
        out[actual] = " ".join(lineas).strip()
    return out


def recuperar_cuerpo(conn, content):
    """Busca el cuerpo completo en el corpus usando un fragmento del medio.

    El prefijo no sirve: el fragmento truncado es identico al original. El
    fragmento del MEDIO (offset 200-240) es lo que distingue una fila
    truncada de una completa.
    """
    frag = content[200:240].strip()
    if len(frag) < 20:
        return None
    for tabla, col in (("sessions_relacional", "content_bare"), ("daily_notes", "content")):
        row = conn.execute(
            "SELECT %s FROM %s WHERE %s LIKE ? LIMIT 1" % (col, tabla, col),
            ("%" + frag + "%",),
        ).fetchone()
        if not row:
            continue
        texto = row[0] or ""
        if frag not in texto:
            continue
        for _titulo, cuerpo in _secciones_de_extract_learnings(texto).items():
            # La seccion que contiene el fragmento, y que es mas larga que la
            # version truncada: esa es la original.
            if frag not in cuerpo or len(cuerpo) <= len(content) + 20:
                continue
            # `extract_learnings` une las lineas con ESPACIOS, no con saltos de
            # linea: el cuerpo no tiene "\n" en ningun lado. Por eso el corte
            # busca " ## " y no "\n## ". Y corta solo en el limite de documento:
            # lo que sigue al `##` no es de la leccion. Medido: id=222 arrastraba
            # el cierre de sesion entero.
            corte = re.search(r"\s##\s", cuerpo)
            if corte:
                cuerpo = cuerpo[:corte.start()].strip()
            if len(cuerpo) > len(content) + 20:
                return cuerpo
    return None


def main():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    cambios = []

    # --- C4: poblar la junction con los tags reales de la columna ---------
    for lid, tags in cur.execute(
        "SELECT id, tags FROM learnings WHERE tags IS NOT NULL AND TRIM(tags) != ''"
    ).fetchall():
        reales = [t.strip() for t in (tags or "").split(",") if t.strip() and VALID_TAG.match(t.strip())]
        if not reales:
            continue
        junction = cur.execute(
            "SELECT group_concat(t.name, ',') FROM learning_tags lt "
            "JOIN tags t ON t.id = lt.tag_id WHERE lt.learning_id = ?",
            (lid,),
        ).fetchone()[0]
        if junction:
            continue
        cambios.append(("C4", lid, "junction: %d tag(s)" % len(reales)))
        if not DRY:
            for name in reales:
                cur.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (name,))
                cur.execute(
                    "INSERT OR IGNORE INTO learning_tags (learning_id, tag_id) "
                    "SELECT ?, id FROM tags WHERE name = ?",
                    (lid, name),
                )

    # --- C5: recuperar cuerpos truncados desde el corpus ------------------
    truncadas = cur.execute(
        "SELECT id, title, content FROM learnings WHERE length(content) = ? ORDER BY id",
        (CATALOG_TRUNCATION,),
    ).fetchall()
    for lid, title, content in truncadas:
        cuerpo = recuperar_cuerpo(conn, content)
        if not cuerpo:
            continue
        cambios.append(("C5", lid, "cuerpo recuperado: %d -> %d chars" % (len(content), len(cuerpo))))
        if not DRY:
            cur.execute(
                "UPDATE learnings SET content=?, updated_at=datetime('now') WHERE id=?",
                (cuerpo, lid),
            )

    if not DRY:
        conn.commit()

    print("Reparaciones (%s): %d" % ("DRY" if DRY else "aplicado -> " + DB, len(cambios)))
    c4 = [c for c in cambios if c[0] == "C4"]
    c5 = [c for c in cambios if c[0] == "C5"]
    print("  C4 tags a la junction: %d filas" % len(c4))
    print("  C5 cuerpos recuperados: %d filas" % len(c5))
    for clase, lid, msg in c5:
        print("    id=%-4s %s" % (lid, msg))

    # Lo que queda sin recuperar
    if not DRY:
        pend = cur.execute(
            "SELECT id, title FROM learnings WHERE length(content) = ? ORDER BY id",
            (CATALOG_TRUNCATION,),
        ).fetchall()
        if pend:
            print("\nTruncadas sin recuperar (%d) - deuda aceptada:" % len(pend))
            for lid, title in pend:
                print("  id=%-4s %s" % (lid, title[:60]))

    conn.close()


if __name__ == "__main__":
    main()
