#!/usr/bin/env python3
"""
check-freshness-display.py - Falla si una vista que muestra un numero derivado de una medicion
no muestra tambien cuando se midio.

Por que existe (2026-11-11, clase studies/ai-home-dashboard-observatory): en el video el
ponente construye un dashboard de casa sobre lecturas de sensores y el criterio que sostiene
todo es "si no hay una lectura fresca, el pulso se detiene" - un dato viejo presentado como
vivo miente. La misma regla aplicada al workspace: cualquier superficie que exponga un valor
capturado (un scan, un resultado de build, una metrica) tiene que declarar su antiguedad en
esa misma vista. Un numero sin fecha se lee como actual.

Que verifica: en cada vista de UI (deteccion por nombre, ver abajo), si el archivo muestra un
campo numerico derivado de una medicion (`score`, `grade`, `blocking`, `count`, `durationMs`,
`result`, `value`, `reading`), la vista debe tambien renderizar su marca de tiempo
(`scannedAt`, `createdAt`, `updatedAt`, `lastRun`, `measuredAt`, `fetchedAt`) via
`toLocaleDateString`, `Intl.DateTimeFormat`, `timeAgo`, `<time>`, `Date(`, etc.

Limitacion conocida: es un gate lexico, no de comportamiento. Detecta que el timestamp se
lea/renderice, no que sea visible para el usuario final. Sirve para que la ausencia sea
imposible, no para certificar la UI.

Las vistas de UI se detectan por nombre (page.*, component.*, view.*, ui.*, *.html, *.astro,
*.vue, *.svelte, o un archivo bajo un directorio `components/`). Un `lib/` o un `types.ts`
solo transporta el dato: un tipo no miente, una pantalla si.

Uso:
    check-freshness-display.py <ruta...>                 # reporta
    check-freshness-display.py --check <ruta...>        # exit 1 si falta la fecha
    check-freshness-display.py --check --glob '*.tsx' src
"""
import argparse
import fnmatch
import re
import sys
from pathlib import Path

TIME_FIELD = re.compile(r"\b(scannedAt|createdAt|created_at|updatedAt|updated_at|lastRun|measuredAt|fetchedAt)\b")
DERIVED_FIELD = re.compile(r"\b(score|grade|blocking|duration_ms|durationMs|readingCount|results?|findings?)\b")
RENDER_DATE = re.compile(
    r"(toLocaleDateString|toLocaleString|toISOString|Intl\.DateTimeFormat|timeAgo|relativeTime|formatDate|date-fns|<time\b|Date\()",
)
SKIP_DIRS = {"node_modules", ".next", "dist", "build", ".git", "__pycache__"}


UI_NAME = re.compile(r"(page|component|view|layout|screen|dashboard)\.", re.I)
UI_SUFFIX = {".html", ".astro", ".vue", ".svelte"}


def is_ui(f):
    if f.suffix in UI_SUFFIX:
        return True
    if "components" in f.parts:
        return True
    return bool(UI_NAME.search(f.name))


def walk(paths, glob):
    for p in paths:
        p = Path(p)
        if p.is_file():
            if is_ui(p):
                yield p
            continue
        for f in p.rglob("*"):
            if not f.is_file() or f.suffix not in {".tsx", ".ts", ".jsx", ".js", ".html", ".astro", ".vue", ".svelte"}:
                continue
            if SKIP_DIRS & set(f.parts):
                continue
            if "ui" in f.name.lower():
                continue
            if not is_ui(f):
                continue
            if fnmatch.fnmatch(f.name, glob):
                yield f


def check_file(f):
    try:
        src = f.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    if not DERIVED_FIELD.search(src):
        return None
    if TIME_FIELD.search(src) and RENDER_DATE.search(src):
        return ("ok", f)
    return ("miss", f)
    if RENDER_DATE.search(src):
        return ("ok", f)
    return ("miss", f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--glob", default="*")
    args = ap.parse_args()

    seen = set()
    ok = miss = 0
    for f in walk(args.paths, args.glob):
        if f in seen:
            continue
        seen.add(f)
        r = check_file(f)
        if not r:
            continue
        status, path = r
        if status == "ok":
            ok += 1
            print(f"ok    {path}")
        else:
            miss += 1
            print(f"MISS  {path}  <- muestra un dato medido sin declarar cuando se midio")

    print(f"\n{ok + miss} vistas revisadas, {miss} sin fecha  (ok={ok})")
    if args.check and miss:
        print("FALLA: una vista con dato medido tiene que declarar cuando se midio.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
