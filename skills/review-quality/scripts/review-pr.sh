#!/usr/bin/env bash
# review-pr.sh — Automated PR review checks
# Usage: ./review-pr.sh [--pr <number>] [--output <file>]

set -euo pipefail

PR_NUMBER="${2:-}"
OUTPUT="${4:-pr-review-$(date +%Y%m%d-%H%M%S).md}"

echo "🔍 Running PR review checks..."
echo ""

cat > "$OUTPUT" << 'HEADER'
# PR Review Report

HEADER
echo "**Date:** $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT"
echo "" >> "$OUTPUT"

PASS=0
FAIL=0

check() {
  local name="$1"
  local cmd="$2"
  
  echo "  $name..."
  if eval "$cmd" 2>/dev/null; then
    echo "    ✅ Passed"
    echo "| $name | 🟢 Pass |" >> "$OUTPUT"
    PASS=$((PASS + 1))
  else
    echo "    ❌ Failed"
    echo "| $name | 🔴 Fail |" >> "$OUTPUT"
    FAIL=$((FAIL + 1))
  fi
}

echo "## Results" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Check | Result |" >> "$OUTPUT"
echo "|-------|--------|" >> "$OUTPUT"

# Build check
check "Build" "npm run build 2>&1 | tail -3"

# Type check
check "TypeScript" "npx tsc --noEmit 2>&1 | tail -3"

# Lint
check "Lint" "npx biome ci . 2>&1 | tail -3"

# Tests
check "Tests" "npm test -- --run 2>&1 | tail -5"

# Console.log check
check "No console.log" "! grep -r 'console\.log' src/ --include='*.ts' --include='*.tsx' 2>/dev/null | grep -v node_modules | head -1"

# TODO check
check "No unresolved TODOs" "! grep -r 'TODO\|FIXME' src/ --include='*.ts' --include='*.tsx' 2>/dev/null | grep -v node_modules | grep -v '// TODO' | head -1"

echo "" >> "$OUTPUT"
echo "## Summary" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "- 🟢 Passed: $PASS" >> "$OUTPUT"
echo "- 🔴 Failed: $FAIL" >> "$OUTPUT"
echo "" >> "$OUTPUT"

echo ""
echo "✅ Review complete: $PASS passed, $FAIL failed"
echo "   Report: $OUTPUT"
