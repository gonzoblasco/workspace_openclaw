#!/usr/bin/env bash
# ============================================================
# project-closure.sh - Immortalize a finished project
# Captures the decision (ADR), the state (memory.db), and makes
# the closure reproducible. See skills/project-closure/SKILL.md.
#
# Usage:
#   ./scripts/project-closure.sh \
#     --name "<slug>" \
#     --title "<titulo ADR>" \
#     --summary "<resumen para DB y daily>" \
#     --complexity <T-score, opcional> \
#     --model "<modelo, opcional>" \
#     --tag "pipeline,cierre" \
#     [--create-adr]
#
# Exit: 0 ok, 1 missing args, 2 db error.
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DB="$WORKSPACE_DIR/memory/memory.db"
ADR_DIR="$WORKSPACE_DIR/docs/adr"

NAME=""
TITLE=""
SUMMARY=""
COMPLEXITY=""
MODEL=""
TAGS=""
CREATE_ADR=0

usage() {
  echo "Usage: $0 --name <slug> --title <titulo> --summary <resumen> [--complexity T] [--model m] [--tag t] [--create-adr]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) NAME="$2"; shift 2 ;;
    --title) TITLE="$2"; shift 2 ;;
    --summary) SUMMARY="$2"; shift 2 ;;
    --complexity) COMPLEXITY="$2"; shift 2 ;;
    --model) MODEL="$2"; shift 2 ;;
    --tag) TAGS="$2"; shift 2 ;;
    --create-adr) CREATE_ADR=1; shift ;;
    *) echo "Unknown: $1"; usage ;;
  esac
done

if [[ -z "$NAME" || -z "$TITLE" || -z "$SUMMARY" ]]; then
  echo "ERROR: --name, --title, --summary son obligatorios." >&2
  usage
fi

TODAY="$(date +%Y-%m-%d)"
NOW="$(date +%Y-%m-%dT%H:%M:%S)"
SAFE_NAME="$(echo "$NAME" | sed 's/[^a-z0-9-]/-/g')"

echo "🌿 Project closure: $NAME"
echo ""

# --- 1. ADR (optional) ---
if [[ "$CREATE_ADR" -eq 1 ]]; then
  NEXT=$(ls "$ADR_DIR"/ADR-*.md 2>/dev/null | sed -E 's|.*/ADR-([0-9]+).*|\1|' | sort -n | tail -1)
  NEXT_NUM=$(( ${NEXT:-42} + 1 ))
  ADR_FILE="$ADR_DIR/ADR-$(printf '%03d' "$NEXT_NUM")-$SAFE_NAME.md"
  cat > "$ADR_FILE" << ADREOF
# ADR-$(printf '%03d' "$NEXT_NUM"): $TITLE

**Status:** Accepted ($(date +%Y-%m-%d))
**Deciders:** Gonzo / Kanam
**Fecha:** $(date +%Y-%m-%d)
**Origen:** workspace (cierre de proyecto $NAME)

## Contexto

[Completar: problema que motiva la decision]

## Decision

[Completar: que se decidio, conciso y accionable]

## Implementacion

[Completar: archivos y componentes]

## Consecuencias

- **Positivas:** [..]
- **Limitaciones asumidas:** [..]

## Alternativas

[Completar: que se descarto y por que]

## Validacion

[Completar: evidencia empirica]

---

*Cierre de proyecto $NAME. Registrado $(date +%Y-%m-%d) en daily + DB.*
ADREOF
  echo "   ✅ ADR creado: $ADR_FILE"
fi

# --- 2. Registrar en DB ---
if [[ -f "$DB" ]] && command -v python3 >/dev/null 2>&1; then
  python3 - "$DB" "$TODAY" "$TITLE" "$TAGS" "$COMPLEXITY" "$MODEL" "$SUMMARY" "$SAFE_NAME" << PYEOF
import sys, sqlite3
from datetime import datetime
db, today, title, tags = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
complexity = sys.argv[5] if sys.argv[5] else None
model = sys.argv[6] if sys.argv[6] else "unknown"
summary = sys.argv[7]
name = sys.argv[8]
now = datetime.now().isoformat()

c = sqlite3.connect(db)
# daily_notes
c.execute("INSERT INTO daily_notes (date, type, content, source_file, created_at) VALUES (?, 'daily', ?, ?, ?)",
          (today, summary, "memory/" + today + ".md", now))
# sessions_relacional
c.execute("""INSERT INTO sessions_relacional
             (date, title, tags, complexity_score, model_used, thinking_level, summary, content_bare, created_at)
             VALUES (?, ?, ?, ?, ?, 'max', ?, ?, ?)""",
          (today, title, tags, complexity, model, summary, "# Cierre de proyecto: " + name + "\n\n" + summary + "\n", now))
c.commit()
print("   ✅ DB: daily_notes + sessions_relacional registrados")
PYEOF
else
  echo "   ⚠️  DB o python3 no disponibles - registro en DB omitido" >&2
fi

echo ""
echo "✅ Closure registrada para: $NAME"
echo "   Titulo: $TITLE"
echo "   TAGS: ${TAGS:-n/a}"
echo "   Complejidad: ${COMPLEXITY:-n/a}"
echo ""
echo "   Siguiente: commit del workspace + mirror de skills + push."
