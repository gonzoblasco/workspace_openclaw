#!/bin/bash
# init-project.sh - Create a new project with double-git structure
#
# Usage:
#   ./scripts/init-project.sh <slug> [--repo <url>]
#
# By default, creates a private repo on GitHub under gonzoblasco.
# If --repo is provided, uses that URL instead.
# If the repo already exists on GitHub, asks how to proceed.
#
# Creates:
#   projects/<slug>/
#   projects/<slug>/.knowledge/   (tracked by workspace git)
#   projects/<slug>/.knowledge/BRIEF.md
#   projects/<slug>/.knowledge/STATUS.md
#   projects/<slug>/.gitignore    (ignores .knowledge/ for project git)
#   projects/<slug>/README.md
#
# If repo is set up, also:
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

# .gitignore (for the project's own git repo - ignores .knowledge/)
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

# Determine repo URL
if [[ -z "$REPO_URL" ]]; then
  # Default: private repo on GitHub under gonzoblasco
  REPO_URL="https://github.com/gonzoblasco/${SLUG}.git"
fi

echo ""
echo "Checking if remote repo exists..."

# Extract owner/repo from URL for gh check
REPO_PATH=$(echo "$REPO_URL" | sed -E 's|https://github.com/||; s|git@github.com:||; s|\.git$||')

if gh repo view "$REPO_PATH" --json name &>/dev/null; then
  echo "  ⚠️  Repo already exists: ${REPO_PATH}"
  echo ""
  echo "Options:"
  echo "  1) Use existing repo (clone/fetch into submodule)"
  echo "  2) Use a different URL"
  echo "  3) Skip git setup (no submodule)"
  echo ""
  read -p "Choose [1/2/3]: " choice

  case "$choice" in
    1)
      echo "Setting up submodule from existing repo..."
      cd "${WORKSPACE_DIR}"
      git submodule add "${REPO_URL}" "projects/${SLUG}"
      echo "  ✅ Submodule registered from existing repo"
      ;;
    2)
      read -p "Enter repo URL: " REPO_URL
      echo "Setting up submodule from ${REPO_URL}..."
      cd "${WORKSPACE_DIR}"
      git submodule add "${REPO_URL}" "projects/${SLUG}"
      echo "  ✅ Submodule registered"
      ;;
    3)
      echo "Skipping git setup. Project scaffold is ready."
      echo ""
      echo "To add git later:"
      echo "  cd projects/${SLUG} && git init && git add -A && git commit -m 'initial'"
      echo "  # then from workspace root: git submodule add <url> projects/${SLUG}"
      exit 0
      ;;
    *)
      echo "Invalid choice. Skipping git setup."
      exit 0
      ;;
  esac
else
  echo "  Repo does not exist yet. Creating private repo on GitHub..."

  # Create private repo on GitHub (no --push yet; we init git first)
  gh repo create "${REPO_PATH}" --private

  echo ""
  echo "Setting up project git (double-git, no submodule)..."

  # Initialize the project's own git repo and push initial commit
  cd "${PROJECT_DIR}"
  git init -q
  git branch -M main
  git remote add origin "${REPO_URL}"
  git add -A
  git commit -q -m "chore: initial scaffold"
  git push -u origin main

  # Track .knowledge/ as a blob in the workspace git (NOT a submodule)
  cd "${WORKSPACE_DIR}"
  git add "projects/${SLUG}/.knowledge"
  git commit -q -m "feat(projects): add ${SLUG} project (.knowledge)"

  echo ""
  echo "  ✅ Private repo created at ${REPO_URL}"
  echo "  ✅ Project git initialized and pushed"
  echo "  ✅ .knowledge/ tracked as blob in workspace (double-git)"
fi

echo ""
 echo "Next steps:"
 echo "  1. cd projects/${SLUG}"
 echo "  2. Start coding!"
 echo ""
 echo "Remember: .knowledge/ is tracked by workspace git (blob, double-git)."
 echo "Project code is tracked by its own repo at ${REPO_URL}."
