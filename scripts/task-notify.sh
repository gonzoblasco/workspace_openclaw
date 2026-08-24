#!/bin/bash
# task-notify.sh - Desktop notification when an agent finishes a task (macOS).
#
# Ported concept from the Task Notifier plugin (ClawHub). Shows a native
# macOS notification so the orchestrator/human knows a background agent
# finished without polling. Useful for the A/B pipeline.
#
# Usage:
#   task-notify.sh "Task done" "Agente B termino U2 - listo para review"
#   task-notify.sh <title> <message> [sound]
#
# On macOS uses osascript. No-op silently on non-macOS.

set -uo pipefail

TITLE="${1:-Kanam}"
MSG="${2:-Tarea terminada}"
SOUND="${3:-}"

if [ "$(uname)" != "Darwin" ]; then
  echo "[task-notify] no macOS, skip notificacion" >&2
  exit 0
fi

# Escape for AppleScript (double quotes)
TITLE_ESC=$(echo "$TITLE" | sed 's/"/\\"/g')
MSG_ESC=$(echo "$MSG" | sed 's/"/\\"/g')

if [ -n "$SOUND" ]; then
  osascript -e "display notification \"$MSG_ESC\" with title \"$TITLE_ESC\" sound name \"$SOUND\"" 2>/dev/null
else
  osascript -e "display notification \"$MSG_ESC\" with title \"$TITLE_ESC\"" 2>/dev/null
fi

echo "[task-notify] $TITLE: $MSG"
