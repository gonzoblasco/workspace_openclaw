#!/bin/bash
# test-skills.sh — Syntax check for all skill scripts
#
# Usage:
#   ./scripts/test-skills.sh
#   ./scripts/test-skills.sh --verbose
#
# Checks:
#   - bash -n on every skills/*/scripts/*.sh
#   - python3 -m py_compile on every skills/*/scripts/*.py

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${WORKSPACE_DIR}/skills"
VERBOSE=0

if [[ "${1:-}" == "--verbose" || "${1:-}" == "-v" ]]; then
  VERBOSE=1
fi

BASH_OK=0
BASH_FAIL=0
PYTHON_OK=0
PYTHON_FAIL=0

failures=()

while IFS= read -r -d '' file; do
  if bash -n "$file" 2>/tmp/bash.err; then
    BASH_OK=$((BASH_OK + 1))
    [[ $VERBOSE -eq 1 ]] && echo "  ✅ bash OK: $file"
  else
    BASH_FAIL=$((BASH_FAIL + 1))
    echo "  ❌ bash FAIL: $file"
    sed 's/^/      /' /tmp/bash.err
    failures+=("$file")
  fi
done < <(find "$SKILLS_DIR" -type f -name "*.sh" -not -path "*/node_modules/*" -print0)

while IFS= read -r -d '' file; do
  if python3 -m py_compile "$file" 2>/tmp/python.err; then
    PYTHON_OK=$((PYTHON_OK + 1))
    [[ $VERBOSE -eq 1 ]] && echo "  ✅ python OK: $file"
  else
    PYTHON_FAIL=$((PYTHON_FAIL + 1))
    echo "  ❌ python FAIL: $file"
    sed 's/^/      /' /tmp/python.err
    failures+=("$file")
  fi
done < <(find "$SKILLS_DIR" -type f -name "*.py" -not -path "*/node_modules/*" -print0)

rm -f /tmp/bash.err /tmp/python.err

echo ""
echo "Skill script syntax check complete"
echo "  Bash:  $BASH_OK passed, $BASH_FAIL failed"
echo "  Python: $PYTHON_OK passed, $PYTHON_FAIL failed"

if [[ ${#failures[@]} -gt 0 ]]; then
  echo ""
  echo "Failed files:"
  printf '  - %s\n' "${failures[@]}"
  exit 1
fi

exit 0
