---
name: "tech-docs"
description: "Technical documentation: ADRs, README, API docs, CHANGELOG, architecture guides."
---

# Workflow: Technical Documentation

## What it does

Creation and management of project technical documentation: architecture decisions, README, API docs, CHANGELOG, contribution guides, and architecture design.

## Phases

### 1. Audience
Who reads these docs? (team devs, external contributors, end users, stakeholders)

### 2. Architecture Design (pre-ADRs)
Before documenting decisions, design the architecture:
- **C4/Mermaid diagrams** — context, containers, components, code
- **Trade-offs** — evaluate stack options, patterns, database
- **Dependency analysis** — project health, versions, compatibility
- **Technical risks** — identify early

### 3. Structure
What docs the project needs (README, API docs, guides, ADRs, CHANGELOG, CONTRIBUTING).

### 4. ADRs
Create or synchronize architectural decisions with standard format: context, decision, consequences, alternatives considered.

Reference patterns:
- **Hexagonal Architecture** — ports and adapters, inward dependencies
- **Clean Architecture** — layers, dependency rules
- **Domain-Driven Design** — bounded contexts, entities, value objects

### 5. Technical Writing
Write or update docs with concrete examples, not theory. Real code, not pseudocode.

### 6. Review
Coherence, completeness, examples work, links not broken, consistent tone.

### 7. Publication
Commit + push, integration with the project.

## Outputs
- README.md updated
- C4 architecture diagrams
- ADRs created or synchronized
- CHANGELOG.md updated
- API docs, technical guides
- CONTRIBUTING.md if applicable

## When to use
- When starting a new project (initial docs + design)
- When changing an API or feature (update docs)
- When closing an epic or milestone (update CHANGELOG + ADRs)
- When needing to document an architectural decision
- When a contributor needs clear guides
