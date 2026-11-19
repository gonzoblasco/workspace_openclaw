#!/usr/bin/env bash
# Watcher de la cola durable del pipeline A/B (Kanam OS).
#
# Reemplaza al trigger-gate de code mode que fallaba por timeout: el gate tiene
# un presupuesto fijo de 30s de wall-clock y 5 tool calls (docs OpenClaw,
# automation/cron-jobs/schedules.md), y la latencia del tool-call lo excedia
# (corridas medidas: 41.8s y 108.8s). Al correr como payload de tipo command no
# hay gate ni modelo: el script decide en milisegundos.
#
# Contrato con el scheduler: si no hay nada que reportar imprime exactamente
# NO_REPLY, que el scheduler suprime sin marcar error. Si hay algo, imprime la
# alerta (2-3 lineas) y esa linea es lo que se entrega.
#
# Diseno de senales (heredado del gate original): la cola no es el driver de
# ejecucion, asi que "queued sin running" en un solo check es normal. Solo se
# alerta si el MISMO conjunto lleva 2 checks seguidos detenido. Las huerfanas y
# las unidades en `failed` son senales duras.

set -euo pipefail

W="$(cd "$(dirname "$0")/.." && pwd)"
cd "$W"

STATE=".pipeline-watch.state"

# 1. Recuperacion deterministica: reencolar huerfanas. Si falla, no abortamos:
#    el reporte de abajo tiene que salir igual.
TICK_OUT="$(./scripts/pipeline-queue.sh tick 2>&1 || true)"

# 2. Observacion
ORPH="$(./scripts/pipeline-queue.sh orphans 2>&1 || true)"
STATUS_OUT="$(./scripts/pipeline-queue.sh status 2>&1 || true)"

# 3. Contadores desde la linea "QUEUED: n RUNNING: n ..." si existe.
num() { printf '%s' "$1" | sed -n "s/.*$2: *\([0-9][0-9]*\).*/\1/p" | head -1; }
QUEUED="$(num "$STATUS_OUT" QUEUED)";  QUEUED="${QUEUED:-0}"
RUNNING="$(num "$STATUS_OUT" RUNNING)"; RUNNING="${RUNNING:-0}"
FAILED="$(num "$STATUS_OUT" FAILED)";   FAILED="${FAILED:-0}"

# 4. Lista de unidades huerfanas (si las hay)
ORPH_LIST="$(printf '%s' "$ORPH" | tr '\n' ' ' | sed 's/  */ /g; s/^ //; s/ $//')"

# 5. Deteccion de stall persistente con estado propio (2 checks seguidos iguales)
KEY="q${QUEUED}-r${RUNNING}"
PREV_KEY=""; PREV_COUNT=0
if [ -f "$STATE" ]; then
  PREV_KEY="$(sed -n 's/^key=//p' "$STATE" | head -1)"
  PREV_COUNT="$(sed -n 's/^count=//p' "$STATE" | head -1)"
  PREV_COUNT="${PREV_COUNT:-0}"
fi

STALL_COUNT=1
if [ "$KEY" = "$PREV_KEY" ] && [ "$QUEUED" -gt 0 ] && [ "$RUNNING" -eq 0 ]; then
  STALL_COUNT=$((PREV_COUNT + 1))
fi
printf 'key=%s\ncount=%s\n' "$KEY" "$STALL_COUNT" > "$STATE"

# 6. Decision
ACTIONABLE=0
if [ -n "$ORPH_LIST" ]; then ACTIONABLE=1; fi
if [ "$FAILED" -gt 0 ]; then ACTIONABLE=1; fi
if [ "$QUEUED" -gt 0 ] && [ "$RUNNING" -eq 0 ] && [ "$STALL_COUNT" -ge 2 ]; then ACTIONABLE=1; fi

if [ "$ACTIONABLE" -eq 0 ]; then
  echo "NO_REPLY"
  exit 0
fi

if [ -n "$ORPH_LIST" ]; then echo "Unidades huérfanas (proceso muerto): $ORPH_LIST"; fi
if [ "$FAILED" -gt 0 ]; then echo "En failed (terminal, no bloquea el resto): $FAILED unidades"; fi
if [ "$QUEUED" -gt 0 ] && [ "$RUNNING" -eq 0 ] && [ "$STALL_COUNT" -ge 2 ]; then
  echo "Cola detenida $STALL_COUNT checks seguidos: $QUEUED pendientes sin nada corriendo."
fi
echo "Estado: queued=$QUEUED running=$RUNNING failed=$FAILED"
printf 'tick: %s\n' "$(printf '%s' "$TICK_OUT" | tr '\n' ' ' | cut -c1-200)"
