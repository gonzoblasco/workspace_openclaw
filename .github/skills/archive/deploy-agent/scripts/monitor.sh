#!/bin/bash
# monitor.sh — Monitorea build en Vercel hasta READY o ERROR
# Uso: ./monitor.sh <deploy-id> [timeout-seconds]
# Output: JSON con estado final

DEPLOY_ID="$1"
TIMEOUT="${2:-300}"  # 5 min default

if [ -z "$DEPLOY_ID" ] || [ -z "$VERCEL_TOKEN" ]; then
  echo '{"status":"error","error":"DEPLOY_ID and VERCEL_TOKEN required"}'
  exit 1
fi

START_TIME=$(date +%s)
TIMEOUT_AT=$((START_TIME + TIMEOUT))

while [ "$(date +%s)" -lt "$TIMEOUT_AT" ]; do
  INSPECT=$(vercel inspect "$DEPLOY_ID" --token "$VERCEL_TOKEN" 2>&1)

  if echo "$INSPECT" | grep -q "Ready"; then
    ELAPSED=$(( $(date +%s) - START_TIME ))
    cat <<EOF
{
  "status": "ready",
  "deployId": "$DEPLOY_ID",
  "elapsedSeconds": $ELAPSED
}
EOF
    exit 0
  fi

  if echo "$INSPECT" | grep -q "Error\|Failed\|Cancelled"; then
    ELAPSED=$(( $(date +%s) - START_TIME ))
    INSPECT_ESC=$(echo "$INSPECT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
    cat <<EOF
{
  "status": "error",
  "deployId": "$DEPLOY_ID",
  "elapsedSeconds": $ELAPSED,
  "inspect": $INSPECT_ESC
}
EOF
    exit 1
  fi

  sleep 5
done

cat <<EOF
{
  "status": "timeout",
  "deployId": "$DEPLOY_ID",
  "elapsedSeconds": $TIMEOUT
}
EOF
exit 1
