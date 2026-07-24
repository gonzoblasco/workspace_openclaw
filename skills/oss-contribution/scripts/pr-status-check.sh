#!/usr/bin/env bash
# pr-status-check.sh — Batch check status of open PRs by author
# Usage: ./pr-status-check.sh [--author <username>]

set -euo pipefail

AUTHOR="${2:-gonzoblasco}"

echo "🔍 Checking PR status for: $AUTHOR"
echo ""

# Get all open PRs
PRS=$(gh pr list --author "$AUTHOR" --state open --json number,title,headRepository,headRefName,mergeable,reviews,comments,updatedAt,url 2>/dev/null || echo "[]")

# Parse and display
node -e "
const prs = $PRS;

if (prs.length === 0) {
  console.log('📭 No open PRs found for $AUTHOR');
  process.exit(0);
}

console.log('| # | Repo | Title | Status | Reviews | Updated |');
console.log('|---|------|-------|--------|---------|---------|');

prs.forEach(pr => {
  const repo = pr.headRepository?.name || 'unknown';
  const mergeable = pr.mergeable === 'MERGEABLE' ? '🟢' : pr.mergeable === 'CONFLICTING' ? '🔴' : '🟡';
  const reviewCount = pr.reviews?.length || 0;
  const updated = new Date(pr.updatedAt).toLocaleDateString();
  console.log('| ' + pr.number + ' | ' + repo + ' | ' + pr.title.substring(0, 50) + ' | ' + mergeable + ' | ' + reviewCount + ' | ' + updated + ' |');
});

console.log('');
console.log('🔗 Links:');
prs.forEach(pr => {
  console.log('  #' + pr.number + ': ' + pr.url);
});
"
