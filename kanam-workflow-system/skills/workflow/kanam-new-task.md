# Kanam New-Task (Task Initialization Lifecycle)

> **Master workflow**: Initialize tasks from spec → create branch → implement → merge with unified lifecycle gates

---

## Purpose

Initialize and manage the complete task lifecycle within a Kanam Epic. This skill orchestrates: reading specification, creating isolated branch structure, implementing gated workflow, and coordinating PR creation for merged closure.

**Fusion source:** `workflow-kit/new-task` + `antigravity/new-task` + `chatgpt-project-architect` (task initiation patterns)

---

## Preconditions

Before invoking `kanam-new-task`, ensure these conditions are met:

1. **Specification exists**: `.kanam/TASK_SPEC.md` or equivalent spec file in Epic context
2. **Epic active**: Current Epic has `kanam-copilot` pre-flight passed and is being worked on
3. **Branch target identified**: Main branch (`main`) or feature branch for isolated task

---

## Invocation

```bash
# Initialize new task with project scoping
kanam-new-task --project "[Epic Name]" --task T0X:[Short Task Description] --spec ".kanam/TASK_SPEC.md"

# Auto-detect mode when no arguments provided
kanam-new-task
```

**Auto-mode behavior:**
- No arguments: Read `SKILL.md` and `.kanam/AGENT_TASKS.md` for current context, ask task initiation questions
- With `--project`: Contextualize task within Epic scope and dependencies
- With `--task`: Initialize task immediately if spec exists, create branch

---

## Unified Task Lifecycle (5 Steps)

### Step 1: Specification Validation & Context Reading

| Action | Source | Validate |
|--------|--------|----------|
| Read `.kanam/TASK_SPEC.md` or similar spec file in Epic context | Kanam spec system | Spec contains requirements, acceptance criteria, edge cases, dependencies |
| Read `SKILL.md` for base workflow instructions | SKILL.md | Master copilot workflow and gates understood |
| Check `.kanam/AGENT_TASKS.md` for current Epic active tasks | Active task list | Task not already assigned to another Epic task; no conflicts with ongoing work |

**Output:** Context summary + validation report

```markdown
### 📋 KANAM TASK INITIALIZATION REPORT

**Epic**: brainweb (AI assistant notes app)
**Task**: T0X — AI Copilot Drawer feature integration

### ✅ Preconditions Met
[✓] Specification exists: `.kanai/TASK_SPEC.md`
[✓] Epic active: brainweb with `kanam-copilot` pre-flight passed
[✓] Branch target identified: `e4/t11-ai-copilot-drawer`

### 📊 Specification Summary
**Name**: AI Copilot Drawer Feature Integration
**Description**: Implement AI-powered auto-reply capability with draft state tracking
**Priority**: High (user-requested feature in backlog)
**Dependencies**: T08, T09, kanam-copilot base skill integration
**Acceptance Criteria**:
- Draft state visible to admin in Kanam dashboard
- Auto-reply flag opt-in/user-controlled
- Integration with kanam-copilot draft storage layer

### ⚠️ Potential Risks/Blockers
**Blocker**: Need access to existing draft storage schema in database
**Mitigation**: Request team review of current storage architecture; plan migration if necessary

---

Next Step: Create isolated branch structure
```

### Step 2: Isolated Branch Creation (Unified Naming)

| Action | Format | Constraint |
|--------|--------|------------|
| Create or switch to task-specific branch | `e[Epic]/t[N-Task]-[short-description]` (e.g., `e4/t11-ai-copilot-drawer`) | Branch name matches Epic naming convention; no special characters |

**Example:** For brainweb task T0X:
```bash
git checkout -b "e4/t11-ai-copilot-drawer"
```

**Branch rules:**
- Starts with `e[N]` (Epic number)
- Follows with `/t[N-Task]` format (task identifier in epic task list)
- Task description short, lowercase, no spaces replaced by hyphens
- No merge commits until actual PR creation via `kanam-pr`

**Auto-detection:** If branch already exists from previous task attempts, warn user to check if still valid; otherwise create new isolated branch.

### Step 3: Gate Structure Creation (Kanam Gated Workflow)

| Action | Format | Purpose |
|--------|--------|---------|
| Create gate directory structure | `.kanam/workflow/<task-name>/` | Organize task-specific workflows, checks, and validations |
| Initialize gate state files | `.kanam/workflow/<task-name>/status.md` | Track progress through gates (Pre-flight → Gate 0-4) |

**Example gate structure:**
```
.kanam/
└── workflow/
    └── ai-copilot-drawer/
        ├── status.md          # Current gate status
        ├── preflight-checks.md # Pre-flight validation checklist
        └── gates/
            ├── 0-branch.md     # Gate 0: Isolated branching
            ├── 1-impl.md       # Gate 1: Atomic implementation
            ├── 2-build.md       # Gate 2: Build verification
            ├── 3-changelog.md   # Gate 3: CHANGELOG registration
            └── 4-commit-pr.md   # Gate 4: Commit + PR review
```

**Auto-detect gates:** Based on task dependencies from spec, create necessary gate structure before implementation begins.

### Step 4: Implementation with Copilot Integration

| Action | Source | Block if fails |
|--------|--------|----------------|
| Implement task scope exclusively within Gate 1 rules | `kanam-copilot` + current spec | Feature creep or out-of-scope changes |
| If build fails in Gate 2, STOP and fix before proceeding | Real production build command (e.g., `npm run build`) | Types errors, broken references, compilation errors |
| Document changes in CHANGELOG.md immediately after implementation | Auto-update | Missed changelog entry blocking Gate 3 |

**Auto-mode integration:** When implementing task with Kanam copilot active:
- Read `.kanam/TASK_SPEC.md` for requirements
- Execute `kanam-copilot --task T0X` to validate implementation against spec
- If implementation diverges from spec, abort and revert to base branch

### Step 5: PR Creation and Merge Coordination

| Action | Format | Dependency |
|--------|--------|-------------|
| Create PR via GitHub API with structured description | `kanam-pr --project [Epic]` | Gate 2 (build) must pass, CHANGELOG entry created in Gate 3 |
| Run review locally before send | `git diff main...HEAD` + local linters | Any blocking linter errors fixed before PR submission |
| Merge when review approves | `git merge --no-ff main` (or use GitHub API) | PR state in API must be `ready_to_merge` with 0 open reviews |

**Auto-detect merge:** If branch already merged locally, check remote status and coordinate merge or creation accordingly.

---

## Invocation Examples

```bash
# Full lifecycle with project context
kanam-new-task --project "brainweb" --task T0X:"AI Copilot Drawer feature" --spec ".kanam/TASK_SPEC.md"

# Auto-init mode (asks scoping questions first)
kanam-new-task

# Gate-specific workflow
kanam-new-task --gate 2 --build-only --auto-fix
```

**Auto-mode:**
- No arguments: `kanam-copilot` and `.kanam/AGENT_TASKS.md` read → ask task initiation questions (which Epic? what scope?)
- With `--project`: Contextualize within current Epic + dependencies
- With `--task`: Immediately create branch if spec exists; otherwise ask clarifying questions

---

## Output Format

When executed via CLI, skill generates unified task initiation report with validation status and next steps:

```markdown
## 🔧 KANAM TASK INITIALIZATION COMPLETE

### 📋 Task Summary
**Epic**: brainweb (AI notes app with assistant features)
**Task**: T0X — AI Copilot Drawer feature integration
**Branch**: `e4/t11-ai-copilot-drawer`

### ✅ Preconditions Status
[✓] Specification exists: `.kanam/TASK_SPEC.md`
[✓] Epic active: brainweb with `kanam-copilot` pre-flight passed
[✓] Branch created successfully: `e4/t11-ai-copilot-drawer`
[ ] Gate structure initialized (pending)

### 🚧 Next Steps Required
1. Initialize gate structure in `.kanam/workflow/ai-copilot-drawer/`
2. Create pre-flight validation checklist based on spec requirements
3. Begin implementation with `kanam-copilot` active
4. Run Gate 2 build verification after initial code changes

### 📊 Risk Assessment
**Blocker**: No critical blockers identified at initialization stage
**Mitigation**: Team review of storage architecture planned for Gate 1 (implementation phase)

---

Action: Confirm branch creation and start implementation with `kanam-copilot` integration.
```

---

## Anti-Patterns (Do Not Do)

- ❌ Don't create PR without pre-flight validation — this guarantees rework and merge conflicts
- ❌ Don't skip Gate 2 build check — dev mode builds are insufficient for production commits
- ❌ Don't write code outside task scope — feature creep is strictly forbidden by Kanam workflow rules

---

*Last updated: 2026-07-19 • Kanam AI System v0.1 • Fusion source documented in MANIFESTO.md*
