#!/usr/bin/env bash
# Refresca el cache del estado de canales (E3.1).
#
# POR QUE EXISTE
# --------------
# El watchdog medía con `openclaw channels status --json` dentro del code-mode
# del trigger. Ese comando arranca un Node completo, y dentro del sandbox del
# trigger se encola detras de otros procesos: 1.8s a mano, 50-80s ahi. El
# trigger da ~30s, asi que el job moria por timeout en rafaga (2026-11-09 y de
# nuevo 2026-11-18, con corridas de 49 a 83 segundos).
#
# Subir el timeout del trigger NO es opcion: no es configurable por job.
#
# Solucion: separar medir de decidir, igual que drift/risk-policy.
#   - ESTE script mide, sin apuro, fuera del trigger (lo corre un job lento
#     o la propia alerta anterior).
#   - El trigger solo LEE un archivo. Leer un archivo no tiene timeout.
#
# El cache es JSON con el veredicto ya calculado, para que el trigger no tenga
# que interpretar nada.
set -uo pipefail

CACHE="${CHANNELS_CACHE:-$HOME/.openclaw/gateway-channels-state.json}"
TIMEOUT="${CHANNELS_TIMEOUT:-25}"
WATCH="$(cd "$(dirname "$0")" && pwd)/gateway-channels-watch.sh"

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

# La medicion en si sigue viviendo en gateway-channels-watch.sh: un solo
# duenio de la logica.
CHANNELS_TIMEOUT="$TIMEOUT" bash "$WATCH" > "$tmp" 2>&1
rc=$?

{
  printf '{\n'
  printf '  "ts": "%s",\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '  "exitCode": %d,\n' "$rc"
  printf '  "healthy": %s,\n' "$([ "$rc" -eq 0 ] && echo true || echo false)"
  printf '  "detail": %s\n' "$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' < "$tmp")"
  printf '}\n'
} > "$CACHE.new"

mv "$CACHE.new" "$CACHE"
echo "Cache actualizado: $CACHE (exit $rc)"
exit 0
