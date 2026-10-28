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
#
# TRAMPA QUE YA MORDIÓ (2026-10-28 11:00): la fase cloud termina, la fase
# local arranca un minuto despues, y en ese hueco el watcher vio "Docker
# abierto + nada corriendo" y aviso. La fase local SI necesita Docker
# (opencode y openhands corrian en contenedores; AMBOS FUERON ELIMINADOS el
# 2026-10-28, ver ADR-106, asi que hoy la cata no necesita Docker en absoluto.
# El watcher se mantiene por si se reintroduce un harness en Docker). Por eso
# el watcher no se
# conforma con mirar procesos: mira el ESTADO de la cata. La fase local sella
# cada modelo con LOCAL-DONE; si faltan sellos, la cata NO termino.
set -uo pipefail

OUT="${CATA_OUT:-/tmp/cata-harnesses}"
CATA_DIR="${CATA_DIR_OVERRIDE:-/Users/gonzoblasco/.openclaw/workspace/playground/cata-harnesses-2026-10-27}"
STAMP="${CATA_OUT:-/tmp/cata-harnesses}/.docker-alert-stamp"
COOLDOWN=3600   # segundos entre avisos (1 hora)
GRACE=5400      # 90 min: hueco maximo que se tolera sin sello ni driver vivo

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
# OJO: pgrep -f matchea cualquier linea de comando que MENCIONE el nombre,
# incluyendo los wrappers "zsh -f -c ... run-local-1task.sh" de mis propios
# comandos de diagnostico. Por eso se descartan los comandos con " -c ".
driver_vivo() {
  local pids p cmd
  pids=$(pgrep -f "run-sweep-9\.sh|run-cloud-3\.sh|run-all\.sh|run-local-1task\.sh|chain-local\.sh" 2>/dev/null)
  [ -z "$pids" ] && return 1
  for p in $pids; do
    [ "$p" = "$$" ] && continue
    cmd=$(ps -o command= -p "$p" 2>/dev/null)
    case "$cmd" in
      *" -c "*) continue ;;
    esac
    return 0
  done
  return 1
}

if driver_vivo; then
  rm -f "$STAMP"
  echo '{"fire": false, "reason": "la tanda sigue en curso"}'
  exit 0
fi

# 3c. El driver puede haberse lanzado con otro nombre: se busca cualquier
# proceso con cwd en la cata que sea un script o el runner.
driver_por_cwd() {
  local pids p cmd
  pids=$(pgrep -f "\.sh" 2>/dev/null)
  [ -z "$pids" ] && return 1
  for p in $pids; do
    if lsof -a -p "$p" -d cwd -Fn 2>/dev/null | grep -qx "n$CATA_DIR"; then
      cmd=$(ps -o command= -p "$p" 2>/dev/null)
      case "$cmd" in
        *" -c "*) continue ;;
        *runner.py*|*run-*.sh|*chain-*.sh) return 0 ;;
      esac
    fi
  done
  return 1
}

if driver_por_cwd; then
  rm -f "$STAMP"
  echo '{"fire": false, "reason": "la tanda sigue en curso (driver por cwd)"}'
  exit 0
fi

# 3d. ESTADO de la cata: la fase local sella cada modelo con LOCAL-DONE.
# Si faltan sellos, la cata NO termino -> Docker hace falta todavia.
# Los slugs se leen del propio driver para no duplicar la lista a mano.
slugs_locales() {
  local f="$CATA_DIR/run-local-1task.sh" line
  [ -f "$f" ] || return 0
  awk '/^LOCALES=\(/,/\)/' "$f" | sed -n 's/.*"\(.*\)".*/\1/p' | while IFS= read -r line; do
    printf '%s\n' "$(printf '%s' "$line" | tr ':/' '__')"
  done
}

TOTAL=0
SELLADOS=0
PENDIENTES=""
while IFS= read -r s; do
  [ -z "$s" ] && continue
  TOTAL=$((TOTAL + 1))
  if [ -f "$OUT/$s/LOCAL-DONE" ]; then
    SELLADOS=$((SELLADOS + 1))
  else
    PENDIENTES="$PENDIENTES $s"
  fi
done < <(slugs_locales)

if [ "$TOTAL" -gt 0 ] && [ "$SELLADOS" -lt "$TOTAL" ]; then
  # Fase local incompleta. Solo se avisa si ademas lleva mucho tiempo MUERTA
  # (nada cambio en /tmp/cata-harnesses desde hace mas de GRACE).
  # OJO: en macOS (BSD find) no existe -newermt; se usa -mmin.
  # El sello propio se excluye: si no, escribirlo lo convertiria en
  # "actividad reciente" y el aviso nunca volveria a disparar.
  ULTIMO=$(find "$OUT" -type f -mmin -$((GRACE / 60)) ! -name ".docker-alert-stamp" 2>/dev/null | head -1)
  if [ -n "$ULTIMO" ]; then
    rm -f "$STAMP"
    echo "{\"fire\": false, \"reason\": \"fase local incompleta ($SELLADOS/$TOTAL) pero hay actividad reciente\"}"
    exit 0
  fi
  MSG="La fase LOCAL de la cata de harnesses quedo incompleta ($SELLADOS/$TOTAL modelos sellados, pendientes:$PENDIENTES) y no hay ninguna corrida en curso desde hace mas de $((GRACE / 60)) min. Docker Desktop sigue ABIERTO y reserva 7,7 GB de los 24 GB del host como memoria wired. Cerralo con: osascript -e 'quit app \"Docker\"'  (o pedile a Kanam que lo cierre)."
  NOW=$(date +%s)
  if [ -f "$STAMP" ]; then
    LAST=$(cat "$STAMP" 2>/dev/null || echo 0)
    if [ "$((NOW - LAST))" -lt "$COOLDOWN" ]; then
      echo '{"fire": false, "reason": "ya se aviso hace poco (cooldown)"}'
      exit 0
    fi
  fi
  echo "$NOW" > "$STAMP"
  python3 - "$MSG" <<'PY'
import json, sys
print(json.dumps({"fire": True, "message": sys.argv[1]}))
PY
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
