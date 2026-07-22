---
name: "dependency-management"
description: "Dependency health, risk assessment, and governance throughout the project lifecycle."
---

# Workflow: Dependency Management

## Purpose

Keep the dependency ecosystem healthy, secure, and sustainable throughout the project lifecycle.

Does not install dependencies automatically.
Does not update versions without evaluation.

Its goal is to minimize technical risk while allowing the stack to evolve.

## Philosophy

> Every dependency is a long-term commitment.

Adding a dependency is incorporating third-party code into your project.
Each new dependency must justify its existence.

## When to use

- Adding a new library
- Updating dependencies
- Removing dependencies
- Reviewing vulnerabilities
- Preparing an important release
- Framework migrations
- Periodic audits

## Phases

### 1. Inventory
Build inventory. Record: dependency, version, usage, type (runtime/dev), size, maintainer, license. Detect: orphaned dependencies, duplicates, critical transitive dependencies.

### 2. Health Assessment
Evaluate health. Answer: active maintenance? Last release? Number of contributors? Open issues? Average response time? Release frequency? Deprecated?

Classify: 🟢 Healthy, 🟡 Watch, 🔴 Risk.

### 3. Risk Analysis
Evaluate: breaking changes, CVEs, compatibility, lock-in, critical dependency, abandonment risk. Calculate risk level.

### 4. Update Strategy
Classify updates: Patch, Minor, Major. For each: benefit, risk, effort, rollback plan.

### 5. Dependency Review
Before adding a new library, answer: Can we solve it with the language standard? Does an equivalent library already exist? Do we have another dependency doing the same thing? How much code are we importing? Is maintenance reliable? What will migration cost in the future?

Never add a dependency without justification.

### 6. Compatibility Check
Verify: framework, runtime, language version, bundler, testing, CI/CD, cloud. Do not assume compatibility.

### 7. Migration Planning
If a major update exists. Generate: plan, risks, steps, rollback, needed tests. Do not implement.

### 8. Knowledge Capture
Update: changelog, architecture decisions (if architecture changes), README (if installation changes). Record: why it was adopted, why it was removed, why it was postponed.

## Outputs
- Dependency report
- Dependency inventory
- Risk matrix
- Health report
- Update plan
- Migration plan
- Recommendations

## Checklist
- Are there unused dependencies?
- Are there vulnerabilities?
- Are there outdated versions?
- Is there duplication?
- Is there unnecessary lock-in?
- Is the license compatible?
- Does the update have rollback?

## Principles
- Fewer dependencies mean less risk surface
- Every dependency must justify its existence
- Updating incrementally reduces risk
- Critical vulnerabilities have priority
- Stability is worth more than having the latest version
- Dependency decisions must be documented
