#!/usr/bin/env bash
# metrics-report.sh — Collect and report key metrics
# Usage: ./metrics-report.sh [--output <file>]

set -euo pipefail

OUTPUT="${2:-metrics-$(date +%Y%m%d-%H%M%S).md}"

echo "📊 Collecting metrics..."
echo ""

cat > "$OUTPUT" << 'HEADER'
# Metrics Report

HEADER
echo "**Date:** $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# --- Git metrics ---
echo "## Git Metrics" >> "$OUTPUT"
echo "" >> "$OUTPUT"

if git rev-parse --git-dir &>/dev/null; then
  # Commit count
  COMMITS=$(git rev-list --count HEAD 2>/dev/null || echo "0")
  echo "- **Total commits:** $COMMITS" >> "$OUTPUT"

  # Branch count
  BRANCHES=$(git branch -r 2>/dev/null | wc -l | tr -d ' ')
  echo "- **Remote branches:** $BRANCHES" >> "$OUTPUT"

  # Recent activity
  RECENT=$(git log --since="7 days ago" --oneline 2>/dev/null | wc -l | tr -d ' ')
  echo "- **Commits (7 days):** $RECENT" >> "$OUTPUT"

  # Contributors
  CONTRIBUTORS=$(git log --format="%an" 2>/dev/null | sort -u | wc -l | tr -d ' ')
  echo "- **Contributors:** $CONTRIBUTORS" >> "$OUTPUT"
fi

echo "" >> "$OUTPUT"

# --- Code metrics ---
echo "## Code Metrics" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# File counts
TS_FILES=$(find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | grep -v node_modules | grep -v ".next" | wc -l | tr -d ' ')
echo "- **TypeScript files:** $TS_FILES" >> "$OUTPUT"

# Test files
TEST_FILES=$(find . -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | grep -v node_modules | wc -l | tr -d ' ')
echo "- **Test files:** $TEST_FILES" >> "$OUTPUT"

# Package size
if [[ -d "node_modules" ]]; then
  MODULES_SIZE=$(du -sh node_modules 2>/dev/null | cut -f1)
  echo "- **node_modules size:** $MODULES_SIZE" >> "$OUTPUT"
fi

echo "" >> "$OUTPUT"

# --- Build metrics ---
echo "## Build Metrics" >> "$OUTPUT"
echo "" >> "$OUTPUT"

if [[ -f "package.json" ]]; then
  # Count dependencies
  DEPS=$(node -e "const p=require('./package.json'); console.log(Object.keys(p.dependencies||{}).length)" 2>/dev/null || echo "0")
  DEV_DEPS=$(node -e "const p=require('./package.json'); console.log(Object.keys(p.devDependencies||{}).length)" 2>/dev/null || echo "0")
  echo "- **Runtime deps:** $DEPS" >> "$OUTPUT"
  echo "- **Dev deps:** $DEV_DEPS" >> "$OUTPUT"
  echo "- **Total deps:** $((DEPS + DEV_DEPS))" >> "$OUTPUT"
fi

echo "" >> "$OUTPUT"
echo "✅ Metrics collected: $OUTPUT"
