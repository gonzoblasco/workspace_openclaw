#!/usr/bin/env bash
# close-epic.sh — Close epic with CHANGELOG, tags, and lessons
# Usage: ./close-epic.sh --epic E<N> --version <semver>

set -euo pipefail

EPIC=""
VERSION=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --epic) EPIC="$2"; shift 2 ;;
    --version) VERSION="$2"; shift 2 ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

if [[ -z "$EPIC" || -z "$VERSION" ]]; then
  echo "Usage: $0 --epic E<N> --version <semver>"
  exit 1
fi

echo "🔖 Closing epic: $EPIC"
echo ""

# Update CHANGELOG
if [[ -f "CHANGELOG.md" ]]; then
  DATE=$(date '+%Y-%m-%d')
  sed -i.bak "s/\[Unreleased\]/[$VERSION] - $DATE/" CHANGELOG.md 2>/dev/null || true
  rm -f CHANGELOG.md.bak
  echo "✅ CHANGELOG updated to v$VERSION"
fi

# Create tag
git tag -a "$EPIC-complete" -m "Epic $EPIC completed in v$VERSION"
echo "✅ Tag created: $EPIC-complete"

# Update STATUS
if [[ -f "STATUS.md" ]]; then
  cat >> "STATUS.md" << STATUS

## Epic $EPIC — Completed $DATE
- **Version:** $VERSION
- **Tasks:** [list]
- **Lessons learned:**
  1.
  2.
STATUS
  echo "✅ STATUS.md updated"
fi

echo ""
echo "✅ Epic $EPIC closed"
echo "   Version: $VERSION"
echo "   Tag: $EPIC-complete"
echo ""
echo "📋 Don't forget to:"
echo "   1. Push tags: git push --tags"
echo "   2. Update ROADMAP.md"
echo "   3. Archive completed tasks"
