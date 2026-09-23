#!/bin/bash
# oss-sync.sh - Sincroniza el estado real de las contribuciones OSS contra GitHub.
# Fuente de verdad de estados: memory/memory.db (tabla contributions).
# GitHub es la fuente para PR states: open/merged/closed + mergeability + actividad.
#
# Uso:
#   ./scripts/oss-sync.sh            - sync completo de PRs con numero (consulta GitHub)
#   ./scripts/oss-sync.sh --dry-run  - solo reporta diferencias, no escribe en la DB
#   ./scripts/oss-sync.sh --quiet    - solo imprime los cambios aplicados
#
# Reglas de escritura:
#   - SOLO actualiza status cuando GitHub lo confirma: merged (state=closed + merged_at)
#     o closed (state=closed sin merged). Los estados propios (waiting_review, active,
#     comment, verified, collab) se preservan si GitHub no dictamina merged/closed.
#   - Guarda metadata de cada consulta en la tabla oss_sync (historial por PR).
#   - El detalle NO se pisa: si el script detecta actividad nueva lo anota en context,
#     no reemplaza el detail que documenta nuestro rol en el ticket.

DB="memory/memory.db"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_PATH="$SCRIPT_DIR/../$DB"
DRY_RUN=0
QUIET=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --quiet) QUIET=1 ;;
  esac
done

command -v gh >/dev/null 2>&1 || { echo "Error: gh CLI requerido (brew install gh)." >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Error: gh sin autenticar." >&2; exit 1; }

sql_escape() { printf '%s' "$1" | sed "s/'/''/g"; }

# Crea la tabla de metadata de sync si no existe.
sqlite3 -cmd "PRAGMA foreign_keys=ON" "$DB_PATH" "CREATE TABLE IF NOT EXISTS oss_sync (
  repo TEXT NOT NULL,
  pr TEXT NOT NULL,
  last_checked TEXT,
  state TEXT,
  merged TEXT,
  mergeable_state TEXT,
  comments INTEGER,
  updated_at TEXT,
  PRIMARY KEY (repo, pr)
);"

changed=0
checked=0

# Itera las contribuciones tipo pr con numero de PR real (ignora collab y '-').
# Process substitution: la iteracion corre en el shell padre para que los contadores sobrevivan.
while IFS='|' read -r id repo pr; do
  # Solo PRs con numero real (acepta '#123' o '123'), nunca ids tipo 'comment-126876'.
  case "$pr" in
    ''|'-'|*[!0-9#]*) continue ;;
  esac
  num=$(printf '%s' "$pr" | tr -d '#')
  checked=$((checked + 1))

  raw=$(gh api "repos/$repo/pulls/$num" --jq '{state, merged, mergeable_state, comments, updated_at}' 2>/dev/null) || {
    # PR puede haber sido borrado o repo renombrado - lo reportamos sin romper el ciclo.
    echo "SKIP|$repo|$pr|no-pull-or-api-error"
    continue
  }

  state=$(printf '%s' "$raw" | jq -r '.state // "unknown"')
  merged=$(printf '%s' "$raw" | jq -r '.merged // "false"')
  mergeable_state=$(printf '%s' "$raw" | jq -r '.mergeable_state // "unknown"')
  comments=$(printf '%s' "$raw" | jq -r '.comments // 0')
  updated_at=$(printf '%s' "$raw" | jq -r '.updated_at // ""')
  now=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  # Dictamen de GitHub -> status propio de la DB.
  new_status=""
  if [ "$state" = "closed" ] && [ "$merged" = "true" ]; then
    new_status="merged"
  elif [ "$state" = "closed" ]; then
    new_status="closed"
  fi

  # Consulta el estado actual en la DB.
  current=$(sqlite3 -cmd "PRAGMA foreign_keys=ON" "$DB_PATH" "SELECT status FROM contributions WHERE id='$id';")
  action=""

  if [ -n "$new_status" ] && [ "$current" != "$new_status" ]; then
    if [ "$DRY_RUN" = "1" ]; then
      action="DRY|$repo|$pr|$current->$new_status"
    else
      sqlite3 -cmd "PRAGMA foreign_keys=ON" "$DB_PATH" "UPDATE contributions SET status='$new_status' WHERE id='$id';"
      action="UPD|$repo|$pr|$current->$new_status"
    fi
  elif [ "$current" = "open" ] && [ "$mergeable_state" = "dirty" ] || [ "$current" = "open" ] && [ "$mergeable_state" = "failing" ]; then
    # PR abierto pero con problemas de merge - anotarlo, no cambiar el estado.
    if [ "$DRY_RUN" = "1" ]; then
      action="DRY|$repo|$pr|needs-rebase($mergeable_state)"
    else
      sqlite3 -cmd "PRAGMA foreign_keys=ON" "$DB_PATH" "INSERT OR REPLACE INTO oss_sync (repo, pr, last_checked, state, merged, mergeable_state, comments, updated_at) VALUES ('$(sql_escape "$repo")', '$(sql_escape "$pr")', '$now', '$state', '$merged', '$mergeable_state', $comments, '$updated_at');"
      action="NOTE|$repo|$pr|needs-rebase($mergeable_state)"
    fi
  fi

  # Guarda metadata de la consulta (si no es dry-run y no se guardo arriba).
  if [ "$DRY_RUN" != "1" ] && [ -z "$action" ] || [ "$DRY_RUN" != "1" ] && [ "${action#NOTE}" = "$action" ]; then
    sqlite3 -cmd "PRAGMA foreign_keys=ON" "$DB_PATH" "INSERT OR REPLACE INTO oss_sync (repo, pr, last_checked, state, merged, mergeable_state, comments, updated_at) VALUES ('$(sql_escape "$repo")', '$(sql_escape "$pr")', '$now', '$state', '$merged', '$mergeable_state', $comments, '$updated_at');"
  fi

  if [ -n "$action" ]; then
    echo "$action"
  fi
done < <(sqlite3 -cmd "PRAGMA foreign_keys=ON" "$DB_PATH" "SELECT id, repo, pr FROM contributions WHERE tipo='pr'
  AND pr <> '-' AND pr <> '' AND pr GLOB '*[0-9]*';")

if [ "$QUIET" != "1" ]; then
  echo "---"
  echo "Sync completo: $checked PRs consultados."
fi