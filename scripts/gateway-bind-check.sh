#!/usr/bin/env bash
# gateway-bind-check.sh - Detecta la degradacion silenciosa de gateway.bind.
#
# POR QUE EXISTE (2026-11-10). Con gateway.bind="tailnet", el gateway necesita
# una IPv4 del tailnet disponible EN EL MOMENTO de arrancar. Si el proceso de
# LaunchAgent gana la carrera contra Tailscale, cae a loopback y se queda ahi
# sin decirlo: el archivo sigue diciendo "tailnet", el proceso escucha en
# 127.0.0.1, y la unica senal es que un cliente remoto no conecta.
#
# Eso fue lo que paso el 2026-11-09 19:34 (el gateway volvio en loopback) y lo
# que dejo la puerta abierta al segundo sintoma del 2026-11-10: la Control UI
# hace `config.patch` con el estado que ve correr, asi que escribio "loopback"
# sobre el archivo y se llevo puestos bind, tailscale.mode y allowedOrigins.
# Un desvio de runtime se convirtio en un cambio de config.
#
# Uso: gateway-bind-check.sh [--json]
# Exit 0 = el bind configurado coincide con lo que escucha.
# Exit 1 = no coincide (degradacion) o falta evidencia.
set -uo pipefail

JSON_OUT=false
[[ "${1:-}" == "--json" ]] && JSON_OUT=true

CONFIG="$HOME/.openclaw/openclaw.json"
TS_BIN="/Applications/Tailscale.app/Contents/MacOS/Tailscale"
PORT="$(python3 -c "import json;print(json.load(open('$CONFIG'))['gateway'].get('port',18789))" 2>/dev/null || echo 18789)"
BIND="$(python3 -c "import json;print(json.load(open('$CONFIG'))['gateway'].get('bind','loopback'))" 2>/dev/null || echo "?")"

LISTEN="$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | awk 'NR>1{print $9}' | sed 's/:[0-9]*$//' | sort -u)"
TS_IP="$("$TS_BIN" ip -4 2>/dev/null | head -1)"

status="ok"
detail=""

case "$BIND" in
  tailnet)
    if [ -z "$TS_IP" ]; then
      status="unknown"
      detail="bind=tailnet pero Tailscale no reporta IPv4 (¿daemon caido?)"
    elif ! printf '%s\n' "$LISTEN" | grep -qx "$TS_IP"; then
      status="degraded"
      detail="bind=tailnet ($TS_IP) pero escucha en: $(echo $LISTEN | tr '\n' ' ')— arranco antes que Tailscale; hay que reiniciar el gateway"
    fi
    ;;
  loopback)
    # Con bind=loopback no debe haber NINGUN listener fuera de loopback: si el
    # proceso arranco antes de un cambio de bind, sigue expuesto y este check
    # lo dejaba pasar (paso el 2026-11-10: decia OK con 100.126.255.95 abierto).
    exposed="$(printf '%s\n' "$LISTEN" | grep -vx '127.0.0.1' | grep -vx '\[::1\]' | grep -v '^$' | tr '\n' ' ')"
    if ! printf '%s\n' "$LISTEN" | grep -qx "127.0.0.1"; then
      status="degraded"
      detail="bind=loopback pero no escucha en 127.0.0.1: $(echo $LISTEN | tr '\n' ' ')"
    elif [ -n "$exposed" ]; then
      status="degraded"
      detail="bind=loopback pero hay listeners fuera de loopback: $exposed (proceso sin reiniciar tras el cambio de bind)"
    fi
    ;;
  *)
    status="unknown"
    detail="bind desconocido: $BIND"
    ;;
esac

if $JSON_OUT; then
  printf '{"bind":"%s","tailnetIp":"%s","listeners":"%s","status":"%s","detail":"%s"}\n' \
    "$BIND" "$TS_IP" "$(echo $LISTEN | tr '\n' ',')" "$status" "$detail"
else
  case "$status" in
    ok)       echo "OK: bind=$BIND coincide con lo que escucha ($(echo $LISTEN | tr '\n' ' '))" ;;
    degraded) echo "PROBLEMA: $detail" ;;
    *)        echo "AVISO: $detail" ;;
  esac
fi

[[ "$status" == "ok" ]] || exit 1
