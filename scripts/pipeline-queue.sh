#!/bin/bash
# pipeline-queue.sh - Durable execution queue on top of pipeline-track.sh.
#
# Additive layer: writes the same state fields as pipeline-track.sh plus three
# new ones (attempts, pid, lastError) into the same pipeline-state.json.
# Adds: next-unit selection, orphan detection (kill -0), retries with a cap
# (PIPELINE_MAX_ATTEMPTS, default 3) and a terminal `failed` state that does
# not block the rest of the queue.
#
# Usage:
#   pipeline-queue.sh enqueue "<fase>" [--score T] U1 U2 ...  # new plan, attempts=0
#   pipeline-queue.sh next                                    # first queued unit, skips failed
#   pipeline-queue.sh claim <unit> <pid>                      # running + pid + attempts++ + startTime
#   pipeline-queue.sh release <unit> [reason]                 # retry or failed per attempts
#   pipeline-queue.sh done <unit>                             # delegates to pipeline-track
#   pipeline-queue.sh review <unit>                           # delegates to pipeline-track
#   pipeline-queue.sh orphans                                 # running units with dead pid
#   pipeline-queue.sh tick                                    # requeue orphans, print next
#   pipeline-queue.sh report                                  # per-unit telemetry
#   pipeline-queue.sh status                                 # extended status
#
# Exit: 0 ok. 2 usage/validation error.

set -uo pipefail

STATE_FILE="${PIPELINE_STATE_FILE:-pipeline-state.json}"
MAX_ATTEMPTS="${PIPELINE_MAX_ATTEMPTS:-3}"
# Sanitize the cap: a non-numeric or <1 value leaks `integer expression
# expected` and silently disables the retry ceiling.
case "$MAX_ATTEMPTS" in
  ''|*[!0-9]*)
    echo "PIPELINE_MAX_ATTEMPTS='$MAX_ATTEMPTS' invalido: usando 3." >&2
    MAX_ATTEMPTS=3
    ;;
esac
if [ "$MAX_ATTEMPTS" -lt 1 ]; then
  echo "PIPELINE_MAX_ATTEMPTS=$MAX_ATTEMPTS invalido (minimo 1): usando 3." >&2
  MAX_ATTEMPTS=3
fi
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
TRACK="$SCRIPT_DIR/pipeline-track.sh"

usage() {
  echo "Usage: pipeline-queue.sh {enqueue|next|claim|release|done|review|orphans|tick|report|status} [args]" >&2
  exit 2
}

read_state() {
  if [ -f "$STATE_FILE" ] && [ -s "$STATE_FILE" ]; then
    cat "$STATE_FILE"
  else
    echo '{"fase":"","units":[]}'
  fi
}

# A corrupt state file must fail loud: reading it as an empty queue would
# drop every pending unit without a trace.
require_valid_state() {
  if [ -f "$STATE_FILE" ] && [ -s "$STATE_FILE" ]; then
    if ! jq -e . "$STATE_FILE" >/dev/null 2>&1; then
      echo "Estado corrupto: '$STATE_FILE' no es JSON valido. Abortando." >&2
      exit 2
    fi
  fi
}

write_state() {
  # Atomic write: build the full document in a temp file and rename it into
  # place. A bare `> "$STATE_FILE"` truncated the file before jq ran, and a
  # failed redirection was swallowed by the pipeline (echo/jq both exit 0),
  # so the command reported success while the on-disk state never changed.
  local tmp="${STATE_FILE}.tmp.$$"
  if command -v jq >/dev/null 2>&1; then
    if ! printf '%s' "$1" | jq . > "$tmp" 2>/dev/null; then
      rm -f "$tmp"
      echo "Error: estado invalido, no se pudo serializar. '$STATE_FILE' sin cambios." >&2
      exit 2
    fi
  else
    if ! printf '%s' "$1" > "$tmp" 2>/dev/null; then
      rm -f "$tmp"
      echo "Error: no se pudo escribir '$tmp' (disco o permisos)." >&2
      exit 2
    fi
  fi
  if ! mv "$tmp" "$STATE_FILE" 2>/dev/null; then
    rm -f "$tmp"
    echo "Error: no se pudo reemplazar '$STATE_FILE' (directorio inexistente o sin permiso)." >&2
    exit 2
  fi
}

# --- Locking ----------------------------------------------------------------
# macOS has no flock(1). Atomic mkdir is the portable mutual-exclusion
# primitive: exactly one process can create the directory. Held for the whole
# mutating command, so the read-modify-write window is protected.
LOCK_DIR="${STATE_FILE}.lock"
LOCK_PID_FILE="$LOCK_DIR/pid"
LOCK_TRIES=100   # ~10s at 0.1s per attempt
LOCK_GRACE=20    # ~2s before breaking a lock that has no pid file
LOCK_HELD=0

acquire_lock() {
  local i=0 locker=""
  # Fail fast and clearly when the state directory itself is missing:
  # retrying mkdir for 10s only to blame a lock holder is misleading.
  case "$STATE_FILE" in
    */*)
      local parent; parent=$(dirname "$STATE_FILE")
      if [ ! -d "$parent" ]; then
        echo "Error: el directorio '$parent' no existe. No se puede escribir '$STATE_FILE'." >&2
        return 1
      fi
      ;;
  esac
  while ! mkdir "$LOCK_DIR" 2>/dev/null; do
    i=$((i + 1))
    # Break a lock whose owner is gone (crashed agent, killed shell).
    if [ -f "$LOCK_PID_FILE" ]; then
      locker=$(cat "$LOCK_PID_FILE" 2>/dev/null || echo "")
      case "$locker" in
        ''|*[!0-9]*) : ;;
        *)
          if ! kill -0 "$locker" 2>/dev/null; then
            rm -rf "$LOCK_DIR" 2>/dev/null || true
            continue
          fi
          ;;
      esac
    elif [ "$i" -gt "$LOCK_GRACE" ]; then
      # No pid file: the owner died between mkdir and writing its pid, or the
      # pid file vanished. Without this, such a lock is never broken and every
      # later command stalls until the retry ceiling and then fails.
      rm -rf "$LOCK_DIR" 2>/dev/null || true
      continue
    fi
    if [ "$i" -ge "$LOCK_TRIES" ]; then
      echo "No se pudo adquirir el lock de '$STATE_FILE' (pid ${locker:-?} lo retiene)." >&2
      return 1
    fi
    sleep 0.1
  done
  printf '%s' "$$" > "$LOCK_PID_FILE" 2>/dev/null || true
  LOCK_HELD=1
  return 0
}

release_lock() {
  [ "$LOCK_HELD" -eq 1 ] || return 0
  rm -rf "$LOCK_DIR" 2>/dev/null || true
  LOCK_HELD=0
}

# unit_count <unit>: 1 if the unit exists, 0 otherwise
unit_count() {
  read_state | jq --arg u "$1" '[.units[] | select(.name==$u)] | length' 2>/dev/null || echo 0
}

require_unit() {
  [ "$(unit_count "$1")" = "1" ] || {
    echo "Unidad '$1' no existe en el pipeline (o estado corrupto)." >&2
    exit 2
  }
}

# orphan_names: running units whose pid is set and dead, one name per line.
# Rule: a running unit without pid is NOT an orphan (old plan compatibility).
orphan_names() {
  read_state | jq -r '.units[] | select(.state == "running" and (.pid != null)) | (.name + "\t" + (.pid | tostring))' 2>/dev/null |
  while IFS=$'\t' read -r name pid; do
    # Only a positive integer is a real pid. `kill -0 0` and `kill -0 -1`
    # succeed (process group / all processes), so such a unit would look
    # permanently alive and never be requeued. Non-numeric pids are dead.
    case "$pid" in
      ''|*[!0-9]*) echo "$name"; continue ;;
    esac
    if [ "$pid" -le 0 ]; then
      echo "$name"; continue
    fi
    if ! kill -0 "$pid" 2>/dev/null; then
      echo "$name"
    fi
  done
}

CMD="${1:-}"
shift || true

# Fail loud on a corrupt state file for every command that reads it.
# enqueue is excluded: it rewrites the plan and is the recovery path.
if [ "$CMD" != "enqueue" ]; then
  require_valid_state
fi

# Commands that mutate the plan take the lock for their whole duration, so
# two concurrent claims cannot both read `queued` and both write `running`.
case "$CMD" in
  enqueue|claim|release|done|review|tick)
    acquire_lock || exit 2
    trap 'release_lock' EXIT INT TERM
    ;;
esac

case "$CMD" in
  enqueue)
    # Delegate plan creation to pipeline-track (parity + complexity), then add
    # the queue counter `attempts` to every unit of the new plan.
    bash "$TRACK" init "$@" >/dev/null || exit 2
    STATE=$(read_state)
    NEW=$(echo "$STATE" | jq '.units[] |= . + {attempts: 0}')
    write_state "$NEW"
    N_UNITS=$(echo "$NEW" | jq '[.units[]] | length')
    # A silent zero here means the plan never landed on disk (missing dir,
    # full disk). Reporting success would let an automation march on.
    if [ "${N_UNITS:-0}" -lt 1 ]; then
      echo "Error: no se pudo encolar el plan (0 unidades escritas en '$STATE_FILE')." >&2
      exit 2
    fi
    echo "Pipeline encolado: $N_UNITS unidades con attempts=0."
    ;;

  next)
    # Deterministic: always the first queued unit in declaration order.
    # `failed` units are skipped, never block the queue.
    read_state | jq -r '[.units[] | select(.state == "queued") | .name] | .[0] // empty'
    ;;

  claim)
    UNIT="${1:-}"; PID="${2:-}"
    [ -n "$UNIT" ] && [ -n "$PID" ] || { echo "claim requires <unit> <pid>" >&2; exit 2; }
    require_unit "$UNIT"
    STATE=$(read_state)
    CSTATE=$(echo "$STATE" | jq -r --arg u "$UNIT" '.units[] | select(.name==$u) | .state')
    case "$CSTATE" in
      running)
        CPID=$(echo "$STATE" | jq -r --arg u "$UNIT" '.units[] | select(.name==$u) | .pid // empty')
        # Idempotency: same unit already running with live pid is not duplicated.
        if [ -n "$CPID" ] && kill -0 "$CPID" 2>/dev/null; then
          echo "Unidad '$UNIT' ya esta en ejecucion (pid $CPID). Claim ignorado."
          exit 0
        fi
        # Otherwise: pid dead or absent, proceed as a re-claim (new attempt).
        ;;
      done)
        echo "Unidad '$UNIT' esta done: no se puede claim." >&2
        exit 2
        ;;
      failed)
        echo "Unidad '$UNIT' esta failed (terminal): no se puede claim." >&2
        exit 2
        ;;
    esac
    CA=$(echo "$STATE" | jq -r --arg u "$UNIT" '.units[] | select(.name==$u) | (.attempts // 0)')
    NA=$(( ${CA:-0} + 1 ))
    # Cap defense: never start an attempt beyond the max (would loop forever).
    if [ "$NA" -gt "$MAX_ATTEMPTS" ]; then
      NEW=$(echo "$STATE" | jq --arg u "$UNIT" --arg m "max attempts reached ($MAX_ATTEMPTS)" \
        '(.units[] | select(.name==$u) | .state) = "failed"
       | (.units[] | select(.name==$u) | .pid) = null
       | (.units[] | select(.name==$u) | .lastError) = $m')
      write_state "$NEW"
      echo "Unidad '$UNIT' supera el maximo de reintentos ($MAX_ATTEMPTS): failed."
      exit 0
    fi
    NOW=$(date +%s)
    NEW=$(echo "$STATE" | jq --arg u "$UNIT" --arg p "$PID" --arg t "$NOW" --argjson na "$NA" \
      '(.units[] | select(.name==$u) | .state) = "running"
     | (.units[] | select(.name==$u) | .pid) = $p
     | (.units[] | select(.name==$u) | .attempts) = $na
     | (.units[] | select(.name==$u) | .startTime) = (if .startTime == null then $t else .startTime end)
     | (.units[] | select(.name==$u) | .lastError) = null')
    write_state "$NEW"
    echo "[claim] $UNIT -> running (pid $PID, intento $NA de $MAX_ATTEMPTS)"
    ;;

  release)
    UNIT="${1:-}"; REASON="${2:-}"
    [ -n "$UNIT" ] || { echo "release requires <unit> [reason]" >&2; exit 2; }
    require_unit "$UNIT"
    STATE=$(read_state)
    CA=$(echo "$STATE" | jq -r --arg u "$UNIT" '.units[] | select(.name==$u) | (.attempts // 0)')
    CA=${CA:-0}
    if [ "$CA" -ge "$MAX_ATTEMPTS" ]; then
      MSG="${REASON:-max attempts reached ($MAX_ATTEMPTS)}"
      NEW=$(echo "$STATE" | jq --arg u "$UNIT" --arg m "$MSG" \
        '(.units[] | select(.name==$u) | .state) = "failed"
       | (.units[] | select(.name==$u) | .pid) = null
       | (.units[] | select(.name==$u) | .lastError) = $m')
      write_state "$NEW"
      echo "[release] $UNIT -> failed (intentos $CA >= max $MAX_ATTEMPTS): $MSG"
    else
      NEW=$(echo "$STATE" | jq --arg u "$UNIT" \
        '(.units[] | select(.name==$u) | .state) = "queued"
       | (.units[] | select(.name==$u) | .pid) = null')
      if [ -n "$REASON" ]; then
        NEW=$(echo "$NEW" | jq --arg u "$UNIT" --arg r "$REASON" \
          '(.units[] | select(.name==$u) | .lastError) = $r')
      fi
      write_state "$NEW"
      echo "[release] $UNIT -> queued (intento $CA de max $MAX_ATTEMPTS)"
    fi
    ;;

  done|review)
    # Pure delegation: pipeline-track owns these transitions.
    UNIT="${1:-}"
    [ -n "$UNIT" ] || { echo "$CMD requires <unit>" >&2; exit 2; }
    bash "$TRACK" "$CMD" "$UNIT"
    ;;

  orphans)
    orphan_names
    ;;

  tick)
    # Single entry point for automations: requeue orphans (or fail them when
    # attempts are exhausted) and print the next unit to run.
    REQUEUED=0
    FAILED=0
    for NAME in $(orphan_names); do
      STATE=$(read_state)
      CA=$(echo "$STATE" | jq -r --arg u "$NAME" '.units[] | select(.name==$u) | (.attempts // 0)')
      CA=${CA:-0}
      if [ "$CA" -ge "$MAX_ATTEMPTS" ]; then
        NEW=$(echo "$STATE" | jq --arg u "$NAME" --arg m "huerfana con reintentos agotados ($MAX_ATTEMPTS)" \
          '(.units[] | select(.name==$u) | .state) = "failed"
         | (.units[] | select(.name==$u) | .pid) = null
         | (.units[] | select(.name==$u) | .lastError) = $m')
        write_state "$NEW"
        FAILED=$((FAILED+1))
        echo "[tick] $NAME -> failed (reintentos agotados)"
      else
        NEW=$(echo "$STATE" | jq --arg u "$NAME" \
          '(.units[] | select(.name==$u) | .state) = "queued"
         | (.units[] | select(.name==$u) | .pid) = null')
        write_state "$NEW"
        REQUEUED=$((REQUEUED+1))
        echo "[tick] $NAME -> queued (huerfana)"
      fi
    done
    echo "[tick] $REQUEUED reencolada(s), $FAILED failed."
    read_state | jq -r '[.units[] | select(.state == "queued") | .name] | .[0] // empty'
    ;;

  report)
    # Per-unit telemetry: queue counters, liveness fields, track history.
    read_state | jq -r '"UNIT | STATE | OWNER | ATTEMPTS | PID | LAST-ERROR | ITER | REGR",
      (.units[] | (.name + " | " + .state + " | " + .owner + " | " + ((.attempts // 0)|tostring) + " | " + (.pid // "-") + " | " + (.lastError // "-") + " | " + ((.iterations // 0)|tostring) + " | " + ((.regressions // 0)|tostring)))' 2>/dev/null || {
      echo "Telemetria (sin jq):"; read_state; }
    ;;

  status)
    # Extended status: phase header, queue counts by state, per-unit line.
    read_state | jq -r --arg max "$MAX_ATTEMPTS" '
      "Fase: " + .fase + " | T-score: " + (.complexity // "n/a") + " | max attempts: " + $max,
      "QUEUED: " + ([.units[] | select(.state=="queued")] | length | tostring) +
      " RUNNING: " + ([.units[] | select(.state=="running")] | length | tostring) +
      " REVIEW: " + ([.units[] | select(.state=="review")] | length | tostring) +
      " DONE: " + ([.units[] | select(.state=="done")] | length | tostring) +
      " FAILED: " + ([.units[] | select(.state=="failed")] | length | tostring),
      "UNIT | STATE | OWNER | ATTEMPTS | PID | LAST-ERROR",
      (.units[] | (.name + " | " + .state + " | " + .owner + " | " + ((.attempts // 0)|tostring) + " | " + (.pid // "-") + " | " + (.lastError // "-")))' 2>/dev/null || {
      echo "Estado (sin jq):"; read_state; }
    ;;

  *)
    usage
    ;;
esac
