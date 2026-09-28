#!/usr/bin/env bash
# test-verify-delegation.sh - Test suite for verify-delegation.sh
#
# Asserts the exit contract: 0 pass, 1 criteria failed, 3 cannot run.
# A test that runs zero cases must fail the suite.

# NOTE: no `set -e`. Cases 2 and 4 expect a non-zero exit from the script
# under test; `set -e` would abort the suite at the first expected failure and
# make it look like the suite passed when it stopped early.

set -uo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
VERIFY="$SCRIPT_DIR/verify-delegation.sh"

checked=0
failed=0

run_test() {
  local name="$1"
  local expected_exit="$2"
  shift 2
  echo "=== test: $name (expect exit $expected_exit) ==="
  local actual=0
  bash "$VERIFY" "$@" || actual=$?
  checked=$((checked + 1))
  if [[ "$actual" -eq "$expected_exit" ]]; then
    echo "PASS (exit=$actual)"
  else
    echo "FAIL (expected $expected_exit, got $actual)"
    failed=$((failed + 1))
  fi
}

WS=$(mktemp -d "${TMPDIR:-/tmp}/verify-delegation-test-XXXXXX") || exit 3
trap 'rm -rf "$WS"' EXIT
cd "$WS" || exit 3

# 1. Exact count matches -> 0
touch a1.txt a2.txt a3.txt
run_test "matching count" 0 '*.txt' 3

# 2. Count mismatch -> 1
run_test "count mismatch" 1 '*.txt' 2

# 3. No artifacts at all -> 3 (zero cases is NOT a pass)
rm -f ./*.txt
run_test "zero artifacts" 3 '*.txt' 0

# 4. Extra command fails -> 1
touch b.txt
run_test "extra command fails" 1 'b.txt' 1 'false'

# 5. Extra command succeeds -> 0
run_test "extra command succeeds" 0 'b.txt' 1 'true'

# 6. Path-shaped pattern is rejected -> 3 (never silently matches nothing)
run_test "path-shaped pattern rejected" 3 'sub/*.md' 1

# 7. Universal pattern is rejected -> 3 (verifies nothing)
run_test "universal pattern rejected" 3 '*' 1

# 8. Pattern with no match -> 3 even when expected is 0
run_test "no match expects zero" 3 'nope-*.md' 0

# A suite that checked nothing cannot pass.
if [[ $checked -eq 0 ]]; then
  echo 'ERROR: no cases ran'
  exit 3
fi

echo "---"
echo "checked: $checked | failed: $failed"
if [[ $failed -ne 0 ]]; then
  exit 1
fi
echo "All tests passed."
exit 0
