#!/usr/bin/env bash
#
# validate-spec.sh - delega en el validador de la skill spec-driven-development.
#
# Por que delega en vez de tener su propia copia (decision 2026-10-05):
# esta version chequeaba forma, no sustancia. Daba exit 0 sobre una spec con el
# Brief vacio, sin Status y con placeholders de plantilla sin completar. La
# version de la skill detecta los tres.
#
# Dos validadores con criterios distintos es peor que uno malo: el mismo archivo
# pasa en uno y falla en el otro, y no se sabe a cual creer. Una sola fuente.
#
# La version anterior quedo en validate-spec.sh.bak-share-20261005.
#
# Uso: bash validate-spec.sh [directorio]     (default: ./specs)
#
# Nota: la rutina que antes exigia CWD=$HOME ya no aplica; el directorio es un
# argumento y el default es relativo al CWD.

set -euo pipefail

SHARED_VALIDATOR="$HOME/.agents/skills/spec-driven-development/scripts/validate-spec.sh"

if [ ! -f "$SHARED_VALIDATOR" ]; then
  echo "::error ::No se encontro el validador compartido en $SHARED_VALIDATOR" >&2
  echo "  La skill spec-driven-development es la fuente unica. Instalala o revisa la ruta." >&2
  exit 2
fi

exec bash "$SHARED_VALIDATOR" "$@"
