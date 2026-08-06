# Skills Architecture

**Status:** Draft - audit baseline
**Date:** 2026-08-06
**Scope:** `skills/` catalog in `workspace_openclaw`

## Purpose

Define the architecture of the skill catalog before merging, deleting, or renaming skills.
The goal is not to minimize the raw number of files. The goal is to reduce ambiguous entry points,
prevent competing routers, and keep reusable capabilities discoverable.

## Inventory baseline

- 93 skill directories are tracked by git in `skills/`.
- 24 additional local skill directories are currently untracked copies from `addyosmani/agent-skills`.
- Those 24 files are byte-identical to the cloned Addy repository and must not be committed as duplicates.
- `SKILLS-INDEX.md` currently describes 93 skills.

## Catalog layers

Every skill should eventually have one primary layer:

| Layer | Purpose | Examples |
|---|---|---|
| Core workflow | General engineering lifecycle decisions | spec, plan, build, test, review, ship |
| Orchestration | Selecting and coordinating workers | orchestrator, execution, checkmate |
| Governance | Improving the OS and its knowledge | engineering governance, knowledge management |
| Session | Context, handoffs, lifecycle, compaction | session lifecycle, session context |
| Domain | Specialized technical or product knowledge | accessibility, Supabase, Godot |
| Integration | External tools and services | GitHub, DeepWiki, Photos, MCP |
| Personal | Non-engineering personal workflows | ADHD, calories, habits |
| Internal module | Reusable implementation detail, not a primary user entry point | handoff matrix, pipeline detector |

A skill can keep its own directory while being classified as an internal module. Classification comes before filesystem moves.

## Public entry-point rule

A public skill must represent a distinct workflow decision. It should have:

1. a clear trigger;
2. a distinct owner/responsibility;
3. a verification or exit condition;
4. no competing skill that claims the same default trigger.

Useful instructions do not automatically justify a separate public skill.

## Initial consolidation candidates

### Cluster A - Agents and execution

Current members:

- `agent-workflow`
- `dev-workflow-orchestrator`
- `orchestrator-agent`
- `execution-agent`
- `task-execution`
- `checkmate`

Initial hypothesis:

- Keep `orchestrator-agent` as the routing entry point.
- Keep `execution-agent` as the autonomous implementation entry point.
- Keep `checkmate` as the generic worker + judge verification pattern.
- Treat `agent-workflow`, `dev-workflow-orchestrator`, and `task-execution` as consolidation candidates or internal modules until distinct boundaries are proven.

### Cluster B - Session, context, and memory

Current members:

- `session-lifecycle`
- `session-context`
- `context-anchor`
- `context-aware-delegation`
- `handoff-matrix`
- `memory-agent`
- `context-slimmer`

Initial hypothesis:

- Keep `session-lifecycle` as the session workflow entry point.
- Keep `session-context` as persistent per-project state storage.
- Keep `memory-agent` as the durable knowledge consolidation entry point.
- Treat the remaining skills as sub-capabilities/modules unless they have independent triggers and verification.

### Cluster C - Quality and QA

Current members:

- `code-review-agent`
- `code-review-and-quality`
- `review-quality`
- `quality-gate`
- `qa-patrol`
- `pre-deploy-qa`

Initial hypothesis:

- Keep `code-review-and-quality` as the general review standard.
- Keep `qa-patrol` as browser/integration QA.
- Keep `pre-deploy-qa` as the release gate if its PWA/deploy-specific checks remain unique.
- Treat `code-review-agent`, `review-quality`, and `quality-gate` as orchestration/adapters pending evidence.

### Cluster D - Governance and learning

Current members:

- `engineering-governance`
- `governance-agent`
- `knowledge-management`
- `observability`
- `failure-memory`
- `pipeline-detector`
- `tide-watch`

Initial hypothesis:

- Keep `engineering-governance` as the system-improvement workflow.
- Keep `knowledge-management` as project knowledge ownership and consistency.
- Keep `observability` as measurement/instrumentation.
- Keep `failure-memory` as an evidence-based learning mechanism.
- Treat `governance-agent`, `pipeline-detector`, and `tide-watch` as adapters or internal modules unless independent operation is demonstrated.

## Provisional catalog decisions

| Skill | Provisional state | Rationale |
|---|---|---|
| `orchestrator-agent` | keep | Single routing entry point for agent work. |
| `execution-agent` | keep | Autonomous implementation entry point with scripts and validation loop. |
| `checkmate` | keep | Distinct worker + judge loop, usable beyond coding. |
| `agent-workflow` | candidate | Broad discipline; overlaps with orchestration and execution. |
| `dev-workflow-orchestrator` | candidate | Pipeline router overlaps with `agent-workflow`. |
| `task-execution` | candidate | Base workflow inherited by `execution-agent`; likely internal. |
| `session-lifecycle` | keep | Canonical lifecycle and already replaces prior session skills. |
| `session-context` | keep | Persistent SQLite-backed project context, distinct from lifecycle. |
| `memory-agent` | keep | Autonomous durable-memory maintenance entry point. |
| `context-anchor` | internalize | Post-compaction briefing capability. |
| `context-aware-delegation` | internalize | Context transfer capability for isolated agents/cron. |
| `handoff-matrix` | internalize | Handoff format, not a complete workflow. |
| `context-slimmer` | candidate | Specialized context optimization; retain pending usage evidence. |
| `code-review-and-quality` | keep | Canonical multi-axis review standard. |
| `qa-patrol` | keep | Browser/integration QA specialization. |
| `pre-deploy-qa` | keep | Deploy-specific gate with PWA checks. |
| `code-review-agent` | candidate | Agent wrapper over review workflow; likely adapter. |
| `review-quality` | candidate | Existing consolidated workflow wrapper; compare with canonical review standard. |
| `quality-gate` | candidate | Parallel validator + tester sync point; may become a review module. |
| `engineering-governance` | keep | Canonical AI Engineering OS evolution workflow. |
| `knowledge-management` | keep | Canonical project knowledge workflow. |
| `observability` | keep | Canonical measurement and instrumentation workflow. |
| `failure-memory` | keep | Evidence-based recurring-failure learning mechanism. |
| `governance-agent` | candidate | Agent wrapper over `engineering-governance`. |
| `pipeline-detector` | internalize | Reusable deterministic + contextual detection pattern. |
| `tide-watch` | candidate | Session-capacity monitor; evaluate as integration/module after usage review. |

These are hypotheses, not deletion instructions. No skill should be moved, merged, or deleted based only on this table.

## Decision states

Each catalog entry will eventually receive one state:

- **keep** - public entry point with unique responsibility;
- **merge** - content moves into a canonical skill;
- **internalize** - remains reusable but is not a top-level entry point;
- **adapter** - thin integration over a canonical workflow;
- **archive** - no current use or superseded;
- **candidate** - insufficient evidence; do not change yet.

## Evidence required before consolidation

Do not merge solely because two names sound similar. Collect:

- actual invocation history, if available;
- distinct triggers and outputs;
- scripts/references/tests owned by each skill;
- links from other skills and workspace rules;
- whether the skill is user-invocable or internal;
- whether removing it would make a real workflow harder to execute.

## Working hypothesis

The target is not a fixed number. A plausible steady state is:

- 25-35 public workflow entry points;
- 20-40 internal modules/adapters;
- domain and personal skills retained where they have distinct users and outputs.

The catalog should expose fewer ambiguous choices without flattening specialized capabilities.
