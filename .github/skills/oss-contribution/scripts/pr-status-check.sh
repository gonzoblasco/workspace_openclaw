#!/usr/bin/env bash
# pr-status-check.sh — Batch check all PRs involving a user (author, commenter, reviewer)
# Usage: ./pr-status-check.sh [--user <username>]

set -euo pipefail

USER="${2:-gonzoblasco}"

echo "🔍 Checking all PRs involving: $USER"
echo ""

# Combine multiple queries
RESULTS=$(mktemp)
echo "[]" > "$RESULTS"

merge_json() {
  local new="$1"
  python3 -c "
import json, sys
try:
  with open('$RESULTS') as f: existing = json.load(f)
  with open('$new') as f: new_data = json.load(f)
  seen = {(pr['number'], pr['headRepository']['name'] if pr.get('headRepository') else '') for pr in existing}
  for pr in new_data:
    key = (pr['number'], pr['headRepository']['name'] if pr.get('headRepository') else '')
    if key not in seen:
      existing.append(pr)
      seen.add(key)
  print(json.dumps(existing, indent=2))
except: print(json.dumps(new_data, indent=2))
" > "$RESULTS.tmp" && mv "$RESULTS.tmp" "$RESULTS"
}

# 1. PRs authored by user
gh pr list --author "$USER" --state open --json number,title,headRepository,headRefName,mergeable,reviews,comments,updatedAt,url 2>/dev/null > /tmp/_prs_auth.json || true
merge_json /tmp/_prs_auth.json

# 2. PRs where user commented
gh pr list --search "commenter:$USER" --state open --json number,title,headRepository,headRefName,mergeable,reviews,comments,updatedAt,url --limit 20 2>/dev/null > /tmp/_prs_comment.json || true
merge_json /tmp/_prs_comment.json

# 3. PRs where user was mentioned
gh pr list --search "mentions:$USER" --state open --json number,title,headRepository,headRefName,mergeable,reviews,comments,updatedAt,url --limit 20 2>/dev/null > /tmp/_prs_mention.json || true
merge_json /tmp/_prs_mention.json

# 4. PRs where user was requested as reviewer
gh pr list --search "review-requested:$USER" --state open --json number,title,headRepository,headRefName,mergeable,reviews,comments,updatedAt,url --limit 20 2>/dev/null > /tmp/_prs_review.json || true
merge_json /tmp/_prs_review.json

# Parse and display
python3 -c "
import json

with open('$RESULTS') as f:
    prs = json.load(f)

if not prs:
    print('📭 No open PRs found involving $USER')
    exit(0)

# Sort by updatedAt (most recent first)
prs.sort(key=lambda p: p.get('updatedAt', ''), reverse=True)

print(f'📊 {len(prs)} open PRs involving $USER')
print()
print('| # | Repo | Title | Status | Reviews | Updated |')
print('|---|------|-------|--------|---------|---------|')

for pr in prs:
    repo = pr.get('headRepository', {}).get('name', 'unknown') if pr.get('headRepository') else 'unknown'
    mergeable = pr.get('mergeable', '')
    status = '🟢' if mergeable == 'MERGEABLE' else '🔴' if mergeable == 'CONFLICTING' else '🟡'
    review_count = len(pr.get('reviews', []))
    updated = pr.get('updatedAt', '')[:10]
    title = pr.get('title', '')[:50]
    print(f'| {pr[\"number\"]} | {repo} | {title} | {status} | {review_count} | {updated} |')

print()
print('🔗 Links:')
for pr in prs:
    print(f'  #{pr[\"number\"]}: {pr[\"url\"]}')
"

rm -f "$RESULTS" /tmp/_prs_*.json
