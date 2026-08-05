#!/bin/bash
# init-project.sh — Create a new project with double-git structure
#
# Usage:
#   ./scripts/init-project.sh <slug> [--repo <url>]
#
# Creates:
#   projects/<slug>/
#   projects/<slug>/.knowledge/   (tracked by workspace git)
#   projects/<slug>/.knowledge/BRIEF.md
#   projects/<slug>/.knowledge/STATUS.md
#   projects/<slug>/.gitignore    (ignores .knowledge/ for project git)
#   projects/<slug>/README.md
#
# If --repo is provided, also:
#   - Initializes the project as its own git repo
#   - Adds it as a submodule to the workspace
#   - Pushes initial commit to the remote

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECTS_DIR="${WORKSPACE_DIR}/projects"
SLUG="${1:-}"
REPO_URL=""

# Parse args
shift 2>/dev/null || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO_URL="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$SLUG" ]]; then
  echo "Usage: $0 <slug> [--repo <url>]"
  echo ""
  echo "Examples:"
  echo "  $0 my-project"
  echo "  $0 my-project --repo https://github.com/gonzoblasco/my-project.git"
  exit 1
fi

PROJECT_DIR="${PROJECTS_DIR}/${SLUG}"
KNOWLEDGE_DIR="${PROJECT_DIR}/.knowledge"

if [[ -d "$PROJECT_DIR" ]]; then
  echo "Error: Project already exists at ${PROJECT_DIR}"
  exit 1
fi

echo "Creating project: ${SLUG}"

# Create directory structure
mkdir -p "${KNOWLEDGE_DIR}"

# .knowledge/BRIEF.md
cat > "${KNOWLEDGE_DIR}/BRIEF.md" << 'BRIEF'
# BRIEF — Project Overview

## What

[One-line description of the project]

## Why

[Why this project exists — problem it solves, goal it serves]

## Stack

- [Tech 1]
- [Tech 2]

## Status

- [ ] Discovery
- [ ] Definition
- [ ] In Development
- [ ] Live
- [ ] Archived

## Key Decisions

- [Decision 1] — [rationale]
BRIEF

# .knowledge/STATUS.md
cat > "${KNOWLEDGE_DIR}/STATUS.md" << 'STATUS'
# STATUS — Project Status

## Current Phase

[Discovery / Definition / Development / Live / Archived]

## What's Working

- [ ]

## What's Blocked

- [ ]

## Next Up

1. [ ]
STATUS

# .gitignore (for the project's own git repo — ignores .knowledge/)
cat > "${PROJECT_DIR}/.gitignore" << 'GITIGNORE'
# Project .gitignore
# .knowledge/ is tracked by the workspace git, not the project git
.knowledge/

# Node
node_modules/
dist/
.next/
.turbo/

# Env
.env
.env.local
.env.*.local

# OS
.DS_Store
GITIGNORE

# README.md
cat > "${PROJECT_DIR}/README.md" << 'README'
# ${SLUG}

[Description]

## Stack

- [Tech]

## Getting Started

\`\`\`bash
# commands
\`\`\`
README

echo "  ✅ Created ${PROJECT_DIR}/"
echo "  ✅ Created .knowledge/BRIEF.md"
echo "  ✅ Created .knowledge/STATUS.md"
echo "  ✅ Created .gitignore"
echo "  ✅ Created README.md"

# If --repo was provided, set up as submodule
if [[ -n "$REPO_URL" ]]; then
  echo ""
  echo "Setting up git repo + submodule..."

  cd "${PROJECT_DIR}"

  git init
  git add -A
  git commit -m "chore: initial scaffold for ${SLUG}"

  git remote add origin "${REPO_URL}"
  git push -u origin main

  cd "${WORKSPACE_DIR}"

  # Add as submodule
  git submodule add "${REPO_URL}" "projects/${SLUG}"

  echo ""
  echo "  ✅ Git repo initialized at ${REPO_URL}"
  echo "  ✅ Submodule registered in workspace"
  echo ""
  echo "Next steps:"
  echo "  1. cd projects/${SLUG}"
  echo "  2. Start coding!"
  echo ""
  echo "Remember: .knowledge/ is tracked by workspace git."
  echo "Project code is tracked by its own repo at ${REPO_URL}."
else
  echo ""
  echo "Next steps:"
  echo "  1. Edit projects/${SLUG}/.knowledge/BRIEF.md"
  echo "  2. Edit projects/${SLUG}/.knowledge/STATUS.md"
  echo "  3. Start building!"
  echo ""
  echo "No git repo set up. To add one later:"
  echo "  cd projects/${SLUG} && git init && git add -A && git commit -m 'initial'"
  echo "  # then from workspace root: git submodule add <url> projects/${SLUG}"
fi
