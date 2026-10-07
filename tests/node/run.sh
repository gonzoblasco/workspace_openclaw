#!/usr/bin/env bash
# Runner de los tests Node del workspace.
#
# Por que existe (2026-10-06): `tests/node/` tenia tres suites (pipeline-queue,
# gateway-jobs-watcher y el clasificador de a11y-scan) y NINGUNA corria en CI -
# solo bats (tests/bash) y pytest (tests/python) estaban cableados. Una suite
# que nadie invoca no verifica nada: es el mismo patron que la Etapa 2 (gates
# que existen y no se invocan). Este runner es el punto de entrada unico.
#
# Cada archivo *.test.js es autonomo: corre con `node`, imprime su resumen y
# sale con exit != 0 si algo falla. No necesita framework ni dependencias.
set -uo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
fail=0

for t in "$DIR"/*.test.js; do
  [ -e "$t" ] || continue
  echo "=== $(basename "$t") ==="
  if ! node "$t"; then
    fail=1
  fi
  echo
done

if [ "$fail" -ne 0 ]; then
  echo "RUNNER: hubo fallos."
  exit 1
fi
echo "RUNNER: todo verde."
