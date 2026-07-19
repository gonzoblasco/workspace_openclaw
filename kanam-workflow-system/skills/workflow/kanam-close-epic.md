# Kanam Close-Epic (Formal Epic Closure)

> **Epic closure ritual**: Security audit → CHANGELOG entry → release tag → merge → final validation with unified blocking gates

---

## Purpose

Execute formal epic closure protocol ensuring all security audits pass, documentation is complete, and changes are properly tagged and released. This skill orchestrates the final consolidation of multi-phase work into a maintainable codebase state.

**Fusion source:** `workflow-kit/close-epic` + `antigravity/close-epic` + `kanam-pr` (PR merge coordination)

---

## Preconditions

Before invoking `kanam-close-epic`, these conditions must be satisfied:

1. **All gates passed**: Gates 0-4 successfully completed (branch, impl, build, changelog, commit+review)
2. **Security audit complete**: `kanam-security-audit` found no CRITICAL findings (multi-tenancy leaks or auth guard failures)
3. **Pr review approved**: `kanam-pr-review` returned `APPROVED` verdict with 0 blocking changes
4. **CHANGELOG documented**: All substantially modified files listed in `[Unreleased]` section of `CHANGELOG.md`
5. **Branch clean**: No uncommitted changes, all diffs merged into main

---

## Invocation

```bash
kanam-close-epic --project "[Epic Name]" --version "X.Y.Z" [--auto-tag] [--changelog-file path]

# Auto-detect mode when no arguments provided
kanam-close-epic
```

**Auto-mode behavior:**
- No arguments: Read `SKILL.md` and `.kanam/AGENT_TASKS.md` for current Epic context, ask version scoping questions
- With `--project`: Contextualize within current Epic scope and coordinate existing task closures
- With `--version`: Set semantic version number for release (e.g., `1.0.0`, `2.3.4`)
- With `--auto-tag`: Automatically create Git tag after merge without prompt

---

## Unified Closure Workflow (6 Steps)

### Step 1: Pre-Closure Validation Check

| Action | Source | Validate |
|--------|--------|----------|
| Verify all gates passed | Gate status files in `.kanam/workflow/` | All 5 gates completed successfully with no blocked findings |
| Security audit cleared | `kanam-security-audit --quiet` output | **NO CRITICAL** findings remain (multi-tenancy or auth guard failures) |
| PR review approved | `kanam-pr-review` last run verdict | Verdict = `APPROVED` with no blocking changes pending |

**Block if any validation fails:** Epic closure cannot proceed until all preconditions met. Report findings to team lead for remediation planning.

```markdown
### 🔒 KANAM EPIC CLOSURE VALIDATION REPORT

**Epic**: brainweb (AI notes app)
**Version Target**: 1.0.0

### ✅ Pre-Closure Checklist Status
[✓] Gate 0 completed: Branch created and merged
[✓] Gate 1 completed: Implementation scoped correctly
[✓] Gate 2 completed: Build passed with no type errors
[✓] Gate 3 completed: CHANGELOG updated with all changed files
[✓] Gate 4 completed: Review approved, changes merged
[✓] Security audit cleared: No CRITICAL findings (kanam-security-audit)
[✓] PR review approved: kanam-pr-review returned APPROVED

### ⚠️ Risk Assessment
All pre-closure validations passed. Epic ready for closure procedure.

**Next Step**: Proceed to formal closure workflow
```

### Step 2: CHANGELOG Update & Release Notes Generation

| Action | Format | Source |
|--------|--------|--------|
| Add entry to `[Unreleased]` section in CHANGELOG.md | One bullet per substantially modified file + semantic version note | CHANGELOG generator or manual review |
| Generate release notes from task descriptions | Markdown list with features/bugfixes/changelog links | `kanam-pr-review` output + task specs |

**CHANGELOG entry format:**
```markdown
### [1.0.0] 2026-07-19

#### Features
- AI Copilot Drawer feature (T0X) — Auto-reply draft state tracking

#### Bugfixes
- Auth guard on protected routes (multi-tenancy leak fix)

#### Other Changes
- Multi-tenancy data isolation strengthened per security audit requirements
```

**Auto-detect changes:** If branch merged, `git diff main...HEAD` extracts changed files; otherwise ask user to provide list of modified files.

### Step 3: Version Tag Creation (Semantic)

| Action | Format | Auto-tag? |
|--------|--------|-----------|
| Create semantic version Git tag | `git tag vX.Y.Z` (e.g., `v1.0.0`, `v2.3.4`) | Optional, prompted if not specified |
| Tag with commit message | `chore(release): release v1.0.0 brainweb` | Auto-create if `--auto-tag` provided |

**Version naming:**
- SemVer format: `X.Y.Z` (major.minor.patch)
- Prefix `v` for version tags (e.g., `v1.0.0`)
- Update `package.json` version field and CHANGELOG entry match

**Auto-detect version:** If no version specified, read package.json or ask user to provide target version number based on release history.

### Step 4: PR Coordination & Merge Preparation

| Action | Format | Dependency |
|--------|--------|-------------|
| Check PR status in GitHub API | `GET /repos/{owner}/{repo}/pulls/{number}` | PR must exist with state = `ready_to_merge` |
| Verify merge method choice | Method always `merge` (never squash) | Preserves task-level commit history |
| Coordinate team review if needed | Ask for approval or coordinate with lead reviewer | Blocker: If any open reviews, wait for approval |

**Auto-detect PR state:** If branch already merged locally and on remote, verify merge complete; otherwise prepare for new PR creation.

### Step 5: Tagging & Release Coordination

| Action | Format | Purpose |
|--------|--------|---------|
| Create Git tag with semantic version | `git tag vX.Y.Z` + commit message | Semantic versioning for release tracking |
| Verify tag on remote repository | `git push origin vX.Y.Z` | Push tag to GitHub for CI/CD and public visibility |
| Coordinate team notification (if applicable) | Slack/Email notification | Inform team of release availability |

**Auto-detect if needed:** If user specified `--auto-tag`, automatically create tag without additional prompts.

### Step 6: Final Cleanup & Validation

| Action | Format | Blocker |
|--------|--------|---------|
| Clean up uncommitted files in branch | `git status --untracked-files=all` | Uncommitted changes must be cleared for clean merge |
| Verify no open issues related to task | GitHub API issue queries | Open high-priority issues require triage before closure |
| Generate release announcement if public release | Draft PR/commit announcing feature | Ensure team aware of what's been released |

**Auto-detect cleanup:** If branch has any remaining changes, warn user to clean up before final merge.

---

## Invocation Examples

```bash
# Full closure ritual with version control
kanam-close-epic --project "brainweb" --version "1.0.0" --auto-tag

# Auto-detect mode (asks release scoping questions first)
kanam-close-epic

# Gate-specific workflow if any issues detected
kanam-close-epic --verify-gates-only
```

**Auto-mode:**
- No arguments: `kanam-copilot` and `.kanam/AGENT_TASKS.md` read → ask release version scoping questions (which Epic? what target version?)
- With `--project`: Contextualize within current Epic scope, coordinate existing task closures
- With `--version`: Set semantic version number for release with auto-tagging

---

## Output Format

When executed via CLI or IDE analysis, skill generates unified epic closure report with findings and blocking status:

```markdown
## 🏁 KANAM EPIC CLOSURE REPORT — [Project/Epic Name]

### ✅ Closure Steps Completed Successfully

| Step | Status | Details |
|------|--------|---------|
| Pre-Closure Validation | ✓ Passed | All gates passed, security audit cleared |
| CHANGELOG Update | ✓ Added | Entry added to `[Unreleased]` section |
| Version Tag Creation | ✓ Created | `v1.0.0` tag created with commit message |
| PR Coordination | ✓ Ready | Merge method: merge (no squash) |
| Final Cleanup | ✓ Verified | No uncommitted changes, team notified |

### 📊 Release Summary

**Epic**: brainweb (AI notes app with assistant features)
**Version Tagged**: v1.0.0
**Release Date**: 2026-07-19

**Changes Released:**
- AI Copilot Drawer feature integration (T0X task completed)
- Multi-tenancy data isolation strengthening
- Auth guard implementation on protected routes

### 🛡️ Security Status

**Kanam Security Audit**: PASSED with no CRITICAL findings
**Multi-Tenancy Isolation**: Verified (company_id filter on all queries)
**Auth Guards**: Implemented and validated (no auth bypass vulnerabilities)

---

Action: Epic closure complete. Version v1.0.0 tagged and ready for distribution.
```

---

## Anti-Patterns (Do Not Do)

- ❌ Don't close Epic without running security audit first — multi-tenancy leaks cost orders of magnitude more than dev time
- ❌ Don't tag releases without proper version tracking — semantic versioning ensures CI/CD and public visibility stay in sync
- ❌ Don't skip team notification coordination — silent releases cause confusion and missed feature adoption

---

*Last updated: 2026-07-19 • Kanam AI System v0.1 • Fusion source documented in MANIFESTO.md*
