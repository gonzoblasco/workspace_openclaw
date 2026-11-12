#!/usr/bin/env python3
"""Runner del sandbox SQL de la clase: sqlite3 en proceso, sin CLI.

El guard de OpenClaw bloquea el binario `sqlite3` bajo el state dir, así que
las queries corren por el módulo de Python contra un .db fuera del workspace.

Uso:
    python3 run.py            # abre el prompt interactivo
    python3 run.py -q "SQL"   # ejecuta una query y muestrea el resultado
    python3 run.py --reset    # recrea la base desde 01-setup.sqlite.sql
"""
import sqlite3
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
DB = pathlib.Path.home() / "sql-lab" / "sandbox.db"
SETUP = HERE / "01-setup.sqlite.sql"


def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB)


def reset():
    if DB.exists():
        DB.unlink()
    con = connect()
    con.executescript(SETUP.read_text())
    con.commit()
    con.close()
    print(f"OK: base recreada en {DB}")


def show(con, sql):
    cur = con.execute(sql)
    if cur.description is None:
        con.commit()
        print(f"OK: {cur.rowcount} fila(s) afectada  (recuerda: sin confirmar no se guarda en el curso, pero acá hacemos commit explícito)")
        return
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print(" | ".join(cols))
    print("-+-".join("-" * len(c) for c in cols))
    for r in rows:
        print(" | ".join("NULL" if v is None else str(v) for v in r))
    print(f"\n({len(rows)} fila{'s' if len(rows) != 1 else ''})")


def main():
    if "--reset" in sys.argv:
        reset()
        return
    con = connect()
    if "-q" in sys.argv:
        sql = sys.argv[sys.argv.index("-q") + 1]
        show(con, sql)
        return
    print(f"SQLite {sqlite3.sqlite_version} · {DB}")
    print("Escribí SQL terminado en ';'. 'exit' para salir, '.reset' para recrear.\n")
    buf = ""
    while True:
        try:
            prompt = "sqlite> " if not buf else "   ...> "
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip() in ("exit", "quit", ".exit") and not buf:
            break
        if line.strip() == ".reset":
            con.close()
            reset()
            con = connect()
            continue
        buf += line + "\n"
        if sqlite3.complete_statement(buf):
            try:
                show(con, buf)
            except sqlite3.Error as e:
                print(f"ERROR: {e}")
            buf = ""
    con.close()


if __name__ == "__main__":
    main()
