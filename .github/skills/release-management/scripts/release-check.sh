#!/usr/bin/env bash
# release-check.sh — Verify release readiness
# Usage: ./release-check.sh --version <semver>

set -euo pipefail

VERSION=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version) VERSION="$2"; shift 2 ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 --version <semver>"
  exit 1
fi

echo "🔍 Checking release readiness for v$VERSION..."
echo ""

PASS=***
FAIL=0

check() {
  local name="$1"
  local cmd="$2"
  
  echo "  $name..."
  if eval "$cmd" 2>/dev/null; then
    echo "    ✅ Passed"
    PASS=*** + 1))
  else
    echo "    ❌ Failed"
    FAIL=$((FAIL + 1))
  fi
}

# Readiness checks
check "Build passes" "npm run build 2>&1 | tail -1"
check "Tests pass" "npm test -- --run 2>&1 | tail -3"
check "CHANGELOG has version" "grep -q \"## \[$VERSION\]\" CHANGELOG.md 2>/dev/null"
check "Git tag doesn't exist" "! git tag | grep -q \"v$VERSION\"" || true
check "No uncommitted changes" "git diff --quiet"

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "✅ All checks passed! Ready to release v$VERSION"
else
  echo "❌ $FAIL checks failed. Fix before releasing."
  exit 1
fi
