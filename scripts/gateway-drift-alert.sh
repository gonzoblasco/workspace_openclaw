#!/usr/bin/env bash
set -euo pipefail
OUT=$(~/.openclaw/workspace/scripts/gateway-config-drift.sh 2>&1)
if echo "$OUT" | grep -q "OK: sin drift"; then exit 0; fi
msg="⚠️ Drift detectado en gateway-config. Detalles: $OUT"
openclaw notify telegram --to 7921100122 --message "$msg"
