#!/bin/bash
# cuento.sh - Cuento en dos etapas: glm encuentra la estructura, muse la escribe.
#
# Por que dos modelos y no uno (medido 2026-11-05):
#   - glm-5.3-flash con think=low produce la mejor ESTRUCTURA: conflictos con
#     consecuencias, un reloj concreto, un giro de segundo orden. Pero a las
#     2.500 palabras se le cae la sintaxis: 23 oraciones de mas de 45 palabras,
#     "pabellon liberio" por liberiano, "cosas que no yo escribi".
#   - muse-spark-open sostiene la voz 2.500 palabras sin romperse, pero solo no
#     encuentra un conflicto con consecuencias: describe bien, decide poco.
# Separar los dos trabajos usa lo mejor de cada uno.
#
# Y resuelve el ritmo: el outline fija QUE pasa, el template de redaccion fija
# CUANTOS parrafos y de que tamano. Sin esa regla los dos modelos escriben
# bloques de 113-155 palabras promedio, uno detras del otro, sin aire.
#
# Uso:
#   cuento.sh --genero terror --tema "..." [--minimo 2200] [--maximo 2600]
#             [--out ARCHIVO] [--keep-outline] [--dry-run]
#
# Salida por stdout: el cuento. El outline y las metricas van a stderr.
#
# Exit: 0 ok, 2 uso invalido, 4 fallo una etapa.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LLM="$SCRIPT_DIR/llm.sh"
TPL="$SCRIPT_DIR/templates"
CHECK="$SCRIPT_DIR/cuento-check.py"

GENERO=""; TEMA=""; MINIMO=2200; MAXIMO=2600; OUT=""; KEEP=0; DRY=0

die() { echo "cuento.sh: $*" >&2; exit 2; }
usage() { sed -n '2,28p' "$0" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --genero) [ -n "${2:-}" ] || die "--genero necesita valor"; GENERO="$2"; shift 2 ;;
    --tema)   [ -n "${2:-}" ] || die "--tema necesita valor";   TEMA="$2";   shift 2 ;;
    --minimo) MINIMO="${2:-}"; shift 2 ;;
    --maximo) MAXIMO="${2:-}"; shift 2 ;;
    --out)    OUT="${2:-}";    shift 2 ;;
    --keep-outline) KEEP=1; shift ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) usage; exit 2 ;;
    *) die "flag desconocida: $1" ;;
  esac
done

[ -z "$GENERO" ] && die "falta --genero (terror, cf, thriller, ...)"
[ -z "$TEMA" ] && die "falta --tema"
[ -x "$LLM" ] || die "no encuentro $LLM"

if [ "$DRY" = "1" ]; then
  echo "== etapa 1: outline (glm, think=low) ==" >&2
  "$LLM" outline --show >&2
  echo "   template: $TPL/outline-cuento.md" >&2
  echo "== etapa 2: redaccion (muse, think=false) ==" >&2
  "$LLM" redaccion --show >&2
  echo "   template: $TPL/redaccion-cuento.md" >&2
  exit 0
fi

# ---------- etapa 1: el esqueleto ----------
echo "cuento.sh: etapa 1 - esqueleto (glm, ~15s)" >&2
ESQUELETO=$("$LLM" outline --template "$TPL/outline-cuento.md" \
  --var genero="$GENERO" --var minimo="$MINIMO" --var maximo="$MAXIMO" --var tema="$TEMA")

if [ -z "$ESQUELETO" ]; then
  echo "cuento.sh: la etapa 1 devolvio un esqueleto vacio" >&2
  exit 4
fi

printf '%s\n' "$ESQUELETO" | sed 's/^/  [outline] /' >&2

# ---------- etapa 2: la prosa ----------
echo "cuento.sh: etapa 2 - redaccion (muse, ~20-40s)" >&2
CUENTO=$("$LLM" redaccion --template "$TPL/redaccion-cuento.md" \
  --var genero="$GENERO" --var minimo="$MINIMO" --var maximo="$MAXIMO" \
  --var esqueleto="$ESQUELETO")

if [ -z "$CUENTO" ]; then
  echo "cuento.sh: la etapa 2 devolvio un cuento vacio" >&2
  exit 4
fi

# ---------- checks: fidelidad y ritmo ----------
# El redactor no puede renombrar el elenco: si lo hace, el outline dejo de ser
# la decision y la planificacion no vale nada. El check no frena (una omision
# puede ser legitima), pero avisa con nombre y apellido.
if [ -x "$CHECK" ] || [ -f "$CHECK" ]; then
  printf '%s\n' "$ESQUELETO" > /tmp/cuento-outline.$$.md
  printf '%s\n' "$CUENTO" > /tmp/cuento-story.$$.md
  python3 "$CHECK" /tmp/cuento-outline.$$.md /tmp/cuento-story.$$.md >&2
  rm -f /tmp/cuento-outline.$$.md /tmp/cuento-story.$$.md
fi

# ---------- salida ----------
if [ -n "$OUT" ]; then
  printf '%s\n' "$CUENTO" > "$OUT"
  if [ "$KEEP" = "1" ]; then
    printf '%s\n' "$ESQUELETO" > "${OUT%.md}-outline.md"
  fi
  echo "cuento.sh: OK -> $OUT" >&2
else
  printf '%s\n' "$CUENTO"
fi

exit 0
