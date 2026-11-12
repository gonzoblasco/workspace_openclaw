#!/usr/bin/env python3
import sqlite3, sys
db = sqlite3.connect('m0_workers.db')
rows = db.execute("SELECT name, SUM(stipend) AS t FROM workers GROUP BY name ORDER BY t DESC").fetchall()
print(f"{'name':8} {'total':>6}")
for name, total in rows:
    print(f"{name:8} {total:6}")
zero = db.execute("SELECT name, month FROM workers WHERE stipend = 0").fetchall()
if zero:
    print(f"FAIL: estipendio 0 en {zero}", file=sys.stderr)
    sys.exit(1)
print("OK")
