#!/bin/bash
# build-cv-docs.sh - Convierte un CV en HTML a DOCX y PDF, 100% local.
#
# POR QUE EXISTE (2026-10-22). Los CVs se postulan en formato archivo: el ATS
# de los recrutadores (y los que los abren a mano) necesitan DOCX y PDF, no
# Markdown. El workspace no tiene pandoc, ni LibreOffice, ni python-docx. Los
# dos conversores que SI existen en macOS son:
#
#   - DOCX: textutil (html -> rtf -> docx). El paso por RTF es lo que conserva
#     el <b> (negritas de keywords). El camino directo html -> docx de
#     textutil PIERDE la negrita (verificado: 0 tags <w:b/> vs 3 con el
#     paso por RTF). Por eso el script no hace html -> docx directo.
#   - PDF: chrome-headless-shell de Playwright (ya instalado en
#     ~/Library/Caches/ms-playwright). cupsfilter y textutil NO sirven: con
#     html y con rtf producen un PDF de 0 bytes.
#
# Uso:
#   build-cv-docs.sh <cv.html> <salida-base>   # produce <base>.docx y <base>.pdf
#
# Salida: 0 si genero ambos, 1 si fallo.

set -uo pipefail

HTML="${1:-}"
BASE="${2:-}"

if [ -z "$HTML" ] || [ -z "$BASE" ]; then
  echo "Uso: build-cv-docs.sh <cv.html> <salida-base>" >&2
  exit 1
fi

if [ ! -f "$HTML" ]; then
  echo "No existe el HTML fuente: $HTML" >&2
  exit 1
fi

# --- Localizadores (con fallbacks) -----------------------------------------

find_chrome() {
  local candidates=(
    "$HOME/Library/Caches/ms-playwright/chromium_headless_shell-"*/chrome-headless-shell-mac-arm64/chrome-headless-shell
    "$HOME/Library/Caches/ms-playwright/chromium-"*/chrome-mac/Chromium.app/Contents/MacOS/Chromium
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
  )
  local c
  for c in "${candidates[@]}"; do
    if [ -x "$c" ]; then
      echo "$c"
      return 0
    fi
  done
  return 1
}

CHROME="$(find_chrome)" || {
  echo "No se encontro un Chromium/Chrome headless para el PDF." >&2
  echo "Instalalo con: npx playwright install chromium" >&2
  exit 1
}

command -v textutil >/dev/null 2>&1 || {
  echo "textutil no disponible (es parte de macOS, deberia estar)." >&2
  exit 1
}

TMP_RTF="$(mktemp -t cvcv).rtf"
trap 'rm -f "$TMP_RTF"' EXIT

# --- DOCX: html -> rtf -> docx (preserva negrita) ---------------------------

if ! textutil -convert rtf -output "$TMP_RTF" "$HTML" 2>/dev/null; then
  echo "Fallo textutil html -> rtf" >&2
  exit 1
fi

if ! textutil -convert docx -output "${BASE}.docx" "$TMP_RTF" 2>/dev/null; then
  echo "Fallo textutil rtf -> docx" >&2
  exit 1
fi

# --- PDF: headless chrome ---------------------------------------------------

if ! "$CHROME" --headless --disable-gpu --no-sandbox \
  --print-to-pdf="${BASE}.pdf" --no-pdf-header-footer \
  "file://$(cd "$(dirname "$HTML")" && pwd)/$(basename "$HTML")" >/dev/null 2>&1; then
  echo "Fallo la impresion a PDF con headless chrome" >&2
  exit 1
fi

# --- Verificacion (no confiar en el exit code) ------------------------------

fail=0

for f in "${BASE}.docx" "${BASE}.pdf"; do
  if [ ! -s "$f" ]; then
    echo "VACIO o inexistente: $f" >&2
    fail=1
  fi
done

if [ -s "${BASE}.docx" ]; then
  if ! unzip -p "${BASE}.docx" word/document.xml 2>/dev/null | grep -q "<w:body"; then
    echo "El DOCX no parece un OOXML valido: ${BASE}.docx" >&2
    fail=1
  fi
fi

if [ -s "${BASE}.pdf" ]; then
  if ! head -c 5 "${BASE}.pdf" | grep -q "%PDF"; then
    echo "El PDF no tiene cabecera %PDF: ${BASE}.pdf" >&2
    fail=1
  fi
fi

if [ "$fail" -ne 0 ]; then
  exit 1
fi

# Paginas del PDF (para el reporte)
PAGES="$(strings "${BASE}.pdf" | grep -c "/Type /Page$" 2>/dev/null || echo "?")"

echo "OK  ${BASE}.docx  ($(wc -c <"${BASE}.docx" | tr -d ' ') bytes)"
echo "OK  ${BASE}.pdf   ($(wc -c <"${BASE}.pdf" | tr -d ' ') bytes, ~${PAGES} paginas)"
