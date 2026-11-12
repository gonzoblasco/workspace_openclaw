#!/usr/bin/env python3
"""check-session-learning-rate.py - Módulo 1 del curso AI Engineer: memoria y aprendizaje.

El curso da el diagnóstico de tres pasos para cuando un agente olvida:
  1. algo se guardó?  2. la pieza correcta se encontró?  3. entró en el contexto?

Y define "learning" como adaptación en runtime: el sistema usa lo que pasó antes
para hacerlo mejor la próxima, sin reentrenar. El cierre de sesión de este
workspace guarda (daily, HANDOFF) y comunica (HANDOFF), pero no siempre aprende:
una sesión puede cerrar sin dejar un solo learning en la DB.

Este chequeo mide eso: cuántas sesiones cerradas no dejaron aprendizaje.

Uso:
  python3 scripts/check-session-learning-rate.py            # por defecto, últimos 30 días
  python3 scripts/check-session-learning-rate.py --days 60
  python3 scripts/check-session-learning-rate.py --strict   # falla si hay sesión sin learning

Salida: tabla por día y veredicto. Exit 1 sólo con --strict y huecos.
"""
import argparse
import datetime as dt
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory", "memory.db")


def load_db():
    """La DB vive bajo el state dir de OpenClaw: se copia y se consulta la copia."""
    tmp = os.path.join(tempfile.mkdtemp(), "memory.db")
    shutil.copy(DB, tmp)
    conn = sqlite3.connect(tmp)
    return conn


def rows(conn, table, since):
    try:
        return conn.execute(
            f"select substr(created_at,1,10) d, count(*) from {table} "
            f"where substr(created_at,1,10) >= ? group by d",
            (since,),
        ).fetchall()
    except sqlite3.Error:
        return []


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-h", "--help", action="store_true")
    args = ap.parse_args()
    if args.help:
        print(__doc__)
        return 0

    since = (dt.date.today() - dt.timedelta(days=args.days)).isoformat()
    conn = load_db()
    sessions = dict(rows(conn, "daily_notes", since))
    learnings = dict(rows(conn, "learnings", since))
    conn.close()

    days = sorted(set(sessions) | set(learnings))
    gaps = 0
    print(f"{'día':12} {'cierres':>8} {'learnings':>10}  estado")
    print("-" * 46)
    for d in days:
        s, l = sessions.get(d, 0), learnings.get(d, 0)
        if s and not l:
            gaps += 1
            state = "HUECO: cerró sin learning"
        elif s and l:
            state = "ok"
        else:
            state = "(solo learnings)"
        print(f"{d:12} {s:8} {l:10}  {state}")
    print("-" * 46)
    total_s, total_l = sum(sessions.values()), sum(learnings.values())
    print(f"{'TOTAL':12} {total_s:8} {total_l:10}")
    if gaps:
        print(f"\n{gaps} día(s) con cierre de sesión y cero learnings.")
        print("Diagnóstico de 3 pasos: ¿no se guardó (nadie lo escribió) o no se encontró")
        print("(se escribió y no se recupera)? El paso 3 queda fuera de este chequeo.")
    else:
        print("\nSin huecos: toda sesión cerrada dejó al menos un learning.")
    return 1 if (args.strict and gaps) else 0


if __name__ == "__main__":
    sys.exit(main())
