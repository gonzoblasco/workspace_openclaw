#!/usr/bin/env bash
# Corre la practica completa del modulo 1 y devuelve un solo exit code.
# Uso: ./run.sh [--shot]
set -uo pipefail

GODOT="${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}"
cd "$(dirname "$0")" || exit 1

fail=0
run() {
  local label="$1"; shift
  echo "── $label"
  if "$@" 2>&1 | grep -E "OK|FAIL|BUILD_OK|LEVEL_OK|SHOT_OK|_FAIL|ERROR: " | grep -v "RID allocations\|leaked at exit\|still in use\|PagedAllocator\|ObjectDB"; then :; fi
  local rc=${PIPESTATUS[0]}
  if [[ $rc -ne 0 ]]; then
    echo "   ↳ exit $rc"
    fail=1
  fi
  echo
}

run "1/4 construir mesh library"  "$GODOT" --headless --path . --script build_mesh_library.gd
run "2/4 test mesh library"        "$GODOT" --headless --path . --script test_mesh_library.gd
run "3/4 construir level"          "$GODOT" --headless --path . --script build_level.gd
run "4/4 test level"               "$GODOT" --headless --path . --script test_level.gd

if [[ "${1:-}" == "--shot" ]]; then
  echo "── captura (ventana real)"
  "$GODOT" --path . --script shot.gd 2>&1 | grep SHOT_OK || fail=1
  echo
fi

if [[ $fail -eq 0 ]]; then
  echo "M1 PRACTICA OK"
else
  echo "M1 PRACTICA FAIL"
fi
exit $fail
