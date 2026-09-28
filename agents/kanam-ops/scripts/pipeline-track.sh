#!/bin/bash
# pipeline-track.sh - Durable pipeline state for the A/B agent pipeline.
#
# Ported concept from Pipeline Architect plugin (ClawHub): track units with
# durable state that survives crashes (SIGKILL), restarts, and evictions.
# When an agent dies mid-task, `status` shows what's pending and `resume`
# lists what to relaunch.
#
# State lives in pipeline-state.json (or $PIPELINE_STATE_FILE). Each unit has:
#   state: queued | running | review | done
#   owner: A | B        (parity)
#   note:  last comment
#   complexity: T-score (1-20) from complexity-scorer.sh
#
# Usage:
#   pipeline-track.sh init "<fase>" U1 U2 U3 ...   # create plan
#   pipeline-track.sh init "<fase>" --score T U1 U2 # create plan with complexity
#   pipeline-track.sh start U2                     # mark running (owner auto)
#   pipeline-track.sh review U2                    # mark needs review
#   pipeline-track.sh done U2                      # mark done
#   pipeline-track.sh status                       # show state table
#   pipeline-track.sh resume                       # show units not done (to relaunch)
#   pipeline-track.sh note U2 "<msg>"              # attach note
#   pipeline-track.sh reset                        # clear state
#
# Exit: 0 ok.

set -uo pipefail

STATE_FILE="${PIPELINE_STATE_FILE:-pipeline-state.json}"

usage() {
  echo "Usage: pipeline-track.sh {init|start|review|done|status|resume|note|reset} [args]" >&2
  exit 2
}

read_state() {
  if [ -f "$STATE_FILE" ]; then
    cat "$STATE_FILE"
  else
    echo '{"fase":"","units":[]}'
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

case "$CMD" in
  init)
    FASE="${2:-}"
    shift 2 || true
    COMPLEXITY_SCORE=""
    UNITS=()
    # scan for --score T
    WAIT_SCORE=""
    for arg in "$@"; do
      if [ "$arg" = "--score" ]; then
        WAIT_SCORE=true; continue
      elif [ "${WAIT_SCORE:-}" = "true" ]; then
        COMPLEXITY_SCORE="$arg"; WAIT_SCORE=""
      else
        UNITS+=("$arg")
      fi
    done
    if [ -z "$FASE" ] || [ "${#UNITS[@]}" -eq 0 ]; then
      echo "init requires: <fase> [--score T] <U1> <U2> ..." >&2; exit 2
    fi
    units_json="[]"
    i=0
    for u in "${UNITS[@]}"; do
      if [ $((i % 2)) -eq 0 ]; then owner="A"; else owner="B"; fi
      units_json=$(echo "$units_json" | jq --arg u "$u" --arg o "$owner" --arg s "queued" --arg n "" \
        '. + [{name: $u, state: $s, owner: $o, note: $n, startTime: null, endTime: null, iterations: 0, regressions: 0}]')
      i=$((i+1))
    done
    if [ -n "$COMPLEXITY_SCORE" ]; then
      write_state "{\"fase\":\"$FASE\",\"complexity\":\"$COMPLEXITY_SCORE\",\"units\":$units_json}"
      echo "Pipeline '$FASE' inicializado: ${#UNITS[@]} unidades. Complexity: T=$COMPLEXITY_SCORE."
    else
      write_state "{\"fase\":\"$FASE\",\"units\":$units_json}"
      echo "Pipeline '$FASE' inicializado: ${#UNITS[@]} unidades. (sin T-score)"
    fi
    ;;

  show|status)
    # separator is | to avoid tab/quote escaping issues in jq
    read_state | jq -r '"Fase: " + .fase + " | T-score: " + (.complexity // "n/a"), "", "UNIT | STATE | OWNER | NOTE", (.units[] | (.name + " | " + .state + " | " + .owner + " | " + (.note // "-")))' 2>/dev/null || {
      echo "Estado (sin jq):"; read_state; }
    ;;

  resume)
    read_state | jq -r '.units[] | select(.state != "done") | (.name + " | " + .state + " | " + .owner)' 2>/dev/null || \
    read_state | jq -r '[.units[] | select(.state != "done") | .name] | join(" ")' 2>/dev/null || \
    echo "Sin unidades pendientes (o estado vacio)."
    ;;

  start|review|done)
    UNIT="${2:-}"
    [ -z "$UNIT" ] && { echo "$CMD requires <unit>" >&2; exit 2; }
    STATE=$(read_state)
    # validate unit exists (fail-friendly)
    COUNT=$(echo "$STATE" | jq --arg u "$UNIT" '[.units[] | select(.name==$u)] | length' 2>/dev/null)
    if [ "$COUNT" != "1" ]; then
      echo "Unidad '$UNIT' no existe en el pipeline (o estado corrupto)." >&2; exit 2
    fi

    # Telemetry logic
    NOW=$(date +%s)
    if [ "$CMD" = "start" ]; then
      # If it already had a startTime, it's a re-iteration
      S_TIME=$(echo "$STATE" | jq --arg u "$UNIT" '.units[] | select(.name==$u) | .startTime')
      if [ "$S_TIME" != "null" ]; then
        STATE=$(echo "$STATE" | jq --arg u "$UNIT" '(.units[] | select(.name==$u) | .iterations) += 1')
      fi
      NEW=$(echo "$STATE" | jq --arg u "$UNIT" --arg s "$CMD" --arg t "$NOW" \
        '(.units[] | select(.name==$u) | .state) = $s | (.units[] | select(.name==$u) | .startTime) = (if .startTime == null then $t else .startTime end)')
    elif [ "$CMD" = "done" ]; then
      NEW=$(echo "$STATE" | jq --arg u "$UNIT" --arg s "$CMD" --arg t "$NOW" \
        '(.units[] | select(.name==$u) | .state) = $s | (.units[] | select(.name==$u) | .endTime) = $t')
    else
      NEW=$(echo "$STATE" | jq --arg u "$UNIT" --arg s "$CMD" '(.units[] | select(.name==$u) | .state) = $s')
    fi
    write_state "$NEW"
    echo "[$CMD] $UNIT"
    ;;

  note)
    UNIT="${2:-}"; NOTE="${3:-}"
    [ -z "$UNIT" ] || [ -z "$NOTE" ] && { echo "note requires <unit> <msg>" >&2; exit 2; }
    STATE=$(read_state)
    NEW=$(echo "$STATE" | jq --arg u "$UNIT" --arg n "$NOTE" '(.units[] | select(.name==$u) | .note) = $n')
    write_state "$NEW"
    echo "[note] $UNIT: $NOTE"
    ;;

  regress)
    UNIT="${2:-}"
    [ -z "$UNIT" ] && { echo "regress requires <unit>" >&2; exit 2; }
    STATE=$(read_state)
    # validate unit exists
    COUNT=$(echo "$STATE" | jq --arg u "$UNIT" '[.units[] | select(.name==$u)] | length' 2>/dev/null)
    if [ "$COUNT" != "1" ]; then
      echo "Unidad '$UNIT' no existe en el pipeline." >&2; exit 2
    fi
    NEW=$(echo "$STATE" | jq --arg u "$UNIT" '(.units[] | select(.name==$u) | .regressions) += 1')
    write_state "$NEW"
    echo "[regress] $UNIT: regression marked (Agent B introduced error)"
    ;;

  reset)
    rm -f "$STATE_FILE"
    echo "Estado del pipeline borrado."
    ;;

  *)
    usage
    ;;
esac
