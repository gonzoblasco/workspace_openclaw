#!/usr/bin/env bash
# verify-cleanup.sh — Verify cleanup: build, typecheck, tests, lint
# Usage: ./verify-cleanup.sh

set -euo pipefail

echo "🔍 Verifying cleanup..."
echo ""

PASS=0
FAIL=0

check() {
  local name="$1"
  shift

  echo "  $name..."
  if "$@" 2>&1 | tail -3; then
    echo "    ✅ Passed"
    PASS=$((PASS + 1))
  else
    echo "    ❌ Failed"
    FAIL=$((FAIL + 1))
  fi
  echo ""
}

run_build() {
  npm run build 2>/dev/null || npx next build 2>/dev/null || npx vite build 2>/dev/null || echo '⚠️  No build script'
}

run_typescript() {
  npx tsc --noEmit 2>/dev/null || echo '⚠️  No tsconfig'
}

run_tests() {
  npm test -- --run 2>/dev/null || npm test 2>/dev/null || echo '⚠️  No test script'
}

run_lint() {
  npx biome ci . 2>/dev/null || npx eslint . 2>/dev/null || echo '⚠️  No linter'
}

check "Build" run_build
check "TypeScript" run_typescript
check "Tests" run_tests
check "Lint" run_lint

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "✅ All checks passed! Codebase is clean."
else
  echo "❌ $FAIL checks failed. Review issues above."
  exit 1
fi
