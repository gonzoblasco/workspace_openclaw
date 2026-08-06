#!/usr/bin/env bash
# health-check.sh — Run health checks on all layers
# Usage: ./health-check.sh [--url <base-url>] [--output <file>]

set -euo pipefail

BASE_URL="${2:-http://localhost:3000}"
OUTPUT="${4:-health-check-$(date +%Y%m%d-%H%M%S).md}"

echo "🏥 Running health checks..."
echo ""

cat > "$OUTPUT" << 'HEADER'
# Health Check Report

HEADER
echo "**Date:** $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT"
echo "**Base URL:** $BASE_URL" >> "$OUTPUT"
echo "" >> "$OUTPUT"

PASS=0
FAIL=0

check_endpoint() {
  local name="$1"
  local url="$2"
  local expected="${3:-200}"

  echo "🔍 $name..."
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null || echo "000")

  if [[ "$STATUS" == "$expected" ]]; then
    echo "   ✅ $STATUS"
    echo "| $name | 🟢 $STATUS |" >> "$OUTPUT"
    PASS=$((PASS + 1))
  else
    echo "   ❌ Got $STATUS, expected $expected"
    echo "| $name | 🔴 $STATUS (expected $expected) |" >> "$OUTPUT"
    FAIL=$((FAIL + 1))
  fi
}

echo "## Endpoint Health" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Endpoint | Status |" >> "$OUTPUT"
echo "|----------|--------|" >> "$OUTPUT"

# Common health endpoints
check_endpoint "Health" "$BASE_URL/health"
check_endpoint "API" "$BASE_URL/api/health"
check_endpoint "Root" "$BASE_URL/"

# Check response time
echo ""
echo "## Response Times" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Endpoint | Time |" >> "$OUTPUT"
echo "|----------|------|" >> "$OUTPUT"

for endpoint in "/health" "/api/health" "/"; do
  TIME=$(curl -s -o /dev/null -w "%{time_total}" --max-time 10 "$BASE_URL$endpoint" 2>/dev/null || echo "0")
  echo "| $endpoint | ${TIME}s |" >> "$OUTPUT"
done

echo "" >> "$OUTPUT"
echo "## Summary" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "- ✅ Passed: $PASS" >> "$OUTPUT"
echo "- ❌ Failed: $FAIL" >> "$OUTPUT"
echo "" >> "$OUTPUT"

echo ""
echo "✅ Health check complete: $PASS passed, $FAIL failed"
echo "   Report: $OUTPUT"
