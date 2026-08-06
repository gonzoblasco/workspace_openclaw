#!/bin/bash
# pr.sh — Genera PR description estructurada
# Uso: ./pr.sh <repo-path> <title> <description> <branch>
# Output: JSON con la descripción del PR

REPO_PATH="$1"
TITLE="$2"
DESCRIPTION="$3"
BRANCH="$4"

if [ -z "$REPO_PATH" ] || [ -z "$TITLE" ]; then
  echo '{"status":"error","error":"REPO_PATH and TITLE required"}'
  exit 1
fi

cd "$REPO_PATH" || {
  echo "{\"status\":\"error\",\"error\":\"REPO_PATH not found: $REPO_PATH\"}"
  exit 1
}

# Obtener cambios desde main
CHANGES=$(git log main..HEAD --oneline 2>/dev/null | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
FILES=$(git diff --name-only main..HEAD 2>/dev/null | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

cat <<EOF
{
  "status": "ready",
  "title": "$TITLE",
  "description": "$DESCRIPTION",
  "branch": "${BRANCH:-$(git rev-parse --abbrev-ref HEAD)}",
  "changes": $CHANGES,
  "files": $FILES,
  "prBody": "## Description\\n\\n$DESCRIPTION\\n\\n## Changes\\n\\n$CHANGES\\n\\n## Files\\n\\n$FILES\\n\\n## Checklist\\n- [ ] Build passes\\n- [ ] Tests pass\\n- [ ] Lint passes\\n- [ ] No console.log/debugger"
}
EOF
