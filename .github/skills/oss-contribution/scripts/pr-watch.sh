#!/usr/bin/env bash
# pr-watch.sh — Watch a PR for comments/reviews after opening
# Usage: ./pr-watch.sh <pr-url> [--wait <minutes>] [--interval <seconds>]

set -euo pipefail

PR_URL="${1:?Usage: $0 <pr-url> [--wait <minutes>] [--interval <seconds>]}"
WAIT_MIN="${3:-10}"
INTERVAL_SEC="${5:-30}"

# Extract owner/repo/number from URL
REPO=$(echo "$PR_URL" | sed -E 's|https://github.com/([^/]+/[^/]+)/.*|\1|')
PR_NUM=$(echo "$PR_URL" | grep -oP 'pull/\K\d+' || echo "$PR_URL" | grep -oP '#\K\d+')

echo "👀 Watching PR #$PR_NUM in $REPO"
echo "   Wait: ${WAIT_MIN}min · Check every ${INTERVAL_SEC}s"
echo ""

END=$(( $(date +%s) + (WAIT_MIN * 60) ))

while [[ $(date +%s) -lt $END ]]; do
  # Fetch PR details
  PR_DATA=$(gh pr view "$PR_NUM" --repo "$REPO" --json state,mergeable,reviews,comments 2>/dev/null || echo "{}")
  
  STATE=$(echo "$PR_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('state',''))" 2>/dev/null || echo "unknown")
  MERGEABLE=$(echo "$PR_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('mergeable',''))" 2>/dev/null || echo "unknown")
  REVIEW_COUNT=$(echo "$PR_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('reviews',[])))" 2>/dev/null || echo "0")
  COMMENT_COUNT=$(echo "$PR_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('comments',{}).get('totalCount',0))" 2>/dev/null || echo "0")

  echo "[$(date '+%H:%M:%S')] State: $STATE | Mergeable: $MERGEABLE | Reviews: $REVIEW_COUNT | Comments: $COMMENT_COUNT"

  # Check for bot comments that need response
  BOT_COMMENTS=$(gh pr view "$PR_NUM" --repo "$REPO" --json comments --jq '.comments[] | select(.author.__typename == "Bot") | .body' 2>/dev/null | head -5 || true)
  if [[ -n "$BOT_COMMENTS" ]]; then
    echo "⚠️  Bot comments detected:"
    echo "$BOT_COMMENTS" | head -3
  fi

  # Check for human review requests
  REVIEWS=$(gh pr view "$PR_NUM" --repo "$REPO" --json reviews --jq '.[] | select(.state == "CHANGES_REQUESTED") | .body' 2>/dev/null | head -5 || true)
  if [[ -n "$REVIEWS" ]]; then
    echo "🔴 Changes requested:"
    echo "$REVIEWS" | head -3
  fi

  # If PR was merged or closed, stop watching
  if [[ "$STATE" == "MERGED" ]]; then
    echo "✅ PR merged! 🎉"
    exit 0
  elif [[ "$STATE" == "CLOSED" ]]; then
    echo "❌ PR closed without merge"
    exit 1
  fi

  sleep "$INTERVAL_SEC"
done

echo ""
echo "⏰ Watch period ended. PR still open."
echo "   Review: $PR_URL"
