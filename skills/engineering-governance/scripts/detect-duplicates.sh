#!/usr/bin/env bash
# detect-duplicates.sh — Find duplicate checklists, phases, or prompts across skills
# Usage: ./detect-duplicates.sh [--output <file>]

set -euo pipefail

OUTPUT_FILE="${2:-duplicates-report.md}"
SKILLS_DIR="${SKILLS_DIR:-/Users/gonzoblasco/.openclaw/workspace/skills}"

echo "🔍 Scanning for duplicate content across skills..."
echo ""

cat > "$OUTPUT_FILE" << 'HEADER'
# Duplicate Content Report

HEADER
echo "**Date:** $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Extract all section headings from all SKILL.md files
echo "## Shared Section Headings" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "| Heading | Found In |" >> "$OUTPUT_FILE"
echo "|---------|----------|" >> "$OUTPUT_FILE"

# Find headings that appear in multiple skills
declare -A heading_map

for skill_file in "$SKILLS_DIR"/*/SKILL.md; do
  skill_name=$(basename "$(dirname "$skill_file")")
  while IFS= read -r heading; do
    key=$(echo "$heading" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')
    if [[ -n "$key" ]]; then
      heading_map["$key"]="${heading_map[$key]:-}$skill_name, "
    fi
  done < <(grep -E '^## ' "$skill_file" 2>/dev/null || true)
done

# Report duplicates
for key in "${!heading_map[@]}"; do
  skills="${heading_map[$key]}"
  count=$(echo "$skills" | grep -o "," | wc -l | tr -d ' ')
  if [[ "$count" -ge 2 ]]; then
    # Get a sample of original heading text from one of the duplicate skills
    sample_skill=$(echo "$skills" | tr ',' '\n' | sed 's/^ *//;s/ *$//' | grep -v '^$' | head -1)
    heading_text=$(grep -m1 "^## " "$SKILLS_DIR/$sample_skill/SKILL.md" 2>/dev/null | sed 's/^## //' | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z' || true)
    if [[ -z "$heading_text" ]]; then
      heading_text="$key"
    fi
    echo "| $heading_text | ${skills%, } |" >> "$OUTPUT_FILE"
  fi
done

echo "" >> "$OUTPUT_FILE"

# Check for duplicate checklist items
echo "## Shared Checklist Items" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

declare -A checklist_map

for skill_file in "$SKILLS_DIR"/*/SKILL.md; do
  skill_name=$(basename "$(dirname "$skill_file")")
  while IFS= read -r line; do
    item=$(echo "$line" | sed 's/^- \[ \] //' | sed 's/^- //' | xargs)
    if [[ -n "$item" ]]; then
      key=$(echo "$item" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')
      if [[ -n "$key" ]]; then
        checklist_map["$key"]="${checklist_map[$key]:-}$skill_name, "
      fi
    fi
  done < <(grep -E '^- \[ \] ' "$skill_file" 2>/dev/null || true)
done

for key in "${!checklist_map[@]}"; do
  skills="${checklist_map[$key]}"
  count=$(echo "$skills" | grep -o "," | wc -l | tr -d ' ')
  if [[ "$count" -ge 2 ]]; then
    echo "- \"$key\" appears in: ${skills%, }" >> "$OUTPUT_FILE"
  fi
done

echo "" >> "$OUTPUT_FILE"
echo "✅ Duplicate scan complete: $OUTPUT_FILE"
