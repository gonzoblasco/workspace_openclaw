#!/usr/bin/env bash
# heartbeat-snapshot-agent.sh - Snapshot temporal de sesiones (invocado por el job agentTurn).
# NO cierra sesiones: solo copia el estado para poder retomar.
# Uso: heartbeat-snapshot-agent.sh [--agent main]
set -uo pipefail

AGENT="${1:-main}"
TS=$(date +%Y%m%d-%H%M%S)
BASE="$HOME/.openclaw/backups/heartbeat-$TS"
mkdir -p "$BASE"

# 1) Snapshot de cada sesion del agente (trajectory legible, redactado)
openclaw sessions list --json --agent "$AGENT" --limit all 2>/dev/null \
  | python3 -c "import sys,json; d=json.load(sys.stdin); [print(s['key']) for s in d.get('sessions',[]) if s.get('key')]" \
  | while read -r SK; do
      [ -n "$SK" ] || continue
      SAFE=$(printf '%s' "$SK" | tr '/:' '__')
      find "$HOME/.openclaw/backups" -type f -name "$SAFE.md" -delete 2>/dev/null || true
      openclaw sessions tail --session-key "$SK" --tail 200 --agent "$AGENT" > "$BASE/$SAFE.md" 2>/dev/null || true
    done

# 2) Documentos en curso
#
# rsync y no `cp -r`: `cp -r` no lee .gitignore, asi que copiaba enteros los
# videos de docs/entrevistas/mercor-project-odin (108 MB de grabaciones
# confidenciales de Mercor, gitignored a proposito) en CADA snapshot. Con 12
# snapshots/dia eso son ~1,3 GB/dia de material que ya vive en el disco y que
# ademas nunca debe salir del workspace.
#
# Se excluye:
#   *.mp4 / *.mov       grabaciones crudas; su texto derivado si se copia
#   *.pre-rechunk       residuo de rechunk-vectors.py: un backup de DB que
#                       solo sirve durante la migracion que ya termino
#   Odin ... Handbook   el PDF de 25 MB del manual; su texto completo vive en
#                       handbook.txt (27.738 palabras, mismo contenido)
rsync -a \
  --exclude='*.mp4' \
  --exclude='*.mov' \
  --exclude='*.pre-rechunk' \
  --exclude='Project Odin Writer Handbook.pdf' \
  "$HOME/.openclaw/workspace/memory/" "$BASE/memory/" 2>/dev/null || true
rsync -a \
  --exclude='*.mp4' \
  --exclude='*.mov' \
  --exclude='*.pre-rechunk' \
  --exclude='Project Odin Writer Handbook.pdf' \
  "$HOME/.openclaw/workspace/docs/" "$BASE/docs/" 2>/dev/null || true

# 3) Retencion: snapshots con mas de 48 horas
#
# Era 7 dias, pero 7 dias x 12 snapshots x ~69 MB no entraba en disco. El
# proposito del snapshot es poder retomar una sesion reciente; 48 horas
# cubren ese caso y dejan el backup en ~1,6 GB.
#
# 2026-11-09: `-mtime +2` no podaba nada en la practica (93 dirs, 4,3 GB):
# -mtime mide el *mtime del directorio*, que cambia cada vez que se escribe
# dentro (el script borra $SAFE.md de snapshots viejos -> toca el dir viejo
# y lo revive). Ahora se poda por la fecha del nombre `heartbeat-YYYYMMDD-HHMMSS`
# con mas de 48 h, sin depender del mtime. Se mantiene el umbral de 48 h.
CUTOFF=$(date -v-48H +%Y%m%d-%H%M%S 2>/dev/null || date -d '48 hours ago' +%Y%m%d-%H%M%S)
for d in "$HOME/.openclaw/backups"/heartbeat-*; do
  [ -d "$d" ] || continue
  ts=${d##*/heartbeat-}
  [ "$ts" \> "$CUTOFF" ] && continue
  rm -rf "$d" 2>/dev/null || true
done

echo "$BASE"
