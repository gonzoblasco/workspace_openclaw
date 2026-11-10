#!/usr/bin/env bash
# gateway-audit.sh - Full gateway operations snapshot.
# Combines: gateway reachability, channel status, automations/jobs, config drift,
# and the nativo `openclaw doctor --lint` health check (A3, 2026-10-12).
# Usage: gateway-audit.sh [--json]
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
JSON_OUT=false
[[ "${1:-}" == "--json" ]] && JSON_OUT=true
NOW="$(date '+%Y-%m-%d %H:%M:%S')"

# A3 (2026-10-12): usar el health-check NATIVO de OpenClaw (`doctor --lint`) en vez
# de escribir un auditor propio (el curso reinventa uno en su L10). Read-only:
# `--lint` no repara ni pide credenciales. Ojo: `doctor --lint --json` sale con
# exit != 0 cuando hay findings (ok:false), asi que NO se usa `|| fallback` con
# `set -e` (eso agregaria un segundo JSON vacio). Se captura la salida y se valida.
doctor_json() {
  local out
  out="$(timeout 90 openclaw doctor --lint --json 2>/dev/null)" || true
  if printf '%s' "$out" | jq -e . >/dev/null 2>&1; then
    printf '%s' "$out"
  else
    echo '{"ok":null,"checksRun":null,"findings":[],"note":"doctor no disponible"}'
  fi
}

if $JSON_OUT; then
  jobs_json="$(bash "$DIR/gateway-jobs-check.sh" --json | jq -s '.')"
  drift_json="$(bash "$DIR/gateway-config-drift.sh" --json || true)"
  doctor="$(doctor_json)"
  jq -n \
    --arg ts "$NOW" \
    --argjson jobs "$jobs_json" \
    --argjson drift "$drift_json" \
    --argjson doctor "$doctor" \
    '{timestamp: $ts, jobs: $jobs, configDrift: $drift, doctor: $doctor}'
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

echo "--- Bind ---"
bash "$DIR/gateway-bind-check.sh" || true
echo ""

echo "--- Jobs ---"
bash "$DIR/gateway-jobs-check.sh" || true
echo ""

echo "--- Config drift ---"
bash "$DIR/gateway-config-drift.sh" || true
echo ""

echo "--- Health check (openclaw doctor --lint) ---"
doctor_json | jq -r '
  if (.findings | type) != "array" then "   (doctor: sin datos)"
  elif (.findings | length) == 0 then "   OK: sin findings (checksRun=" + (.checksRun|tostring) + ")"
  else (.findings[] | "   [" + (.severity // "?") + "] " + .checkId + ": " + .message) end
' 2>/dev/null || echo "   (doctor: sin datos)"