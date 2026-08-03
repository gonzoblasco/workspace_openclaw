#!/usr/bin/env bash
# pre-deploy-check.sh — Run all pre-deploy QA checks
# Usage: ./pre-deploy-check.sh [--url <base-url>] [--output <file>]

set -euo pipefail

BASE_URL="${2:-http://localhost:3000}"
OUTPUT="${4:-qa-report-$(date +%Y%m%d-%H%M%S).md}"

echo "🔍 Running pre-deploy QA checks..."
echo ""

cat > "$OUTPUT" << 'HEADER'
# Pre-Deploy QA Report

HEADER
echo "**Date:** $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT"
echo "**URL:** $BASE_URL" >> "$OUTPUT"
echo "" >> "$OUTPUT"

PASS=0
FAIL=0
WARN=0

check() {
  local phase="$1"
  local name="$2"
  shift 2

  echo "  [$phase] $name..."
  if "$@" 2>/dev/null; then
    echo "    ✅ Passed"
    echo "| $phase | $name | 🟢 Pass |" >> "$OUTPUT"
    PASS=$((PASS + 1))
  else
    echo "    ❌ Failed"
    echo "| $phase | $name | 🔴 Fail |" >> "$OUTPUT"
    FAIL=$((FAIL + 1))
  fi
}

echo "## Results" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Phase | Check | Result |" >> "$OUTPUT"
echo "|-------|-------|--------|" >> "$OUTPUT"

build_succeeds() {
  npm run build 2>&1 | tail -3
}

health_endpoint_ok() {
  curl -sf "$BASE_URL/health" > /dev/null
}

homepage_ok() {
  curl -sf "$BASE_URL" > /dev/null
}

sitemap_ok() {
  curl -sf "$BASE_URL/sitemap.xml" > /dev/null
}

auth_session_ok() {
  curl -sf "$BASE_URL/api/auth/session" > /dev/null
}

npm_audit_high() {
  npm audit --audit-level=high 2>&1 | tail -1
}

no_console_logs() {
  ! grep -r 'console\.log' src/ --include='*.ts' --include='*.tsx' 2>/dev/null | grep -v node_modules | head -1
}

# Build
check "Build" "Build succeeds" build_succeeds

# Routes
check "Routes" "Health endpoint" health_endpoint_ok
check "Routes" "Homepage" homepage_ok
check "Routes" "Sitemap" sitemap_ok

# API
check "API" "Auth session" auth_session_ok

# Security
check "Security" "npm audit" npm_audit_high

# Cleanup
check "Cleanup" "No console.log" no_console_logs

echo "" >> "$OUTPUT"
echo "## Summary" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "- 🟢 Passed: $PASS" >> "$OUTPUT"
echo "- 🔴 Failed: $FAIL" >> "$OUTPUT"
echo "" >> "$OUTPUT"

if [[ "$FAIL" -gt 0 ]]; then
  echo "❌ QA FAILED: $FAIL checks failed"
  echo "   Decision: NO-GO"
  echo "🔴 **Decision: NO-GO**" >> "$OUTPUT"
else
  echo "✅ QA PASSED: All checks green"
  echo "   Decision: GO"
  echo "🟢 **Decision: GO**" >> "$OUTPUT"
fi

echo ""
echo "   Report: $OUTPUT"
