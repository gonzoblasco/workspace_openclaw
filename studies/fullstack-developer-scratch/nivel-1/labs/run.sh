#!/usr/bin/env bash
# run.sh - Corre el checker contra todos los labs del Nivel 1.
#
# Uso:
#   ./run.sh          # estado de todo
#   ./run.sh lab3     # solo uno
#
# Exit 0 = todos los labs pasan. 1 = alguno falla (imprime cual).
#
# Por que existe: con 7 labs, correr uno por uno se olvida. Un solo comando
# dice donde estas parado y cual sigue.

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

LABS_ALL=(lab1 lab2 lab3 lab5 lab6 lab8 lab9)
LABS=("${@:-}")
if [ -z "${1:-}" ]; then LABS=("${LABS_ALL[@]}"); fi

pass=0
fail=0
failed_names=()

for l in "${LABS[@]}"; do
  if [ ! -d "$l" ]; then
    echo "  ??  $l no existe"
    continue
  fi
  out=$(python3 check.py "$l" "$l" 2>&1)
  rc=$?
  if [ $rc -eq 0 ]; then
    echo "  ✅  $l"
    pass=$((pass+1))
  else
    echo "  ❌  $l"
    echo "$out" | grep 'FAIL' | sed 's/^/        /'
    fail=$((fail+1))
    failed_names+=("$l")
  fi
done

echo
echo "────────────────────────────"
echo "  $pass OK · $fail pendientes"
if [ $fail -gt 0 ]; then
  echo "  Siguiente: ${failed_names[0]}  (./run.sh ${failed_names[0]})"
  exit 1
fi
echo "  Nivel 1 completo ✅"
exit 0
