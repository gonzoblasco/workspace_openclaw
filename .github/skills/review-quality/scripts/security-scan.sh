#!/usr/bin/env bash
# security-scan.sh — Quick security scan of staged changes
# Usage: ./security-scan.sh [--diff]

set -euo pipefail

SCAN_MODE="${1:-}"

echo "🔒 Running security scan..."
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

no_secrets_in_diff() {
  ! git diff --cached | grep -iE '(password|secret|token|api.?key|auth.?token)' | grep -v 'example\|sample\|test' | head -1
}

no_hardcoded_urls_in_diff() {
  ! git diff --cached | grep -E '(localhost|127\.0\.0\.1|0\.0\.0\.0)' | grep -v 'example\|test' | head -1
}

run_npm_audit() {
  npm audit --audit-level=high 2>&1 | tail -1
}

no_secrets_in_src() {
  ! grep -rE '(password|secret|api.?key)' src/ --include='*.ts' --include='*.tsx' --include='*.env' 2>/dev/null | grep -v 'example\|sample\|test\|\.env\.example' | head -1
}

no_eval_in_src() {
  ! grep -r 'eval(' src/ --include='*.ts' --include='*.tsx' --include='*.js' 2>/dev/null | head -1
}

# Scan staged diff for secrets
if [[ "$SCAN_MODE" == "--diff" ]]; then
  check "No secrets in diff" no_secrets_in_diff
  check "No hardcoded URLs" no_hardcoded_urls_in_diff
else
  # Full scan
  check "npm audit" run_npm_audit
  check "No secrets in src" no_secrets_in_src
  check "No eval" no_eval_in_src
fi

echo ""
echo "✅ Security scan complete: $PASS passed, $FAIL failed"
