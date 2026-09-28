#!/usr/bin/env bash
# gateway-audit.sh - Full gateway operations snapshot.
# Combines: gateway reachability, channel status, automations/jobs, config drift.
# Usage: gateway-audit.sh [--json]
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
JSON_OUT=false
[[ "${1:-}" == "--json" ]] && JSON_OUT=true
NOW="$(date '+%Y-%m-%d %H:%M:%S')"

if $JSON_OUT; then
  jobs_json="$(bash "$DIR/gateway-jobs-check.sh" --json | jq -s '.')"
  drift_json="$(bash "$DIR/gateway-config-drift.sh" --json || true)"
  jq -n \
    --arg ts "$NOW" \
    --argjson jobs "$jobs_json" \
    --argjson drift "$drift_json" \
    '{timestamp: $ts, jobs: $jobs, configDrift: $drift}'
  exit 0
fi

echo "=== Gateway Audit - $NOW ==="
echo ""
echo "--- Gateway status ---"
openclaw status 2>&1 | grep -E "^│ (Gateway |Gateway service|Heartbeat|Telegram|Channel |Sessions|Memory)" || true
echo ""

echo "--- Channels ---"
openclaw channels status 2>&1 | grep -viE "^Checking|^Tip:|^Config:|^Mode:" || true
echo ""

echo "--- Jobs ---"
bash "$DIR/gateway-jobs-check.sh" || true
echo ""

echo "--- Config drift ---"
bash "$DIR/gateway-config-drift.sh" || true