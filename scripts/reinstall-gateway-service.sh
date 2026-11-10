#!/bin/sh
# reinstall-gateway-service.sh - Regenera la definicion del servicio y recarga
# el job. Se lanza con `launchctl submit` para sobrevivir al reinicio.
#
# POR QUE (2026-11-10): `launchctl bootstrap` a mano devolvio EIO cinco veces y
# dejo el job en "partial import", con reinicios cada 60-90s y el chequeo de
# propiedad de OpenClaw fallando. `gateway install --force` es el camino
# soportado: regenera plist + wrapper y recarga desde cero.
LOG="$HOME/.openclaw/service-reload.log"

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') install --force solicitado ==="
  sleep 20   # deja salir la respuesta del agente

  echo "[1] openclaw gateway install --force"
  openclaw gateway install --force 2>&1

  sleep 8
  echo "[2] estado del job"
  launchctl print gui/501/ai.openclaw.gateway 2>/dev/null | grep -iE "properties|pid =|state = " | head -4

  echo "[3] listeners y health"
  lsof -nP -iTCP:18789 -sTCP:LISTEN 2>/dev/null | awk 'NR>1{print "   "$9}'
  echo "   loopback: $(curl -s -o /dev/null -w '%{http_code}' -m 8 http://127.0.0.1:18789/health)"
  echo "   https:    $(curl -s -o /dev/null -w '%{http_code}' -m 12 https://mac-mini-de-gonzalo-1.tailca859c.ts.net/health)"

  echo "[4] bind check"
  bash /Users/gonzoblasco/.openclaw/workspace/scripts/gateway-bind-check.sh 2>&1
  echo "=== fin ==="
} >> "$LOG" 2>&1
