#!/bin/bash
# initial-setup.sh - One-shot setup for a fresh machine (laptop / new Mac)
#
# Brings the triple-git structure up to date:
#   1. Workspace  -> clone or update workspace_openclaw
#   2. Aggregate  -> set up projects/ as a clone of projects_openclaw (PRIVATE)
#   3. Sub-repos  -> clone every gonzoblasco/<slug> into projects/<slug>/
#   4. Verify     -> gitlink check, subrepo count, remotes, clean status
#
# Safe & idempotent: re-running does nothing destructive. Nothing is deleted.
# `.knowledge/` dirs are ALWAYS preserved (they belong to the workspace git).
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
AGGREGATE_REPO="projects_openclaw"
AGGREGATE_URL="https://github.com/${GH_OWNER}/${AGGREGATE_REPO}.git"
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
echo "🌿 initial-setup.sh - triple-git machine setup"
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

# --- 2. aggregate (projects/ -> projects_openclaw) ---
# projects/ holds .knowledge/ dirs from the workspace clone. The aggregate's
# checkout could overwrite the ones it tracks, so preserve them all first
# (same procedure verified on 2026-09-02 on the desktop).
setup_aggregate() {
  echo ""
  echo "=== 2. Aggregate repo (${PROJECTS_DIR} -> ${AGGREGATE_REPO}) ==="
  if [[ "${DRY_RUN}" == "1" ]]; then
    if [[ -d "${PROJECTS_DIR}/.git" ]]; then
      info "Already a repo -> would verify remote + $([[ ${DO_PULL} == 1 ]] && echo pull || echo skip-pull)"
    else
      info "Would init + fetch + reset --hard to ${AGGREGATE_REPO}/main"
      info "  (preserving all .knowledge/ dirs first)"
    fi
    return 0
  fi

  if [[ -d "${PROJECTS_DIR}/.git" ]]; then
    url=$(git -C "${PROJECTS_DIR}" remote get-url origin 2>/dev/null || echo "")
    if [[ "${url}" != *"${AGGREGATE_REPO}"* ]]; then
      fail "projects/ origin is ${url}, expected ${AGGREGATE_REPO}. Fix manually."
      return 1
    fi
    ok "aggregate already set up (${url})"
    [[ "${DO_PULL}" == "1" ]] && { git -C "${PROJECTS_DIR}" pull --rebase -q; ok "aggregate pulled"; }
    return 0
  fi

  if [[ ! -d "${PROJECTS_DIR}" ]]; then
    mkdir -p "${PROJECTS_DIR}"
  fi

  # Preserve workspace-owned content that the aggregate does not track
  local tmp; tmp="$(mktemp -d)"
  local preserved=0
  for d in "${PROJECTS_DIR}"/*/; do
    [[ -d "$d" ]] || continue
    slug="$(basename "$d")"
    if [[ -e "$d/.knowledge" ]]; then
      mkdir -p "${tmp}/knowledge/${slug}"
      mv "$d/.knowledge" "${tmp}/knowledge/${slug}/.knowledge"
      preserved=1
    fi
  done
  if [[ -f "${PROJECTS_DIR}/PROYECTOS.md" ]]; then
    mv "${PROJECTS_DIR}/PROYECTOS.md" "${tmp}/PROYECTOS.md"
  fi
  if [[ -f "${PROJECTS_DIR}/.gitignore-template" ]]; then
    mv "${PROJECTS_DIR}/.gitignore-template" "${tmp}/.gitignore-template"
  fi

  git -C "${PROJECTS_DIR}" init -q -b main
  git -C "${PROJECTS_DIR}" remote add origin "${AGGREGATE_URL}"
  git -C "${PROJECTS_DIR}" fetch -q origin
  git -C "${PROJECTS_DIR}" reset --hard -q origin/main

  # Restore workspace-owned content. Copy the CONTENTS (trailing /. ) so the
  # destination is a merge, never a nested .knowledge/.knowledge/.
  if [[ -d "${tmp}/knowledge" ]]; then
    for d in "${tmp}/knowledge"/*/; do
      slug="$(basename "$d")"
      mkdir -p "${PROJECTS_DIR}/${slug}/.knowledge"
      cp -Rf "$d/.knowledge/." "${PROJECTS_DIR}/${slug}/.knowledge/" 2>/dev/null
    done
    rm -rf "${tmp}/knowledge"
  fi
  [[ -f "${tmp}/PROYECTOS.md" ]] && mv "${tmp}/PROYECTOS.md" "${PROJECTS_DIR}/PROYECTOS.md"
  [[ -f "${tmp}/.gitignore-template" ]] && mv "${tmp}/.gitignore-template" "${PROJECTS_DIR}/.gitignore-template"
  rm -rf "$tmp"
  ok "aggregate cloned (${AGGREGATE_REPO}, all .knowledge/ preserved)"
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
    # .knowledge always comes back from the workspace (workspace version wins)
    if [[ "${kept_k}" == "1" ]]; then
      rm -rf "${dir}/.knowledge"
      mv "${tmp}/.knowledge" "${dir}/.knowledge"
    fi
    # Same triple-git rule as the fallback: repos that do NOT track .knowledge
    # in their history ignore it locally (the memory belongs to the workspace).
    if ! git -C "${dir}" ls-files --error-unmatch .knowledge >/dev/null 2>&1; then
      printf '\n# Triple-git: .knowledge/ belongs to the workspace git\n.knowledge/\n' >> "${dir}/.git/info/exclude"
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

  # Clone failed (usually: dir not empty because the aggregate checkout
  # already contains the source). Fallback: give the folder its own .git
  # (init + fetch + reset to the individual repo = source of truth).
  local reset_ok=0
  if git -C "${dir}" init -q -b main 2>/dev/null \
     && git -C "${dir}" remote add origin "https://github.com/${GH_OWNER}/${slug}.git" 2>/dev/null \
     && git -C "${dir}" fetch -q origin 2>"${tmp}/fetch.err"; then
    # Reset may fail (worktree files the repo does not want to overwrite,
    # e.g. .knowledge/ owned by the workspace). Try clean reset first, then
    # with a stash of the offending files.
    if git -C "${dir}" reset --hard -q origin/main 2>/dev/null; then
      reset_ok=1
    elif git -C "${dir}" stash -q 2>/dev/null \
         && git -C "${dir}" reset --hard -q origin/main 2>/dev/null \
         && git -C "${dir}" stash pop -q 2>/dev/null; then
      reset_ok=1
    fi
  fi
  if [[ "${reset_ok}" == "1" ]]; then
    # .knowledge: the workspace version wins over the repo's committed copy
    if [[ "${kept_k}" == "1" ]]; then
      rm -rf "${dir}/.knowledge"
      mv "${tmp}/.knowledge" "${dir}/.knowledge"
    fi
    # Repos that do NOT track .knowledge in their history should ignore it
    # locally (triple-git rule: the memory belongs to the workspace).
    if ! git -C "${dir}" ls-files --error-unmatch .knowledge >/dev/null 2>&1; then
      printf '\n# Triple-git: .knowledge/ belongs to the workspace git\n.knowledge/\n' >> "${dir}/.git/info/exclude"
    fi
    if [[ "${kept_readme}" == "1" ]]; then
      [[ ! -f "${dir}/README.md" ]] && mv "${tmp}/README.md" "${dir}/README.md" || rm -f "${tmp}/README.md"
    fi
    echo "  ✅ ${slug}: git attached to existing source (from aggregate checkout)"
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
    if git -C "${dir}" rev-parse --git-dir >/dev/null 2>&1; then
      info "${slug}: already cloned"
      if [[ "${DO_PULL}" == "1" ]]; then
        git -C "${dir}" pull --rebase -q && info "  pulled"
      fi
      continue
    fi
    if [[ "${DRY_RUN}" == "1" ]]; then
      if is_in "${slug}" "${remote_repos[@]}"; then
        info "${slug}: would clone (preserving .knowledge/)"
      else
        info "${slug}: no repo on GitHub (workspace memory only)"
      fi
      continue
    fi
    if ! is_in "${slug}" "${remote_repos[@]}"; then
      warn "${slug}: no repo on GitHub (workspace memory only)"
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
    if git -C "$d" rev-parse --git-dir >/dev/null 2>&1; then
      with_git=$((with_git + 1))
    fi
  done
  ok "${with_git}/${total} projects have their own .git (rest are workspace-memory only)"

  if [[ -d "${PROJECTS_DIR}/.git" ]]; then
    if git -C "${PROJECTS_DIR}" ls-files -s | grep -q '^160000'; then
      fail "gitlinks detected in the aggregate repo. Run: ./scripts/aggregate-sync.sh check"
    else
      ok "aggregate: no gitlinks (all content tracked as plain files)"
    fi
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
  echo "  projects  -> $(git -C "${PROJECTS_DIR}" remote get-url origin 2>/dev/null || echo '?')"
}

# --- run ---
setup_workspace
setup_aggregate
setup_subrepos

# Guarantee: every .knowledge/ tracked by the workspace git matches its index.
# (The aggregate checkout and the sub-repo resets may have restored repo
# versions of the same files - the workspace memory wins.)
if [[ -d "${WORKSPACE_DIR}/.git" ]]; then
  git -C "${WORKSPACE_DIR}" restore --worktree -- projects/ >/dev/null 2>&1 || true
fi

verify

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ "${DRY_RUN}" == "1" ]]; then
  echo "🌿 dry-run complete - nothing changed. Re-run without --dry-run to apply."
else
  echo "🌿 setup complete. All repos are in place."
  echo "   Next: sync the aggregate anytime with ./scripts/aggregate-sync.sh sync"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
