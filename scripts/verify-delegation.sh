#!/usr/bin/env bash
# verify-delegation.sh - Verify that a pattern matches an expected count of artifacts.
#
# Usage: bash scripts/verify-delegation.sh <pattern> <expected_count> [extra_command]
#
# Exit codes:
#   0 - criteria met (exact count matches, and extra command, if any, succeeded)
#   1 - criteria failed (count mismatch, or extra command failed)
#   3 - could not run (no matching artifacts): zero cases is NOT a pass
#
# Rule: a check that ran nothing must never report success.

# NOTE: no `set -e`. The extra command is EXPECTED to fail in the negative
# case, and `set -e` would abort before its status can be captured.

set -uo pipefail

usage() {
  echo "Usage: $0 <pattern> <expected_count> [extra_command]"
  exit 3
}

if [[ $# -lt 2 ]]; then
  usage
fi

PATTERN="$1"
EXPECTED_COUNT="$2"
EXTRA_CMD="${3-}"

# Collect matches into an array. Read -d '' keeps paths with spaces intact.
MATCHES=()
while IFS= read -r -d '' file; do
  MATCHES+=("$file")
done < <(find . -type f -name "$PATTERN" -print0 2>/dev/null)

COUNT=${#MATCHES[@]}

# Raw evidence first: the paths and the count, always.
printf 'Found %d artifact(s):\n' "$COUNT"
if [[ $COUNT -gt 0 ]]; then
  printf '%s\n' "${MATCHES[@]}"
fi
printf 'Expected count: %s\n' "$EXPECTED_COUNT"

# No matches at all: cannot verify. Distinct, loud code. Never 0.
if [[ $COUNT -eq 0 ]]; then
  echo 'RESULT: cannot run (no matching artifacts)'
  exit 3
fi

# Count must match exactly.
if [[ "$COUNT" -ne "$EXPECTED_COUNT" ]]; then
  echo "RESULT: count mismatch (found $COUNT, expected $EXPECTED_COUNT)"
  exit 1
fi

# Optional extra command. Capture its status without aborting on failure.
if [[ -n $EXTRA_CMD ]]; then
  extra_status=0
  eval "$EXTRA_CMD" || extra_status=$?
  if [[ $extra_status -ne 0 ]]; then
    echo "RESULT: extra command failed (exit $extra_status)"
    exit 1
  fi
fi

echo 'RESULT: pass'
exit 0
