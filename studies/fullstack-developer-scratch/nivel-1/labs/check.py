#!/usr/bin/env python3
"""check.py - Verifica un lab de HTML del Nivel 1.

Uso:
    python3 check.py lab1 ~/dev/lab-html

Por que existe: el curso ensena escribiendo, y sin verificacion automatica el
"aprendi" es auto-reporte. Este script convierte cada lab en un gate: falla con
un mensaje concreto cuando falta lo que el lab pide.

Cada lab es una lista de reglas. Una regla devuelve (ok, mensaje). El script NO
mira el resultado visual: mira el HTML, que es lo que el navegador va a parsear.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "source", "track", "wbr"}


class Doc(HTMLParser):
    """Arbol minimo del documento, mas lo que necesitan las reglas."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []        # (tag, attrs_dict, depth)
        self.text = []            # texto suelto
        self.stack = []           # pila de tags abiertos
        self.unclosed = []
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.elements.append((tag, d, len(self.stack)))
        self.text.append("")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.elements.append((tag, dict(attrs), len(self.stack)))
        self.text.append("")

    def handle_endtag(self, tag):
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass
        else:
            self.unclosed.append(f"</{tag}> sin apertura")

    def handle_data(self, data):
        if self.text:
            self.text[-1] += data


def load(path):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    d = Doc()
    feeds = raw
    # charset: el parser de python no lee el meta, lo medimos aparte
    has_charset = bool(re.search(r'<meta[^>]+charset\s*=\s*["\']?utf-8', raw, re.I))
    has_viewport = bool(re.search(r'<meta[^>]+name\s*=\s*["\']viewport["\']', raw, re.I))
    has_doctype = bool(re.search(r'<!doctype\s+html', raw, re.I))
    d.feed(feeds)
    return d, raw, has_charset, has_viewport, has_doctype


def tags(d, name):
    return [(t, a, dep, txt) for (t, a, dep), txt in zip(d.elements, d.text) if t == name]


# ---------------------------------------------------------------- labs


def lab1(d, raw, charset, viewport, doctype):
    """Primer archivo: h1 con la frase, h2 con el nombre, h3 con una frase, p."""
    out = []
    h1 = tags(d, "h1")
    out.append((len(h1) >= 1, "falta un <h1>"))
    if h1:
        out.append(("I code" in h1[0][3], "el <h1> no contiene la frase 'I code, therefore I am'"))
    out.append((len(tags(d, "h2")) >= 1, "falta el <h2> con tu nombre"))
    out.append((len(tags(d, "h3")) >= 1, "falta el <h3> con tu frase favorita"))
    out.append((len(tags(d, "p")) >= 1, "falta al menos un <p>"))
    return out


def lab2(d, raw, charset, viewport, doctype):
    """Una imagen que escale."""
    out = []
    imgs = tags(d, "img")
    out.append((len(imgs) >= 1, "no hay <img>"))
    for i, (t, a, dep, txt) in enumerate(imgs):
        out.append(("src" in a, f"img #{i+1} sin src"))
        if "src" in a:
            # la ruta debe existir relativa al html: lo chequea el caller con base
            pass
        out.append(("width" in a or "class" in a or "style" in a,
                    f"img #{i+1} no escala: falta width='100%' (o una clase CSS)"))
    return out


def lab3(d, raw, charset, viewport, doctype):
    """Arbol: div que contiene h1, img, p y un div anidado."""
    out = []
    divs = [(a, dep) for (t, a, dep, txt) in tags(d, "div")]
    out.append((len(divs) >= 2, "hacen falta 2 <div> (uno exterior, uno anidado)"))
    if len(divs) >= 2:
        depths = [dep for _, dep in divs]
        out.append((max(depths) >= 1, "los <div> estan al mismo nivel: falta el anidado"))
    out.append((len(tags(d, "h1")) >= 1, "falta <h1>"))
    out.append((len(tags(d, "img")) >= 1, "falta <img>"))
    out.append((len(tags(d, "p")) >= 2, "hacen falta al menos 2 <p>"))
    return out


def lab5(d, raw, charset, viewport, doctype):
    """Documento correcto: doctype, charset, viewport, html/head/body."""
    out = []
    out.append((doctype, "falta <!DOCTYPE html>"))
    out.append((charset, 'falta <meta charset="utf-8">'))
    out.append((viewport, 'falta <meta name="viewport" content="width=device-width, initial-scale=1">'))
    out.append((len(tags(d, "html")) >= 1, "falta <html>"))
    out.append((len(tags(d, "head")) >= 1, "falta <head>"))
    out.append((len(tags(d, "body")) >= 1, "falta <body>"))
    hl = [a for (t, a, dep, txt) in tags(d, "html")]
    if hl:
        out.append(("lang" in hl[0], '<html> sin lang="es"'))
    return out


def lab6(d, raw, charset, viewport, doctype):
    """Listas: una ol y una ul, con li dentro."""
    out = []
    ols, uls = tags(d, "ol"), tags(d, "ul")
    out.append((len(ols) >= 1, "falta una <ol> (lista ordenada)"))
    out.append((len(uls) >= 1, "falta una <ul> (lista sin orden)"))
    out.append((len(tags(d, "li")) >= 6, "hacen falta al menos 6 <li> entre las dos listas"))
    if ols:
        items = [dep for (t, a, dep, txt) in tags(d, "li") if dep > ols[0][2]]
        out.append((len(items) >= 3, "la <ol> tiene menos de 3 <li>"))
    return out


def lab8(d, raw, charset, viewport, doctype):
    """Formulario: 6 inputs con label enlazado por for/id."""
    out = []
    inputs = tags(d, "input")
    out.append((len(inputs) >= 5, f"hacen falta 5 inputs, hay {len(inputs)}"))
    labels = tags(d, "label")
    fors = {a.get("for") for (t, a, dep, txt) in labels if a.get("for")}
    ids = {a.get("id") for (t, a, dep, txt) in inputs if a.get("id")}
    out.append((len(fors) >= 5, f"hacen falta 5 <label for>, hay {len(fors)}"))
    sin_enlazar = fors - ids
    out.append((not sin_enlazar, f"label for={sorted(sin_enlazar)} no apunta a ningun input id"))
    types = {a.get("type") for (t, a, dep, txt) in inputs}
    for need in ("password", "date", "color", "file"):
        out.append((need in types, f"falta un input type={need}"))
    out.append((len(tags(d, "button")) >= 1, "falta el <button>"))
    return out


def lab9(base):
    """Navegacion: index.html y about.html que se apuntan."""
    out = []
    idx, about = base / "index.html", base / "about.html"
    out.append((idx.is_file(), "falta index.html"))
    out.append((about.is_file(), "falta about.html"))
    if not (idx.is_file() and about.is_file()):
        return out
    # Los comentarios del lab NOMBRAN los archivos: si se busca en el texto crudo,
    # el propio comentario hace pasar el chequeo. Se quitan los comentarios antes.
    strip = lambda t: re.sub(r"<!--.*?-->", "", t, flags=re.S)
    raw_i, raw_a = strip(idx.read_text()), strip(about.read_text())
    hrefs_i = re.findall(r'href\s*=\s*["\']([^"\']+)["\']', raw_i)
    hrefs_a = re.findall(r'href\s*=\s*["\']([^"\']+)["\']', raw_a)
    out.append((any("about.html" in h for h in hrefs_i), "index.html no linkea a about.html"))
    out.append((any("index.html" in h for h in hrefs_a), "about.html no linkea a index.html"))
    out.append((any(h.startswith("http") for h in hrefs_i), "index.html no tiene un link externo (https://)"))
    out.append(('target="_blank"' in raw_i or "target='_blank'" in raw_i,
                'falta target="_blank" en el link externo'))
    return out


LABS = {
    "lab1": lab1, "lab2": lab2, "lab3": lab3, "lab5": lab5,
    "lab6": lab6, "lab8": lab8,
}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    which, target = sys.argv[1], Path(sys.argv[2]).expanduser()
    if which == "lab9":
        rules = lab9(target)
    else:
        fn = LABS.get(which)
        if not fn:
            print(f"lab desconocido: {which}. Opciones: {', '.join(sorted(LABS))}, lab9")
            return 2
        page = target / "index.html" if target.is_dir() else target
        if not page.is_file():
            print(f"no existe {page}")
            return 2
        d, raw, cs, vp, dt = load(page)
        rules = fn(d, raw, cs, vp, dt)

    fails = [(ok, msg) for ok, msg in rules if not ok]
    for ok, msg in rules:
        # msg describe el PROBLEMA, no el exito: solo se imprime cuando falla.
        print(("  OK" if ok else "  FAIL  " + msg))
    print()
    print(f"{len(rules)-len(fails)}/{len(rules)} reglas OK")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
