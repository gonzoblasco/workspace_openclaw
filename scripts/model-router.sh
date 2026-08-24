#!/bin/bash
# model-router.sh - Route which Ollama model to use per task type.
#
# Ported concept from the ToggleLogic plugin (ClawHub) WITHOUT its patented
# license: a simple configurable router by task type + sticky owner overrides.
# Choose the model per task (code/review/long/cheap) instead of picking it
# manually every time.
#
# State lives in model-routes.json (or $MODEL_ROUTES_FILE).
#
# Usage:
#   model-router.sh list                  # show routes + override
#   model-router.sh model <tipo>          # what model to use for a task type
#   model-router.sh set <tipo> <model>    # override model for a type (sticky)
#   model-router.sh reset <tipo>          # clear override for a type
#   model-router.sh default <model>       # set the fallback default
#   model-router.sh edit                  # open routes file for manual edit
#
# Exit: 0 ok.

set -uo pipefail

STATE_FILE="${MODEL_ROUTES_FILE:-model-router.json}"

# Default routes (task type -> model). Edit with `model-router.sh edit`.
ROUTES='{
  "default": "deepseek-v4-flash:cloud",
  "routes": {
    "code": "kimi-k2.7-code:cloud",
    "review": "deepseek-v4-flash:cloud",
    "long": "deepseek-v4-pro:cloud",
    "cheap": "gemma4:cloud",
    "writing": "kimi-k3:cloud"
  },
  "overrides": {}
}'

read_state() {
  if [ -f "$STATE_FILE" ]; then
    cat "$STATE_FILE"
  else
    echo "$ROUTES"
  fi
}

write_state() {
  if command -v jq >/dev/null 2>&1; then
    echo "$1" | jq . > "$STATE_FILE"
  else
    echo "$1" > "$STATE_FILE"
  fi
}

CMD="${1:-}"
[ -z "$CMD" ] && { echo "Usage: model-router.sh {list|model|set|reset|default|edit}" >&2; exit 1; }

case "$CMD" in
  list)
    read_state | jq -r '"Default: " + .default, "",
      "TIPO\tMODELO\t(override)",
      (.routes | to_entries[] | "\(.key)\t\(.value)\t\(.key)"), 
      "\nOverrides:",
      (.overrides | if length==0 then "  (ninguno)" else (to_entries[] | "  \(.key) -> \(.value)") end)' 2>/dev/null || read_state
    ;;

  model)
    TYPE="${2:-default}"
    STATE=$(read_state)
    # override wins if present
    OVER=$(echo "$STATE" | jq -r --arg t "$TYPE" '.overrides[$t] // empty' 2>/dev/null)
    if [ -n "$OVER" ]; then
      echo "$OVER"
    else
      echo "$STATE" | jq -r --arg t "$TYPE" '.routes[$t] // .default' 2>/dev/null || echo "deepseek-v4-flash:cloud"
    fi
    ;;

  set)
    TYPE="${2:-}"; MODEL="${3:-}"
    [ -z "$TYPE" ] || [ -z "$MODEL" ] && { echo "set requires <tipo> <model>" >&2; exit 1; }
    STATE=$(read_state)
    NEW=$(echo "$STATE" | jq --arg t "$TYPE" --arg m "$MODEL" '.overrides[$t] = $m')
    write_state "$NEW"
    echo "[override] $TYPE -> $MODEL"
    ;;

  reset)
    TYPE="${2:-}"
    [ -z "$TYPE" ] && { echo "reset requires <tipo>" >&2; exit 1; }
    STATE=$(read_state)
    NEW=$(echo "$STATE" | jq --arg t "$TYPE" 'del(.overrides[$t])')
    write_state "$NEW"
    echo "[reset] override de $TYPE borrado"
    ;;

  default)
    MODEL="${2:-}"
    [ -z "$MODEL" ] && { echo "default requires <model>" >&2; exit 1; }
    STATE=$(read_state)
    NEW=$(echo "$STATE" | jq --arg m "$MODEL" '.default = $m')
    write_state "$NEW"
    echo "[default] $MODEL"
    ;;

  edit)
    if [ ! -f "$STATE_FILE" ]; then
      write_state "$ROUTES"
    fi
    echo "Editando $STATE_FILE ..."
    "${EDITOR:-vi}" "$STATE_FILE"
    ;;

  *)
    echo "usage: model-router.sh {list|model|set|reset|default|edit}" >&2
    exit 1
    ;;
esac
