#!/bin/bash
# bisect.sh — Git bisect wrapper con output JSON
# Uso: ./bisect.sh <repo-path> <good-commit> "<test-command>"
# Output: JSON con { status, firstBadCommit, author, date, message, log }

REPO_PATH="$1"
GOOD_COMMIT="$2"
TEST_COMMAND="$3"

if [ -z "$REPO_PATH" ] || [ -z "$GOOD_COMMIT" ] || [ -z "$TEST_COMMAND" ]; then
  echo '{"status":"error","error":"REPO_PATH, GOOD_COMMIT, and TEST_COMMAND required"}'
  exit 1
fi

cd "$REPO_PATH" || {
  echo "{\"status\":\"error\",\"error\":\"REPO_PATH not found: $REPO_PATH\"}"
  exit 1
}

# Guardar estado actual
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
CURRENT_COMMIT=$(git rev-parse HEAD)

# Asegurar que no hay un bisect en progreso
git bisect reset 2>/dev/null

# Iniciar bisect
git bisect start HEAD "$GOOD_COMMIT" 2>&1

# Ejecutar test en cada paso
git bisect run sh -c "$TEST_COMMAND" 2>&1 | tee /tmp/bisect_output.txt

BISECT_RESULT=$(tail -15 /tmp/bisect_output.txt)

# Extraer el primer commit malo
FIRST_BAD=$(echo "$BISECT_RESULT" | sed -nE 's/([a-f0-9]{7,40}) is the first bad commit.*/\1/p' | head -1)

if [ -n "$FIRST_BAD" ]; then
  AUTHOR=$(git log -1 --format="%an" "$FIRST_BAD" 2>/dev/null)
  DATE=$(git log -1 --format="%ad" "$FIRST_BAD" 2>/dev/null)
  MESSAGE=$(git log -1 --format="%s" "$FIRST_BAD" 2>/dev/null)
  FULL_LOG=$(git log -1 --format="%B" "$FIRST_BAD" 2>/dev/null | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
fi

# Resetear bisect
git bisect reset 2>/dev/null

# Volver al estado original
git checkout "$CURRENT_BRANCH" 2>/dev/null || git checkout "$CURRENT_COMMIT" 2>/dev/null

BISECT_LOG=$(cat /tmp/bisect_output.txt | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
rm -f /tmp/bisect_output.txt

if [ -n "$FIRST_BAD" ]; then
  cat <<EOF
{
  "status": "found",
  "firstBadCommit": "$FIRST_BAD",
  "author": "$AUTHOR",
  "date": "$DATE",
  "message": "$MESSAGE",
  "fullLog": $FULL_LOG,
  "bisectLog": $BISECT_LOG
}
EOF
else
  cat <<EOF
{
  "status": "not_found",
  "bisectLog": $BISECT_LOG
}
EOF
fi
