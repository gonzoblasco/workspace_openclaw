---
name: "oss-contribute"
description: "\"Find, evaluate, and contribute to open source repos strategically — from pipeline building to PR submission.\""
---

# OSS Contribute

Use when contributing to open source repos as part of a visibility/job-search strategy. Covers the full cycle: finding repos, evaluating issues, forking, implementing, opening PRs, and tracking.

## Prerequisites

- `gh` CLI authenticated
- Git configured (username, email, SSH keys)
- Fork remote convention: `origin` = upstream, `fork` = your fork

## Phase 1 — Pipeline building (strategic discovery)

When asked to find new repos to contribute to:

1. **Define the dev profile** — stack, specialization, tools they already use. Read `MEMORY.md` and `CONTRIBUTING.md` from the workspace for context.
2. **Search candidate repos** using `gh search repos` and `gh api`:
   - Filter by language (TypeScript, etc.), stars (500+), sort by activity
   - Check `pushed_at` (active in last 30 days), `open_issues_count`, `stargazers_count`
   - Cross-reference with what the dev actually uses (not just popular repos)
3. **Evaluate issues** per repo:
   - `gh search issues --repo <repo> --state open --label "help wanted"` and `"good first issue"`
   - Also check unlabeled bugs/enhancements with recent activity
   - Count issues updated in last 30 days as a proxy for maintainer responsiveness
4. **Classify into tiers:**
   - Tier 1: High visibility, active, aligned with specialization
   - Tier 2: Good but more effort or less activity
   - Tier 3: Interesting but cold
5. **Output a table** with: repo, stars, activity (30d), why it fits, specific issues found
6. **Update `CONTRIBUTING.md`** pipeline section with new repos

## Phase 2 — Issue selection and setup

When starting work on a specific repo/issue:

1. **Read `CONTRIBUTING.md`** from the workspace for rules of gold
2. **Read the repo's CONTRIBUTING.md** before touching anything
3. **Fork** if not already: `gh repo fork <repo> --clone=false`
4. **Clone** to `projects/<repo-name>/`:
   ```bash
   cd projects/
   git clone <upstream-url> <repo-name>
   cd <repo-name>
   git remote add fork <fork-url>
   ```
5. **Create branch:** `feature/<issue>-<short-description>` or `fix/<issue>-<description>`
6. **Read the issue** and all maintainer comments:
   ```bash
   gh issue view <number> --repo <repo> --json title,body,comments,labels,state
   ```
7. **Create `projects/<repo>/HANDOFF.md`** with: issue context, repo structure notes, plan

## Phase 3 — Implementation

1. **Read the repo structure** — understand conventions, test setup, lint config
2. **Implement the fix/feature** following repo conventions exactly
3. **Write tests** — if repo has tests, include them. If not, write them anyway.
4. **Verify:**
   ```bash
   # Adapt to repo's package manager and scripts
   npm run build && npm run lint && npm test
   # or: pnpm build && pnpm lint && pnpm test
   # or: bun run build && bun run lint && bun test
   ```
5. **Commits — semantic, one concern each:**
   - `feat(scope): description (#issue)`
   - `fix(scope): description (#issue)`
   - `test(scope): description (#issue)`
   - `docs(scope): description (#issue)`
6. **Never mix concerns** — one PR per issue. Split if needed.

## Phase 4 — PR submission

1. **Push to fork:**
   ```bash
   git push fork <branch-name>
   ```
2. **Create PR:**
   ```bash
   gh pr create --repo <upstream-repo> \
     --title "feat: concise title" \
     --body-file /tmp/pr-body.md
   ```
3. **PR description (English for international repos):**
   - What: what does this change do
   - Why: reference the issue (`Closes #N`)
   - How: approach taken, key decisions
   - Verification: build, lint, tests results
   - Notes: anything reviewers should know
4. **Reference the issue** in PR body: `Closes #N` or `Related to #N`

## Phase 5 — Tracking and follow-up

1. **Update `projects/<repo>/HANDOFF.md`:**
   - What was done
   - PR number and URL
   - What follows
2. **Update `memory/YYYY-MM-DD.md`** with session summary
3. **Update `CONTRIBUTING.md`** pipeline table (status column)
4. **Commit + push workspace:**
   ```bash
   cd /Users/gonzoblasco/.openclaw/workspace
   git add -A && git commit -m "oss: <repo> PR #<n> <description>" && git push
   ```
5. **Follow-up:** wait 1-2 weeks before pinging maintainers. Check PR comments with:
   ```bash
   gh pr view <number> --repo <repo> --json comments,reviews,state
   ```

## Red flags

- Don't open PRs without reading the repo's CONTRIBUTING.md
- Don't break CI — if it fails for repo reasons, note it in the PR
- Don't mix concerns in one PR
- Don't write placeholder/empty commits
- Don't open PRs in repos with no activity in 30+ days (nobody will review)
- Don't contribute to repos you don't use — domain knowledge is the advantage

## Context files

- `CONTRIBUTING.md` (workspace) — pipeline, tiers, rules of gold
- `MEMORY.md` (workspace) — dev profile, specialization, methodology
- `projects/<repo>/HANDOFF.md` — per-repo state
- `memory/YYYY-MM-DD.md` — session log
