#!/bin/bash
# github-pr-risk.sh — Detect risk signals in a PR from its file paths and title.
#
# Ported from the heuristics in the `github-workflow` OpenClaw plugin (chris-openclaw),
# adapted to use the `gh` CLI + jq instead of Octokit. No new dependencies.
#
# Usage:
#   github-pr-risk.sh <owner/repo> <pr-number>
#
# Output: markdown with risk areas + review questions (or a "no risk signals" note).
#
# Exit codes: 0 on success (risk detected or not), 1 on usage/auth/API error.

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <owner/repo> <pr-number>" >&2
  exit 1
fi

REPO="$1"
PR_NUM="$2"

# ---- Fetch PR metadata + file list ----
# Capturamos el fallo de gh sin que set -e mate el script (mensaje amigable).
GH_ERR_FILE=$(mktemp)
PR_JSON=$(gh pr view "$PR_NUM" --repo "$REPO" --json title,files 2>"$GH_ERR_FILE") || {
  GH_ERR=$(cat "$GH_ERR_FILE")
  rm -f "$GH_ERR_FILE"
  echo "Error: no se pudo obtener el PR #$PR_NUM en $REPO." >&2
  if echo "$GH_ERR" | grep -qi 'not found\|GraphQL\|404'; then
    echo "El PR o repo no existe, o el token no tiene acceso." >&2
  elif [ -n "$GH_ERR" ]; then
    echo "Detalle: $GH_ERR" >&2
  fi
  exit 1
}
rm -f "$GH_ERR_FILE"

TITLE=$(echo "$PR_JSON" | jq -r '.title')
FILES=$(echo "$PR_JSON" | jq -r '.files[].path')
NFILES=$(echo "$PR_JSON" | jq '.files | length')

# ---- Risk areas from file paths (ported from inferRiskAreasFromFiles) ----
RISKS=()

if echo "$FILES" | grep -qiE '(migration|migrate|schema|\.sql$)'; then
  RISKS+=("**Schema o migraciones** - verificar plan de rollback y seguridad de escrituras concurrentes.")
fi
if echo "$FILES" | grep -qiE '(auth|login|session|jwt|token|password|oauth)'; then
  RISKS+=("**Codigo relacionado a auth** - revisar invalidacion de sesiones, cambios de scope y audit logging.")
fi
if echo "$FILES" | grep -qiE '\.(env|config|secret|credential)'; then
  RISKS+=("**Archivos de config o secrets modificados** - asegurar que no se commiteen secrets reales.")
fi
# API/rutas, excluyendo tests
if echo "$FILES" | grep -qiE '(api|route|endpoint|controller)' && ! echo "$FILES" | grep -qiE '(test|spec)'; then
  RISKS+=("**Cambios de API publica o rutas** - verificar breaking changes y compatibilidad de version.")
fi
if echo "$FILES" | grep -qiE '(package\.json|requirements\.txt|Gemfile|Cargo\.toml|go\.mod)'; then
  RISKS+=("**Dependencias actualizadas** - revisar changelogs por breaking changes en paquetes actualizados.")
fi
if [ "$NFILES" -gt 50 ]; then
  RISKS+=("**PR grande ($NFILES archivos)** - considerar pedir que se divida para review mas facil.")
fi

# --- Risk hint from title (ported from inferRiskHint) ----
LOWER_TITLE=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]')
if echo "$LOWER_TITLE" | grep -qE '\b(migration|migrate|schema)\b'; then
  RISKS+=("Titulo: toca schema/migraciones - revisar con cuidado.")
fi
if echo "$LOWER_TITLE" | grep -qE '\b(auth|login|session|token)\b'; then
  RISKS+=("Titulo: relacionado con auth - revisar implicaciones de seguridad.")
fi
if echo "$LOWER_TITLE" | grep -qE '\b(breaking|major)\b'; then
  RISKS+=("Titulo: marcado como breaking change.")
fi
if echo "$LOWER_TITLE" | grep -qE '\b(hotfix|urgent|critical)\b'; then
  RISKS+=("Titulo: urgente/hotfix - el contexto puede faltar.")
fi
if echo "$LOWER_TITLE" | grep -qE '\b(refactor|rewrite|rework)\b'; then
  RISKS+=("Titulo: refactor - verificar preservacion de comportamiento.")
fi

# --- Output: risk signals ---
echo "## Risk signals del PR #$PR_NUM en $REPO"
echo "**Titulo:** $TITLE"
echo "**Archivos:** $NFILES"
echo ""

if [ "${#RISKS[@]}" -eq 0 ]; then
  echo "_Sin senales de riesgo evidentes por paths/titulo._"
else
  for r in "${RISKS[@]}"; do
    echo "- $r"
  done
fi

# --- Suggested review questions (adaptadas de buildReviewQuestions) ---
echo ""
echo "## Preguntas sugeridas para el review"
echo ""
Q=()

# Sin tests + hay source
HAS_SRC=$(echo "$FILES" | grep -qiE '\.(ts|tsx|js|jsx|py|rb|go|rs|java|c|cpp|cs|php)$' && echo yes || echo no)
HAS_TESTS=$(echo "$FILES" | grep -qiE '(test|spec)' && echo yes || echo no)

if [ "$HAS_SRC" = "yes" ] && [ "$HAS_TESTS" = "no" ]; then
  Q+=("Hay cambios de codigo pero no tests en este PR. ¿Se cubren en otro lado o habria que agregarlos?")
fi
if [ "$HAS_TESTS" = "yes" ]; then
  Q+=("¿Cual es la estrategia de tests aca? ¿Cubren happy path o tambien edge cases?")
fi

RISK_TEXT=$(printf '%s\n' "${RISKS[@]:-}")
if echo "$RISK_TEXT" | grep -qi 'Schema'; then
  Q+=("¿Como se backfillean las filas existentes y cual es el plan de rollback si la migracion falla a mitad del deploy?")
fi
if echo "$RISK_TEXT" | grep -qi 'auth'; then
  Q+=("¿Este cambio afecta sesiones o tokens existentes? ¿Los usuarios logueados tendran que re-autenticarse?")
fi
if echo "$RISK_TEXT" | grep -qi 'API publica'; then
  Q+=("¿Es un breaking change para consumidores de la API? ¿Se bumpo la version?")
fi
if echo "$RISK_TEXT" | grep -qi 'Dependencias'; then
  Q+=("¿Que hay de nuevo en las dependencias actualizadas y como podria afectarnos?")
fi

# Catch-alls para llegar a minimo 3
if [ "${#Q[@]}" -lt 3 ]; then
  Q+=("¿Cual fue el approach alternativo que consideraste y por que fuiste con este?")
fi
if [ "${#Q[@]}" -lt 4 ]; then
  Q+=("¿Cual es la parte mas fragil de este cambio? ¿Donde es mas probable que aparezca una regresion?")
fi

for q in "${Q[@]:0:5}"; do
  echo "- $q"
done
echo ""
