#!/usr/bin/env bash
# check-outdated.sh — npm outdated with semver classification and risk filter
# Usage: ./check-outdated.sh [--risk <low|medium|high>]

set -euo pipefail

RISK_FILTER="${2:-}"

echo "📌 Checking outdated dependencies..."
echo ""

# Run npm outdated with JSON
OUTDATED=$(npm outdated --json 2>/dev/null || echo "{}")

# Parse and classify
node -e "
const data = $OUTDATED;
const entries = Object.entries(data);

if (entries.length === 0) {
  console.log('✅ All dependencies are up to date!');
  process.exit(0);
}

const classify = (current, wanted, latest) => {
  const c = current.replace(/[^0-9.]/g, '').split('.').map(Number);
  const w = wanted.replace(/[^0-9.]/g, '').split('.').map(Number);
  const l = latest.replace(/[^0-9.]/g, '').split('.').map(Number);

  if (l[0] > w[0]) return { type: 'major', risk: 'high' };
  if (l[0] > c[0]) return { type: 'major', risk: 'high' };
  if (l[1] > c[1]) return { type: 'minor', risk: 'medium' };
  return { type: 'patch', risk: 'low' };
};

const riskFilter = '$RISK_FILTER';

console.log('| Package | Current | Wanted | Latest | Type | Risk |');
console.log('|---------|---------|--------|--------|------|------|');

entries.forEach(([name, info]) => {
  const { type, risk } = classify(info.current, info.wanted, info.latest);
  if (riskFilter && risk !== riskFilter) return;
  console.log('| ' + name + ' | ' + info.current + ' | ' + info.wanted + ' | ' + info.latest + ' | ' + type + ' | ' + risk + ' |');
});
"
