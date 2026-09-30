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
cp -r "$HOME/.openclaw/workspace/memory" "$BASE/" 2>/dev/null || true
cp -r "$HOME/.openclaw/workspace/docs"   "$BASE/" 2>/dev/null || true

# 3) Retencion: snapshots con mas de 7 dias
find "$HOME/.openclaw/backups" -maxdepth 1 -type d -name 'heartbeat-*' -mtime +7 -exec rm -rf {} + 2>/dev/null || true

echo "$BASE"
