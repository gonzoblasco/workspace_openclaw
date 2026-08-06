#!/usr/bin/env bash
# reproduce-check.sh — Verify reproduction steps from DEBUG_REPORT.md
# Usage: ./reproduce-check.sh <debug-report>

set -euo pipefail

REPORT="${1:?Usage: $0 <debug-report>}"

if [[ ! -f "$REPORT" ]]; then
  echo "❌ Report not found: $REPORT"
  exit 1
fi

echo "🔍 Verifying reproduction steps from: $REPORT"
echo ""

# Extract reproduction steps from the report
# Look for "## Reproduction" or "## Steps to Reproduce" sections
STEPS=$(sed -n '/^## Reproduction/,/^## /p' "$REPORT" | grep -E '^[0-9]+\.' || true)

if [[ -z "$STEPS" ]]; then
  echo "⚠️  No numbered reproduction steps found in report"
  echo "   Looking for: '## Reproduction' section with numbered steps"
  exit 1
fi

echo "📋 Reproduction steps found:"
echo "$STEPS" | while IFS= read -r step; do
  echo "   $step"
done
echo ""

# Check if there's a reproduction script referenced
REPRO_SCRIPT=$(grep -E 'repro(duce)?\.(sh|js|ts|mjs)' "$REPORT" | head -1 || true)

if [[ -n "$REPRO_SCRIPT" ]]; then
  echo "📌 Reproduction script referenced: $REPRO_SCRIPT"
  if [[ -f "$REPRO_SCRIPT" ]]; then
    echo "   ✅ Script exists"
    echo "   Running..."
    bash "$REPRO_SCRIPT" && echo "   ✅ Reproduction successful" || echo "   ❌ Reproduction failed"
  else
    echo "   ⚠️  Script not found at path"
  fi
else
  echo "⚠️  No reproduction script referenced in report"
  echo "   Consider adding a script for automated reproduction"
fi

echo ""
echo "✅ Verification complete"
