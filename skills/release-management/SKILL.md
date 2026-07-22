---
name: "release-management"
description: "Coordinate safe releases to production: planning, strategy, communication, execution, and closure."
---

# Workflow: Release Management

## Purpose

Coordinate the release of new versions to production safely, predictably, and repeatably.

Does not validate quality — that belongs to pre-deploy-qa.
Does not develop features.
Does not fix bugs.

Its responsibility begins when the software is ready to be released.

## Philosophy

> Shipping is a business decision, not a Git command.

A release is not a deploy.
A release is putting new capability in users' hands.

## When to use

- Production release
- Internal release
- Beta
- Canary
- Hotfix
- Rollback
- Important milestone

## Release Strategies

### Full Release
All users.

### Canary
Small percentage. Monitor. Expand gradually.

### Feature Flags
Deploy now. Activate later.

### Blue / Green
Two environments. Instant switch. Fast rollback.

### Rolling
Gradual instances.

### Hotfix
Maximum priority. Simplified process.

## Phases

### 1. Release Planning
Define: version, objective, scope, included features, excluded features, risks, rollback plan.

### 2. Readiness Review
Verify: QA approved, build stable, tests green, documentation updated, changelog ready, decisions synchronized. Do not continue if any is missing.

### 3. Versioning
Apply SemVer. Major. Minor. Patch. Create tag. Verify consistency.

### 4. Deployment Strategy
Choose strategy. Justify decision.

### 5. Communication
Prepare: release notes, visible changes, breaking changes, needed migrations, affected stakeholders, support.

### 6. Release Execution
Coordinate: deploy, monitoring, quick validations, smoke tests. Do not modify code during this phase.

### 7. Post Release Verification
Verify: metrics, errors, latency, logs, health checks, early feedback. Do not close the release immediately.

### 8. Release Closure
Update: changelog, status, versions, release notes, lessons learned. Close release.

## Outputs
- Release plan
- Release notes
- Release checklist
- Rollback plan
- SemVer tag
- Release report

## Checklist

### Before
QA approved, build green, tests, documentation, versioning, rollback defined.

### During
Deploy, smoke tests, health checks, metrics, alerts.

### After
Observability, feedback, changelog, release notes, lessons learned.

## Integration

If the release fails → incident-response workflow
If concerning metrics appear → observability workflow
If the release completes successfully → session-lifecycle → engineering-governance (for important retrospectives)

## Principles
- Small releases are safer than huge releases
- Every release must be revertible
- Communication is part of the release
- The deploy ends when the system is stable, not when the pipeline finishes
- Every release must leave enough evidence to reconstruct what changed and why
