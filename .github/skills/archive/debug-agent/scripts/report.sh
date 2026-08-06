#!/bin/bash
# report.sh — Genera DEBUG_REPORT.md + JSON estructurado
# Uso: ./report.sh <output-dir> <json-input>
# El JSON se pasa por stdin

OUTPUT_DIR="${1:-.}"

if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
fi

# Leer JSON de stdin
INPUT=$(cat)

# Extraer campos
STATUS=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','unknown'))")
CONFIDENCE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('confidence',0))")
ROOT_CAUSE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('rootCause',''))")
EVIDENCE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\\n'.join(d.get('evidence',[])))")
HYPOTHESES=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\\n'.join(d.get('hypothesesTested',[])))")
FIX_REC=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('fixRecommendation',''))")
TEST_CASES=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\\n'.join(d.get('testCases',[])))")
REPRO_STEPS=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\\n'.join(d.get('reproductionSteps',[])))")
FILES=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\\n'.join(d.get('affectedFiles',[])))")

# Generar DEBUG_REPORT.md
cat > "$OUTPUT_DIR/DEBUG_REPORT.md" << EOF
# Debug Report

## Status
**Status:** $STATUS
**Confidence:** $CONFIDENCE

## Root Cause
$ROOT_CAUSE

## Evidence
$EVIDENCE

## Hypotheses Tested
$HYPOTHESES

## Fix Recommendation
$FIX_REC

## Test Cases
$TEST_CASES

## Reproduction Steps
$REPRO_STEPS

## Affected Files
$FILES
EOF

# Guardar JSON
echo "$INPUT" > "$OUTPUT_DIR/debug_result.json"

echo "{\"status\":\"done\",\"reportPath\":\"$OUTPUT_DIR/DEBUG_REPORT.md\",\"jsonPath\":\"$OUTPUT_DIR/debug_result.json\"}"
