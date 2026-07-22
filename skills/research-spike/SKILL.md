---
name: "research-spike"
description: "Reduce technical uncertainty through structured investigation before making decisions."
---

# Workflow: Research Spike

## Purpose

Reduce technical uncertainty through structured investigation.

Do not implement solutions.
Do not write production code.
Do not make definitive decisions.

Its mission is to answer:

> What do we need to learn before building?

## Philosophy

> Learn first. Build second.

A Spike buys knowledge, not features.
Its success is measured by uncertainty eliminated, not lines of code written.

## When to use

- New technology
- Unknown library
- External API
- Uncertain architecture
- Important decision
- Benchmark between alternatives
- Complex integration
- Proof of concept
- Viability doubts

## Phases

### 1. Research Question
Define a single question.

Examples:
- Should we use MCP or REST?
- Can we support 100k users?
- What are the limitations of this API?

Never investigate without a clear question.

### 2. Success Criteria
What evidence do we need to consider the question answered?

Examples:
- benchmark
- official documentation
- prototype
- integration test
- experiment

### 3. Scope
Define boundaries.
What we investigate.
What we do NOT investigate.
Maximum time.
Expected depth.
Avoid infinite research.

### 4. Information Gathering
Collect evidence.

Sources:
- Official documentation
- RFCs
- Repositories
- Issues
- Technical discussions
- Engineering blogs
- Benchmarks
- Own experiments

Prioritize primary sources.

### 5. Experimentation
If necessary, build a minimal prototype.
Do not reuse code.
Do not turn the Spike into production.

Goal: answer questions, not develop product.

### 6. Analysis
Compare alternatives.
For each option document:
- benefits
- risks
- cost
- maintenance
- scalability
- complexity
- maturity

### 7. Recommendation
Answer:
- What do we recommend?
- Why?
- What evidence supports this decision?
- What uncertainty remains?

Be explicit about confidence level.

### 8. Knowledge Capture
Update research notes, architecture decisions (if the decision is made), knowledge base, lessons learned.
Do not lose the generated knowledge.

## Outputs
- Research report
- Research notes
- Alternative comparison
- Experiment results
- Recommendation
- Open questions
- Identified risks

## Checklist
- Is there a concrete question?
- Is there sufficient evidence?
- Are sources reliable?
- Did the experiment answer the question?
- Is the recommendation supported?
- Is knowledge reusable?

## Principles
- Research has a time limit
- A good question is worth a hundred searches
- Evidence weighs more than opinions
- Prototypes are disposable
- Generated knowledge must remain in the project
- Not all research ends in implementation
