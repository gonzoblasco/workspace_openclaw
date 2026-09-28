#!/usr/bin/env bash
set -euo pipefail

# Validation script for kanam-spec-v2 specifications.
# Checks that each spec markdown file under projects/kanam-spec-v2/specs
# contains required metadata and sections.

SPEC_DIR="projects/kanam-spec-v2/specs"
FAIL=0

for file in "$SPEC_DIR"/*.md; do
  echo "Validating $file"
  # ---- Mandatory metadata ----
  if ! grep -qE '^#\s+kanam-spec' "$file"; then
    echo "::error file=$file::Missing top-level title '# kanam-spec'"
    FAIL=1
  fi
  if ! grep -qE '^\*\*ID:\*\*' "$file"; then
    echo "::error file=$file::Missing **ID:** metadata"
    FAIL=1
  fi
  if ! grep -qE '^\*\*Title:\*\*' "$file"; then
    echo "::error file=$file::Missing **Title:** metadata"
    FAIL=1
  fi
  if ! grep -qE '^\*\*Owner:\*\*' "$file"; then
    echo "::error file=$file::Missing **Owner:** metadata"
    FAIL=1
  fi
  # ---- Required sections ----
  if ! grep -qE '^##\s+Acceptance Criteria' "$file"; then
    echo "::error file=$file::Missing ## Acceptance Criteria section"
    FAIL=1
  fi
  if ! grep -qE '^##\s+Edge Cases \& Error Handling' "$file"; then
    echo "::error file=$file::Missing ## Edge Cases & Error Handling section"
    FAIL=1
  fi
  if ! grep -qE '^##\s+Verification Plan' "$file"; then
    echo "::error file=$file::Missing ## Verification Plan section"
    FAIL=1
  fi
done

if [ $FAIL -ne 0 ]; then
  echo "::error ::Spec validation failed"
  exit 1
fi

echo "All specs passed validation."

