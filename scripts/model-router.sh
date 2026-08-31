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
#   model-router.sh fail <tipo> <model>   # log a failure for telemetry
#   model-router.sh edit                  # open routes file for manual edit
#
# Exit: 0 ok.

set -uo pipefail

STATE_FILE="${MODEL_ROUTES_FILE:-model-router.json}"

# Default routes (task type -> model). Edit with `model-router.sh edit`.
# Pipeline A/B (2026-08-30): DeepSeek Flash (iter 1-2) -> GLM 5.3 Flash (iter 3) -> Kimi K2.7 Code (iter 4, nivel superior).
# Sincronizado con Regla MAX/HIGH: Code y Review usan DeepSeek Flash.
ROUTES='{
  "default": "deepseek-v4-flash:cloud",
  "routes": {
    "code": "deepseek-v4-flash:cloud",
    "review": "deepseek-v4-flash:cloud",
    "long": "glm-5.3-flash:cloud",
    "cheap": "gemma4:cloud",
    "writing": "glm-5.3-flash:cloud",
    "pipeline_ab": "deepseek-v4-flash:cloud | glm-5.3-flash:cloud | kimi-k2.7-code:cloud"
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
[ -z "$CMD" ] && { echo "Usage: model-router.sh {list|model|set|reset|default|fail|edit}" >&2; exit 1; }

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

  fail)
    TYPE="${2:-}"; MODEL="${3:-}"
    [ -z "$TYPE" ] || [ -z "$MODEL" ] && { echo "fail requires <tipo> <model>" >&2; exit 1; }
    LOG_FILE="model-failures.json"
    # Initialize log file if not exists
    [ ! -f "$LOG_FILE" ] && echo "[]" > "$LOG_FILE"
    # Append failure: timestamp, type, model
    TIMESTAMP=$(date +%s)
    NEW_LOG=$(jq --arg t "$TYPE" --arg m "$MODEL" --arg ts "$TIMESTAMP" \
      '. + [{timestamp: $ts, type: $t, model: $m}]' "$(cat "$LOG_FILE")")
    echo "$NEW_LOG" > "$LOG_FILE"
    echo "[fail] Registered failure for $MODEL in $TYPE"
    ;;

  edit)
    if [ ! -f "$STATE_FILE" ]; then
      write_state "$ROUTES"
    fi
    echo "Editando $STATE_FILE ..."
    "${EDITOR:-vi}" "$STATE_FILE"
    ;;

  *)
    echo "usage: model-router.sh {list|model|set|reset|default|fail|edit}" >&2
    exit 1
    ;;
esac
