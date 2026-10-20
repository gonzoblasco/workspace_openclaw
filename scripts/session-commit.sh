#!/usr/bin/env bash
# session-commit.sh - Commitea SOLO las rutas que le nombras.
#
# Por que existe (2026-10-19): `git commit` sin pathspec commitea el indice
# ENTERO, incluido lo que otra sesion dejo staged. Paso el 2026-10-18: 13
# archivos de un cierre quedaron staged y otra sesion se los llevo en su commit
# de ADRs, sin aviso y sin conflicto. El indice es estado global del repo; el
# pathspec es lo unico que lo aisla por commit.
#
# Uso:
#   ./scripts/session-commit.sh -m "tipo: mensaje" -- archivo1 archivo2 ...
#
# El `--` es obligatorio: separa el mensaje de las rutas y evita que una ruta
# que empieza con `-` se lea como flag.
#
# Hace `git add` y `git commit` con las MISMAS rutas: el add registra archivos
# nuevos (el pathspec de commit solo ve archivos trackeados), el commit toma
# solo esas rutas y deja el resto del indice como estaba.

set -euo pipefail

MSG=""
PATHS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -m|--message) MSG="$2"; shift 2 ;;
    --) shift; PATHS=("$@"); break ;;
    *) echo "session-commit: argumento inesperado: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$MSG" ]]; then
  echo "session-commit: falta -m \"mensaje\"" >&2; exit 2
fi
if [[ ${#PATHS[@]} -eq 0 ]]; then
  echo "session-commit: nombra las rutas despues de -- (commit sin pathspec no se permite)" >&2
  exit 2
fi

# El lock cubre add + commit: son dos pasos que no deben intercalarse con otro
# cierre. Si el lock no se consigue, sale 75 y no toca el indice.
exec ./scripts/with-lock.py .git/index -- bash -c '
  set -euo pipefail
  git --literal-pathspecs add -- "$@"
  git commit -m "$0" -- "$@"
' "$MSG" "${PATHS[@]}"
