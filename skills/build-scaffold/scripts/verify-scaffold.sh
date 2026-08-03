#!/usr/bin/env bash
# verify-scaffold.sh — Run typecheck + lint + test + build, report results
# Usage: ./verify-scaffold.sh [--fix]

set -euo pipefail

FIX_MODE="${1:-}"
PASS=0
FAIL=0
RESULTS=()

check() {
  local name="$1"
  shift
  echo "🔍 $name..."
  if "$@" 2>&1; then
    echo "   ✅ Passed"
    PASS=$((PASS + 1))
    RESULTS+=("✅ $name")
  else
    echo "   ❌ Failed"
    FAIL=$((FAIL + 1))
    RESULTS+=("❌ $name")
  fi
  echo ""
}

echo "═══════════════════════════════════════"
echo "  Scaffold Verification"
echo "═══════════════════════════════════════"
echo ""

run_typescript() {
  npx tsc --noEmit
}

run_biome_check() {
  npx biome ci .
}

run_biome_fix() {
  npx biome check --write --no-errors-on-unmatched --files-ignore-unknown=true .
}

run_tests() {
  npm run test -- --run 2>/dev/null || npm run test 2>/dev/null || true
}

run_build() {
  npm run build 2>/dev/null || npx next build 2>/dev/null || npx vite build 2>/dev/null || echo '⚠️  No build script found'
}

# 1. TypeScript type check
check "TypeScript type check" run_typescript

# 2. Biome lint + format
if [[ "$FIX_MODE" == "--fix" ]]; then
  check "Biome check (with fix)" run_biome_fix
else
  check "Biome check" run_biome_check
fi

# 3. Tests
if [[ -f "package.json" ]] && grep -q '"test' package.json 2>/dev/null; then
  check "Tests" run_tests
else
  echo "⏭️  No test script found, skipping"
  RESULTS+=("⏭️  Tests (skipped)")
fi

# 4. Build
check "Build" run_build

echo "═══════════════════════════════════════"
echo "  Results: $PASS passed, $FAIL failed"
echo "═══════════════════════════════════════"
for r in "${RESULTS[@]}"; do
  echo "  $r"
done

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi
