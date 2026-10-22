#!/usr/bin/env python3
"""
cv-md-to-html.py - Convierte un CV en Markdown a HTML con estilos de CV.

POR QUE EXISTE (2026-10-22). El flujo de postulacion termina en un archivo
(DOCX + PDF) que un ATS y un recruiter abren. El workspace tiene el HTML
final de cada CV (el de Staffy, con sus estilos) pero no tiene el conversor
de Markdown a ese HTML: cada CV nuevo obligaba a reescribir el HTML a mano,
que es donde aparecen las divergencias de formato entre postulaciones.

Este script toma el Markdown que escribe el subagente y produce el HTML con
los MISMOS estilos que el CV de referencia, para que todos los CVs del
workspace se vean iguales (una sola version de la verdad, tambien en el
formato).

REGLAS:
  - Single columna, sin tablas de layout (ATS).
  - El markdown puede traer tablas (el "Keyword map"). Se renderizan como
    tablas reales, que el ATS tolera si no son de layout.
  - Las secciones "## Notes / gaps" y "## Keyword map" NO son parte del CV
    que se manda: son el mapa de trabajo del proceso. El script las marca
    con un atributo `data-workdoc` para poder excluirlas al generar el
    archivo final.
    - `--include-workdoc` las deja (para revision interna y para el PDF de
      trabajo, que muestra los gaps al recruiter si Gonzo decide eso).
    - por defecto se EXCLUYEN del archivo que se posta: un CV de 3 paginas
      con un mapa de keywords al final es un CV de 2 paginas con las partes
      que importan. Verificado 2026-10-22: con las secciones de trabajo, los
      tres CVs daban 3 paginas; sin ellas, 2.

Uso:
    cv-md-to-html.py <cv.md> <salida.html> [--include-workdoc]
"""
import html
import re
import sys
from pathlib import Path

STYLE = """  body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 10pt; color: #1a1a1a; line-height: 1.28; margin: 0; }
  h1 { font-size: 19pt; margin: 0 0 2pt 0; letter-spacing: 0.5pt; }
  .role { font-size: 10.5pt; color: #333; margin: 0 0 5pt 0; font-weight: 600; }
  .contact { font-size: 8.5pt; color: #444; margin: 0 0 11pt 0; }
  h2 { font-size: 10pt; text-transform: uppercase; letter-spacing: 1pt; border-bottom: 1.2pt solid #1a1a1a; padding-bottom: 2pt; margin: 11pt 0 6pt 0; }
  h3 { font-size: 10pt; margin: 8pt 0 1pt 0; }
  .meta { font-size: 8.5pt; color: #555; font-style: italic; margin: 0 0 4pt 0; }
  ul { margin: 2pt 0 2pt 0; padding-left: 14pt; }
  li { margin-bottom: 2.5pt; }
  p { margin: 0 0 6pt 0; }
  .skills p { margin: 0 0 4pt 0; }
  .label { font-weight: 700; }
  table { border-collapse: collapse; width: 100%; margin: 4pt 0 8pt 0; font-size: 9pt; }
  th { text-align: left; border-bottom: 1pt solid #1a1a1a; padding: 2pt 4pt 2pt 0; }
  td { border-bottom: 0.5pt solid #ddd; padding: 2pt 4pt 2pt 0; vertical-align: top; }
  /* Las URLs y el email NO se parten: si el guion bajo cae al final de linea,
     el extractor de texto del ATS lo come y "linkedin.com/in/gonzalo-blasco"
     se lee "linkedin.com/in/gonzaloblasco" - un contacto roto en el archivo
     que el sistema lee, no en el que el humano ve. Verificado 2026-10-22 con
     pdftotext: la URL se partia y el guion desaparecia. */
  .nb { white-space: nowrap; }
"""


def inline(text: str) -> str:
    """Markdown inline -> HTML. Solo lo que los CVs usan."""
    text = html.escape(text)
    # **bold** y *italic*
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*([^*]+?)\*(?![\w*])", r"<i>\1</i>", text)
    # `code`
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


# Secciones de trabajo (mapa del proceso, no parte del CV que se manda).
# Incluyen las versiones en espanol: el CV de Mercado Pago esta en espanol,
# y sin esto sus secciones "Notas / vacios" y "Mapa de keywords" se colaban
# en el archivo final (3 paginas en vez de 2). Verificado 2026-10-22.
WORKDOC_SECTIONS = (
    "notes / gaps",
    "notes",
    "gaps",
    "keyword map",
    "keywords map",
    "notas / vacios",
    "notas / vacíos",
    "notas",
    "vacios",
    "vacíos",
    "mapa de keywords",
    "mapa de keywords",
)


def convert(md: str, include_workdoc: bool = False) -> str:
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)
    skip_until_next_h2 = False
    while i < n:
        line = lines[i]

        # Tabla markdown
        if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            if skip_until_next_h2:
                i += 2
                while i < n and lines[i].strip().startswith("|"):
                    i += 1
                continue
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append("<table>")
            out.append("<tr>" + "".join(f"<th>{inline(h)}</th>" for h in headers) + "</tr>")
            for r in rows:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</table>")
            continue

        # H1: nombre
        if line.startswith("# "):
            out.append(f"<h1>{inline(line[2:].strip())}</h1>")
            i += 1
            continue

        # H2: seccion
        if line.startswith("## "):
            title = line[3:].strip()
            low = title.lower().strip()
            is_workdoc = any(low == w or low.startswith(w) for w in WORKDOC_SECTIONS)
            if is_workdoc and not include_workdoc:
                skip_until_next_h2 = True
                i += 1
                continue
            skip_until_next_h2 = False
            out.append(f"<h2>{inline(title)}</h2>")
            i += 1
            continue

        if skip_until_next_h2:
            i += 1
            continue

        # H3: rol
        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:].strip())}</h3>")
            i += 1
            continue

        # Lista
        if line.strip().startswith("- "):
            items = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(inline(lines[i].strip()[2:].strip()))
                i += 1
            out.append("<ul>")
            for it in items:
                out.append(f"<li>{it}</li>")
            out.append("</ul>")
            continue

        # Parrafo (linea siguiente al H1: subtitulo de rol)
        if line.strip():
            out.append(f"<p>{inline(line.strip())}</p>")
        i += 1

    body = "\n".join(out)
    # La linea de contacto va con su clase propia.
    body = re.sub(
        r"<p>(Núñez[^<]*)</p>",
        r'<p class="contact">\1</p>',
        body,
    )
    # URLs y email en la linea de contacto: no se parten. Un ATS que extrae
    # texto come el guion bajo si cae al final de linea, y el LinkedIn queda
    # roto. Verificado 2026-10-22.
    body = re.sub(
        r"(\S+@\S+\.com|linkedin\.com/\S+|github\.com/\S+)",
        r'<span class="nb">\1</span>',
        body,
    )
    # La primera linea despues del h1 es el titulo del puesto.
    body = re.sub(
        r'(<h1>[^<]*</h1>\s*)<p>(.*?)</p>',
        r'\1<p class="role">\2</p>',
        body,
        count=1,
    )
    # Las lineas en italic que siguen a un h3 son metadatos de rol.
    body = re.sub(
        r"(<h3>[^<]*</h3>\s*)<p>(\*.*?\*)</p>",
        r'\1<p class="meta">\2</p>',
        body,
    )
    return body


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    include_workdoc = "--include-workdoc" in sys.argv
    if len(args) < 2:
        print("Uso: cv-md-to-html.py <cv.md> <salida.html> [--include-workdoc]", file=sys.stderr)
        return 1
    src = Path(args[0])
    dst = Path(args[1])
    md = src.read_text(encoding="utf-8")
    body = convert(md, include_workdoc=include_workdoc)
    doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{STYLE}</style>
</head>
<body>

{body}

</body>
</html>
"""
    dst.write_text(doc, encoding="utf-8")
    print(f"OK  {dst}  ({len(doc)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
