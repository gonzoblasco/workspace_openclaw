#!/bin/bash
# ============================================================
# complexity-scorer.sh
# Evaluates a task objective and returns a T-score (1-20)
# with recommended model, thinking level, and pipeline config.
#
# Usage:
#    ./complexity-scorer.sh "<objective>"
#    echo '<objective>' | ./complexity-scorer.sh --stdin
#    ./complexity-scorer.sh --interactive
#    ./complexity-scorer.sh --score <T> "<objective>"  # force score without LLM
# ============================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# --- Config ---
DEFAULT_MODEL="ollama/deepseek-v4.1-flash:cloud"
OLLAMA_BASE="${OLLAMA_BASE:-http://127.0.0.1:11434}"

# --- Helpers ---
usage() {
  echo "Usage: $0 <objective>"
  echo "       echo '<objective>' | $0 --stdin"
  echo "      $0 --interactive"
  echo "      $0 --score <T> '<objective>'  # force score without LLM"
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
   # Use remaining args as the actual objective when --score is provided
  shift 2 || true
  if [[ $# -gt 0 ]]; then
    OBJECTIVE="$*"
  else
    OBJECTIVE="forced-t$FORCE_T-for-validation"
  fi
else
  OBJECTIVE="$*"
fi

if [[ -z "${OBJECTIVE:-}" ]]; then
  log_warn "Objective is empty."
  usage
fi

OBJECTIVE=$(echo "$OBJECTIVE" | sed 's/"/\\"/g' | tr -d '\n')

log_info "Scoring objective: ${OBJECTIVE:0:80}..."

# --- Prompt for scoring ---
# Meta-prompt is the single source of truth (prompts/complexity-scorer.md).
# Build the LLM system prompt from that file's scoring rules.
SYSTEM_PROMPT="You are the task complexity evaluator. Score the objective on 4 dimensions (1-5 each):\n"
META="prompts/complexity-scorer.md"
if [[ -f "$META" ]]; then
  # Extract the 4 dimension descriptions from the meta-prompt
  DIMS=$(grep -A1 -E '^   \* \*\*(Alcance|Abstracción|Riesgo|Ambigüedad)\*\*' "$META" | grep -oE '\(1=.*\)' | tr '\n' '; ')
  SYSTEM_PROMPT="You are the task complexity evaluator. Score the objective on 4 dimensions A/B/C/D (each 1-5):\n"
  SYSTEM_PROMPT+="A (Scope): 1=one file, 5=multi-repo. B (Abstraction): 1=trivial fix, 5=system arch. C (Risk): 1=cosmetic, 5=critical/data loss. D (Ambiguity): 1=crystal clear, 5=vague.\n"
  SYSTEM_PROMPT+="Return ONLY valid JSON: { \"A\":<1-5>,\"B\":<1-5>,\"C\":<1-5>,\"D\":<1-5>,\"justification\":\"<one line>\" }. No prose, no markdown fences."
else
  SYSTEM_PROMPT="You are a task complexity evaluator. Analyze the objective and score it. Return ONLY valid JSON, no markdown fences or extra text:\n\n{\n   \"A\": <1-5 integer, scope: 1=one file, 2=2-3 files, 3=multi-file same module, 4=multi-module, 5=multi-repo>,\n   \"B\": <1-5 integer, abstraction: 1=trivial fix, 2=feature, 3=refactor, 4=design, 5=system architecture>,\n   \"C\": <1-5 integer, risk: 1=cosmetic, 2=minor breakage, 3=feature broken, 4=significant, 5=critical/data loss>,\n   \"D\": <1-5 integer, ambiguity: 1=crystal clear, 2=mostly clear, 3=some interpretation, 4=needs research, 5=vague>,\n   \"justification\": \"<one line explaining each dimension value>\"\n}\n\nDimensions:\n- A (Scope): 1=single file, 2=2-3 files/same system, 3=multi-file module, 4=multi-module, 5=multi-repo\n- B (Abstraction): 1=trivial fix, 2=feature, 3=refactor, 4=design, 5=system architecture\n- C (Risk): 1=cosmetic, 2=minor breakage, 3=feature broken, 4=significant, 5=critical/data loss\n- D (Ambiguity): 1=crystal clear, 2=mostly clear, 3=some interpretation, 4=needs research, 5=vague\n\nReturn ONLY the JSON object with A, B, C, D as integers and justification. No markdown fences."
fi

USER_PROMPT="Objective: $OBJECTIVE"

# --- Call Ollama (with fallback chain) ---
T=""
SCORED_MODEL=""

if [[ -n "${FORCE_T:-}" ]]; then
  T="$FORCE_T"
  SCORED_MODEL="manual"
  log_info "Forced score: T=$T"
else
   # Try models in order: local first, then cloud fallbacks
  # Order: gemma4:e4b-mlx (local, 6.7x faster than qwen3.5) first, then cloud fallbacks.
  # qwen3.5:9b-mlx kept as last local fallback (slow, 154s vs 23s on benchmark 2026-08-30).
  for SCORER_MODEL in "gemma4:e4b-mlx" "deepseek-v4.1-flash:cloud" "gemma4:cloud" "qwen3.5:9b-mlx"; do
    log_info "Trying model: $SCORER_MODEL"
    
    # Compact JSON payload (avoids "Thinking Style" eating the response on local models)
    PAYLOAD=$(python3 -c "
import json,sys
sys.stdout.write(json.dumps({
  'model': '$SCORER_MODEL',
  'system': 'Return ONLY a JSON object: {\"A\":<1-5>,\"B\":<1-5>,\"C\":<1-5>,\"D\":<1-5>,\"justification\":\"<text>\"}. No prose.',
  'prompt': 'Score this objective. A=scope 1-5 (1=1file,5=multirepo). B=abstraction 1-5 (1=fix,5=arch). C=risk 1-5 (1=cosmetic,5=critical). D=ambiguity 1-5 (1=clear,5=vague). Return ONLY JSON.\n\nObjective: $OBJECTIVE',
  'stream': False,
  # ADR-109: sin 'think' el default de deepseek es pensar. Medido 2026-11-05:
  # 626 tokens y 3,4s con thinking, 18 tokens y 0,4s con think=false, misma respuesta.
  'think': False,
  'options': {'temperature': 0.1, 'num_predict': 800, 'num_ctx': 4096}
}))
")
    
    RESPONSE=$(curl -s --max-time 60 "$OLLAMA_BASE/api/generate" -H "Content-Type: application/json" -d "$PAYLOAD" 2>&1) || {
      log_warn "$SCORER_MODEL: curl failed (network/auth)"
      continue
    }
    
    # Check for quota/auth error in response
    if echo "$RESPONSE" | grep -qi "usage limit\|upgrade\|error.*:.*you.*have\|refused"; then
      ERR_MSG=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error','')[:200])" 2>/dev/null || echo "$RESPONSE" | head -c 200)
      log_warn "$SCORER_MODEL rejected (quota/auth): $ERR_MSG"
      continue
    fi
    
    # Extract response + thinking (local models put content in 'thinking' field)
    RAW_JSON=$(echo "$RESPONSE" | python3 -c "
import sys,json
try:
  d = json.load(sys.stdin)
  r = d.get('response','')
  t = d.get('thinking','')
  # Prefer 'response', fall back to 'thinking' if response is empty
  if r.strip():
    print(r)
  elif t.strip():
    print(t)
  else:
    print('')
except Exception:
  print('')
" 2>/dev/null)
    
    if [[ -z "$RAW_JSON" ]]; then
      log_warn "$SCORER_MODEL: empty response (no response, no thinking)"
      continue
    fi
    
    # Parse dimensions using external parser (handles JSON or prose/thinking text)
    DIM_JSON=$(echo "$RAW_JSON" | python3 "$SCRIPT_DIR/complexity-parse.py" 2>/dev/null) || {
      log_warn "$SCORER_MODEL: python3 parse failed"
      continue
    }
  
    if [[ -n "$DIM_JSON" ]] && [[ "$DIM_JSON" != ERROR* ]]; then
      A=$(echo "$DIM_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('A',2))" 2>/dev/null || echo 2)
      B=$(echo "$DIM_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('B',2))" 2>/dev/null || echo 2)
      C=$(echo "$DIM_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('C',2))" 2>/dev/null || echo 2)
      D=$(echo "$DIM_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('D',2))" 2>/dev/null || echo 2)
      
      SCORED_MODEL="$SCORER_MODEL"
      log_info "$SCORER_MODEL: parsed A=$A B=$B C=$C D=$D (T=$((A+B+C+D)))"
      break
    fi
  done
  
  if [[ -z "${SCORED_MODEL:-}" ]]; then
    log_warn "All scorer models failed. Use --score T to force a value."
    echo "{\"error\": \"No scorer model available or reachable. Use --score T to force.\"}"
    exit 2
  fi
  
  T=$((A + B + C + D))
fi

# --- Risk escalation rule (calibration 2026-08-31) ---
# A high-risk task (C>=4) that is moderately complex (T>=14) must be treated
# as HIGH, even if low ambiguity drops the linear total below 17.
# Rationale: ambiguity (D) can be clarified, but production data-loss risk (C)
# cannot. This protects dangerous-yet-clear tasks from being under-pipelined.
ESCALATED=0
if [[ -n "${A:-}" && -n "${C:-}" ]] && [[ "${C}" -ge 4 ]] && [[ "$T" -ge 14 ]]; then
  ESCALATED=1
  log_info "Risk escalation: C=$C >= 4 and T=$T >= 14 -> forcing HIGH bucket"
fi

# --- Map to config ---
if [[ "$ESCALATED" -eq 1 ]] \
   || [[ "$T" -ge 17 ]]; then
  BUCKET="high"
  MODEL="$DEFAULT_MODEL"
  THINKING="max"
  AGENTS="A+B+Kanam"
  PIPELINE="Kanam diseña(max) -> A escribe(high) -> B revisa(high) -> verification"
elif [[ $T -le 6 ]]; then
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
   "escalated": $ESCALATED,
   "model": "$MODEL",
   "thinking": "$THINKING",
   "agents": "$AGENTS",
   "pipeline": "$PIPELINE",
   "objective": "${OBJECTIVE:0:120}",
   "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
   "scorer_model": "$SCORED_MODEL"
}
EOF

log_info "T=$T [$BUCKET] | thinking=$THINKING | pipeline=$PIPELINE | scorer=$SCORED_MODEL"

# Confirmation gate for T >= 17 (Gonzo must confirm)
if [[ $T -ge 17 ]]; then
  echo "" >&2
  log_warn "T=$T is HIGH-CRITICAL. Requires Gonzo confirmation before proceeding."
fi
