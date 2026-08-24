#!/bin/bash
# pdf-tool.sh - Local PDF/OCR toolkit: read, extract, OCR, and generate PDFs.
#
# Reading/extraction: poppler (pdftotext/pdfinfo/pdftoppm) + tesseract (OCR).
# Generation (markdown -> PDF): md-to-pdf (npm/Puppeteer).
# 100% local, no cloud services. Ported concept from the PDF/OCR plugin
# family (ClawHub: media + tools categories).
#
# Usage:
#   pdf-tool.sh check                    # verify installed tools
#   pdf-tool.sh info <pdf>               # metadata (pages, size, title)
#   pdf-tool.sh text <pdf>               # extract text (pdftotext)
#   pdf-tool.sh pages <pdf> <n>          # extract text of page N (1-based)
#   pdf-tool.sh search <pdf> <term>      # grep text for a term
#   pdf-tool.sh ocr <pdf>                # OCR a scanned/textless PDF
#   pdf-tool.sh pdfimages <pdf> [outdir] # render pages to PNG (for OCR/QA)
#   pdf-tool.sh md2pdf <md> [out.pdf]    # convert Markdown to PDF (md-to-pdf)
#
# Exit: 0 ok, 1 no tool/error.

set -uo pipefail

check_read_tools() {
  local missing=()
  for t in pdftotext pdfinfo pdftoppm tesseract; do
    command -v $t >/dev/null 2>&1 || missing+=("$t")
  done
  if [ "${#missing[@]}" -gt 0 ]; then
    echo "Faltan herramientas de lectura PDF: ${missing[*]}. Instala: brew install poppler tesseract" >&2
    return 1
  fi
  return 0
}

CMD="${1:-}"
[ -z "$CMD" ] && { echo "Usage: pdf-tool.sh {check|info|text|pages|search|ocr|pdfimages|md2pdf} [args]" >&2; exit 1; }

case "$CMD" in
  check)
    local_ok=0; read_ok=0
    command -v npx >/dev/null 2>&1 && local_ok=1
    check_read_tools && read_ok=1 || read_ok=0
    echo "Lectura/OCR (poppler+tesseract): $([ $read_ok = 1 ] && echo OK || echo FALTAN)"
    echo "Generacion MD->PDF (npx md-to-pdf): $([ $local_ok = 1 ] && echo OK || echo 'NO (npm/npx)')"
    [ $read_ok = 1 ] || exit 1
    ;;

  info)
    check_read_tools || exit 1
    PDF="${2:-}"; [ -z "$PDF" ] && { echo "info requires <pdf>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    pdfinfo "$PDF"
    ;;

  text)
    check_read_tools || exit 1
    PDF="${2:-}"; [ -z "$PDF" ] && { echo "text requires <pdf>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    pdftotext "$PDF" - 2>/dev/null | sed '/^[[:space:]]*$/d'
    ;;

  pages)
    check_read_tools || exit 1
    PDF="${2:-}"; PAGE="${3:-1}"
    [ -z "$PDF" ] && { echo "pages requires <pdf> <n>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    pdftotext -f "$PAGE" -l "$PAGE" "$PDF" - 2>/dev/null | sed '/^[[:space:]]*$/d'
    ;;

  ocr)
    check_read_tools || exit 1
    PDF="${2:-}"; [ -z "$PDF" ] && { echo "ocr requires <pdf>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    TMP=$(mktemp -d)
    pdftoppm -r 150 -png "$PDF" "$TMP/page" 2>/dev/null
    for img in "$TMP"/page-*.png; do
      [ -f "$img" ] || continue
      echo "--- $(basename "$img" .png) ---"
      tesseract "$img" - 2>/dev/null
    done
    rm -rf "$TMP"
    ;;

  search)
    check_read_tools || exit 1
    PDF="${2:-}"; TERM="${3:-}"
    [ -z "$PDF" ] || [ -z "$TERM" ] && { echo "search requires <pdf> <term>" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    pdftotext "$PDF" - 2>/dev/null | grep -i -n -A1 -B1 -- "$TERM" || echo "(termino no encontrado)"
    ;;

  pdfimages|pdf2img)
    check_read_tools || exit 1
    PDF="${2:-}"; OUT="${3:-pdf_images}"
    [ -z "$PDF" ] && { echo "pdfimages requires <pdf> [outdir]" >&2; exit 1; }
    [ -f "$PDF" ] || { echo "No existe: $PDF" >&2; exit 1; }
    mkdir -p "$OUT"
    pdftoppm -r 150 -png "$PDF" "$OUT/page"
    echo "Imagenes renderizadas en $OUT/ (paginas -> page-*.png)"
    ;;

  md2pdf)
    # Markdown -> PDF via md-to-pdf (npx/Puppeteer). Good for code/tables.
    # md-to-pdf generates <name>.pdf next to the source; we copy to a temp
    # dir and move the result to the requested output path.
    command -v npx >/dev/null 2>&1 || { echo "npx no encontrado (instala node)" >&2; exit 1; }
    MD="${2:-}"; [ -z "$MD" ] && { echo "md2pdf requires <md> [out.pdf]" >&2; exit 1; }
    [ -f "$MD" ] || { echo "No existe: $MD" >&2; exit 1; }
    OUT="${3:-${MD%.md}.pdf}"
    TMP=$(mktemp -d)
    cp "$MD" "$TMP/input.md"
    ( cd "$TMP" && npx --yes md-to-pdf input.md 2>&1 | tail -2 )
    if [ -f "$TMP/input.pdf" ]; then
      cp "$TMP/input.pdf" "$OUT"
      echo "PDF generado: $OUT"
    else
      echo "Error: no se genero el PDF." >&2
      exit 1
    fi
    rm -rf "$TMP"
    ;;

  *)
    echo "usage: pdf-tool.sh {check|info|text|pages|ocr|search|pdfimages|md2pdf} [args]" >&2
    exit 1
    ;;
esac
