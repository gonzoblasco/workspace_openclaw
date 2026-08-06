#!/bin/bash
# validate.sh — Pre-deploy validation: build + tests + types + lint
# Uso: ./validate.sh <repo-path>
# Output: JSON con resultados

REPO_PATH="$1"

if [ -z "$REPO_PATH" ]; then
  echo '{"status":"error","error":"REPO_PATH required"}'
  exit 1
fi

cd "$REPO_PATH" || {
  echo "{\"status\":\"error\",\"error\":\"REPO_PATH not found: $REPO_PATH\"}"
  exit 1
}

RESULTS="["

# Build
BUILD_OUTPUT=$(npm run build 2>&1)
BUILD_EXIT=$?
BUILD_ESC=$(echo "$BUILD_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
if [ $BUILD_EXIT -eq 0 ]; then
  RESULTS+="{\"step\":\"build\",\"status\":\"pass\"}"
else
  RESULTS+="{\"step\":\"build\",\"status\":\"fail\",\"output\":$BUILD_ESC}"
fi

# Tests
TEST_OUTPUT=$(npx vitest run 2>&1)
TEST_EXIT=$?
TEST_ESC=$(echo "$TEST_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
if [ $TEST_EXIT -eq 0 ]; then
  RESULTS+=",{\"step\":\"tests\",\"status\":\"pass\"}"
else
  RESULTS+=",{\"step\":\"tests\",\"status\":\"fail\",\"output\":$TEST_ESC}"
fi

# Types
TYPES_OUTPUT=$(npx tsc --noEmit 2>&1)
TYPES_EXIT=$?
TYPES_ESC=$(echo "$TYPES_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
if [ $TYPES_EXIT -eq 0 ]; then
  RESULTS+=",{\"step\":\"types\",\"status\":\"pass\"}"
else
  RESULTS+=",{\"step\":\"types\",\"status\":\"fail\",\"output\":$TYPES_ESC}"
fi

# Lint
LINT_OUTPUT=$(npx biome check 2>&1)
LINT_EXIT=$?
LINT_ESC=$(echo "$LINT_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
if [ $LINT_EXIT -eq 0 ]; then
  RESULTS+=",{\"step\":\"lint\",\"status\":\"pass\"}"
else
  RESULTS+=",{\"step\":\"lint\",\"status\":\"fail\",\"output\":$LINT_ESC}"
fi

RESULTS+="]"

# Overall
OVERALL="pass"
if echo "$RESULTS" | grep -q "\"status\":\"fail\""; then
  OVERALL="fail"
fi

cat <<EOF
{
  "status": "$OVERALL",
  "results": $RESULTS
}
EOF
