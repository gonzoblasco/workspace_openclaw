#!/usr/bin/env bash
# Alerta de drift de config del gateway.
#
# BUG CORREGIDO 2026-11-09: la version anterior tenia `set -euo pipefail` y
# hacia `OUT=$(...drift.sh...)`. Con drift real, drift.sh sale 1 (que es lo
# CORRECTO: encontro drift), y `set -e` mataba el script ahi mismo. Resultado:
# el alerta nunca avisaba cuando habia que avisar, el job fallaba 10 veces
# seguidas y el scheduler lo auto-deshabilitaba. Un watchdog que muere justo
# en el caso que vigila es peor que no tenerlo.
#
# Por eso NO se usa `set -e` sobre la captura: el exit code del medidor es
# DATO, no error. Solo se corta si falta el script.
set -uo pipefail

DRIFT=/Users/gonzoblasco/.openclaw/workspace/agents/kanam-ops/scripts/gateway-config-drift.sh

if [[ ! -x "$DRIFT" ]]; then
  echo "No se encuentra o no es ejecutable: $DRIFT"
  exit 2
fi

OUT="$("$DRIFT" 2>&1)"
RC=$?

# 0 = sin drift (o solo cambios esperados). Nada que avisar: salida vacia.
if [[ $RC -eq 0 ]]; then
  exit 0
fi

# drift.sh usa 1 para drift sin explicar y 2 para error de lectura.
# Los dos merecen aviso: un drift que no se puede leer no es "todo bien".
if [[ $RC -eq 2 ]]; then
  PREFIX="No se pudo medir el drift"
else
  PREFIX="Drift detectado en gateway-config"
fi

echo "$PREFIX (exit $RC)"
echo "$OUT"

# SEGUNDO BUG CORREGIDO 2026-11-09: este script salia 1 para señalar drift, y
# el job lo interpretaba como "command error with no output": lo marcaba error,
# no entregaba el mensaje, y a la decima vez el scheduler lo deshabilitaba.
#
# En este job el exit code NO es el canal de la alerta: el mensaje lo entrega
# el `--announce` con el stdout. Por eso sale 0 siempre que haya podido MEDIR.
# El exit 2 sigue siendo error real: si no se puede medir, eso si es falla.
if [[ $RC -eq 2 ]]; then
  exit 2
fi
exit 0
