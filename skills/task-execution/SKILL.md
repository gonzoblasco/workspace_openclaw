---
name: "task-execution"
description: "Day-to-day task execution: plan, implement, verify, PR, and close epic."
---

# Workflow: Task Execution

## What it does

Executes tasks from definition to completion: plan, implement, verify, create PR, merge, and close the epic.

## Phases

### 1. Intake
Read context of the active epic, acceptance criteria, relevant project files. Do not start writing code without understanding constraints.

### 2. Planning
Break task into subtasks of 2-5 minutes each, each with a clear verification ("how do I know it's done?"). Maximum 10 subtasks per plan. If more, split into multiple plans.

### 3. Branch
```bash
git checkout main && git pull origin main
git checkout -b task/E[N]-T[NN]-[short-description]
```

### 4. Implementation
Code + tests + types. Atomic commits: one change per commit, do not accumulate everything at the end.

### 5. Verification
```bash
npm run build    # must pass without errors
npm run dev      # test main flow manually
```

### 6. PR
Structured PR with:
- Title: `feat|fix|refactor(scope): description`
- Body: what it does, main changes, how to test, checklist
- Auto-review before merging

### 7. Merge
Merge to main preserving history (`--no-ff`). Do not delete the branch (historical reference).

### 8. Epic Close (when all tasks are complete)
- CHANGELOG: move `[Unreleased]` to new semver version
- Tags: `git tag -a E[N]-complete`
- Lessons learned documented
- Status updated

## Outputs
- Task plan
- Branch with atomic commits
- PR with structured description
- Epic closed with CHANGELOG and tags
