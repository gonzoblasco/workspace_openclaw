#!/usr/bin/env bash
# Watcher: avisa si Docker quedo ABIERTO despues de la cata de harnesses.
#
# POR QUE: la VM de Docker reserva 7,7 GB de los 24 GB del host como memoria
# WIRED. Con Docker abierto quedan 0,14 GB libres; con Docker cerrado, 8,32 GB.
# Los runners MLX de Ollama expiran solos a los 5 minutos: lo que NO expira
# nunca es la VM de Docker.
#
# REGLA: dispara si Docker esta abierto Y hay evidencia de que hubo cata Y no
# hay ninguna corrida en curso. No depende de un marcador de fin: si la sesion
# muere a mitad de camino, el aviso sigue siendo valido.
set -uo pipefail

OUT="/tmp/cata-harnesses"
CATA_DIR="/Users/gonzoblasco/.openclaw/workspace/playground/cata-harnesses-2026-10-27"
STAMP="/tmp/cata-harnesses/.docker-alert-stamp"
COOLDOWN=3600   # segundos entre avisos (1 hora)

# 1. Docker abierto?
if ! pgrep -f "Docker.app" > /dev/null 2>&1; then
  rm -f "$STAMP"
  echo '{"fire": false, "reason": "docker ya esta cerrado"}'
  exit 0
fi

# 2. Hubo cata?
if [ ! -d "$OUT" ]; then
  echo '{"fire": false, "reason": "no hay cata en esta maquina"}'
  exit 0
fi

# 3. Todavia hay corridas en curso?
# OJO: el runner se lanza como "python runner.py" con cwd en la cata, asi que
# el comando NO contiene la ruta. Hay que mirar el cwd del proceso, no su argv.
runner_vivo() {
  local pids p
  pids=$(pgrep -f "runner\.py" 2>/dev/null)
  [ -z "$pids" ] && return 1
  for p in $pids; do
    if lsof -a -p "$p" -d cwd -Fn 2>/dev/null | grep -qx "n$CATA_DIR"; then
      return 0
    fi
  done
  return 1
}

if runner_vivo; then
  rm -f "$STAMP"
  echo '{"fire": false, "reason": "la cata sigue en curso"}'
  exit 0
fi

# 3b. El driver de la tanda esta vivo (puede estar entre modelos, sin runner).
if pgrep -f "run-sweep-9\.sh|run-cloud-3\.sh|run-all\.sh" > /dev/null 2>&1; then
  rm -f "$STAMP"
  echo '{"fire": false, "reason": "la tanda sigue en curso"}'
  exit 0
fi

# 4. Cooldown: el aviso es util mientras Docker siga abierto, pero no cada 7
# minutos. Se dispara una vez por hora como maximo. El sello se borra cuando
# la cata arranca de nuevo o cuando Docker se cierra.
NOW=$(date +%s)
if [ -f "$STAMP" ]; then
  LAST=$(cat "$STAMP" 2>/dev/null || echo 0)
  if [ "$((NOW - LAST))" -lt "$COOLDOWN" ]; then
    echo '{"fire": false, "reason": "ya se aviso hace poco (cooldown)"}'
    exit 0
  fi
fi
echo "$NOW" > "$STAMP"

# 4. Docker abierto y la cata no esta corriendo: hay que avisar.
MSG="La cata de harnesses ya no tiene corridas en curso y Docker Desktop sigue ABIERTO. La VM de Docker reserva 7,7 GB de los 24 GB del host como memoria wired: con Docker abierto quedan 0,14 GB libres y con Docker cerrado 8,32 GB. Los runners MLX de Ollama expiran solos a los 5 minutos; la VM de Docker NO expira nunca. Cerralo con: osascript -e 'quit app \"Docker\"'  (o pedile a Kanam que lo cierre)."
python3 - "$MSG" <<'PY'
import json, sys
print(json.dumps({"fire": True, "message": sys.argv[1]}))
PY
