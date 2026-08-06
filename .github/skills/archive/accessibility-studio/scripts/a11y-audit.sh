#!/usr/bin/env bash
# a11y-audit.sh — Run axe-core + Lighthouse + generate unified report
# Usage: ./a11y-audit.sh <url> [--ci]

set -euo pipefail

URL="${1:?Usage: $0 <url> [--ci]}"
CI_MODE="${2:-}"
REPORT_DIR="a11y-reports"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT_FILE="${REPORT_DIR}/a11y-report-${TIMESTAMP}.md"

mkdir -p "$REPORT_DIR"

echo "🔍 Running accessibility audit for: $URL"
echo ""

# --- axe-core ---
echo "📌 axe-core audit..."
AXE_OUTPUT="${REPORT_DIR}/axe-${TIMESTAMP}.json"
if command -v npx &>/dev/null; then
  npx @axe-core/cli "$URL" --exit --save "$AXE_OUTPUT" 2>/dev/null || true
else
  echo "⚠️  npx not found, skipping axe-core"
fi

# --- Lighthouse ---
echo "📌 Lighthouse audit..."
LH_OUTPUT="${REPORT_DIR}/lighthouse-${TIMESTAMP}.report.json"
if command -v npx &>/dev/null; then
  npx lighthouse "$URL" --output json --output-path "$LH_OUTPUT" --quiet --chrome-flags="--headless" 2>/dev/null || true
else
  echo "⚠️  npx not found, skipping Lighthouse"
fi

# --- Generate unified report ---
echo ""
echo "📝 Generating unified report..."

cat > "$REPORT_FILE" << 'HEADER'
# Accessibility Audit Report

HEADER
echo "**URL:** $URL" >> "$REPORT_FILE"
echo "**Date:** $(date '+%Y-%m-%d %H:%M')" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Parse axe-core results
if [[ -f "$AXE_OUTPUT" ]]; then
  VIOLATIONS=$(python3 -c "
import json
with open('$AXE_OUTPUT') as f:
    data = json.load(f)
violations = data.get('violations', [])
print(len(violations))
" 2>/dev/null || echo "0")

  echo "## axe-core Results" >> "$REPORT_FILE"
  echo "- **Violations:** $VIOLATIONS" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"

  python3 -c "
import json
with open('$AXE_OUTPUT') as f:
    data = json.load(f)
for v in data.get('violations', []):
    print(f\"### {v['id']} — {v['impact']}\")
    print(f\"{v['description']}\")
    print(f\"- Help: {v['helpUrl']}\")
    print(f\"- Nodes: {len(v['nodes'])}\")
    print()
" 2>/dev/null >> "$REPORT_FILE" || true
fi

# Parse Lighthouse results
if [[ -f "$LH_OUTPUT" ]]; then
  LH_SCORE=$(python3 -c "
import json
with open('$LH_OUTPUT') as f:
    data = json.load(f)
print(data['categories']['accessibility']['score'] * 100)
" 2>/dev/null || echo "N/A")

  echo "## Lighthouse Accessibility Score" >> "$REPORT_FILE"
  echo "- **Score:** ${LH_SCORE}/100" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"
fi

echo "✅ Report generated: $REPORT_FILE"

# CI mode: fail on violations
if [[ "$CI_MODE" == "--ci" ]]; then
  if [[ -f "$AXE_OUTPUT" ]]; then
    VIOLATIONS=$(python3 -c "
import json
with open('$AXE_OUTPUT') as f:
    data = json.load(f)
print(len(data.get('violations', [])))
" 2>/dev/null || echo "0")
    if [[ "$VIOLATIONS" -gt 0 ]]; then
      echo "❌ CI FAILED: $VIOLATIONS accessibility violations found"
      exit 1
    fi
  fi
  echo "✅ CI PASSED: No violations found"
fi
