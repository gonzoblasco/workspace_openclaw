#!/usr/bin/env bash
# diagnose-codebase.sh — Quick scan for technical debt in generated code
# Usage: ./diagnose-codebase.sh [--dir <src-dir>] [--output <file>]

set -euo pipefail

SRC_DIR="${2:-src}"
OUTPUT="${4:-diagnosis-$(date +%Y%m%d-%H%M%S).md}"

if [[ ! -d "$SRC_DIR" ]]; then
  echo "❌ Source directory not found: $SRC_DIR"
  exit 1
fi

echo "🔍 Diagnosing codebase: $SRC_DIR"
echo ""

cat > "$OUTPUT" << 'HEADER'
# Codebase Diagnosis Report

HEADER
echo "**Date:** $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT"
echo "**Source:** $SRC_DIR" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# File counts
TS_FILES=$(find "$SRC_DIR" -name "*.ts" -o -name "*.tsx" 2>/dev/null | wc -l | tr -d ' ')
TOTAL_LINES=$(find "$SRC_DIR" -name "*.ts" -o -name "*.tsx" -exec cat {} + 2>/dev/null | wc -l | tr -d ' ')

echo "## Overview" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "- **TypeScript files:** $TS_FILES" >> "$OUTPUT"
echo "- **Total lines:** $TOTAL_LINES" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Red flags
echo "## Red Flags" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Issue | Count | Severity |" >> "$OUTPUT"
echo "|-------|-------|----------|" >> "$OUTPUT"

check_issue() {
  local name="$1"
  local pattern="$2"
  local severity="$3"
  local count=$(grep -r "$pattern" "$SRC_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')
  echo "| $name | $count | $severity |" >> "$OUTPUT"
  echo "$count"
}

ANY_COUNT=$(check_issue "any types" '\bany\b' "🔴 High")
CONSOLE_COUNT=$(check_issue "console.log" 'console\.log' "🟢 Low")
TODO_COUNT=$(check_issue "TODOs/FIXMEs" 'TODO\|FIXME' "🟡 Medium")
SECRETS_COUNT=$(check_issue "Potential secrets" 'password\|secret\|api_key\|auth_token' "🔴 High")
EVAL_COUNT=$(check_issue "eval() usage" '\beval\b' "🔴 High")

echo "" >> "$OUTPUT"

# Long functions
echo "## Long Functions (>150 lines)" >> "$OUTPUT"
echo "" >> "$OUTPUT"
find "$SRC_DIR" -name "*.ts" -o -name "*.tsx" -exec awk '
  /function |=> {/ { start=NR }
  NR > start && /^}/ { if (NR - start > 150) print FILENAME ":" start }
' {} + 2>/dev/null >> "$OUTPUT" || echo "None found" >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "## Recommendations" >> "$OUTPUT"
echo "" >> "$OUTPUT"

if [[ "$ANY_COUNT" -gt 0 ]]; then
  echo "- 🔴 Replace $ANY_COUNT \`any\` types with explicit types" >> "$OUTPUT"
fi
if [[ "$SECRETS_COUNT" -gt 0 ]]; then
  echo "- 🔴 Remove $SECRETS_COUNT potential secrets from source" >> "$OUTPUT"
fi
if [[ "$TODO_COUNT" -gt 0 ]]; then
  echo "- 🟡 Resolve $TODO_COUNT TODOs/FIXMEs" >> "$OUTPUT"
fi
if [[ "$CONSOLE_COUNT" -gt 0 ]]; then
  echo "- 🟢 Remove $CONSOLE_COUNT console.log statements" >> "$OUTPUT"
fi

echo "" >> "$OUTPUT"
echo "✅ Diagnosis complete: $OUTPUT"
