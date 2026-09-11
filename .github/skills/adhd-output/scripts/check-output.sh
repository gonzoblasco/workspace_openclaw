#!/usr/bin/env bash
# check-output.sh - Lint heuristico de formato ADHD-friendly
#
# Uso:
#   check-output.sh <archivo>
#   echo "texto" | check-output.sh
#
# Salida: lista de violaciones por regla, o "OK" si pasa.
# Exit 0 = sin violaciones, 1 = hay violaciones.

set -uo pipefail

if [ $# -ge 1 ] && [ -f "$1" ]; then
  INPUT=$(cat "$1")
else
  INPUT=$(cat)
fi

if [ -z "${INPUT// }" ]; then
  echo "ERROR: sin input. Uso: check-output.sh <archivo> o echo \"texto\" | check-output.sh"
  exit 2
fi

VIOLATIONS=0
report() { printf '  - [%s] %s\n' "$1" "$2"; VIOLATIONS=$((VIOLATIONS + 1)); }

echo "== ADHD output lint =="

# Regla 10: preambulo
PRE=$(printf '%s\n' "$INPUT" | grep -inE '^\s*(gran pregunta|buena pregunta|excelente pregunta|dejame pensar|claro que si|por supuesto!|great question|let me think)' || true)
if [ -n "$PRE" ]; then
  report "R10 preambulo" "$(printf '%s' "$PRE" | head -1)"
fi

# Regla 10: cierres
CLO=$(printf '%s\n' "$INPUT" | grep -inE '(espero que (ayude|sirva|te sirva)|avisame si|dejame saber si|no dudes en|hope this helps|let me know if)' || true)
if [ -n "$CLO" ]; then
  report "R10 cierre" "$(printf '%s' "$CLO" | head -1)"
fi

# Regla 10: disculpas largas
SORRY=$(printf '%s\n' "$INPUT" | grep -inE '(lo siento mucho|perdon por|disculpa por|i apologi[sz]e|lamento el inconveniente)' || true)
if [ -n "$SORRY" ]; then
  report "R8 disculpa" "$(printf '%s' "$SORRY" | head -1)"
fi

# Regla 7: felicitacion vacia
CHEER=$(printf '%s\n' "$INPUT" | grep -inE '(excelente trabajo|gran trabajo|muy buen trabajo|great job|nice work|bien hecho!)' || true)
if [ -n "$CHEER" ]; then
  report "R7 adjetivo vacio" "$(printf '%s' "$CHEER" | head -1)"
fi

# Regla 6: estimados vagos
VAGUE=$(printf '%s\n' "$INPUT" | grep -inE '\b(un rato|un poco de tiempo|rapidito|en un rato|a bit|a while|in a bit)\b' || true)
if [ -n "$VAGUE" ]; then
  report "R6 estimado vago" "$(printf '%s' "$VAGUE" | head -1)"
fi

# Regla 9: listas de mas de 5 items (bloques consecutivos de bullets)
BULLETS=$(printf '%s\n' "$INPUT" | grep -cE '^\s*([-*]|[0-9]+\.)\s' || true)
MAXB=0
RUN=0
while IFS= read -r line; do
  if printf '%s' "$line" | grep -qE '^\s*([-*]|[0-9]+\.)\s'; then
    RUN=$((RUN + 1))
    [ "$RUN" -gt "$MAXB" ] && MAXB=$RUN
  else
    RUN=0
  fi
done <<< "$INPUT"
if [ "$MAXB" -gt 5 ]; then
  report "R9 lista larga" "bloque de $MAXB items (max 5; usar tabla si la lista es el entregable)"
fi

# Regla de escritura: em dash / en dash
# grep con locale UTF-8 falla en macOS/zsh ("character not in range"); python3 es portable.
DASH=$(printf '%s' "$INPUT" | python3 -c '
import sys
d = sys.stdin.read()
hits = [i + 1 for i, l in enumerate(d.splitlines()) if "\u2014" in l or "\u2013" in l]
if hits:
    print("lineas " + ", ".join(map(str, hits)))
' 2>/dev/null || true)
if [ -n "$DASH" ]; then
  report "guion" "em/en dash en $DASH - usar guion comun (-)"
fi

if [ "$VIOLATIONS" -eq 0 ]; then
  echo "OK - sin violaciones ($BULLETS bullets totales)"
  exit 0
fi

echo ""
echo "Total: $VIOLATIONS violacion(es). Revisar antes de enviar."
exit 1
