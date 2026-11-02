#!/bin/sh
# Ollama watchdog (operativo).
#
# Objetivo: que el server de Ollama en 127.0.0.1:11434 nunca se quede caido.
# El 2026-11-02 estuvo muerto 1h42m (10:07 -> 11:49) y con el cayeron TODOS los
# modelos, incluidos los :cloud, porque el transporte es el mismo socket.
#
# Por que un loop y no un `exec ollama serve`:
#   un wrapper que hace `exec serve` y muere con el server deja el LaunchAgent
#   inactivo entre caidas (KeepAlive solo vigila SU proceso). Como watchdog,
#   este script nunca sale mientras el host viva: cada CHECK_INTERVAL revisa
#   salud y, si el server no responde, lo levanta y lo espera.
#
# Convivencia con Ollama.app: si la app ya tiene el puerto, el health check
# pasa y no hacemos nada. Solo levantamos server cuando NO hay nadie.

set -u

CHECK_INTERVAL="${CHECK_INTERVAL:-30}"
HEALTH_URL="${OLLAMA_HEALTH_URL:-http://127.0.0.1:11434/api/version}"
OLLAMA_BIN="${OLLAMA_BIN:-/usr/local/bin/ollama}"
LOG_TAG="ollama-watchdog"

log() { echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') $LOG_TAG: $*"; }

healthy() { curl -s --max-time 3 "$HEALTH_URL" >/dev/null 2>&1; }

log "arrancado (pid $$, interval ${CHECK_INTERVAL}s)"

while :; do
  if healthy; then
    sleep "$CHECK_INTERVAL"
    continue
  fi

  log "server caido -> levantando $OLLAMA_BIN serve"
  "$OLLAMA_BIN" serve &
  SERVE_PID=$!

  # Esperar hasta 60s a que responda.
  n=0
  while [ "$n" -lt 60 ]; do
    if healthy; then
      log "server arriba (pid $SERVE_PID)"
      break
    fi
    if ! kill -0 "$SERVE_PID" 2>/dev/null; then
      log "serve salio sin levantar (otro proceso gano el puerto?)"
      break
    fi
    n=$((n + 1))
    sleep 1
  done

  wait "$SERVE_PID" 2>/dev/null
  log "serve termino -> reintento en ${CHECK_INTERVAL}s"
  sleep "$CHECK_INTERVAL"
done
