---
name: "performance-optimization"
description: "Evidence-based performance optimization: measure, understand, optimize, verify."
---

# Workflow: Performance Optimization

## Purpose

Improve system performance through evidence, measurement, and incremental optimizations.

Does not develop new features.
Does not fix functional bugs.
Does not chase arbitrary metrics.

Its mission is to eliminate real bottlenecks.

## Philosophy

> Measure. Understand. Optimize. Verify.

Never optimize by intuition.
Never sacrifice maintainability for micro-optimizations.
Optimize where there is measurable impact.

## When to use

- Low Lighthouse scores
- High response times
- Excessive CPU consumption
- Excessive memory consumption
- Slow queries
- Large bundles
- Degradation after releases
- User growth

## Domains

### Frontend
Rendering, hydration, bundle size, images, fonts, CSS, JavaScript.

### Backend
CPU, memory, concurrency, APIs, serialization, cache.

### Database
Indexes, N+1, joins, locks, execution plans.

### Infrastructure
CDN, cache, compression, scalability, workers, queues.

### AI
Tokens, prompts, context, embeddings, RAG, model latency.

## Phases

### 1. Baseline
Measure. Never start optimizing. Record: times, consumption, current metrics. Build baseline.

### 2. Profiling
Find bottlenecks. Tools: Chrome Performance, React Profiler, CPU Profiler, Heap Snapshots, EXPLAIN ANALYZE, flamegraphs.

### 3. Bottleneck Analysis
Classify: CPU, memory, I/O, network, database, rendering, LLM, cache. Identify the dominant bottleneck. Never optimize multiple at once.

### 4. Optimization Strategy
Choose the minimal intervention. Examples:
- Frontend: memoization, virtualization, code splitting, lazy loading, image optimization
- Backend: caching, batching, streaming, async, pooling
- Database: indexes, query rewrite, eliminate N+1
- AI: prompt compression, context pruning, caching, embeddings, reranking

### 5. Implementation Planning
Define: expected impact, risk, effort, rollback. Do not write code. Generate plan.

### 6. Verification
Measure again. Compare against baseline. Answer: did it actually improve? How much? Were there regressions?

### 7. Cost / Benefit
Evaluate: how much did it cost to optimize? How much did it improve? Is it worth it? Avoid premature optimizations.

### 8. Knowledge Capture
Update architecture decisions (if architecture changes), changelog, performance notes. Record before/after benchmark.

## Outputs
- Performance report
- Baseline
- Performance profile
- Bottlenecks
- Optimization plan
- Benchmark before/after
- Recommendations

## Checklist
- Does baseline exist?
- Does profiling exist?
- Is there evidence?
- Was the dominant bottleneck identified?
- Was the improvement measured?
- Was it documented?
- Were there regressions?

## Principles
- Measurement precedes optimization
- Optimizing the dominant bottleneck produces the greatest impact
- An unmeasured improvement is an opinion
- Simplicity is still a performance requirement
- The best code is the code that doesn't need to run
