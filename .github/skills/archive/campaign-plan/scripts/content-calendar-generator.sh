#!/usr/bin/env bash
# content-calendar-generator.sh — Generate a content calendar CSV from a campaign brief
# Usage: ./content-calendar-generator.sh <campaign_name> <start_date> <weeks>

set -euo pipefail

NAME="${1:-Campaign}"
START_DATE="${2:-$(date +%Y-%m-%d)}"
WEEKS="${3:-4}"

add_days() {
  local base="$1"
  local days="$2"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    date -j -v+"${days}"d -f "%Y-%m-%d" "$base" +%Y-%m-%d
  else
    date -d "$base + $days days" +%Y-%m-%d
  fi
}

echo "week,date,channel,content,format,status,owner"

for ((w=1; w<=WEEKS; w++)); do
  # 3 content pieces per week (Mon/Wed/Fri)
  for day_offset in 0 2 4; do
    total_days=$(((w-1)*7 + day_offset))
    piece_date=$(add_days "$START_DATE" "$total_days")

    channels=("social" "blog" "email")
    channel=${channels[$((day_offset % 3))]}

    echo "W${w},${piece_date},${channel},,,"

    # Extra piece for launch week
    if [ "$w" -eq 1 ] && [ "$day_offset" -eq 0 ]; then
      echo "W${w},${piece_date},all,Launch announcement,,,"
    fi
  done
done
