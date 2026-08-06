#!/usr/bin/env bash
# a11y-ci.sh — CI accessibility check, fails on critical/major violations
# Usage: ./a11y-ci.sh <url>

set -euo pipefail

URL="${1:?Usage: $0 <url>}"
echo "🔒 CI Accessibility Check: $URL"
echo ""

# Run axe-core with exit on violations
echo "📌 Running axe-core..."
npx @axe-core/cli "$URL" --exit --chromium --tags wcag2a,wcag2aa,wcag22aa 2>&1 || {
  echo "❌ Accessibility violations detected"
  exit 1
}

echo "✅ All accessibility checks passed"
