#!/usr/bin/env bash
# security-scan.sh — Quick security scan of staged changes
# Usage: ./security-scan.sh [--diff]

set -euo pipefail

SCAN_MODE="${1:-}"

echo "🔒 Running security scan..."
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

# Scan staged diff for secrets
if [[ "$SCAN_MODE" == "--diff" ]]; then
  DIFF=$(git diff --cached)
  
  check "No secrets in diff" "! echo \"$DIFF\" | grep -iE '(password|secret|token|api.?key|auth.?token)' | grep -v 'example\|sample\|test' | head -1"
  
  check "No hardcoded URLs" "! echo \"$DIFF\" | grep -E '(localhost|127\.0\.0\.1|0\.0\.0\.0)' | grep -v 'example\|test' | head -1"
else
  # Full scan
  check "npm audit" "npm audit --audit-level=high 2>&1 | tail -1"
  
  check "No secrets in src" "! grep -rE '(password|secret|api.?key)' src/ --include='*.ts' --include='*.tsx' --include='*.env' 2>/dev/null | grep -v 'example\|sample\|test\|\.env\.example' | head -1"
  
  check "No eval" "! grep -r 'eval(' src/ --include='*.ts' --include='*.tsx' --include='*.js' 2>/dev/null | head -1"
fi

echo ""
echo "✅ Security scan complete: $PASS passed, $FAIL failed"
