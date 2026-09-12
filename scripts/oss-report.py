#!/usr/bin/env python3
# oss-report.py - Genera el JSON de report nativo del dashboard de contribuciones OSS.
# Lee memory.db (contributions + oss_sync) y emite un report compatible con session:report
# (limites: 24 bloques, 8 columnas, 40 filas por tabla, 20 links, 8KB total).
# Uso: python3 scripts/oss-report.py [--json]

import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "memory", "memory.db")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# ---- Dedupe por (repo, pr, tipo): si un ticket tiene registro pr + otro collab del mismo PR,
# nos quedamos con la fila pr (la accionable) y descartamos la collab duplicada del mismo PR -------
rows = conn.execute(
    "SELECT id, repo, COALESCE(pr,'-') AS pr, tipo, status, COALESCE(pr_url,'') AS pr_url "
    "FROM contributions ORDER BY id"
).fetchall()

def norm_pr(p):
    # Normaliza el número de PR: "#10554" y "10554" son el mismo ticket.
    return p.lstrip('#').strip() if p and p != '-' else '-'

best = {}
for r in rows:
    key = (r["repo"].lower(), norm_pr(r["pr"]), r["tipo"])
    if key not in best or r["id"] > best[key]["id"]:
        best[key] = {"id": r["id"], "repo": r["repo"], "pr": r["pr"],
                     "tipo": r["tipo"], "status": r["status"], "pr_url": r["pr_url"]}

items = sorted(best.values(), key=lambda x: (x["repo"].lower(), norm_pr(x["pr"])))

# Una collab cuyo pr coincide con un registro pr del mismo repo+pr (normalizado) es el
# contextual del mismo ticket: la descartamos para estadisticas.
pr_keys = {(i["repo"].lower(), norm_pr(i["pr"])) for i in items if i["tipo"] == "pr"}
prs = [i for i in items if i["tipo"] == "pr" and i["pr"] != "-"]
collabs = [i for i in items if (i["tipo"] != "pr" or i["pr"] == "-") and (i["repo"].lower(), norm_pr(i["pr"])) not in pr_keys]

# ---- Conteos por estado (solo PRs) ----
counts = {}
for i in prs:
    counts[i["status"]] = counts.get(i["status"], 0) + 1

total = len(prs)
merged = counts.get("merged", 0)
closed = counts.get("closed", 0)
open_st = counts.get("open", 0)
review = counts.get("waiting_review", 0) + counts.get("active", 0) + counts.get("comment", 0) + counts.get("verified", 0)
other = total - merged - closed - open_st - counts.get("waiting_review", 0) - counts.get("active", 0) - counts.get("comment", 0) - counts.get("verified", 0)

# ---- Badge de estado en texto (columna Estado) ----
ACTIVE = {"open", "waiting_review", "active", "comment", "verified"}
def state_label(s):
    return {
        "merged": "merged", "closed": "closed", "open": "open",
        "waiting_review": "waiting review", "active": "active",
        "comment": "commented", "verified": "verified", "collab": "collab",
    }.get(s, s)

# ---- Tabla de activas (PRs en curso + collabs activas) ----
active_prs = [i for i in prs if i["status"] in ACTIVE]
active_collabs = [i for i in collabs if i["status"] in ("active", "open", "comment", "verified", "waiting_review")]
active_rows = [[i["repo"], i["pr"], state_label(i["status"]), "collab" if i in collabs else "pr"] for i in active_collabs + active_prs]
active_rows = [[c[:60] for c in row] for row in active_rows]

done_items = [i for i in prs if i["status"] in ("merged", "closed")]
done_rows = [[i["repo"], i["pr"], state_label(i["status"])] for i in done_items]

# ---- Links (activos primero, hasta 20) ----
link_items = []
for i in active_collabs + active_prs:
    if i["pr_url"] and len(link_items) < 20:
        label = f'{i["repo"].split("/")[-1]} {i["pr"]}'
        link_items.append({"label": label, "url": i["pr_url"], "detail": state_label(i["status"])})

blocks = [
    {
        "type": "metrics",
        "items": [
            {"label": "Abiertos", "value": str(open_st)},
            {"label": "En review/activos", "value": str(review)},
            {"label": "Merged", "value": str(merged)},
            {"label": "Cerrados", "value": str(closed)},
            {"label": "Otros", "value": str(other)},
            {"label": "Total PRs", "value": str(total)},
            {"label": "Colabs", "value": str(len(collabs))},
        ],
    }
]
if active_rows:
    blocks.append({
        "type": "table",
        "title": "Activas (PRs en curso + colaboraciones)",
        "columns": ["Repo", "PR", "Estado", "Tipo"],
        "rows": active_rows[:40],
    })
if done_rows:
    blocks.append({
        "type": "table",
        "title": "Finalizadas (merged/closed)",
        "columns": ["Repo", "PR", "Estado"],
        "rows": done_rows[:40],
    })
if link_items:
    blocks.append({"type": "links", "title": "Links activos", "items": link_items})

report = {"title": "Contribuciones OSS", "blocks": blocks}
out = json.dumps(report, ensure_ascii=False)

# Verificacion de limite: max 8KB
if len(out.encode("utf-8")) > 8192:
    # Reduce tablas: solo activas
    blocks = [blocks[0]]
    if active_rows:
        blocks.append({
            "type": "table",
            "title": "Activas",
            "columns": ["Repo", "PR", "Estado", "Tipo"],
            "rows": active_rows[:40],
        })
    if link_items:
        blocks.append({"type": "links", "title": "Links activos", "items": link_items[:20]})
    report = {"title": "Contribuciones OSS", "blocks": blocks}
    out = json.dumps(report, ensure_ascii=False)

if "--json" in sys.argv:
    print(out)
else:
    # Reporte humano compacto para el chat
    print(f"{total} PRs | abiertos {open_st} | en review {review} | merged {merged} | cerrados {closed} | collab {len(collabs)}")
    if active_rows:
        print("Activas:")
        for row in active_rows[:15]:
            print(f"  - {row[0]} {row[1]} [{row[2]}]")
