#!/usr/bin/env bash
# Watchdog de presupuesto de disco por agente (E3.2).
#
# READ-ONLY, a proposito: mide y avisa. NO borra, NO rota, NO mueve nada.
# Los .bak de migracion son respaldos reales: borrarlos es decision humana,
# no de un watchdog. Un check que "arregla" solo es un check que puede
# destruir datos de noche.
#
# Exit codes (contrato que consume el trigger):
#   0 = todo bajo los umbrales
#   1 = algun umbral cruzado            -> dispara alerta
#   2 = no se pudo medir                -> TAMBIEN dispara
#
# Umbrales configurables por env (las pruebas los usan):
#   AGENT_DB_MAX_GB   DB viva de un agente      (default 4)
#   AGENT_DIR_MAX_GB  directorio de un agente   (default 6)
set -uo pipefail

AGENT_DB_MAX_GB="${AGENT_DB_MAX_GB:-4}"
AGENT_DIR_MAX_GB="${AGENT_DIR_MAX_GB:-6}"
ROOT="${OPENCLAW_AGENTS_ROOT:-$HOME/.openclaw/agents}"

if [[ ! -d "$ROOT" ]]; then
  echo "No existe el directorio de agentes: $ROOT"
  exit 2
fi

# awk con bytes -> GB (base 1024) y comparacion contra el umbral.
# Se usa awk porque macOS no tiene `bc` garantizado ni `numfmt`.
REPORT="$(find "$ROOT" -maxdepth 3 -type f -name '*.sqlite' -not -name '*-wal' -not -name '*-shm' -print0 2>/dev/null \
  | xargs -0 -I{} du -k {} 2>/dev/null \
  | awk -v dbmax="$AGENT_DB_MAX_GB" -v dirmax="$AGENT_DIR_MAX_GB" '
    {
      kb = $1; path = $2;
      gb = kb / 1048576;
      if (gb > dbmax) {
        printf "DB GRANDE %.2fGB %s\n", gb, path;
        bad = 1;
      }
    }
    END { exit 0 }
  ')"

DIR_REPORT="$(find "$ROOT" -mindepth 1 -maxdepth 1 -type d 2>/dev/null \
  | while IFS= read -r d; do
      kb="$(du -sk "$d" 2>/dev/null | awk '{print $1}')"
      [[ -z "$kb" ]] && continue
      awk -v kb="$kb" -v max="$AGENT_DIR_MAX_GB" -v d="$d" '
        BEGIN {
          gb = kb / 1048576;
          if (gb > max) printf "DIR GRANDE %.2fGB %s\n", gb, d;
        }'
    done)"

if [[ -z "$REPORT" && -z "$DIR_REPORT" ]]; then
  exit 0
fi

[[ -n "$REPORT" ]] && echo "$REPORT"
[[ -n "$DIR_REPORT" ]] && echo "$DIR_REPORT"
echo ""
echo "Umbrales: DB viva ${AGENT_DB_MAX_GB}GB, directorio de agente ${AGENT_DIR_MAX_GB}GB."
echo "Este check solo avisa. No borra nada: los .bak de migracion son respaldos."
exit 1
