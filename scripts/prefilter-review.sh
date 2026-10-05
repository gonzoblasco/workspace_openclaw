#!/bin/bash
# prefilter-review.sh - Cheap triage pass of the A/B pipeline (ADR-089).
#
# Runs the gemma4:cloud pre-filter over a diff/patch and prints an advisory
# triage. It does NOT decide: gemma4 has a measured false negative on semantic
# defects (the clamp that makes a branch dead code), so anything touching
# logic/semantics still goes through the B gate (deepseek-v4.1-flash:cloud).
#
# The saving: for purely structural changes (CSS, styles, docs, format config)
# where the pre-filter comes back clean, the B call can be skipped. For
# anything else, B always runs.
#
# Usage:
#   prefilter-review.sh <file-with-diff>
#   git show HEAD | prefilter-review.sh -
#   PREFILTER_MODEL=glm-4.7-flash:q4_K_M prefilter-review.sh -   # override (not recommended)
#
# Exit: 0 always (advisory). Prints a TRIAGE line the CORE can act on.

set -uo pipefail

MODEL="${PREFILTER_MODEL:-gemma4:cloud}"
OLLAMA_BASE="${OLLAMA_BASE:-http://127.0.0.1:11434}"
MAX_DIFF_BYTES="${PREFILTER_MAX_BYTES:-48000}"

SRC="${1:-}"
if [ -z "$SRC" ]; then
  echo "Usage: prefilter-review.sh <file-with-diff | ->" >&2
  exit 2
fi
DIFF=$(cat "$SRC")
[ -z "$DIFF" ] && { echo "TRIAGE: EMPTY - nada que revisar."; exit 0; }

# Truncate defensively: a pre-filter is a triage, not a full read.
DIFF=$(printf '%s' "$DIFF" | head -c "$MAX_DIFF_BYTES")

# Classify the change by what it touches, to make the guard explicit.
# Structural (CSS/style/doc/format): pre-filter is authoritative when clean.
# Logic (everything else: .js/.ts/.py/.rs/... behaviour): B always runs.
STRUCTURAL_ONLY=1
while IFS= read -r line; do
  case "$line" in
    # File paths that are purely structural.
    ""|"+++ /dev/null"|"--- /dev/null"|"+++ b/"*.css|"--- a/"*.css|"+++ b/"*.md|"--- a/"*.md|"+++ b/"*.json|"--- a/"*.json|"+++ b/"*.toml|"--- a/"*.toml|"+++ b/"*.yml|"--- a/"*.yml|"+++ b/"*.yaml|"--- a/"*.yaml) ;;
    "+++ "*|"--- "*) STRUCTURAL_ONLY=0 ;;
  esac
done <<< "$DIFF"

PROMPT="Sos un REVISOR DE CODIGO. Triage rapido de este diff. Reporta SOLO defectos que
rompen comportamiento (no estilo). Un defecto por linea: DEFECTO: <archivo> - <que> - <fix>.
Si el diff no tiene defectos, responde exactamente: LIMPIO.

DIFF:
$DIFF"

BODY=$(python3 - "$MODEL" "$PROMPT" <<'PY'
import json, sys
model, prompt = sys.argv[1], sys.argv[2]
print(json.dumps({"model": model, "stream": False, "think": False,
                  "messages": [{"role": "user", "content": prompt}],
                  "options": {"temperature": 0, "num_ctx": 8192, "num_predict": 600}}))
PY
)

RESP=$(curl -s --max-time 120 "$OLLAMA_BASE/api/chat" -d "$BODY" \
  | python3 -c "import json,sys; print((json.load(sys.stdin).get('message',{}) or {}).get('content',''))" 2>/dev/null)

echo "== pre-filtro ($MODEL) =="
echo "$RESP"
echo
if printf '%s' "$RESP" | grep -qiE "^\s*LIMPIO\s*$|sin defectos"; then
  if [ "$STRUCTURAL_ONLY" = "1" ]; then
    echo "TRIAGE: LIMPIO (solo estructural) -> se puede omitir el gate B."
  else
    echo "TRIAGE: LIMPIO pero TOCA LOGICA -> el gate B (deepseek) corre igual (FN medido en semantica)."
  fi
else
  echo "TRIAGE: CANDIDATOS -> el gate B (deepseek) adjudica y decide."
fi
exit 0
