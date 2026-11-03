#!/usr/bin/env bash
# session-start.sh - Initialize session context
# Usage: ./session-start.sh --project "<name>" --objective "<objective>"

set -euo pipefail

PROJECT=""
OBJECTIVE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --objective) OBJECTIVE="$2"; shift 2 ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

if [[ -z "$PROJECT" || -z "$OBJECTIVE" ]]; then
  echo "Usage: $0 --project \"<name>\" --objective \"<objective>\""
  exit 1
fi

DATE=$(date '+%Y-%m-%d %H:%M')

# --- HANDOFF del proyecto (o del workspace) ---
# El destino lo resuelve scripts/session-handoff.py, que es la unica fuente de
# verdad: recorre projects/, _workbench/, forks/, clones/ y oss/ y encuentra la
# carpeta real. Antes esta rama duplicaba el mapa en bash y solo conocia
# projects/: una sesion de `vane` leia un HANDOFF inexistente y arrancaba fria
# aunque el archivo real existiera en otra carpeta. (2026-11-03)
# La raiz del workspace se deriva con git (el script vive dentro del repo), no
# subiendo directorios a mano: el scanner de seguridad marca `../..` como
# path traversal, y ademas git es la respuesta correcta si el arbol se mueve.
WS_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel 2>/dev/null || pwd)"
HANDOFF_FILE="$(
  python3 - "$PROJECT" "$WS_ROOT" <<'PY'
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[2])
# session-handoff.py hace `from lockutil import file_lock`; lockutil vive en
# scripts/, asi que ese directorio tiene que estar en sys.path antes de cargarlo.
sys.path.insert(0, str(root / "scripts"))
spec = importlib.util.spec_from_file_location("sh", root / "scripts" / "session-handoff.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["sh"] = mod
spec.loader.exec_module(mod)
try:
    print(mod.resolve_handoff_path(sys.argv[1], None).relative_to(mod.WORKSPACE))
except Exception:
    # Un slug invalido no debe romper el arranque: se cae al path historico.
    print(f"projects/{sys.argv[1]}/.knowledge/HANDOFF.md")
PY
)" || HANDOFF_FILE="projects/$PROJECT/.knowledge/HANDOFF.md"

echo "🔧 Starting session for: $PROJECT"
echo ""

# --- Session plan: memoria de intencion (Kanam OS Etapa 2, 2026-10-06) ---
# El plan vive en .knowledge/session_plan.json y sobrevive reinicios del
# Gateway. Si hay un plan activo de una sesion anterior, se presenta para
# retomarlo en vez de re-descubrir donde quedamos. Idempotente: sin plan, no
# imprime nada.
if [[ -f "scripts/session_plan.py" ]] && command -v python3 >/dev/null 2>&1; then
  PLAN_SUMMARY=$(python3 scripts/session_plan.py summary 2>/dev/null || true)
  if [[ -n "$PLAN_SUMMARY" && "$PLAN_SUMMARY" != "No hay plan activo." ]]; then
    echo "📋 Plan de sesion activo:"
    echo "$PLAN_SUMMARY"
    echo ""
    echo "---"
    echo ""
  fi
fi

# --- Complexity score (complexity-driven-pipeline, 2026-08-30) ---
# Score the objective upfront so model/thinking/pipeline depth is decided
# together before spawning any agent.
SCORER="scripts/complexity-scorer.sh"
if [[ -f "$SCORER" ]] && command -v python3 >/dev/null 2>&1; then
  echo "📊 Scoring complexity of objective..."
  SCORE_OUT=$("$SCORER" "$OBJECTIVE" 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f\"{d.get('score','?')} ({d.get('bucket','unknown')}) - {d.get('pipeline','')}\")
except Exception:
    print('not scored')
" 2>/dev/null || echo "not scored") || true
  echo "   📈 Complexity T-score: $SCORE_OUT"
  echo ""
else
  echo "   ⚠️  Scorer not available - starting without T-score"
  echo ""
  SCORE_OUT="not scored"
fi

# Check for existing HANDOFF
if [[ -f "$HANDOFF_FILE" ]]; then
  echo "📋 Previous HANDOFF found:"
  head -10 "$HANDOFF_FILE"
  echo ""
  echo "---"
  echo ""
fi

# --- Semantic memory injection (2026-08-31) ---
# Search past sessions + learnings relevant to the objective and surface them
# as context, so the session starts with relevant memory instead of cold.
SEARCHER="scripts/memory-search.py"
if [[ -f "$SEARCHER" ]] && command -v python3 >/dev/null 2>&1; then
  echo "🧠 Searching memory for relevant context..."
  echo ""
  python3 "$SEARCHER" "$OBJECTIVE" --top 3 2>/dev/null | head -40 || echo "   (no memory results)"
  echo ""
  echo "---"
  echo ""
else
  echo "   ⚠️  memory-search.py not available - starting without semantic context"
  echo ""
fi

# Create session log
MEMORY_DIR="memory"
mkdir -p "$MEMORY_DIR"
SESSION_LOG="$MEMORY_DIR/$(date +%Y-%m-%d).md"

if [[ ! -f "$SESSION_LOG" ]]; then
  cat > "$SESSION_LOG" << LOG
# Session Log - $(date '+%Y-%m-%d')

## $PROJECT
**Objective:** $OBJECTIVE
**Complexity T-score:** $SCORE_OUT
**Start:** $DATE

LOG
fi

echo "✅ Session started"
echo "   Project: $PROJECT"
echo "   Objective: $OBJECTIVE"
echo "   Log: $SESSION_LOG"
