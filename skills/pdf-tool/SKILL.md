---
name: pdf-tool
metadata:
  category: "Tools"
  tags:
    - pdf
    - ocr
    - documentos
    - markdown
description: "Manejo local de PDFs: leer (extraer texto, metadata, OCR) y generar (exportar markdown a PDF). Usa poppler + tesseract para lectura y md-to-pdf para exportar MD. 100% local sin servicios cloud. Portado de la familia PDF/OCR de ClawHub."
user-invocable: false
---

# PDF Tool

Procesar PDFs localmente: extraer texto, OCR de documentos escaneados, y **exportar markdown a PDF**. Portado del concepto de la familia PDF/OCR (ClawHub: media + tools). 100% local, sin mandar documentos a la nube.

## Cuando usar

- Leer/extraer texto de specs, documentos, articulos en PDF.
- OCR de documentos escaneados (sin texto nativo) o imagenes con texto.
- Obtener metadata de un PDF (paginas, tamaño).
- Buscar un termino dentro de un PDF.
- **Exportar los MDs que generamos (dailies, HANDOFF, README) a PDF.**

## Como usarlo

```bash
./scripts/pdf-tool.sh check                    # verificar herramientas instaladas
./scripts/pdf-tool.sh info <pdf>               # metadata (paginas, tam, titulo)
./scripts/pdf-tool.sh text <pdf>                # extraer todo el texto
./scripts/pdf-tool.sh pages <pdf> <n>           # texto de la pagina N
./scripts/pdf-tool.sh search <pdf> <termino>    # buscar un termino
./scripts/pdf-tool.sh ocr <pdf>                 # OCR de un PDF escaneado
./scripts/pdf-tool.sh pdfimages <pdf> [out]     # renderizar paginas a PNG
./scripts/pdf-tool.sh md2pdf <md> [out.pdf]     # EXPORTAR markdown a PDF
```

## Interpretar resultados

- **`text`**: texto plano extraido (mejor para PDFs con texto nativo).
- **`ocr`**: para PDFs escaneados (imagenes). Tesseract reconoce el texto. Mas lento, menos exacto.
- **`md2pdf`**: convierte un archivo .md a .pdf (mismo nombre por default, o especifica el output). Bueno para tablas, code blocks y headers - usa md-to-pdf (Puppeteer/Chromium en el fondo).

## Exportar MD a PDF (md2pdf)

Para exportar los markdowns del workspace (daily, HANDOFF, README, docs) a PDF:

```bash
./scripts/pdf-tool.sh md2pdf memory/2026-08-24.md /tmp/daily.pdf
./scripts/pdf-tool.sh md2pdf HANDOFF.md                 # -> HANDOFF.pdf (default)
```

- El output por default es el mismo nombre con .pdf.
- Genera PDF con estilos decentes (headers, tablas, code blocks resaltados).
- Usa npx md-to-pdf (descarga Puppeteer la primera vez, luego cacheado).

## Requisitos

- **poppler**: `brew install poppler` (pdftotext, pdfinfo, pdftoppm) - lectura.
- **tesseract**: `brew install tesseract` (OCR).
- **node/npx**: para md2pdf (npm). Puppeteer se descarga la primera vez.

## Reglas

- **100% local** - los documentos nunca se envian a servicios externos.
- Para documentos grandes, extraer texto y leer por partes (pages).
- Para PDFs escaneados, usar `ocr`.

## Limites

- El OCR no es perfecto (depende de la resolucion).
- md2pdf requiere node/npx (descarga Chromium la primera vez, ~170MB).

## Related

- [Technical Docs](../tech-docs): documentacion tecnica (puede incluir PDFs).
- [Knowledge Management](../knowledge-management): consolidar lo extraido de PDFs a la memoria.
