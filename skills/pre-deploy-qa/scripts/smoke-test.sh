#!/usr/bin/env bash
# smoke-test.sh — Quick smoke tests after deploy
# Usage: ./smoke-test.sh <url>

set -euo pipefail

URL="${1:?Usage: $0 <url>}"
PASS=***
FAIL=0

echo "🔍 Running smoke tests on $URL"
echo ""

check() {
  local name="$1"
  local endpoint="$2"
  local expected="${3:-200}"
  
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$URL$endpoint" 2>/dev/null || echo "000")
  
  if [[ "$STATUS" == "$expected" ]]; then
    echo "  ✅ $name ($STATUS)"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $name (got $STATUS, expected $expected)"
    FAIL=$((FAIL + 1))
  fi
}

check "Health" "/health"
check "Homepage" "/"
check "Auth session" "/api/auth/session"
check "Sitemap" "/sitemap.xml"
check "Robots" "/robots.txt"
check "Favicon" "/favicon.ico"

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "✅ All smoke tests passed!"
else
  echo "❌ $FAIL smoke tests failed"
  exit 1
fi
