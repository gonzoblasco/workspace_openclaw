#!/usr/bin/env bash
# session-end.sh - Cierra una sesion: informe en memory/ (DB-first) + HANDOFF del proyecto.
# Usage: ./session-end.sh --project "<name>" --summary "<summary>" \
#          [--status "<estado actual>"] [--next-steps "<pasos>"] [--decisions "<contexto>"]

set -euo pipefail

PROJECT=""
SUMMARY=""
STATUS=""
NEXT_STEPS=""
DECISIONS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --summary) SUMMARY="$2"; shift 2 ;;
    --status) STATUS="$2"; shift 2 ;;
    --next-steps) NEXT_STEPS="$2"; shift 2 ;;
    --decisions) DECISIONS="$2"; shift 2 ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

if [[ -z "$PROJECT" || -z "$SUMMARY" ]]; then
  echo "Usage: $0 --project \"<name>\" --summary \"<summary>\" [--status ..] [--next-steps ..] [--decisions ..]"
  exit 1
fi

DATE=$(date '+%Y-%m-%d %H:%M')
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

# --- CHANGELOG en ventana (2026-10-06, ADR-092) -------------------------------
# El CHANGELOG activo muestra solo los ultimos ~30 dias; lo viejo se archiva.
# Se corre en cada cierre para que nunca quede desfasado. El pre-commit lo
# verifica cuando el archivo esta staged; aca se rota solo.
if [ -f "scripts/changelog-rotate.py" ]; then
  python3 scripts/changelog-rotate.py >/dev/null 2>&1 \
    && echo "   📅 CHANGELOG en ventana (30 dias)" \
    || echo "   ⚠️  changelog-rotate.py fallo"
fi

# --- HANDOFF del proyecto (o del workspace) -------------------------------------
# El destino lo resuelve scripts/session-handoff.py:
#   workspace/sistema -> <workspace>/.knowledge/HANDOFF.md
#   proyecto          -> ~/projects/<slug>/.knowledge/HANDOFF.md  (ADR-075)
HANDOFF_MSG=""
if [[ -f "scripts/session-handoff.py" ]]; then
  HANDOFF_ARGS=(--project "$PROJECT" --summary "$SUMMARY" --branch "$BRANCH")
  [[ -n "$STATUS" ]] && HANDOFF_ARGS+=(--status "$STATUS")
  [[ -n "$NEXT_STEPS" ]] && HANDOFF_ARGS+=(--next-steps "$NEXT_STEPS")
  [[ -n "$DECISIONS" ]] && HANDOFF_ARGS+=(--decisions "$DECISIONS")
  HANDOFF_MSG=$(python3 scripts/session-handoff.py "${HANDOFF_ARGS[@]}") || HANDOFF_MSG="   ⚠️  HANDOFF no generado"
else
  HANDOFF_MSG="   ⚠️  scripts/session-handoff.py no encontrado - HANDOFF omitido"
fi

# Update daily log - DB-first (2026-08-31)
# The DB (memory.db) is the source of truth; the .md is a regenerable view.
MEMORY_DIR="memory"
mkdir -p "$MEMORY_DIR"
SESSION_LOG="$MEMORY_DIR/$(date +%Y-%m-%d).md"

# Recover the complexity T-score recorded at session start for a clean record
TSCORE_LINE=""
if grep -q "^## $PROJECT$" "$SESSION_LOG" 2>/dev/null; then
  TSCORE_LINE=$(grep -A3 "^## $PROJECT$" "$SESSION_LOG" 2>/dev/null | grep -oE "\*\*Complexity T-score:\*\* .*" | head -1)
fi

# Write to DB as source of truth, then regenerate the .md view
if command -v python3 >/dev/null 2>&1 && [ -f "scripts/memory-end-session.py" ]; then
  python3 scripts/memory-end-session.py \
    --project "$PROJECT" \
    --summary "$SUMMARY" \
    --branch "$BRANCH" \
    --tscore "$TSCORE_LINE" \
    --skip-catalog || echo "   ⚠️  Fallback: session-end DB write failed"
else
  # Fallback to the old direct .md append if the DB-first script is unavailable
  cat >> "$SESSION_LOG" << LOG

## Session End - $PROJECT
**End:** ${DATE}
**Summary:** $SUMMARY
**Branch:** $BRANCH
LOG
fi

echo "✅ Session closed"
echo "$HANDOFF_MSG"
echo "   Log: $SESSION_LOG"
echo ""

# Limpieza de snapshots temporales del heartbeat (2026-09-30)
# El cierre manual de sesion tambien purga los documentos temporales:
# mantiene la misma politica de retencion (7 dias) que el job heartbeat-global-snapshot.
if command -v find >/dev/null 2>&1; then
  find "$HOME/.openclaw/backups" -maxdepth 1 -type d -name 'heartbeat-*' -mtime +7 -exec rm -rf {} + 2>/dev/null || true
  echo "🧹 Snapshots temporales >7 dias purgados"
  echo ""
fi

# Auto-catalog memory into relational DB + embeddings (2026-08-30)
# Keeps memory.db always in sync with the daily notes without manual runs.
if command -v python3 >/dev/null 2>&1 && [ -f "scripts/memory-catalog-v2.py" ]; then
  echo "🗂️  Cataloging memory into DB..."
  python3 "scripts/memory-catalog-v2.py" >/dev/null 2>&1 && echo "   ✅ Memory cataloged" || echo "   ⚠️  Catalog skipped (see error above)"
else
  echo "   ⚠️  memory-catalog-v2.py not found - skip cataloging"
fi
echo ""

# Reflection prompt
# Post-task reflection (2026-09-03): automatic post-task reflection stage.
# Complements the closing self-reflection: this one runs per task, not per session.
# Usage: ./scripts/post-task-reflection.sh --type <type> --summary "..." [--check-dups --propose-skill --save]
if [[ -x "scripts/post-task-reflection.sh" ]]; then
  echo "🤔 Post-task reflection available:"
  echo "   ./scripts/post-task-reflection.sh --type <debug|feature|review|config|research|oss|docs|other> \\"
  echo "       --summary \"<what happened>\" --lesson \"<lesson>\" --check-dups --propose-skill --save"
  echo "   (run it per complex task, not only when closing a session)"
  echo ""
fi
# Closing self-reflection (global learnings)
echo "🤔 Quick reflection:"
echo "   What did we learn? Any new pattern?"
echo "   Is it global (🌍) or project-specific (🏗️)?"
echo "   If there is something, record it in docs/LEARNINGS.md"
echo ""
# PRs (2026-08-25): Gonzo reviews them manually on GitHub and passes the URLs to review.
# PRs are not checked automatically when closing a session.
echo "📋 Don't forget to:"
echo "   1. Review HANDOFF.md"
echo "   2. Commit workspace changes"
echo "   3. Push to remote"
