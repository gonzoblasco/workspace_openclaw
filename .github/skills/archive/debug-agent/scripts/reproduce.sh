#!/bin/bash
# reproduce.sh — Ejecuta pasos de reproducción y verifica resultado
# Uso: ./reproduce.sh <repo-path> "<comando>" "<expected-output>"
# Output: JSON con { status, output, exitCode, matched }

REPO_PATH="$1"
COMMAND="$2"
EXPECTED="$3"

if [ -z "$REPO_PATH" ] || [ -z "$COMMAND" ]; then
  echo '{"status":"error","error":"REPO_PATH and COMMAND required"}'
  exit 1
fi

cd "$REPO_PATH" || {
  echo "{\"status\":\"error\",\"error\":\"REPO_PATH not found: $REPO_PATH\"}"
  exit 1
}

OUTPUT=$(eval "$COMMAND" 2>&1)
EXIT_CODE=$?

if [ -n "$EXPECTED" ]; then
  if echo "$OUTPUT" | grep -q "$EXPECTED"; then
    MATCHED=true
  else
    MATCHED=false
  fi
else
  MATCHED=null
fi

# Escape for JSON
OUTPUT_ESCAPED=$(echo "$OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

cat <<EOF
{
  "status": "done",
  "exitCode": $EXIT_CODE,
  "matched": $MATCHED,
  "output": $OUTPUT_ESCAPED
}
EOF
