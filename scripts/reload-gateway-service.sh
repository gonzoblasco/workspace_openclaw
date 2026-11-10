#!/bin/sh
# reload-gateway-service.sh - Reimporta el LaunchAgent del gateway sin depender
# del proceso que lo sirve.
#
# POR QUE EXISTE (2026-11-10). Un plist reescrito mientras el job seguia cargado
# deja launchd en "partial import": el chequeo de propiedad del propio OpenClaw
# falla con service-ownership-changed y bloquea la proxima actualizacion. Doctor
# no puede arreglarlo porque el chequeo que falla es el mismo que autoriza el
# arreglo. Se reimporta a mano.
#
# Este script NO se ejecuta desde el gateway: lo lanza `launchctl submit`, asi
# sobrevive al bootout que mata al propio gateway.
LOG="$HOME/.openclaw/service-reload.log"
PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
LABEL="gui/501/ai.openclaw.gateway"

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') reload solicitado ==="
  sleep 20   # deja salir la respuesta del agente antes de matar el proceso

  echo "[1] bootout"
  launchctl bootout "$LABEL" 2>&1
  sleep 3

  echo "[2] bootstrap"
  ok=0
  for i in 1 2 3 4 5; do
    if launchctl bootstrap gui/501 "$PLIST" 2>&1; then ok=1; break; fi
    echo "    intento $i fallo; reintento en 3s"
    sleep 3
  done

  if [ "$ok" -eq 0 ]; then
    echo "[3] FALLBACK: launchctl load -w"
    launchctl load -w "$PLIST" 2>&1
  fi

  sleep 5
  echo "[4] estado final"
  launchctl list 2>/dev/null | grep ai.openclaw.gateway || echo "    NO CARGADO"
  echo "=== fin ==="
} >> "$LOG" 2>&1
