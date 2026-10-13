#!/bin/bash
# initial-setup.sh - One-shot setup for a fresh machine (laptop / new Mac)
#
# Brings the workspace + projects up:
#   1. Workspace  -> clone or update workspace_openclaw
#   2. Container  -> ensure the flat `projects/` folder exists (NOT a repo)
#   3. Sub-repos  -> clone every gonzoblasco/<slug> into projects/<slug>/
#   4. Verify     -> repo count, remotes, clean status
#
# Model (ADR-098; clarified by Gonzo 2026-10-13):
#   `projects/` is a FLAT container folder, ignored 100% by the workspace git.
#   Each `projects/<slug>/` is its OWN git repo (source of truth, with its own
#   `.knowledge/`). There is NO aggregate repo layer (retired; the old
#   `projects_openclaw` aggregate is archived).
#
# Safe & idempotent: re-running does nothing destructive. Nothing is deleted.
#
# Usage:
#   ./scripts/initial-setup.sh                     # full setup (default)
#   ./scripts/initial-setup.sh --dry-run           # show plan, change nothing
#   ./scripts/initial-setup.sh --pull              # also pull existing repos
#   ./scripts/initial-setup.sh --workspace <dir>   # workspace location (default ~/.openclaw/workspace)
#
# Requirements: git, gh CLI authenticated (https://github.com/gonzoblasco)

set -euo pipefail

DO_PULL=0
DRY_RUN=0
WORKSPACE_DIR="${HOME}/.openclaw/workspace"
GH_OWNER="gonzoblasco"
WORKSPACE_URL="https://github.com/${GH_OWNER}/workspace_openclaw.git"

# --- arg parsing ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --pull) DO_PULL=1 ;;
    --workspace)
      WORKSPACE_DIR="${2:-}"
      if [[ -z "${WORKSPACE_DIR}" ]]; then
        echo "Error: --workspace requires a path"; exit 1
      fi
      shift
      ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//' | head -30
      exit 0
      ;;
    *)
      echo "Unknown option: $1 (try --help)"
      exit 1
      ;;
  esac
  shift
done

WORKSPACE_DIR="${WORKSPACE_DIR%/}"
PROJECTS_DIR="${WORKSPACE_DIR}/projects"

say()  { printf '%s\n' "$*"; }
info() { printf '  %s\n' "$*"; }
ok()   { printf '  ✅ %s\n' "$*"; }
warn() { printf '  ⚠️  %s\n' "$*"; }
fail() { printf '  ❌ %s\n' "$*"; }

# --- preflight ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌿 initial-setup.sh - workspace + projects setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Target workspace: ${WORKSPACE_DIR}"
[[ "${DRY_RUN}" == "1" ]] && echo "MODE: dry-run (nothing will change)"
echo ""

command -v git >/dev/null 2>&1 || { echo "❌ git not found"; exit 1; }
if ! command -v gh >/dev/null 2>&1; then
  echo "❌ GitHub CLI (gh) not found. Install: brew install gh && gh auth login"
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "❌ gh is not authenticated. Run: gh auth login"
  exit 1
fi

# --- 1. workspace ---
setup_workspace() {
  local WS_CLONED=0
  echo "=== 1. Workspace (${WORKSPACE_DIR}) ==="
  if [[ "${DRY_RUN}" == "1" ]]; then
    if [[ -d "${WORKSPACE_DIR}/.git" ]]; then
      info "Already a git repo -> would pull ($(git -C "${WORKSPACE_DIR}" remote get-url origin 2>/dev/null || echo no-remote))"
      [[ "${DO_PULL}" == "1" ]] && info "would run: git pull --rebase"
    elif [[ ! -d "${WORKSPACE_DIR}" ]]; then
      info "Would clone ${WORKSPACE_URL}"
    else
      info "Exists but is not a git repo - would SKIP (manual review needed)"
    fi
    return 0
  fi

  if [[ -d "${WORKSPACE_DIR}/.git" ]]; then
    url=$(git -C "${WORKSPACE_DIR}" remote get-url origin 2>/dev/null || echo "")
    if [[ "${url}" != *"workspace_openclaw"* ]]; then
      fail "workspace points at ${url}, expected workspace_openclaw. Check manually."
      return 1
    fi
    ok "workspace already cloned (${url})"
    [[ "${DO_PULL}" == "1" ]] && { git -C "${WORKSPACE_DIR}" pull --rebase -q; ok "workspace pulled"; }
  elif [[ ! -d "${WORKSPACE_DIR}" ]]; then
    mkdir -p "$(dirname "${WORKSPACE_DIR}")"
    git clone -q "${WORKSPACE_URL}" "${WORKSPACE_DIR}"
    ok "workspace cloned"
    WS_CLONED=1
  else
    fail "workspace dir exists but is not a git repo. Refusing to touch it."
    return 1
  fi
  WORKSPACE_FRESH="${WS_CLONED}"
}

# --- 2. container (projects/ is a flat folder, NOT a repo) ---
setup_container() {
  echo ""
  echo "=== 2. Projects container (${PROJECTS_DIR}) ==="
  if [[ -e "${PROJECTS_DIR}/.git" ]]; then
    # Under ADR-098 projects/ must NOT be a repo. A .git here is leftover from
    # the retired aggregate layer - report it, never delete without review.
    fail "projects/ has a .git of its own - it must be a plain folder (ADR-098)."
    fail "Inspect it manually before removing (could be the old aggregate checkout)."
    return 1
  fi
  if [[ ! -d "${PROJECTS_DIR}" ]]; then
    if [[ "${DRY_RUN}" == "1" ]]; then
      info "Would create the flat folder ${PROJECTS_DIR}"
    else
      mkdir -p "${PROJECTS_DIR}"
      ok "flat projects/ folder ready (not a repo)"
    fi
  else
    ok "projects/ is a plain folder (correct)"
  fi
}

# --- 3. individual repos ---
is_in() { # needle haystack...
  local needle="$1"; shift
  for item in "$@"; do [[ "$item" == "$needle" ]] && return 0; done
  return 1
}

clone_preserving() {
  local slug="$1"
  local dir="${PROJECTS_DIR}/${slug}"
  local tmp; tmp="$(mktemp -d)"
  local kept_k=0 kept_readme=0

  [[ -e "${dir}/.knowledge" ]] && { mv "${dir}/.knowledge" "${tmp}/.knowledge"; kept_k=1; }
  [[ -f "${dir}/README.md" ]] && { mv "${dir}/README.md" "${tmp}/README.md"; kept_readme=1; }

  if gh repo clone "${GH_OWNER}/${slug}" "${dir}" -- --quiet 2>"${tmp}/clone.err"; then
    # If a local .knowledge existed, the on-disk local version wins over the
    # repo's committed copy (it may carry unsynced memory).
    if [[ "${kept_k}" == "1" ]]; then
      rm -rf "${dir}/.knowledge"
      mv "${tmp}/.knowledge" "${dir}/.knowledge"
    fi
    if [[ "${kept_readme}" == "1" ]]; then
      if [[ -f "${dir}/README.md" ]]; then
        if ! diff -q "${tmp}/README.md" "${dir}/README.md" >/dev/null 2>&1; then
          mv "${tmp}/README.md" "${dir}/README.md.local-backup"
          info "${slug}: local README differed - kept as README.md.local-backup"
        else
          rm -f "${tmp}/README.md"
        fi
      else
        mv "${tmp}/README.md" "${dir}/README.md"
      fi
    fi
    echo "  ✅ ${slug}: cloned"
    rm -rf "$tmp"
    return 0
  fi

  # Clone failed (dir not empty). Fallback: give the folder its own .git
  # (init + fetch + reset to the individual repo = source of truth).
  local reset_ok=0
  if git -C "${dir}" init -q -b main 2>/dev/null \
     && git -C "${dir}" remote add origin "https://github.com/${GH_OWNER}/${slug}.git" 2>/dev/null \
     && git -C "${dir}" fetch -q origin 2>"${tmp}/fetch.err"; then
    # Reset may fail (worktree files the repo does not want to overwrite).
    # Try clean reset first, then with a stash of the offending files.
    if git -C "${dir}" reset --hard -q origin/main 2>/dev/null; then
      reset_ok=1
    elif git -C "${dir}" stash -q 2>/dev/null \
         && git -C "${dir}" reset --hard -q origin/main 2>/dev/null \
         && git -C "${dir}" stash pop -q 2>/dev/null; then
      reset_ok=1
    fi
  fi
  if [[ "${reset_ok}" == "1" ]]; then
    # Local .knowledge wins over the repo's committed copy.
    if [[ "${kept_k}" == "1" ]]; then
      rm -rf "${dir}/.knowledge"
      mv "${tmp}/.knowledge" "${dir}/.knowledge"
    fi
    if [[ "${kept_readme}" == "1" ]]; then
      [[ ! -f "${dir}/README.md" ]] && mv "${tmp}/README.md" "${dir}/README.md" || rm -f "${tmp}/README.md"
    fi
    echo "  ✅ ${slug}: git attached to existing source"
    rm -rf "$tmp"
    return 0
  fi

  [[ "${kept_k}" == "1" ]] && mv "${tmp}/.knowledge" "${dir}/.knowledge"
  [[ "${kept_readme}" == "1" && -f "${tmp}/README.md" ]] && mv "${tmp}/README.md" "${dir}/README.md"
  fail "${slug}: could not clone or attach git ($(tail -1 "${tmp}/clone.err" 2>/dev/null || tail -1 "${tmp}/fetch.err"))"
  rm -rf "$tmp"
  return 1
}

setup_subrepos() {
  echo ""
  echo "=== 3. Individual repos (gonzoblasco/<slug>) ==="
  local remote_repos=()
  while IFS= read -r line; do remote_repos+=("$line"); done < <(gh repo list "${GH_OWNER}" --json name --limit 200 --jq '.[].name' 2>/dev/null || true)

  for dir in "${PROJECTS_DIR}"/*/; do
    [[ -d "$dir" ]] || continue
    slug="$(basename "$dir")"
    if [[ "$(git -C "${dir}" rev-parse --show-toplevel 2>/dev/null)" == "${dir%/}" ]]; then
      info "${slug}: already cloned"
      if [[ "${DO_PULL}" == "1" ]]; then
        git -C "${dir}" pull --rebase -q origin main && info "  pulled"
      fi
      continue
    fi
    if [[ "${DRY_RUN}" == "1" ]]; then
      if is_in "${slug}" "${remote_repos[@]}"; then
        info "${slug}: would clone (preserving .knowledge/)"
      else
        info "${slug}: no repo on GitHub (local only)"
      fi
      continue
    fi
    if ! is_in "${slug}" "${remote_repos[@]}"; then
      warn "${slug}: no repo on GitHub (local only)"
      continue
    fi
    clone_preserving "${slug}"
  done
}

# --- 4. verify ---
verify() {
  echo ""
  echo "=== 4. Verification ==="
  local with_git=0 total=0
  for d in "${PROJECTS_DIR}"/*/; do
    [[ -d "$d" ]] || continue
    total=$((total + 1))
    if [[ "$(git -C "$d" rev-parse --show-toplevel 2>/dev/null)" == "${d%/}" ]]; then
      with_git=$((with_git + 1))
    fi
  done
  ok "${with_git}/${total} projects have their own .git"

  if [[ -e "${PROJECTS_DIR}/.git" ]]; then
    fail "projects/ is a git repo - it must be a plain folder (ADR-098)."
  else
    ok "projects/ is a plain folder (no aggregate repo layer)"
  fi

  if [[ -d "${WORKSPACE_DIR}/.git" ]]; then
    dirty=$(git -C "${WORKSPACE_DIR}" status --porcelain --untracked-files=no | wc -l | tr -d ' ')
    if [[ "${dirty}" == "0" ]]; then
      ok "workspace clean (only untracked cosmetic entries)"
    else
      warn "workspace has ${dirty} tracked changes (review before committing)"
    fi
  fi

  echo ""
  echo "  workspace -> $(git -C "${WORKSPACE_DIR}" remote get-url origin 2>/dev/null || echo '?')"
  echo "  projects  -> (flat folder; each <slug>/ is its own repo)"
}

# --- run ---
setup_workspace
setup_container
setup_subrepos

verify

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ "${DRY_RUN}" == "1" ]]; then
  echo "🌿 dry-run complete - nothing changed. Re-run without --dry-run to apply."
else
  echo "🌿 setup complete. All repos are in place."
  echo "   Work with each project directly: git -C projects/<slug> ..."
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
