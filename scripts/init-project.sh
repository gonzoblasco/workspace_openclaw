#!/bin/bash
# init-project.sh - Create a new project
#
# Usage:
#   ./scripts/init-project.sh <slug> [--repo <url>]
#
# By default, creates a private repo on GitHub under gonzoblasco.
# If --repo is provided, uses that URL instead.
# If the repo already exists on GitHub, asks how to proceed.
#
# Model (ADR-098, 2026-10-08; clarified by Gonzo 2026-10-13):
#   workspace/                 (repo: workspace_openclaw - ignores projects/ 100%)
#   `-- projects/              (flat container folder - NOT a repo; ignored by the workspace git)
#       `-- <slug>/            (the project's own git repo: gonzoblasco/<slug> - source of truth)
#           `-- .knowledge/    (institutional memory - TRACKED BY THE PROJECT REPO, travels with it)
#
# There is NO aggregate repo layer (retired; `projects_openclaw` is archived).
#
# Creates:
#   projects/<slug>/
#   projects/<slug>/.knowledge/   (tracked by the project's own repo)
#   projects/<slug>/.knowledge/BRIEF.md
#   projects/<slug>/.knowledge/STATUS.md
#   projects/<slug>/.gitignore
#   projects/<slug>/README.md
#
# Also:
#   - Initializes the project as its own git repo (creates the remote if needed)
#   - Commits code + .knowledge/ together and pushes to its remote

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
# BRIEF - Project Overview

## What

[One-line description of the project]

## Why

[Why this project exists - problem it solves, goal it serves]

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

- [Decision 1] - [rationale]
BRIEF

# .knowledge/STATUS.md
cat > "${KNOWLEDGE_DIR}/STATUS.md" << 'STATUS'
# STATUS - Project Status

## Current Phase

[Discovery / Definition / Development / Live / Archived]

## What's Working

- [ ]

## What's Blocked

- [ ]

## Next Up

1. [ ]
STATUS

# .gitignore (for the project's own git repo)
# .knowledge/ is NOT ignored: the project's memory travels with the project
# (tracked by its own repo, ADR-098).
cat > "${PROJECT_DIR}/.gitignore" << 'GITIGNORE'
# Project .gitignore

# Node
node_modules/
dist/
.next/
.turbo/
coverage/

# Env
.env
.env.local
.env.*.local
!.env.example

# OS
.DS_Store
GITIGNORE

# README.md
cat > "${PROJECT_DIR}/README.md" << README
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

# Determine repo URL
if [[ -z "$REPO_URL" ]]; then
  # Default: private repo on GitHub under gonzoblasco
  REPO_URL="https://github.com/gonzoblasco/${SLUG}.git"
fi

echo ""
echo "Checking if remote repo exists..."

# Extract owner/repo from URL for gh check
REPO_PATH=$(echo "$REPO_URL" | sed -E 's|https://github.com/||; s|git@github.com:||; s|\.git$||')

cd "${PROJECT_DIR}"
git init -q
git branch -M main

if gh repo view "$REPO_PATH" --json name &>/dev/null; then
  echo "  Repo already exists: ${REPO_PATH}"
  git remote add origin "${REPO_URL}"
  git fetch -q origin
  git checkout -q main || git checkout -q -b main
  git add -A
  if git diff --cached --quiet; then
    echo "  ℹ️  No changes to commit (already in sync with remote)"
  else
    git commit -q -m "chore: init via init-project.sh"
    git push -q -u origin main
    echo "  ✅ Pushed to ${REPO_URL}"
  fi
else
  echo "  Repo does not exist yet. Creating private repo on GitHub..."
  gh repo create "${REPO_PATH}" --private
  git remote add origin "${REPO_URL}"
  git add -A
  git commit -q -m "chore: initial scaffold"
  git push -q -u origin main
  echo "  ✅ Private repo created at ${REPO_URL}"
fi

echo ""
echo "Next steps:"
echo "  1. cd projects/${SLUG}"
echo "  2. Start coding!"
echo ""
echo "The project is its own git repo (code + .knowledge/ together)."
echo "Source of truth: ${REPO_URL}"
