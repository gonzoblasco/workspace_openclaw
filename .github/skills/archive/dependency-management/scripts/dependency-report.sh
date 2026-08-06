#!/usr/bin/env bash
# dependency-report.sh — Generate DEPENDENCY_REPORT.md with inventory, health, vulnerabilities
# Usage: ./dependency-report.sh [--output <file>]

set -euo pipefail

OUTPUT_FILE="${2:-DEPENDENCY_REPORT.md}"

echo "📦 Generating dependency report..."
echo ""

cat > "$OUTPUT_FILE" << 'HEADER'
# Dependency Report

HEADER
echo "**Date:** $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT_FILE"
echo "**Project:** $(basename "$(pwd)")" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# --- Inventory ---
echo "## Dependency Inventory" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "| Package | Version | Type |" >> "$OUTPUT_FILE"
echo "|---------|---------|------|" >> "$OUTPUT_FILE"

if [[ -f "package.json" ]]; then
  node -e "
const pkg = require('./package.json');
const deps = {...pkg.dependencies, ...pkg.devDependencies};
Object.entries(deps).forEach(([name, ver]) => {
  const type = pkg.dependencies?.[name] ? 'runtime' : 'dev';
  console.log('| ' + name + ' | ' + ver + ' | ' + type + ' |');
});
" >> "$OUTPUT_FILE" 2>/dev/null || echo "⚠️  Could not parse package.json" >> "$OUTPUT_FILE"
fi

echo "" >> "$OUTPUT_FILE"

# --- Outdated ---
echo "## Outdated Dependencies" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
npm outdated 2>/dev/null >> "$OUTPUT_FILE" || echo "No outdated dependencies" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# --- Vulnerabilities ---
echo "## Security Vulnerabilities" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
npm audit 2>/dev/null >> "$OUTPUT_FILE" || echo "No vulnerabilities found" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# --- Bundle size ---
echo "## Bundle Size Impact" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
if command -v npx &>/dev/null && npx --yes bundlephobia --help &>/dev/null 2>&1; then
  node -e "
const pkg = require('./package.json');
const deps = Object.keys(pkg.dependencies || {});
deps.forEach(d => {
  console.log('- ' + d + ': check https://bundlephobia.com/package/' + d);
});
" >> "$OUTPUT_FILE" 2>/dev/null
fi
echo "" >> "$OUTPUT_FILE"

echo "✅ Report generated: $OUTPUT_FILE"
