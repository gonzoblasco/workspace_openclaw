#!/bin/bash
# pr-dashboard.sh — Fetch open PRs authored by gonzoblasco across all repos
# Uses gh search prs to find PRs in any repo (including forks/OSS)
# Output: JSON with summary stats + PR list

set -euo pipefail

# Fetch PRs via search (catches PRs in any repo, not just owned repos)
PRS=$(gh search prs --author gonzoblasco --state open --limit 50 --json number,title,repository,url,state,createdAt,updatedAt,author,isDraft,labels 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$PRS" ] || [ "$PRS" = "[]" ]; then
  echo '{"open_count":0,"review_count":0,"draft_count":0,"stale_count":0,"total_additions":0,"total_deletions":0,"oldest_days":0,"prs":[]}'
  exit 0
fi

# Get detailed info for each PR (additions, deletions, reviewDecision)
# We need to fetch each PR individually for those fields
DETAILED=$(echo "$PRS" | jq -c '.[]' | while read -r pr; do
  REPO=$(echo "$pr" | jq -r '.repository.nameWithOwner')
  NUM=$(echo "$pr" | jq -r '.number')
  DETAIL=$(gh pr view "$NUM" --repo "$REPO" --json additions,deletions,reviewDecision,headRefName,baseRefName,mergeable 2>/dev/null)
  if [ -n "$DETAIL" ] && [ "$DETAIL" != "null" ]; then
    echo "$pr" | jq -c --argjson detail "$DETAIL" '. + $detail'
  else
    echo "$pr" | jq -c '. + {additions: 0, deletions: 0, reviewDecision: null, headRefName: "", baseRefName: "", mergeable: null}'
  fi
done)

# Build array from the stream
ENRICHED=$(echo "$DETAILED" | jq -s '.')

# Count by status
OPEN_COUNT=$(echo "$ENRICHED" | jq 'length')
REVIEW_COUNT=$(echo "$ENRICHED" | jq '[.[] | select(.reviewDecision == "REVIEW_REQUIRED" or .reviewDecision == "CHANGES_REQUESTED")] | length')
DRAFT_COUNT=$(echo "$ENRICHED" | jq '[.[] | select(.isDraft == true)] | length')

# Calculate additions/deletions
TOTAL_ADD=$(echo "$ENRICHED" | jq '[.[] | .additions // 0] | add // 0')
TOTAL_DEL=$(echo "$ENRICHED" | jq '[.[] | .deletions // 0] | add // 0')

# Find oldest PR in days
NOW_EPOCH=$(date +%s)
OLDEST_SECS=$(echo "$ENRICHED" | jq "[.[] | (.createdAt | fromdateiso8601)] | min // $NOW_EPOCH")
OLDEST_DAYS=$(( (NOW_EPOCH - OLDEST_SECS) / 86400 ))

# Stale: no activity in 14+ days
STALE_COUNT=$(echo "$ENRICHED" | jq "[.[] | select((.updatedAt | fromdateiso8601) < $((NOW_EPOCH - 1209600)))] | length")

# Bucket cada PR por estado (agrupacion portada del plugin github-workflow, aditivo)
BUCKETED=$(echo "$ENRICHED" | jq --argjson now "$NOW_EPOCH" '
  map(
    . + { bucket: (
      if .isDraft then "draft"
      elif (.reviewDecision == "REVIEW_REQUIRED" or .reviewDecision == "CHANGES_REQUESTED") then "needs_review"
      elif ((.updatedAt | fromdateiso8601) < ($now - 1209600)) then "stale"
      else "ok" end
    ) }
  )
')

# Resumen por estado (count por bucket)
BY_STATE=$(echo "$BUCKETED" | jq 'group_by(.bucket) | map({key: .[0].bucket, value: length}) | from_entries')

# Build final output with clean shape
jq -n \
  --argjson open_count "$OPEN_COUNT" \
  --argjson review_count "$REVIEW_COUNT" \
  --argjson draft_count "$DRAFT_COUNT" \
  --argjson stale_count "$STALE_COUNT" \
  --argjson total_additions "$TOTAL_ADD" \
  --argjson total_deletions "$TOTAL_DEL" \
  --argjson oldest_days "$OLDEST_DAYS" \
  --argjson by_state "$BY_STATE" \
  --argjson prs "$BUCKETED" \
  '{open_count: $open_count, review_count: $review_count, draft_count: $draft_count, stale_count: $stale_count, total_additions: $total_additions, total_deletions: $total_deletions, oldest_days: $oldest_days, by_state: $by_state, prs: $prs}'
