---
name: "oss-contribute"
description: "Find, evaluate, and contribute to open source repos strategically — from pipeline building to PR submission and maintainer feedback handling."
---

# OSS Contribute

Use when contributing to open source repos as part of a visibility/job-search strategy. Covers the full cycle: finding repos, evaluating issues, forking, implementing, opening PRs, tracking, and responding to maintainer feedback.

## Prerequisites

- `gh` CLI authenticated
- Git configured (username, email, SSH keys)
- Fork remote convention: `fork` = your fork, `upstream` = original repo (NOT `origin` = upstream which is the common default but confusing)

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

## Phase 2.5 — Triage: before investing time, check for competing PRs

This is the most important lesson from real experience. Before implementing anything:

1. **Search for existing PRs referencing the issue:**
   ```bash
   gh pr list --repo <repo> --search "<issue-number>" --state open --json number,title,additions,deletions
   ```
2. **Evaluate competition:**
   - **0 PRs** → green light, proceed
   - **1 PR** → read it, assess if yours can be better (more complete, better tests, cleaner approach). If theirs is good, consider a review comment instead of a competing PR.
   - **2-3 PRs** → only proceed if you have a clearly superior approach. Otherwise, review the best one.
   - **4+ PRs** → skip. The maintainer is overwhelmed with options. Your PR won't stand out.
3. **Read competing PRs:** compare their approach, file coverage, test quality, and any maintainer comments. Look for:
   - Missing files (e.g., a PR that fixes styles but not the registry source)
   - Missing tests (positive AND negative coverage)
   - Breaking changes not flagged
   - Pre-existing flaky tests (verify by running tests on main without your change)
4. **Decide: PR or review?** Sometimes the highest-value contribution is a technical review on someone else's PR — it demonstrates expertise without creating noise.

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

> ⚠️ **Workspace files must stay out of PRs.** `HANDOFF.md` and any other workspace-specific files (notes, tracking, memory) must NEVER be committed to the upstream repo clone. If you create them inside the clone, add them to the clone's `.git/info/exclude` (local-only ignore) immediately. See Lessons learned — Session 2026-07-15.

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
7. **Pre-commit guard:** before committing, run `git status` and verify only repo-relevant files are staged. No `HANDOFF.md`, no notes, no workspace artifacts.

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
5. **Post-submission guard:** verify PR files with `gh pr view <number> --repo <repo> --json files --jq '.files[].path'`. If any workspace file (HANDOFF.md, notes, etc.) leaked in, remove it immediately and force-push.

## Phase 4.5 — Reviewing competing PRs (high-value alternative to opening your own)

When you decide not to open a PR (saturated issue, better approach exists), leave a technical review instead:

1. **Fetch the PR diff:** `gh pr diff <number> --repo <repo>`
2. **Clone the repo and check out the PR branch** to run tests locally:
   ```bash
   git fetch upstream pull/<number>/head:pr-<number>
   git checkout pr-<number>
   ```
3. **Analyze for gaps the PR author missed:**
   - Floating promises (Promise.race where one branch never settles)
   - Missing cleanup (subscribers, event listeners not unsubscribed)
   - Missing positive test coverage (tests verify the fix but not that the original behavior still works)
   - Breaking changes not flagged in the PR body or changeset
   - Adapter-breaking signature changes (e.g., changing a function signature in core that framework adapters don't update)
   - Bundle size impact
4. **Write a constructive review** — be specific, provide code examples, don't just say "good job":
   - Acknowledge what's right about the approach
   - List concerns with numbered points
   - Suggest concrete fixes with code snippets
   - Compare approaches if multiple PRs exist (maintainers appreciate this)
5. **Post the review:** `gh pr comment <number> --repo <repo> --body-file /tmp/pr-review.md`

Reviews build reputation too. A well-written technical review on a popular repo is visible to the maintainer, the PR author, and anyone watching the repo.

## Phase 4.6 — Responding to automated review bots

Many repos use CodeRabbit or similar AI review bots. They leave actionable comments:

1. **Read each comment carefully** — bots often flag real issues (curly braces, missing types, etc.)
2. **Apply valid suggestions immediately** — don't argue with the bot, just fix
3. **Force-push the amended commit:**
   ```bash
   git add -A && git commit -S --amend --no-edit
   git push fork <branch> --force
   ```
4. **The bot will re-review automatically** after the push
5. **Skip suggestions that don't apply** — but mention why if challenged by the bot

## Phase 4.7 — Responding to human maintainer requests

When a maintainer (MEMBER/OWNER association) leaves a review comment requesting a change on your PR:

1. **Fetch the comment context:**
   ```bash
   gh api repos/<repo>/pulls/<number>/comments --jq '.[] | select(.user.login == "<maintainer>") | {id, path, body, line}'
   gh pr view <number> --repo <repo> --json reviews,comments,state
   ```
2. **Verify current state before acting** — the branch may already be clean:
   - Check the PR's current files: `gh pr view <number> --repo <repo> --json files --jq '.files[].path'`
   - Fetch the branch and inspect locally if needed
   - If a squash/rebase already removed the offending file, the PR is already clean — skip to step 5
3. **Implement the requested change:**
   - Clone/fetch the branch if not already local
   - Make the change (remove file, fix code, add test, etc.)
   - Verify: build, lint, tests
   - Commit and push (force-push if amending)
4. **Verify on GitHub** that the PR now reflects the change:
   ```bash
   gh pr view <number> --repo <repo> --json files --jq '.files[].path'
   ```
5. **Reply to the maintainer** on the specific comment thread:
   ```bash
   gh pr comment <number> --repo <repo> --body "Hi @<maintainer> — done! <brief explanation of what was done or that it was already clean>"
   ```
   - Be concise and friendly
   - If the change was already done (e.g., via a previous rebase), say so briefly — no need to over-explain
   - Reference the specific request in your reply so the thread reads naturally

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
- **Don't commit workspace files (HANDOFF.md, notes, memory) to upstream repo clones** — they leak into PRs and look unprofessional

## Lessons learned (from real sessions)

### Session 2026-07-14 — shadcn/ui + TanStack/router + vercel/ai

**What worked:**
- Checking competing PRs before implementing saved hours (shadcn #11104 had 4 PRs, we skipped it)
- Opening PRs on issues with 0 competing PRs (#11161, #7787) — highest chance of merge
- Comparing approaches across competing PRs and leaving reviews — builds reputation without noise
- SSH commit signing configured once, benefits all future repos
- Responding to CodeRabbit immediately (curly braces) kept the PR clean

**What didn't work:**
- Repos where every issue already has PRs (shadcn/ui is very active — bugs get covered within hours)
- Issues that are actually upstream bugs (shadcn #10543 Select misalignment → Base UI library, not shadcn)
- Issues that are hard to reproduce (#9399 hydration error "sometimes", #10509 headless Chromium only)
- TanStack/query issues: very competido (3-4 PRs per issue) — better to review than compete

**Key insights:**
- **Registry vs styles:** In shadcn/ui, the `apps/v4/registry/` files are the SOURCE — `apps/v4/styles/` are DERIVED. A PR that only fixes styles is incomplete. Always fix the registry source and run `pnpm registry:build`.
- **Pre-existing flaky tests:** Always verify a failing test fails on `main` too (git stash, run, git stash pop). Don't claim your change broke it.
- **Monorepo install:** TanStack monorepo is huge — `pnpm install` can timeout. Use `pnpm --filter <pkg> install` to install only what you need, then `pnpm --filter <pkg> build` to build dependencies.
- **PR body with backticks:** `gh pr create --body` with backticks gets mangled by zsh. Use `--body-file /tmp/pr-body.md` instead.
- **HANDOFF.md in projects/:** Since `projects/` is in `.gitignore`, the HANDOFF lives in the cloned repo, not the workspace. That's fine — it survives in the clone.

### Session 2026-07-15 — TanStack/router #7818: maintainer feedback + workspace file leak

**What happened:**
- LadyBluenotes (TanStack MEMBER) reviewed PR #7818 and asked to remove `HANDOFF.md` from the PR
- The file had been committed in an intermediate commit, then removed by a later squash/rebase
- GitHub still showed it in the review context (CodeRabbit reviewed the commit that had it), but the PR HEAD no longer included it
- Verified with `gh pr view --json files` — only the 2 intended files remained
- Replied to the maintainer confirming the file was already removed

**What worked:**
- Verifying PR state before acting — avoided unnecessary commits since the file was already gone
- Replying on the specific comment thread so the maintainer gets notified
- Quick response time (same day as the review)

**What didn't work:**
- `HANDOFF.md` was committed to the upstream clone in the first place — it should never have been in the repo
- No pre-commit guard caught it before pushing

**Key insights:**
- **Workspace files in upstream clones:** `HANDOFF.md`, tracking notes, and any workspace-specific files must never be committed to an upstream repo. If you create them inside the clone, immediately add them to `.git/info/exclude` (local-only ignore that doesn't modify the repo's `.gitignore`):
  ```bash
  echo "HANDOFF.md" >> .git/info/exclude
  ```
- **Verify before acting on maintainer requests:** Always check the current PR state (`gh pr view --json files`) before making changes. Squashes and rebases may have already resolved the issue.
- **GitHub shows intermediate commits in reviews:** Even after a squash, review bots and maintainers may reference commits that no longer exist in the branch history. The PR file list (`gh pr view --json files`) is the source of truth, not the review timeline.
- **Pre-commit guard:** Always run `git status` before committing and verify only repo-relevant files are staged.

## Context files

- `CONTRIBUTING.md` (workspace) — pipeline, tiers, rules of gold
- `MEMORY.md` (workspace) — dev profile, specialization, methodology
- `projects/<repo>/HANDOFF.md` — per-repo state (keep out of upstream commits!)
- `memory/YYYY-MM-DD.md` — session log
