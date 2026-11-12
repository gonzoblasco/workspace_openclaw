#!/usr/bin/env bash
# agente-minimo.sh - el loop más pequeño posible: actuar -> ver -> adaptarse.
# El harness NO razona. Solo da tools y devuelve el resultado. El loop es esto.
set -uo pipefail

TAREA="${1:-corre el test}"
CMD="${2:-node test-malo.mjs}"
MAX=3
i=0

while [ $i -lt $MAX ]; do
  i=$((i+1))
  echo "── vuelta $i ─────────────"
  OUT=$(eval "$CMD" 2>&1); RC=$?
  echo "   actuo: $CMD"
  echo "   exit: $RC"
  if [ $RC -eq 0 ]; then
    echo "   VERDE -> el loop termina"
    exit 0
  fi
  echo "   ROJO -> el harness DEVUELVE la señal al modelo"
  echo "   señal: $(echo "$OUT" | grep -m1 'AssertionError\|Error' )"
done
echo "── se agotaron las $MAX vueltas (esto es lo que ve un modelo sin tool) ──"
exit 1
