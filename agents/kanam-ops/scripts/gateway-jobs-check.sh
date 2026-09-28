#!/usr/bin/env bash
# gateway-jobs-check.sh - Watchdog of gateway automations/jobs.
# Checks: jobs exist, enabled, nextRun not overdue, status not error.
# Exit 1 on any problem (usable by a future watcher cron), 0 if all good.
# Usage: gateway-jobs-check.sh [--json]
set -euo pipefail

JSON_OUT=false
[[ "${1:-}" == "--json" ]] && JSON_OUT=true

if ! command -v jq >/dev/null; then
  echo "ERROR: jq not found" >&2
  exit 2
fi

RAW="$(openclaw automations list --json 2>/dev/null)"
if [[ -z "$RAW" ]]; then
  echo "ERROR: could not get automations from gateway" >&2
  exit 2
fi

NOW_MS=$(( $(date +%s) * 1000 ))
PROBLEMS="$(echo "$RAW" | jq -c --argjson now "$NOW_MS" '
  .jobs[]
  | select(
      ((.enabled // true) | not)
      or ((.status // "idle") == "error")
      or (((.state.nextRunAtMs // .nextRunAtMs // 0) != 0) and ((.state.nextRunAtMs // .nextRunAtMs) < ($now - 3600000)))
      or (((.state.nextRunAtMs // .nextRunAtMs // 0) == 0) and ((.schedule.kind // "") != ""))
    )
  | {id: (.declarationKey // .id), name, enabled: (.enabled // true), status: (.status // "unknown"), nextRunAtMs: (.state.nextRunAtMs // .nextRunAtMs), schedule: .schedule.kind}
')"

if $JSON_OUT; then
  echo "$PROBLEMS"
  exit 0
fi

COUNT="$(echo "$PROBLEMS" | jq -s 'length')"
NOW_HUMAN="$(date '+%Y-%m-%d %H:%M:%S')"

if [[ "$COUNT" -gt 0 ]]; then
  echo "[$NOW_HUMAN] PROBLEMS in gateway jobs ($COUNT):"
  echo "$PROBLEMS" | jq -r '"  - \(.id): enabled=\(.enabled) status=\(.status) nextRun=\(.nextRunAtMs // "none") sched=\(.schedule // "none")"'
  exit 1
fi

echo "[$NOW_HUMAN] OK: all gateway jobs healthy"
exit 0