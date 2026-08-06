#!/usr/bin/env bash
# bisect.sh — Automated git bisect with reproduction script
# Usage: ./bisect.sh <good-commit> [repro-script]

set -euo pipefail

GOOD_COMMIT="${1:?Usage: $0 <good-commit> [repro-script]}"
REPRO_SCRIPT="${2:-npm run test -- --run}"

echo "🔍 Starting git bisect..."
echo "   Good commit: $GOOD_COMMIT"
echo "   Bad commit:  HEAD"
echo "   Script:      $REPRO_SCRIPT"
echo ""

# Check for uncommitted changes
if ! git diff --quiet; then
  echo "⚠️  Uncommitted changes detected. Stashing..."
  git stash push -m "bisect-auto-stash"
  STASHED=true
else
  STASHED=false
fi

# Run bisect
git bisect start HEAD "$GOOD_COMMIT"
git bisect run $REPRO_SCRIPT

BISECT_RESULT=$?

# Get the first bad commit
FIRST_BAD=$(git log --format="%H %s" -1 bisect/bad 2>/dev/null || echo "unknown")

# Generate report
echo ""
echo "═══════════════════════════════════════"
echo "  Bisect Results"
echo "═══════════════════════════════════════"
echo "  First bad commit: $FIRST_BAD"
echo ""

# Show diff of the bad commit
git show --stat "$FIRST_BAD" 2>/dev/null || true

# Reset bisect
git bisect reset

# Restore stash if needed
if [[ "$STASHED" == true ]]; then
  git stash pop 2>/dev/null || true
fi

exit $BISECT_RESULT
