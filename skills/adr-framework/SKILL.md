---
name: "adr-framework"
description: "Maintain technical decision documentation system for product/technical teams. Create, update ADRs with decision, context, status tracking."
---

# ADR Framework Skill

## Purpose

Maintains a Decision Record (ADR) system for documenting technical decisions in OpenClaw workspace products. Ensures decisions are recorded, tracked, and linked to roadmaps.

## When to Apply

Trigger conditions:
- [ ] Decision made that affects future implementation (e.g., "Regeneration from scratch")
- [ ] Decision impacts multiple files across project
- [ ] Stakeholder decision needs documentation for future reference
- [ ] Team discussion reached consensus but needs record

## Execution Pipeline

```
[Decision Made] → Create ADR document with:
   ├─ Title (ADR-XXXX format)
   └─ Content (decision, context, alternatives considered)
   ↓
[Document] Write markdown file docs/ADR-XXXX.md
   └─ Include: decision, context, links to related decisions
   ↓
[Track Status] Update ADR with: implemented/pending/rejected/quarantined
   └─ Link in ROADMAP.md as reference
   ↓
[Maintain] Keep related docs synchronized (BRIEF, DEFINITION)
```

## Required Structure

Each ADR must include:
- **Title**: ADR-001 format (sequential number)
- **Decision**: Short one-line summary of what was decided
- **Context**: Multi-line context about why this decision matters
- **Status**: implemented | pending | rejected | quarantined
- **Links**: References to related ADRs, files, roadmaps

## Related Skills

- `workspace-scaffold` — Generates initial scaffold including docs structure
- `project-regeneration` — Uses ADR framework to document regeneration decisions

## Example Use Case

**ADR-001: Regeneration Strategy Decision**
```markdown
# Decision
Complete rebuild from scratch rather than incremental refactoring.

Context
12 commits with decisions never applied correctly
Legacy stack (Webpack + React 18) incompatible with current goals
Stakeholder agrees to start fresh
Impact: Zero technical debt, modern build system, full WAI-APG target

Status: Implemented - Regeneration completed
```
