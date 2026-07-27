#!/usr/bin/env bash
# content-calendar-generator.sh — Generate a content calendar CSV from a campaign brief
# Usage: ./content-calendar-generator.sh <campaign_name> <start_date> <weeks>

set -euo pipefail

NAME="${1:-Campaign}"
START_DATE="${2:-$(date +%Y-%m-%d)}"
WEEKS="${3:-4}"

echo "week,date,channel,content,format,status,owner"

for ((w=1; w<=WEEKS; w++)); do
  # Calculate week start (macOS date compatible)
  if [[ "$OSTYPE" == "darwin"* ]]; then
    week_start=$(date -j -v+$(((w-1)*7))d -f "%Y-%m-%d" "$START_DATE" +%Y-%m-%d 2>/dev/null || date -d "$START_DATE + $(((w-1)*7)) days" +%Y-%m-%d)
  else
    week_start=$(date -d "$START_DATE + $(((w-1)*7)) days" +%Y-%m-%d)
  fi

  # 3 content pieces per week (Mon/Wed/Fri)
  for day_offset in 0 2 4; do
    if [[ "$OSTYPE" == "darwin"* ]]; then
      piece_date=$(date -j -v+$(((w-1)*7 + day_offset))d -f "%Y-%m-%d" "$START_DATE" +%Y-%m-%d 2>/dev/null || date -d "$START_DATE + $(((w-1)*7 + day_offset)) days" +%Y-%m-%d)
    else
      piece_date=$(date -d "$START_DATE + $(((w-1)*7 + day_offset)) days" +%Y-%m-%d)
    fi

    channels=("social" "blog" "email")
    channel=${channels[$((day_offset % 3))]}

    echo "W${w},${piece_date},${channel},,,"

    # Extra piece for launch week
    if [ "$w" -eq 1 ] && [ "$day_offset" -eq 0 ]; then
      echo "W${w},${piece_date},all,Launch announcement,,,"
    fi
  done
done
