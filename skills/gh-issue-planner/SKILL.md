---
name: "gh-issue-planner"
metadata:
  category: "Project Management"
  tags:
    - github
    - issues
    - planning
    - project-management
description: "Plan and break down a project into GitHub Issues (epics → stories → subtasks). Phase 0.4 of Product Discovery. ONLY for personal repos."
user-invocable: false
---

# Workflow: GitHub Issue Planner

## Purpose
Break down a project ROADMAP into GitHub Issues (epics → stories → subtasks) to sync the development team.

## ⚠️ INVOLABLE RULE
This workflow runs ONLY on **personal/owned repos**. NEVER on third-party repos (forks, contributions, PRs to external projects).

On third-party repos, planning stays in local docs (`.knowledge/ROADMAP.md`) or the session HANDOFF. To track progress, use `.knowledge/TRACKER.md` locally.

## Prerequisites
- `gh` CLI authenticated with repo permissions
- Repo created on GitHub
- ROADMAP.md completed (Product Discovery Phase 0.2)

## Routine

### Step 1: Configure labels

```bash
# Base labels
gh label create epic --color "B60205" --description "Epic: large work block"

# Per-sprint labels
gh label create sprint-1 --color "0E8A16" --description "Sprint 1"
gh label create sprint-2 --color "006BFF" --description "Sprint 2"
# ... as many sprints as needed

# Auxiliary labels
gh label create good-first-issue --color "7057FF" --description "Good for new contributors"
```

### Step 2: Create Epics

For each epic in the ROADMAP, create an issue with the `epic` label:

```bash
gh issue create --label epic --title "Epic N: Name — Short description" --body "$(cat templates/epic-template.md)"
```

**Epic Template:** (see `templates/epic-template.md`)

### Step 3: Create Stories

For each feature in a sprint, create an issue with the corresponding sprint label:

```bash
gh issue create --label sprint-N --title "Story name" --body "$(cat templates/story-template.md)"
```

**Story Template:** (see `templates/story-template.md`)

### Step 4: Create Subtasks

For each subtask of a story, create an issue referencing the parent story:

```bash
gh issue create --label sprint-N --title "[#PARENT_ID] Subtask name" --body "$(cat templates/subtask-template.md)"
```

The body must include `**Parent:** #[PARENT_ID]` to maintain hierarchy.

### Step 5: Mark good-first-issues

Identify 2-3 issues ideal for new contributors and add the label:

```bash
gh issue edit ISSUE_ID --add-label good-first-issue
```

### Step 6: Update Epic descriptions

Once all issues are created, update epic descriptions to be self-contained:

```bash
gh issue edit EPIC_ID --body "$(cat templates/epic-description.md)"
```

The epic description must include:
- **What this epic achieves** (overview)
- **What it includes** (feature list)
- **Who can pick these up** (suggested profile)
- **Success criteria** (how to know it's done)

## Templates

### epic-template.md
```
## 🏗️ Epic N: Name

### What this epic achieves
[General description]

### What it includes
- [Feature list]

### Success criteria
- [Criterion 1]
- [Criterion 2]
```

### story-template.md
```
## [Story name]

**Epic:** #[EPIC_ID]

### What to do
[One-line description]

### Subtasks
- [#ID] [Subtask name]
- [#ID] [Subtask name]

### Technical details
[Commands, snippets, config, references to .knowledge/]

### Success criteria
- [Criterion 1]
- [Criterion 2]
```

### subtask-template.md
```
**Parent:** #[PARENT_ID]

### What to do
[One-line description]

### Technical details
[Commands, snippets, references]

### Success criteria
- [Criterion 1]
```

### epic-description.md
```
## 🏗️ Epic N: Name — Short description

### What this epic achieves
[Overview: what the user/admin can do when this epic is complete]

### What it includes
- [Feature 1]
- [Feature 2]
- [Feature 3]

### Who can pick these up
[Suggested profile: frontend, backend, fullstack, etc.]

### Success criteria
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]
```

## Reference Scripts

### `scripts/create-sprint.sh`
Script to create all issues for a sprint at once. Takes:
- Sprint number
- CSV/JSON file with stories and subtasks

(Not yet implemented — pending until the pattern repeats 3+ times)

## Issue Hierarchy

```
Epic (label: epic)
  └── Story (label: sprint-N, body: "**Epic:** #[epic_id]")
        └── Subtask (label: sprint-N, title: "[#story_id] name", body: "**Parent:** #[story_id]")
```

## Naming Conventions

- **Epic:** `Epic N: Name — Short description`
- **Story:** `Descriptive feature name`
- **Subtask:** `[#PARENT_ID] Concrete action to perform`

## Related

- [Product Discovery](../product-discovery): Phase 0.4 of which this skill is part
- [Build & Scaffold](../build-scaffold): For building the project post-planning
