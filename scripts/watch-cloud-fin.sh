#!/usr/bin/env bash
# Watcher de FASES de la cata de harnesses (2026-10-28).
#
# Por que una automatizacion y no un proceso encadenado: un proceso colgado
# (nohup &) muere cuando el exec que lo lanzo termina. La automatizacion
# persiste en el gateway y este trigger corre cada 5 minutos.
#
# El trigger es una MAQUINA DE ESTADOS, no un "el cloud termino?":
#
#   A. la cloud termino y la local no arranco  -> dispara "arranca la local"
#   B. la local esta corriendo                  -> NO dispara
#   C. la local se murio a medias               -> dispara "reanuda la local"
#   D. la local termino (4/4 sellados)         -> dispara "informe final"
#
# POR QUE B importa: la local dura horas y tiene ventanas SIN runner.py
# (descargar el modelo, dormir 3 s, cambiar de harness). Si en esa ventana el
# trigger disparara, el agent volveria a lanzar run-local-1task.sh y se
# medirian celdas en duplicado. Por eso se mira el DRIVER (run-local-1task.sh),
# no solo el runner.
#
# POR QUE C importa: si el driver se muere (OOM, reinicio, un crash), el
# driver NO esta vivo pero tampoco termino. Sin el caso C, el watcher
# declararia "termino" con 2 de 4 modelos medidos y publicaria un informe
# final incompleto. Con el, se reanuda: el driver es idempotente (sello por
# modelo), asi que relanzarlo solo repite lo que falto.
set -uo pipefail

# OUT se puede sobreescribir (CATA_OUT) para probar el script en un sandbox
# sin tocar la tanda real.
OUT="${CATA_OUT:-/tmp/cata-harnesses}"

# Los 4 modelos locales y su slug (tr ':/' -> '__', como en run-local-1task.sh).
LOCALES=(
  "hf.co_ModernoTech_nova-2b_latest"
  "ornith-1.5_9b"
  "gemma4_12b-mlx"
  "qwen3.5_9b-mlx"
)

SELLO_FINAL="$OUT/FINAL-REPORT-DONE"
CONTADOR_RESUME="$OUT/RESUME-COUNT"
MAX_RESUME=3

# --- B. Algo esta corriendo? No se molesta al driver en curso ---------------------------
# El driver de la local manda sobre todo: si esta vivo, la tanda SIGUE, sin
# importar que no haya runner.py en este instante.
if pgrep -f "run-local-1task\.sh" > /dev/null 2>&1; then
  # El driver esta vivo: la tanda SIGUE. Se reinicia el contador de reanudar
  # porque un reinicio exitoso es un episode nuevo.
  rm -f "$CONTADOR_RESUME"
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

# --- Estado de la local ------------------------------------------------------------------
n_sellos=0
celdas=0
local_arrancada=0
for slug in "${LOCALES[@]}"; do
  d="$OUT/$slug"
  [ -f "$d/LOCAL-DONE" ] && n_sellos=$((n_sellos + 1))
  n=$(ls "$d"/artefactos/T1/*.md 2>/dev/null | wc -l | tr -d ' ')
  celdas=$((celdas + n))
  if [ -d "$d" ] && { [ -f "$d/LOCAL-DONE" ] || [ -n "$(ls -A "$d/artefactos" 2>/dev/null)" ]; }; then
    local_arrancada=1
  fi
done

# --- D. La local termino: toca el informe final -----------------------------------------
if [ "$local_arrancada" = "1" ] && [ "$n_sellos" -eq 4 ]; then
  if [ -f "$SELLO_FINAL" ]; then
    echo '{"fire": false, "reason": "el informe final ya se hizo"}'
    exit 0
  fi

  echo "$(python3 - "$n_sellos" "$celdas" <<'PY'
import json, sys
sello, celdas = int(sys.argv[1]), int(sys.argv[2])
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

# --- C. La local arranco pero no termino: se murio. Se reanuda --------------------------
if [ "$local_arrancada" = "1" ]; then
  if [ -f "$SELLO_FINAL" ]; then
    echo '{"fire": false, "reason": "el informe final ya se hizo"}'
    exit 0
  fi

  intentos=0
  [ -f "$CONTADOR_RESUME" ] && intentos=$(cat "$CONTADOR_RESUME" 2>/dev/null || echo 0)
  case "$intentos" in ''|*[!0-9]*) intentos=0 ;; esac

  if [ "$intentos" -ge "$MAX_RESUME" ]; then
    # Se reintento demasiado: no es un crash transitorio. Better un informe
    # final con lo que hay que un bucle infinito de relanzamientos.
    echo "$(python3 - "$n_sellos" "$celdas" "$intentos" <<'PY'
import json, sys
sello, celdas, intentos = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
msg = (
    "La FASE LOCAL de la cata de harnesses NO pudo completarse.\n\n"
    f"  Modelos locales sellados: {sello}/4 (faltan {4 - sello})\n"
    f"  Celdas T1 con entregable: {celdas}/12\n"
    f"  Reintentos de reanudacion agotados: {intentos}\n\n"
    "HACER AHORA:\n"
    "1. Correr analyze.py y consolidar la matriz con lo que HAY (10 modelos x 3\n"
    "   harnesses; los cloud con 3 tareas y los locales con 1). Marcar en el informe\n"
    "   los locales que quedaron sin medir y POR QUE.\n"
    "2. Actualizar docs/evaluacion/cata-harnesses-3-modelos-2026-10-28.md con la matriz\n"
    "   y el analisis (no tocar los resultados: son la verdad de base).\n"
    "3. Commitear y pushear; dejar la CI en verde.\n"
    "4. Escribir el sello /tmp/cata-harnesses/FINAL-REPORT-DONE.\n"
    "5. Avisarle a Gonzo que puede cerrar Docker Desktop y reportar el resultado\n"
    "   final, incluyendo los locales que faltaron."
)
print(json.dumps({"fire": True, "message": msg}))
PY
)"
    exit 0
  fi

  echo $((intentos + 1)) > "$CONTADOR_RESUME"
  echo "$(python3 - "$n_sellos" "$celdas" "$intentos" <<'PY'
import json, sys
sello, celdas, intentos = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
msg = (
    "La FASE LOCAL de la cata de harnesses SE MURIO a medias: hay que REANUDARLA.\n\n"
    f"  Modelos locales sellados: {sello}/4 (faltan {4 - sello})\n"
    f"  Celdas T1 con entregable: {celdas}/12\n"
    f"  Reintento de reanudacion: {intentos + 1}/3\n\n"
    "HACER AHORA:\n"
    "1. Relanza el driver EN BACKGROUND (es idempotente: saltea los modelos ya\n"
    "   sellados y solo repite los que faltan):\n"
    "   cd /Users/gonzoblasco/.openclaw/workspace/playground/cata-harnesses-2026-10-27\n"
    "   ./run-local-1task.sh\n"
    "2. NO cierres Docker: opencode y OpenHands son containers.\n"
    "3. NO borres /tmp/cata-harnesses: los artefactos son la verdad de base.\n"
    "4. Reporta el progreso con python3 playground/cata-harnesses-2026-10-27/status.py."
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
