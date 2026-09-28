#!/usr/bin/env bash
# gateway-config-drift.sh - Detect config drift of ~/.openclaw/openclaw.json
# Baseline: ~/.openclaw/gateway-config.baseline (sha256 + timestamp)
# Usage:
#   gateway-config-drift.sh              # check: exit 1 if drift, 0 if clean
#   gateway-config-drift.sh --accept     # accept current config as new baseline
#   gateway-config-drift.sh --json       # machine-readable output
set -euo pipefail

CONFIG="$HOME/.openclaw/openclaw.json"
BASELINE="$HOME/.openclaw/gateway-config.baseline"
NOW="$(date '+%Y-%m-%d %H:%M:%S')"
JSON_OUT=false
ACCEPT=false

for arg in "$@"; do
  case "$arg" in
    --json) JSON_OUT=true ;;
    --accept) ACCEPT=true ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

hash_now() { shasum -a 256 "$CONFIG" | awk '{print $1}'; }

if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: config not found at $CONFIG" >&2
  exit 2
fi

CURRENT="$(hash_now)"

if [[ "$ACCEPT" == true ]]; then
  printf '%s  %s\n' "$CURRENT" "$(date '+%Y-%m-%dT%H:%M:%S%z')" > "$BASELINE"
  echo "[$NOW] Baseline accepted: $CURRENT"
  exit 0
fi

if [[ ! -f "$BASELINE" ]]; then
  echo "[$NOW] No baseline found. Creating one from current config: $CURRENT"
  printf '%s  %s\n' "$CURRENT" "$(date '+%Y-%m-%dT%H:%M:%S%z')" > "$BASELINE"
  exit 0
fi

EXPECTED="$(awk '{print $1}' "$BASELINE")"
if [[ "$CURRENT" == "$EXPECTED" ]]; then
  $JSON_OUT && echo '{"drift":false,"hash":"'$CURRENT'"}' || echo "[$NOW] OK: no config drift ($CURRENT)"
  exit 0
fi

if $JSON_OUT; then
  echo '{"drift":true,"expected":"'$EXPECTED'","current":"'$CURRENT'"}'
else
  echo "[$NOW] DRIFT: config changed since baseline."
  echo "  expected: $EXPECTED"
  echo "  current:  $CURRENT"
  echo "  If this change is expected: $0 --accept"
fi
exit 1