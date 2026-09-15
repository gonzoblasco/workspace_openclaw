#!/usr/bin/env bash
# pipeline-report.sh - Aggregated telemetry from the durable pipeline queue.
#
# Read-only view over $PIPELINE_STATE_FILE (default pipeline-state.json).
# It does NOT mutate anything: what it reports is already captured by
# pipeline-track.sh (startTime/endTime/iterations/regressions) and
# pipeline-queue.sh (attempts/pid/lastError). This script only sums and
# renders them, so the observability signal costs zero and adds no
# dependency - per ROADMAP 1.1 and the "observabilidad 0 $/0 dependencias"
# decision.
#
# Signals it surfaces:
#   - duration per unit (endTime - startTime) and total for a phase
#   - retries/attempts per unit (flaky or crashed work)
#   - regressions: how many times Agent B introduced a bug while 'fixing'
#     - this is the ROADMAP 1.1 signal no one has measured yet
#   - phase rollup: counts by state, avg/max duration
#
# Usage:
#   ./scripts/pipeline-report.sh                 # human table
#   ./scripts/pipeline-report.sh --json          # machine-readable
#   PIPELINE_STATE_FILE=/tmp/state.json ./scripts/pipeline-report.sh
#
# Exit 0 ok. Exit 2 on a missing/corrupt/unparseable state file.

set -uo pipefail

STATE_FILE="${PIPELINE_STATE_FILE:-pipeline-state.json}"

if [ ! -f "$STATE_FILE" ] || [ ! -s "$STATE_FILE" ]; then
  echo "No hay estado de pipeline en '$STATE_FILE' (aun no se inicializo)." >&2
  exit 2
fi

if ! jq -e . "$STATE_FILE" >/dev/null 2>&1; then
  echo "Estado corrupto: '$STATE_FILE' no es JSON valido." >&2
  exit 2
fi

JQ_SCRIPT='
  def epoch: select(type == "number") | .;
  . as $root |
  ($root.units | length) as $N |
  ($root.units | map(select(.state == "done")) | length) as $Ndone |
  # duration per unit; units with endTime but no startTime are unmeasurable
  ($root.units | map(
    { n: .name,
      state: .state,
      owner: (.owner // "?"),
      seconds: ((.endTime // null) as $e | (.startTime // null) as $s |
                (if ($e != null and $s != null and ($e|type)=="number" and ($s|type)=="number") then $e - $s else null end)),
      iter: (.iterations // 0),
      regr: (.regressions // 0),
      attempts: (.attempts // 0)
    })) as $u |
  # totals over measurable done/failed units
  ($u | map(select(.seconds != null)) | map(.seconds) | add // 0) as $sumSec |
  ($u | map(select(.seconds != null)) | length) as $sumN |
  ($u | map(.regr) | add // 0) as $Tregr |
  ($u | map(.attempts) | add // 0) as $Tattempts |
  ($u | map(select(.seconds != null)) | map(.seconds) | (if length>0 then max else null end)) as $maxSec |
  ($u | map(select(.seconds != null)) | map(.seconds) | (if length>0 then add/length else null end)) as $avgSec |
  {
    phase: ($root.fase // ""),
    complexity: ($root.complexity // null),
    units_total: $N,
    units_done: $Ndone,
    units_failed: ($root.units | map(select(.state == "failed")) | length),
    total_seconds: $sumSec,
    measured_units: $sumN,
    avg_seconds: $avgSec,
    max_seconds: $maxSec,
    regressions_total: $Tregr,
    attempts_total: $Tattempts,
    units: $u
  }
'

RESULT="$(jq -c "$JQ_SCRIPT" "$STATE_FILE" 2>/dev/null)" || {
  echo "Error: no se pudo agregar el estado de '$STATE_FILE'." >&2
  exit 2
}

if [ "${1:-}" = "--json" ]; then
  echo "$RESULT"
  exit 0
fi

echo "$RESULT" | jq -r '
  "# " + (.phase | if .=="" then "(sin fase)" else . end)
    + (if .complexity then "   T=" + (.complexity|tostring) else "" end),
  "",
  "Unidades: " + (.units_total|tostring) + " | done: " + (.units_done|tostring)
    + " | failed: " + (.units_failed|tostring),
  (if (.measured_units // 0) > 0 then
     "Tiempo total: " + (.total_seconds|tostring) + "s sobre " + (.measured_units|tostring) + " unidades medibles"
     + " | avg: " + ((.avg_seconds // 0)|tostring) + "s | max: " + ((.max_seconds // 0)|tostring) + "s"
   else "Tiempo: sin unidades medibles (no hay endTime+startTime)." end),
  "Regresiones (bugs de B al 'corregir'): " + (.regressions_total|tostring)
    + " | Reintentos totales: " + (.attempts_total|tostring),
  "",
  "UNIT | STATE | OWNER | ATTEMPTS | ITER | REGR | SECS",
  (.units[] | .n + " | " + .state + " | " + .owner + " | " + (.attempts|tostring)
    + " | " + (.iter|tostring) + " | " + (.regr|tostring)
    + " | " + (if .seconds != null then (.seconds|tostring) else "-" end))
' 2>/dev/null || {
  echo "$RESULT"
}