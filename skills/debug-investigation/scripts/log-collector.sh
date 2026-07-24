#!/usr/bin/env bash
# log-collector.sh — Collect logs from server, browser console, network
# Usage: ./log-collector.sh [--server <log-dir>] [--output <file>]

set -euo pipefail

SERVER_LOG_DIR=""
OUTPUT_FILE="debug-logs-$(date +%Y%m%d-%H%M%S).md"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --server) SERVER_LOG_DIR="$2"; shift 2 ;;
    --output) OUTPUT_FILE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

echo "📋 Collecting debug logs..."
echo ""

cat > "$OUTPUT_FILE" << 'HEADER'
# Debug Log Collection

HEADER
echo "**Date:** $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT_FILE"
echo "**Host:** $(hostname)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Server logs
if [[ -n "$SERVER_LOG_DIR" ]]; then
  echo "## Server Logs" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  for logfile in "$SERVER_LOG_DIR"/*.log; do
    if [[ -f "$logfile" ]]; then
      echo "### $(basename "$logfile")" >> "$OUTPUT_FILE"
      echo '```' >> "$OUTPUT_FILE"
      tail -100 "$logfile" >> "$OUTPUT_FILE"
      echo '```' >> "$OUTPUT_FILE"
      echo "" >> "$OUTPUT_FILE"
    fi
  done
fi

# System info
echo "## System Information" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "Node: $(node -v 2>/dev/null || echo 'N/A')"
echo "npm: $(npm -v 2>/dev/null || echo 'N/A')"
echo "OS: $(uname -a)"
echo "Memory:"
vm_stat 2>/dev/null | head -5 || free -h 2>/dev/null || echo "N/A"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Git info
if git rev-parse --git-dir &>/dev/null; then
  echo "## Git Information" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  echo '```' >> "$OUTPUT_FILE"
  echo "Branch: $(git branch --show-current)"
  echo "Last commit: $(git log -1 --format='%h %s')"
  echo "Modified files:"
  git status --short
  echo '```' >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
fi

echo "✅ Logs collected: $OUTPUT_FILE"
