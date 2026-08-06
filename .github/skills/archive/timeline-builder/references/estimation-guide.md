# Estimation Guide

## Why Estimation Is Hard

- Unknowns are unknown until you start
- Dependencies multiply uncertainty
- Parkinson's Law: work expands to fill available time
- Hofstadter's Law: it always takes longer than you expect, even when you account for Hofstadter's Law

## Estimation Techniques

### 1. Three-Point Estimation
```
Optimistic: 2 days
Most likely: 5 days
Pessimistic: 12 days

Expected = (O + 4M + P) / 6 = (2 + 20 + 12) / 6 = 5.7 days
```

### 2. T-Shirt Sizing
| Size | Meaning | Range |
|------|---------|-------|
| XS | Trivial change | < 1 day |
| S | Small feature | 1-3 days |
| M | Medium feature | 3-5 days |
| L | Large feature | 1-2 weeks |
| XL | Epic | 2-4 weeks |

### 3. Reference Class Forecasting
Find a similar past task and use its actual time as your baseline. Adjust for differences.

### 4. Decomposition
Break into sub-tasks until each is < 1 day. Sum them. Add 30-50% for integration and unknowns.

## Common Pitfalls

- **Optimism bias:** "This time it'll be different" — it won't
- **Anchoring:** First number you hear sticks — get multiple estimates
- **Ignoring non-coding time:** Reviews, testing, deployment, communication — add 40-60%
- **Assuming full focus:** Nobody codes 8 hours straight — plan for 4-5 productive hours/day
- **Forgetting dependencies:** "I just need the API" — and the API team has their own timeline

## Rules of Thumb

- Double your first estimate, then move up one unit (days → weeks, weeks → months)
- If a task is "simple, just..." — it's not simple
- The last 10% takes 50% of the time (polish, edge cases, testing)
- Estimate in ranges, not points: "3-5 days" not "5 story points"
