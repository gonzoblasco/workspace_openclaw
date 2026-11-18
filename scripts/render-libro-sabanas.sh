#!/usr/bin/env bash
# Renderiza todos los capítulos de Las Tres Sabanas con la voz oficial (ADR-115).
# Kokoro em_alex, defaults del script. Registra duración y cola de cada uno.

set -uo pipefail
cd /Users/gonzoblasco/.openclaw/workspace

SRC=docs/stories/las_tres_sabanas/manuscript
OUT=docs/stories/las_tres_sabanas/audio
LOG=/tmp/render-libro.log
PY=.venvs/kokoro/bin/python

mkdir -p "$OUT"
: > "$LOG"

for n in $(seq 2 17); do
  f="$SRC/capitulo_$n.md"
  o="$OUT/capitulo-$n-kokoro.m4a"
  echo "=== capítulo $n ===" >> "$LOG"
  t0=$(date +%s)
  if "$PY" scripts/tts-kokoro.py "$f" --out "$o" >> "$LOG" 2>&1; then
    t1=$(date +%s)
    dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$o")
    words=$(wc -w < "$f" | tr -d ' ')
    echo "OK cap $n · ${words} palabras · ${dur}s audio · $((t1-t0))s render" >> "$LOG"
  else
    echo "FALLO cap $n" >> "$LOG"
  fi
done

echo "=== RESUMEN ===" >> "$LOG"
for n in $(seq 1 17); do
  o="$OUT/capitulo-$n-kokoro.m4a"
  if [ -f "$o" ]; then
    d=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$o")
    printf "cap %2d  %7.1fs  %s\n" "$n" "$d" "$(du -h "$o" | cut -f1)" >> "$LOG"
  else
    printf "cap %2d  FALTA\n" "$n" >> "$LOG"
  fi
done
echo "FIN" >> "$LOG"
