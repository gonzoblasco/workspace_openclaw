#!/usr/bin/env bash
# timeline.sh — Generate incident timeline from log entries
# Usage: ./timeline.sh <log-file> [--output <file>]

set -euo pipefail

LOG_FILE="${1:?Usage: $0 <log-file> [--output <file>]}"
OUTPUT="${3:-timeline-$(date +%Y%m%d-%H%M%S).md}"

if [[ ! -f "$LOG_FILE" ]]; then
  echo "❌ Log file not found: $LOG_FILE"
  exit 1
fi

echo "📋 Generating timeline from: $LOG_FILE"
echo ""

cat > "$OUTPUT" << 'HEADER'
# Incident Timeline

HEADER
echo "**Generated:** $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT"
echo "**Source:** $LOG_FILE" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Time | Event | Source |" >> "$OUTPUT"
echo "|------|-------|--------|" >> "$OUTPUT"

# Extract timestamps and messages from log
# Supports common log formats
grep -E '^\d{4}-\d{2}-\d{2}' "$LOG_FILE" | head -100 | while IFS= read -r line; do
  # Extract timestamp (first 19 chars for ISO format)
  TIMESTAMP="${line:0:19}"
  MESSAGE="${line:20}"
  echo "| $TIMESTAMP | $MESSAGE | log |" >> "$OUTPUT"
done

echo "" >> "$OUTPUT"
echo "---" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "## Key Events" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "- **Detection:** " >> "$OUTPUT"
echo "- **Classification:** " >> "$OUTPUT"
echo "- **Containment:** " >> "$OUTPUT"
echo "- **Resolution:** " >> "$OUTPUT"

echo "✅ Timeline generated: $OUTPUT"
