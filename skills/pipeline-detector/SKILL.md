---
name: "pipeline-detector"
description: "Build detection pipelines combining deterministic local rules with contextual AI analysis"
---

# Pipeline Detector

Use to build tools that scan inputs (code, config, infra) for issues by combining **fast deterministic detectors** with **contextual analysis**. The pattern: local rules catch the obvious quickly with zero false positives; contextual analysis catches the subtle, assigns severity, and detects false positives.

## When to use

- Code review / linting tools
- Security audit scanners
- PR analysis bots
- Infrastructure (CloudFormation/Terraform) validators
- Team standards / quality dashboards

The pattern works wherever you scan many inputs and need both speed (deterministic) and judgment (contextual).

## Core pattern

```
Input → [Deterministic detectors] → [Contextual analyzer] → Structured report
```

1. **Deterministic detectors** — regex, AST parsing, heuristics. Fast, repeatable, zero false positives. Catch what's obvious.
2. **Contextual analyzer** — assigns severity, detects false positives, suggests remediation. Can be real AI or simulated with rules.
3. **Structured report** — merge both, with severity, confidence, remediation. Human validates the final call.

## Rules

- **Deterministic first.** Detect with local rules before any AI. AI is for judgment, not for finding the obvious.
- **AI is a filter, not a gatekeeper.** It comments, flags, scores — it does not block. Only objective rules (team standards) may block.
- **Severity + confidence + remediation** for every finding. A list of problems without severity and fix is not actionable.
- **Detect false positives.** AI hallucinates; so do naive detectors. The analyzer must flag probable FPs (e.g. secrets in test files, XSS in non-UI files).
- **Score the result.** A single 0-100 score (or 1-10) with color threshold makes the report usable and trackable.
- **Escalate on repetition.** Multiple findings of the same type in one file = higher severity.

## Workflow

1. Define the contract: what are you scanning, what issues matter, what's the report shape.
2. Build deterministic detectors first (one per issue type). Each returns `{ file, line, type, snippet, risk }`.
3. Add a contextual analyzer that: assigns severity, detects false positives, generates remediation, computes a score.
4. Merge into a structured report (markdown/JSON) with severity ordering and prioritized recommendations.
5. Validate: run against a deliberately-broken input to confirm detectors fire; run against clean input to confirm no false positives.
6. Iterate rules based on real results (falsos positivos → adjust).

## Report shape

A good report has:
- **Executive summary** — score, total findings, critical count
- **Findings table** — file, line, type, severity, description
- **Per-category detail** — grouped by issue type
- **Prioritized recommendations** — critical/high first, with concrete remediation
- **False positives flagged** — so the human knows what to ignore

## Simulating AI

When you don't have an AI API, simulate contextual analysis with rules:
- Severity escalation on repetition (≥3 same-type findings in a file → bump)
- False-positive heuristics (test files, non-UI files, missing DB imports)
- Remediation map (issue type → concrete fix)
- Score = f(count, max severity, FP ratio)

This keeps the architecture identical so you can swap in real AI later.

## Verification

Before shipping a detector pipeline:
- ✅ Fires on a deliberately-broken sample (each detector catches its type)
- ✅ Clean on a well-written sample (no false positives)
- ✅ Report is actionable (severity + remediation, not just a list)
- ✅ Score reflects reality (bad input → low score, good input → high)

## Examples

The pattern was built 5 times in the AI Engineering Bootcamp:
- N3: CLI code review tool (style + complexity detectors + report)
- N5: Security audit CLI (secrets, injection, deps + AI analyzer)
- N6: PR review commenter (diff analysis + GitHub comment)
- N8: CloudFormation validator (port mismatch, health checks, exposed ports)
- N9: Team standards validator (standards.json + dashboard score)

See `references/` for the reusable detector templates.
