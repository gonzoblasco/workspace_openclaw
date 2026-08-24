#!/bin/bash
# pdf-tool.sh - Local PDF/OCR toolkit for extracting text, metadata, and OCR.
#
# Wraps poppler (pdftotext/pdfinfo/pdftoppm) + tesseract (OCR) for common
# PDF operations. 100% local, no cloud services. Ported concept from the
# PDF/OCR plugin family (ClawHub: media + tools categories).
#
# Usage:
#   pdf-tool.sh info <pdf>              # metadata (pages, size, title)
#   pdf-tool.sh text <pdf>              # extract text (pdftotext)
#   pdf-tool.sh ocr <pdf>               # OCR a scanned/textless PDF
#   pdf-tool.sh pages <pdf> <n>         # extract text of page N (1-based)
#   pdf-tool.sh search <pdf> <term>     # grep text for a term
#   pdf-tool.sh pdf2img <pdf> [outdir]  # render pages to PNG (for OCR/QA)
#   pdf-tool.sh check                   # verify tools are installed
#
# Exit: 0 ok, 1 no tool/error.

set -uo pipefail

check_tools() {
  local missing=()
  for t in pdftotext pdfinfo pdftoppm tesseract; do
    command -v $t >/dev/null 2>&1 || missing+=("$t")
  done
  if [ "${#missing[@]}" -gt 0 ]; then
    echo "Faltan herramientas: ${missing[*]}. Instala con: brew install poppler tesseract" >&2
    return 1
  fi
  return 0
}

CMD="${1:-}"
[ -z "$CMD" ] && { echo "Usage: pdf-tool.sh {check|info|text|ocr|pages|search|pdf2img} [args]" >&2; exit 1; }

case "$CMD" in
  check)
    check_tools && echo "Herramientas PDF/OCR OK" || exit 1
    ;;

  info)
    check_tools || exit 1
    PDF="${2:-}"; [ -z "$PDF" ] && { echo "info requires <pdf>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    pdfinfo "$PDF"
    ;;

  text)
    check_tools || exit 1
    PDF="${2:-}"; [ -z "$PDF" ] && { echo "text requires <pdf>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    pdftotext "$PDF" - 2>/dev/null | sed '/^[[:space:]]*$/d'
    ;;

  pages)
    check_tools || exit 1
    PDF="${2:-}"; PAGE="${3:-1}"
    [ -z "$PDF" ] && { echo "pages requires <pdf> <n>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    pdftotext -f "$PAGE" -l "$PAGE" "$PDF" - 2>/dev/null | sed '/^[[:space:]]*$/d'
    ;;

  ocr)
    check_tools || exit 1
    PDF="${2:-}"; [ -z "$PDF" ] && { echo "ocr requires <pdf>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    TMP=$(mktemp -d)
    # render pages to PNG at 150 DPI, then OCR each
    pdftoppm -r 150 -png "$PDF" "$TMP/page" 2>/dev/null
    for img in "$TMP"/page-*.png; do
      [ -f "$img" ] || continue
      echo "--- $(basename "$img" .png) ---"
      tesseract "$img" - 2>/dev/null
    done
    rm -rf "$TMP"
    ;;

  search)
    check_tools || exit 1
    PDF="${2:-}"; TERM="${3:-}"
    [ -z "$PDF" ] || [ -z "$TERM" ] && { echo "search requires <pdf> <term>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    pdftotext "$PDF" - 2>/dev/null | grep -i -n -A1 -B1 -- "$TERM" || echo "(termino no encontrado)"
    ;;

  pdfimages|pdf2img)
    check_tools || exit 1
    PDF="${2:-}"; OUT="${3:-pdf_images}"
    [ -z "$PDF" ] && { echo "pdfimages requires <pdf> [outdir]" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    mkdir -p "$OUT"
    pdftoppm -r 150 -png "$PDF" "$OUT/page"
    echo "Imagenes renderizadas en $OUT/ (paginas -> page-*.png)"
    ;;

  *)
    echo "usage: pdf-tool.sh {check|info|text|ocr|pages|search|pdfimages} [args]" >&2
    exit 1
    ;;
esac
