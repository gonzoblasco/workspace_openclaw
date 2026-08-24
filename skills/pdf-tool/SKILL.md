---
name: pdf-tool
metadata:
  category: "Tools"
  tags:
    - pdf
    - ocr
    - documentos
description: "Manejo local de PDFs y OCR: extraer texto, metadata, buscar en documentos, y OCR de PDFs escaneados o imagenes. Usa poppler (pdftotext/pdfinfo/pdftoppm) + tesseract, 100% local sin servicios cloud. Portado de la familia PDF/OCR de ClawHub."
user-invocable: false
---

# PDF Tool

Procesar PDFs localmente: extraer texto, metadata, OCR de documentos escaneados, y convertir a imagenes. Portado del concepto de la familia PDF/OCR (ClawHub: media + tools). 100% local, sin mandar documentos a la nube.

## Cuando usar

- Leer/extraer texto de specs, documentos, articulos en PDF.
- OCR de documentos escaneados (sin texto nativo) o imagenes con texto.
- Obtener metadata de un PDF (paginas, tamaño).
- Buscar un termino dentro de un PDF.
- Convertir paginas de PDF a imagenes (para QA visual, revisar).

## Como usarlo

```bash
./scripts/pdf-tool.sh check                    # verificar herramientas instaladas
./scripts/pdf-tool.sh info <pdf>               # metadata (paginas, tam, titulo)
./scripts/pdf-tool.sh text <pdf>               # extraer todo el texto
./scripts/pdf-tool.sh pages <pdf> <n>          # texto de la pagina N
./scripts/pdf-tool.sh search <pdf> <termino>   # buscar un termino
./scripts/pdf-tool.sh ocr <pdf>                # OCR de un PDF escaneado/sin texto
./scripts/pdf-tool.sh pdfimages <pdf> [out]    # renderizar paginas a PNG
```

## Interpretar resultados

- **`text`**: texto plano extraido (mejor para PDFs con texto nativo - son la mayoria de los digitales).
- **`ocr`**: para PDFs escaneados (imagenes, sin texto). Tesseract reconoce el texto de las imagenes. Mas lento y menos exacto que text, pero funciona donde text no da nada.
- **`info`**: cuantas paginas, tamano, titulo. Util para entender el documento antes de leerlo.
- **`search`**: ubica un termino en el texto (grep). Util para encontrar una seccion especifica.

## Requisitos

- **poppler**: `brew install poppler` (pdftotext, pdfinfo, pdftoppm).
- **tesseract**: `brew install tesseract` (OCR). Para mejor OCR en espanol: `brew install tesseract-lang`.

## Reglas

- **100% local** - los documentos nunca se envian a servicios externos. Respetamos la privacidad de specs, recibos y documentos sensibles.
- Para documentos grandes, extraer texto y leerlo por partes (pages) en vez de cargar todo.
- Para PDFs escaneados, usar `ocr` (tesseract) - es lo que da texto donde no lo hay.

## Limites

- El OCR de tesseract no es perfecto: calidad depende de la resolucion y claridad del escaneado. Textos manchados o fuentes raras pueden dar errores.
- No hace analisis semantico - solo extrae texto/OCR. El agente interpreta.

## Related

- [Technical Docs](../tech-docs): documentacion tecnica (puede incluir PDFs).
- [Knowledge Management](../knowledge-management): consolidar lo extraido de PDFs a la memoria.
