#!/usr/bin/env bash
# init-git.sh — Git init + .gitignore + .knowledge/ + submodule setup
# Usage: ./init-git.sh <project-name> [--with-submodule <repo-url>]

set -euo pipefail

PROJECT_NAME="${1:?Usage: $0 <project-name> [--with-submodule <repo-url>]}"
SUBMODULE_URL=""

# Parse optional submodule
if [[ "${2:-}" == "--with-submodule" ]]; then
  SUBMODULE_URL="${3:?Missing submodule URL}"
fi

echo "🔧 Initializing git for: $PROJECT_NAME"
echo ""

# Git init
git init
echo "✅ Git initialized"

# .gitignore
cat > .gitignore << 'GITIGNORE'
node_modules/
.next/
dist/
build/
.env
.env.local
*.log
.DS_Store
coverage/
.turbo/
GITIGNORE
echo "✅ .gitignore created"

# .knowledge/ directory
mkdir -p .knowledge
cat > .knowledge/.gitkeep << 'EOF'
EOF
echo "✅ .knowledge/ directory created"

# Initial commit
git add -A
git commit -m "chore: initial scaffold for $PROJECT_NAME" --allow-empty
echo "✅ Initial commit created"

# Submodule setup (optional)
if [[ -n "$SUBMODULE_URL" ]]; then
  echo ""
  echo "📌 Adding submodule..."
  git submodule add "$SUBMODULE_URL" .
  echo "✅ Submodule added"
fi

echo ""
echo "═══════════════════════════════════════"
echo "  Git setup complete!"
echo "═══════════════════════════════════════"
echo "  Next steps:"
echo "  1. Create remote repo on GitHub"
echo "  2. git remote add origin <url>"
echo "  3. git push -u origin main"
echo ""
