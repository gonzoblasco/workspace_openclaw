#!/usr/bin/env bash
# pr-thread-brief.sh - Brief de un hilo de PR: quien hizo que, y quien tiene la pelota.
#
# Uso:
#   pr-thread-brief.sh <owner/repo> <numero> [login]
#
# Clasifica cada evento del hilo (comentarios, reviews, comentarios inline) en:
#   OURS  = nuestro login (default: gonzoblasco)
#   BOT   = autor de bot o cuenta automatica
#   THIRD = cualquier otra cuenta (INCLUIDOS maintainers que revisan nuestro trabajo)
#
# Por que existe (docs/AGENTS-DETALLE.md, regla del 2026-09-22):
#   La autoria se verifica por el user.login de la API, NUNCA por proximidad de
#   contexto. En astryx #4690 el CHANGES_REQUESTED de un maintainer se reporto
#   como nuestro por estar cerca en el tiempo de otro hilo nuestro. Este script
#   hace ese chequeo mecanico en vez de a ojo.
#
# Solo lectura: usa `gh api` (GET), nunca escribe ni comenta.

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Uso: $0 <owner/repo> <numero> [login]" >&2
  echo "Ej:  $0 facebook/astryx 4421 gonzoblasco" >&2
  exit 2
fi

REPO="$1"
NUM="$2"
OURS="${3:-gonzoblasco}"

command -v gh >/dev/null 2>&1 || { echo "Error: falta el CLI 'gh'." >&2; exit 3; }
command -v jq >/dev/null 2>&1 || { echo "Error: falta 'jq'." >&2; exit 3; }

# Trae los tres tipos de evento y los normaliza a: ts<TAB>login<TAB>kind<TAB>nota
fetch() {
  local out
  out=$(
    {
      gh api --paginate "repos/$REPO/issues/$NUM/comments" \
        --jq '.[] | [.created_at, .user.login, "comment", (.body|gsub("\n";" ")|.[0:60])] | @tsv' 2>/dev/null || true
      gh api --paginate "repos/$REPO/pulls/$NUM/reviews" \
        --jq '.[] | [(.submitted_at // .created_at), .user.login, ("review:" + (.state|ascii_downcase)), ""] | @tsv' 2>/dev/null || true
      gh api --paginate "repos/$REPO/pulls/$NUM/comments" \
        --jq '.[] | [.created_at, .user.login, "inline", (.body|gsub("\n";" ")|.[0:60])] | @tsv' 2>/dev/null || true
    } | sort
  )
  printf '%s\n' "$out"
}

classify() {
  local login="$1"
  if [ "$login" = "$OURS" ]; then
    echo "OURS"
  # Convencion de GitHub: las cuentas de app llevan el sufijo [bot].
  # Ademas, unos pocos nombres conocidos sin sufijo.
  # NO se usa un glob '*bot': clasificaria 'abbot' o 'talbot' como bot.
  elif [[ "$login" == *"[bot]" ]] || [[ "$login" == "dependabot" ]] || [[ "$login" == "renovate"* ]] || [[ "$login" == "github-actions" ]]; then
    echo "BOT"
  else
    echo "THIRD"
  fi
}

EVENTS=$(fetch)

if [ -z "$EVENTS" ]; then
  echo "Sin eventos en $REPO #$NUM (o el numero no existe / sin permisos)."
  exit 0
fi

echo "=== $REPO #$NUM - hilo por actor (nuestro login: $OURS) ==="
echo

# Detalle clasificado
echo "--- eventos (cronologico) ---"
printf '%s\n' "$EVENTS" | while IFS=$'\t' read -r ts login kind nota; do
  [ -z "${login:-}" ] && continue
  tag=$(classify "$login")
  printf '  %s  %-6s  %-14s %-14s %s\n' "$ts" "$tag" "$login" "$kind" "$nota"
done

echo
echo "--- resumen por actor ---"
printf '%s\n' "$EVENTS" | while IFS=$'\t' read -r ts login kind nota; do
  [ -z "${login:-}" ] && continue
  printf '%s\t%s\n' "$(classify "$login")" "$login"
done | sort | uniq -c | sort -rn | while read -r n tag login; do
  printf '  %-6s %-16s %s evento(s)\n' "$tag" "$login" "$n"
done

echo
echo "--- quien tiene la pelota ---"
# El ultimo acto NO-BOT del hilo. Los bots de review no mueven el estado.
LAST=$(printf '%s\n' "$EVENTS" | while IFS=$'\t' read -r ts login kind nota; do
  [ -z "${login:-}" ] && continue
  [ "$(classify "$login")" = "BOT" ] && continue
  printf '%s\t%s\t%s\n' "$ts" "$login" "$kind"
done | tail -1)

if [ -z "$LAST" ]; then
  echo "  (solo hay eventos de bots: nadie humano actuo todavia)"
else
  LTS=$(printf '%s' "$LAST" | cut -f1)
  LLOGIN=$(printf '%s' "$LAST" | cut -f2)
  LKIND=$(printf '%s' "$LAST" | cut -f3)
  TAG=$(classify "$LLOGIN")
  if [ "$TAG" = "OURS" ]; then
    echo "  NOSOTROS ($LLOGIN) - $LKIND @ $LTS [la pelota nos toca / esperamos a otro]"
  else
    echo "  TERCERO ($LLOGIN) - $LKIND @ $LTS [la pelota la tiene $LLOGIN, no nosotros]"
  fi
fi

echo
echo "Regla: 'nuestro' = login $OURS verificado aca. Cualquier otra cuenta es tercero,"
echo "INCLUIDOS maintainers que revisan nuestro trabajo en este repo. No inferir por contexto."
