#!/bin/bash
# plan.sh — Genera plan de tarea estructurado
# Uso: ./plan.sh <epic> <task> <title> <output-dir>
# Output: archivo markdown con el plan

EPIC="${1:-E0}"
TASK="${2:-T00}"
TITLE="${3:-Untitled}"
OUTPUT_DIR="${4:-.}"

if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
fi

FILENAME="${OUTPUT_DIR}/${EPIC}-${TASK}-plan.md"

cat > "$FILENAME" << EOF
# Task: $TITLE

## Context
- **Epic:** $EPIC
- **Task:** $TASK
- **Date:** $(date +%Y-%m-%d)

## Acceptance Criteria
- [ ] TBD

## Plan

### Subtask 1: TBD (~5 min)
**Verification:** TBD
- [ ] Step 1

EOF

echo "{\"status\":\"done\",\"path\":\"$FILENAME\"}"
