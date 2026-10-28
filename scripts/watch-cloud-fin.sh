#!/usr/bin/env bash
# Watcher de FASES de la cata de harnesses (2026-10-28).
#
# Por que una automatizacion y no un proceso encadenado: un proceso colgado
# (nohup &) muere cuando el exec que lo lanzo termina. La automatizacion
# persiste en el gateway y este trigger corre cada 5 minutos.
#
# El trigger es una MAQUINA DE ESTADOS, no un "el cloud termino?":
#
#   A. la cloud termino y la local todavia no arranco  -> dispara "arranca la local"
#   B. la local esta corriendo                          -> NO dispara (evita relanzar
#                                                          una segunda tanda en paralelo)
#   C. la local termino (con o sin todos los sellos)    -> dispara "analisis final"
#
# POR QUE B importa: la local dura horas y tiene ventanas SIN runner.py
# (descargar el modelo, dormir 3 s, cambiar de harness). Si en esa ventana el
# trigger disparara, el agent volveria a lanzar run-local-1task.sh y se
# medirian celdas en duplicado. Por eso se mira el DRIVER (run-local-1task.sh),
# no solo el runner.
set -uo pipefail

OUT="/tmp/cata-harnesses"

# Los 4 modelos locales y su slug (tr ':/' -> '__', como en run-local-1task.sh).
LOCALES=(
  "hf.co_ModernoTech_nova-2b_latest"
  "ornith-1.5_9b"
  "gemma4_12b-mlx"
  "qwen3.5_9b-mlx"
)

# El informe final ya se hizo -> no volver a disparar.
SELLO_FINAL="$OUT/FINAL-REPORT-DONE"

# --- El motor de la automatizacion -----------------------------------------------------
# Si el driver de la local esta vivo, la tanda SIGUE. No importa que no haya
# runner.py en este instante.
if pgrep -f "run-local-1task\.sh" > /dev/null 2>&1; then
  echo '{"fire": false, "reason": "la fase local sigue en curso"}'
  exit 0
fi
if pgrep -f "chain-local\.sh" > /dev/null 2>&1; then
  echo '{"fire": false, "reason": "la fase local sigue encadenada"}'
  exit 0
fi
if pgrep -f "run-cloud-3\.sh" > /dev/null 2>&1; then
  echo '{"fire": false, "reason": "la fase cloud sigue en curso"}'
  exit 0
fi
if pgrep -f "runner\.py" > /dev/null 2>&1; then
  echo '{"fire": false, "reason": "hay una corrida en curso"}'
  exit 0
fi

# --- La local ya arranco alguna vez? (artefactos o sellos) --------------------------------
local_arrancada=0
for slug in "${LOCALES[@]}"; do
  d="$OUT/$slug"
  if [ -d "$d" ] && { [ -f "$d/LOCAL-DONE" ] || [ -n "$(ls -A "$d/artefactos" 2>/dev/null)" ]; }; then
    local_arrancada=1
    break
  fi
done

# --- C. La local termino: toca el analisis final ------------------------------------------
if [ "$local_arrancada" = "1" ]; then
  if [ -f "$SELLO_FINAL" ]; then
    echo '{"fire": false, "reason": "el informe final ya se hizo"}'
    exit 0
  fi

  n_sellos=0
  celdas=0
  for slug in "${LOCALES[@]}"; do
    [ -f "$OUT/$slug/LOCAL-DONE" ] && n_sellos=$((n_sellos + 1))
    n=$(ls "$OUT/$slug"/artefactos/T1/*.md 2>/dev/null | wc -l | tr -d ' ')
    celdas=$((celdas + n))
  done

  echo "$(python3 - "$n_sellos" "$celdas" <<'PY'
import json, sys
sello, celdas = int(sys.argv[1]), int(sys.argv[2]
msg = (
    "La FASE LOCAL de la cata de harnesses TERMINO.\n\n"
    f"  Modelos locales sellados: {sello}/4\n"
    f"  Celdas T1 con entregable: {celdas}/12\n\n"
    "HACER AHORA (en este orden):\n"
    "1. Correr analyze.py y consolidar la matriz completa (10 modelos x 3 harnesses;\n"
    "   los cloud con 3 tareas y los locales con 1).\n"
    "2. Actualizar docs/evaluacion/cata-harnesses-3-modelos-2026-10-28.md con la matriz\n"
    "   y el analisis (no tocar los resultados: son la verdad de base).\n"
    "3. Commitear y pushear; dejar la CI en verde.\n"
    "4. Escribir el sello /tmp/cata-harnesses/FINAL-REPORT-DONE para que este\n"
    "   watcher no vuelva a disparar.\n"
    "5. Avisarle a Gonzo que puede cerrar Docker Desktop (los containers opencode y\n"
    "   openhands-canvas ya no hacen falta) y reportar el resultado final."
)
print(json.dumps({"fire": True, "message": msg}))
PY
)"
  exit 0
fi

# --- A. La local todavia no arranco -----------------------------------------------------
if [ ! -d "$OUT" ]; then
  echo '{"fire": false, "reason": "no hay resultados de la cata"}'
  exit 0
fi

echo '{"fire": true, "message": "La fase cloud de la cata termino: arranca la fase local (4 modelos locales x 3 harnesses x 1 tarea)."}'
