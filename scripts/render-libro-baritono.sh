#!/usr/bin/env bash
# Renderiza el audiolibro con la voz definitiva (ADR-116): Chatterbox clonando la referencia
# barítona de 100 Hz. Corta por párrafo, recorta la cola y filtra las notas de producción.
#
# Es lento (~5,5x el tiempo real): el libro entero son ~13 horas. Corre desatendido y deja
# un log con la duración de cada capítulo.

set -uo pipefail
cd /Users/gonzoblasco/.openclaw/workspace

SRC=docs/stories/las_tres_sabanas/manuscript
OUT=docs/stories/las_tres_sabanas/audio
LOG=/tmp/render-baritono.log
PY=.venvs/chatterbox/bin/python
REF="$OUT/voz/referencia-baritono-4st.wav"

mkdir -p "$OUT"
: > "$LOG"

# capítulo 1 usa el archivo definitivo; 2..17 son capitulo_N.md
for n in $(seq 1 17); do
  if [ "$n" = "1" ]; then f="$SRC/capitulo_1-definitivo.md"; else f="$SRC/capitulo_$n.md"; fi
  o="$OUT/capitulo-$n-baritono.m4a"
  echo "=== capítulo $n ($(date +%H:%M)) ===" >> "$LOG"
  t0=$(date +%s)
  if "$PY" scripts/tts-chatterbox.py "$f" --out "$o" --ref "$REF" >> "$LOG" 2>&1; then
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
  o="$OUT/capitulo-$n-baritono.m4a"
  if [ -f "$o" ]; then
    d=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$o")
    printf "cap %2d  %7.1fs  %s\n" "$n" "$d" "$(du -h "$o" | cut -f1)" >> "$LOG"
  else
    printf "cap %2d  FALTA\n" "$n" >> "$LOG"
  fi
done
echo "FIN" >> "$LOG"
