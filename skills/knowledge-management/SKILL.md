---
name: "knowledge-management"
description: "Knowledge base governance and synchronization. Maintains a single source of truth."
---

# Workflow: Knowledge Management

## Purpose

Manage persistent project knowledge throughout its lifecycle.

Does not develop features.
Does not modify business code.

Its responsibility is to keep documentation consistent, up-to-date, and useful for humans and agents.

## Philosophy

> Every decision deserves a home.

Documentation is not a deliverable.
It is shared memory.
Every important piece of knowledge should exist once and be easily discoverable.

## When to use

- After completing a workflow
- Before starting a new session
- Before creating a PR
- After closing an epic
- After a retrospective
- When architectural decisions change
- When inconsistencies appear

## Known Artifacts

### Strategic
- BRIEF.md
- EVALUATION.md
- DEFINITION.md
- ROADMAP.md

### Architecture
- ARCHITECTURE.md
- DATA_MODEL.md
- DESIGN.md
- Architecture decisions

### Status
- STATUS.md
- TRACKER.md
- HANDOFF.md

### Project
- README.md
- CHANGELOG.md
- CONTRIBUTING.md

### Memory
- Session logs

## Principles

Single Source of Truth.
Do not duplicate knowledge.
Document decisions, not conversations.
Prefer updating over creating new files.
Eliminate obsolete knowledge.
Maintain traceability.

## Phases

### 1. Discovery
Detect: what documents exist, which are missing, which are empty, which seem abandoned. Build a knowledge map.

### 2. Ownership
Determine the owner of each piece of information. Examples: architecture → ARCHITECTURE.md, technical decision → ADR, current status → STATUS.md, history → CHANGELOG.md. Never duplicate.

### 3. Consistency Audit
Look for contradictions. Examples: roadmap says "OAuth pending" but status says "OAuth done" → inconsistency. ADR indicates Hexagonal but README describes MVC → inconsistency. Generate report. Never modify automatically.

### 4. Freshness
Detect old knowledge. Questions: how long since last update? Is it still valid? Does it reference deleted files? Does it talk about features that no longer exist?

Classify: 🟢 Current, 🟡 Review, 🔴 Obsolete.

### 5. Knowledge Graph
Relate information. Example: Feature → Epic → ADR → PR → CHANGELOG → HANDOFF → STATUS. Build cross-references.

### 6. Compression
Reduce redundancy. Look for: repeated text, repeated tables, repeated examples, duplicated decisions. Propose consolidation. Never delete automatically.

### 7. Evolution
Detect: documents that should be split, documents that are too small, new documents needed, unnecessary documents. Propose improvements.

### 8. Publishing
Update index. Verify links. Verify references. Update dates. Generate final report.

## Outputs
- Knowledge report
- Knowledge map
- Inconsistencies found
- Obsolete documents
- Missing documents
- Consolidation proposals
- Knowledge graph

## Checklist
- Does a single source exist for each decision?
- Are there contradictions?
- Are there abandoned documents?
- Are there broken references?
- Is there duplication?
- Is there undocumented knowledge?
- Can the project be understood without reading chat history?
