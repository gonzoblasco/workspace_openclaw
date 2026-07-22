---
name: "debug-investigation"
description: "Systematic bug investigation to root cause. Diagnose before you prescribe."
---

# Workflow: Debug Investigation

## Purpose

Investigate software problems methodically until root cause is identified.

Do not implement fixes.
Do not refactor.
Do not optimize.

Its only mission is to answer:

> What is happening?
> Why is it happening?

## Philosophy

> Diagnose before you prescribe.

The first hypothesis is usually wrong.
Never modify code without evidence.
Symptoms are not the cause.

## When to use

- Bugs
- Inconsistent behavior
- Intermittent errors
- Performance degradation
- Race conditions
- Hard-to-reproduce problems
- Regressions
- User-reported errors

## Phases

### 1. Intake
Record: observed problem, environment, version, frequency, impact, available evidence. Never assume the cause.

### 2. Reproduction
Goal: reproduce the problem. Record: steps, data, configuration, browser, device, user. If it cannot be reproduced, document missing conditions.

### 3. Scope Analysis
Determine: always occurs, sometimes, only production, only development, only certain users, only certain data. Answer: what works correctly? That helps narrow the search space.

### 4. Evidence Collection
Collect: logs, stack traces, network, database, events, screenshots, videos, telemetry. Never delete evidence.

### 5. Hypothesis Generation
Generate multiple hypotheses. Do not fall in love with the first one. Order by probability.

### 6. Experiment Design
Design minimal experiments. Each experiment must answer a single question. Examples: add logging, mock dependency, change config, reduce dataset, disable feature flag. Never mix multiple changes.

### 7. Root Cause Analysis
When sufficient evidence exists. Document: immediate cause, systemic cause, contributing factors, why it was not detected. Do not look for blame. Look for mechanisms.

### 8. Handoff
Generate documentation for the implementation workflow. Must include: summary, evidence, discarded hypotheses, root cause, fix recommendation, risks, recommended tests.

## Outputs
- Debug report
- Reproduction steps
- Timeline
- Hypotheses
- Experiments
- Root cause
- Recommendation
- Suggested test cases

## Techniques

### Binary Search
Quickly reduce the search space.

### Git Bisect
Find the commit that introduced the problem.

### Rubber Duck
Explain the flow step by step.

### Five Whys
Find deep causes.

### Delta Debugging
Reduce to minimal reproducible case.

### Event Timeline
Reconstruct chronologically what happened.

## Checklist
- Is the bug reproducible?
- Is there sufficient evidence?
- Were hypotheses discarded?
- Does root cause exist?
- Does the proposed fix attack the cause, not the symptom?
- Are there tests to prevent regression?

## Principles
- Symptoms are deceptive
- Evidence weighs more than intuition
- Each experiment must answer a single question
- A good diagnosis is worth more than a quick fix
- Every important bug should leave reusable knowledge
