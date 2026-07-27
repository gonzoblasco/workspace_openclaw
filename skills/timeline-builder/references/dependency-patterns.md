# Dependency Patterns

## Types of Dependencies

### Finish-to-Start (FS) — Most Common
Task B can't start until Task A finishes.
```
[A: Design] ──→ [B: Implement]
```

### Start-to-Start (SS)
Task B can start once Task A has started.
```
[A: Write copy] ──→ [B: Design landing page]
```

### Finish-to-Finish (FF)
Task B can't finish until Task A finishes.
```
[A: Write docs] ──→ [B: Review docs]
```

### Start-to-Finish (SF) — Rare
Task B can't finish until Task A starts.
```
[A: New system goes live] ──→ [B: Old system shuts down]
```

## Dependency Patterns

### Sequential (Waterfall)
```
[A] → [B] → [C] → [D]
```
- **Pros:** Simple, predictable
- **Cons:** Slow, one bottleneck blocks everything
- **When:** Hard dependencies, small team, well-understood domain

### Parallel (Independent)
```
[A] ──→ [D]
[B] ──→ [D]
[C] ──→ [D]
```
- **Pros:** Fast, resilient
- **Cons:** Integration risk, coordination overhead
- **When:** Independent workstreams, large team

### Staggered (Pipeline)
```
[A1] → [A2] → [A3]
       [B1] → [B2] → [B3]
              [C1] → [C2] → [C3]
```
- **Pros:** Continuous delivery, no big bang
- **Cons:** Requires good architecture (feature flags, API versioning)
- **When:** Mature product, continuous deployment

## Critical Path

The longest chain of dependent tasks. Any delay here delays the whole project.

To find it:
1. List all tasks with dependencies
2. Calculate earliest start/finish for each
3. Calculate latest start/finish for each
4. Tasks where earliest = latest are on the critical path

## Buffer Strategies

- **Project buffer:** Add 20-30% at the end of the critical path
- **Feeding buffer:** Add buffer where non-critical paths feed into critical path
- **Resource buffer:** Have backup for key people (bus factor > 1)

## Red Flags

- One person on the critical path for multiple tasks → bottleneck
- Long chain of FS dependencies → fragile
- No parallel workstreams → slow
- External dependency with no SLA → risk
