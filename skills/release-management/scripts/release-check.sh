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

PASS=0
FAIL=0

check() {
  local name="$1"
  shift

  echo "  $name..."
  if "$@" 2>/dev/null; then
    echo "    ✅ Passed"
    PASS=$((PASS + 1))
  else
    echo "    ❌ Failed"
    FAIL=$((FAIL + 1))
  fi
}

has_build_output() {
  npm run build 2>&1 | tail -1
}

has_tests_output() {
  npm test -- --run 2>&1 | tail -3
}

has_changelog_version() {
  grep -q "## \[$VERSION\]" CHANGELOG.md 2>/dev/null
}

tag_does_not_exist() {
  ! git tag | grep -q "v$VERSION"
}

no_uncommitted_changes() {
  git diff --quiet
}

# Readiness checks
check "Build passes" has_build_output
check "Tests pass" has_tests_output
check "CHANGELOG has version" has_changelog_version
check "Git tag doesn't exist" tag_does_not_exist
check "No uncommitted changes" no_uncommitted_changes

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "✅ All checks passed! Ready to release v$VERSION"
else
  echo "❌ $FAIL checks failed. Fix before releasing."
  exit 1
fi
