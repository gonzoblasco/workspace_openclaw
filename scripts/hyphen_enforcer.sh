#!/usr/bin/env bash
# hyphen_enforcer.sh – replace en‑dash (U+2013) with hyphen (-) in markdown/spec files
# Usage: ./scripts/hyphen_enforcer.sh [paths...]
# If no paths are given, it scans the entire workspace for *.md and *.spec files.

set -euo pipefail

# Find files to process
if [[ $# -gt 0 ]]; then
  FILES=($@)
else
  # Search for markdown and spec files, ignoring binaries and vendor dirs
  mapfile -t FILES < <(git ls-files "*.md" "*.spec" "*.txt" 2>/dev/null || true)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No markdown/spec files found to process."
  exit 0
fi

EN_DASH=$'\u2013'
HYPHEN='-'

for f in "${FILES[@]}"; do
  if [[ -f $f ]]; then
    # Only replace if the file contains the en‑dash
    if grep -q "$EN_DASH" "$f"; then
      echo "Replacing en‑dash in $f"
      # Use perl for Unicode safe replacement
      perl -i -pe "s/\x{2013}/$HYPHEN/g" "$f"
    fi
  fi
done

echo "Hyphen enforcement completed."
