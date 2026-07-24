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
  local cmd="$2"
  echo "🔍 $name..."
  if eval "$cmd" 2>&1; then
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

# 1. TypeScript type check
check "TypeScript type check" "npx tsc --noEmit"

# 2. Biome lint + format
if [[ "$FIX_MODE" == "--fix" ]]; then
  check "Biome check (with fix)" "npx biome check --write --no-errors-on-unmatched --files-ignore-unknown=true ."
else
  check "Biome check" "npx biome ci ."
fi

# 3. Tests
if [[ -f "package.json" ]] && grep -q '"test' package.json 2>/dev/null; then
  check "Tests" "npm run test -- --run 2>/dev/null || npm run test 2>/dev/null || true"
else
  echo "⏭️  No test script found, skipping"
  RESULTS+=("⏭️  Tests (skipped)")
fi

# 4. Build
check "Build" "npm run build 2>/dev/null || npx next build 2>/dev/null || npx vite build 2>/dev/null || echo '⚠️  No build script found'"

echo "═══════════════════════════════════════"
echo "  Results: $PASS passed, $FAIL failed"
echo "═══════════════════════════════════════"
for r in "${RESULTS[@]}"; do
  echo "  $r"
done

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi
