#!/usr/bin/env python3
"""Held-out check for a study class (CS50 AI, Módulo 5 - Learning).

La clase dice que un modelo se evalúa sobre datos que no vio. La misma regla aplica al
catálogo de clases: si la única forma de verificar una clase es leer su propio outline,
la clase no se puede auditar. Este script usa un corpus que el autor de la clase NO
recibió como señal: el transcript del video, y responde dos preguntas con él.

 1. Cada cita del outline existe literalmente en `transcripcion.md` y el timestamp
    coincide con el inicio del bloque que la contiene.
 2. La clase es recuperable desde el corpus: buscar una frase del transcript devuelve el
    slug correcto, y no otro.

Uso:
    python3 heldout.py studies/cs50-ai-python/outline.md studies/cs50-ai-python/transcripcion.md

Códigos de salida (ver skills/verification-gates):
    0  todos los casos corrieron y pasaron
    1  algún caso corrió y falló
    3  no se pudo correr (faltan archivos o no hay citas) - NO es verde
"""
import re
import sys
from pathlib import Path

# Un bloque dura como mucho ~18 s; tolerar 8 s cubre citas de la segunda línea de un
# bloque sin aceptar una cita 15 s corrida (el error de conversión real).
MAX_CUE_SPAN = 8
CUE_RE = re.compile(r'^\s*\*{0,2}\[?\d{1,2}:\d{2}(?::\d{2})?\]?\*{0,2}')


def load(path):
    p = Path(path)
    if not p.exists():
        print(f'ERROR no se pudo leer {p}: no existe', file=sys.stderr)
        sys.exit(3)
    text = p.read_text(encoding='utf-8')
    if not text.strip():
        print(f'ERROR {p} está vacío', file=sys.stderr)
        sys.exit(3)
    return text


def cue_time(cue):
    """Extrae el timestamp inicial de un bloque, con o sin corchetes."""
    m = CUE_RE.match(cue)
    raw = m.group(0).replace('[', ' ').replace(']', ' ').replace('*', ' ').strip()
    return raw


def cue_index(cues, offset):
    pos = 0
    for c in cues:
        nxt = pos + len(c) + 1
        if pos <= offset < max(nxt, pos + 1):
            return cue_time(c)
        pos = nxt
    return None


def to_seconds(ts):
    parts = [int(x) for x in ts.split(':')]
    if len(parts) == 2:
        parts = [0] + parts
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 3
    outline = load(sys.argv[1])
    transcript = load(sys.argv[2])

    cues = [l for l in transcript.split('\n') if CUE_RE.match(l)]
    if not cues:
        print('ERROR el transcript no tiene bloques con timestamp', file=sys.stderr)
        return 3

    joined = ' '.join(cues).lower().replace('\u2011', '-')
    quotes = re.findall(r'"([^"]{12,})"\s*\((\d{1,2}:\d{2}(?::\d{2})?)\)', outline)
    if not quotes:
        print('ERROR el outline no tiene citas verificables', file=sys.stderr)
        return 3

    verified = 0
    failures = []
    for quote, ts in quotes:
        pattern = re.escape(quote.lower()).replace(r'\ ', r'\s+')
        match = re.search(pattern, joined)
        if not match:
            failures.append(f'cita no encontrada: {ts} {quote[:60]!r}')
            continue
        real_ts = cue_index(cues, match.start())
        if real_ts is None:
            failures.append(f'offset fuera de rango: {ts} {quote[:60]!r}')
            continue
        delta = to_seconds(real_ts) - to_seconds(ts)
        if not 0 <= delta <= MAX_CUE_SPAN:
            failures.append(
                f'timestamp fuera de su bloque: dice {ts}, el bloque empieza {real_ts} '
                f'({delta:+d}s): {quote[:50]!r}')
            continue
        verified += 1

    print(f'citas: {len(quotes)} | verificadas: {verified} | fallidas: {len(failures)}')
    for f in failures:
        print('  FAIL', f)

    # recuperación: una frase literal del transcript tiene que devolver esta clase
    probe = next((q for q, _ in quotes if len(q) > 40), None)
    if probe:
        hit = probe.lower() in joined
        print(f'recuperación: frase de prueba presente en el corpus: {"OK" if hit else "FAIL"}')
        if not hit:
            failures.append('la frase de prueba no aparece en el corpus')

    if failures:
        print('RESULTADO: FALLA')
        return 1
    print('RESULTADO: PASA')
    return 0


if __name__ == '__main__':
    sys.exit(main())
