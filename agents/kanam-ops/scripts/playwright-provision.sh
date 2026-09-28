#!/usr/bin/env bash
#
# playwright-provision.sh - Provisiona un browser de Playwright cuando el
# instalador oficial se cuelga al extraer o deja el build incompleto.
#
# Por que existe: `playwright install <engine>` puede quedarse colgado al
# descomprimir (sin output por minutos) o dejar el directorio a medio armar
# (solo algunas dylibs). Ademas, un build completo en disco pero SIN los
# markers es borrado por el siguiente `playwright install` de cualquier
# engine. Verificado 2026-09-24 en adobe/react-spectrum #10517: webkit-2227
# quedo con solo libwebrtc.dylib y fue borrado por un install de firefox.
#
# El flujo que funciona: sacar la URL con --dry-run, bajar el zip con curl,
# descomprimir en el install location y crear AMBOS markers.
#
# Uso:
#   ./playwright-provision.sh <engine> [--repo <dir>] [--force] [--keep-zip]
#
#   <engine>      chromium | chromium-headless-shell | firefox | webkit
#   --repo <dir>  Directorio con node_modules/ (donde corre playwright).
#                 Default: el directorio actual.
#   --force       Reinstalar aunque el build ya este completo.
#   --keep-zip    No borrar el zip temporal al terminar (debug).
#
# Variables:
#   PLAYWRIGHT_BROWSERS_PATH  Respeta el cache alternativo de Playwright.
#
# Salida: 0 si el build quedo completo y el binario responde.

set -euo pipefail

ENGINE=""
REPO="$PWD"
FORCE=0
KEEP_ZIP=0

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
info() { printf '  %s\n' "$*"; }
step() { printf '\n== %s\n' "$*"; }

usage() {
  sed -n '2,29p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="${2:?--repo necesita un directorio}"; shift 2 ;;
    --force) FORCE=1; shift ;;
    --keep-zip) KEEP_ZIP=1; shift ;;
    -h|--help) usage 0 ;;
    chromium|chromium-headless-shell|firefox|webkit) ENGINE="$1"; shift ;;
    *) die "argumento desconocido: $1 (ver --help)" ;;
  esac
done

[ -n "$ENGINE" ] || usage 1
[ -d "$REPO" ] || die "no existe el directorio --repo: $REPO"
REPO="$(cd "$REPO" && pwd)"

# --- localizar el binario de playwright del repo ---------------------------
step "Localizando playwright en $REPO"
if [ -x "$REPO/node_modules/.bin/playwright" ]; then
  PW=("$REPO/node_modules/.bin/playwright")
elif [ -f "$REPO/node_modules/playwright/package.json" ]; then
  PW=("node" "$REPO/node_modules/playwright/cli.js")
else
  info "sin playwright local; uso npx"
  PW=("npx" "--yes" "playwright")
fi
info "usando: ${PW[*]}"

# --- detectar cache ---------------------------------------------------------
if [ -n "${PLAYWRIGHT_BROWSERS_PATH:-}" ]; then
  CACHE="$PLAYWRIGHT_BROWSERS_PATH"
else
  case "$(uname -s)" in
    Darwin) CACHE="$HOME/Library/Caches/ms-playwright" ;;
    Linux)  CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/ms-playwright" ;;
    *)      die "SO no soportado: $(uname -s)" ;;
  esac
fi
info "cache: $CACHE"

# --- dry-run: URL de descarga + install location ----------------------------
step "Consultando el manifiesto ($ENGINE)"
DRY="$(cd "$REPO" && "${PW[@]}" install "$ENGINE" --dry-run 2>&1)" \
  || die "playwright install --dry-run fallo:
$DRY"

URL="$(printf '%s\n' "$DRY" | sed -n 's/^[[:space:]]*Download url:[[:space:]]*//p' | head -1)"
LOC="$(printf '%s\n' "$DRY" | sed -n 's/^[[:space:]]*Install location:[[:space:]]*//p' | head -1)"
[ -n "$URL" ] || die "no pude parsear la Download url del dry-run:
$DRY"
[ -n "$LOC" ] || die "no pude parsear el Install location del dry-run:
$DRY"
info "url:  $URL"
info "dest: $LOC"

# --- el binario esperado, por engine ---------------------------------------
binary_path() {
  case "$1" in
    webkit) printf '%s/pw_run.sh' "$LOC" ;;
    firefox)
      # el layout cambia entre versiones; busco el ejecutable real
      find "$LOC" -type f -path '*MacOS/firefox' -o -type f -name 'firefox' 2>/dev/null | head -1 ;;
    chromium)
      find "$LOC" -type f \( -name 'Chromium' -o -name 'Google Chrome for Testing' \
        -o -name 'chrome' \) 2>/dev/null | head -1 ;;
    chromium-headless-shell)
      find "$LOC" -type f -name 'chrome-headless-shell' 2>/dev/null | head -1 ;;
  esac
}

is_complete() {
  [ -f "$LOC/INSTALLATION_COMPLETE" ] || return 1
  [ -f "$LOC/DEPENDENCIES_VALIDATED" ] || return 1
  local bin; bin="$(binary_path "$ENGINE")"
  [ -n "$bin" ] && [ -f "$bin" ]
}

# --- caso ya completo -------------------------------------------------------
step "Estado del build"
if is_complete && [ "$FORCE" -eq 0 ]; then
  info "ya esta completo ($LOC)"
  info "binario: $(binary_path "$ENGINE")"
  info "nada que hacer (usar --force para reinstalar)"
  exit 0
fi

if [ -d "$LOC" ]; then
  if is_complete; then
    info "reinstalando por --force"
  else
    info "build incompleto en disco; lo reemplazo"
  fi
  # trash sobre rm: es cache regenerable, pero preferimos el camino reversible
  if command -v trash >/dev/null 2>&1; then
    trash "$LOC" || die "no pude mover a trash: $LOC"
  else
    rm -rf "$LOC"
  fi
fi

# --- descarga + extraccion --------------------------------------------------
step "Descargando"
mkdir -p "$LOC" "$CACHE"
ZIP="$(mktemp "${TMPDIR:-/tmp}/pw-${ENGINE}-XXXXXX.zip")"
cleanup() { [ "$KEEP_ZIP" -eq 1 ] || rm -f "$ZIP"; }
trap cleanup EXIT

if ! curl -fsSL --retry 3 --retry-delay 2 -o "$ZIP" "$URL"; then
  die "la descarga fallo. Si el CDN responde un body corto (GatewayExceptionResponse), esta bloqueado para esta red: no reintentar."
fi
SIZE="$(wc -c < "$ZIP" | tr -d ' ')"
info "bajado: $SIZE bytes"
# un zip real de browser pesa decenas de MB; un body de error, unos pocos bytes
[ "$SIZE" -gt 1048576 ] || die "el zip pesa $SIZE bytes, demasiado poco: no es un browser (CDN bloqueado?)"

step "Extrayendo"
unzip -qo "$ZIP" -d "$LOC" || die "unzip fallo"

# --- markers ANTES de verificar --------------------------------------------
# Sin los markers, el siguiente `playwright install` de cualquier engine
# considera el build incompleto y lo BORRA.
touch "$LOC/INSTALLATION_COMPLETE" "$LOC/DEPENDENCIES_VALIDATED"

# --- verificacion -----------------------------------------------------------
step "Verificando"
BIN="$(binary_path "$ENGINE")"
[ -n "$BIN" ] && [ -f "$BIN" ] || die "el binario esperado no existe tras extraer: $LOC
Contenido: $(ls "$LOC" | head -5 | tr '\n' ' ')"
[ -x "$BIN" ] || chmod +x "$BIN" 2>/dev/null || true
info "binario: $BIN"

# los markers tienen que estar los dos
for m in INSTALLATION_COMPLETE DEPENDENCIES_VALIDATED; do
  [ -f "$LOC/$m" ] || die "falta el marker $m en $LOC"
done
info "markers: OK"

printf '\nLISTO: %s completo en %s\n' "$ENGINE" "$LOC"
