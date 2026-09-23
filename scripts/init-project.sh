#!/bin/bash
# init-project.sh - Create a new project with triple-git structure
#
# Usage:
#   ./scripts/init-project.sh <slug> [--repo <url>]
#
# By default, creates a private repo on GitHub under gonzoblasco.
# If --repo is provided, uses that URL instead.
# If the repo already exists on GitHub, asks how to proceed.
#
# Triple-git structure (2026-09-02):
#   workspace/                 (repo: workspace_openclaw)
#   `-- projects/              (repo agregado: projects_openclaw - archivo de todo el codigo)
#       `-- <slug>/            (repo individual: gonzoblasco/<slug> - fuente de la verdad)
#           `-- .knowledge/    (memoria institucional, SOLO workspace)
#
# Creates:
#   projects/<slug>/
#   projects/<slug>/.knowledge/   (tracked by workspace git)
#   projects/<slug>/.knowledge/BRIEF.md
#   projects/<slug>/.knowledge/STATUS.md
#   projects/<slug>/.gitignore    (does NOT list .knowledge/ - exclusion lives in .git/info/exclude)
#   projects/<slug>/README.md
#
# Also:
#   - Tracks .knowledge/ as a blob in the workspace git (BEFORE the project's own git init - see note below)
#   - Initializes the project as its own git repo (excludes .knowledge/ via .git/info/exclude)
#   - Pushes initial commit to its remote
#   - Registers the folder in the aggregate repo (projects/ -> projects_openclaw)

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECTS_DIR="${WORKSPACE_DIR}/projects"
AGGREGATE_REPO="gonzoblasco/projects_openclaw"
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

# Sanity: the aggregate repo must be the remote of projects/
if [[ "$(git -C "$PROJECTS_DIR" remote get-url origin 2>/dev/null)" != *"projects_openclaw"* ]]; then
  echo "Warning: projects/ is not pointing to ${AGGREGATE_REPO}. Aggregate registration will be skipped."
  echo "  Fix with: git -C ${PROJECTS_DIR} remote set-url origin https://github.com/${AGGREGATE_REPO}.git"
  AGGREGATE_OK=0
else
  AGGREGATE_OK=1
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
# NOTE: .knowledge/ is NOT listed here on purpose. This .gitignore is also parsed
# by the aggregate repo (projects/ -> projects_openclaw) and by the workspace git;
# listing .knowledge/ would break workspace blob tracking (triple-git).
# The project-local exclusion lives in .git/info/exclude instead.
cat > "${PROJECT_DIR}/.gitignore" << 'GITIGNORE'
# Project .gitignore
# .knowledge/ exclusion lives in .git/info/exclude (do not list it here)

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

# Track .knowledge/ as a blob in the workspace git (NOT a submodule, NOT a gitlink).
#
# ORDER MATTERS: this must run BEFORE the project's own `git init`. Once
# projects/<slug>/.git exists, the workspace repo treats the directory as an
# embedded repository, and `git add projects/<slug>/.knowledge` stages NOTHING
# (git exits 0 with no effect - silent failure). Seeding the index first makes
# every later update to .knowledge/ work normally.
# Verified 2026-09-22 (sandbox /tmp/gt3, /tmp/gt4): add-before-init works;
# add-after-init fails regardless of .gitignore; existing tracked projects
# (kanam-lab, langchain-starter, kanam-pulse) are unaffected.
cd "${WORKSPACE_DIR}"
git add "projects/${SLUG}/.knowledge"
if git diff --cached --quiet -- "projects/${SLUG}/.knowledge"; then
  echo "  ❌ .knowledge/ NO se pudo stagear en el workspace git."
  echo "     Causa tipica: projects/${SLUG}/.git ya existe. Revisar ANTES de seguir."
  exit 1
fi
git commit -q -m "feat(projects): add ${SLUG} project (.knowledge)"
echo "  ✅ .knowledge/ tracked as blob in workspace (triple-git)"

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
  echo "  Repo already exists: ${REPO_PATH}"
  echo "  Setting up project git from existing repo (triple-git, no submodule)..."
  cd "${PROJECT_DIR}"
  git init -q
  git branch -M main
  printf '\n# Triple-git: .knowledge/ belongs to the workspace git, never to this repo\n.knowledge/\n' >> .git/info/exclude
  git remote add origin "${REPO_URL}"
  git fetch -q origin
  git checkout -q main || git checkout -q -b main
  git add -A
  if git diff --cached --quiet; then
    echo "  ℹ️  No changes to commit (already in sync with remote)"
  else
    git commit -q -m "chore: init via init-project.sh (triple-git)"
    git push -q -u origin main
    echo "  ✅ Pushed to ${REPO_URL}"
  fi
else
  echo "  Repo does not exist yet. Creating private repo on GitHub..."

  # Create private repo on GitHub (no --push yet; we init git first)
  gh repo create "${REPO_PATH}" --private

  echo ""
  echo "Setting up project git (triple-git, no submodule)..."

  # Initialize the project's own git repo and push initial commit
  cd "${PROJECT_DIR}"
  git init -q
  git branch -M main
  # Triple-git: exclude .knowledge/ locally (NOT via .gitignore - workspace and aggregate parse it too)
  printf '\n# Triple-git: .knowledge/ belongs to the workspace git, never to this repo\n.knowledge/\n' >> .git/info/exclude
  git remote add origin "${REPO_URL}"
  git add -A
  git commit -q -m "chore: initial scaffold"
  git push -u origin main

  echo "  ✅ Private repo created at ${REPO_URL}"
  echo "  ✅ Project git initialized and pushed"
fi

# Register in the aggregate repo
if [[ "$AGGREGATE_OK" == "1" ]]; then
  cd "${PROJECTS_DIR}"
  git add "${SLUG}"
  if git diff --cached --quiet; then
    echo "  ℹ️  Aggregate repo: nothing new to commit for ${SLUG}"
  else
    git commit -q -m "feat: register ${SLUG} in aggregate repo"
    echo "  ✅ ${SLUG} registered in aggregate repo (projects/ -> projects_openclaw)"
    echo "  ℹ️  Remember to push the aggregate: ./scripts/aggregate-sync.sh push"
  fi
else
  echo "  ⚠️  Aggregate repo not configured on projects/ - register manually:"
  echo "     cd ${PROJECTS_DIR} && git add ${SLUG} && git commit && ./scripts/aggregate-sync.sh push"
fi

echo ""
echo "Next steps:"
echo "  1. cd projects/${SLUG}"
echo "  2. Start coding!"
echo ""
echo "Remember: .knowledge/ is tracked by workspace git (blob, triple-git)."
echo "Project code is tracked by its own repo at ${REPO_URL}."
echo "The aggregate repo (projects_openclaw) mirrors the folder for the full-code archive."
