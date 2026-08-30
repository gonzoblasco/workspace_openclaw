#!/bin/bash
# ============================================================
# complexity-scorer.sh
# Evaluates a task objective and returns a T-score (1-20)
# with recommended model, thinking level, and pipeline config.
#
# Usage:
#   ./complexity-scorer.sh "<objective>"
#   ./complexity-scorer.sh --interactive
#   cat task.txt | ./complexity-scorer.sh --stdin
#
# Output: JSON to stdout (parseable, machine-readable)
#   { score, bucket, model, thinking, ticket, justification }
#
# Buckets:
#   trivial  (T 1-6)  : Kanam solo, no pipeline
#   low      (T 7-12)  : A/B pipeline, model high, thinking high
#   medium   (T 13-16) : A/B pipeline, cross-review by B, thinking high
#   high     (T 17-20) : Kanam designs in max, A/B execute in high, verification
#
# Exit codes:
#   0 = scored successfully
#   1 = missing input
#   2 = model error
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# --- Config ---
DEFAULT_MODEL="ollama/deepseek-v4-flash:cloud"
OLLAMA_BASE="${OLLAMA_BASE:-http://127.0.0.1:11434}"

# --- Helpers ---
usage() {
  echo "Usage: $0 <objective>"
  echo "       echo '<objective>' | $0 --stdin"
  echo "       $0 --interactive"
  echo "       $0 --score <T>   # force score without LLM"
  exit 1
}

log_info() { echo "[INFO] $*" >&2; }
log_warn() { echo "[WARN] $*" >&2; }

# --- Input ---
OBJECTIVE=""

if [[ $# -eq 0 ]]; then
  usage
elif [[ "$1" == "--interactive" ]]; then
  echo -n "Describe la tarea: " >&2
  read -r OBJECTIVE
elif [[ "$1" == "--stdin" ]]; then
  OBJECTIVE=$(cat)
elif [[ "$1" == "--score" ]]; then
  FORCE_T="$2"
else
  OBJECTIVE="$*"
fi

if [[ -z "${OBJECTIVE}" ]]; then
  log_warn "Objective is empty."
  usage
fi

OBJECTIVE=$(echo "$OBJECTIVE" | sed 's/"/\\"/g' | tr -d '\n')

log_info "Scoring: ${OBJECTIVE:0:80}..."

# --- Prompt for scoring ---
SYSTEM_PROMPT="You are a task complexity evaluator. Analyze the objective and score it.
Return ONLY valid JSON with no markdown fences or extra text:

{
  \"A\": <1-5, scope: files/systems touched>,
  \"B\": <1-5, abstraction: trivial=1, full-arch-design=5>,
  \"C\": <1-5, risk: cosmetic=1, data-loss/breakage=5>,
  \"D\": <1-5, ambiguity: crystal-clear=1, abstract=5>,
  \"justification\": \"<one line explaining each dimension value>\"
}

Dimensions:
- A (Scope): 1=single file, 2=2-3 files/same system, 3=multi-file/same module, 4=multi-module, 5=multi-repo
- B (Abstraction): 1=trivial fix, 2=feature, 3=refactor, 4=design, 5=system architecture
- C (Risk): 1=cosmetic, 2=minor breakage, 3=feature broken, 4=significant breakage, 5=data loss/critical
- D (Ambiguity): 1=crystal clear, 2=mostly clear, 3=needs some interpretation, 4=needs significant interpretation, 5=vague

Return ONLY the JSON. No markdown, no explanation."

USER_PROMPT="Objective: $OBJECTIVE"

# --- Call Ollama ---
if [[ -n "${FORCE_T:-}" ]]; then
  T="$FORCE_T"
  log_info "Forced score: T=$T"
else
  # Try primary model first, then fallback if quota/auth error
  for SCORER_MODEL in "glm-5.3-flash:cloud" "deepseek-v4-flash:cloud" "gemma4:cloud"; do
    log_info "Trying model: $SCORER_MODEL"
    RESPONSE=$(curl -s --max-time 30 "$OLLAMA_BASE/api/generate" \
      -H "Content-Type: application/json" \
      -d "{
        \"model\": \"$SCORER_MODEL\",
        \"system\": \"$SYSTEM_PROMPT\",
        \"prompt\": \"$USER_PROMPT\",
        \"stream\": false,
        \"options\": { \"temperature\": 0.1, \"num_predict\": 300 }
      }" 2>&1) || {
        log_warn "$SCORER_MODEL: curl failed"
        continue
      }

    # Check for quota/auth error in response
    if echo "$RESPONSE" | grep -qi "usage limit\|upgrade\|error.*:.*you\|refused"; then
      ERR_MSG=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error','')[:200])" 2>/dev/null || echo "$RESPONSE" | head -c 200)
      log_warn "$SCORER_MODEL rejected: $ERR_MSG"
      continue
    fi

    # Extract JSON response
    RAW=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response',''))" 2>/dev/null) || continue

    if [[ -z "$RAW" ]]; then
      log_warn "$SCORER_MODEL: empty response"
      continue
    fi

    # Parse dimensions using Python (more robust than regex)
    DIM_JSON=$(echo "$RAW" | python3 -c "
import sys, re
text = sys.stdin.read()
# Try to find JSON block
m = re.search(r'\{[^{}]*\"A\"[^{}]*\}', text)
if m:
    print(m.group(0))
else:
    # Try to extract individual values
    a = re.search(r'\"A\"\\s*:\\s*(\\d)', text)
    b = re.search(r'\"B\"\\s*:\\s*(\\d)', text)
    c = re.search(r'\"C\"\\s*:\\s*(\\d)', text)
    d = re.search(r'\"D\"\\s*:\\s*(\\d)', text)
    if all([a,b,c,d]):
        print('{\"A\":'+a.group(1)+',\"B\":'+b.group(1)+',\"C\":'+c.group(1)+',\"D\":'+d.group(1)+'}')
")
    if [[ -n "$DIM_JSON" ]]; then
      A=$(echo "$DIM_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('A',2))" 2>/dev/null || echo 2)
      B=$(echo "$DIM_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('B',2))" 2>/dev/null || echo 2)
      C=$(echo "$DIM_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('C',2))" 2>/dev/null || echo 2)
      D=$(echo "$DIM_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('D',2))" 2>/dev/null || echo 2)
      SCORED_MODEL="$SCORER_MODEL"
      break
    fi
  done

  if [[ -z "${SCORED_MODEL:-}" ]]; then
    log_warn "All scorer models failed. Use --score T to force a value."
    echo "{\"error\": \"No scorer model available. Use --score T to force.\"}"
    exit 2
  fi

  T=$((A + B + C + D))
  log_info "Scored by $SCORER_MODEL: T=$T (A=$A B=$B C=$C D=$D)"
fi

# --- Map to config ---
if   [[ $T -le 6 ]];  then
  BUCKET="trivial"
  MODEL="$DEFAULT_MODEL"
  THINKING="off"
  AGENTS="none"
  PIPELINE="Kanam solo"
elif [[ $T -le 12 ]]; then
  BUCKET="low"
  MODEL="$DEFAULT_MODEL"
  THINKING="high"
  AGENTS="A"
  PIPELINE="A escribe -> Kanam revisa"
elif [[ $T -le 16 ]]; then
  BUCKET="medium"
  MODEL="$DEFAULT_MODEL"
  THINKING="high"
  AGENTS="A+B"
  PIPELINE="A escribe -> B cross-review -> Kanam aprueba"
else
  BUCKET="high"
  MODEL="$DEFAULT_MODEL"
  THINKING="max"
  AGENTS="A+B+Kanam"
  PIPELINE="Kanam diseña(max) -> A escribe(high) -> B revisa(high) -> verification"
fi

# --- Ticket ID ---
TICKET="T-${T}-$(date +%H%M%S)"

# --- Output JSON ---
cat <<EOF
{
  "ticket": "$TICKET",
  "score": $T,
  "bucket": "$BUCKET",
  "model": "$MODEL",
  "thinking": "$THINKING",
  "agents": "$AGENTS",
  "pipeline": "$PIPELINE",
  "objective": "${OBJECTIVE:0:120}",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

log_info "T=$T [$BUCKET] | thinking=$THINKING | pipeline=$PIPELINE"

# Confirmation gate for T >= 17
if [[ $T -ge 17 ]]; then
  echo "" >&2
  log_warn "T=$T is HIGH-CRITICAL. Requires Gonzo confirmation before proceeding."
fi
