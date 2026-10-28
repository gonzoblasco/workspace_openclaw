#!/usr/bin/env bash
# Dispara cuando la fase CLOUD de la cata termino: la fase local arranca sola.
#
# Por que una automatizacion y no un proceso encadenado: un proceso colgado
# (nohup &) muere cuando el exec que lo lanzo termina. La automatizacion
# persiste en el gateway y el trigger corre cada 5 minutos.
set -uo pipefail

OUT="/tmp/cata-harnesses"
SELLO="$OUT/LOCAL-DONE"

# 1. La fase local ya corrio?
if [ -f "$SELLO" ]; then
  echo '{"fire": false, "reason": "la fase local ya corrio"}'
  exit 0
fi

# 2. La fase cloud sigue corriendo?
if pgrep -f "run-cloud-3.sh" > /dev/null 2>&1; then
  echo '{"fire": false, "reason": "la fase cloud sigue en curso"}'
  exit 0
fi

# 3. Hay una corrida en curso de cualquier tipo?
if pgrep -f "runner\.py" > /dev/null 2>&1; then
  echo '{"fire": false, "reason": "hay una corrida en curso"}'
  exit 0
fi

# 4. El cloud dejo resultados? (si no, seAbortó y no hay que seguir)
if [ ! -d "$OUT" ]; then
  echo '{"fire": false, "reason": "no hay resultados de la cata"}'
  exit 0
fi

echo '{"fire": true, "message": "La fase cloud de la cata termino: arranca la fase local (4 modelos locales x 3 harnesses x 1 tarea)."}'
