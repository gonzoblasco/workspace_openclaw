#!/bin/bash
# rollback.sh — Rollback al último deploy bueno en Vercel
# Uso: ./rollback.sh [deploy-id]
# Si no se pasa deploy-id, usa el último deploy conocido bueno

TARGET_DEPLOY="$1"

if [ -z "$VERCEL_TOKEN" ]; then
  echo '{"status":"error","error":"VERCEL_TOKEN not set"}'
  exit 1
fi

if [ -n "$TARGET_DEPLOY" ]; then
  ROLLBACK_OUTPUT=$(vercel rollback "$TARGET_DEPLOY" --token "$VERCEL_TOKEN" 2>&1)
else
  ROLLBACK_OUTPUT=$(vercel rollback --token "$VERCEL_TOKEN" 2>&1)
fi

ROLLBACK_EXIT=$?
ROLLBACK_ESC=$(echo "$ROLLBACK_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

if [ $ROLLBACK_EXIT -eq 0 ]; then
  cat <<EOF
{
  "status": "success",
  "targetDeploy": "${TARGET_DEPLOY:-latest}",
  "output": $ROLLBACK_ESC
}
EOF
else
  cat <<EOF
{
  "status": "failed",
  "targetDeploy": "${TARGET_DEPLOY:-latest}",
  "output": $ROLLBACK_ESC
}
EOF
fi
