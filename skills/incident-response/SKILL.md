---
name: "incident-response"
description: "Structured incident management: detection, containment, restoration, RCA, and prevention."
---

# Workflow: Incident Response

## Purpose

Manage production incidents quickly, orderly, and repeatably.

Its priority is to restore service with the least possible impact.
It does not look for blame.
It seeks to minimize impact and generate learning.

## Philosophy

> Restore service first. Understand later. Improve forever.

Incidents are inevitable.
Improvisation is not.

## When to use

- Production outage
- Severe degradation
- Data loss
- Security issues
- Mass errors
- Abnormal latency increase
- Critical alerts
- Urgent rollback

## Severity

### SEV-1
System down. Data loss. Security issue. Immediate action.

### SEV-2
Important part of system degraded. Workaround exists.

### SEV-3
Localized problem. Moderate impact.

### SEV-4
Minor incident. Can wait.

## Phases

### 1. Detection
Identify: what happened, when it started, who detected it, available evidence. Do not assume causes. Record facts.

### 2. Classification
Determine: severity, scope, affected users, risk. Assign priority.

### 3. Containment
Reduce impact. Examples: rollback, feature flag OFF, disable endpoint, scale infrastructure, block traffic. Goal: prevent the incident from worsening.

### 4. Service Restoration
Restore service. Do not optimize. Do not refactor. Do not take the opportunity to "improve code." Only restore stability.

### 5. Root Cause Analysis
With the service stable. Answer: what happened? Why did it happen? Why wasn't it detected earlier? Why did it reach production?

Use: Five Whys, Timeline Analysis, Fishbone (optional). Never look for blame. Look for systemic causes.

### 6. Corrective Actions
Define: immediate fixes, permanent fixes, automations, new tests, new alerts, needed documentation. Each action must have an owner.

### 7. Knowledge Capture
Update: status, changelog, handoff, architecture decisions (if applicable), postmortem, lessons learned.

### 8. Prevention
Questions: how do we prevent it from happening again? What workflow should improve? What test was missing? What alert was missing? What documentation was missing? Generate backlog.

## Outputs
- Incident report
- Postmortem
- Incident timeline
- Root cause analysis
- Corrective actions
- Preventive actions
- Improvement backlog

## Postmortem Template

### Summary
### Impact
### Timeline
### Root Cause
### Contributing Factors
### Mitigation
### Recovery
### Corrective Actions
### Preventive Actions
### Lessons Learned

## Checklist
- Was service restored?
- Was evidence preserved?
- Is root cause documented?
- Are there preventive actions?
- Were documents updated?
- Did the incident improve the system?
- Could it happen again tomorrow?
