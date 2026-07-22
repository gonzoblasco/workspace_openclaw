---
name: "engineering-governance"
description: "Continuous evolution of the engineering system: audit workflows, consolidate learnings, eliminate duplication."
---

# Workflow: Engineering Governance

## Purpose

Maintain and evolve the system of workflows, principles, and engineering standards.

Does not develop features.
Does not write product code.

Its client is the engineering operating system itself.

## Philosophy

> Build the system that builds the system.

The goal is not to optimize a project.
The goal is to continuously improve the organization that develops projects.

## When to use

- After closing a milestone
- After closing an important epic
- After several similar PRs
- After a retrospective
- When repetitive bugs appear
- When multiple workflows start duplicating responsibilities
- When industry best practices change

Never during task implementation.

## Inputs

- All workflows
- Architecture decisions
- Retrospectives
- Status documents
- Changelog
- Handoff documents
- Execution metrics
- Bugs
- Incidents
- Human feedback

## Phases

### 1. System Health Check
Answer: which workflows are almost never used? Which generate the most value? Which parts of the process create friction? Where do bottlenecks appear? What tasks are still manual?

### 2. Pattern Mining
Look for repetitive patterns. Examples: same checklist copied, same validations, same decisions, same prompts, same errors, same solutions. If a pattern appears repeatedly, propose extracting it.

### 3. Workflow Audit
Audit each workflow. Questions: does it have a single responsibility? Does it do too much? Does it unnecessarily depend on another? Is there duplication? Is it outdated? Does it respect engineering principles?

Classify: 🟢 Healthy, 🟡 Needs Review, 🔴 Needs Refactor.

### 4. Knowledge Consistency
Look for inconsistencies between documents. Detect contradictory documents. Never modify automatically. Generate recommendations.

### 5. Industry Review
Compare the engineering system with the state of the art. Look for new practices related to: AI Engineering, Agentic Systems, MCP, RAG, Testing, Accessibility, DevOps, Architecture, OSS.

Answer: what should we adopt? What should we abandon?

### 6. Governance Review
Verify: obsolete workflows, oversized workflows, mixed responsibilities, skills that should merge, overly generic skills.

Propose: merge, split, deprecation, new version. Never modify automatically.

### 7. Engineering Principles
Audit the principles. Questions: are they still valid? Are there contradictions? Is one missing?

Examples: Accessibility First, Security by Default, Progressive Disclosure, Small Commits, Spec Driven Development, HTML before ARIA, Documentation as Code.

### 8. Improvement Proposal
Generate RFCs. Each RFC must include: problem, evidence, proposal, impact, risks, migration. Never apply changes automatically.

## Outputs
- Governance report
- RFCs
- New workflow proposals
- Deprecation proposals
- Engineering principle improvements
- Engineering system improvement backlog

## Principles
- Stability is worth more than novelty
- Do not optimize without evidence
- Remove complexity before adding features
- Each workflow must have a single responsibility
- Improvements must be incremental
- Decisions must be documented
- Governance exists to reduce system entropy

## Final Checklist
- Is there duplication?
- Is there contradiction?
- Is there process debt?
- Are there obsolete workflows?
- Is there undocumented knowledge?
- Are there new patterns that deserve a workflow?
- Is the system better today than a month ago?
