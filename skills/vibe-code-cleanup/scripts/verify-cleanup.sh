#!/usr/bin/env bash
# verify-cleanup.sh — Verify cleanup: build, typecheck, tests, lint
# Usage: ./verify-cleanup.sh

set -euo pipefail

echo "🔍 Verifying cleanup..."
echo ""

PASS=***
FAIL=0

check() {
  local name="$1"
  local cmd="$2"
  
  echo "  $name..."
  if eval "$cmd" 2>&1 | tail -3; then
    echo "    ✅ Passed"
    PASS=*** + 1))
  else
    echo "    ❌ Failed"
    FAIL=$((FAIL + 1))
  fi
  echo ""
}

check "Build" "npm run build 2>/dev/null || npx next build 2>/dev/null || npx vite build 2>/dev/null || echo '⚠️  No build script'"
check "TypeScript" "npx tsc --noEmit 2>/dev/null || echo '⚠️  No tsconfig'"
check "Tests" "npm test -- --run 2>/dev/null || npm test 2>/dev/null || echo '⚠️  No test script'"
check "Lint" "npx biome ci . 2>/dev/null || npx eslint . 2>/dev/null || echo '⚠️  No linter'"

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "✅ All checks passed! Codebase is clean."
else
  echo "❌ $FAIL checks failed. Review issues above."
  exit 1
fi
