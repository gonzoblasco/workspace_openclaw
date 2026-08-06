#!/usr/bin/env bash
# setup-biome.sh — Configure Biome with recommended rules + shadcn/ui ignores
# Usage: ./setup-biome.sh [--shadcn]

set -euo pipefail

SHADCN_MODE="${1:-}"

echo "🔧 Setting up Biome..."

# Install
npm install -D --save-exact @biomejs/biome

# Generate biome.json if not exists
if [[ ! -f "biome.json" ]]; then
  npx @biomejs/biome init
fi

echo "✅ Biome installed"

# Add shadcn/ui ignore if requested
if [[ "$SHADCN_MODE" == "--shadcn" ]]; then
  echo "📌 Adding shadcn/ui ignore..."

  # Check if biome.json exists and has files.ignore
  if command -v python3 &>/dev/null; then
    python3 -c "
import json
with open('biome.json', 'r') as f:
    config = json.load(f)
if 'files' not in config:
    config['files'] = {}
if 'ignore' not in config['files']:
    config['files']['ignore'] = []
if 'src/components/ui/*' not in config['files']['ignore']:
    config['files']['ignore'].append('src/components/ui/*')
with open('biome.json', 'w') as f:
    json.dump(config, f, indent=2)
    f.write('\n')
"
  fi

  echo "✅ shadcn/ui components ignored from Biome checks"
fi

# Run initial format
echo "📌 Running initial format..."
npx biome check --write --no-errors-on-unmatched --files-ignore-unknown=true . 2>/dev/null || true

echo ""
echo "✅ Biome setup complete!"
echo "   Run 'npx biome ci .' to check in CI"
