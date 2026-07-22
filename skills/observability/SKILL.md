---
name: "observability"
description: "System and process observability: instrumentation, metrics, tracing, and analysis."
---

# Workflow: Engineering Observability

## Purpose

Make the state of the product, infrastructure, and engineering system observable.

Does not fix problems.
Does not optimize.

Its responsibility is to answer:

> What is happening?
> Why did it happen?
> How do we know?

## Philosophy

> You can't improve what you can't observe.

Every important decision should be backed by data.
Observability does not exist to generate dashboards.
It exists to reduce uncertainty.

## When to use

- Before optimizations
- After incidents
- Before retrospectives
- After releases
- Periodically (health checks)
- When degradations appear
- When a workflow seems inefficient

## Observability Layers

### Product
Answer: how do users use the product? Where do they drop off? What features do they use? What errors do they encounter?

### Application
Answer: what endpoints fail? What routes are slow? Where are exceptions? What requests degrade?

### Infrastructure
Answer: CPU, RAM, disk, network, database, cache, workers, queues.

### Engineering System
Answer: what workflows are executed? How long do they take? Which fail? Which generate rework? What agent intervened? What cost did they have? What decisions did they produce?

## Phases

### 1. Instrumentation Audit
Verify observability coverage: application, infrastructure, database, APIs, agents, workflows, events.

### 2. Metrics
Define KPIs.

**Engineering:** Lead Time, Cycle Time, MTTR, Deployment Frequency, Change Failure Rate.

**Quality:** Post-release bugs, coverage, regressions.

**Performance:** Response Time, Throughput, Error Rate, P95, P99.

**Agents:** Time per workflow, tokens consumed, estimated cost, retries, tasks completed.

### 3. Logging
Verify: structured logs, correlation IDs, request IDs, user IDs (anonymized). No sensitive information.

### 4. Tracing
Follow a complete operation. Example: User → Frontend → API → LLM → MCP → Database → Response. Detect bottlenecks.

### 5. Alerting
Classify alerts: Critical, Major, Minor, Informational. Avoid alert fatigue.

### 6. Dashboard Review
Verify dashboards exist for: product, backend, frontend, infrastructure, AI, workflows, releases.

### 7. Trend Analysis
Compare: last week, last month, last quarter. Answer: are we improving? Where did we get worse? What trend is concerning?

### 8. Recommendations
Generate actions. Example: reduce latency, add tracing, instrument endpoint, add metric, remove useless dashboard. Never modify automatically.

## Outputs
- Observability report
- Health score
- Metrics list
- Alerts
- Bottlenecks
- Recommendations
- Dashboard checklist

## Minimum Metrics

### Engineering
Deployment Frequency, Lead Time, MTTR, Change Failure Rate.

### Application
Availability, Error Rate, Latency P95, Latency P99, CPU, RAM, DB Response Time.

### AI
Daily cost, tokens, duration per workflow, most executed workflow, workflow with most errors, workflow with most rework.

### Quality
Coverage, Build Success Rate, PR Approval Time, Accessibility Score, Lighthouse.

## Checklist
- Can we explain every incident with data?
- Are all workflows measurable?
- Are there duplicate metrics?
- Are there unused dashboards?
- Do alerts generate actions?
- Do metrics help decide?
- Can we demonstrate the system is improving?
