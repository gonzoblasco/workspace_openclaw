#!/usr/bin/env python3
"""
check-observability-gaps.py — gate de «paso 4» del curso de system design.

De dónde sale este gate (studies/system-design-interview-guide):
  El curso llama al monitoreo «a strong signal that you think like a senior
  engineer» (0:18:11) y pone en el checklist del paso 4: SPOFs con fallback, y
  latencia/errores/umbrales que disparan alertas. Es la etapa que se olvida.

Qué mide, sobre un servicio que expone estado operativo:
  1. saturación  — scans activos contra un máximo
  2. cola        — cuántos esperan: un servicio que encola y no muestra la cola
                   no distingue «ocupado» de «saturado»; es el SPOF silencioso
  3. latencia    — p50/p95 o duración por request, no sólo un acumulado
  4. umbral      — un número explícito contra el cual alertar

Dos versiones anteriores de este gate fallaron, y las dos fallas son la razón
por la que ahora exige lo siguiente:

  v1  pasó en verde porque «waiting» aparecía en un comentario que explicaba el
      flapping de un banner de cookies. Un gate que se satisface con prosa mide
      cero. -> ahora se descartan los comentarios.

  v2  pasó en verde porque `'queued'` aparecía en `status: 'queued' | ...`, un
      type literal que NUNCA se asigna y cuya interfaz (`ScanJob`) no usa
      nadie. El nombre de una señal no es la señal. -> ahora la señal tiene que
      llegar a una respuesta HTTP (json(...) o res.write/end), que es donde un
      operador realmente la puede leer.

Uso:
    python3 check-observability-gaps.py <ruta-del-repo>
Sale 0 si las cuatro señales alcanzan una respuesta, 1 si alguna no.
"""
import re
import sys
from pathlib import Path

# (nombre, patrón de la señal, por qué importa)
GATES = [
    ("saturación", r"activeScans|inflight|inFlight", "scans activos contra el máximo"),
    ("cola", r"queued|queueDepth|waiters\.length|pendingCount", "quién espera detrás del límite"),
    ("latencia", r"\bp95\b|\bp99\b|percentile|latencyMs|durationMs|elapsedMs", "cuánto tarda un request"),
    ("umbral", r"\bthreshold\b|maxConcurrent|\bSLO\b|alertAt", "el número contra el que se alerta"),
]

CODE_EXTS = {".ts", ".tsx", ".js", ".mjs", ".go", ".py", ".rs", ".rb"}
# la señal tiene que atravesar una respuesta al cliente
EMIT = re.compile(r"\bjson\s*\(|res\.write|\bres\.end\(|NextResponse\.json|JSONResponse|jsonify|write\(|print\(")


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    text = re.sub(r"(?m)^\s*//.*$", "", text)
    text = re.sub(r"(?m)\s+#.*$", "", text)
    text = re.sub(r"(?m)^\s*\*.*$", "", text)
    return text


def scan(repo: Path):
    files = [
        p for p in repo.rglob("*")
        if p.suffix in CODE_EXTS
        and not ({"node_modules", ".next", "vendor", "dist"} & set(p.parts))
    ]
    gates = {}
    for name, pat, why in GATES:
        found, reachable = [], []
        for f in files:
            try:
                text = strip_comments(f.read_text(errors="ignore"))
            except OSError:
                continue
            if not re.search(pat, text):
                continue
            found.append(f"{f.relative_to(repo)}")
            # la señal cuenta sólo si su archivo emite hacia un cliente y la
            # línea de la señal no es una declaración de tipo pura
            for m in re.finditer(pat, text):
                line_start = text.rfind("\n", 0, m.start()) + 1
                line = text[line_start: text.find("\n", m.start())]
                if re.match(r"\s*\w+\??\s*:\s*'", line):  # type literal: no es señal
                    continue
                if EMIT.search(text):
                    reachable.append(f"{f.relative_to(repo)}:{text[:m.start()].count(chr(10))+1}")
                    break
        gates[name] = (found, reachable, why)
    return gates, len(files)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    repo = Path(sys.argv[1]).resolve()
    if not repo.is_dir():
        print(f"not a directory: {repo}")
        return 2

    gates, nfiles = scan(repo)
    print(f"repo: {repo}")
    print(f"archivos de código: {nfiles} (comentarios descartados, type literals descartados)\n")

    missing = 0
    for name, (found, reachable, why) in gates.items():
        if reachable:
            print(f"  OK      {name:<11} {reachable[0]:<34} ({why})")
        elif found:
            print(f"  PARCIAL {name:<11} aparece en {found[0]} pero no llega a una respuesta")
            missing += 1
        else:
            print(f"  FALTA   {name:<11} {why}: sin señal")
            missing += 1

    print()
    if missing:
        print(f"RESULTADO: {missing} de {len(GATES)} señales no son observables.")
        print("El paso 4 queda incompleto: sin cola publicada y sin umbral, la")
        print("saturación se descubre cuando el cliente ya la reporta.")
        return 1
    print(f"RESULTADO: las {len(GATES)} señales alcanzan una respuesta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
