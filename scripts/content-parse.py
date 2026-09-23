#!/usr/bin/env python3
"""
content-parse.py - Extrae estructura del contenido markdown de memory.db.

Todo el contenido de la DB es markdown guardado en un solo campo de texto
(`daily_notes.content`, `sessions_relacional.content_bare`). Este modulo lo
descompone en campos consultables.

QUE EXTRAE (y con que fiabilidad, medido sobre 165 documentos):

  doc_kind        harness | daily. El prefijo "# Session:" distingue el dump
                  crudo del harness. 100% confiable (65/65).
  session_key     de los dumps del harness. 100% parseable (65/65).
  session_id      idem. 100% parseable (65/65).
  source          webchat | gateway:sessions.reset. 100% (65/65).
  sections        los headings ## y ###. 1255 secciones en 106 docs.
  checklist       los "- [ ]" y "- [x]" embebidos. 67 abiertos, 35 hechos.

QUE NO EXTRAE, a proposito:

  Entidades (repos, PRs) del texto libre. Medido: de 5143 matches de
  `owner/name`, la mayoria son rutas de archivo (`dist/stacks`,
  `memory/archive`) y fechas (`28/08`). Extraer eso con regex fabrica datos
  falsos. Las referencias estructuradas van en `contributions`, donde el
  dato es regular, no inferido.

Uso:
    from content_parse import doc_kind, harness_fields, split_sections, extract_checklist
"""
import re

H_ANY = re.compile(r"^(#{1,6})\s+(.*)$")
# "(08:00 - 10:35)" o "(08:00-10:35)" al final del titulo.
TIME_RANGE = re.compile(r"\(\s*(\d{1,2}:\d{2})\s*[-\u2013]\s*(\d{1,2}:\d{2})\s*\)\s*$")
CHECKBOX = re.compile(r"^\s*-\s*\[([ xX])\]\s*(.+?)\s*$")

HARNESS_FIELDS = {
    "session_key": re.compile(r"^- \*\*Session Key\*\*:\s*(\S+)", re.M),
    "session_id": re.compile(r"^- \*\*Session ID\*\*:\s*(\S+)", re.M),
    "source": re.compile(r"^- \*\*Source\*\*:\s*(\S+)", re.M),
}


def doc_kind(text: str) -> str:
    """'harness' para el dump crudo del harness, 'daily' para todo lo demas.

    No se intenta distinguir el daily narrativo del resume de cierre: los dos
    son el mismo tipo de documento (el archivo memory/YYYY-MM-DD.md) y la
    distincion fina va en las secciones, no en el tipo.
    """
    if not text:
        return "daily"
    return "harness" if text.lstrip().startswith("# Session:") else "daily"


def harness_fields(text: str) -> dict:
    """Metadatos del dump del harness. Campos ausentes -> None."""
    out = {"session_key": None, "session_id": None, "source": None}
    if doc_kind(text) != "harness":
        return out
    for field, pat in HARNESS_FIELDS.items():
        m = pat.search(text)
        if m:
            out[field] = m.group(1)
    return out


def _time_range(title: str):
    """(start, end) del rango horario al final del titulo, o (None, None)."""
    m = TIME_RANGE.search(title)
    if not m:
        return None, None
    return m.group(1), m.group(2)


# Marcador de scoping por proyecto: `<!-- project: owner/repo -->`.
# Es metadata para busquedas (regla del workspace), no parte del titulo humano.
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


def clean_title(title: str) -> str:
    """Titulo legible: sin rango horario y sin comentarios HTML.

    El comentario de proyecto se filtra de los titulos porque se VEIA crudo en
    la UI: 'Engram - adopcion completa <!-- project: github.com/... -->'. La
    metadata sigue en el texto del documento; solo no ensucia el encabezado.
    """
    return TIME_RANGE.sub("", HTML_COMMENT.sub("", title)).strip()


def _strip_time_range(title: str) -> str:
    """Compatibilidad: el nombre queda, la logica vive en clean_title."""
    return clean_title(title)


def split_sections(text: str):
    """Divide el markdown en secciones por headings ## y ###.

    Devuelve dicts con level, title, time_start, time_end y **char_start/**
    **char_end**: offsets hacia el `content` del documento padre.

    Por que offsets y no una copia del body: medido, copiar el body duplicaba
    1948 KB (el 95% del texto, que ya vive en el padre). Es el mismo defecto
    que la tabla gemela de ADR-058. Con offsets, `sections` pesa ~78 KB.

    La reconstruccion es `content[char_start:char_end]`. Se puede porque el
    contenido de un documento solo CRECE por append (memory-end-session.py
    hace `content + block`): el `char_start` de todas las secciones y el
    `char_end` de las no-finales no se mueven.

    Matiz: el `char_end` de la ULTIMA seccion si avanza, porque absorbe lo que
    se agregue antes del proximimo heading. Eso es correcto (ese texto
    pertenece a la ultima seccion), pero significa que el body de la ultima
    seccion puede crecer sin que cambie su `char_start`.

    El rango horario se SACA del titulo: asi "Session End - workspace" agrupa
    aunque cada instancia tenga horas distintas.
    """
    if not text:
        return []

    lines = text.split("\n")
    offsets = []
    p = 0
    for line in lines:
        offsets.append(p)
        p += len(line) + 1  # +1 por el newline
    total = len(text)

    # Headings de nivel >= 2 marcan secciones. El h1 titula el documento.
    marks = []
    for i, line in enumerate(lines):
        m = H_ANY.match(line)
        if m and len(m.group(1)) >= 2:
            marks.append((i, len(m.group(1)), m.group(2).strip()))

    def body_start_after(line_idx):
        end = offsets[line_idx] + len(lines[line_idx]) + 1
        return min(end, total)

    sections = []

    # Preambulo: contenido antes del primer ##, si tiene cuerpo real.
    if marks:
        first = marks[0][0]
        # si la primera linea es un h1, el preambulo arranca despues de el
        pre_start = 0
        if lines and H_ANY.match(lines[0]) and len(H_ANY.match(lines[0]).group(1)) == 1:
            pre_start = body_start_after(0)
        pre_end = offsets[first]
        if pre_end > pre_start and text[pre_start:pre_end].strip():
            sections.append(
                {
                    "level": 1,
                    "title": "",
                    "char_start": pre_start,
                    "char_end": pre_end,
                    "time_start": None,
                    "time_end": None,
                }
            )

    for idx, (i, lvl, raw_title) in enumerate(marks):
        start = body_start_after(i)
        end = offsets[marks[idx + 1][0]] if idx + 1 < len(marks) else total
        if start > end:
            start = end
        ts, te = _time_range(raw_title)
        sections.append(
            {
                "level": lvl,
                "title": clean_title(raw_title),
                "char_start": start,
                "char_end": end,
                "time_start": ts,
                "time_end": te,
            }
        )

    return sections


def extract_checklist(text: str):
    """Items de checklist embebidos, con la seccion a la que pertenecen.

    Los checkboxes viven dentro del markdown y nunca llegaron a la tabla
    `todos`: hoy hay 67 abiertos que no aparecen en ningun listado. Esto los
    hace consultables conservando su origen.
    """
    items = []
    current_section = ""
    for line in text.split("\n"):
        h = H_ANY.match(line)
        if h and len(h.group(1)) >= 2:
            current_section = _strip_time_range(h.group(2).strip())
            continue
        m = CHECKBOX.match(line)
        if m:
            items.append(
                {
                    "section": current_section,
                    "done": 1 if m.group(1).lower() == "x" else 0,
                    "text": m.group(2).strip(),
                }
            )
    return items


if __name__ == "__main__":
    import sys

    sample = """# 2026-09-22

## Cambio de config (01:41 - 01:46)

Aplicado el cambio.

- [ ] Verificar el resultado
- [x] Backup hecho

### Detalle

Texto de detalle.
"""
    assert doc_kind(sample) == "daily"
    assert doc_kind("# Session: x\n\n- **Session Key**: abc") == "harness"

    secs = split_sections(sample)
    # El h1 no es una seccion (solo titula el documento): quedan los 2 headings.
    assert len(secs) == 2, secs
    assert secs[0]["title"] == "Cambio de config"
    assert secs[0]["time_start"] == "01:41" and secs[0]["time_end"] == "01:46"
    assert secs[1]["title"] == "Detalle" and secs[1]["level"] == 3

    # Los offsets deben reconstruir el body desde el texto del padre.
    for s in secs:
        body = sample[s["char_start"]:s["char_end"]]
        assert body.strip(), f"body vacio para {s['title']!r}"
    assert "Aplicado el cambio" in sample[secs[0]["char_start"]:secs[0]["char_end"]]
    assert "Texto de detalle" in sample[secs[1]["char_start"]:secs[1]["char_end"]]

    items = extract_checklist(sample)
    assert len(items) == 2, items
    assert items[0]["done"] == 0 and items[1]["done"] == 1
    assert items[0]["section"] == "Cambio de config"

    hf = harness_fields("# Session: x\n\n- **Session Key**: agent:main:x\n- **Session ID**: abc\n- **Source**: webchat")
    assert hf == {"session_key": "agent:main:x", "session_id": "abc", "source": "webchat"}

    print("content-parse: OK")
    sys.exit(0)
