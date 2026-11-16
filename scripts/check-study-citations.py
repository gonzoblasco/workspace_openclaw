#!/usr/bin/env python3
"""check-study-citations.py - gate de citas de las clases de `studies/`.

Promovido desde `studies/cs50-ai-python/heldout.py` el 2026-11-12, tras siete
usos reales en un día (los siete módulos del curso CS50 AI). Ver
`studies/cs50-ai-python/ADOPCION.md` para la evidencia de adopción.

La idea es la del Módulo 5 del curso: un modelo se evalúa sobre datos que NO vio.
Una clase (`outline.md` / `modulo-*.md` / `practica-*.md`) cita el transcript del
video, y el transcript es el corpus con el que NO se escribió la clase. Si una
cita no existe literalmente o su timestamp no es el inicio del bloque que la
contiene, la clase no es auditable.

Qué verifica
------------
1. Cada cita `"texto"` con `(h:mm:ss)` o `(mm:ss)` existe literalmente en el
   transcript (con los espacios normalizados, no con paráfrasis).
2. El timestamp es el del bloque del transcript que CONTIENE la cita, con una
   tolerancia de `MAX_CUE_SPAN` segundos hacia adelante.

Códigos de salida (ver `skills/verification-gates`)
---------------------------------------------------
    0  todos los casos corrieron y pasaron
    1  algún caso corrió y falló
    3  no se pudo correr (faltan archivos, no hay citas, formato no soportado)
       - NO es verde. Un gate que devuelve 0 sin haber mirado es peor que ninguno.

Uso
---
    # una clase
    python3 scripts/check-study-citations.py studies/<slug>/outline.md \\
                                                studies/<slug>/transcripcion.md

    # un directorio de clase: autodetecta transcript y verifica todas las clases
    python3 scripts/check-study-citations.py studies/<slug>

    # todo el catálogo
    python3 scripts/check-study-citations.py --all [--verbose]

    # arreglar los timestamps corridos por tabla de offsets (no a mano)
    python3 scripts/check-study-citations.py --all --fix

Nota de implementación (el bug que costó tiempo)
------------------------------------------------
El cue que contiene una cita NO se obtiene contando `[` en el texto unido: ese
conteo devuelve el cue SIGUIENTE, porque el `[` del cue de la cita ya se contó al
llegar a su posición. Hay que recorrer los cues con sus longitudes acumuladas y
quedarse con el primero cuyo rango `[pos, pos+len+1)` contiene el offset. La
primera versión de `heldout.py` tenía exactamente ese error y marcaba TS-DIFF en
las 15 citas de una clase que estaba bien.
"""
import argparse
import re
import sys
from pathlib import Path

# Un bloque del transcript agrupado dura a lo sumo ~18 s. Tolerar 8 s cubre una
# cita tomada de la segunda línea de un bloque sin aceptar una cita 15 s corrida
# (que es el error de conversión real que este gate cazó en `ai-engineer-full-course`).
MAX_CUE_SPAN = 8
# Tolerancia hacia ATRÁS: algunos transcripts citan el cue donde ARRANCA la idea
# (la línea previa del caption), no donde empieza la oración citada. 5 s es una
# línea de caption; 15 s es el desfasaje de conversión real que hay que cazar.
MAX_CUE_BACK = 5

CUE_RE = re.compile(r'^\s*\*{0,2}\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?\*{0,2}')
# [^\"] cita entre comillas rectas, con timestamp entre paréntesis después.
QUOTE_RE = re.compile(r'"([^"]{12,})"\s*\((\d{1,2}:\d{2}(?::\d{2})?)\)')

# Archivos de una clase que se verifican cuando se pasa un directorio.
CLASS_FILES = ('outline.md', 'modulo-*.md', 'practica-*.md')
TRANSCRIPT_NAMES = ('transcripcion.md',)


class NotVerifiable(Exception):
    """La clase existe pero este gate no puede verificar su formato."""


def strip_cue(line):
    """Texto del bloque sin su timestamp. Las citas se comparan contra esto."""
    m = CUE_RE.match(line)
    return line[m.end():].strip() if m else line.strip()


def load(path):
    p = Path(path)
    if not p.exists():
        raise SystemExit(_err(f'no se pudo leer {p}: no existe'))
    text = p.read_text(encoding='utf-8')
    if not text.strip():
        raise SystemExit(_err(f'{p} está vacío'))
    return text


def _err(msg):
    print(f'ERROR {msg}', file=sys.stderr)
    return 3


def parse_cues(transcript):
    """Devuelve [(start_seconds, start_str, line)] de los bloques con timestamp."""
    cues = []
    for line in transcript.split('\n'):
        m = CUE_RE.match(line)
        if m:
            cues.append((to_seconds(m.group(1)), m.group(1), line))
    return cues


def to_seconds(ts):
    parts = [int(x) for x in ts.split(':')]
    if len(parts) == 2:
        parts = [0] + parts
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def fmt_seconds(s):
    h, rem = divmod(int(s), 3600)
    m, sec = divmod(rem, 60)
    return f'{h}:{m:02d}:{sec:02d}' if h else f'{m}:{sec:02d}'


def find_cue(cues, offset, joined):
    """Cue que CONTIENE `offset` en `joined` (los cues unidos por un espacio).

    Recorre longitudes acumuladas. NO cuenta `[`: ese conteo adelanta un cue.
    """
    pos = 0
    for start, ts, _ in cues:
        nxt = pos + len(_line_of(ts, joined)) + 1
        if pos <= offset < max(nxt, pos + 1):
            return start, ts
        pos = nxt
    return None


def _line_of(ts, joined):
    """No se usa: el recorrido real va por longitudes de las líneas originales."""
    return ''


def build_index(cues):
    """[(start_pos, end_pos, start_seconds, ts_str)] sobre los cues unidos.

    IMPORTANTE: el texto que se indexa es el de `strip_cue()` normalizado, y
    `normalize()` colapsa espacios. Por eso la longitud de cada bloque indexado
    tiene que ser la del MISMO texto normalizado, no la de la línea cruda: si no,
    los offsets se desalinean y el gate marca el bloque equivocado (cazado el
    2026-11-12 sobre `sql-full-course` en el gate de la primera pasada).
    """
    idx = []
    pos = 0
    for start, ts, line in cues:
        n = len(normalize(strip_cue(line)))
        end = pos + n + 1                      # +1 por el ' ' del join
        idx.append((pos, end, start, ts))
        pos = end
    return idx


def locate(index, offset):
    for pos, end, start, ts in index:
        if pos <= offset < end:
            return start, ts
    return None


def normalize(text):
    """Normaliza para comparar: minúsculas, guion no-separador, espacios."""
    return ' '.join(text.lower().replace('\u2011', '-').split())


def verify_file(path, cues, index, joined_norm, fix=False, verbose=False):
    """Verifica (y opcionalmente corrige) un archivo de clase.

    Devuelve (total, verified, failures, changed_text). Lanza NotVerifiable si el
    archivo no tiene citas en el formato soportado.
    """
    text = load(path)
    quotes = QUOTE_RE.findall(text)
    if not quotes:
        raise NotVerifiable('el archivo no tiene citas con timestamp en el formato '
                            '"texto" (h:mm:ss)')
    if not cues:
        raise NotVerifiable('el transcript no tiene bloques con timestamp')

    failures = []
    verified = 0
    fixes = {}

    for quote, ts in quotes:
        needle = normalize(quote)
        haystack = joined_norm
        pos = haystack.find(needle)
        if pos < 0:
            failures.append((ts, f'cita no encontrada: {ts} {quote[:70]!r}'))
            continue
        # El timestamp correcto es el del bloque donde EMPIEZA la cita, no el
        # que contiene su final: una cita puede cruzar uno o más límites de bloque.
        found = locate(index, pos)
        if found is None:
            failures.append((ts, f'offset fuera de rango: {ts} {quote[:70]!r}'))
            continue
        real_start, real_ts = found
        delta = real_start - to_seconds(ts)
        if (to_seconds(ts) - MAX_CUE_BACK <= real_start
                <= to_seconds(ts) + MAX_CUE_SPAN):
            verified += 1
            continue
        if fix:
            fixes[(quote, ts)] = real_ts
            verified += 1
            if verbose:
                print(f'  FIX  {ts} -> {real_ts}  {quote[:50]!r}')
            continue
        failures.append(
            (ts, f'timestamp fuera de su bloque: dice {ts}, el bloque empieza '
                 f'{real_ts} ({delta:+d}s): {quote[:60]!r}'))

    changed = text
    if fixes:
        for (quote, old_ts), new_ts in fixes.items():
            changed = changed.replace(f'"{quote}" ({old_ts})',
                                      f'"{quote}" ({new_ts})')
    return len(quotes), verified, failures, changed


def discover(target):
    """Devuelve [(class_file, transcript_file)] para un directorio o archivos."""
    p = Path(target)
    if p.is_file():
        return [(p, None)]
    transcripts = [p / n for n in TRANSCRIPT_NAMES if (p / n).exists()]
    if not transcripts:
        raise SystemExit(_err(f'{p} no tiene transcripcion.md'))
    transcript = transcripts[0]
    files = []
    for pattern in CLASS_FILES:
        files.extend(sorted(p.glob(pattern)))
    if not files:
        raise SystemExit(_err(f'{p} no tiene outline.md ni modulo-*.md'))
    return [(f, transcript) for f in files]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('args', nargs='*', metavar='PATH',
                    help='archivo de clase + transcript, o un directorio de clase')
    ap.add_argument('--all', action='store_true',
                    help='recorre studies/*/ y verifica cada clase')
    ap.add_argument('--fix', action='store_true',
                    help='reescribe los timestamps corridos por tabla de offsets')
    ap.add_argument('--verbose', '-v', action='store_true')
    ns = ap.parse_args(argv)

    if ns.all:
        root = Path(__file__).resolve().parent.parent / 'studies'
        targets = []
        for d in sorted(root.iterdir()):
            if not d.is_dir():
                continue
            try:
                targets.extend(discover(d))
            except SystemExit:
                continue   # directorio sin transcripcion o sin clase: se saltea
    elif len(ns.args) == 2 and Path(ns.args[0]).is_file():
        # El hook pre-commit pasa CUALQUIER .md dentro de studies/<slug>/, incluidos
        # entregables de practica (m2-modelos.md, m1-*.md) que legitimamente no
        # citan el transcript con timestamp. Si el archivo no es de clase, el gate
        # no tiene nada que verificar: SKIP con exito, no "no corrible".
        # Bug real 2026-11-16: este camino bloqueaba commits de practicas sin cita.
        target = Path(ns.args[0])
        is_class = target.name in ('outline.md', 'transcripcion.md') or \
            target.name.startswith('modulo-') or target.name.startswith('practica-')
        if not is_class:
            print(f'SKIP {target}: no es archivo de clase (no aplica)', file=sys.stderr)
            return 0
        targets = [(target, Path(ns.args[1]))]
    elif len(ns.args) == 1:
        targets = discover(ns.args[0])
    else:
        print(__doc__, file=sys.stderr)
        return 3

    total_files = 0
    failed_files = 0
    not_verifiable = 0
    total_quotes = 0
    total_verified = 0
    all_failures = []

    for class_file, transcript in targets:
        if transcript is None:
            print(f'SKIP {class_file}: no se pasó transcript', file=sys.stderr)
            not_verifiable += 1
            continue
        transcript_text = load(transcript)
        cues = parse_cues(transcript_text)
        index = build_index(cues)
        # Se comparan las citas contra el TEXTO de los bloques, sin sus timestamps:
        # una cita que cruza el final de un bloque se encontraría pegada al
        # `[h:mm:ss]` del siguiente y daría "no encontrada" con el transcript bien.
        joined_norm = normalize(' '.join(strip_cue(l) for _, _, l in cues))

        for f in [class_file] if class_file.is_file() else []:
            total_files += 1
            try:
                n, ok, fails, changed = verify_file(
                    f, cues, index, joined_norm, fix=ns.fix, verbose=ns.verbose)
            except NotVerifiable as e:
                print(f'{f.parent.name}/{f.name}: no corrible ({e})')
                not_verifiable += 1
                continue
            total_quotes += n
            total_verified += ok
            if fails:
                failed_files += 1
                all_failures.extend((f, ts, msg) for ts, msg in fails)
                print(f'{f.parent.name}/{f.name}: FALLA '
                      f'({len(fails)} de {n} citas)')
                for ts, msg in fails:
                    print(f'  FAIL {msg}')
            else:
                extra = ' (con --fix aplicado)' if ns.fix else ''
                print(f'{f.parent.name}/{f.name}: PASA ({n} citas){extra}')
            if ns.fix and changed != f.read_text(encoding='utf-8'):
                f.write_text(changed, encoding='utf-8')
                print(f'  escrito: {f}')

    print()
    print(f'archivos: {total_files} | citas: {total_quotes} | '
          f'verificadas: {total_verified} | fallidas: {len(all_failures)} | '
          f'no corribles: {not_verifiable}')
    if all_failures:
        print('RESULTADO: FALLA')
        return 1
    if total_files == 0 or not_verifiable == total_files:
        print('RESULTADO: no corrible (nada verificable)')
        return 3
    print('RESULTADO: PASA')
    return 0


if __name__ == '__main__':
    sys.exit(main())
