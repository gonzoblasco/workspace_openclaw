#!/bin/bash
# deploy.sh — Deploy a Vercel
# Uso: ./deploy.sh <environment> [repo-path]
# environment: "preview" | "production"

ENV="${1:-preview}"
REPO_PATH="${2:-.}"

cd "$REPO_PATH" || {
  echo "{\"status\":\"error\",\"error\":\"REPO_PATH not found: $REPO_PATH\"}"
  exit 1
}

if [ -z "$VERCEL_TOKEN" ]; then
  echo '{"status":"error","error":"VERCEL_TOKEN not set"}'
  exit 1
fi

if [ "$ENV" = "production" ]; then
  DEPLOY_OUTPUT=$(vercel --prod --token "$VERCEL_TOKEN" 2>&1)
else
  DEPLOY_OUTPUT=$(vercel --token "$VERCEL_TOKEN" 2>&1)
fi

DEPLOY_EXIT=$?
DEPLOY_ESC=$(echo "$DEPLOY_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

# Extract deploy URL and ID
DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -oP 'https://[a-zA-Z0-9.-]+\.vercel\.app' | head -1)
DEPLOY_ID=$(echo "$DEPLOY_OUTPUT" | grep -oP 'dpl_[a-zA-Z0-9]+' | head -1)

if [ $DEPLOY_EXIT -eq 0 ] && [ -n "$DEPLOY_URL" ]; then
  cat <<EOF
{
  "status": "deploying",
  "environment": "$ENV",
  "url": "$DEPLOY_URL",
  "deployId": "$DEPLOY_ID",
  "output": $DEPLOY_ESC
}
EOF
else
  cat <<EOF
{
  "status": "failed",
  "environment": "$ENV",
  "error": "Deploy command failed",
  "output": $DEPLOY_ESC
}
EOF
fi
