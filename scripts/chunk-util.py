#!/usr/bin/env python3
"""
chunk-util.py - Corte de texto en chunks, compartido.

Por que existe: `rechunk-vectors.py` (que genera los chunks) y `memory-search.py`
(que los muestra) tienen que cortar IGUAL. Si divergen aunque sea un caracter, el
texto que se muestra no seria el que se vectorizo, y la busqueda mentiria en
silencio sobre su propio contenido.

La primera version tenia estas funciones duplicadas en los dos scripts. Es el
mismo error que venimos corrigiendo: dos fuentes para un mismo dato. Una sola.

Uso:
    from chunk_util import split_large, strip_harness_header, chunk_text

    pieces = split_large(cuerpo)            # list[str]
    texto  = chunk_text("Titulo", piece)    # "## Titulo\\n\\n piece"
"""
import re

# Tamano objetivo de un chunk. La mediana de las unidades de tema es 1121 chars,
# asi que 1800 deja entrar la mayoria sin partir y solo divide las grandes.
MAX_CHARS = 1800
# Solape al partir una unidad grande: una idea que cae justo en el corte se
# encuentra desde los dos lados.
OVERLAP = 200
# Un chunk mas corto que esto no aporta contexto util.
MIN_CHARS = 120


def split_large(text, max_chars=MAX_CHARS, overlap=OVERLAP):
    """Parte un texto largo en fronteras de PARRAFO, nunca a mitad de palabra.

    Si un parrafo solo ya pasa el limite, se parte por oraciones; si tampoco,
    por palabras. El orden importa: se prefiere la frontera mas natural posible.
    """
    if len(text) <= max_chars:
        return [text]

    paras = [p for p in text.split("\n\n") if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if len(p) > max_chars:
            if cur.strip():
                chunks.append(cur.strip())
                cur = ""
            sentences = [s for s in p.replace("\n", " ").split(". ") if s.strip()]
            sc = ""
            for s in sentences:
                if len(sc) + len(s) + 2 <= max_chars:
                    sc = f"{sc}. {s}" if sc else s
                else:
                    if sc.strip():
                        chunks.append(sc.strip())
                    sc = s
            if sc.strip():
                chunks.append(sc.strip())
            continue

        if len(cur) + len(p) + 2 <= max_chars:
            cur = f"{cur}\n\n{p}" if cur else p
        else:
            if cur.strip():
                chunks.append(cur.strip())
            cur = (cur[-overlap:] + "\n\n" + p) if cur.strip() else p

    if cur.strip():
        chunks.append(cur.strip())
    return chunks


def strip_harness_header(text):
    """Saca la cabecera de metadata que el harness pone al inicio.

        # Session: 2026-08-29 23:45:25 GMT-3
        - **Session Key**: agent:main:main
        - **Session ID**: e91165bc...
        - **Source**: ...

    Es metadata de la sesion, no contenido: vectorizarla hace que la busqueda
    encuentre sesiones por su uuid. Medido: era 15% de los chunks viejos.
    """
    t = re.sub(r"^#\s*Session:.*$\n?", "", text or "", count=1, flags=re.M)
    t = re.sub(
        r"^\s*[-*]\s*\*\*(Session Key|Session ID|Source)\*\*:.*$", "", t, flags=re.M
    )
    return t.strip()


def chunk_text(title, piece):
    """El texto final de un chunk: el titulo adelante, despues el cuerpo.

    El titulo es lo que da contexto: un fragmento que empieza en "should be
    archived to..." no dice de que habla; con "## Configuracion OpenClaw VPS"
    adelante, si.
    """
    return f"## {strip_harness_header(title)}\n\n{piece}"


def chunks_for(title, body):
    """Todos los chunks de una unidad, ya con el titulo al frente.

    Los pedazos que no llegan a MIN_CHARS se descartan: no aportan contexto.
    """
    return [
        chunk_text(title, p) for p in split_large(body) if len(chunk_text(title, p)) >= MIN_CHARS
    ]
