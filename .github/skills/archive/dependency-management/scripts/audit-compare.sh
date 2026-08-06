#!/usr/bin/env bash
# audit-compare.sh — Compare dependency state between two points in time
# Usage: ./audit-compare.sh <commit-a> <commit-b>

set -euo pipefail

COMMIT_A="${1:?Usage: $0 <commit-a> <commit-b>}"
COMMIT_B="${2:?Usage: $0 <commit-a> <commit-b>}"

echo "📊 Comparing dependencies between:"
echo "   A: $COMMIT_A"
echo "   B: $COMMIT_B"
echo ""

# Extract package.json from both commits
PACKAGE_A=$(git show "$COMMIT_A:package.json" 2>/dev/null || echo "{}")
PACKAGE_B=$(git show "$COMMIT_B:package.json" 2>/dev/null || echo "{}")

# Compare
node -e "
const a = $PACKAGE_A;
const b = $PACKAGE_B;

const depsA = {...a.dependencies, ...a.devDependencies};
const depsB = {...b.dependencies, ...b.devDependencies};

const allDeps = new Set([...Object.keys(depsA), ...Object.keys(depsB)]);

console.log('| Package | Version A | Version B | Change |');
console.log('|---------|-----------|-----------|--------|');

allDeps.forEach(name => {
  const vA = depsA[name] || '-';
  const vB = depsB[name] || '-';
  if (vA !== vB) {
    const change = vA === '-' ? 'added' : vB === '-' ? 'removed' : 'updated';
    console.log('| ' + name + ' | ' + vA + ' | ' + vB + ' | ' + change + ' |');
  }
});
"
