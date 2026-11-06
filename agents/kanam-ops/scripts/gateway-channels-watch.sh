#!/usr/bin/env bash
# Watchdog de canales del gateway (E3.1).
#
# READ-ONLY, a proposito: mide y sale con un codigo. No reinicia canales, no
# toca config. La reparacion vive en el payload del agente que recibe la alerta,
# con su propio limite de aprobacion.
#
# Exit codes (contrato que consume el trigger):
#   0 = todo sano
#   1 = hay un canal caido o degradado  -> dispara alerta
#   2 = no se pudo medir               -> TAMBIEN dispara
#
# El 2 es deliberado: un watchdog que se calla cuando su propio check falla
# parece sano estando roto. Ese fue un bug real del jobs-watcher (2026-09-15).
set -uo pipefail

TIMEOUT="${CHANNELS_TIMEOUT:-45}"

JSON=""
if command -v timeout >/dev/null 2>&1; then
  JSON="$(timeout "$TIMEOUT" openclaw channels status --json 2>&1)"
  rc=$?
else
  # macOS no trae timeout(1) por defecto: perl alarma como reemplazo.
  JSON="$(perl -e 'alarm shift; exec @ARGV' "$TIMEOUT" openclaw channels status --json 2>&1)"
  rc=$?
fi

if [[ $rc -ne 0 ]]; then
  echo "No se pudo consultar 'openclaw channels status' (exit $rc)."
  echo "$JSON" | head -5
  exit 2
fi

# El comando puede imprimir avisos antes del JSON. Se recorta desde la primera llave.
JSON="$(printf '%s' "$JSON" | sed -n '/^{/,$p')"

REPORT="$(printf '%s' "$JSON" | python3 -c '
import json, sys

try:
    data = json.load(sys.stdin)
except Exception as e:
    print("__UNPARSEABLE__: " + str(e))
    sys.exit(0)

chans = data.get("channels") or {}
if not isinstance(chans, dict) or not chans:
    print("__EMPTY__")
    sys.exit(0)

bad = []
for name, c in sorted(chans.items()):
    if not isinstance(c, dict):
        continue
    if c.get("enabled") is False:
        continue  # deshabilitado a drede no es una caida
    lifecycle = c.get("lifecycle") or "?"
    running = c.get("running")
    configured = c.get("configured")
    if running is True and lifecycle in ("ready",):
        continue
    bad.append((name, lifecycle, running, configured))

if not bad:
    print("OK")
    sys.exit(0)

for name, lifecycle, running, configured in bad:
    print("CAIDO %s: lifecycle=%s running=%s configured=%s"
          % (name, lifecycle, running, configured))
sys.exit(0)
')"

case "$REPORT" in
  OK)
    exit 0
    ;;
  __UNPARSEABLE__*)
    echo "La salida de channels status no es JSON valido: ${REPORT#__UNPARSEABLE__: }"
    exit 2
    ;;
  __EMPTY__)
    echo "channels status no reporto ningun canal. O no hay canales configurados, o el reporte esta roto."
    exit 2
    ;;
  *)
    echo "$REPORT"
    exit 1
    ;;
esac
