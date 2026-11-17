#!/usr/bin/env bash
# Watcher semanal de dev.to -> memory/devto/YYYY-Www.md
#
# Diseno: docs/pipeline/roadmap-ingresos-a11y-2026-11.md §3
#
# MEDIDO EL 2026-11-16 CONTRA LA API REAL (no cambiar sin volver a medir):
#   - `&top=N` NO sirve como filtro: recorta la respuesta a 1 item.
#   - Dos llamadas seguidas a /api/articles/latest dan 429.
#   - `?tag=X&per_page=10` con 6s de pausa entre tags: 200 en todos.
# De ahi: per_page=10 sin top, y 6 segundos ENTRE tags (no antes del primero).
#
# REGLA DEL DIGEST: no es una lista de links. Cada item entra con status
# `pendiente` y un campo `cambio` vacio que CORE/MIND completa con "que
# hariamos distinto". Un item sin `cambio` no se publica.

set -uo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
OUT_DIR="$WORKSPACE/memory/devto"
PER_PAGE=10
PAUSE=6
RETRIES=3

TAGS=(accessibility frontend react typescript webdev ai agents llm career discuss opensource)

YEAR=$(date -u +%G)
WEEK=$(date -u +%V)
OUTFILE="$OUT_DIR/${YEAR}-W${WEEK}.md"
mkdir -p "$OUT_DIR"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
FAILURES="$TMP/_failures.txt"
: > "$FAILURES"

first=1
for tag in "${TAGS[@]}"; do
  # La pausa va ENTRE requests. Dormir antes de la primera es tiempo regalado.
  if [ "$first" -eq 0 ]; then
    sleep "$PAUSE"
  fi
  first=0

  code="000"
  attempt=0
  while [ "$attempt" -lt "$RETRIES" ]; do
    attempt=$((attempt + 1))
    code=$(curl -sS -m 25 -o "$TMP/${tag}.json" -w '%{http_code}' \
      "https://dev.to/api/articles?tag=${tag}&per_page=${PER_PAGE}" 2>/dev/null) || code="000"
    [ "$code" = "200" ] && break
    sleep $((PAUSE * attempt))
  done

  if [ "$code" != "200" ]; then
    printf '%s:%s\n' "$tag" "$code" >> "$FAILURES"
    rm -f "$TMP/${tag}.json"
  fi
done

python3 - "$TMP" "$OUTFILE" <<'PY'
import collections
import datetime
import json
import os
import sys

tmp, outfile = sys.argv[1], sys.argv[2]

NICHE = {
    "accessibility": "a11y",
    "frontend": "fullstack",
    "react": "fullstack",
    "typescript": "fullstack",
    "webdev": "fullstack",
    "ai": "agentic",
    "agents": "agentic",
    "llm": "agentic",
    "career": "mercado",
    "discuss": "mercado",
    "opensource": "mercado",
}
ORDER = ["a11y", "fullstack", "agentic", "mercado"]
CAP = 3  # cupo por nicho ANTES de rankear: si no, `accessibility` se ahoga

# Solo lo que se publico en los ultimos N dias. El endpoint ?tag= devuelve
# articulos viejos cuando no hay volumen (un post de 2024 llego a colarse), y
# un digest de tendencias con material de hace dos anos no es un digest.
MAX_AGE_DAYS = 90
cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=MAX_AGE_DAYS)

items = {}
niche_of = {}

for tag, niche in NICHE.items():
    path = os.path.join(tmp, tag + ".json")
    if not os.path.exists(path):
        continue
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        continue
    if not isinstance(data, list):
        continue
    for art in data:
        url = (art.get("url") or "").strip()
        if not url or url in items:
            continue

        published = (art.get("published_at") or "").strip()
        try:
            pdt = datetime.datetime.fromisoformat(published.replace("Z", "+00:00"))
        except Exception:
            continue
        if pdt < cutoff:
            continue

        desc = " ".join((art.get("description") or "").split())
        items[url] = {
            "title": (art.get("title") or "").strip() or "(sin titulo)",
            "what": desc[:220],
            "url": url,
            "reactions": int(art.get("public_reactions_count") or 0),
            "comments": int(art.get("comments_count") or 0),
            "published": pdt.strftime("%Y-%m-%d"),
            "tags": art.get("tag_list") or [],
        }
        niche_of[url] = niche

if not items:
    sys.stderr.write("sin items: la API no devolvio nada usable\n")
    sys.exit(1)

grouped = collections.defaultdict(list)
for url, item in items.items():
    grouped[niche_of[url]].append(item)

chosen = {}
for niche in ORDER:
    ranked = sorted(
        grouped.get(niche, []),
        key=lambda x: (-x["reactions"], -x["comments"]),
    )
    chosen[niche] = ranked[:CAP]

failures = []
fail_path = os.path.join(tmp, "_failures.txt")
if os.path.exists(fail_path):
    failures = [l.strip() for l in open(fail_path, encoding="utf-8") if l.strip()]

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
total = sum(len(v) for v in chosen.values())

lines = []
lines.append("# dev.to - semana %s" % os.path.basename(outfile).replace(".md", ""))
lines.append("")
lines.append("Generado: %s" % now)
lines.append("")
lines.append(
    "%d items de %d descargados (ultimos %d dias). Cupo %d por nicho antes de rankear "
    "(dentro del nicho: reacciones, despues comentarios)."
    % (total, len(items), MAX_AGE_DAYS, CAP)
)
lines.append("")
lines.append("Tags consultados: %s" % ", ".join(sorted(NICHE)))
if failures:
    lines.append("")
    lines.append("Tags que fallaron: %s" % ", ".join(failures))
lines.append("")
lines.append(
    "Cada item entra en `status: pendiente`. Antes de publicarse, CORE/MIND "
    "completa `cambio:` con que hariamos distinto y `verified_against:` con la "
    "fuente primaria. Sin esos dos campos, el item no sale de aca."
)
lines.append("")

for niche in ORDER:
    rows = chosen.get(niche, [])
    lines.append("## %s (%d)" % (niche, len(rows)))
    lines.append("")
    if not rows:
        lines.append("Sin items esta semana.")
        lines.append("")
        continue
    for it in rows:
        lines.append("- **%s**" % it["title"])
        if it["what"]:
            lines.append("  - que dice: %s" % it["what"])
        lines.append(
            "  - senal: %d reacciones, %d comentarios, %s"
            % (it["reactions"], it["comments"], it["published"] or "sin fecha")
        )
        lines.append("  - source: %s" % it["url"])
        if it["tags"]:
            lines.append("  - tags: %s" % ", ".join(it["tags"]))
        lines.append("  - category: %s" % niche)
        lines.append("  - status: pendiente")
        lines.append("  - verified_against: pendiente")
        lines.append("  - cambio: (a completar por CORE)")
        lines.append("")

with open(outfile, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

print("por nicho: " + ", ".join("%s=%d" % (n, len(chosen.get(n, []))) for n in ORDER))
print("items unicos: %d" % len(items))
if failures:
    print("fallidos: " + ", ".join(failures))
print("escrito: %s (%d bytes)" % (outfile, os.path.getsize(outfile)))
PY
