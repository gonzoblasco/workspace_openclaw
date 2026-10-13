#!/bin/bash
# aggregate-sync.sh - Sync the aggregate repo (projects/ <-> projects_openclaw)
#
# The aggregate repo (projects/) is the full-code archive of all projects.
# It is NOT the source of truth for working on a project (that is each
# individual repo at gonzoblasco/<slug>). Keep it in sync explicitly.
#
# Note (ADR-098, 2026-10-08): projects live in <workspace>/projects/, inside the
# gateway tree; ~/projects is a symlink to it (agents use the real path). ADR-075
# (projects outside the worktree) is superseded. This script follows ADR-098.
#
# Usage:
#   ./scripts/aggregate-sync.sh status          - show pending changes in projects/
#   ./scripts/aggregate-sync.sh commit ["msg"]  - stage + commit all changes (default msg)
#   ./scripts/aggregate-sync.sh push            - git pull --rebase + push
#   ./scripts/aggregate-sync.sh sync ["msg"]    - status + commit + push (all in one)
#   ./scripts/aggregate-sync.sh check           - verify gitlink safety (no embedded .git tracked)
#
# Notes:
#   - Committing here NEVER touches the individual project repos (their .git/
#     dirs live on disk but are ignored by the aggregate's .gitignore).
#   - A change made inside projects/<slug>/ is visible to both the project repo
#     and the aggregate. Commit in each where it belongs.
#   - If a project's .gitignore excludes its .knowledge/, that memory is NOT
#     part of the aggregate.

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECTS_DIR="${PROJECTS_DIR:-${WORKSPACE_DIR}/projects}"
AGGREGATE_URL="https://github.com/gonzoblasco/projects_openclaw.git"
DEFAULT_MSG="chore: sync aggregate repo (projects_openclaw)"

if [[ ! -d "${PROJECTS_DIR}/.git" ]]; then
  echo "Error: ${PROJECTS_DIR} is not a git repo. Expected the aggregate repo."
  echo "Initialize it with:"
  echo "  cd ${PROJECTS_DIR} && git init && git remote add origin ${AGGREGATE_URL} && git fetch && git checkout -b main origin/main"
  exit 1
fi

# Ensure origin points to the aggregate repo (safety: never push to a project repo from here)
ORIGIN_URL="$(git -C "${PROJECTS_DIR}" remote get-url origin 2>/dev/null || echo "")"
if [[ "${ORIGIN_URL}" != *"projects_openclaw"* ]]; then
  echo "Error: origin of ${PROJECTS_DIR} is ${ORIGIN_URL:-<none>}, expected projects_openclaw."
  echo "Fix: git -C ${PROJECTS_DIR} remote set-url origin ${AGGREGATE_URL}"
  exit 1
fi

cmd="${1:-status}"
msg="${2:-${DEFAULT_MSG}}"

gitlink_check() {
  local links
  links=$(git -C "${PROJECTS_DIR}" ls-files -s | grep '^160000' || echo "")
  if [[ -n "$links" ]]; then
    echo "❌ GITLINKS DETECTED in aggregate repo:"
    echo "$links"
    echo "Fix: git -C ${PROJECTS_DIR} rm --cached -f <path> (the .git/ of that project is being tracked - remove it)"
    return 1
  fi
  echo "  ✅ No gitlinks. All content tracked as plain files."
  return 0
}

case "$cmd" in
  status)
    echo "=== Aggregate repo: ${PROJECTS_DIR} (-> projects_openclaw) ==="
    git -C "${PROJECTS_DIR}" status -sb | head -30
    echo ""
    gitlink_check
    ;;
  commit)
    echo "=== Staging changes in ${PROJECTS_DIR} ==="
    # Note: git add of a dir containing .git/ would re-create a gitlink; add by explicit
    # path below. Plain `git add -A` is safe because */.git/ is gitignored in the aggregate.
    git -C "${PROJECTS_DIR}" add -A
    if git -C "${PROJECTS_DIR}" diff --cached --quiet; then
      echo "  ℹ️  Nothing to commit."
    else
      git -C "${PROJECTS_DIR}" commit -m "${msg}"
      echo "  ✅ Committed: ${msg}"
      echo "  ℹ️  Push with: ./scripts/aggregate-sync.sh push"
    fi
    gitlink_check
    ;;
  push)
    echo "=== Pull --rebase + push (${PROJECTS_DIR}) ==="
    git -C "${PROJECTS_DIR}" pull --rebase
    git -C "${PROJECTS_DIR}" push
    echo "  ✅ Pushed to projects_openclaw"
    ;;
  sync)
    "${BASH_SOURCE[0]}" status
    "${BASH_SOURCE[0]}" commit "${msg}"
    "${BASH_SOURCE[0]}" push
    ;;
  check)
    gitlink_check
    ;;
  *)
    echo "Usage: $0 [status|commit [msg]|push|sync [msg]|check]"
    exit 1
    ;;
esac
