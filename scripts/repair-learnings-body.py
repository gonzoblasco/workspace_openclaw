#!/usr/bin/env python3
"""
repair-learnings-body.py - Devuelve el cuerpo a su columna.

Causa (medida el 2026-10-27): la tabla `learnings` tiene el cuerpo de la leccion
en `content`, pero hay filas donde el cuerpo quedo en `title` (C2) o en `tags`
(C1). El export lee el cuerpo de `content`, asi que esas lecciones se
renderizaban como seccion sin cuerpo.

Este script mueve el cuerpo de vuelta, deriva un titulo corto cuando hace
falta, y NO toca lo que no puede recuperar. Es idempotente: correrlo dos
veces no cambia nada la segunda vez.

Se corre sobre una COPIA primero (--db) y recien despues sobre la real.
"""
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = sys.argv[sys.argv.index("--db") + 1] if "--db" in sys.argv else str(ROOT / "memory" / "memory.db")
DRY = "--dry" in sys.argv

VALID_TAG = re.compile(r"^[a-z0-9._-]+$")


def derive_title(body, fallback):
    """Primer parrafo o primera frase del cuerpo, como titulo."""
    text = (body or "").strip()
    if not text:
        return fallback
    # Preferir una linea que parezca un encabezado.
    for line in text.split("\n"):
        line = line.strip().lstrip("#").strip()
        if 15 < len(line) < 150:
            return line
    # Si no, primera frase.
    m = re.match(r"^(.{20,150}?[.!?])\s", text)
    if m:
        return m.group(1).strip()
    return text[:120].strip()


def main():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    cambios = []

    # --- C1: el cuerpo esta en `tags` -------------------------------------
    for lid, cat, title, content, tags in cur.execute(
        "SELECT id, category, title, content, tags FROM learnings "
        "WHERE length(trim(content)) = 0 AND length(trim(tags)) >= 40"
    ).fetchall():
        cuerpo = tags.strip()
        tags_reales = ",".join(
            t.strip() for t in tags.split(",") if t.strip() and VALID_TAG.match(t.strip())
        )
        titulo = title.strip() or derive_title(cuerpo, "sin titulo")
        cambios.append(("C1", lid, cat, "cuerpo movido de tags a content"))
        if not DRY:
            cur.execute(
                "UPDATE learnings SET content=?, tags=?, updated_at=datetime('now') WHERE id=?",
                (cuerpo, tags_reales, lid),
            )

    # --- C2: el cuerpo esta en `title` -------------------------------------
    for lid, cat, title, content in cur.execute(
        "SELECT id, category, title, content FROM learnings "
        "WHERE length(trim(content)) = 0 AND length(trim(title)) >= 40"
    ).fetchall():
        cuerpo = title.strip()
        titulo = derive_title(cuerpo, "sin titulo")
        cambios.append(("C2", lid, cat, "cuerpo movido de title a content"))
        if not DRY:
            cur.execute(
                "UPDATE learnings SET content=?, title=?, updated_at=datetime('now') WHERE id=?",
                (cuerpo, titulo, lid),
            )

    if not DRY:
        conn.commit()

    print("Reparaciones (%s%s): %d" % ("DRY" if DRY else "aplicado", "" if DRY else " -> " + DB, len(cambios)))
    for clase, lid, cat, msg in cambios:
        print("  %-3s id=%-4s %-14s %s" % (clase, lid, cat, msg))

    # Verificacion: quedan filas con content vacio?
    vacias = cur.execute(
        "SELECT id, title, length(trim(tags)) FROM learnings WHERE length(trim(content)) = 0"
    ).fetchall()
    if vacias:
        print("\nSin content y sin cuerpo recuperable (%d filas) - se aceptan como deuda:" % len(vacias))
        for lid, title, tlen in vacias:
            print("  id=%-4s title=%r tags_len=%s" % (lid, title[:60], tlen))

    conn.close()


if __name__ == "__main__":
    main()
