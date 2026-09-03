---
name: "complexity-driven-pipeline"
metadata:
  category: "Workflow"
  tags:
    - pipeline
    - complejidad
    - orquestacion
description: "Orquestacion complexity-first: scorer de complejidad antes de spawnear agentes A/B. Decide modelo, thinking level y profundidad de pipeline."
user-invocable: false
---

# complexity-driven-pipeline

> Complexity-first orchestration. Score before spawning.

## Purpose

Before any A/B pipeline task, Kanam runs the complexity scorer to decide: model, thinking level, and pipeline depth. This avoids over-engineering trivial tasks and under-engineering critical ones.

## Workflow

```
User objective
    │
    ▼
┌─────────────────────────────────────┐
│  1. COMPLEXITY SCORE                │
│     ./scripts/complexity-scorer.sh  │
│     "<objective>"                   │
│                                     │
│     Returns: T (1-20)               │
│     Bucket: trivial/low/medium/high │
└─────────────────┬─────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
 trivial       low/medium    high
 (T≤6)         (T7-16)      (T17-20)
    │             │             │
    ▼             ▼             ▼
 Kanam solo   A/B pipeline  Kanam(max)
                             + A(high)
                             + B(high)
                             + verification
                             + Gonzo confirm
```

## T-Score Buckets

| Bucket  | T-range | Pipeline | Model    | Thinking | A/B  |
|---------|---------|----------|----------|----------|------|
| trivial | 1-6     | Kanam direct | default | off      | none |
| low     | 7-12    | A → Kanam | default | high     | A    |
| medium  | 13-16   | A → B → Kanam | default | high     | A+B  |
| high    | 17-20   | Kanam(max) → A(high) → B(high) → verify | default | max+high | A+B+Kanam |

**Risk escalation (2026-08-31):** if `C >= 4` AND `T >= 14`, force the `high`
bucket even if low ambiguity (D) leaves the linear total below 17. This protects
dangerous-but-clear tasks (e.g. prod DB migration to sharding: T=16 but C=5) from
being under-pipelined. Output marks `escalated: 1`. Rationale: ambiguity can be
clarified, production data-loss risk cannot.

## Step-by-step

### 1. Score
```bash
./scripts/complexity-scorer.sh "<objective>"
```
Or inline in Kanam's thinking: apply the 4-dimension rubric manually (faster for trivial cases).

### 2. Initialize pipeline-track with T
```bash
./scripts/pipeline-track.sh init "<fase>" --score T U1 U2 ...
```
This persists the score for the run.

### 3. Execute
- **trivial**: Kanam executes directly. No agents.
- **low**: Agent A writes. Kanam reviews.
- **medium**: Agent A writes. Agent B cross-reviews (check against real docs/API). Kanam approves.
- **high**: Kanam designs in max thinking. Agent A writes in high. Agent B revises in high. Kanam verifies build. **Requires explicit Gonzo approval** (T≥17 gate).

### 4. Archive
After completion, if T ≥ 13:
- Write a line to today's daily: task + T-score + model + outcome.
- Optional: feed back to calibrate future scoring.

## Manual Scoring (without LLM)

When Ollama is unavailable, score manually:

- **A (Scope)**: 1=one file, 2=2-3 files, 3=multi-file module, 4=multi-module, 5=multi-repo
- **B (Abstraction)**: 1=trivial fix, 2=feature, 3=refactor, 4=design, 5=system arch
- **C (Risk)**: 1=cosmetic, 2=minor breakage, 3=feature broken, 4=significant, 5=critical/data loss
- **D (Ambiguity)**: 1=crystal clear, 2=mostly clear, 3=some interpretation, 4=needs research, 5=vague

T = A + B + C + D

## Key Rules

1. **No max thinking in agents A/B**  -  only in Kanam (orchestrator) for high-complexity design.
2. **T≥17 = Gonzo gate**  -  confirm before proceeding.
3. **trivial = no agents**  -  don't spawn agents for T≤6. Kanam handles it.
4. **Document in daily if T≥13**  -  builds a calibration dataset over time.
5. **Use pipeline-track**  -  always init with `--score T` so the run is auditable.

## Force Score (no LLM)

```bash
./scripts/complexity-scorer.sh --score 14 "rediseñar auth"
```
Use when Ollama is slow or unavailable.

## Files

- `scripts/complexity-scorer.sh` - main scorer (tries local qwen3.5:9b-mlx first, then cloud fallbacks)
- `scripts/complexity-parse.py` - external parser (handles strict JSON or prose/thinking text from local models)
- `scripts/pipeline-track.sh` - durable pipeline state (accepts `--score T`)

## Notes (2026-08-30)

- Local models (qwen3.5:9b-mlx) put the answer in the `thinking` field, not `response`, and often truncate before closing the JSON. The external parser handles both formats.
- Cloud models (deepseek-v4-flash:cloud, gemma4:cloud) may hit weekly usage limits; the scorer falls back gracefully and reports which model scored.

## Status

- Version: 1.0.0
- Created: 2026-08-30
- Depends on: `scripts/complexity-scorer.sh`, `scripts/pipeline-track.sh`
