#!/bin/bash
# validate.sh — Corre el auto-validation loop
# Uso: ./validate.sh <repo-path> [build-command] [test-command]
# Output: JSON con { build, tests, status }

REPO_PATH="$1"
BUILD_CMD="${2:-npm run build}"
TEST_CMD="${3:-npx vitest run}"

if [ -z "$REPO_PATH" ]; then
  echo '{"status":"error","error":"REPO_PATH required"}'
  exit 1
fi

cd "$REPO_PATH" || {
  echo "{\"status\":\"error\",\"error\":\"REPO_PATH not found: $REPO_PATH\"}"
  exit 1
}

# Build
BUILD_OUTPUT=$(eval "$BUILD_CMD" 2>&1)
BUILD_EXIT=$?

# Tests
TEST_OUTPUT=$(eval "$TEST_CMD" 2>&1)
TEST_EXIT=$?

# Escape outputs for JSON
BUILD_ESC=$(echo "$BUILD_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
TEST_ESC=$(echo "$TEST_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

if [ $BUILD_EXIT -eq 0 ] && [ $TEST_EXIT -eq 0 ]; then
  STATUS="passed"
elif [ $BUILD_EXIT -ne 0 ]; then
  STATUS="build_failed"
else
  STATUS="tests_failed"
fi

cat <<EOF
{
  "status": "$STATUS",
  "build": {"exitCode": $BUILD_EXIT, "output": $BUILD_ESC},
  "tests": {"exitCode": $TEST_EXIT, "output": $TEST_ESC}
}
EOF
